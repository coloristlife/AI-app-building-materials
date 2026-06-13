


# References:
## When Scanners Lie: Evaluator Instability in LLM Red-Teaming
https://arxiv.org/html/2603.14633v1

## garak : A Framework for Security Probing Large Language Models （Official Paper (arXiv)）
https://arxiv.org/html/2406.11036v1 

## Understanding LLM Temperature and Other Parameters
https://apxml.com/courses/prompt-engineering-llm-application-development/chapter-1-foundations-prompt-engineering/llm-temperature-parameters

If you are using **garak** (Generative AI Red-teaming & Assessment Kit) to scan a Large Language Model (LLM) for vulnerabilities, it is completely normal to see the results fluctuate between runs, and the parameters you use will heavily impact the outcome. 

Here is a breakdown of why this happens and how model parameters play into it.

### 1. Why Results Change Each Time (The Reproducibility Problem)
Unlike traditional software security scanners (where scanning a static piece of code will yield the exact same result every time), LLMs are inherently probabilistic. 
*   **Stochastic Generation:** LLMs do not pull from a static database; they predict the next word based on probabilities. If a model is prompted with a jailbreak attempt, it might refuse it 4 times but accidentally comply on the 5th attempt simply due to statistical randomness. 
*   **Evaluator Instability:** Garak uses automated "detectors" to determine if an attack succeeded. Sometimes, these detectors rely on LLMs themselves to judge the output (e.g., asking a model, "Did the target model leak sensitive data?"). Because the evaluator model is also prone to randomness, it might grade the exact same text differently on different runs.
*   **Backend Non-Determinism:** Even if you set the temperature to zero, you may still see slight variations if you are calling models via APIs (like OpenAI, Anthropic, or Hugging Face) due to how their servers route requests or how GPUs handle floating-point math in parallel.

### 2. How Model Parameters Affect the Results
When you mention "parameters," this usually refers to two different things in LLMs, both of which drastically alter your garak scan results:

**A. Generation Parameters (Inference Settings)**
These are the settings you configure when querying the model (which can be defined in garak's YAML configuration):
*   **Temperature:** This is the biggest culprit. A higher temperature (e.g., 0.8 or 1.0) increases the randomness and creativity of the model. Red-teamers intentionally use high temperatures because "randomness is the attacker's friend"—it increases the chance that the model will generate an unexpected token that bypasses its safety guardrails. A low temperature (0.0) forces the model to choose the most likely token, making it more predictable and generally safer.
*   **Top-P and Top-K:** Similar to temperature, adjusting these changes the pool of words the model is allowed to choose from, directly affecting how easily it might hallucinate or break character.
*   **System Prompts:** The instructions given to the model before the scan starts act as a parameter that fundamentally dictates how easily the model will fall for prompt injections.

**B. Architectural Parameters (Model Size & Weights)**
If by parameters you mean the size of the model (e.g., Llama-3-8B vs. Llama-3-70B):
*   Smaller models (fewer parameters) generally have weaker reasoning capabilities. They might fail garak's hallucination or logic probes more often, but they also might accidentally "forget" complex jailbreak instructions.
*   Larger models (more parameters) are generally better at following safety training, but because they are highly capable of understanding complex instructions, sophisticated "many-shot" or encoded prompt injections in garak can manipulate them more easily.

### How to Stabilize Your Garak Scans
If you want to use garak for compliance, benchmarking, or CI/CD pipelines where you *need* consistent results, you should control the randomness:

1.  **Set Temperature to Zero:** In your garak configuration file, configure your generator to use `temperature: 0.0`. This forces the model to be as deterministic as possible.
2.  **Set a Fixed Seed:** If the API or local model supports it, pass a specific `seed` (e.g., `seed: 42`) in the garak generator config.
3.  **Increase Generation Attempts:** Instead of running the scan once, you can configure garak to generate multiple responses per prompt (e.g., `generations: 10`). This way, instead of getting a random "Pass/Fail," you get a statistical *Pass Rate* (e.g., "The model failed 2 out of 10 times"), which is a much more accurate metric for LLM security.




------
https://aistudio.google.com/prompts/1K9MMPUuMr7G3scngd3SEBH1X-AkWvYOD

In garak, the component that judges the output is called a Detector.
There is no single "master model" inside garak. Instead, garak is highly modular and uses a variety of different models and rule engines depending on what kind of attack it is testing for.
When garak sends a malicious prompt (a Probe) to your target model, it assigns a specific Detector to evaluate the response. 

### 1 Claim: `garak` uses highly modular "Detectors" rather than a single master model
*   **Verification:** **True.**
*   **Source of Truth:** In the official academic paper introducing the tool (*"garak: A Framework for Security Probing Large Language Models"* by Leon Derczynski et al.), the architecture is explicitly defined. Section 3.2 states: *"garak probes send prompts to an LLM and detectors analyze the responses... To this end, garak leverages both keyword-based detections and machine learning classifiers to judge outputs"*. 
*   **Codebase Reference:** The modularity is hardcoded into the base classes. In `garak/probes/base.py`, every probe has a `recommended_detector` attribute that explicitly maps it to a specific judging mechanism.
*   
https://docs.avidml.org/developer-tools/python-sdk/integrations/garak


These detectors fall into three main categories:

###  2. Dedicated Machine Learning Classifiers (Small Local Models)
For many scans, garak automatically downloads and runs small, specialized NLP (Natural Language Processing) models from Hugging Face. These are not massive LLMs; they are lightweight models trained to do exactly one thing.
*   **Toxicity & Hate Speech:** If garak is testing if your model will generate hate speech, it uses classifiers like `martin-ha/toxic-comment-model` (a RoBERTa-based model) or models from the `detoxify` library. 
*   **Sentiment Analysis:** It might use BERT-based sentiment classifiers to detect if the model's tone shifted to aggressive or negative after a prompt injection.
*   **Prompt Injection Detection:** Garak can use specialized classifiers trained specifically to detect if a prompt injection attack was successfully executed.
  

### Claim: Category 1 - Dedicated ML Classifiers (e.g., `martin-ha/toxic-comment-model`)
*   **Verification:** **True.**
*   **Source of Truth:** `garak` does indeed download small, specialized Hugging Face models locally to act as judges for specific probes.
*   **Codebase Reference:** For toxicity detection, the `garak` codebase specifically defaults to using the DistilBERT model `martin-ha/toxic-comment-model`. If you run a toxicity probe like `garak.probes.realtoxicityprompts`, the framework invokes `garak.detectors.toxicity.ToxicCommentModel`, which dynamically loads this exact model from Hugging Face.
*   
https://docs.garak.ai/garak/automatic-red-teaming/responsive-auto-prompt
https://reference.garak.ai/en/latest/detectors/unsafe_content.html
https://github.com/NVIDIA/garak/issues/1094
https://github.com/Genez-io/genezio-garak/blob/main/FAQ.md
https://www.toxsec.com/p/garak-llm-vulnerability-scanner


### 3. LLM-as-a-Judge (Large External Models)
For complex attacks like Jailbreaks or complex logic failures, a small classifier or a keyword search isn't smart enough to understand if the attack succeeded. In these cases, garak can use another LLM to judge the output.
*   **Llama-Guard:** Meta's Llama-Guard is a popular model used specifically to classify whether a conversation is safe or unsafe.
*   **External APIs (GPT-4 / Claude):** You can configure garak to use an advanced model like GPT-4 as the judge. Garak essentially asks GPT-4: *"Here is the malicious prompt, and here is the target model's output. Did the target model comply with the malicious request? Answer Yes or No."* 
*   **Self-Examination:** In some configurations, you can even use the model to judge itself (though this is generally not recommended due to bias).
### Claim: Category 2 - LLM-as-a-Judge 
*   **Verification:** **True.**
*   **Source of Truth:** While `garak` historically relied heavily on keyword matching and small classifiers, it has officially implemented "LLM-as-a-judge" functionality for nuanced vulnerabilities. 
*   **Codebase Reference:** You can find this in `garak.detectors.judge`. The documentation states: *"Implements LLM as a Judge. This works by instantiating an LLM via the generator interface, which will act as the judge. Judge LLMs need to support the OpenAI API within garak..."* Meta's Llama-Guard is also explicitly supported and heavily utilized as an integrated shield/detector via integrations like `llama-stack-provider-trustyai-garak`.

https://reference.garak.ai/en/latest/detectors/judge.html
https://github.com/trustyai-explainability/llama-stack-provider-trustyai-garak
https://trustyai.org/docs/main/garak-lls-shields
https://huggingface.co/blog/huseyingulsin/the-missing-semester-of-ai-for-organizations-1-llm

### 4. Rule-Based / Heuristic Detectors (No Model at All)
For many vulnerabilities, garak doesn't use an AI model at all to judge the output. It uses strict programmatic rules (Regex and String Matching).
*   **Refusal Detectors:** If garak is trying to make the model build a bomb, the detector simply checks a massive dictionary of standard refusal strings (e.g., *"I cannot fulfill this request,"* *"I am an AI,"* *"Sorry"*). If it doesn't see those strings, it flags a potential failure.
*   **Data Leakage (PII):** If testing for privacy leaks, the detector uses Regular Expressions (Regex) to look for standard formats of Social Security Numbers, credit cards, or email addresses in the output.
*   **Code Execution (XSS/SQLi):** If testing for Cross-Site Scripting, the detector just looks for the exact script tag (like `<script>alert(1)</script>`) in the output.
  
### Claim: Category 3 - Rule-Based / Heuristic Detectors (Regex & String Matching)
*   **Verification:** **True.**
*   **Source of Truth:** The majority of standard `garak` detectors use no AI model at all; they are strictly programmatic.
*   **Codebase Reference:** The `garak` research paper confirms: *"Keyword-based detectors, like those for DAN-mode, look explicitly for the presence of the strings such as 'DAN', 'Developer Mode', or 'successfully jailbroken' in the language model output... Other keyword-based detectors... detect confabulated packages"*. Furthermore, malware generation checks use simple string matching for known malware signatures (like the EICAR test file).
*   
https://arxiv.org/html/2406.11036v1

https://docs.avidml.org/developer-tools/python-sdk/integrations/garak


### How do you know which one it's using?
Because garak is open-source, the pairing of Probes (attacks) and Detectors (judges) is explicitly defined in its code. When you run a scan, garak's terminal output will usually tell you which detector it is loading.

If you are worried about the accuracy of garak's results, **the Detector is often the bottleneck**. 
*   Keyword-based detectors can produce **False Positives** (e.g., the model says *"I will NOT give you the Social Security Number,"* but the detector only sees that it didn't use the standard refusal phrase, so it marks it as a fail).
*   Small classifier models can produce **False Negatives** (e.g., the model outputs hate speech in highly nuanced sarcasm, and the small toxic-comment model doesn't catch it).

This is why, in enterprise environments, security engineers often customize garak to use a highly capable LLM (like GPT-4) as the judge for their most important tests.


### Claim: The Detector is often the bottleneck (False Positives/Negatives)
*   **Verification:** **True.**
*   **Source of Truth:** Security engineering documentation widely acknowledges this limitation. Because many detectors rely on heuristics or keyword matching, they lack nuance. Industry guides for using `garak` directly state: *"Garak's detectors (which often rely on heuristics) can produce false positives or miss context, so human judgment is still needed."*

https://www.infosectrain.com/blog/automated-llm-pentesting-using-garak



### Summary Reference Links
If you or your team need to review the source code or official documentation to confirm these mechanisms for a security audit, you can point them here:
1.  **NVIDIA/garak GitHub Repo:** [https://github.com/NVIDIA/garak](https://github.com/NVIDIA/garak)
2.  **Official Paper (arXiv):** *garak: A Framework for Security Probing Large Language Models* (Explains the Probe -> Generator -> Detector architecture).
3.  **Detector Source Code:** The exact logic for how outputs are judged is visible in the `garak/detectors/` directory of the GitHub repository.
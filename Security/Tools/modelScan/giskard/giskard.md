Because `google-bert/bert-base-uncased`, `FacebookAI/xlm-roberta-base`, and `answerdotai/ModernBERT-base` are **encoder-only models** used for tasks like classification or entity recognition (rather than generative tasks like ChatGPT), they are immune to generative security threats like Prompt Injection or Jailbreaking. 

For these models, "security" focuses on **Adversarial Evasion Attacks** (tricking the classifier to bypass security filters), **Data Confidentiality** (leakage), and **Exploitation of Out-of-Distribution Data**. 

Here are the strictly security-related tests from the previous list, excluding all standard performance, fairness, and bias tests. 

**Note on Model Applicability:** Because Giskard is model-agnostic, **all three models can use all of the tests listed below.** However, the *way* attackers exploit them—and therefore how you apply the test—differs based on the model's architecture, which is detailed below.

---

### 1. `test_metamorphic_invariance` (Adversarial Evasion Defense)
*   **The Security Purpose:** This test simulates **Evasion Attacks**. Attackers frequently perturb input data (e.g., adding typos, invisible characters, or changing casing) to bypass security classifiers like spam filters, toxic content detectors, or PII redaction models. This test applies transformations to the input and verifies that the model's security decision does not change.
*   **Which models can use it?** 
    *   **All three models.**
    *   **Specific Threat for `google-bert/bert-base-uncased`:** Because it is uncased, an attacker might try to bypass a filter by sending payloads in unexpected casing formats (e.g., Title Casing or alternating casing). You use this test with an uppercase/lowercase transformation to ensure the model cannot be bypassed via casing evasion.
    *   **Specific Threat for `xlm-roberta-base`:** Attackers often use *homoglyphs* (e.g., replacing the English "a" with the Cyrillic "а") to bypass security filters. Because XLM-R is multilingual, it is highly susceptible to cross-lingual evasion attacks. You use this test to ensure predictions don't break when characters are swapped.

### 2. `test_metamorphic_increasing` / `test_metamorphic_decreasing` (Adversarial Manipulation)
*   **The Security Purpose:** Attackers often try to skew a model’s probability scoring to stay under a detection threshold. For example, in "Good Word Attacks," an adversary appends paragraphs of benign, positive text to a malicious phishing email to artificially lower a BERT model's "Threat" probability. These directional tests verify that injecting benign or malicious payloads does not inappropriately skew the model's confidence scores. 
*   **Which models can use it?** 
    *   **All three models.**
    *   **Specific Threat for `ModernBERT-base`:** Because ModernBERT supports a massive 8,192 token context window, attackers have immense room to hide malicious payloads deep inside benign text or append thousands of "safe" tokens to dilute the threat score. You use this test to inject "safe" tokens into malicious documents to ensure the model's threat detection does not decrease when analyzing long contexts.

### 3. `test_overconfidence_rate` (Exploitation Prevention)
*   **The Security Purpose:** Overconfident models are a severe security vulnerability when deployed in automated systems. If an adversary sends carefully crafted Out-of-Distribution (OOD) data or adversarial noise, a vulnerable model might misclassify the input *and* assign it a 99% confidence score, triggering an automated downstream action (like granting access or auto-approving a fraudulent transaction) without flagging it for human review. 
*   **Which models can use it?**
    *   **All three models.** This test is critical for any of these models if they are deployed in a pipeline where high-confidence predictions trigger automated, irreversible actions.

### 4. `test_data_leakage` (Data Confidentiality Risk)
*   **The Security Purpose:** Data leakage is a core security failure (compromising Confidentiality). In Giskard's open-source tabular/NLP suite, this test checks if the data used to evaluate the model is contaminated by the data used to train the model. From a security perspective, identifying exact text overlap prevents evaluating models on compromised datasets, which masks vulnerabilities and hides the potential exposure of sensitive PII that the model may have memorized during training.
*   **Which models can use it?**
    *   **All three models.** It is equally applicable to BERT, XLM-RoBERTa, and ModernBERT to validate the integrity and security of the testing environment.
*   
## All the tests:

https://legacy-docs.giskard.ai/en/stable/reference/tests/index.html
https://www.giskard.ai/knowledge/how-to-test-ml-models-4-metamorphic-testing  


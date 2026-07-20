



To conduct a realistic adversarial robustness test, we must simulate specific threat profiles. For sequence classification models (BERT, ModernBERT, XLM-RoBERTa), the primary security risk is **Evasion Attacks** (manipulating the input payload to force a misclassification).

Below are the three primary Threat Actor profiles you must define and map to your TextAttack recipes.

## Profile 1: The "Noisy" Evasion Adversary
*   **Who they are:** Cybercriminals, Spammers, Phishers, and Automated Botnets.
*   **Motivation:** Financial gain or malware distribution. Their goal is to bypass automated security filters (e.g., spam detection, phishing filters, hate-speech moderation) so their malicious payload reaches the human target. 
*   **Capabilities & TTPs:** They use low-sophistication, high-volume attacks. They do not care if the text looks slightly "broken" or misspelled, as long as the victim can still read it. They rely on token-breaking techniques like *l33tspeak*, character insertions, deletions, and visual homoglyphs (e.g., replacing a Latin "a" with a Cyrillic "а").
*   **Access Level:** Black-Box (They only know if their email/post was blocked or accepted).
*   **SOP Recipe Mapping:** Simulate this actor using **Character-Level Recipes**.
    *   `TextBuggerLi2018`
    *   `DeepWordBugGao2018`

## Profile 2: The Semantic Manipulator (The "Stealth" Attacker)
*   **Who they are:** Disinformation Agents, Malicious Competitors, Black-hat SEOs, and Advanced Persistent Threats (APTs).
*   **Motivation:** Reputational damage, market manipulation, or sophisticated social engineering. Their goal is to alter the classification of a document (e.g., turning a negative product review into a positive one, or evading a toxicity filter) **without raising any human suspicion.** 
*   **Capabilities & TTPs:** Highly sophisticated. The manipulated text must maintain perfect grammar, syntax, and semantics. If a human auditor reviews the text, it must look entirely benign and natural. They achieve this using context-aware synonym substitutions and masked language models to generate adversarial payloads.
*   **Access Level:** Black-Box (Querying the model API and using confidence scores to map the decision boundary).
*   **SOP Recipe Mapping:** Simulate this actor using **Word-Level / Semantic Recipes**.
    *   `TextFoolerJin2019` (For general text).
    *   `BAEGarg2019` or `BERTAttackLi2020` (For highly specialized, domain-specific text where grammar must be flawless).

## Profile 3: The Insider Threat / Supply Chain Compromise
*   **Who they are:** Disgruntled employees, compromised MLOps pipelines, or attackers who have breached your model registry (e.g., a compromised Hugging Face repository).
*   **Motivation:** Sabotage, IP theft, or implanting backdoors (Data Poisoning).
*   **Capabilities & TTPs:** They have full access to the model's architecture, training data, and gradients. They can perform gradient-based adversarial attacks to find the exact mathematical weaknesses of your specific model checkpoint. 
*   **Access Level:** White-Box (Full access to weights and gradients).
*   **SOP Recipe Mapping:** Simulate this actor using **White-Box / Gradient-based Recipes**.
    *   `HotFlipEbrahimi2017` (Uses the model's own gradients to calculate the most devastating character/word swaps).

---

### Security Engineering Checklist for the SOP:

Before initiating Phase 2 (Data Preparation), the security engineer must document the following in the test plan:

1.  [ ] **Identify the Asset:** What business logic does this NLP model control? (e.g., Auto-approving loan applications, filtering malicious emails, analyzing legal contracts).
2.  [ ] **Select the Threat Actor:** Based on the asset, who is the most likely attacker? (Choose Profile 1, 2, or 3).
3.  [ ] **Assume the Access Level:** Assume the attacker has API access returning prediction probabilities (Soft-label Black-Box). *Note: If your API only returns the final class without probabilities (Hard-label), you must restrict TextAttack to use hard-label search algorithms.*
4.  [ ] **Execute Simulation:** Proceed to Phase 4/5 of the SOP using the Recipes mapped to the selected Threat Actor.




Based on the official TextAttack recipes you provided, here is the comprehensive mapping of every recipe to the three Threat Actor profiles we defined in the SOP, along with the security rationale for each.

---

### Profile 1: The "Noisy" Evasion Adversary
**Attacker Persona:** Spammers, Phishers, Botnets.
**TTPs:** Character obfuscation, typos, l33tspeak, and token-breaking to bypass automated filters. They don't care if the text looks slightly unnatural, as long as it gets past the firewall.

**Mapped Recipes:**
*   **DeepWordBug:** The ultimate token-breaking simulator. It uses character-level perturbations (insertions, deletions, substitutions, and swapping adjacent letters) to simulate typos and adversarial obfuscation. 
*   **TextBugger:** A hybrid attack that heavily utilizes character-level manipulation. It is famous for effectively attacking deep learning systems by simulating the exact typographical errors human moderators or spam filters often miss.
*   **Pruthi2019 (Combating with Robust Word Recognition):** Specifically designed to simulate spelling mistakes (dropping characters, swapping, inserting). Highly relevant for testing if your tokenizer (like BERT's WordPiece) is resilient to noisy input.

---

### Profile 2: The Semantic Manipulator (The "Stealth" Attacker)
**Attacker Persona:** Advanced Persistent Threats (APTs), Disinformation Agents, Black-Hat SEOs.
**TTPs:** Using Machine Learning against Machine Learning. These attackers use word embeddings and Masked Language Models (MLMs) to change words while perfectly preserving the sentence's grammar and semantic meaning. Their payload must look completely benign to a human auditor.

**Mapped Recipes:**
*   **TextFooler (Is BERT Really Robust?):** The industry standard for this profile. It identifies the most important words and swaps them with semantically similar words using counter-fitting word embeddings.
*   **BAE (BERT-Based Adversarial Examples):** Extremely stealthy. It masks a word and uses a pre-trained BERT model to predict a grammatically perfect replacement that flips the classification. 
*   **BERT-Attack:** Similar to BAE, this uses BERT to generate context-aware, highly fluent substitutions. Excellent for simulating sophisticated state-sponsored disinformation bots.
*   **CLARE:** One of the most advanced stealth attacks. Instead of just replacing words, it uses a pre-trained language model to dynamically *Replace, Insert, and Merge* words, making the adversarial text incredibly difficult for humans to detect.
*   **PWWS (Probability Weighted Word Saliency):** Uses WordNet (a lexical database) to find synonyms, prioritizing words that have the highest mathematical impact on the model's confidence score.
*   **Imperceptible Perturbations Algorithm:** As the name implies, this algorithm specifically constraints the attack to ensure the perturbations remain entirely unnoticeable to human readers.
*   **A2T (Attack for Adversarial Training):** A highly efficient, fast word-substitution attack designed specifically to quickly generate stealthy payloads for adversarial training.
*   **The Heuristic Optimization Family (Alzantot, Faster Alzantot, IGA, PSO, Kuleshov2017):** 
    *   *Alzantot Genetic Algorithm / Faster Alzantot / Improved Genetic Algorithm (IGA):* These simulate an attacker using evolutionary algorithms (Genetic Algorithms) to breed the perfect, stealthy adversarial sentence over multiple generations.
    *   *Particle Swarm Optimization (PSO):* Simulates an attacker using swarm intelligence to optimize synonym substitutions.
    *   *Kuleshov2017:* Another foundational word-level synonym substitution attack.

---

### Profile 3: The Insider Threat / Supply Chain Compromise (White-Box)
**Attacker Persona:** Rogue Data Scientists, MLOps pipeline hackers.
**TTPs:** Gradient exploitation. They have breached your infrastructure and have full read-access to your model's architecture, weights, and gradients. They use advanced calculus to find the exact mathematical Achilles' heel of your model.

**Mapped Recipes:**
*   **HotFlip:** The quintessential white-box attack. Instead of guessing which words to swap, it uses the model's own gradients (directional derivatives) to calculate the exact character or word flip that will cause the maximum loss in the network. 
*   **Seq2Sick (Attacks on sequence-to-sequence models):** A highly targeted, white-box attack designed for Seq2Seq models (like translation or summarization models). It uses projected gradient descent to force the model to output specific malicious strings or completely fail to summarize.

---

### Specialized / Diagnostic Recipes (The "Auditor" Profile)
As a security engineer, you will also act as an Auditor to test the foundational logic and interpretability of the model. TextAttack includes recipes specifically for this diagnostic purpose.

**Mapped Recipes:**
*   **CheckList:** This is behavioral testing, not a malicious attack. It tests if your model is biased or brittle by applying specific templates (e.g., swapping "John" with "Mohammed", or changing "Chicago" to "Dallas") to see if the prediction changes based on protected entities.
*   **Input Reduction:** A diagnostic tool used to find the absolute minimal set of words required to trigger a classification. It iteratively removes the least important words. (e.g., An attacker might use this to find that the word "urgent" alone triggers your model, allowing them to craft a payload around it).
*   **MORPHEUS2020 (Attacks on sequence-to-sequence models):** Focuses on morphological inflections (changing the tense, plurality, or form of a word, like "run" to "running"). Often used by auditors to test the grammatical robustness of translation models.
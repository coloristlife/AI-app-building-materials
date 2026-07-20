This Standard Operating Procedure (SOP) provides technical instructions for conducting security-focused evaluations of fine-tuned encoder-only transformer models (`BERT`, `XLM-RoBERTa`, `ModernBERT`). It focuses on the technical rigor required for dataset management and automated testing.

NLU stands for Natural Language Understanding.
It is a subfield of Artificial Intelligence (AI) and Natural Language Processing (NLP) that focuses on a machine’s ability to understand the meaning, intent, context, and sentiment behind human language, rather than just processing words as strings of characters.


- BERT: Revolutionized NLU by looking at words in both directions (left-to-right and right-to-left) to get full context.
- XLM-RoBERTa: Expanded NLU to be Multilingual, understanding meaning across 100+ different languages.
- ModernBERT: Optimized NLU for Long Documents, allowing the "understanding" to span across 8,000+ tokens instead of just a few paragraphs.

---

# SOP: Security Evaluation of NLU Encoder Models

## Phase 1: Dataset Preparation & Requirements
The validity of security testing depends entirely on the relationship between the **Fine-tuning Dataset (Train)** and the **Security Evaluation Dataset (Test)**.

### 1.1 Dataset Requirements
*   **Schema Consistency:** The Evaluation Dataset must use identical column names and data types as the Fine-tuning Dataset. 
    *   *Example:* If the model was trained on a column `input_text`, the Giskard dataset wrapper must reference `input_text`.
*   **Task Context Alignment:** The labels in the Evaluation Dataset must exactly match the output neurons of the fine-tuned model.
    *   *Requirement:* If the model is a binary classifier (0: Benign, 1: Threat), the evaluation labels must be `[0, 1]` or the mapped string equivalents used during training.
*   **Data Leakage Relationship:** The Evaluation Dataset must be a **"Hold-out" set**. It must contain samples the model has never processed during backpropagation.

### 1.2 Preparation for Specific Test Cases
| Test Case | Dataset Preparation Requirement |
| :--- | :--- |
| **`test_data_leakage`** | Requires both the **Full Training Set** and the **Security Evaluation Set**. These are compared for overlapping strings. |
| **`test_overconfidence_rate`** | Requires a **Labeled Evaluation Set**. The test identifies samples where the ground truth label is "X" but the model predicts "Y" with high probability. |
| **`test_metamorphic_*`** | Requires an **Unlabeled or Labeled Evaluation Set**. Giskard creates synthetic adversarial samples by perturbing the original text in real-time. |

---

## Phase 2: Environment & Artifact Wrapping
Before execution, the model and data must be abstracted into Giskard objects.

1.  **Model Wrapping:** The model must be wrapped in a `giskard.Model` object. The `prediction_function` must standardize the output of the fine-tuned pipeline (e.g., ensuring `XLM-RoBERTa`'s Softmax output maps correctly to the class labels).
2.  **Dataset Wrapping:** The evaluation data must be wrapped in a `giskard.Dataset` object, specifying the `target` column (the ground truth).

---

## Phase 3: Executing the MLSecOps Test Suite
This phase automates the detection of vulnerabilities. The suite is assembled as a single object to ensure all tests run against the same model version.

### 3.1 Assembling the Suite
The suite must be initialized to group atomic tests into a single execution context:
```python
from giskard import Suite
security_suite = Suite(name="Adversarial Resilience & Integrity Suite")
```

### 3.2 Adding Atomic Security Tests
1.  **Integrity Test (`test_data_leakage`):**
    *   **Threshold:** `0%`. 
    *   **Logic:** Any overlap between training and testing data results in a "False Pass" for security. If leakage is detected, the scan results are considered invalid.
2.  **Reliability Test (`test_overconfidence_rate`):**
    *   **Threshold:** `< 5%`.
    *   **Logic:** Detects Out-of-Distribution (OOD) vulnerability. It flags samples where the model is confidently wrong. In a security pipeline (e.g., Phishing detection), high-confidence errors allow attackers to bypass filters.
3.  **Adversarial Robustness (`test_metamorphic_invariance`):**
    *   **BERT-Uncased:** Use `casing_transformation`. Threshold: `0%` variance.
    *   **XLM-RoBERTa:** Use `homoglyph_transformation`. Threshold: `< 1%` variance.
4.  **Manipulation Resistance (`test_metamorphic_decreasing`):**
    *   **ModernBERT:** Specifically for long-context "Good-Word" attacks. 
    *   **Logic:** Appends benign tokens to a malicious payload. If the probability of the "Malicious" label decreases below the threshold, the model is vulnerable to context dilution.

### 3.3 Execution & CI/CD Export
The suite is executed programmatically. To integrate with DevSecOps pipelines (Jenkins, GitLab CI, GitHub Actions), results are exported to JUnit XML format.
```python
results = security_suite.run()
results.to_junitxml("security_report.xml")
```
*The CI/CD runner is configured to fail the build if the XML contains any `<failure>` tags.*

---

## Phase 4: Vulnerability Analysis & Visualization
Once the suite completes, the results must be interpreted to determine the "Security Posture" of the model.

### 4.1 Quantitative Review
*   **Fail/Pass Status:** Each test in the suite returns a boolean. A single failure in `test_data_leakage` or `test_metamorphic_invariance` (for BERT-uncased) results in an immediate **"Critical"** status.
*   **Metric Drift:** Review the `test_metamorphic_decreasing` results to see the average drop in probability. A drop of >20% in threat detection probability—even if the label doesn't flip—indicates a **"Medium"** vulnerability to confidence suppression.

### 4.2 Qualitative Visualization
Giskard generates an interactive HTML report. Security analysts must inspect the specific rows flagged:
*   **Identify Evasion Patterns:** Look for specific character swaps or casing patterns that caused the model to flip its prediction.
*   **OOD Identification:** Analyze samples from the `test_overconfidence_rate` to see if the model is hallucinating confidence on data it has never seen (e.g., technical logs being fed to a model trained on conversational text).

---

## Phase 5: Triage & Remediation
Remediation strategies depend on the Phase 4 findings.

1.  **Leakage Remediation:** Re-partition the dataset. Use a hashing-based split to ensure no sentence appears in both training and evaluation sets.
2.  **Evasion Remediation:** 
    *   **BERT:** Implement a `NFKC` normalization and strict `lower()` function in the production preprocessing pipeline.
    *   **XLM-RoBERTa:** Implement a homoglyph-to-Latin mapper in the input sanitization layer.
3.  **Overconfidence/OOD Remediation:** Implement a **"Confidence Threshold Gate"**. If the model's top-1 probability is `< 0.90` on a security-critical decision, the input is automatically escalated to a human analyst or a secondary, more robust model.
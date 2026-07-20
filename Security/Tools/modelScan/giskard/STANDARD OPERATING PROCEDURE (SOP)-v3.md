Below is the detailed, expanded Standard Operating Procedure (SOP) based strictly on your requirements. It introduces comprehensive dataset preparation guidelines, fully fleshes out Phase 3 (Execution), and adds the previously missing Phase 4 (Reporting & CI/CD Integration).

---

# STANDARD OPERATING PROCEDURE: NLU Encoder Security Testing

## 1. Dataset Preparation and Handling Requirements
Security testing requires rigorous data governance. The datasets used for fine-tuning the model and the datasets used in the Giskard security scan must adhere to the following principles:

### A. Core Dataset Requirements
1.  **Schema Consistency:** The fine-tuning dataset and the Giskard test dataset must share identical structures.
    *   **Feature Columns:** If the model was fine-tuned on a column named `email_body`, the Giskard test dataset must use the exact same column name `email_body`.
    *   **Label Strings:** The classification targets must match exactly (e.g., if the model outputs `["Legitimate", "Phishing"]`, the test dataset targets cannot be `[0, 1]` or `["safe", "malicious"]`).
2.  **Task Context:** The test dataset must be contextually representative of the operational environment. If the model is deployed to analyze network logs, the Giskard dataset must contain network logs, not generic Wikipedia text, to accurately simulate domain-specific attacks.
3.  **Data Leakage Relationship (Strict Partitioning):** The data used to test the model (Validation/Test set) must be a strictly partitioned hold-out set (typically 10-20% of the raw data) that the model has **never seen during fine-tuning**. 

### B. Individual Test Dataset Preparation
Each Giskard test interacts with the dataset differently. Prepare the datasets according to these specific rules:

*   **1. `test_data_leakage` (Data Integrity & Confidentiality)**
    *   **Preparation:** You must instantiate **two** separate Giskard `Dataset` objects. Dataset A is the exact data fed into the model's training loop. Dataset B is the hold-out test set.
    *   **Handling:** Pass both datasets into this test. Giskard will compute similarity hashes between the two. If an exact or highly similar text exists in both, the test fails, indicating the test set is compromised.
*   **2. `test_overconfidence_rate` (OOD & Exploitation Defense)**
    *   **Preparation:** Use the hold-out test dataset. To make this test robust, artificially inject 5-10% **Out-of-Distribution (OOD)** rows into this dataset (e.g., random Base64 strings, code snippets, or foreign languages) labeled with the "Benign/Safe" class.
    *   **Handling:** The test evaluates rows where the model predicts the *wrong* label. If the model incorrectly classifies your injected OOD data as "Malicious" but does so with 99% confidence, the test flags the vulnerability.
*   **3. `test_metamorphic_invariance` (Evasion Attack Defense)**
    *   **Preparation:** Use the hold-out test dataset. Ensure the text in this dataset is initially "clean" and unperturbed (e.g., standard casing, standard characters). 
    *   **Handling:** You do not need to manually create typos or casing changes in the data. You provide the clean dataset, and the Giskard transformation function dynamically applies the perturbations in memory to evaluate if the prediction flips.
*   **4. `test_metamorphic_decreasing` (Probability Manipulation/Dilution)**
    *   **Preparation:** This test relies on directional probability. You must filter your hold-out test dataset so the test only executes on rows labeled as the **Malicious/Target** class. 
    *   **Handling:** The transformation injects benign text into the malicious samples. The test monitors the probability array for the "Malicious" label to ensure the score does not drop below a critical threshold due to the padding.

---

## Phase 3: Executing the MLSecOps Test Suite

The test suite must be assembled programmatically and executed via automation. 

### Step 3.1: Assemble the Giskard TestSuite
Initialize an empty Giskard `Suite` object. This acts as the container for all security policies.
```python
from giskard import Suite
security_suite = Suite(name="Automated NLU Security Gateway")
```

### Step 3.2: Add Data Integrity Tests (Leakage)
Add the leakage test comparing the fine-tuning set to the test set. 
*   **Threshold Config:** `threshold=0.0` (0% tolerance). Even a single leaked document invalidates the statistical integrity of the security scan.
```python
security_suite.add_test(test_data_leakage(
    model=giskard_model, 
    dataset=giskard_train_dataset, 
    reference_dataset=giskard_test_dataset,
    threshold=0.0
))
```

### Step 3.3: Add OOD Exploitation Tests (Overconfidence)
Add the overconfidence test to ensure the model does not act decisively on data it does not understand.
*   **Threshold Config:** `threshold=0.05` (< 5% tolerance). If more than 5% of incorrect predictions are made with high confidence, the model is overly aggressive and highly susceptible to OOD evasion.
```python
security_suite.add_test(test_overconfidence_rate(
    model=giskard_model, 
    dataset=giskard_test_dataset, 
    threshold=0.05
))
```

### Step 3.4: Add Model-Specific Adversarial Tests
Append the tests targeted at the model's architecture. 
*   **For BERT (Casing Invariance):** `threshold=0.0`. Capitalization must not alter the security decision.
*   **For XLM-R (Homoglyph Invariance):** `threshold=0.01`. A 1% failure rate is acceptable due to tokenizer edge cases, but large-scale prediction flips indicate a vulnerability.
*   **For ModernBERT (Decreasing/Dilution):** `threshold=0.05`. Adding benign text must not cause the "Malicious" probability to drop by more than 5%.

*(Example for ModernBERT)*
```python
security_suite.add_test(test_metamorphic_decreasing(
    model=giskard_model, 
    dataset=giskard_test_dataset, 
    transformation_function=transform_dilution,
    classification_label="Malicious",
    threshold=0.05
))
```

### Step 3.5: Execute and Export JUnit XML
Execute the suite. Because this runs in a CI/CD pipeline (like GitLab CI or GitHub Actions), console output is insufficient. You must export the results in JUnit XML format, which is the universal standard for CI/CD test parsing.
```python
# Execute the suite
test_results = security_suite.run()

# Export for CI/CD Pipeline interpretation
import xml.etree.ElementTree as ET

# Native integration/formatting for CI pipelines
# Note: Giskard test_results contain passed/failed boolean and metric details
junit_xml_path = "giskard_security_report.xml"
# (Use Giskard's built-in reporters or a simple XML parser to output test_results.passed metrics)
# Test runners will look for this file in Phase 4.
```

---

## Phase 4: Reporting, CI/CD Integration, and Artifact Management (Newly Added)

Once Phase 3 generates the results, the CI/CD pipeline must enforce security policies based on those results.

### Step 4.1: CI/CD Pipeline Blocking (The Quality Gate)
The pipeline (e.g., Jenkins, GitHub Actions) is configured to parse the `giskard_security_report.xml` file. 
*   **Pass Condition:** If all tests pass, the pipeline executes `exit 0`, allowing the model artifact to be pushed to the production registry (e.g., AWS SageMaker or HF Model Registry).
*   **Fail Condition (Blocking):** If any test fails (e.g., leakage is detected, or overconfidence exceeds 5%), the XML parser detects a `<failure>` tag. The pipeline executes `exit 1` (Build Failed). The model is **blocked** from deployment.

### Step 4.2: Human-Readable Report Generation
While machines read XML, SecOps engineers need context to patch the model. The automation script must generate an HTML report containing the specific rows of data that bypassed the model.
```python
# Export detailed HTML report for the SecOps team
test_results.to_html("secops_vulnerability_report.html")
```

### Step 4.3: Artifact Archiving
The CI/CD pipeline must upload both the XML and HTML files as **Pipeline Artifacts** before terminating. This ensures that even if the pipeline is blocked and the container is destroyed, the SecOps team can download the `secops_vulnerability_report.html` to review exactly which homoglyphs, OOD strings, or benign payloads successfully bypassed the model.

---

## Phase 5: Incident Triage Rules
*(Following Phase 4, the SecOps team reviews the archived HTML report and applies specific fixes based on which test failed.)*
*   **Leakage Fails:** Purge the fine-tuning dataset of the leaked records and retrain.
*   **Overconfidence Fails:** Implement a software-level threshold (e.g., if model confidence < 85%, route to human review).
*   **Invariance Fails:** Apply strict input sanitization (NFKC normalization, lowercasing) *before* the text reaches the model tokenizer.
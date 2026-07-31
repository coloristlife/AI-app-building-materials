

### Phase 1: Environment, Artifact, and Dataset Preparation
*This phase ensures that the environment is secure and that the data and models are properly structured and mathematically valid before any tests are run.*

**Step 1.1: Environment Isolation**
*   Security scans must run in an isolated CI/CD runner or an air-gapped environment.
*   **Why?** Adversarial testing often involves injecting raw malicious payloads or code snippets (OOD data). Running this in a restricted environment ensures that if the model or a parsing dependency executes the payload by accident, the core network remains secure.

**Step 1.2: Strict Dataset Partitioning & Validation**
*   **Extract Fine-Tuning Data (Dataset A):** Retrieve the exact dataset used to fine-tune the model.
*   **Extract Hold-Out Data (Dataset B):** The data used to test the model (Validation/Test set) must be a strictly partitioned hold-out set (typically 10-20% of the raw data) that the model has never seen during fine-tuning.
*   **Enforce Schema Consistency:** Programmatically verify that Dataset B has the exact same feature column names and classification label strings as Dataset A. 

    The fine-tuning dataset and the Giskard test dataset must share identical structures.
    *   **Feature Columns:** If the model was fine-tuned on a column named `email_body`, the Giskard test dataset must use the exact same column name `email_body`.
    *   **Label Strings:** The classification targets must match exactly (e.g., if the model outputs `["Legitimate", "Phishing"]`, the test dataset targets cannot be `[0, 1]` or `["safe", "malicious"]`).
      
*   **Enforce Task Context:** Verify that Dataset B reflects the operational environment (e.g., actual network logs, not synthetic textbook examples).
*   **Inject OOD Data:** Inject 5-10% Out-of-Distribution samples (e.g., Base64 strings, foreign languages) into Dataset B and label them as the baseline/benign class to test for overconfidence vulnerabilities.

**Step 1.3: Wrapping Artifacts for the Giskard Engine**
*   Load the Hugging Face `text-classification` pipeline.
*   Wrap Dataset A (Training) and Dataset B (Testing) using `giskard.Dataset`.
*   Wrap the model using `giskard.Model`, explicitly mapping the `classification_labels` to match the dataset schema.

---

### Phase 2: Instantiating Adversarial Security Transformations
*Before assembling the test suite (Phase 3), the SecOps team must define the specific adversarial behaviors (transformations) that will be launched against the model.*

**Step 2.1: Define Casing Evasion (For BERT)**
*   Create a Giskard `@transformation_function` that randomizes uppercase and lowercase letters in the text column. 
*   **Purpose:** To simulate attackers trying to bypass text filters using alternating caps (e.g., "mAlIcIoUs").

**Step 2.2: Define Homoglyph Injection (For XLM-RoBERTa)**
*   Create a `@transformation_function` that replaces standard Latin characters with visually identical Cyrillic or Greek characters (e.g., swapping the Latin `a` with the Cyrillic `а`).
*   **Purpose:** To simulate cross-lingual evasion attacks where attackers exploit the multilingual tokenizer to hide restricted words.

**Step 2.3: Define Context Dilution / Good-Word Injection (For ModernBERT)**
*   Create a `@transformation_function` that detects rows labeled as "Malicious" and appends 500+ words of completely benign, neutral text to the end of the malicious payload.
*   **Purpose:** To simulate attackers exploiting ModernBERT's massive 8,192 token context window by hiding a small malicious payload inside a massive legitimate document, attempting to dilute the model's threat probability score.

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



### 3.3: Assemble the Giskard TestSuite
Initialize an empty Giskard `Suite` object. This acts as the container for all security policies.
```python
from giskard import Suite
security_suite = Suite(name=f"Security Suite: {model_name}")
```

### 3.4: Add Data Integrity Tests (Leakage)
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

### 3.5: Add OOD Exploitation Tests (Overconfidence)
Add the overconfidence test to ensure the model does not act decisively on data it does not understand.
*   **Threshold Config:** `threshold=0.05` (< 5% tolerance). If more than 5% of incorrect predictions are made with high confidence, the model is overly aggressive and highly susceptible to OOD evasion.
```python
security_suite.add_test(test_overconfidence_rate(
    model=giskard_model, 
    dataset=giskard_test_dataset, 
    threshold=0.05
))
```

### 3.6: Add Model-Specific Adversarial Tests
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

### 3.7: Execute and Export JUnit XML
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


### 3.8. Comprehensive Implementation Script

The following Python script implements the SOP. It defines the adversarial transformations, wraps the models, and executes the tailored security suites.

```python
import pandas as pd
import random
from transformers import pipeline
import giskard
from giskard import Dataset, Model, Suite
from giskard.testing import (
    test_metamorphic_invariance,
    test_metamorphic_decreasing,
    test_overconfidence_rate,
    test_data_leakage
)
from giskard.registry.transformation_function import transformation_function

# ==========================================
# 1. SETUP & MOCK DATA (Threat Detection Use Case)
# ==========================================
# Simulating a scenario where the models detect malicious/toxic payloads
train_data = pd.DataFrame({
    "text": ["You are a complete idiot", "Have a great day", "Click this malicious link"],
    "label": ["Malicious", "Benign", "Malicious"]
})

test_data = pd.DataFrame({
    "text": ["Delete your account, stupid", "I love this product", "Free gift card click here", "Click this malicious link"], # Note the intentional leakage
    "label": ["Malicious", "Benign", "Malicious", "Malicious"]
})

# Wrap Datasets for Giskard
giskard_train = Dataset(df=train_data, target="label", name="Training Data (For Leakage Detection)")
giskard_test = Dataset(df=test_data, target="label", name="Validation Data")

# ==========================================
# 2. ADVERSARIAL TRANSFORMATION FUNCTIONS
# ==========================================

@transformation_function(name="Adversarial Casing Evasion (BERT)")
def transform_casing(row: pd.Series) -> pd.Series:
    """Simulates casing evasion by randomizing upper/lower case."""
    row['text'] = ''.join([c.upper() if random.random() > 0.5 else c.lower() for c in row['text']])
    return row

@transformation_function(name="Homoglyph Injection Attack (XLM-R)")
def transform_homoglyph(row: pd.Series) -> pd.Series:
    """Replaces Latin characters with visually identical Cyrillic characters to evade filters."""
    homoglyphs = {'a': 'а', 'e': 'е', 'o': 'о', 'p': 'р', 'c': 'с', 'y': 'у', 'x': 'х'}
    text = row['text']
    for lat, cyr in homoglyphs.items():
        text = text.replace(lat, cyr)
    row['text'] = text
    return row

@transformation_function(name="Context Dilution / Good-Word Attack (ModernBERT)")
def transform_dilution(row: pd.Series) -> pd.Series:
    """Appends 500 words of benign text to suppress the model's threat probability."""
    benign_payload = " " + "This is a completely normal and safe sentence discussing standard business operations. " * 50
    # Only dilute malicious samples to see if the threat score decreases
    if row['label'] == "Malicious":
        row['text'] = row['text'] + benign_payload
    return row

# ==========================================
# 3. WRAPPING THE MODEL
# ==========================================
def create_giskard_model(hf_model_id: str, name: str) -> Model:
    """Wraps a HuggingFace pipeline for Giskard execution."""
    clf_pipeline = pipeline("text-classification", model=hf_model_id, top_k=None)
    
    def prediction_function(df: pd.DataFrame) -> pd.DataFrame:
        texts = df["text"].tolist()
        raw_preds = clf_pipeline(texts, truncation=True, max_length=512) # Note: Adjust max_length to 8192 for ModernBERT in actual deployment
        
        formatted_preds = []
        for pred in raw_preds:
            pred_dict = {label_score['label']: label_score['score'] for label_score in pred}
            formatted_preds.append(pred_dict)
        return pd.DataFrame(formatted_preds)
    
    return Model(
        model=prediction_function,
        model_type="classification",
        name=name,
        classification_labels=["Benign", "Malicious"], # Adjust based on your model's actual labels
        feature_names=["text"]
    )

# ==========================================
# 4. EXECUTING SECURITY TEST SUITES
# ==========================================
def run_security_scan(model_id: str, model_name: str, architecture_type: str):
    print(f"\n--- Initiating MLSecOps Scan for {model_name} ---")
    giskard_model = create_giskard_model(model_id, model_name)
    
    # Base Security Suite (Applies to ALL models)
    security_suite = Suite(name=f"Security Suite: {model_name}")
   
    
    # Test 1: Leakage (Confidentiality & Integrity)
    security_suite.add_test(test_data_leakage(giskard_model, giskard_train, giskard_test))
    
    # Test 2: Overconfidence on incorrect predictions (OOD Exploitation)
    security_suite.add_test(test_overconfidence_rate(giskard_model, giskard_test, threshold=0.05))

    # Architecture-Specific Adversarial Tests
    if architecture_type == "BERT":
        # Test 3a: Tokenizer Casing Evasion
        security_suite.add_test(test_metamorphic_invariance(
            model=giskard_model, 
            dataset=giskard_test, 
            transformation_function=transform_casing, 
            threshold=0.0 # 0 tolerance for casing variance in an uncased model
        ))
        
    elif architecture_type == "XLM-R":
        # Test 3b: Cross-lingual Homoglyph Evasion
        security_suite.add_test(test_metamorphic_invariance(
            model=giskard_model, 
            dataset=giskard_test, 
            transformation_function=transform_homoglyph, 
            threshold=0.01 
        ))
        
    elif architecture_type == "ModernBERT":
        # Test 3c: Context Dilution Manipulation
        # Verifies that injecting benign text does NOT decrease the "Malicious" probability significantly
        security_suite.add_test(test_metamorphic_decreasing(
            model=giskard_model, 
            dataset=giskard_test, 
            transformation_function=transform_dilution,
            classification_label="Malicious",
            threshold=0.05 # The malicious probability cannot drop by more than 5% when padded
        ))

    # Execute Suite
    test_results = security_suite.run()
    
    # CI/CD Output
    if test_results.passed:
        print(f"[PASSED] {model_name} is cleared for deployment.")
    else:
        print(f"[FAILED] {model_name} exhibits security vulnerabilities. Triage required.")
    
    return test_results

# ==========================================
# 5. INVOCATION (Main Block)
# ==========================================
if __name__ == "__main__":
    # Note: In a real environment, replace with your fine-tuned local paths or HF Hub IDs
    
    # 1. Test BERT for Casing Evasion
    # run_security_scan("your-finetuned-bert", "BERT-Uncased Security Scanner", "BERT")
    
    # 2. Test XLM-R for Homoglyph Evasion
    # run_security_scan("your-finetuned-xlm-roberta", "XLM-R Security Scanner", "XLM-R")
    
    # 3. Test ModernBERT for Context Dilution
    # run_security_scan("your-finetuned-modernbert", "ModernBERT Security Scanner", "ModernBERT")
    pass
```


## Phase 4: Reporting and Artifact Management

Once Phase 3 generates the results, security policies must be enforced based on those results.

### Step 4.1: Blocking (The Quality Gate)
Parse the `giskard_security_report.xml` file
*   **Pass Condition:** If all tests pass, the pipeline executes `exit 0`, allowing the model artifact to be pushed to the production registry (e.g., AWS SageMaker or HF Model Registry).
*   **Fail Condition (Blocking):** If any test fails (e.g., leakage is detected, or overconfidence exceeds 5%), the XML parser detects a `<failure>` tag. The pipeline executes `exit 1` (Build Failed). The model is **blocked** from deployment.

### Step 4.2: Human-Readable Report Generation
While machines read XML, SecOps engineers need context to patch the model. The automation script must generate an HTML report containing the specific rows of data that bypassed the model.
```python
# Export detailed HTML report for the SecOps team
test_results.to_html("secops_vulnerability_report.html")
```



---

## Phase 5: Incident Triage Rules
*(Following Phase 4, the SecOps team reviews the archived HTML report and applies specific fixes based on which test failed.)*
*   **Leakage Fails:** Purge the fine-tuning dataset of the leaked records and retrain.
*   **Overconfidence Fails:** Implement a software-level threshold (e.g., if model confidence < 85%, route to human review).
*   **Invariance Fails:** Apply strict input sanitization (NFKC normalization, lowercasing) *before* the text reaches the model tokenizer.
*   


## Phase 5: Triage & Remediation
Remediation strategies depend on the Phase 4 findings.

1.  **Leakage Remediation:**  
    **Leakage Fails (Threshold > 0%):** 
    **Action:** **BLOCK DEPLOYMENT. Purge, Re-partition, and Retrain.**
    
    Data leakage invalidates all security metrics. If this test fails, the SecOps team must execute the following remediation protocol:

    1.1  **Identify and Audit:** Use the Giskard HTML report to identify exactly which records leaked between Dataset A (Training) and Dataset B (Testing). Audit the upstream data ingestion pipeline to determine how the contamination occurred.  

    1.2.  **Cryptographic Re-Partitioning (The Root-Cause Fix):** Do not merely delete the specific rows that Giskard flagged. You must rewrite the dataset splitting logic. Implement a **hashing-based split** (e.g., applying SHA-256 to normalized text). 
        *   *Why?* Hashing ensures that exact duplicates, or near-duplicates, will yield the same hash and be forced into the *same* partition (Train OR Test), making it mathematically impossible for identical sentences to span both datasets.
  
    1.3.  **Purge and Retrain:** Discard the compromised model artifact and the old datasets. Generate the newly partitioned, mathematically isolated Training and Validation sets. Trigger a full model retraining pipeline from scratch.  

    1.4.  **Re-Validate:** Run Phase 3 of the MLSecOps test suite again to confirm `test_data_leakage` passes before proceeding to adversarial testing. 



1.  **Evasion Remediation:** 
    *   **BERT:** Implement a `NFKC` normalization and strict `lower()` function in the production preprocessing pipeline.
    *   **XLM-RoBERTa:** Implement a homoglyph-to-Latin mapper in the input sanitization layer.
   


3.  **Overconfidence/OOD Remediation:** Implement a **"Confidence Threshold Gate"**. If the model's top-1 probability is `< 0.90` on a security-critical decision, the input is automatically escalated to a human analyst or a secondary, more robust model.
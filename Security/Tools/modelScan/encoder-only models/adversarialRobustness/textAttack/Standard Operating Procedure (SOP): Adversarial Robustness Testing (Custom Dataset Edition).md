

This SOP integrates threat intelligence (Threat Actor Profiles) with MLOps pipelines (Custom Dataset Fine-tuning) and mapped TextAttack algorithms, providing a comprehensive playbook for securing NLP models (e.g., BERT, ModernBERT, XLM-RoBERTa).

---


## **Phase 1: Threat Modeling & Scope Definition**
Before executing any code, the security engineer must document the asset and the simulated adversary. NLP security testing must simulate specific **Tactics, Techniques, and Procedures (TTPs)** based on real-world threat actors.

Select the primary Threat Actor Profile targeting your custom dataset:

### **Profile 1: The "Noisy" Evasion Adversary**
*   **Target Asset:** Spam filters, phishing detection, toxicity/hate-speech moderators.
*   **Access Level:** Black-Box (Query access only).
*   **TTPs:** Token-breaking. Relies on character obfuscation, *l33tspeak*, typos, and visual homoglyphs. The text may look unnatural to a machine but remains readable to the human victim.

### **Profile 2: The Semantic Manipulator (The "Stealth" Attacker)**
*   **Target Asset:** Financial sentiment analysis, legal document classifiers, disinformation filters.
*   **Access Level:** Soft-Label Black-Box (API returns confidence probabilities).
*   **TTPs:** Advanced context-aware synonym substitutions and masked language models (MLMs). The adversarial payload must maintain flawless grammar and semantics to evade human auditors.

### **Profile 3: The Insider Threat / Supply Chain Compromise**
*   **Target Asset:** Core proprietary models, MLOps pipelines.
*   **Access Level:** White-Box (Full access to architecture, weights, and gradients).
*   **TTPs:** Gradient exploitation. The attacker calculates the exact mathematical derivatives of the model to find the most devastating perturbation with minimal effort.

---

## **Phase 2: Data Preparation & Ingestion**
Format your domain-specific data to ensure compatibility with both Hugging Face and TextAttack.
1.  Prepare your custom dataset as a CSV (`custom_data.csv`).
2.  Ensure strict column naming: `text` (the input) and `label` (integer classification).
3.  Split the data: **80% Training Set** (for Phase 3) and **20% Test Set** (for Phase 5).

---

## **Phase 3: Domain-Specific Fine-Tuning**
Base models (`bert-base-uncased`, `ModernBERT-base`, `xlm-roberta-base`) produce random noise until fine-tuned. You must adapt them to your custom domain first.

**Implementation Script (`train_custom.py`):**
```python
import pandas as pd
from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

# 1. Select Target Architecture
MODEL_NAME = "google-bert/bert-base-uncased"
# MODEL_NAME = "answerdotai/ModernBERT-base"
# MODEL_NAME = "FacebookAI/xlm-roberta-base"

# 2. Load and Split Custom Data
df = pd.read_csv("custom_data.csv")
hf_dataset = Dataset.from_pandas(df)
train_test = hf_dataset.train_test_split(test_size=0.2, seed=42)
NUM_LABELS = len(df['label'].unique())

# 3. Tokenization (Include Truncation for long custom texts)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=256)

tokenized_datasets = DatasetDict({'train': train_test['train'], 'test': train_test['test']}).map(tokenize_function, batched=True)

# 4. Train Model
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=NUM_LABELS)
training_args = TrainingArguments(
    output_dir=f"./custom_tuned_{MODEL_NAME.split('/')[-1]}",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    num_train_epochs=4
)

trainer = Trainer(model=model, args=training_args, train_dataset=tokenized_datasets["train"], eval_dataset=tokenized_datasets["test"])
trainer.train()

# 5. Save Artifacts
trainer.save_model(f"./custom_tuned_{MODEL_NAME.split('/')[-1]}")
tokenizer.save_pretrained(f"./custom_tuned_{MODEL_NAME.split('/')[-1]}")
tokenized_datasets["test"].to_csv("test_split_for_attack.csv")
print("Model fine-tuned and Test split saved.")
```

---

## **Phase 4: Recipe Selection Matrix**
Based on the Threat Actor chosen in Phase 1 and the linguistic nature of your custom dataset, select the appropriate TextAttack Recipe.

| Threat Profile | Dataset Language/Domain | Mapped TextAttack Recipes | Security Rationale |
| :--- | :--- | :--- | :--- |
| **Profile 1: Noisy / Evasion** | English OR Multilingual (`XLM-R`) | **`DeepWordBug`**, **`TextBugger`**, **`Pruthi2019`** | Modifies characters (typos, swaps) to break tokenizers. Crucial for XLM-RoBERTa, as English semantic tools fail on multilingual text. |
| **Profile 2: Stealth (General)** | General English (News, Reviews) | **`TextFooler`**, **`PWWS`**, **`CLARE`**, **Heuristic Family** (Alzantot, PSO, IGA) | Swaps words using WordNet/Embeddings. Fast and highly effective for standard English. |
| **Profile 2: Stealth (Specialized)**| Highly Specialized English (Medical, Legal, Tech) | **`BAE`**, **`BERT-Attack`**, **`Imperceptible Perturbations`** | Uses context-aware Masked Language Models. Ensures domain-specific jargon is not swapped with nonsensical general words. |
| **Profile 3: Insider Threat** | Any Language (Full System Access) | **`HotFlip`** | Uses white-box gradient computation to find the exact mathematical weakness of your fine-tuned weights. |
| **Auditor / Diagnostic (Bonus)** | Behavior & Interpretability Testing | **`CheckList`**, **`Input Reduction`** | Not a malicious attack. Used by engineers to detect demographic bias or identify the minimum tokens triggering a classification. |

---

## **Phase 5: Attack Execution**
Execute the attack using the locally fine-tuned model and the selected recipe. 

**Implementation Script (`attack_custom.py`):**
```python
import textattack
import transformers
import datasets
from textattack.models.wrappers import HuggingFaceModelWrapper
from textattack.datasets import HuggingFaceDataset

# Import recipes based on Phase 4 Matrix
from textattack.attack_recipes import TextBuggerLi2018, BAEGarg2019, HotFlipEbrahimi2017

# 1. Load the locally fine-tuned model
model_path = "./custom_tuned_bert-base-uncased" 
model = transformers.AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = transformers.AutoTokenizer.from_pretrained(model_path)
model_wrapper = HuggingFaceModelWrapper(model, tokenizer)

# 2. Load the Custom Test Set (Generated in Phase 3)
custom_test_hf = datasets.load_dataset("csv", data_files="test_split_for_attack.csv")["train"]
dataset = HuggingFaceDataset(custom_test_hf, input_columns=["text"], label_names=["Class_0", "Class_1"])

# 3. Instantiate the selected Recipe (Simulating Profile 2: Specialized Stealth here)
attack = BAEGarg2019.build(model_wrapper)

# 4. Modify Constraints (CRITICAL for Custom Domains and Long Texts)
# To prevent infinite loops on long documents, restrict the modification rate.
from textattack.constraints.overlap import MaxModificationRate
attack.constraints.append(MaxModificationRate(max_rate=0.15, min_length=1))

# 5. Define Attack Arguments
attack_args = textattack.AttackArgs(
    num_examples=100,               # Scan 100 successful initial predictions
    log_to_csv="attack_results.csv",# Output for Phase 6 Analysis
    checkpoint_interval=10,       
    disable_stdout=False,
    parallel=True                   # Enable for multi-GPU speedup
)

# 6. Execute Simulation
print("Initiating Adversarial Simulation...")
attacker = textattack.Attacker(attack, dataset, attack_args)
attacker.attack_dataset()
```

---

## **Phase 6: Post-Incident Analysis & Hardening (Adversarial Training)**
Once the `attack_results.csv` is generated, the security team must analyze the vulnerabilities and harden the model.

### 1. Architectural Triage
*   **Attack Success Rate (ASR):** Did the attacker succeed >30% of the time? If `ModernBERT-base` shows a 15% ASR and `bert-base-uncased` shows 45% against the same Profile, `ModernBERT` is architecturally more robust for your domain.
*   **Words Perturbed:** If the recipe flipped a document's classification by changing only 2% of the words, the model's decision boundary is highly brittle.

### 2. Model Hardening (Closing the Loop)
To fix the vulnerabilities discovered during the simulation, perform **Adversarial Training**:
1.  Extract the `Perturbed Text` column from your `attack_results.csv` (these are the successful attacks).
2.  Append these malicious examples back into your original `custom_data.csv` with their *correct* labels.
3.  Re-run **Phase 3 (Domain-Specific Fine-Tuning)**. 
4.  *(Optional):* Use the `A2T (Attack for Adversarial Training)` recipe natively inside TextAttack's training loop to continuously generate and defend against Profile 2 stealth payloads dynamically during training.
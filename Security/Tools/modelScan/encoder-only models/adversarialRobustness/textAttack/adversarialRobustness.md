
https://towardsdatascience.com/what-are-adversarial-examples-in-nlp-f928c574478e/

https://textattack.readthedocs.io/en/master/1start/what_is_an_adversarial_attack.html



The above article explains how AI models can be tricked into making mistakes (adversarial examples) and specifically how this concept applies to Natural Language Processing (AI that reads and understands text).

Here is a summary of the key takeaways:

### 1. What is an Adversarial Example?
An adversarial example is an input specifically designed to fool a machine learning model. 
* **The Image Example:** In computer vision, a classic example is taking an image of a pig and adding an invisible layer of digital static (noise) to it. To a human eye, the image still looks exactly like a pig. But to the AI, that specific mathematical noise tricks it into classifying the pig as an airliner.

### 2. The Problem with Text (NLP)
Tricking an AI with images is relatively easy because you can change pixel values by tiny fractions that the human eye can't see. 
However, **you cannot do this with text.** You can't change a word "invisibly". If you change "pig" to "hog" or "p1g", the text has fundamentally and visibly changed. Because of this, researchers had to come up with new definitions for what makes a valid "trick" (adversarial example) in text. 

### 3. Two Ways to Trick NLP Models
Because text can't be invisibly altered, the article groups NLP adversarial attacks into two categories of "similarity":

* **Visual Similarity (Character-level):** These are attacks that look almost identical to the original text to a human, usually achieved by changing just a few characters or introducing realistic typos. For example, changing *"fantastic movie"* to *"fantast1c movie."* The human brain reads it the exact same way, but the slight character change might completely break the AI's prediction. *(Note: The article mentions these are often easily defended against with basic spellcheckers).*
* **Semantic Similarity (Word/Sentence-level):** These attacks change the words entirely but keep the exact same meaning (paraphrasing or using synonyms). For example, changing *"The film was awful"* to *"The movie was terrible."* A human knows these mean the same thing, but if the AI is poorly trained, it might classify the first as a negative review and the second as a positive review. 

### 4. Introducing "TextAttack"
The second half of the article introduces **TextAttack**, an open-source Python library built by the author's team. It is designed to help researchers easily generate these adversarial examples. 
It works by running thousands of tests on an AI model, systematically swapping out words or characters until it finds the exact combination that causes the AI to fail (while making sure the text still makes sense to humans). 

### Why does this matter?
Understanding how AI can be tricked is vital for **AI Security (Adversarial Robustness)**. If an AI is sorting spam emails, identifying hate speech, or analyzing legal documents, bad actors can use these subtle text tweaks to bypass the AI. By using tools like *TextAttack* to find the blind spots in AI models, developers can train their models on those tricky examples to make them smarter, safer, and more robust.


# Terminology


## 1. "Adversarial Example" vs. "Adversarial Perturbation"
The text begins by drawing a distinction between two terms that are often used interchangeably, but have different meanings:

* **Adversarial Example (The broad category):** Any input that fools an AI model. This includes completely fake inputs created from scratch. For instance, generating a sequence of random, gibberish characters that somehow tricks a model into thinking it is a positive review.
* **Adversarial Perturbation (The specific category):** A tweak made to an already existing, normal ("benign") input. You start with a real, human-written sentence and make small changes to it. 
* **The Takeaway:** **TextAttack only does the second one.** It does not generate random fake text from scratch. It takes your real data and perturbs (tweaks) it to find flaws.

---

### 2. How the Attack Process Works
The passage explains how TextAttack tests a dataset step-by-step:

* **It starts with a dataset:** A list of sentences with their correct labels (e.g., a list of reviews labeled "Positive" or "Negative").
* **It tests the AI first:** Before trying to trick the AI, TextAttack lets the AI predict the label for a sentence.
* **The "Only Attack the Correct Ones" Rule:** 
    * If the AI gets a sentence **wrong** on its own (e.g., the review says "This movie was great!" but the AI predicts "Negative"), TextAttack skips it. There is no point in trying to trick an AI that is already making a mistake.
    * If the AI gets the sentence **correct**, TextAttack begins its attack. It starts searching for those tiny tweaks (perturbations) that will make the AI change its correct answer to a wrong one.

---

### 3. TextAttack’s "Interchangeable Components"

- https://aclanthology.org/2020.emnlp-demos.16/  
- https://textattack.readthedocs.io/en/latest/2notebook/1_Introduction_and_Transformations.html  
- https://textattack.readthedocs.io/en/latest/1start/attacks4Components.html 
- https://textattack.readthedocs.io/en/latest/2notebook/1_Introduction_and_Transformations.html  

The final sentence explains that TextAttack is built like a Lego set. It breaks an attack down into logical stages and lets you swap different strategies in and out. 

Instead of having just one hard-coded way to attack a model, TextAttack has four modular components you can mix and match:
1. **Goal Function:** What is the objective? (e.g., "Make the AI change its prediction classification" or "Make the AI output a specific target word").
2. **Constraints:** What are the rules? (e.g., "The new sentence must look 90% similar to the original" or "Do not change the grammar").
3. **Transformation:** How do we make changes? (e.g., "Swap words with synonyms" or "Insert random typos").
4. **Search Method:** How do we find the best change? (e.g., "Try every word one-by-one" or "Use a smart algorithm to find the most impactful words first").

### Summary
In short, the statement is telling you: **TextAttack is a highly customizable tool that takes real, correctly-predicted text samples and carefully tweaks them (without violating set rules) to see if it can trick an NLP model into making a mistake.**


## Constraints
the definition for the contraints at https://textattack.readthedocs.io/en/latest/2notebook/1_Introduction_and_Transformations.html  

"overlap constraints that measure edit distance, syntactical constraints check part-of-speech and grammar errors, and semantic constraints like language models and sentence encoders."

To understand this statement, it helps to first understand **why** we need constraints in an adversarial attack. 

If you let TextAttack change words in a sentence without any rules, it could easily trick the model by changing *"I love this movie"* into *"This film is terrible"* or into complete gibberish like *"I table this movie"*. 

While both of those would trick the model, they are **useless attacks** because they either completely change the meaning or don't make sense to a human. 

**Constraints are the rules that force TextAttack to make changes that a human wouldn't easily notice.** The statement breaks these rules down into three categories:

---

### 1. Overlap Constraints (Edit Distance)
* **Goal:** *"Don't change too much of the text."*
* **How it works:** This constraint uses mathematical measurements like **edit distance** (e.g., Levenshtein distance) to count how many characters or words were changed, added, or deleted between the original sentence and the attacked sentence.
* **In practice:** You might set a rule that says: *"You are only allowed to change up to 15% of the words in the sentence."* If the sentence has 10 words, TextAttack is only allowed to modify 1 or 2 of them. 

---

### 2. Syntactical Constraints (Part-of-Speech and Grammar)
* **Goal:** *"Keep the grammar correct."*
* **How it works:** 
  * **Part-of-Speech (POS) checking:** This ensures that if TextAttack replaces a word, it replaces it with the same type of word. If the original word is a verb, it must be replaced with a verb. 
  * **Grammar checking:** This runs the tweaked sentence through a grammar checker to make sure the change didn't make the sentence sound unnatural or broken.
* **In practice:** In the sentence *"The **fast** car ran,"* "fast" is an adjective. 
  * *Allowed swap:* *"The **quick** car ran"* (swapping an adjective for an adjective).
  * *Blocked swap:* *"The **quickly** car ran"* (blocked because "quickly" is an adverb and breaks the grammar).

---

### 3. Semantic Constraints (Language Models and Sentence Encoders)
* **Goal:** *"Ensure the sentence still means the exact same thing."*
* **How it works:** 
  * **Sentence Encoders:** These are smart AI models that convert the original sentence and the tweaked sentence into mathematical vectors and compare them. If the mathematical similarity is high (e.g., above 90%), it means the meaning was successfully preserved.
  * **Language Models:** These analyze how likely a human is to actually say the new sentence. If the sentence sounds weird or robotic, the language model flags it.
* **In practice:** 
  * *Allowed swap:* Changing *"The dog fell asleep"* to *"The dog drifted off to sleep"* (the meaning remains the same).
  * *Blocked swap:* Changing *"The dog fell asleep"* to *"The dog died"* (even though the grammar is perfect and only one word changed, the meaning is completely different, so semantic constraints block it).

---

### Summary
Think of these constraints as a three-layer filter:
1. **Overlap:** Did we change too many words?
2. **Syntactical:** Does the new sentence still follow grammar rules?
3. **Semantic:** Does the new sentence still mean the same thing?


-----
# 使用方法
## 示例： https://textattack.readthedocs.io/en/latest/api/attacker.html


### Why must a model be fine-tuned before using TextAttack?

**version 1:**

Base checkpoints such as bert-base-uncased only contain a pre-trained encoder. When AutoModelForSequenceClassification.from_pretrained() is used, Transformers automatically attaches a task-specific classification head whose weights are randomly initialized. Because this classification head has never been trained on the downstream task, the model's predictions are essentially arbitrary and do not reflect meaningful decision boundaries.

TextAttack assumes that the target model already performs the classification task correctly on at least some inputs. It first checks whether the original example is classified correctly. If an example is already misclassified, TextAttack skips it because there is no correct prediction to attack. Even for examples that happen to be classified correctly by chance, attacks against an untrained classifier do not provide meaningful robustness evaluation, since the decision boundary itself has not been learned.

Therefore, TextAttack is intended to evaluate fine-tuned classification models rather than base pre-trained checkpoints with randomly initialized classification heads.


-------
**version 2:**

**For encoder-only base models (e.g., base checkpoints of BERT, RoBERTa, or DeBERTa):**

* During the pre-training phase, only the Encoder is trained.
* The Classification Head (classifier) is either absent or randomly initialized.

**Therefore, without being fine-tuned on a downstream classification task:**
* The logits lack any semantic meaning;
* The predictions are essentially random;
* The loss has no practical value;
* TextAttack cannot obtain stable and reliable predictions, making it unable to properly execute attacks that rely on classification outputs.

**Thus, to be more precise, it is not simply that:**
> *"Random noise causes TextAttack to fail,"*

**But rather:**
> *"Because the model has not been trained on a classification task, it cannot provide meaningful classification predictions, whereas TextAttack fundamentally relies on stable classification outputs to generate attacks."*


-----
**version 3:**

This question touches upon the underlying design of **Transfer Learning** in machine learning, as well as the operational logic of the TextAttack framework.

Simply put, the reason comes down to this: the "classifier" portion of a Base model is randomly initialized. Before fine-tuning, its classification output for any text is just meaningless random noise, which prevents TextAttack from functioning properly.

Below is a detailed breakdown of the reasons, along with the Sources of Truth from the official Hugging Face and TextAttack documentation.

---

### I. Why Must You Fine-Tune First? (Technical Principles)

#### 1. Missing Structure: Base models lack a "Classification Head"
Base models like `bert-base-uncased` only learn general language patterns (e.g., predicting masked words in a "fill-in-the-blank" style) during the Pre-training phase. They do not contain an output layer designed for specific downstream tasks (such as a binary "positive/negative" classification for sentiment analysis).

When you call this in your code:
```python
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
```
Hugging Face's Transformers library executes two steps:
1. Loads the BERT backbone (for feature extraction).
2. Appends a new linear classification layer on top (i.e., the Classification Head, typically `nn.Linear(hidden_size, num_labels)`).

#### 2. "Random Noise" Caused by Random Initialization
The internal weights and biases of this newly appended classification layer are **purely randomly initialized**. This means:
* The model has absolutely no idea what your classification task is (it doesn't know what "positive/negative" or "spam" means).
* For any input text, the classification probabilities output by the model are essentially a coin toss or pure random guessing.

#### 3. Why Can't a Random Model Be Attacked by TextAttack?
TextAttack's attack logic is: *"Find a minor perturbation that can change a model's 'correct' prediction into an 'incorrect' prediction."*

According to TextAttack's code logic, before initiating an attack, it first makes the model predict the original text:
* **If the model predicts incorrectly on its own:** Since a random model has a >50% chance of just guessing wrong, TextAttack assumes "this text has already successfully fooled the model," and will **directly skip** this sample without attempting any attack.
* **If the model happens to guess correctly:** At this stage, the model's Decision Boundary is entirely chaotic. TextAttack would be searching for perturbations within an arbitrary decision space. The resulting "adversarial examples" would just be meaningless, random combinations that do not reflect any genuine semantic vulnerabilities in the model.

---

### II. Sources of Truth

#### Source of Truth 1: Official Runtime Warning from Hugging Face Transformers (Proving Random Initialization)
When you directly load a Base pre-trained model using `AutoModelForSequenceClassification` without fine-tuning, the Hugging Face console will force-print this signature red warning:

> *"Some weights of the model checkpoint at bert-base-uncased were not used when initializing BertForSequenceClassification... Some weights are newly initialized: **['classifier.weight', 'classifier.bias']**. You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference."*

**Interpretation:** This warning is designed by Hugging Face specifically to prevent developers from using non-fine-tuned classification models for downstream predictions. It explicitly states that the weights of the `classifier` (classification head) are newly and randomly initialized, rendering it incapable of making meaningful predictions before fine-tuning.

#### Source of Truth 2: TextAttack Paper and Official Source Code (Proving the Skip Logic)
In the official TextAttack paper, *TextAttack: A Framework for Adversarial Attacks, Data Augmentation, and Adversarial Training in NLP*, and its official GitHub source code:

1. **Source code implementation for skipping incorrect samples:** 
   Within TextAttack's core class `GoalFunction` (located in `textattack/goal_functions/goal_function.py`), its evaluation function `get_results` contains the following filtering logic:
   ```python
   # If check_skip is True, and the model's initial prediction is already wrong
   if check_skip and (not self._is_correct(initial_result)):
       # This sample will be directly marked as Skipped, and no attack is performed
       return GoalFunctionResult(..., skipped=True)
   ```
2. **Model Wrapper Specifications:** 
   According to the official TextAttack *Model Wrappers* documentation, a classification model's wrapper (`ModelWrapper`) must return a two-dimensional list of model prediction scores (List of lists of scores). These scores must come from a model that has been trained, converged on the respective dataset, and can output stable classification logits.

---

**Summary**  
This is why a model must be in a Fine-tuned state before using TextAttack. If it is in its Base state, upon reading the data, TextAttack will directly skip the vast majority of samples due to the model's exceedingly low random accuracy, making it impossible to properly conduct the adversarial attack testing.

### AutoModelForSequenceClassification
https://medium.com/learning-data/under-the-hood-of-automodelforsequenceclassification-in-hugging-face-transformers-e497bc78d828  


这句代码：

```python
model = transformers.AutoModelForSequenceClassification.from_pretrained(model_name)
```

它的作用可以拆成两部分来看。

#### 第一部分：`AutoModelForSequenceClassification`

这是 Hugging Face 提供的 **自动模型加载器**。

它会根据 `model_name` 自动判断应该实例化哪一种模型，例如：

| model_name                  | 实际加载的类                                |
| --------------------------- | ------------------------------------- |
| `bert-base-uncased`         | `BertForSequenceClassification`       |
| `roberta-base`              | `RobertaForSequenceClassification`    |
| `distilbert-base-uncased`   | `DistilBertForSequenceClassification` |
| `microsoft/deberta-v3-base` | `DebertaV2ForSequenceClassification`  |

也就是说，你不用自己写：

```python
BertForSequenceClassification(...)
```

或者

```python
RobertaForSequenceClassification(...)
```

AutoModel 会自动选择。

---

#### 第二部分：`from_pretrained(model_name)`

这一句会：

1. 下载（或读取本地缓存）模型。
2. 根据配置文件构建模型结构。
3. 加载 checkpoint 权重。

例如：

```python
model_name = "bert-base-uncased"
```

它会下载：

* config.json
* pytorch_model.bin（或 model.safetensors）
* tokenizer 相关文件（如果加载 tokenizer）

然后构建

```
BertForSequenceClassification
│
├── BertModel
└── Classification Head
```

---

#### 关键问题：这里的 classifier 是不是训练好的？

这取决于 **`model_name` 是什么**。

##### 情况一：Base 模型（你的情况）

例如：

```python
model_name = "bert-base-uncased"
```

或者

```python
"FacebookAI/roberta-base"
```

这些都是 **Base checkpoint**。

模型结构会变成：

```
Encoder（预训练好的）
        +
Classification Head（随机初始化）
```

所以 Hugging Face 通常会打印类似：

```
Some weights of BertForSequenceClassification were not initialized
and are newly initialized:
['classifier.weight', 'classifier.bias']
```

意思就是：

> 分类层没有权重，所以新建了一个随机初始化的 classifier。

因此：

```
prediction ≈ random
```

---

##### 情况二：已经微调好的模型

例如：

```python
model_name = "textattack/bert-base-uncased-SST-2"
```

这时：

```
Encoder（训练好）
        +
Classification Head（训练好）
```

整个模型都会加载下来。

预测就是：

```
"This movie is great."
↓

Positive (0.998)
```

这种模型才能直接用于 TextAttack。

---

#### 为什么 TextAttack 在 Base 模型上会失败？

因为这一句：

```python
AutoModelForSequenceClassification.from_pretrained(...)
```

**不会自动帮你训练 classifier**。

对于 Base checkpoint，它只是：

```
随机生成 classifier
```

例如：

```
Linear(768 → 2)
```

其中参数可能是：

```
W = random
b = random
```

所以输入任何句子：

```
"I love this movie."
```

得到：

```
logits = [0.12, -0.38]
```

或者

```
[-1.72, 3.41]
```

这些数值没有任何语义，只是随机权重计算出来的结果。

而 TextAttack 依赖模型输出的类别和置信度来决定如何生成对抗样本，因此面对一个输出基本随机的分类器，就无法产生有意义的攻击结果。

---

**一句话总结：**

```python
model = transformers.AutoModelForSequenceClassification.from_pretrained(model_name)
```

的作用是：

> **根据 `model_name` 自动加载一个用于文本分类（Sequence Classification）的 Transformer 模型。如果 `model_name` 是已经微调好的分类模型，则会加载训练好的分类头；如果是 Base 预训练模型，则会创建一个随机初始化的分类头，因此模型尚不具备有意义的文本分类能力。**

## dataset 
https://textattack.readthedocs.io/en/latest/api/datasets.html
https://textattack.readthedocs.io/en/latest/1start/FAQ.html



Here is the English translation of the content provided:

---



#### Suggested Solutions:

If you want to perform testing with TextAttack, you have two options:

*   **Option A (Easiest)**: Search the Hugging Face community directly for versions that have already been fine-tuned by others.
    *   *Example*: Search for `textattack/bert-base-uncased-SST-2` (BERT fine-tuned for SST-2 sentiment analysis).
    *   *Example*: Search for `cardiffnlp/twitter-xlm-roberta-base-sentiment` (XLM-RoBERTa fine-tuned for Twitter sentiment analysis).
*   **Option B (More Flexible)**: Use your own private dataset to train (fine-tune) these three Base models using PyTorch or the Hugging Face Trainer. Save the model weights and then use TextAttack to load the local weights.

---

### I. How to choose a dataset when testing with TextAttack?

When selecting a dataset for TextAttack testing, you should follow these core principles:

#### Principle 1: Consistency of Tasks and Labels
The dataset you choose **must** match the task for which your model was fine-tuned.

*   If your model was fine-tuned on the **SST-2 Sentiment Analysis** dataset, then you must also use the SST-2 validation set or test set for your testing.
*   If you attempt to test a sentiment analysis model using a spam classification dataset, the model will produce completely meaningless predictions, and TextAttack will subsequently error out or provide meaningless results.

#### Principle 2: Controlling Sample Size (Performance Principle)
An adversarial attack is an operation with extremely high computational costs and slow execution speeds.

*   **Reason**: To find a single word that can fool the model, TextAttack must repeatedly modify sentences in the background and perform hundreds or thousands of forward passes (inferences) on the model.
*   **Recommendation**: Do not attempt to attack an entire validation set containing tens of thousands of data points. Randomly sampling **100 to 1,000 samples** from the test/validation set is usually sufficient to evaluate a model's robustness.
    *   *CLI Tip*: In the TextAttack command line, you can use the `--num-examples 100` argument to limit the number of test cases.

#### Principle 3: Choose a Subset with High Model Accuracy (Validity Principle)
As mentioned previously, TextAttack will directly skip samples that the model originally predicted incorrectly.

*   If your model's accuracy on a certain test set is only 50% (roughly equivalent to random guessing), it means that 50% of the samples will be skipped immediately.
*   It is recommended to choose a dataset where the model's accuracy is **above 80%**. Searching for adversarial examples to fool a model only holds value for security assessment when the model itself is "intelligent" and performing well on clean data.

---

### II. Recommended Common Academic Benchmark Datasets

If you are conducting academic research or benchmarking, TextAttack has built-in support for Hugging Face `datasets`. Below are the most commonly used datasets for classification models:

| Task Type | Recommended Dataset Name | Number of Classes | Description |
| :--- | :--- | :--- | :--- |
| **Sentiment Analysis** | **`sst2`** or **`rotten_tomatoes`** | 2 (Pos/Neg) | Short sentences, fast execution; best for beginners. |
| **Sentiment (Long Text)** | **`imdb`** | 2 (Pos/Neg) | Long-form movie reviews. Execution is much slower than `sst2` due to text length. |
| **Topic Classification** | **`ag_news`** | 4 (Tech, Sports, etc.) | Multi-class task. Used to evaluate security vulnerabilities in topic recognition. |
| **NLI (Inference)** | **`glue` (sub-tasks: `mnli` or `qnli`)** | 2 or 3 | Evaluates if the model understands logic between sentences (Entailment, Contradiction, Neutral). |

#### CLI Usage Example:

If you already have a model fine-tuned for `sst2`, you can run the following command directly in the terminal to perform a test:

```bash
textattack attack --recipe textfooler --model-from-huggingface textattack/bert-base-uncased-SST-2 --dataset-from-huggingface sst2 --dataset-split validation --num-examples 100
```

*(This command will automatically download the fine-tuned BERT model and the SST-2 validation set, randomly select 100 samples, and use the classic TextFooler algorithm to conduct the attack test.)*


## available models:

https://textattack.readthedocs.io/en/latest/3recipes/models.html


## built-in models (Bidirectional LSTM and WordCNN)

In TextAttack, the framework specifically includes these two classic and lightweight model architectures (**Bidirectional LSTM** and **WordCNN**) by design.

Simply put, these built-in models serve as **fast and standard "Baseline Models."**

TextAttack provides pre-trained classification weights for these two architectures across various classic NLP datasets (such as SST-2, IMDb, and AG News), utilizing 200-dimensional GLoVE word vectors as the underlying embeddings. They primarily serve the following four core purposes:

---

### 1. Rapid Prototyping and Debugging (CPU-Friendly)
Large Language Models or Transformer-based models (like BERT or ModernBERT) are massive and run extremely slowly on devices lacking high-end GPUs.
* **The Advantage:** Built-in LSTM and CNN models are very lightweight, requiring minimal memory and CPU resources.
* **The Application:** If you are developing a new adversarial attack algorithm or debugging TextAttack scripts on a local machine, using the built-in `lstm` or `cnn` as your target allows the attack to finish in seconds. This saves a significant amount of time compared to loading a massive BERT model for every debug cycle.

### 2. Cross-Architecture Robustness Benchmarking
In both academia and industry, when evaluating a new attack algorithm, researchers often want to know: which model architecture is more resilient to the same attack?
* **The Application:** By providing built-in LSTM (a Recurrent Neural Network representing traditional sequential models) and WordCNN (a Convolutional Neural Network representing local feature extraction), TextAttack allows you to easily compare them against BERT or RoBERTa (Attention-based Transformer models) on a level playing field.
* **Example:** You can test: *"Does the same misspelling attack (e.g., DeepWordBug) cause more disruption to a CNN or to BERT?"*

### 3. Fair Scientific Comparison
When different researchers attempt to replicate adversarial attack papers, inconsistencies in model training parameters or dataset splits can lead to unfair comparisons.
* **The Application:** TextAttack standardizes these two lightweight architectures and hosts their pre-trained weights for various standard datasets (such as IMDb and Rotten Tomatoes) on official servers. This allows all researchers to pull identical models, such as `lstm-mr` or `cnn-sst2`, for a direct and fair "apples-to-apples" comparison of attack algorithm efficiency.

### 4. Educational and Lightweight Training Demos
Beyond attacks, TextAttack also supports **Adversarial Training** and model fine-tuning.
* **The Application:** If you want to test whether adding perturbed text to the training set enhances a model's defensive capabilities, using the built-in `lstm` or `cnn` allows you to complete a full training and testing cycle in just a few minutes. This is ideal for classroom demonstrations or rapid experimentation.

---

### Command-Line Example:
If you want to quickly try out these built-in models, you can load the officially pre-trained versions directly from the command line. For example, to attack a built-in LSTM model trained on the Movie Review (MR) dataset:

```bash
textattack attack --recipe textfooler --model lstm-mr --num-examples 20
```


----

## recipes:

https://textattack.readthedocs.io/en/latest/apidoc/textattack.attack_recipes.html

https://textattack.readthedocs.io/en/latest/3recipes/attack_recipes.html



### What does "recipe" mean in `--recipe textfooler`, and how many recipes are there in total?

#### 1. What does "Recipe" mean?
A **Recipe** is a central concept in TextAttack. In the academic community, many researchers have published various NLP attack algorithm papers. Under the hood, each algorithm is essentially a unique combination of the "Four Modular Components" mentioned earlier (Goal Function, Constraints, Transformation, and Search Method).

To help developers easily reproduce papers from top-tier conferences, TextAttack pre-packages the parameter combinations from these papers into an **Attack Recipe**. For example, when you input `--recipe textfooler`, TextAttack automatically invokes the entire attack logic designed in the classic 2019 paper *"Is BERT Really Robust?"* You do not need to manually configure any complex parameters.

#### 2. How many Recipes are there in total?
According to the official TextAttack documentation, there are currently **16 to 18** built-in attack recipes sourced from top-tier international conferences.

Some of the most commonly used top-tier Recipes include:
*   **`textfooler`**: A classic attack based on word embedding synonym substitution (relatively fast and the most popular).
*   **`bert-attack` / `bae`**: Uses Masked Language Models (like BERT itself) to generate contextually coherent replacement words (produces very natural sentences but is extremely slow).
*   **`textbugger` / `deepwordbug`**: Attacks via character insertion, deletion, or simulating human typing errors (character-level attacks).
*   **`hotflip`**: A white-box attack recipe.
*   **`checklist`**: A recipe for behavioral testing by replacing names, locations, numbers, etc.
*   Others include **`pwws`**, **`alzantot`** (genetic algorithm), **`iga`**, and more.
*   

## Misc



### Question 1: Can TextAttack be used to improve a model's adversarial robustness through different training datasets (Adversarial Training)?

**The answer is: Absolutely. In fact, this is one of its core functions.**

The full title of the official TextAttack paper is: *“TextAttack: A Framework for Adversarial Attacks, **Data Augmentation, and Adversarial Training** in NLP.”*

TextAttack provides two primary methods to enhance model robustness:
1.  **Data Augmentation**: You can use the `textattack augment` command. It takes an existing clean dataset and applies various "perturbations" (such as typos or synonym substitutions) to generate a large number of new samples. By adding these samples to your training set, you allow the model to encounter more "traps" during training.
2.  **Adversarial Training**: TextAttack even includes a built-in `textattack train` command. During this training loop, TextAttack dynamically generates adversarial examples in every epoch and feeds them to the model. As the model undergoes this continuous cycle of being "attacked" and "self-correcting," its adversarial robustness improves significantly.

---

### Question 2: What do `Correct/Whole: 883/1000` and `Accuracy: 88.30%` represent in the model results?

These figures represent the model's **"Baseline Performance"** on the clean (original) test set before any attacks are applied.

Here is the specific breakdown:
*   **Whole (1000)**: This indicates that TextAttack extracted a total of **1,000** samples from the test dataset for evaluation.
*   **Correct (883)**: This means that out of those 1,000 samples, the model **predicted the correct label** for 883 of them initially.
*   **Accuracy (88.30%)**: This is simply 883 divided by 1,000, showing that the model's inherent accuracy is 88.30%.

**Why is this data critical for TextAttack?**
As mentioned in our previous discussion, TextAttack’s core logic is to **"only attack samples that the model predicted correctly."** 
Therefore, in this set of 1,000 samples, there are 117 samples that the model already got wrong. TextAttack will **skip** these 117 samples; the actual adversarial attack will only be carried out on the 883 correctly predicted samples.

---



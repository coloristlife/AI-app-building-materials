To understand why models are classified as **encoder-only**, **decoder-only**, or **bidirectional**, it helps to look at the original Transformer architecture introduced in 2017. 

The original Transformer was a sequence-to-sequence model designed for machine translation (e.g., translating English to French). It consisted of two main parts:
1. **An Encoder:** To analyze and understand the input text (English).
2. **A Decoder:** To take that understanding and generate the output text (French) word by word.

Over time, researchers realized they didn't always need both parts. By using just the encoder or just the decoder, they could build highly specialized models for different tasks.

---

### 1. Encoder-Only Models (and what "Bidirectional" means)

**Encoder-only models** use only the first half of the original Transformer. 
* **Key examples:** BERT, RoBERTa, ALBERT.
* **Primary use case:** Natural Language Understanding (NLU). This includes tasks like sentiment analysis, text classification, named entity recognition, and extractive question-answering.

#### What does "Bidirectional" mean here?
In an encoder-only model, the attention mechanism is **unmasked**. This means that when the model processes a specific word in a sentence, it can look at (or "attend to") all the words that come before it *and* all the words that come after it at the same time. 

For example, in the sentence:  
*"The bank of the river was muddy."*

To understand what the word **"bank"** means, the model needs context from both sides. It looks left to see "The" and right to see "of the river." Because it looks in both directions simultaneously, this is called **bidirectional representation**. 

Since encoder-only models see the whole sentence at once, they are excellent at understanding context, but they are not well-suited for generating long, coherent passages of new text.

---

### 2. Decoder-Only Models

**Decoder-only models** use only the second half of the original Transformer. 
* **Key examples:** GPT-4, LLaMA, Claude, Mistral.
* **Primary use case:** Natural Language Generation (NLG). This includes tasks like writing essays, writing code, summarizing, and conversational AI.

#### How do they work?
Unlike encoders, decoder-only models generate text one token (word or word-piece) at a time, from left to right. This is called **autoregressive generation**. 

To do this successfully during training, the model must be prevented from "cheating." If it could look ahead at the words it is supposed to predict, it wouldn't learn how to generate them. Therefore, decoder-only models use **masked self-attention** (also called **causal attention**). 

When predicting the next word, a decoder-only model is strictly **unidirectional**—it can only look at the words that came before it, not the words that come after. 

For example, if the model has generated:  
*"The cat sat on the..."*  

It can only use those five words to predict the next word ("mat", "couch", etc.). It cannot look "into the future."

---

### Summary of Differences

| Feature | Encoder-Only | Decoder-Only |
| :--- | :--- | :--- |
| **Attention Type** | **Bidirectional** (looks at past and future tokens) | **Causal / Unidirectional** (looks only at past tokens) |
| **Primary Goal** | Understanding the input text | Generating new text |
| **Training Objective** | Masked Language Modeling (predicting missing words in the middle of a sentence) | Causal Language Modeling (predicting the very next word) |
| **Famous Examples** | BERT, RoBERTa | GPT series, LLaMA, Claude |
| **Best For...** | Classification, search, sentiment analysis | Chatbots, creative writing, coding assistants |

*(Note: There is also a third category, **Encoder-Decoder models** like T5 or BART, which keep both parts. These are often used for tasks that require both deep understanding and generation, such as document summarization or language translation).*

---

### I. Are these three models fine-tuned?


They are all **Pre-trained Base Models**:

1.  **`google-bert/bert-base-uncased`**: This is the original BERT base model released by Google. It has only undergone pre-training for Masked Language Modeling (MLM) and Next Sentence Prediction (NSP) and is not designed for any specific task.
2.  **`answerdotai/ModernBERT-base`**: This is a modernized BERT base model released by Answer.AI. Similarly, it only possesses general language representation capabilities and has no fine-tuning.
3.  **`FacebookAI/xlm-roberta-base`**: This is a multilingual base model released by Meta. It has also not been fine-tuned for any specific classification task.
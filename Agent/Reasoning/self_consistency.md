# Advanced Prompt Engineering — Self-Consistency, Tree-of-Thoughts, RAG
- https://medium.com/@sulbha.jindal/advanced-prompt-engineering-self-consistency-tree-of-thoughts-rag-17a2d2c8fb79

## Decoding strategies for text generation

Decoding strategies are crucial in text generation for decoder-only Large Language Models (LLMs). These models generate text sequentially, predicting each token based on the previous context. At each step, the LLM calculates logits, assigning scores to every possible token in its vocabulary, creating a probability distribution. Decoding is the process of converting these probability distributions into actual text. Various decoding methods exist, each with its own approach to selecting the next token from the distribution. These strategies aim to balance factors such as coherence, diversity, and relevance in the generated text, playing a vital role in shaping the final output of LLMs like ChatGPT or Claude.

**Greedy decoding** — Greedy decoding is a deterministic method for text generation in Large Language Models (LLMs) that always selects the token with the highest probability at each step. This approach is equivalent to sampling with a temperature of 0, ensuring consistent outputs for identical prompts. While greedy decoding is fast and efficient, it has limitations. The method’s focus on individual token probabilities can lead to repetitive loops and less creative outputs, as it ignores the broader probability space. Compared to stochastic decoding methods, which better capture output diversity, greedy decoding tends to produce more predictable results. This trade-off between efficiency and creativity makes greedy decoding suitable for certain applications but potentially limiting for tasks requiring more varied or innovative language generation.


**Sampling** — Sampling is a stochastic decoding method for text generation in Large Language Models (LLMs) that introduces randomness into the process. Unlike greedy decoding, sampling selects each subsequent token based on the model’s predicted probability distribution, rather than always choosing the most likely option. This approach allows for greater diversity in the generated text, as the sampled token isn’t guaranteed to have the highest individual probability. By better exploring the full range of potential outputs at each step, sampling helps avoid repetitive loops and enables more creative and varied results. The stochasticity in sampling can be controlled through various parameters, allowing for a balance between coherence and diversity in the generated text. This method enhances the model’s capacity to produce a wider array of outputs, showcasing the breadth of possibilities within the language model’s capabilities.


# code sample
- https://colab.research.google.com/github/NirDiamant/Prompt_Engineering/blob/main/all_prompt_engineering_techniques/self-consistency.ipynb#scrollTo=UO_ehkWer9WX

- https://levelup.gitconnected.com/building-the-entire-rag-ecosystem-and-optimizing-every-component-8f23349b96a4#8cd5

Impact of Long Context

A recurring theme in RAG has been the limited context windows of LLMs. But with the rise of models boasting massive context windows (128k, 200k, or even 1 million tokens), a question arises:

<img width="4800" height="1130" alt="image" src="https://github.com/user-attachments/assets/a907d9cf-8df1-4388-a229-1823482a42db" />

Do we still need RAG? Can we just stuff all our documents into the prompt?

The answer is nuanced. While long context models are incredibly powerful, they are not a silver bullet.

Research has shown that their performance can degrade when the crucial information is buried in the middle of a very long context (the “needle in a haystack” problem).

RAG Advantage: RAG excels at finding the needle first and presenting only that to the LLM. It’s a precision tool.
Long Context’s Advantage: Long context models are fantastic for tasks that require synthesizing information from many different parts of a document simultaneously, something RAG might miss.
The future is likely a hybrid approach: using RAG to perform an initial, precise retrieval of the most relevant documents and then feeding this high-quality, pre-filtered context into a long-context model for final synthesis.

For a deep dive into this topic, this presentation is an excellent resource:

Slides on Long Context: [The Impact of Long Context on RAG](https://docs.google.com/presentation/d/1mJUiPBdtf58NfuSEQ7pVSEQ2Oqmek7F1i4gBwR6JDss/edit#slide=id.g26c0cb8dc66_0_0)

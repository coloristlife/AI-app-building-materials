- https://github.com/NirDiamant/RAG_Techniques?tab=readme-ov-file

  
Overview 🔎

A dynamic approach that combines retrieval-based and generation-based methods, adaptively deciding whether to use retrieved information and how to best utilize it in generating responses.

Implementation 🛠️

• Implement a multi-step process including retrieval decision, document retrieval, relevance evaluation, response generation, support assessment, and utility evaluation to produce accurate, relevant, and useful outputs.


- https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_self_rag/


Self-RAG is a strategy for RAG that incorporates self-reflection / self-grading on retrieved documents and generations.

<img width="1692" height="628" alt="image" src="https://github.com/user-attachments/assets/b96bea87-484d-40b0-932f-406f41f4954a" />


- https://levelup.gitconnected.com/building-the-entire-rag-ecosystem-and-optimizing-every-component-8f23349b96a4#8cd5

Self-RAG: This approach takes it a step further. At each step, it uses an LLM to generate “reflection tokens” that critique the process. It grades the retrieved documents for relevance. If they’re not relevant, it retrieves again. Once it has good documents, it generates an answer and then grades that answer for factual consistency, ensuring it’s grounded in the source documents.


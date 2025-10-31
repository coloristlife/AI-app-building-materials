HyDE

- https://diamantai.substack.com/p/hyde-exploring-hypothetical-document

- https://github.com/NirDiamant/RAG_Techniques/tree/main?tab=readme-ov-file

  
Let's break down the HyDE process step by step:

1. Query Input: The user submits a query or question.

2. Hypothetical Document Generation: An instruction-following LLM (like GPT-4o) creates a possible answer to the query. This "hypothetical document" captures relevance patterns but may contain factual errors.

3. Document Encoding: An unsupervised contrastively learned encoder (like Contriever) converts the hypothetical document into an embedding vector.

4. Similarity Search: The system uses this vector to find similar real documents in the corpus based on vector similarity.

5. Result Retrieval: The most similar real documents are returned as the search results. 

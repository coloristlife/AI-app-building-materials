
- https://github.com/NirDiamant/RAG_Techniques?tab=readme-ov-file

Applying advanced scoring mechanisms to improve the relevance ranking of retrieved results.

Implementation 🛠️

🧠 LLM-based Scoring: Use a language model to score the relevance of each retrieved chunk.

🔀 Cross-Encoder Models: Re-encode both the query and retrieved documents jointly for similarity scoring.

🏆 Metadata-enhanced Ranking: Incorporate metadata into the scoring process for more nuanced ranking.

Additional Resources 📚

Relevance Revolution: [How Re-ranking Transforms RAG Systems](https://diamantai.substack.com/p/relevance-revolution-how-re-ranking?r=336pe4&utm_campaign=post&utm_medium=web&triedRedirect=true) 

A comprehensive blog post exploring the power of re-ranking in enhancing RAG system performance.


# Reranking Methods in RAG Systems

- https://github.com/NirDiamant/RAG_Techniques/blob/main/all_rag_techniques/reranking.ipynb

- https://levelup.gitconnected.com/building-an-agentic-deep-thinking-rag-pipeline-to-solve-complex-queries-af69c5e044db#437f

The key difference is how these models work.

Our initial retrieval uses a bi-encoder (the embedding model), which creates a vector for the query and documents independently. It’s fast and great for searching over millions of items.
A cross-encoder, on the other hand, takes the query and a single document together as a pair and performs a much deeper, more nuanced comparison. It’s slower, but far more accurate.

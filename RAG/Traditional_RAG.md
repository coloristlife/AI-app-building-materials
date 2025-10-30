# Traditional RAG
https://medium.com/@robertdennyson/pathrag-the-enterprise-knowledge-graph-roadmap-from-data-burden-to-corporate-wisdom-and-3d832ff24148


even the most enlightened RAG pipelines often fall back on a blunt instrument: Top-K retrieval. Top-K simply picks the K most similar chunks to your query — no matter how disconnected they might be. This approach suffers from several critical issues:

Contextual Myopia: 
Top-K treats relevance as a one-off score, ignoring how chunks relate to each other. You might retrieve ten brilliant facts — but none of them connect in a way that answers your multi-step question.

Redundancy & Noise: 
Similarity scores tend to cluster around certain topics, dragging in overlapping passages that add little new insight yet bloat your prompt.

Arbitrary Cutoffs: 
Choosing K is a guessing game. Too small, and you miss key evidence; too large, and you overwhelm your model with tangential information.

No Explanation Path: With Top-K, you can’t trace how one fact led to the next. You simply get a bag of “relevant” snippets and hope the LLM knits them together coherently.
In short, traditional RAG sees data as data — raw, unstructured, and indiscriminately collected.

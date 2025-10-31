
HyPE-RAG

- https://www.machinelearningplus.com/gen-ai/hype-rag-how-hypothetical-prompt-embeddings-solve-question-matching-in-retrieval-systems/?utm_source=chatgpt.com


---
# from AI

  HyPE is a retrieval-enhancement technique introduced in the preprint “Bridging the Question-Answer Gap in RAG: Hypothetical Prompt Embeddings” by Vake et al. (2025). The core idea: instead of embedding document chunks directly (or embedding queries and matching to chunks), HyPE pre-generates hypothetical prompts (i.e., questions) for each chunk during the indexing phase, and then stores embeddings of those hypothetical prompts (while linking to the original chunk).

  At query (runtime) time, a user’s question is embedded and matched to those stored hypothetical question embeddings, rather than matching directly to chunk content. Then the chunk(s) behind the matched hypothetical prompt(s) are retrieved.

  Because the hypothetical prompts align query style (questions) with chunk style (answers/explanations), the “style gap” between user queries and document text is reduced. HyPE claims improvements of up to ~42 percentage points in retrieval precision and ~45 points in recall versus a baseline.

HyDE = query-time generation of “fake answer document” → embed → retrieve.

HyPE = indexing-time generation of hypothetical prompts/questions for each chunk → embed → retrieval is question-to-question.

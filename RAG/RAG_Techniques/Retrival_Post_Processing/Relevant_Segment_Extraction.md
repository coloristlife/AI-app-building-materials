Relevant Segment Extraction (RSE)

https://github.com/NirDiamant/RAG_Techniques/tree/main?tab=readme-ov-file


# from AI

**What RSE is**

Relevant Segment Extraction (RSE) is a technique applied after initial retrieval in a RAG pipeline. Rather than just taking the top-K retrieved chunks (each chunk being a fixed size piece of text), RSE groups, merges or expands those chunks into longer, coherent text segments that better reflect the original document structure and provide richer context. For example: instead of retrieving three disjoint paragraphs, RSE might merge them (if they come from the same nearby region in a document) into a full section of text that spans many paragraphs. A core description:

“RSE is a query-time post-processing step that takes clusters of relevant chunks and intelligently combines them into longer sections of text that we call segments.” 

“Relevant Segment Extraction … is a post-processing step that takes clusters of relevant chunks and intelligently combines them into longer sections of text …” 

In short: RSE = retrieve chunks → identify which chunks belong together for the query → form a more coherent segment.

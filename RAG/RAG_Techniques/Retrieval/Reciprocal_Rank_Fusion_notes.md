- https://levelup.gitconnected.com/building-an-agentic-deep-thinking-rag-pipeline-to-solve-complex-queries-af69c5e044db#4ff4
  - Vector Search: Our standard semantic search, but now upgraded to use metadata filters.
  - Keyword Search (BM25): A classic, powerful algorithm that excels at finding documents with specific, exact terms.
  - Hybrid Search: A best of both the approaches is to combines the results of vector and keyword search using a technique called Reciprocal Rank Fusion (RRF).
 
~~~
  # Strategy 1: Pure Vector Search with Metadata Filtering
def vector_search_only(query: str, section_filter: str = None, k: int = 10):
    # This dictionary defines the metadata filter. ChromaDB will only search documents that match this.
    filter_dict = {"section": section_filter} if section_filter and "Unknown" not in section_filter else None
    # Perform the similarity search with the optional filter
    return advanced_vector_store.similarity_search(query, k=k, filter=filter_dict)


# Strategy 2: Pure Keyword Search (BM25)
def bm25_search_only(query: str, k: int = 10):
    # Tokenize the incoming query
    tokenized_query = query.split(" ")
    # Get the BM25 scores for the query against all documents in the corpus
    bm25_scores = bm25.get_scores(tokenized_query)
    # Get the indices of the top k documents
    top_k_indices = np.argsort(bm25_scores)[::-1][:k]
    # Use our doc_map to return the full Document objects for the top results
    return [doc_map[doc_ids[i]] for i in top_k_indices]

# Strategy 3: Hybrid Search with Reciprocal Rank Fusion (RRF)
def hybrid_search(query: str, section_filter: str = None, k: int = 10):
    # 1. Perform a keyword search
    bm25_docs = bm25_search_only(query, k=k)
    # 2. Perform a semantic search with the metadata filter
    semantic_docs = vector_search_only(query, section_filter=section_filter, k=k)
    # 3. Combine and re-rank the results using Reciprocal Rank Fusion (RRF)
    # Get a unique set of all documents found by either search method
    all_docs = {doc.metadata["id"]: doc for doc in bm25_docs + semantic_docs}.values()
    # Create lists of just the document IDs from each search result
    ranked_lists = [[doc.metadata["id"] for doc in bm25_docs], [doc.metadata["id"] for doc in semantic_docs]]
    
    # Initialize a dictionary to store the RRF scores for each document
    rrf_scores = {}
    # Loop through each ranked list (BM25 and Semantic)
    for doc_list in ranked_lists:
        # Loop through each document ID in the list with its rank (i)
        for i, doc_id in enumerate(doc_list):
            if doc_id not in rrf_scores:
                rrf_scores[doc_id] = 0
            # The RRF formula: add 1 / (rank + k) to the score. We use k=61 as a standard default.
            rrf_scores[doc_id] += 1 / (i + 61) 
    # Sort the document IDs based on their final RRF scores in descending order
    sorted_doc_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)
    # Return the top k Document objects based on the fused ranking
    final_docs = [doc_map[doc_id] for doc_id in sorted_doc_ids[:k]]
    return final_docs
print("\nAll retrieval strategy functions ready.")
~~~

We have now implemented the core of our adaptive retrieval system.

  - The vector_search_only function is our upgraded semantic search. The key addition is the filter=filter_dict argument, which allows us to pass the document_section from our planner's Step and force the search to only consider chunks with that metadata.
  - The bm25_search_only function is our pure keyword retriever. It's incredibly fast and effective for finding specific terms that semantic search might miss.
  - The hybrid_search function runs both searches in parallel and then intelligently merges the results using RRF. RRF is a simple but powerful algorithm that ranks documents based on their position in each list, effectively giving more weight to documents that appear high up in both search results.

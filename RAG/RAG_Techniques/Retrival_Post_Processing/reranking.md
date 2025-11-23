
# Reranking Methods in RAG Systems 

- https://github.com/NirDiamant/RAG_Techniques?tab=readme-ov-file

Applying advanced scoring mechanisms to improve the relevance ranking of retrieved results.

Implementation 🛠️

🧠 LLM-based Scoring: Use a language model to score the relevance of each retrieved chunk.

🔀 Cross-Encoder Models: Re-encode both the query and retrieved documents jointly for similarity scoring.

🏆 Metadata-enhanced Ranking: Incorporate metadata into the scoring process for more nuanced ranking.

Additional Resources 📚

Relevance Revolution: [How Re-ranking Transforms RAG Systems](https://diamantai.substack.com/p/relevance-revolution-how-re-ranking?r=336pe4&utm_campaign=post&utm_medium=web&triedRedirect=true) 

A comprehensive blog post exploring the power of re-ranking in enhancing RAG system performance.


# LLM based vs CrossEncoder 

- https://github.com/NirDiamant/RAG_Techniques/blob/main/all_rag_techniques/reranking.ipynb

- https://levelup.gitconnected.com/building-an-agentic-deep-thinking-rag-pipeline-to-solve-complex-queries-af69c5e044db#437f

The key difference is how these models work.

1. Our initial retrieval uses a bi-encoder (the embedding model), which creates a vector for the query and documents independently. It’s fast and great for searching over millions of items.
2. A cross-encoder, on the other hand, takes the query and a single document together as a pair and performs a much deeper, more nuanced comparison. It’s slower, but far more accurate.


# CohereRerank
- https://levelup.gitconnected.com/building-the-entire-rag-ecosystem-and-optimizing-every-component-8f23349b96a4#8177

Using CohereRerank

<img width="2000" height="546" alt="image" src="https://github.com/user-attachments/assets/6c33436d-d81b-4a7a-9691-22d5c10cb79e" />

This ensures that the most relevant documents are placed at the very top of the context we provide to the LLM.

We have already seen one powerful re-ranking method: Reciprocal Rank Fusion (RRF) in our RAG-Fusion section. It’s a great, model-free way to combine results. But for an even more powerful approach, we can use a dedicated re-ranking model, like the one provided by Cohere.

Let’s set up a standard retriever first. We’ll use the same blog post from our previous examples.

~~~
# Load, split, and index the document
loader = WebBaseLoader(web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",))
blog_docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=300, chunk_overlap=50)
splits = text_splitter.split_documents(blog_docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# First-pass retriever: get the top 10 potentially relevant documents
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
~~~

Now, we introduce the ContextualCompressionRetriever. This special retriever wraps our base retriever and adds a "compressor" step. Here, our compressor will be the CohereRerank model.

It will take the 10 documents from our base retriever and re-order them, returning only the most relevant ones.

~~~
# You will need to install cohere: pip install cohere
# And set your COHERE_API_KEY environment variable
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank

# Initialize the Cohere Rerank model
compressor = CohereRerank()

# Create the compression retriever
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, 
    base_retriever=retriever
)

# Let's test it with our query
question = "What is task decomposition for LLM agents?"
compressed_docs = compression_retriever.get_relevant_documents(question)

# Print the re-ranked documents
print("--- Re-ranked and Compressed Documents ---")
for doc in compressed_docs:
    print(f"Relevance Score: {doc.metadata['relevance_score']:.4f}")
    print(f"Content: {doc.page_content[:150]}...\n")


#### OUTPUT ####
--- Re-ranked and Compressed Documents ---
Relevance Score: 0.9982
Content: Task decomposition can be done (1) by LLM with simple prompting like "Steps for XYZ.", "What are the subgoals for achieving XYZ?", (2) by using task...

Relevance Score: 0.9851
Content: Tree of Thoughts (Yao et al. 2023) extends CoT by exploring multiple reasoning possibilities at each step. It first decomposes the problem into mult...

Relevance Score: 0.9765
Content: LLM-powered autonomous agents have been an exciting concept. They can be used for task decomposition by prompting, using task-specific instructions, or ...
~~~

The output is remarkable. The CohereRerank model has not only re-ordered the documents but has also assigned a relevance_score to each one. We can now be much more confident that the context we pass to the LLM is of the highest quality, directly leading to better, more accurate answers.

## more examples using CrossEncoder:
https://levelup.gitconnected.com/building-an-advanced-agentic-rag-pipeline-that-mimics-a-human-thought-process-687e1fd79f61#a6e3

~~~
    query_embedding = list(embedding_model.embed([optimized_query]))[0]
    search_results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=20,          # Fetch more results upfront for reranking
        with_payload=True  # Include chunk metadata/content
    )
    print(f"  - Retrieved {len(search_results)} candidate chunks from vector store.")
    
    # 3. Re-rank results using a cross-encoder for semantic relevance
    rerank_pairs = [[optimized_query, result.payload['content']] for result in search_results]
    scores = cross_encoder_model.predict(rerank_pairs)
    
    # Attach re-rank scores to search results
    for i, score in enumerate(scores):
        search_results[i].score = score
    
    # Sort by descending re-rank score
    reranked_results = sorted(search_results, key=lambda x: x.score, reverse=True)
    print("  - Re-ranked the results using Cross-Encoder.")
    
    # 4. Select top-k results and format for return
    top_k = 5
    final_results = []
    for result in reranked_results[:top_k]:
        final_results.append({
            'source': result.payload['source'],   # Document source path
            'content': result.payload['content'], # Extracted text/table
            'summary': result.payload['summary'], # Pre-computed summary
            'rerank_score': float(result.score)   # Re-rank confidence score
        })
        
    print(f"  - Returning top {top_k} re-ranked chunks.")
    return final_results
~~~



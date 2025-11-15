HyDE

- https://diamantai.substack.com/p/hyde-exploring-hypothetical-document

- https://github.com/NirDiamant/RAG_Techniques/tree/main?tab=readme-ov-file

  
Let's break down the HyDE process step by step:

1. Query Input: The user submits a query or question.

2. Hypothetical Document Generation: An instruction-following LLM (like GPT-4o) creates a possible answer to the query. This "hypothetical document" captures relevance patterns but may contain factual errors.

3. Document Encoding: An unsupervised contrastively learned encoder (like Contriever) converts the hypothetical document into an embedding vector.

4. Similarity Search: The system uses this vector to find similar real documents in the corpus based on vector similarity.

5. Result Retrieval: The most similar real documents are returned as the search results. 



- https://levelup.gitconnected.com/building-the-entire-rag-ecosystem-and-optimizing-every-component-8f23349b96a4#9d43

This final technique is one of the most clever. The core problem of retrieval is that a user’s query might use different words than the document (the “vocabulary mismatch” problem).


<img width="1100" height="407" alt="image" src="https://github.com/user-attachments/assets/6cbca202-cd97-4806-91ae-903e9d6bd4d4" />


HyDE (Hypothetical Document Embeddings) proposes a radical solution: First, have an LLM generate a hypothetical answer to the question. This fake document, while not factually correct, will be semantically rich and use the kind of language we expect to find in a real answer.

We then embed this hypothetical document and use its embedding to perform the retrieval. The result is that we find real documents that are semantically very similar to an ideal answer.

Let’s start by creating a prompt to generate this hypothetical document.

~~~
# HyDE prompt
template = """Please write a scientific paper passage to answer the question
Question: {question}
Passage:"""
prompt_hyde = ChatPromptTemplate.from_template(template)

# Chain to generate the hypothetical document
generate_docs_for_retrieval = (
    prompt_hyde 
    | ChatOpenAI(temperature=0) 
    | StrOutputParser() 
)

# Generate and print the hypothetical document
hypothetical_document = generate_docs_for_retrieval.invoke({"question": question})
print(hypothetical_document)


#### OUTPUT ####
Task decomposition in large language model (LLM) agents refers to the
process of breaking down a complex, high-level task ...
~~~

This passage is a perfect, textbook-style answer. Now, we use its embedding to find real documents.

~~~
# Retrieve documents using the HyDE approach
retrieval_chain = generate_docs_for_retrieval | retriever 
retrieved_docs = retrieval_chain.invoke({"question": question})

# Use our standard RAG chain to generate the final answer from the retrieved context
final_rag_chain.invoke({"context": retrieved_docs, "question": question})

#### OUTPUT ####
Task decomposition for LLM agents involves breaking down a larger task
into smaller, more manageable subgoals. This can be done using techni ...
~~~

~~~
# Final synthesis prompt
template = """Here is a set of Q+A pairs:

{context}

Use these to synthesize an answer to the original question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

final_rag_chain = (
    prompt
    | llm
    | StrOutputParser()
)

~~~

~~~
# Final synthesis prompt
template = """Here is a set of Q+A pairs:

{context}

Use these to synthesize an answer to the original question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

final_rag_chain = (
    prompt
    | llm
    | StrOutputParser()
)

~~~

By using a hypothetical document as a lure, HyDE helped us zero in on the most relevant chunks in our knowledge base, demonstrating another powerful tool in our RAG toolkit.

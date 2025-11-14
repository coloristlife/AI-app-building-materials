# Multi-Query Generation

- https://levelup.gitconnected.com/building-the-entire-rag-ecosystem-and-optimizing-every-component-8f23349b96a4#8d22

A single user query represents just one perspective. Distance-based similarity search might miss relevant documents that use synonyms or discuss related concepts.

The Multi-Query approach tackles this by using an LLM to generate several different versions of the user’s question, effectively searching from multiple angles.

<img width="1100" height="357" alt="image" src="https://github.com/user-attachments/assets/5229153d-9c5b-4347-b768-7025a7324ba2" />

We’ll start by creating a prompt that instructs the LLM to generate these alternative questions.

~~~
from langchain.prompts import ChatPromptTemplate

# Prompt for generating multiple queries
template = """You are an AI language model assistant. Your task is to generate five 
different versions of the given user question to retrieve relevant documents from a vector 
database. By generating multiple perspectives on the user question, your goal is to help
the user overcome some of the limitations of the distance-based similarity search. 
Provide these alternative questions separated by newlines. Original question: {question}"""
prompt_perspectives = ChatPromptTemplate.from_template(template)

# Chain to generate the queries
generate_queries = (
    prompt_perspectives 
    | ChatOpenAI(temperature=0) 
    | StrOutputParser() 
    | (lambda x: x.split("\n"))
)
~~~
Let’s test this chain and see what kind of queries it generates for our question.

~~~
question = "What is task decomposition for LLM agents?"
generated_queries_list = generate_queries.invoke({"question": question})

# Print the generated queries
for i, q in enumerate(generated_queries_list):
    print(f"{i+1}. {q}")


#### OUTPUT ####
1. How can LLM agents break down complex tasks?
2. What is the process of task decomposition in the context of large language model agents?
3. What are the methods for decomposing tasks for LLM-powered agents?
4. Explain the concept of task decomposition as it applies to AI agents using LLMs.
5. In what ways do LLM agents handle task decomposition?

~~~
This is excellent. The LLM has rephrased our original question using different keywords like “break down complex tasks”, “methods”, and “process.” Now, we can retrieve documents for all of these queries and combine the results. A simple way to combine them is to take the unique set of all retrieved documents.


~~~
from langchain.load import dumps, loads

def get_unique_union(documents: list[list]):
    """ A simple function to get the unique union of retrieved documents """
    # Flatten the list of lists and convert each Document to a string for uniqueness
    flattened_docs = [dumps(doc) for sublist in documents for doc in sublist]
    unique_docs = list(set(flattened_docs))
    return [loads(doc) for doc in unique_docs]

# Build the retrieval chain
retrieval_chain = generate_queries | retriever.map() | get_unique_union

# Invoke the chain and check the number of documents retrieved
docs = retrieval_chain.invoke({"question": question})
print(f"Total unique documents retrieved: {len(docs)}")


#### OUTPUT ####
Total unique documents retrieved: 6
~~~

By searching with five different queries, we retrieved a total of 6 unique documents, likely capturing a more comprehensive set of information than a single query would have. Now we can feed this context into our final RAG chain.

~~~
from operator import itemgetter

# The final RAG chain
template = """Answer the following question based on this context:

{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
llm = ChatOpenAI(temperature=0)

final_rag_chain = (
    {"context": retrieval_chain, "question": itemgetter("question")} 
    | prompt
    | llm
    | StrOutputParser()
)

final_rag_chain.invoke({"question": question})


#### OUTPUT ####
Task decomposition for LLM agents involves breaking down large,
complex tasks into smaller, more manageable sub-goals. This allows
the agent to work through a problem systematically. Methods for
decomposition include using the LLM itself with simple prompts ...
~~~
This answer is more robust because it’s based on a wider pool of relevant documents.

So itemgetter("question") simply pulls the value associated with the key "question" from the input.

Example:

If the input to final_rag_chain is:
~~~

{"question": "What is an agent?", "user_id": 12}

~~~
Then:

itemgetter("question") returns "What is an agent?"

It’s the same as doing:

~~~
lambda x: x["question"]
~~~

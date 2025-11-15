- https://levelup.gitconnected.com/building-the-entire-rag-ecosystem-and-optimizing-every-component-8f23349b96a4#9d43

Some questions are too complex to be answered in a single step. For example, “What are the main components of an LLM-powered agent, and how do they interact?” This is really two questions in one.


<img width="1100" height="357" alt="image" src="https://github.com/user-attachments/assets/42abe665-b7d9-40f3-b21e-1fec189d1a12" />


<img width="1100" height="327" alt="image" src="https://github.com/user-attachments/assets/ee866f76-fff5-4af5-be0e-d98de5f0ff93" />



The Decomposition technique uses an LLM to break down a complex query into a set of simpler, self-contained sub-questions. We can then answer each one and synthesize a final answer.

We’ll start with a prompt designed for this purpose.

~~~
# Decomposition prompt
template = """You are a helpful assistant that generates multiple sub-questions related to an input question. \n
The goal is to break down the input into a set of sub-problems / sub-questions that can be answers in isolation. \n
Generate multiple search queries related to: {question} \n
Output (3 queries):"""
prompt_decomposition = ChatPromptTemplate.from_template(template)

# Chain to generate sub-questions
generate_queries_decomposition = (
    prompt_decomposition 
    | ChatOpenAI(temperature=0) 
    | StrOutputParser() 
    | (lambda x: x.split("\n"))
)

# Generate and print the sub-questions
question = "What are the main components of an LLM-powered autonomous agent system?"
sub_questions = generate_queries_decomposition.invoke({"question": question})
print(sub_questions)


#### OUTPUT ####
[
 '1. What are the core components ... agent?',
 '2. How is memory implemented in LLM-po ... agents?',
 '3. What role does planning and task decomposition ... LLMs?'
]
~~~


The LLM successfully decomposed our complex question. Now, we can answer each of these individually and combine the results. One effective method is to answer each sub-question and use the resulting Q&A pairs as context to synthesize a final, comprehensive answer.


~~~
# RAG prompt
prompt_rag = hub.pull("rlm/rag-prompt")

# A list to hold the answers to our sub-questions
rag_results = []
for sub_question in sub_questions:
    # Retrieve documents for each sub-question
    retrieved_docs = retriever.get_relevant_documents(sub_question)
    
    # Use our standard RAG chain to answer the sub-question
    answer = (prompt_rag | llm | StrOutputParser()).invoke({"context": retrieved_docs, "question": sub_question})
    rag_results.append(answer)

def format_qa_pairs(questions, answers):
    """Format Q and A pairs"""
    formatted_string = ""
    for i, (question, answer) in enumerate(zip(questions, answers), start=1):
        formatted_string += f"Question {i}: {question}\nAnswer {i}: {answer}\n\n"
    return formatted_string.strip()

# Format the Q&A pairs into a single context string
context = format_qa_pairs(sub_questions, rag_results)

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

final_rag_chain.invoke({"context": context, "question": question})


#### OUTPUT ####
An LLM-powered autonomous agent system primarily consists of three
core components: planning, memory, and tool use. ...
~~~
By breaking the problem down, we constructed a much more detailed and structured answer than we would have otherwise.

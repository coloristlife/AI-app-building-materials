- https://levelup.gitconnected.com/building-an-agentic-deep-thinking-rag-pipeline-to-solve-complex-queries-af69c5e044db#95ca

# Optimizing Retrieval with a Query Rewriter Agent

The Query Rewriter: We’ll create a specialized agent to transform the planner’s simple sub-questions into highly effective, optimized search queries.

So, basically we have a plan with good sub-questions.

> But a question like “What are the risks?” isn’t a great search query. It’s too generic. Search engines, whether they are vector databases or web search, work best with specific, keyword-rich queries.

<img width="1100" height="464" alt="image" src="https://github.com/user-attachments/assets/1a24fb17-2b19-44c2-833b-3e9f136cc016" />


To fix this, we will build another small, specialized agent: the Query Rewriter. Its only job is to take the sub-question for the current step and make it better for searching by adding relevant keywords and context from what we’ve already learned.

First, let’s design the prompt for this new agent.

~~~
from langchain_core.output_parsers import StrOutputParser # To parse the LLM's output as a simple string

# The prompt for our query rewriter, instructing it to act as a search expert
query_rewriter_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a search query optimization expert. Your task is to rewrite a given sub-question into a highly effective search query for a vector database or web search engine, using keywords and context from the research plan.
The rewritten query should be specific, use terminology likely to be found in the target source (a financial 10-K or news articles), and be structured to retrieve the most relevant text snippets."""),
    ("human", "Current sub-question: {sub_question}\n\nRelevant keywords from plan: {keywords}\n\nContext from past steps:\n{past_context}")
])
~~~

We are basically telling this agent to act like a search query optimization expert. We are giving it **three pieces of information** to work with: the simple sub_question, the keywords our planner already identified, and the past_context from any previous research steps. This gives it all the raw material it needs to construct a much better query.

It is used as below in the whole RAG pipeline.
~~~
def retrieval_node(state: RAGState) -> Dict:
    # First, get the details for the current step in the plan.
    current_step_index = state["current_step_index"]
    current_step = state["plan"].steps[current_step_index]
    console.print(f"--- 🔍: Retrieving from 10-K (Step {current_step_index + 1}: {current_step.sub_question}) ---")
    
    # Use our query rewriter to optimize the sub-question for search.
    past_context = get_past_context_str(state['past_steps'])
    rewritten_query = query_rewriter_agent.invoke({
        "sub_question": current_step.sub_question,
        "keywords": current_step.keywords,
        "past_context": past_context
    })
    console.print(f"  Rewritten Query: {rewritten_query}")
    
    # Get the supervisor's decision on which retrieval strategy is best.
    retrieval_decision = retrieval_supervisor_agent.invoke({"sub_question": rewritten_query})
    console.print(f"  Supervisor Decision: Use `{retrieval_decision.strategy}`. Justification: {retrieval_decision.justification}")
~~~ 

Now we can initiate this agent. It’s a simple chain since we just need a string as output.

~~~
# Create the agent by piping the prompt to our reasoning LLM and a string output parser
query_rewriter_agent = query_rewriter_prompt | reasoning_llm | StrOutputParser()
print("Query Rewriter Agent created successfully.")

# Let's test the rewriter agent. We'll pretend we've already completed the first two steps of our plan.
print("\n--- Testing Query Rewriter Agent ---")

# Let's imagine we are at a final synthesis step that needs context from the first two.
test_sub_q = "How does AMD's 2024 AI chip strategy potentially exacerbate the competitive risks identified in NVIDIA's 10-K?"
test_keywords = ['impact', 'threaten', 'competitive pressure', 'market share', 'technological change']

# We create some mock "past context" to simulate what the agent would know at this point in a real run.
test_past_context = "Step 1 Summary: NVIDIA's 10-K lists intense competition and rapid technological change as key risks. Step 2 Summary: AMD launched its MI300X AI accelerator in 2024 to directly compete with NVIDIA's H100."

# Invoke the agent with our test data
rewritten_q = query_rewriter_agent.invoke({
    "sub_question": test_sub_q,
    "keywords": test_keywords,
    "past_context": test_past_context
})

print(f"Original sub-question: {test_sub_q}")
print(f"Rewritten Search Query: {rewritten_q}")
~~~~
To test this properly, we have to simulate a real scenario. We create a test_past_context string that represents the summaries the agent would have already generated from the first two steps of its plan. Then we feed this, along with the next sub-question, to our query_rewriter_agent.

Let’s look at the result.

~~~~
#### OUTPUT ####
Query Rewriter Agent created successfully.

--- Testing Query Rewriter Agent ---
Original sub-question: How does AMD 2024 AI chip strategy potentially exacerbate the competitive risks identified in NVIDIA 10-K?
Rewritten Search Query: analysis of how AMD 2024 AI
~~~~


The original question is for an analyst, he rewritten query is for a search engine. It has been assigned with specific terms like “MI300X”, “market share erosion” and “data center” all of which were synthesized from the keywords and past context.

A query like this is far more likely to retrieve exactly the right documents, making our entire system more accurate and efficient. This rewriting step will be a crucial part of our main agentic loop.

- https://levelup.gitconnected.com/building-an-agentic-deep-thinking-rag-pipeline-to-solve-complex-queries-af69c5e044db#95ca

The Tool-Aware Planner: We will build an LLM-powered agent whose sole job is to decompose the user’s query into a structured Plan object, deciding which tool to use for each step.

To do this, we will create a dedicated Planner Agent. We need to give it a very clear set of instructions, or a prompt, that tells it exactly what its job is.

~~~
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from rich.pretty import pprint as rprint

# The system prompt that instructs the LLM how to behave as a planner
planner_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert research planner. Your task is to create a clear, multi-step plan to answer a complex user query by retrieving information from multiple sources.
You have two tools available:
1. `search_10k`: Use this to search for information within NVIDIA's 2023 10-K financial filing. This is best for historical facts, financial data, and stated company policies or risks from that specific time period.
2. `search_web`: Use this to search the public internet for recent news, competitor information, or any topic that is not specific to NVIDIA's 2023 10-K.
Decompose the user's query into a series of simple, sequential sub-questions. For each step, decide which tool is more appropriate.
For `search_10k` steps, also identify the most likely section of the 10-K (e.g., 'Item 1A. Risk Factors', 'Item 7. Management's Discussion and Analysis...').
It is critical to use the exact section titles found in a 10-K filing where possible."""),
    ("human", "User Query: {question}") # The user's original, complex query
])
~~~

We are basically giving the LLM a new persona: an expert research planner. We explicitly tell it about the two tools it has at its disposal (search_10k and search_web) and give it guidance on when to use each one. This is the "tool-aware" part.

We are not just asking it for a plan but asking it to create a plan that maps directly to the capabilities we have built.

Now we can initiate the reasoning model and chain it together with our prompt. A very important step here is to tell the LLM that its final output must be in the format of our Pydantic Plan class. This makes the output structured and predictable.

~~~
from langchain_core.documents import Document
from langchain_core.pydantic_v1 import BaseModel, Field

# Pydantic model for a single step in the agent's reasoning plan
class Step(BaseModel):
    # A specific, answerable sub-question for this research step
    sub_question: str = Field(description="A specific, answerable question for this step.")
    # The agent's justification for why this step is necessary
    justification: str = Field(description="A brief explanation of why this step is necessary to answer the main query.")
    # The specific tool to use for this step: either internal document search or external web search
    tool: Literal["search_10k", "search_web"] = Field(description="The tool to use for this step.")
    # A list of critical keywords to improve the accuracy of the search
    keywords: List[str] = Field(description="A list of critical keywords for searching relevant document sections.")
    # (Optional) A likely document section to perform a more targeted, filtered search within
    document_section: Optional[str] = Field(description="A likely document section title (e.g., 'Item 1A. Risk Factors') to search within. Only for 'search_10k' tool.")


# Pydantic model for the overall plan, which is a list of individual steps
class Plan(BaseModel):
    # A list of Step objects that outlines the full research plan
    steps: List[Step] = Field(description="A detailed, multi-step plan to answer the user's query.")

~~~


~~~
# Initialize our powerful reasoning model, as defined in the config
reasoning_llm = ChatOpenAI(model=config["reasoning_llm"], temperature=0)

# Create the planner agent by piping the prompt to the LLM and instructing it to use our structured 'Plan' output
planner_agent = planner_prompt | reasoning_llm.with_structured_output(Plan)
print("Tool-Aware Planner Agent created successfully.")

# Let's test the planner agent with our complex query to see its output
print("\n--- Testing Planner Agent ---")
test_plan = planner_agent.invoke({"question": complex_query_adv})

s# Use rich's pretty print for a clean, readable display of the Pydantic object
rprint(test_plan)
~~~
We take our planner_prompt, pipe it to our powerful reasoning_llm, and then use the .with_structured_output(Plan) method. This tells LangChain to use the model function-calling abilities to format its response as a JSON object that perfectly matches our Plan Pydantic schema. This is much more reliable than trying to parse a plain text response.

Let’s look at the output when we test it with our challenge query.

~~~
#### OUTPUT ####
Tool-Aware Planner Agent created successfully.

--- Testing Planner Agent ---
Plan(
│   steps=[
│   │   Step(
│   │   │   sub_question="What are the key risks related to competition as stated in NVIDIA's 2023 10-K filing?",
│   │   │   justification="This step is necessary to extract the foundational information about competitive risks directly from the source document as requested by the user.",
│   │   │   tool='search_10k',
│   │   │   keywords=['competition', 'risk factors', 'semiconductor industry', 'competitors'],
│   │   │   document_section='Item 1A. Risk Factors'
│   │   ),
│   │   Step(
│   │   │   sub_question="What are the recent news and developments in AMD's AI chip strategy in 2024?",
│   │   │   justification="This step requires finding up-to-date, external information that is not available in the 2023 10-K filing. A web search is necessary to get the latest details on AMD's strategy.",
│   │   │   tool='search_web',
│   │   │   keywords=['AMD', 'AI chip strategy', '2024', 'MI300X', 'Instinct accelerator'],
│   │   │   document_section=None
│   │   )
│   ]
)
~~~

If we look at the output you can see that the agent didn’t just give us a vague plan, it produced a structured Plan object. It correctly identified that the query has two parts.

For the first part, it knew the answer was in the 10-K and chose the search_10k tool, even correctly guessing the right document section.
For the second part, it knew "news from 2024" couldn't be in a 2023 document and correctly chose the search_web tool. This is the first sign our pipeline will give promising result at least in the thinking process.

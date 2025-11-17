- https://levelup.gitconnected.com/building-the-entire-rag-ecosystem-and-optimizing-every-component-8f23349b96a4

# Logical Routing

Routing is a classification problem. Given a user’s question, we need to classify it into one of several predefined categories. While traditional ML models can do this, we can leverage the powerful reasoning engine we already have: the LLM itself.

<img width="720" height="555" alt="image" src="https://github.com/user-attachments/assets/0fdb7262-4252-4c2b-8f81-75bc680def7f" />

By providing the LLM with a clear schema (a set of possible categories), we can ask it to make the classification decision for us.

We’ll start by defining the “contract” for our LLM’s output using a Pydantic model. This schema explicitly tells the LLM the possible destinations for a query.

~~~
from typing import Literal
from langchain_core.pydantic_v1 import BaseModel, Field

# Define the data model for our router's output
class RouteQuery(BaseModel):
    """A data model to route a user query to the most relevant datasource."""

    # The 'datasource' field must be one of the three specified literal strings.
    # This enforces a strict set of choices for the LLM.
    datasource: Literal["python_docs", "js_docs", "golang_docs"] = Field(
        ...,  # The '...' indicates that this field is required.
        description="Given a user question, choose which datasource would be most relevant for answering their question.",
    )
~~~


With our schema defined, we can now build the router chain. We’ll use a prompt to give the LLM its instructions and then use the .with_structured_output() method to ensure its response perfectly matches our RouteQuery model.

~~~
# Initialize our LLM
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

# Create a new LLM instance that is "structured" to output our Pydantic model
structured_llm = llm.with_structured_output(RouteQuery)

# The system prompt provides the core instruction for the LLM's task.
system = """You are an expert at routing a user question to the appropriate data source.

Based on the programming language the question is referring to, route it to the relevant data source."""

# The full prompt template combines the system message and the user's question.
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

# Define the complete router chain
router = prompt | structured_llm
~~~


Now, let’s test our router. We’ll pass it a question that is clearly about Python and inspect the output.

~~~
question = """Why doesn't the following code work:

from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(["human", "speak in {language}"])
prompt.invoke("french")
"""

# Invoke the router and check the result
result = router.invoke({"question": question})

print(result)


#### OUTPUT ####
datasource='python_docs'
~~~

The output is an instance of our RouteQuery model, and the LLM has correctly identified python_docs as the appropriate datasource. This structured output is now something we can reliably use in our code to implement branching logic.


~~~
def choose_route(result):
    """A function to determine the downstream logic based on the router's output."""
    if "python_docs" in result.datasource.lower():
        # In a real app, this would be a complete RAG chain for Python docs
        return "chain for python_docs"
    elif "js_docs" in result.datasource.lower():
        # This would be the chain for JavaScript docs
        return "chain for js_docs"
    else:
        # And this for Go docs
        return "chain for golang_docs"

# The full chain now includes the routing and branching logic
full_chain = router | RunnableLambda(choose_route)

# Let's run the full chain
final_destination = full_chain.invoke({"question": question})

print(final_destination)


#### OUTPUT ####
chain for python_docs
~~~

Our switchboard correctly routed the Python-related query. This approach is incredibly powerful for building multi-source RAG systems.



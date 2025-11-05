# Exploring Tree-of-Thoughts (ToT)
- https://blog.stackademic.com/comparing-reasoning-frameworks-react-chain-of-thought-and-tree-of-thoughts-b4eb9cdde54f

Conceptual Framework
Tree-of-Thoughts takes CoT to the next level. Instead of sticking to one path, it explores multiple possibilities at the same time. Think of it as brainstorming several solutions before picking the best one.

Core principles include:

  - Branching Paths: Explore different solutions simultaneously.
  
  - Evaluation: Compare paths to choose the best one.

Use Cases

ToT is great for:

  - Strategic Planning: Exploring various scenarios for business decisions.
  - Game AI: Finding the best moves in complex games.
  - Creative Thinking: Generating and comparing innovative ideas.

Example Implementation (LangChain)

Here’s an example of ToT in LangChain:

~~~
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

# Define a branching prompt
tot_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
    Question: {question}
    Let's consider multiple approaches to solving this problem.
    Option 1: ...
    Option 2: ...
    Evaluate the options and decide on the best one.
    Answer: ...
    """
)

# Initialize the LLM chain
llm = OpenAI(temperature=0.7)
chain = LLMChain(llm=llm, prompt=tot_prompt)

# Solve a problem
question = "How can we improve user engagement in an app?"
response = chain.run(question)
print(response)
~~~


# Tree of Thoughts
- https://langchain-ai.github.io/langgraph/tutorials/tot/tot/

It has three main steps:

Expand: generate 1 or more candidate solutions to the problem.
Score: measure the quality of the responses.
Prune: retain the top K best candidates
Then return to "Expand" if no solution is found (or if the solution is of insufficient quality).


  

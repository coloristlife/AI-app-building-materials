# Comparing Reasoning Frameworks: ReAct, Chain-of-Thought, and Tree-of-Thoughts

- https://blog.stackademic.com/comparing-reasoning-frameworks-react-chain-of-thought-and-tree-of-thoughts-b4eb9cdde54f

ReAct, short for Reasoning and Acting, helps AI agents think and act simultaneously. 
Imagine you’re solving a puzzle. Instead of planning everything at once, you take a step, see how it goes, then decide on your next move. That’s ReAct in action.

Core principles include:

- Feedback Loops: Learn from each action to improve the next.
- Context Awareness: Adjust actions based on real-time data.

Applications
ReAct is perfect for tasks where decisions depend on changing environments, such as:

- Robotics: Moving through unfamiliar spaces or picking up objects.
- Customer Support: Responding dynamically to user questions.
- Exploration: Learning as the agent works through tasks.

- <img width="400" height="752" alt="image" src="https://github.com/user-attachments/assets/5e43d298-a703-465d-a08e-473b52da2a44" />

~~~~
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

# Define tools the agent can use
def fetch_information(query):
    return f"Fetched result for: {query}"

fetch_tool = Tool(
    name="FetchTool",
    func=fetch_information,
    description="Fetches information based on the query"
)

# Initialize the agent
llm = OpenAI(temperature=0.5)
agent = initialize_agent(
    tools=[fetch_tool],
    llm=llm,
    agent_type="react"
)

# Use the agent
query = "What is the capital of France?"
response = agent.run(query)
print(response)

~~~~
# ReAct: The Power of Reasoning and Acting in LLM Agents
- https://sangeethasaravanan.medium.com/react-the-power-of-reasoning-and-acting-in-llm-agents-3332c95b1e25

ReAct enables LLMs to:

- Think aloud (chain-of-thought reasoning)
- Use tools (like calculators, search APIs, or databases)
- Store intermediate steps and decide next actions


example

~~~~
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.llms import OpenAI
from langchain.tools import DuckDuckGoSearchRun

# Initialize LLM
llm = OpenAI(temperature=0)

# Tools
search = DuckDuckGoSearchRun()
calculator = Tool(
    name="Calculator",
    func=lambda x: eval(x),
    description="Useful for math operations."
)

# Define toolset
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="Useful for answering factual current event questions"
    ),
    calculator
]

# Initialize ReAct-style Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.REACT_DOCSTORE,
    verbose=True
)

# Run a complex query
query = "Who is the president of the United States, and what is 25 multiplied by the number of letters in their last name?"
response = agent.run(query)

print(response)

~~~~

What the Agent Does Behind the Scenes:

1. Thought: I need to find out who the current president of the United States is.
2. Action: Search["current president of the United States"]
3. Observation: “Joe Biden”
4. Thought: Biden has 5 letters.
5. Action: Calculator["25 * 5"]
6. Observation: 125
7. Final Answer: 125


# ReAct Prompting
- https://www.promptingguide.ai/techniques/react

ReAct is a general paradigm that combines reasoning and acting with LLMs. ReAct prompts LLMs to generate verbal reasoning traces and actions for a task. This allows the system to perform dynamic reasoning to create, maintain, and adjust plans for acting while also enabling interaction to external environments (e.g., Wikipedia) to incorporate additional information into the reasoning.

To demonstrate how ReAct prompting works, let's follow an example from the paper.

The first step is to select cases from a training set (e.g., HotPotQA) and compose ReAct-format trajectories. These are used as few-shot exemplars in the prompts. The trajectories consist of multiple thought-action-observation steps as shown in the figure above. The free-form thoughts are used to achieve different tasks such as decomposing questions, extracting information, performing commonsense/arithmetic reasoning, guide search formulation, and synthesizing final answer.

Here is an example of what the ReAct prompt exemplars look like (obtained from the paper and shortened to one example for simplicity):

~~~~
Question What is the elevation range for the area that the eastern sector of the
Colorado orogeny extends into?
Thought 1 I need to search Colorado orogeny, find the area that the eastern sector
of the Colorado orogeny extends into, then find the elevation range of the
area.
Action 1 Search[Colorado orogeny]
Observation 1 The Colorado orogeny was an episode of mountain building (an orogeny) in
Colorado and surrounding areas.
Thought 2 It does not mention the eastern sector. So I need to look up eastern
sector.
Action 2 Lookup[eastern sector]
Observation 2 (Result 1 / 1) The eastern sector extends into the High Plains and is called
the Central Plains orogeny.
Thought 3 The eastern sector of Colorado orogeny extends into the High Plains. So I
need to search High Plains and find its elevation range.
Action 3 Search[High Plains]
Observation 3 High Plains refers to one of two distinct land regions
Thought 4 I need to instead search High Plains (United States).
Action 4 Search[High Plains (United States)]
Observation 4 The High Plains are a subregion of the Great Plains. From east to west, the
High Plains rise in elevation from around 1,800 to 7,000 ft (550 to 2,130
m).[3]
Thought 5 High Plains rise in elevation from around 1,800 to 7,000 ft, so the answer
is 1,800 to 7,000 ft.
Action 5 Finish[1,800 to 7,000 ft]
...
~~~~


# react from langchain 
- https://www.promptingguide.ai/techniques/react

~~~~
llm = OpenAI(model_name="text-davinci-003" ,temperature=0)
tools = load_tools(["google-serper", "llm-math"], llm=llm)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
~~~~

example prompt from https://smith.langchain.com/hub/hwchase17/react for langchain:

~~~~
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}

~~~~


  






# **Reflexive Metacognitive**
- https://levelup.gitconnected.com/building-17-agentic-ai-patterns-and-their-role-in-large-scale-ai-systems-f4915b5615ce#e49b

Our agents can now plan, handle errors, and even simulate the future. But they all share a critical vulnerability, they don’t know what they don’t know.

> A standard agent, if asked a question outside its expertise, will still try its best to answer, often leading to confident-sounding but dangerously wrong information.

This is where the Reflexive Metacognitive architecture comes in. This is one of the most advanced patterns …

> as it gives an agent a form of self-awareness. Before it even tries to solve a problem, it first reasons about its own capabilities, confidence, and limitations.

AI based healthcare or finance domain, this is a non-negotiable safety feature. It’s the mechanism that allows an agent to say “I don’t know” or “You should ask a human expert”. It’s the difference between a helpful assistant and a dangerous liability.

<img width="720" height="542" alt="image" src="https://github.com/user-attachments/assets/5bfc5b67-8ab2-427c-8e02-a3fa1d8e403a" />

1.Perceive Task: The agent receives a user request.

2.Metacognitive Analysis: The agent’s first step is to analyze the request against its own self-model. It assesses its confidence, its tools, and whether the query is within its predefined domain.

3.Strategy Selection: Based on this self-analysis, it chooses a strategy:

  - Reason Directly: For high-confidence, low-risk queries.
  - Use Tool: When the query requires a specific tool it knows it has.
  - Escalate/Refuse: For low-confidence, high-risk, or out-of-scope queries.
    
4. Execute Strategy: The chosen path is executed.

The foundation of this agent is its self-model. This isn’t just a prompt; it’s a structured piece of data that explicitly defines what the agent is and what it can do. We’ll create one for a medical triage assistant.

The foundation of this agent is its self-model. This isn’t just a prompt; it’s a structured piece of data that explicitly defines what the agent is and what it can do. We’ll create one for a medical triage assistant.

~~~
class AgentSelfModel(BaseModel):
    """A structured representation of the agent's capabilities and limitations."""
    name: str; role: str
    knowledge_domain: List[str]
    available_tools: List[str]

medical_agent_model = AgentSelfModel(
    name="TriageBot-3000",
    role="A helpful AI assistant for providing preliminary medical information.",
    knowledge_domain=["common_cold", "influenza", "allergies", "basic_first_aid"],
    available_tools=["drug_interaction_checker"]
)
~~~

Now for the core of the architecture: the metacognitive_analysis_node. This node's prompt forces the LLM to look at the user's query through the lens of the self-model and choose a safe strategy.

~~~
class MetacognitiveAnalysis(BaseModel):
    confidence: float
    strategy: str = Field(description="Must be one of: 'reason_directly', 'use_tool', 'escalate'.")
    reasoning: str

def metacognitive_analysis_node(state: AgentState):
    """The agent's self-reflection step."""
    console.print(Panel("🤔 Agent is performing metacognitive analysis...", title="[yellow]Step: Self-Reflection[/yellow]"))
    prompt = ChatPromptTemplate.from_template(
        """You are a metacognitive reasoning engine for an AI assistant. Your primary directive is SAFETY. Analyze the user's query in the context of the agent's own 'self-model' and choose the safest strategy.
        **WHEN IN DOUBT, ESCALATE.**
        **Agent's Self-Model:** {self_model}
        **User Query:** "{query}"
        """
    )
    chain = prompt | llm.with_structured_output(MetacognitiveAnalysis)
    analysis = chain.invoke({"query": state['user_query'], "self_model": state['self_model'].model_dump_json()})
    # ... (print analysis) ...
    return {"metacognitive_analysis": analysis}
~~~

<img width="664" height="716" alt="image" src="https://github.com/user-attachments/assets/9ec392a3-5ab2-4ddf-91dd-503e6db8a104" />

# Understanding the Blackboard Pattern
- https://medium.com/@dp2580/building-intelligent-multi-agent-systems-with-mcps-and-the-blackboard-pattern-to-build-systems-a454705d5672
  
The Blackboard Pattern consists of three key components:

- Blackboard: A shared knowledge repository where all information, hypotheses, and partial solutions are stored
- Knowledge Sources (Agents): Specialized problem-solvers that can read from and write to the blackboard
- Control Component: Orchestrates which agents should act when, based on the current state of the blackboard

  <img width="720" height="419" alt="image" src="https://github.com/user-attachments/assets/1d3ab45f-06ec-4d6d-831e-c18f3ce89246" />

- https://github.com/FareedKhan-dev/all-agentic-architectures/blob/main/07_blackboard.ipynb

Welcome to the seventh notebook in our series on agentic architectures. Today, we explore the Blackboard System, a powerful and highly flexible pattern for coordinating multiple specialist agents. This architecture is modeled on the idea of a group of human experts collaborating around a physical blackboard to solve a complex problem.

Instead of a rigid, predefined sequence of agent handoffs, a Blackboard system features a central, shared data store (the 'blackboard') where agents can read the current state of the problem and write their contributions. A dynamic Controller observes the blackboard and decides which specialist agent to activate next based on what is needed to move the solution forward. This allows for an opportunistic and emergent workflow.

To highlight its unique advantages, we will compare it to the sequential multi-agent system we built previously. We will present both systems with a complex financial query where the optimal path isn't a simple A → B → C sequence. We will demonstrate how the rigid sequential agent follows a suboptimal path, while the Blackboard system's dynamic Controller activates agents in a more logical, data-driven order, resulting in a more efficient and coherent analysis.

Definition
A Blackboard System is a multi-agent architecture where multiple specialist agents collaborate by reading from and writing to a shared, central data repository called the 'blackboard'. A controller or scheduler dynamically determines which agent should act next based on the evolving state of the solution on the blackboard.

High-level Workflow

- Shared Memory (The Blackboard): A central data structure holds the current state of the problem, including the user's request, intermediate findings, and partial solutions.
- Specialist Agents: A pool of independent agents, each with a specific expertise, continuously monitors the blackboard.
- Controller: A central 'controller' agent also monitors the blackboard. Its job is to analyze the current state and decide which specialist agent is best equipped to make the next contribution.
- Opportunistic Activation: The Controller activates the chosen agent. The agent reads the relevant data from the blackboard, performs its task, and writes its findings back to the blackboard.
- Iteration: The process repeats, with the Controller activating different agents in a dynamic sequence, until it determines that the solution on the blackboard is complete.

# whiteducksoftware/flock

We’ve developed an agent framework that uses blackboard orchestration as its main orchestration pattern:

https://github.com/whiteducksoftware/flock

With it, the flow you designed would take about ten lines of code, and you wouldn’t need to rely on agents or models being “smart enough” to know when to write to the blackboard via tools. 
We’ve also introduced visibility groups, which let you define exactly what each agent can see on the blackboard... so, for example, you can hide sensitive data like patient information from agents that shouldn’t access it.

- https://medium.com/@a.ratzenberger/complex-ai-agent-workflows-with-zero-prompts-7e2e971fd0f9
- https://github.com/whiteducksoftware/flock-showcase 
- https://whiteducksoftware.github.io/flock/guides/blackboard/


**Strengths & Weaknesses**

Strengths:

Flexibility & Adaptability: The workflow is not hardcoded; it emerges based on the problem, making the system highly adaptive.
Modularity: It's very easy to add or remove specialist agents without re-architecting the entire system.

Weaknesses:

Controller Complexity: The intelligence of the entire system depends heavily on the sophistication of the Controller. A naive Controller can lead to inefficient or looping behavior.
Debugging Challenges: The non-linear, emergent nature of the workflow can sometimes make it harder to trace and debug than a simple sequential process.

**What is a Blackboard?**
A blackboard is a shared memory space where:

  - Agents publish artifacts (typed data) when they complete work
  - Agents subscribe to artifact types they want to process
  - Workflows emerge from type-based subscriptions (no explicit wiring needed)
  - Execution is automatic (matching agents trigger when their data appears)
Key principle: Agents never call each other—they only interact through typed data on the blackboard.

**Blackboard vs Graph-Based Orchestration¶**
Graph-Based Approach¶

~~~
# Explicit workflow with hardcoded edges
workflow = StateGraph()

workflow.add_node("bug_detector", bug_detector_func)
workflow.add_node("security", security_func)
workflow.add_node("reporter", reporter_func)

# Manual wiring (tight coupling)
workflow.add_edge("bug_detector", "reporter")
workflow.add_edge("security", "reporter")

# Want to add performance_analyzer? Rewrite the graph!
~~~
Problems: 
- ❌ Tight coupling (agents know about successors)
- ❌ O(n²) edge complexity
- ❌ Hard to modify (rewrite edges)
- ❌ No automatic parallelism
- ❌ Testing requires full graph

Blackboard Approach
~~~
# Agents subscribe to types (loose coupling)
bug_detector = flock.agent("bugs").consumes(Code).publishes(BugReport)
security = flock.agent("security").consumes(Code).publishes(SecurityReport)
reporter = flock.agent("reporter").consumes(BugReport, SecurityReport).publishes(Report)

# Want to add performance_analyzer? Just subscribe it:
perf_analyzer = flock.agent("perf").consumes(Code).publishes(PerfReport)
# Done! No graph rewiring. Reporter can optionally consume it.
~~~
Benefits: 
- ✅ Loose coupling (agents only know types)
- ✅ O(n) subscription complexity
- ✅ Easy to extend (add new subscribers)
- ✅ Automatic parallelism (concurrent consumers)
- ✅ Test agents in isolation


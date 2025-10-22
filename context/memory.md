If agents have the ability to save memories, they also need the ability to select memories relevant to the task they are performing. This can be useful for a few reasons. Agents might select few-shot examples (episodic memories) for examples of desired behavior, instructions (procedural memories) to steer behavior, or facts (semantic memories) give the agent task-relevant context.
https://langchain-ai.github.io/langgraph/concepts/memory/#memory-types
https://github.com/langchain-ai/langgraph/blob/main/docs/docs/concepts/memory.md
- long term memory 
- short term memory


Different applications require various types of memory. Although the analogy isn't perfect, examining [human memory types](https://www.psychologytoday.com/us/basics/memory/types-of-memory?ref=blog.langchain.dev) can be insightful. Some research (e.g., the [CoALA paper](https://arxiv.org/pdf/2309.02427)) have even mapped these human memory types to those used in AI agents.

| Memory Type | What is Stored | Human Example | Agent Example |
|-------------|----------------|---------------|---------------|
| [Semantic](#semantic-memory) | Facts | Things I learned in school | Facts about a user |
| [Episodic](#episodic-memory) | Experiences | Things I did | Past agent actions |
| [Procedural](#procedural-memory) | Instructions | Instincts or motor skills | Agent system prompt |

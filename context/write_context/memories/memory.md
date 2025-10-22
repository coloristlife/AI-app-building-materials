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


`source` https://github.com/jihoo-kim/awesome-context-engineering
# Long-term memory

- [mem0](https://github.com/mem0ai/mem0) (`mem0ai`) ![](https://img.shields.io/github/stars/mem0ai/mem0.svg?style=social) Memory for AI Agents; Announcing OpenMemory MCP - local and secure memory management.
- [letta](https://github.com/letta-ai/letta) (`letta-ai`) ![](https://img.shields.io/github/stars/letta-ai/letta.svg?style=social) Letta (formerly MemGPT) is the stateful agents framework with memory, reasoning, and context management.
- [graphiti](https://github.com/getzep/graphiti) (`getzep`) ![](https://img.shields.io/github/stars/getzep/graphiti.svg?style=social) Build Real-Time Knowledge Graphs for AI Agents
- [cognee](https://github.com/topoteretes/cognee) (`topoteretes`) ![](https://img.shields.io/github/stars/topoteretes/cognee.svg?style=social) Memory for AI Agents in 5 lines of code
- [Memary](https://github.com/kingjulio8238/Memary) ![](https://img.shields.io/github/stars/kingjulio8238/Memary.svg?style=social) The Open Source Memory Layer For Autonomous Agents
- [memobase](https://github.com/memodb-io/memobase) (`memodb-io`) ![](https://img.shields.io/github/stars/memodb-io/memobase.svg?style=social) Profile-Based Long-Term Memory for AI Applications. Memobase handles user profiles, memory events, and evolving context
- [A-mem](https://github.com/agiresearch/A-mem) (`agiresearch`) ![](https://img.shields.io/github/stars/agiresearch/A-mem.svg?style=social) A-MEM: Agentic Memory for LLM Agents
- [MemoryOS](https://github.com/BAI-LAB/MemoryOS) (`BAI-LAB`) ![](https://img.shields.io/github/stars/BAI-LAB/MemoryOS.svg?style=social) A memory operation system for personalized AI
- [core](https://github.com/RedPlanetHQ/core) (`RedPlanetHQ`) ![](https://img.shields.io/github/stars/RedPlanetHQ/core.svg?style=social) Your personal plug and play memory layer for LLMs

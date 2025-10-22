# context_engineering
`source`
https://rlancemartin.github.io/2025/06/23/context_engineering

The structure of the document, "Context Engineering for Agents," is built around defining the problem and then grouping solutions into four core strategies.

### Main Concept and Definition

The central topic is **Context Engineering**, which is defined as the **“delicate art and science of filling the context window with just the right information for the next step”**. The context window is analogized to the RAM of a computer, and the Large Language Model (LLM) is the CPU, serving as the model's working memory. Context engineering is considered effectively the **"#1 job of engineers building AI agents"**.

### Types of Context Managed

Context engineering is an umbrella term that applies across three different types of context that must be managed:

1.  **Instructions** (e.g., prompts, few-shot examples, tool descriptions).
2.  **Knowledge** (e.g., facts, memories).
3.  **Tools** (e.g., feedback from tool calls).

### Core Context Management Strategies

The approaches to tackling context engineering are grouped into four primary strategies:

1.  **Write Context**: This strategy means **saving information outside the context window to help an agent perform a task**.

2.  **Select Context**: This strategy means **pulling information into the context window to help an agent perform a task**.

3.  **Compressing Context**: This strategy involves **retaining only the tokens required to perform a task**.

4.  **Isolating Context**: This strategy involves **splitting the context up to help an agent perform a task**.


`source ` https://www.philschmid.de/context-engineering

The definition of "context"
Here’s a clean, professional format for your content:

---

### **Context Components for AI Systems**

1. **Instructions / System Prompt**  
   *Defines the model’s behavior during a conversation.*  
   - Includes: Rules, examples, and guiding principles.

2. **User Prompt**  
   *Immediate task or question from the user.*

3. **State / History (Short-Term Memory)**  
   *Current conversation context.*  
   - Includes: User and model responses leading up to the present moment.

4. **Long-Term Memory**  
   *Persistent knowledge base across multiple conversations.*  
   - Stores:  
     - Learned user preferences  
     - Summaries of past projects  
     - Facts for future reference

5. **Retrieved Information (RAG)**  
   *External, up-to-date knowledge.*  
   - Sources: Documents, databases, APIs  
   - Purpose: Answer specific questions with relevant data.

6. **Available Tools**  
   *Definitions of all callable functions or built-in tools.*  
   - Examples: `check_inventory`, `send_email`

7. **Structured Output**  
   *Defines the response format.*  
   - Example: JSON object schema


`source` https://blog.langchain.com/the-rise-of-context-engineering/
Why it matters 

`source` www.dbreunig.com%2F2025%2F06%2F22%2Fhow-contexts-fail-and-how-to-fix-them.html
how context fails and how to fix them 

The provided sources, titled "How to Fix Your Context," detail strategies for mitigating and avoiding context failures in AI agents by focusing on effective information management.

The source identifies several ways long contexts can fail:

*   **Context Poisoning:** Occurs when an error or hallucination enters the context and is repeatedly referenced.
*   **Context Distraction:** Happens when the context grows so long that the model over-focuses on the context, neglecting what it learned during training.
*   **Context Confusion:** Results when superfluous information within the context is used by the model, leading to a low-quality response.
*   **Context Clash:** Takes place when new accrued information and tools in the context conflict with other information already present in the prompt.

The underlying principle for mitigation is that **everything in the context influences the response**, following the adage, "Garbage in, garbage out". Managing context is considered *the* job of the agent designer.

The sources detail six primary tactics for context management:

### 1. RAG (Retrieval-Augmented Generation)
RAG is defined as the act of **selectively adding relevant information** to help the LLM generate a better response. Although context windows have increased dramatically (e.g., Llama 4 Scout's 10 million token window), RAG remains critical because treating context like a "junk drawer" ensures that "the junk will influence your response".

### 2. Tool Loadout
Tool Loadout involves **selecting only relevant tool definitions** to add to the context. This term is borrowed from gaming, where a loadout is tailored to the specific context or task.
*   Applying RAG to tool descriptions (e.g., storing them in a vector database) can improve tool selection accuracy.
*   For DeepSeek-v3, problems become critical when models are given more than 30 tools due to overlapping descriptions causing confusion; performance was virtually guaranteed to fail with more than 100 tools.
*   Dynamic tool selection, where an LLM recommends the required tools based on the user's query, improved Llama 3.1 8b performance by 44% on a benchmark.
*   Smaller contexts achieved through tool selection also offer secondary benefits, including reduced power consumption (18% savings) and speed (77% gains), which are crucial metrics for edge operations.

### 3. Context Quarantine
This tactic involves **isolating contexts in their own dedicated threads**, often used by multiple LLMs, to break tasks into smaller, isolated jobs. This strategy promotes the **"separation of concerns"** by giving subagents distinct tools, prompts, and trajectories.
*   Context quarantine, often seen in multi-agent research systems, excels at "breadth-first queries".
*   Internal evaluations showed that a multi-agent system using Claude Opus 4 as the lead agent outperformed a single-agent Claude Opus 4 by 90.2% on research evaluations.
*   This approach also simplifies tool loadouts by allowing the designer to create specialized agent archetypes, each with its own dedicated set of tools and instructions.

### 4. Context Pruning
Context Pruning is the act of **removing irrelevant or otherwise unneeded information** from the context.
*   It can be achieved by tasking the main LLM, designing a separate LLM-powered tool, or using tailored functions like Provence, an "efficient and robust context pruner for Question Answering".
*   Provence was shown to effectively cull documents, cutting 95% of content while maintaining the relevant subset.
*   The use of pruning argues strongly for maintaining a **structured** version of the context (like a dictionary), allowing sections like document history to be pruned while preserving main instructions and goals.

### 5. Context Summarization
This tactic involves **boiling down an accrued context into a condensed summary**. While historically used to manage smaller context windows, summarization is now recognized as vital for mitigating **Context Distraction**.
*   If context grows significantly beyond 100,000 tokens, agents may show a tendency toward favoring repeating actions from history rather than synthesizing novel plans.
*   It is critical for agent builders to customize summarization by defining what specific information must be preserved.

### 6. Context Offloading
Context Offloading is the act of **storing information outside the LLM’s context**, typically utilizing a tool that stores and manages the data. This is often implemented as a **scratchpad** (like Anthropic’s “think” tool) for the model to log notes and progress.
*   Pairing context offloading with a domain-specific prompt yielded significant improvements, up to a 54% gain against benchmarks for specialized agents.
*   Context offloading is particularly useful in three scenarios: when the model needs to carefully process tool output and might need to backtrack; in policy-heavy environments requiring compliance verification; and in sequential decision making where mistakes are costly.

The overall key insight is that **context is not free** and every token influences the model’s behavior, meaning that the large context windows of modern LLMs do not excuse sloppy information management.

`source` https://www.llamaindex.ai/blog/context-engineering-what-it-is-and-techniques-to-consider


### **What Makes Up Context**

- **The system prompt/instruction**  
  Sets the scene for the agent about what sort of tasks we want it to perform.

- **The user input**  
  Can be anything from a question to a request for a task to be completed.

- **Short-term memory or chat history**  
  Provides the LLM context about the ongoing chat.

- **Long-term memory**  
  Can be used to store and retrieve both long-term chat history or other relevant information.

- **Information retrieved from a knowledge base**  
  Could involve retrieval based on vector search over a database or relevant information from external sources via API calls, MCP tools, etc.

- **Tools and their definitions**  
  Provide additional context to the LLM as to what tools it has access to.

- **Responses from tools**  
  Provide the responses from tool runs back to the LLM as additional context to work with.

- **Structured outputs**  
  Provide context on what kind of information we are after from the LLM, or condensed structured information for specific tasks.

- **Global state/context**  
  Especially relevant to agents built with LlamaIndex, allowing workflow context as a scratchpad to store and retrieve global information across agent steps.


### **Techniques and Strategies for Context Engineering**

Context engineering faces two main challenges:  
1. **Selecting the right context**  
2. **Fitting context within the context window**

Below are key strategies and architectural choices:

---

#### **1. Knowledge Base or Tool Selection**
- Modern agentic applications often require **multiple knowledge bases** and tools, not just a single vector store.
- Initial context includes **information about available tools and knowledge bases** to ensure correct resource selection.

---

#### **2. Context Ordering or Compression**
- **Context limits** require efficient use of space.
- Techniques:
  - **Summarization**: Condense retrieved results before adding to LLM context.
  - **Ranking**: Order context by relevance (e.g., date-sensitive tasks).

---

#### **3. Long-Term Memory Storage and Retrieval**
- Ongoing conversations make history part of the context.
- **LlamaIndex memory blocks**:
  - `VectorMemoryBlock`: Stores/retrieves chat messages from a vector DB.
  - `FactExtractionMemoryBlock`: Extracts facts from chat history.
  - `StaticMemoryBlock`: Stores static information.
- Choosing the right memory type and retrieval scope is critical.

---

#### **4. Structured Information**
- Avoid overcrowding the context window with unnecessary data.
- **Structured outputs**:
  - **Requested schema**: Define output format for LLM.
  - **Structured data as context**: Provide condensed, relevant info.
- **LlamaExtract**: Extracts structured data from large files for downstream tasks.

---

#### **5. Workflow Engineering**
- Goes beyond single LLM calls; focuses on **sequence of steps**:
  - Define explicit task sequences.
  - Control context strategically (LLM vs deterministic logic).
  - Ensure reliability with validation and fallback.
  - Optimize for specific outcomes.
- Prevents context overload by breaking tasks into **focused steps**.

### Tools to build:
If this discussion and these techniques have inspired you to overhaul your own approach to agentic engineering, we encourage you to use LlamaIndex, both for our easy to use retrieval infrastructure but also our popular Workflows orchestration framework, which went 1.0 earlier this week, as well as our powerful enterprise tools like LlamaExtract and LlamaParse.
https://developers.llamaindex.ai/python/framework/understanding/rag/

https://www.llamaindex.ai/blog/announcing-workflows-1-0-a-lightweight-framework-for-agentic-systems

https://www.llamaindex.ai/llamaparse

https://www.llamaindex.ai/llamaextract

https://developers.llamaindex.ai/python/framework/understanding/workflows/

`source` https://cognition.ai/blog/dont-build-multi-agents#principles-of-context-engineering

# Don’t Build Multi-Agents
The sources provided focus on the challenges and principles of **Context Engineering** in the development of reliable and long-running AI agents, specifically arguing *against* the use of multi-agent architectures in 2025.

### Principles and Definition of Context Engineering

Context engineering is defined as the "delicate art and science of filling the context window with just the right information for the next step". It is considered the **"#1 job of engineers building AI agents"**. This effort is necessary because even the most intelligent models require the correct context to perform their job effectively.

The goal of Context Engineering, particularly for long-running agents, is to **contain the potential for compounding errors** to maintain reliability and coherent conversations.

The source proposes two critical principles for agent architecture that are often violated by multi-agent systems:

1.  **Share context**: Agents should share full agent traces, not just individual messages.
2.  **Actions carry implicit decisions**: Conflicting decisions resulting from isolated actions lead to bad results.

### Critique of Multi-Agent Architectures

The article explicitly advises **"Don't Build Multi-Agents"**, arguing that libraries promoting multi-agent architectures (like OpenAI's Swarm and Microsoft's AutoGen) are pushing the wrong concept.

The main reason multi-agent systems are considered fragile and unreliable is their inherent difficulty in maintaining consistent context and decision-making:

*   **Failure through Miscommunication:** If a complex task is broken into subtasks handled by subagents (e.g., building a Flappy Bird clone), the subagents may misunderstand or misinterpret their specific assignment.
*   **Inconsistent Results:** Even when subagents receive the original task context, they operate without seeing what others are doing, leading to inconsistent work (e.g., a bird and background with completely different visual styles). The actions of parallel subagents are based on conflicting, unprescribed assumptions.
*   **Fragility in 2025:** While there is optimism for the long-term potential of agent collaboration, in 2025, running multiple collaborative agents results in fragile systems because decision-making is too dispersed and context cannot be thoroughly shared.

### Recommended Solutions and Architectures

The simplest way to adhere to the principles of context sharing and consistent decision-making is to use a **single-threaded linear agent** where the context is continuous.

For tasks too large for a simple linear agent that risks context window overflow, the source suggests an advanced technique:

*   **Context Compression Model:** Introduce a new LLM model whose sole purpose is to **compress a history of actions and conversation into key details, events, and decisions**. This is a difficult task that may require investment, such as fine-tuning a smaller model, but it benefits agents dealing with longer contexts.

### Real-World Examples

The sources provide examples illustrating context management approaches:

*   **Claude Code Subagents:** Claude Code uses subtasks but avoids parallel work. The subagent is usually only tasked with answering a question, not generating code. This strategy is employed because the subagent lacks the full context of the main agent, and running parallel subagents could lead to conflicting responses and reliability issues. The benefit is that the subagent's investigative work does not clutter the main agent's history, allowing for longer traces.
*   **Edit Apply Models (Historical):** In 2024, it was common to use a large model to output a markdown explanation of code edits, which was then fed to a smaller "edit apply model" to rewrite the file. This approach was faulty because the small model often misinterpreted the large model's instructions due to slight ambiguities. Today, the decision-making and applying of edits are more often handled by a **single model in one action**.

The overall message is that agent builders must ensure that **every action is informed by the context of all relevant decisions** made by other parts of the system, even if practical limitations (like context window size) require carefully deciding the level of complexity and context exposure.

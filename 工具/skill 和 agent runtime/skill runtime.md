https://github.com/anomalyco/opencode


有，而且现在其实已经有几款**非常接近你说的“Claude Code / Codex 这种 Agent Runtime”**的开源项目了。更重要的是，其中有些并不绑定某一家模型，这一点对你的 Personal Investment AI 很关键。

我刚查了一下目前的项目，我会重点看下面三个。

### 1. OpenCode —— 我认为与你的需求最接近

[OpenCode GitHub](https://github.com/anomalyco/opencode?utm_source=chatgpt.com)

OpenCode 是开源的 AI Agent，而且明确强调 **provider-agnostic**：可以使用 Claude、OpenAI、Google，甚至本地模型。它采用 MIT License，并且有 CLI、工具调用、subagent 等 Agent 能力。([GitHub](https://github.com/sst/opencode?utm_source=chatgpt.com "GitHub - anomalyco/opencode: The open source coding agent. · GitHub"))

它和 Claude Code 的思路非常接近：

```text
User
 ↓
OpenCode Runtime
 ↓
LLM
 ↓
Tools
 ↓
Files / Web / MCP / etc.
```

所以你完全可以把它理解成：

> **一个开源版、模型无关的 Claude Code 类 Agent Runtime。**

对于你的项目，我会把它列为**第一候选**。

---

### 2. Goose —— 甚至比 OpenCode 更符合你的“投资 AI”场景

[Goose GitHub](https://github.com/aaif-goose/goose?utm_source=chatgpt.com)

Goose 原本由 Block 开发，现在已经进入 Linux Foundation 旗下的 Agentic AI Foundation。它不是单纯的 Coding Agent，而是定位为：

> **general-purpose AI agent**

也就是说，它本来就可以做：

- coding
    
- research
    
- writing
    
- automation
    
- data analysis
    

而且提供：

- Desktop
    
- CLI
    
- API
    

并且支持 15+ 模型提供商，包括 Anthropic、OpenAI、Google、Ollama、OpenRouter、Azure、Bedrock 等，同时可以通过 MCP 接入大量工具。([GitHub](https://github.com/block/goose?utm_source=chatgpt.com "GitHub - aaif-goose/goose: an open source, extensible AI agent that goes beyond code suggestions - install, execute, edit, and test with any LLM · GitHub"))

这个特点其实**非常适合你的 Personal Investment AI**。

因为你的 Agent 根本不是 Coding Agent：

```text
                Goose Runtime
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
    Research      Analysis     Automation
        │            │            │
        └────────────┼────────────┘
                     ↓
              Investment Skills
```

这比把 Claude Code 改造成投资 Agent 更自然。

---

### 3. OpenHands —— 如果以后你想自己构建 Agent Platform

[OpenHands GitHub](https://github.com/OpenHands/OpenHands?utm_source=chatgpt.com)

OpenHands 更值得注意的是它提供 **Software Agent SDK**。

它不是只有一个 CLI，而是把 Agent 能力抽象成可以被你自己的应用调用的 SDK。官方现在把 SDK 定义为其 Agent 技术的核心引擎，可以在本地运行，也可以扩展到云端大规模运行。([GitHub](https://github.com/OpenHands/openhands?utm_source=chatgpt.com "GitHub - OpenHands/OpenHands: 🙌 OpenHands: AI-Driven Development · GitHub"))

更关键的是，它的 SDK 强调：

- custom tools
    
- memory management
    
- multi-LLM routing
    
- sandboxed execution
    
- REST/WebSocket
    
- agent lifecycle
    

所以如果你的目标最终是：

> **“我不是想找一个现成的 Agent，而是想建立自己的 Investment Agent Runtime。”**

OpenHands 会非常值得研究。相关论文也明确把它定位成可组合、可扩展的 Agent 基础设施。([arXiv](https://arxiv.org/abs/2511.03690?utm_source=chatgpt.com "The OpenHands Software Agent SDK: A Composable and Extensible Foundation for Production Agents"))

---

# 对你的项目，我会这样排

|项目|更像什么|模型绑定|适合你的程度|
|---|---|---|---|
|**OpenCode**|Claude Code 类 Runtime|❌|⭐⭐⭐⭐⭐|
|**Goose**|通用 Agent Runtime|❌|⭐⭐⭐⭐⭐|
|**OpenHands**|Agent SDK / Platform|❌|⭐⭐⭐⭐|
|Claude Code|Coding Agent|Anthropic|⭐⭐⭐|
|Codex|Coding Agent|OpenAI|⭐⭐⭐|

这里最关键的是：

> **你现在不应该把“Skill Runtime”和“Coding Agent”混为一谈。**

你的投资系统真正需要的是：

```text
                Your Investment AI
                       │
                       ▼
                Agent Runtime
                       │
                 Skill Engine
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
 Intelligence      Personal       Investment
   Skill            Context         Skill
                    Skill
        │              │              │
        └──────────────┼──────────────┘
                       ↓
                 Tools / MCP
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
     Web Search     Market Data    Obsidian
```

然后：

```text
Agent Runtime
      ↓
Model Router
      ↓
┌─────┼─────┬─────┐
GPT  Claude Qwen Gemini
```

这就是你真正想要的架构。

---

# 我尤其建议你关注 Goose

因为我们刚才讨论的是：

> **Skill-first + 不绑定模型 + 非 Coding 场景 + MCP + 本地知识**

Goose 的定位刚好踩中了这几个点。

它甚至已经有 **Skills Marketplace / Skill 机制**，同时支持 MCP extensions。([Block](https://block.github.io/goose/?utm_source=chatgpt.com "goose | Your open source AI agent"))

所以你可以想象你的第一版：

```text
Goose
 │
 ├── Investment Analysis Skill
 ├── Intelligence Requirement Skill
 ├── Intelligence Extraction Skill
 ├── Personal Context Skill
 └── Prediction Evaluation Skill
       │
       ↓
Obsidian Vault
       │
       ↓
YAML
```

模型可以是：

```text
Claude
GPT
Qwen
Gemini
Ollama
```

而不用自己从零写 Agent Loop。

---

## 但这里有一个非常重要的战略选择

我现在**不建议你马上自己写 Runtime**。

因为你真正有价值的部分不是：

> “我写了一个 Agent Loop。”

这个东西已经有很多成熟开源实现。

你真正有价值的是：

> **Personal Investment Context → Information Requirements → Intelligence → Signal → Reasoning → Prediction → Outcome**

也就是我们刚才设计出来的**投资认知闭环**。

所以我建议第一版直接：

> **用 OpenCode 或 Goose 做 Runtime，自己定义 Skill 和 YAML Data Model。**

等这个系统真正跑起来以后，你会自然发现：

> 哪些 Runtime 能力是现成项目解决不了的。

到那个时候再决定要不要 fork Goose/OpenCode，或者基于 OpenHands SDK 做自己的 Runtime。

**如果让我现在替你选一个做 POC，我会优先试 Goose；如果你希望体验尽可能接近 Claude Code，则试 OpenCode。**
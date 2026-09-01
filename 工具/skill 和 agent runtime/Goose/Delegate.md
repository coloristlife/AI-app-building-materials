`delegate` 的核心目的可以理解成一句话：

> **把一个任务交给另一个独立的 Agent / Subagent 去完成，而不是让当前 Agent 自己完成。**

它和我们刚才讲的 `load` 是一对非常重要的概念。

### `load` vs `delegate`

```text
load
  ↓
“把这个东西教给我”
  ↓
当前 Agent 继续工作


delegate
  ↓
“你帮我把这个事情做了”
  ↓
启动/调用另一个 Agent
  ↓
独立执行
  ↓
返回结果
```

Goose 的设计讨论本身就是这样区分的：`load` 是把 source 加入当前 Agent 的 context，而 `delegate` 是让另一个 Agent 执行这个 source。([github.com](https://github.com/aaif-goose/goose/discussions/6202?utm_source=chatgpt.com))

---

## 为什么需要 delegate？

假设你现在的 Goose Agent 正在做：

> “Review this entire application architecture.”

它可能需要做很多事情：

```text
Architecture Review
│
├── Analyze architecture
├── Identify threats
├── Check MCP security
├── Check authentication
├── Check data security
└── Generate report
```

如果全部让当前 Agent 做：

```text
Main Agent
    │
    ├── Threat analysis
    ├── MCP analysis
    ├── Auth analysis
    ├── Data analysis
    └── Report
```

context 会越来越大，而且任务职责混在一起。

使用 `delegate` 可以变成：

```text
                    Main Agent
                         │
             “Perform security review”
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
      Delegate        Delegate       Delegate
      Threat          MCP            Auth
      Analysis        Analysis       Analysis
          │              │              │
          ▼              ▼              ▼
       Result         Result         Result
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                    Main Agent
                         │
                         ▼
                     Report
```

所以 `delegate` 的价值主要是：

**任务分解 + 隔离 context + 专业化执行 + 并行化。**

---

## 对你的 Security Knowledge 项目特别有意义

比如你定义几个 Skills：

```text
Security Knowledge Skill
MCP Security Skill
Threat Modeling Skill
Cloud Security Skill
```

然后定义一个：

```text
Security Architecture Review Recipe
```

主 Agent 收到：

> “Review this architecture.”

它可以：

```text
Main Agent
    │
    ├── delegate → Threat Modeling
    │
    ├── delegate → MCP Security
    │
    ├── delegate → Cloud Security
    │
    └── delegate → Data Security
```

每个 subagent 有自己的：

```text
context
instructions
skills
tools
```

完成后把结果返回给 Main Agent。

---

## 但是有一个很重要的区别

**delegate 不等于 function call。**

普通 Tool Call：

```text
Agent
  ↓
search_knowledge()
  ↓
Result
```

这是：

> **Agent 调用一个工具。**

而 Delegate：

```text
Agent
  ↓
delegate(Security Review)
  ↓
Subagent
  ↓
LLM reasoning
  ↓
Tools
  ↓
Skills
  ↓
Result
```

这是：

> **Agent 调用另一个 Agent。**

所以它的抽象层级更高。

---

### 你可以这样记

```text
Tool
  = “帮我执行一个动作”

Skill
  = “教我一种能力”

Recipe
  = “告诉我怎么组织一个任务”

delegate
  = “这个任务你替我做”

Agent
  = “真正进行 reasoning 的执行者”
```

这也是为什么 Goose 把 `delegate` 设计成一个重要的 Agent Runtime 能力，而不是普通工具调用。它让 Goose 从“一个 Agent + 一堆 Tools”进一步变成了**可以组织多个 Agent 的 Agent Runtime**。([github.com](https://github.com/aaif-goose/goose/discussions/6202?utm_source=chatgpt.com))

对于你正在设计的 Security Agent，我甚至认为 **delegate 比 Recipe 本身更值得关注**，因为它直接关系到以后你怎么把 **Threat Modeling、Security Review、Knowledge Retrieval、Report Generation** 拆成多个可组合的 Agent。
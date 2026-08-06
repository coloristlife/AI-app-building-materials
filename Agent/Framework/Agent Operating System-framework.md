

**“Agent Operating System（Agent OS / AOS）目前还不是像 Linux、Windows 那样已经统一定义的标准产品类别。它更像一个正在形成的系统架构范式。** 2026 年已经出现了明确以 Agent OS 命名的研究和开源项目，但不同项目对“OS”的理解差别很大。最近的一篇 AOS 研究把它定义为：在传统 OS 之上增加一个面向 Agent 的 control plane，负责调度、上下文/记忆、工具与能力注册、权限/信任、可观测性和审计等。([arXiv][1])

如果把传统 OS 比作：

> **CPU + Memory + Process + File System + Permission + Network + Scheduler**

那么 Agent OS 更像：

> **LLM + Context + Agent Process + Memory + Tools + Identity/Policy + Scheduler + Workflow + Observability**

这也是我认为理解 Agent OS 最好的切入点。

---

# 一、Agent Operating System 到底是什么？

传统软件的执行方式大致是：

```text
User
  ↓
Application
  ↓
Function A
  ↓
Function B
  ↓
Function C
  ↓
Result
```

程序员提前决定：

* 执行什么
* 按什么顺序执行
* 调用什么 API
* 用什么数据
* 什么情况下失败
* 如何重试

Agent 则完全不同：

```text
User
  ↓
Goal
  ↓
Agent
  ↓
Reason
  ↓
Choose Tool
  ↓
Observe Result
  ↓
Reason
  ↓
Choose Another Tool
  ↓
...
  ↓
Goal Completed
```

这里最大的问题是：

**Agent 不再是一个简单的 function，而变成了一个长期运行、具有状态、可以自主选择行动的软件实体。**

这就产生了一系列传统应用框架没有很好解决的问题：

* Agent 怎么调度？
* Agent 怎么暂停和恢复？
* Agent 的 memory 放在哪里？
* 不同 Agent 如何共享/隔离 context？
* Agent 可以调用哪些工具？
* 工具权限谁决定？
* Agent 怎么获得身份？
* Agent 如何访问文件系统？
* Agent 如何访问网络？
* Agent 如何运行代码？
* 多 Agent 怎么通信？
* Agent 运行失败后怎么恢复？
* 一个 Agent 可以运行多久？
* 怎么限制 Agent 的 token / cost / CPU / memory？
* 谁批准 Agent 的高风险操作？
* 如何审计 Agent 做过什么？
* 如何知道 Agent 为什么做了某件事情？

于是就出现了：

# **Agent Operating System**

---

# 二、一个比较准确的定义

我比较推荐把 Agent OS 定义成：

> **Agent OS 是一个面向 Autonomous Agents 的 Runtime + Control Plane，用来管理 Agent 的生命周期、计算资源、上下文、记忆、工具、身份、权限、调度、通信、持久化、可观测性和治理。**

这个定义比“让 AI 变成操作系统”准确得多。

最近的 AOS 研究也基本沿着这个方向，把 Agent OS 的职责拆成：

* Scheduler
* Context & Memory Management
* Tool / Capability Registry
* Policy / Trust Enforcement
* Observability / Audit

并讨论如何映射到 Linux/Windows 的传统 OS primitive。([arXiv][1])

---

# 三、Agent OS 和传统 Agent Framework 的区别

这是最容易混淆的地方。

很多人会说：

> LangGraph 是 Agent OS。

或者：

> AutoGen 是 Agent OS。

严格来说，**不完全对。**

可以把技术栈分成 5 层。

```text
┌─────────────────────────────────────────────┐
│             Agent Applications              │
│                                             │
│  Coding Agent / Research Agent / SWE Agent  │
│  Security Agent / Finance Agent / Support   │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│              Agent Framework                │
│                                             │
│ LangGraph / AutoGen / CrewAI / OpenAI SDK  │
│ Semantic Kernel / PydanticAI                │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│             Agent Runtime                   │
│                                             │
│ Scheduler / State / Memory / Workflow       │
│ Tool execution / Handoff / Retry            │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│             Agent Control Plane              │
│                                             │
│ Identity / Policy / Capability / Governance │
│ Security / Audit / Cost / Quota             │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│              Traditional OS                 │
│                                             │
│ Linux / Windows / Kubernetes / Containers   │
│ CPU / Memory / Network / Filesystem         │
└─────────────────────────────────────────────┘
```

所以：

**LangGraph 更接近 Agent Runtime。**

**AutoGen 更接近 Agent Framework + Runtime。**

**MCP 更接近 Agent Tool/Capability Protocol。**

**Temporal 更接近 Durable Execution Infrastructure。**

而真正完整的 Agent OS，需要把这些东西组合起来。

---

# 四、Agent OS 最核心的 10 个组件

如果你自己设计 Agent OS，我建议至少考虑下面这些 primitive。

---

## 1. Agent Scheduler

这是 Agent OS 最像传统 OS 的部分。

传统 OS：

```text
Process A
Process B
Process C
      ↓
CPU Scheduler
```

Agent OS：

```text
Agent A
Agent B
Agent C
Agent D
      ↓
Agent Scheduler
```

Scheduler 可以根据：

* priority
* deadline
* token budget
* cost budget
* CPU
* memory
* model availability
* tool availability
* tenant
* risk level

决定：

```text
谁现在运行？
谁暂停？
谁等待？
谁重试？
谁终止？
```

例如：

```text
Security Agent
priority = HIGH

Research Agent
priority = MEDIUM

Summarization Agent
priority = LOW
```

如果 GPU / API quota 紧张：

```text
Security Agent       RUN
Research Agent       WAIT
Summarization Agent  WAIT
```

这就是典型 OS scheduler 思想。

---

# 五、Context Management

这是 Agent OS 和传统 OS 最大的不同之一。

传统 OS 有：

```text
RAM
Virtual Memory
Process Memory
Cache
Disk
```

Agent OS 需要：

```text
Context Window
Working Memory
Short-term Memory
Long-term Memory
Episodic Memory
Semantic Memory
Procedural Memory
External Knowledge
```

例如一个 Agent 工作 6 小时：

```text
09:00
用户：研究 OpenAI Agent Security

10:00
Agent 搜索 20 篇论文

11:00
Agent 分析安全模型

12:00
Agent 生成 threat model

13:00
Agent 发现一个新的 attack vector

14:00
继续研究

15:00
生成最终报告
```

你不可能把 6 小时所有 token 都塞进 context window。

因此需要：

```text
                 Agent
                   │
             Context Manager
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
 Working       Episodic     Semantic
 Memory        Memory       Memory
       ↓           ↓           ↓
      Redis      Vector DB    Graph DB
```

这也是为什么 **Letta** 这样的项目值得关注。Letta 把 Agent 定义成有持久状态的 service，而不是一次性 stateless API，并提供 persistent memory/state。([Letta Docs][2])

---

# 六、Tool / Capability Management

Agent 最大的能力来源不是 LLM。

而是：

> **LLM + Tools**

例如：

```text
Agent
 │
 ├── web_search
 ├── database_query
 ├── GitHub
 ├── filesystem
 ├── shell
 ├── browser
 ├── Kubernetes
 ├── Jira
 └── Slack
```

问题马上来了：

> Agent 能调用哪些工具？

这就不能只靠 prompt。

例如：

```text
Research Agent
 ├── Web Search       ✓
 ├── GitHub Read      ✓
 ├── Database Read    ✓
 ├── Database Write   ✗
 ├── Production SSH   ✗
 └── Kubernetes Delete ✗
```

所以 Agent OS 应该有：

```text
Capability Registry
```

例如：

```yaml
agent:
  id: research-agent

capabilities:
  - web.search
  - github.read
  - docs.read

deny:
  - production.write
  - database.delete
  - shell.root
```

这实际上就是：

> **Capability-based Security**

---

# 七、MCP 为什么非常重要？

这里必须提到 **Model Context Protocol（MCP）**。

MCP 是一个开放标准，用于让 AI 应用连接外部：

* tools
* data
* resources
* workflows

官方把它比喻成：

> AI 世界的 USB-C。

([Model Context Protocol][3])

它解决的是：

```text
Agent
 ↓
MCP
 ↓
Tool Server
 ├── GitHub
 ├── Slack
 ├── Database
 ├── Search
 ├── Files
 └── Enterprise API
```

因此：

**MCP ≠ Agent OS**

但：

**MCP 很可能成为 Agent OS 的“设备/能力总线”。**

类似：

```text
Linux
 ├── USB
 ├── Network
 ├── Filesystem
 └── Device Drivers

Agent OS
 ├── MCP
 ├── Tools
 ├── Agents
 ├── APIs
 └── Data Sources
```

---

# 八、Identity & Permission

我认为这是未来 Agent OS 最重要的部分之一。

今天很多 Agent 系统实际上是：

```text
User
 ↓
LLM
 ↓
Tool
 ↓
Database
```

但企业真正需要的是：

```text
User
 ↓
Agent Identity
 ↓
Policy Engine
 ↓
Capability Check
 ↓
Tool
 ↓
Target Resource
```

例如：

```text
Agent: Finance-Aggregator

Identity:
    tenant = companyA
    role = finance-readonly

Capabilities:
    SAP.read
    Snowflake.read

Denied:
    SAP.write
    payroll.write
    bank.transfer
```

这意味着：

> **Agent 不应该因为 prompt 说“我是管理员”就获得管理员权限。**

权限必须来自 Agent OS 的 deterministic policy layer。

这也是一些新 Agent OS 项目强调 identity-first / deny-by-default 的原因。([OS for Agents][4])

---

# 九、Human-in-the-loop

Agent OS 还必须解决：

> **什么时候允许 Agent 自己做？什么时候必须问人？**

例如：

```text
Search web
     ↓
Read document
     ↓
Write draft
     ↓
Create PR
     ↓
Deploy production
```

风险越来越高。

可以设计：

```text
Risk 0
Read-only
    ↓
Automatic

Risk 1
Create document
    ↓
Automatic

Risk 2
Send email
    ↓
Approval

Risk 3
Change database
    ↓
Approval

Risk 4
Production deployment
    ↓
Human approval + MFA
```

这实际上是 Agent OS 的：

> **Policy Enforcement Point**

---

# 十、Agent Communication

当 Agent 数量从：

```text
1 Agent
```

变成：

```text
100 Agents
```

就会产生新的问题。

例如：

```text
Planner Agent
      ↓
Research Agent
      ↓
Analysis Agent
      ↓
Security Agent
      ↓
Writer Agent
```

或者：

```text
Supervisor
 ├── Researcher
 ├── Coder
 ├── Tester
 ├── Security
 └── Reviewer
```

于是需要：

* message bus
* agent registry
* routing
* handoff
* pub/sub
* agent discovery
* lifecycle management

AutoGen Core 就已经开始往这个方向发展，其 Runtime 负责 agent lifecycle、通信、安全边界和监控；同时支持 event-driven、distributed multi-agent runtime。([Microsoft GitHub][5])

---

# 十一、目前有哪些 Agent OS / Framework？

这里我建议不要把所有项目放在一个篮子里。

可以分成：

## 第一类：真正接近 Agent OS

### 1. AIOS

这是学术界比较典型的 Agent Operating System 项目。

AIOS

其目标就是：

> 把 LLM 和 Agent runtime 引入 OS abstraction。

它有：

```text
AIOS Kernel
     ↓
LLM Management
Memory Management
Storage Management
Tool Management
Scheduling
Context Management
Access Control
```

官方项目明确把 AIOS Kernel 定义成传统 OS kernel 之上的 abstraction layer。([GitHub][6])

论文实验还报告了最高约 **2.1× execution speedup**，不过这个数字应理解为其特定实验环境下的结果，而不是 Agent OS 普遍能获得 2.1× 性能。([arXiv][7])

**优点：**

* 架构非常接近真正 OS
* 有 kernel 概念
* 有 scheduler
* 有 context management
* 有 memory
* 有 tool management
* 有 SDK

**缺点：**

* 研究项目属性较强
* 生态还远不如 LangChain
* production readiness 需要自己评估
* 企业级 governance / IAM / observability 仍需补充

---

# 十二、OpenFang

这是 2026 年非常值得关注的一个方向。

OpenFang

它直接把自己定义成：

> **Agent Operating System**

而且是 Rust 实现。

其架构把：

* agents
* tools
* memory
* security
* channels
* protocols
* desktop

整合到一个系统中。官网目前描述为一个单 binary 的 Agent OS，并提供 autonomous “Hands”、agents、tools、memory、channels 等 primitive。([OpenFang][8])

这和 AIOS 的研究型路线很不一样。

它更像：

> **一个真正可以安装运行的 Agent Platform / Agent OS**

**优点：**

* Rust
* single binary
* 自带很多组件
* memory
* tools
* security
* channels
* multi-agent
* 更接近完整产品

**缺点：**

* 相对年轻
* 生态成熟度需要观察
* 如果企业已经有 Kubernetes / IAM / observability / workflow infrastructure，可能重复建设
* “OS”更多是 application/runtime OS，而不是替代 Linux kernel

---

# 十三、Rivet Agent OS

另外一个很有意思的项目是：

Rivet 的 **agentOS**。

它走的是完全不同的路线。

它不是：

> 给 Linux 做一个 Agent Kernel

而是：

> **在应用进程内部提供一个轻量级 Agent execution environment。**

官方描述它基于：

* WebAssembly
* V8 isolates

提供 virtual filesystem、process table、pipes、PTY、virtual network 等。([GitHub][9])

它最大的卖点是：

```text
Traditional Sandbox
      ↓
VM / Container
      ↓
hundreds ms / seconds
```

而：

```text
agentOS
      ↓
WASM / V8 isolate
      ↓
~milliseconds
```

官方给出的 cold start 目标约为 **6ms**，并强调相对于完整 sandbox 的资源和成本优势。([GitHub][9])

这个方向非常值得关注。

因为未来可能不是：

```text
Agent → Docker Container
```

而是：

```text
Agent
 ↓
Lightweight Isolate
 ↓
Capability-based Sandbox
```

---

# 十四、Operator OS

还有一些更加偏：

> Edge / Personal / Embedded Agent OS

例如 Operator OS。

它用 Go 实现，目标是在非常低资源硬件上运行 Agent，官方文档声称 runtime 内存可以低于 10MB。([Mintlify][10])

这个方向对于：

* Raspberry Pi
* IoT
* edge device
* robotics
* personal computer

比较有意思。

---

# 十五、但真正生产环境最值得关注的其实不是这些“Agent OS”项目

如果你的目标是：

> **现在就构建 Enterprise Agent OS**

我反而不会建议直接押注某一个叫“Agent OS”的项目。

我会组合：

### Runtime

**LangGraph**

它定位非常清楚：

> long-running + stateful agent runtime

支持：

* durable execution
* persistence
* human-in-the-loop
* streaming
* state checkpoint

([Docs by LangChain][11])

---

### Multi-Agent

**Microsoft Agent Framework / AutoGen**

AutoGen Core 已经具备：

* event-driven agents
* distributed runtime
* async messaging
* lifecycle management
* multi-agent communication

([Microsoft GitHub][12])

而微软现在正在把 Semantic Kernel 和 AutoGen 的能力整合到 **Microsoft Agent Framework**，官方称其为 Semantic Kernel 的 successor，并加入 session state、type safety、middleware、telemetry、graph workflows 等企业能力。([GitHub][13])

---

### Agent SDK

**OpenAI Agents SDK**

它提供：

```text
Agent
Tools
Handoff
Guardrails
Structured Output
Sessions
Tracing
```

而且 Runner 负责 agent turns、tool calls 和 handoffs。([OpenAI GitHub Page][14])

尤其值得注意的是它已经有比较完善的：

> tracing + guardrail

体系。([OpenAI GitHub Page][15])

---

### Memory

**Letta**

如果重点是：

> Stateful Agent / Long-term Memory

Letta 非常值得研究。

它把 Agent 定义成：

> **stateful service**

而不是一次 API call。([Letta Docs][16])

---

### Tool Protocol

**MCP**

解决：

```text
Agent → Tool
Agent → Data
Agent → Workflow
```

的标准化连接。([Model Context Protocol][3])

---

### Observability

**OpenTelemetry**

这是企业环境非常重要的一层。

OpenTelemetry 已经开始定义 GenAI semantic conventions，包括：

```text
agent.id
agent.name
provider
model
input
output
retrieval
invoke_agent
invoke_workflow
```

同时明确提醒输入输出中可能包含敏感数据。([OpenTelemetry][17])

所以企业 Agent OS 最好从第一天就设计：

```text
Agent
 ↓
Trace
 ↓
Span
 ├── LLM
 ├── Tool
 ├── MCP
 ├── Memory
 ├── Handoff
 └── Policy
```

---

# 十六、还有一个非常重要的 Framework：CrewAI

CrewAI 更偏：

> Multi-Agent Team

而不是 OS。

它有：

```text
Agent
 ↓
Crew
 ↓
Flow
```

其中：

* Crew = autonomous collaboration
* Flow = structured workflow

官方文档特别强调 Flow 可以提供 conditional logic、loops、dynamic state management 和更精确的 execution control。([CrewAI Documentation][18])

所以它适合：

```text
Researcher
    ↓
Writer
    ↓
Reviewer
    ↓
Editor
```

这样的系统。

但如果你需要：

> Enterprise Agent OS

单独使用 CrewAI 仍然不够。

---

# 十七、MetaGPT

MetaGPT 也很值得研究。

MetaGPT

它最大的特点是：

> **把 Agent Team 模拟成一个 Software Company。**

例如：

```text
Product Manager
       ↓
Architect
       ↓
Project Manager
       ↓
Engineer
       ↓
QA
```

它的核心思想是：

> Code = SOP(Team)

也就是把标准流程 SOP 化，再让多个 Agent 按角色执行。([GitHub][19])

这对 Agent OS 有一个重要启发：

**未来 Agent OS 不应该只有“Agent”，还应该有“Organization / Role / SOP / Policy”。**

---

# 十八、OpenHands

如果你关注：

> Coding Agent / Software Engineering Agent

那么 OpenHands 非常值得研究。

OpenHands

它现在已经把 Agent 技术抽象成：

> Software Agent SDK

可以本地运行，也可以扩展到大规模 agent execution。([GitHub][20])

它对于理解：

```text
Agent
 ↓
Shell
 ↓
Filesystem
 ↓
Browser
 ↓
Code execution
 ↓
Sandbox
 ↓
Verification
```

特别有参考价值。

---

# 十九、把这些 Framework 放在一起比较

| 技术                    | 最擅长                   | OS 属性 | Memory | Multi-Agent | Workflow | Security |
| --------------------- | --------------------- | ----: | -----: | ----------: | -------: | -------: |
| **AIOS**              | Agent OS research     | ⭐⭐⭐⭐⭐ |   ⭐⭐⭐⭐ |         ⭐⭐⭐ |      ⭐⭐⭐ |      ⭐⭐⭐ |
| **OpenFang**          | 完整 Agent OS           | ⭐⭐⭐⭐⭐ |   ⭐⭐⭐⭐ |        ⭐⭐⭐⭐ |     ⭐⭐⭐⭐ |     ⭐⭐⭐⭐ |
| **Rivet agentOS**     | Agent sandbox/runtime | ⭐⭐⭐⭐⭐ |     ⭐⭐ |         ⭐⭐⭐ |      ⭐⭐⭐ |    ⭐⭐⭐⭐⭐ |
| **LangGraph**         | Agent Runtime         |  ⭐⭐⭐⭐ |   ⭐⭐⭐⭐ |        ⭐⭐⭐⭐ |    ⭐⭐⭐⭐⭐ |      ⭐⭐⭐ |
| **AutoGen**           | Multi-Agent           |   ⭐⭐⭐ |    ⭐⭐⭐ |       ⭐⭐⭐⭐⭐ |     ⭐⭐⭐⭐ |      ⭐⭐⭐ |
| **CrewAI**            | Agent Team            |    ⭐⭐ |    ⭐⭐⭐ |       ⭐⭐⭐⭐⭐ |     ⭐⭐⭐⭐ |      ⭐⭐⭐ |
| **OpenAI Agents SDK** | Agent application     |    ⭐⭐ |    ⭐⭐⭐ |        ⭐⭐⭐⭐ |     ⭐⭐⭐⭐ |     ⭐⭐⭐⭐ |
| **Letta**             | Stateful Agent        |   ⭐⭐⭐ |  ⭐⭐⭐⭐⭐ |         ⭐⭐⭐ |      ⭐⭐⭐ |      ⭐⭐⭐ |
| **MetaGPT**           | Agent Organization    |    ⭐⭐ |    ⭐⭐⭐ |       ⭐⭐⭐⭐⭐ |     ⭐⭐⭐⭐ |       ⭐⭐ |
| **OpenHands**         | Coding Agent          |   ⭐⭐⭐ |    ⭐⭐⭐ |        ⭐⭐⭐⭐ |     ⭐⭐⭐⭐ |     ⭐⭐⭐⭐ |

---

# 二十、如果你真正要“实施” Agent OS，我建议不要从 Kernel 开始

这是非常重要的一点。

很多人看到 Agent OS 会马上想：

> 我要做一个新的 Agent Kernel。

我认为这是错误的工程顺序。

应该从：

# **Control Plane**

开始。

推荐架构：

```text
                    ┌────────────────────┐
                    │    User / Apps     │
                    └─────────┬──────────┘
                              ↓
                    ┌────────────────────┐
                    │   Agent Gateway    │
                    │ Auth / Rate Limit  │
                    └─────────┬──────────┘
                              ↓
              ┌─────────────────────────────┐
              │       AGENT CONTROL PLANE   │
              │                             │
              │  Agent Registry             │
              │  Scheduler                  │
              │  Policy Engine              │
              │  Identity                   │
              │  Capability Registry        │
              │  Memory Manager             │
              │  Context Manager            │
              │  Cost / Quota Manager       │
              └──────────────┬──────────────┘
                             ↓
              ┌─────────────────────────────┐
              │        AGENT RUNTIME        │
              │                             │
              │ LangGraph / AutoGen / SDK   │
              └──────────────┬──────────────┘
                             ↓
        ┌────────────────────┼─────────────────────┐
        ↓                    ↓                     ↓
      LLMs                 MCP                  Memory
        ↓                    ↓                     ↓
 OpenAI/Claude        Tools/APIs             Vector/Graph
 Gemini/etc.          DB/Git/Slack             SQL/Object
```

---

# 二十一、再加一个 Data Plane

Control Plane 决定：

> **Agent 可以做什么**

Data Plane 执行：

> **Agent 实际做什么**

例如：

```text
Control Plane

Policy:
ResearchAgent
  ├── web.search ✓
  ├── github.read ✓
  ├── github.write ✗
  └── prod.deploy ✗
```

然后：

```text
Data Plane

Agent
 ↓
MCP
 ↓
Web Search
 ↓
GitHub
 ↓
Database
```

二者一定要分开。

这对企业安全尤其重要。

---

# 二十二、一个实际可实施的 MVP

如果让我现在设计一个 Enterprise Agent OS，我会分 6 个阶段。

---

## Phase 1：Agent Runtime

先不要做 OS。

实现：

```text
Agent
 ├── Model
 ├── Prompt
 ├── Tools
 ├── State
 └── Runner
```

技术：

```text
Python
+
LangGraph / OpenAI Agents SDK
```

---

# Phase 2：Tool Layer

统一：

```text
MCP
```

把企业系统包装成：

```text
GitHub MCP
Jira MCP
Slack MCP
Database MCP
Kubernetes MCP
Cloud MCP
Security MCP
```

Agent 不直接连接企业系统。

而是：

```text
Agent
 ↓
MCP
 ↓
Policy
 ↓
Enterprise API
```

---

# Phase 3：Identity + Policy

这是企业版 Agent OS 最重要的一步。

建立：

```text
Agent Identity

Agent ID
Tenant
Owner
Role
Risk Level
Capabilities
Expiration
```

然后：

```text
Tool Request

        ↓
┌──────────────────┐
│ Policy Engine    │
└────────┬─────────┘
         ↓
       Allow?
      /      \
    YES       NO
    ↓          ↓
 Execute     Deny
```

---

# Phase 4：Memory + Context

设计：

```text
Working Memory
       ↓
Short Term
       ↓
Episodic
       ↓
Semantic
       ↓
Procedural
```

并建立：

```text
Context Manager
```

负责：

* compression
* summarization
* retrieval
* forgetting
* relevance
* token budget

---

# Phase 5：Scheduler

然后开始真正像 OS。

例如：

```text
Agent Job

priority: HIGH
token_budget: 100k
time_budget: 30min
risk: MEDIUM
model: GPT-x
```

Scheduler：

```text
Queue
 │
 ├── Priority
 ├── Cost
 ├── Quota
 ├── Resource
 └── Risk
```

最终：

```text
Agent Process
     ↓
RUNNING
     ↓
WAITING
     ↓
SUSPENDED
     ↓
RESUMED
     ↓
COMPLETED
```

---

# 二十三、Phase 6：Observability

这一步很多 Agent 项目严重缺失。

你不能只记录：

```text
Agent → Final Answer
```

必须记录：

```text
Agent Run
 │
 ├── Model Call
 │     ├── prompt
 │     ├── model
 │     ├── tokens
 │     └── latency
 │
 ├── Tool Call
 │     ├── tool
 │     ├── arguments
 │     ├── result
 │     └── policy decision
 │
 ├── Memory
 │     ├── read
 │     └── write
 │
 ├── Handoff
 │
 └── Human Approval
```

形成完整：

# **Agent Trace**

这和传统 distributed tracing 非常类似。

---

# 二十四、Agent OS 最大的优势

如果真正做出来，它会解决一个巨大的问题：

今天企业 Agent 往往是：

```text
Team A → LangChain
Team B → CrewAI
Team C → AutoGen
Team D → OpenAI SDK
Team E → Custom Agent
```

每个 Agent 都自己实现：

```text
Auth
Memory
Tools
Logging
Policy
Audit
Retry
Scheduler
```

结果：

> **Agent Infrastructure 极度碎片化。**

Agent OS 的价值就在于：

```text
             Agent OS
                 │
       ┌─────────┼─────────┐
       ↓         ↓         ↓
    Agent A   Agent B   Agent C
       │         │         │
       └─────────┼─────────┘
                 ↓
       Common Infrastructure
```

就像：

```text
Linux
 ↓
Applications
```

而不是：

```text
Application A → 自己实现 filesystem
Application B → 自己实现 networking
Application C → 自己实现 process manager
```

---

# 二十五、但是 Agent OS 也有非常严重的问题

这是我认为比“优势”更值得关注的部分。

## 1. LLM 本身不是 deterministic

传统 OS：

```text
if x > 5:
    do A
```

永远一致。

Agent：

```text
LLM
 ↓
"我认为应该调用 Tool A"
```

下一次可能：

```text
Tool B
```

所以 Agent OS 的 scheduler 可以 deterministic。

但：

> **Agent decision 本身不一定 deterministic。**

这会严重影响：

* testing
* reproducibility
* auditing
* debugging

---

# 二十六、2. Permission 不能交给 LLM

这是安全设计中最重要的原则之一。

错误：

```text
LLM:
"I believe I am authorized."

→ execute
```

正确：

```text
LLM
 ↓
Tool Request
 ↓
Policy Engine
 ↓
Identity
 ↓
Capability
 ↓
Resource
 ↓
Allow / Deny
```

即：

> **LLM 可以建议行动，但不能决定自己的权限。**

---

# 二十七、3. Memory 会成为新的安全边界

传统系统：

```text
Database
```

Agent OS：

```text
Memory
```

可能保存：

* 用户信息
* 企业机密
* previous decisions
* credentials references
* business strategy
* source code
* personal information

所以 Memory 本身需要：

```text
Authentication
Authorization
Encryption
Retention
Deletion
Tenant isolation
Audit
```

否则：

> Agent Memory 很可能成为新的数据泄露面。

---

# 二十八、4. Multi-Agent 不一定比 Single-Agent 好

这是现在 Agent 行业一个非常容易被营销误导的地方。

很多架构：

```text
Planner
 ↓
Researcher
 ↓
Coder
 ↓
Reviewer
 ↓
Tester
 ↓
Writer
```

看起来非常高级。

但实际上可能变成：

```text
10 × LLM calls
+
10 × latency
+
10 × failure points
+
10 × token cost
```

而单 Agent：

```text
Agent
 ↓
Tools
 ↓
Result
```

可能已经够了。

所以：

> **Multi-Agent 不是默认架构。**

只有当：

* task decomposition 明确
* agent specialization 明确
* parallelism 有价值
* isolation 有价值
* independent verification 有价值

才值得使用。

微软自己的 Agent Framework 文档也明确区分了 agent 和 workflow：开放式、自主规划更适合 agent；步骤明确、需要精确控制执行顺序的任务更适合 workflow。([GitHub][21])

---

# 二十九、5. Agent OS 可能成为新的“超级单点故障”

如果：

```text
                    Agent OS
                       │
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
     Finance         HR             Security
```

那么 Agent OS 出问题：

```text
Agent OS compromise
       ↓
ALL AGENTS
       ↓
ALL TOOLS
       ↓
ALL DATA
```

因此 Agent OS 本身必须是：

> **Zero Trust Architecture**

而不是：

> “一个超级管理员 Agent”。

---

# 三十、我认为未来真正有价值的 Agent OS Architecture

如果结合现在这些项目和技术，我认为比较合理的最终架构应该是：

```text
                       HUMAN
                         │
                         ↓
                ┌─────────────────┐
                │ Agent Gateway   │
                └────────┬────────┘
                         ↓
              ┌──────────────────────┐
              │   AGENT CONTROL PLANE│
              │                      │
              │ Identity             │
              │ Policy               │
              │ Scheduler            │
              │ Capability Registry  │
              │ Agent Registry       │
              │ Cost / Quota         │
              │ Governance           │
              └──────────┬───────────┘
                         ↓
              ┌──────────────────────┐
              │    AGENT RUNTIME     │
              │                      │
              │ LangGraph            │
              │ AutoGen              │
              │ OpenAI Agents SDK    │
              │ CrewAI               │
              └──────────┬───────────┘
                         ↓
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
     Context           Tools            Memory
        │                │                │
        ↓                ↓                ↓
  Context Manager      MCP         Vector / Graph
        │                │                │
        └────────────────┼────────────────┘
                         ↓
              ┌──────────────────────┐
              │ Secure Execution     │
              │ WASM / Sandbox       │
              │ Containers           │
              └──────────┬───────────┘
                         ↓
                Enterprise Systems
```

---

# 三十一、如果你是从 Enterprise / Security 角度研究

结合你之前关注的 **AI security、LLM testing、prompt injection、CI/CD 和 governance**，我其实认为 Agent OS 对你尤其值得研究。

因为 Agent OS 会把传统的：

> **LLM Security**

升级成：

# **Agent Runtime Security**

攻击面会从：

```text
Prompt
 ↓
LLM
```

变成：

```text
User
 ↓
Agent
 ↓
Context
 ↓
Memory
 ↓
Tool
 ↓
MCP
 ↓
Enterprise API
 ↓
Data
 ↓
Side Effect
```

于是 threat model 会发生巨大变化。

---

# 三十二、未来 Agent OS 的 Security Architecture

我会重点设计：

```text
                 Agent
                   │
                   ↓
          ┌─────────────────┐
          │ Intent Analysis │
          └────────┬────────┘
                   ↓
          ┌─────────────────┐
          │ Risk Classifier │
          └────────┬────────┘
                   ↓
          ┌─────────────────┐
          │ Policy Engine   │
          └────────┬────────┘
                   ↓
          ┌─────────────────┐
          │ Capability      │
          │ Check           │
          └────────┬────────┘
                   ↓
          ┌─────────────────┐
          │ Tool Guardrail  │
          └────────┬────────┘
                   ↓
             Tool Execution
                   ↓
          ┌─────────────────┐
          │ Output / Result │
          │ Validation      │
          └─────────────────┘
```

同时每一步都产生：

```text
Audit Event
```

最终形成：

# **Agent Security Audit Trail**

---

# 三十三、Agent OS 和你熟悉的 CI/CD Security 其实可以连接起来

这是一个非常有意思的方向。

今天：

```text
Developer
 ↓
Code
 ↓
CI
 ↓
Security Tests
 ↓
Deploy
```

未来 Agent：

```text
Agent
 ↓
Plan
 ↓
Tool Call
 ↓
Code Change
 ↓
Security Test
 ↓
Approval
 ↓
Deploy
```

于是可以建立：

```text
Agent OS
   +
AI Security Testing
   +
CI/CD
```

例如：

```text
Agent creates code
       ↓
Agent OS detects:
   "production deployment"
       ↓
Risk = HIGH
       ↓
Security Agent
       ↓
Prompt Injection Test
Tool Abuse Test
Data Exfiltration Test
Privilege Escalation Test
       ↓
PASS
       ↓
Human Approval
       ↓
Deploy
```

这比单纯测试 LLM 的 prompt 要高级得多。

因为测试对象已经变成：

> **Agent + Model + Context + Memory + Tools + Environment**

而不是只有：

> **LLM**

---

# 三十四、我对当前技术路线的判断

如果用一句话总结现在的市场：

### 2023

```text
LLM Application
```

### 2024

```text
RAG + Agents
```

### 2025

```text
Agent Framework
```

### 2026

正在向：

```text
Agent Runtime
        ↓
Agent Control Plane
        ↓
Agent Operating System
```

发展。

而真正成熟的 Agent OS，我认为还没有出现一个像 Linux 一样的绝对标准。

目前更像是几个方向正在汇合：

```text
AIOS
 │
 ├── OS research
 │
OpenFang
 │
 ├── Full Agent OS
 │
Rivet agentOS
 │
 ├── Secure lightweight runtime
 │
LangGraph
 │
 ├── Agent orchestration
 │
AutoGen / Microsoft Agent Framework
 │
 ├── Distributed multi-agent
 │
MCP
 │
 ├── Tool interoperability
 │
Letta
 │
 ├── Persistent memory
 │
OpenTelemetry
 │
 └── Agent observability
```

---

# 三十五、如果让我现在选技术栈

如果目标是：

> **2026 年构建一个企业级 Agent Operating System，而不是做一个 demo**

我的第一选择会是：

```text
                Enterprise Agent OS
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
   Control Plane     Runtime           Data Plane
        │                │                │
   Policy/IAM       LangGraph       MCP
   Scheduler        / Agent SDK     APIs
   Registry         AutoGen         Databases
   Quota            Agent Framework SaaS
   Governance
        │
        ├── Memory → Letta / Vector DB / Graph
        │
        ├── Sandbox → WASM / Containers
        │
        ├── Workflow → Temporal / LangGraph
        │
        └── Observability → OpenTelemetry
```

而不是直接：

```text
git clone AIOS
↓
把它当成 Enterprise Agent OS
```

因为目前真正缺的并不是一个“Agent Kernel”。

真正缺的是：

> **一个统一的 Agent Control Plane。**

---

## 最后给你一个最重要的判断

我认为 **Agent OS 真正的价值，不是“让 AI 变成操作系统”**。

真正的价值是：

> **把 Agent 从一个“会调用工具的 LLM 程序”，变成一个具有身份、生命周期、资源、权限、记忆、能力、状态、调度和审计的计算实体。**

传统 OS 管理的是：

> **Processes**

Agent OS 管理的是：

> **Autonomous Processes**

而这两者之间最关键的差别就是：

**传统 Process 不会自己决定下一步做什么；Agent 会。**

所以 Agent OS 最核心的三个东西最终不是 LLM，而是：

> **Scheduler + Policy + State**

这三个东西决定了 Agent 能不能真正进入企业生产环境。

---

如果你准备**从技术架构/Enterprise Security 的角度深入研究这个方向**，下一步我建议直接把它进一步拆成一张完整的 **“Enterprise Agent Operating System Architecture”**：我可以把 **AIOS / OpenFang / LangGraph / AutoGen / MCP / Letta / OpenAI Agents SDK / WASM Sandbox / Temporal / OpenTelemetry** 全部放进一张架构图，并进一步设计 **Agent Kernel、Control Plane、Data Plane、Identity、Capability、Policy Engine、Memory、Scheduler、Sandbox、Audit、Agent Security Testing** 的具体模块、API 和数据模型。这样会比单纯比较 Framework 更接近真正可以开始实施的设计。

[1]: https://arxiv.org/abs/2606.01508?utm_source=chatgpt.com "Agent Operating Systems (AOS): Integrating Agentic Control Planes into, and Beyond, Traditional Operating Systems"
[2]: https://docs.letta.com/guides/ade/overview?utm_source=chatgpt.com "Agent Development Environment (ADE) | Letta Docs"
[3]: https://modelcontextprotocol.io/docs/getting-started/intro?utm_source=chatgpt.com "What is the Model Context Protocol (MCP)? - Model Context Protocol"
[4]: https://www.osforagents.com/?utm_source=chatgpt.com "Agent Operating System | Infrastructure for Autonomous AI"
[5]: https://microsoft.github.io/autogen/dev/user-guide/core-user-guide/framework/agent-and-agent-runtime.html?utm_source=chatgpt.com "Agent and Agent Runtime — AutoGen"
[6]: https://github.com/agiresearch/AIOS?utm_source=chatgpt.com "GitHub - agiresearch/AIOS: AIOS: AI Agent Operating System · GitHub"
[7]: https://arxiv.org/abs/2403.16971?utm_source=chatgpt.com "AIOS: LLM Agent Operating System"
[8]: https://www.openfang.sh/?utm_source=chatgpt.com "OpenFang — The Agent Operating System"
[9]: https://github.com/rivet-dev/agent-os?utm_source=chatgpt.com "GitHub - rivet-dev/agent-os: A portable open-source operating system for agents. ~6 ms coldstarts, 32x cheaper than sandboxes. Powered by WebAssembly and V8 isolates. · GitHub"
[10]: https://www.mintlify.com/operatoronline/standard-operator/introduction?utm_source=chatgpt.com "Introduction - Operator OS"
[11]: https://docs.langchain.com/oss/python/langgraph/overview?utm_source=chatgpt.com "LangGraph overview - Docs by LangChain"
[12]: https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/index.html?utm_source=chatgpt.com "Core — AutoGen"
[13]: https://github.com/microsoft/semantic-kernel?utm_source=chatgpt.com "GitHub - microsoft/semantic-kernel: Integrate cutting-edge LLM technology quickly and easily into your apps · GitHub"
[14]: https://openai.github.io/openai-agents-python/agents/?utm_source=chatgpt.com "Agents - OpenAI Agents SDK"
[15]: https://openai.github.io/openai-agents-python/guardrails/?utm_source=chatgpt.com "Guardrails - OpenAI Agents SDK"
[16]: https://docs.letta.com/guides/get-started/for-agents?utm_source=chatgpt.com "Resources for AI agents building with Letta | Letta Docs"
[17]: https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/?utm_source=chatgpt.com "Gen AI | OpenTelemetry"
[18]: https://docs.crewai.com/core-concepts/Agents?utm_source=chatgpt.com "Introduction - CrewAI"
[19]: https://github.com/foundationagents/metagpt?utm_source=chatgpt.com "GitHub - FoundationAgents/MetaGPT: 🌟 The Multi-Agent Framework: First AI Software Company, Towards Natural Language Programming · GitHub"
[20]: https://github.com/OpenHands/openhands?utm_source=chatgpt.com "GitHub - OpenHands/OpenHands: 🙌 OpenHands: AI-Driven Development · GitHub"
[21]: https://github.com/MicrosoftDocs/semantic-kernel-docs/blob/main/agent-framework/overview/index.md?utm_source=chatgpt.com "semantic-kernel-docs/agent-framework/overview/index.md at main · MicrosoftDocs/semantic-kernel-docs · GitHub"

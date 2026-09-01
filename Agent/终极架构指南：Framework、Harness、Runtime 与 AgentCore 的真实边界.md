


在构建企业级 AI Agent 时，开发者常常会被满天飞的概念（Runtime, Harness, 平台, 框架）绕晕。要理清它们的结构，最关键的原则是**将它们放在不同的抽象层次来理解**。

一个核心定调：
> **AgentCore 不是 Runtime 的同义词，也不是 Harness 的同义词；它是 AWS 提供的一整套 Agent Infrastructure Platform（基础设施平台），其中包含了托管的 Runtime，并部分承担了底层的治理能力。**

---

### 1. Runtime 是什么？（底层执行引擎）

Runtime（运行时）主要回答一个物理和工程问题：
> **“Agent 的代码在哪里运行？怎么运行？怎么隔离？怎么维持执行生命周期？”**

**核心关注点**：进程/容器、会话（Session）、执行生命周期、弹性扩缩容（Scaling）、沙盒隔离（Isolation）、资源管理。

可以继续沿用这个类比：**Agent Runtime ≈ Agent 的操作系统 (OS)**。
在 AWS 的语境下，**AgentCore Runtime 就是 AWS 提供的高级托管 Agent 运行时**。它负责分配安全的 MicroVM，维持 Agent 会话的存活。

### 2. Harness 是什么？（操作支架与控制逻辑）

Harness 解决的问题完全不同，它回答的是逻辑问题：
> **“如何让一个大模型按照预定的方法，安全、可靠、可控地循环执行任务？”**

**核心关注点**：Agent Loop（执行循环）、工具选择策略、超时重试（Retry/Timeout）、人类确认（HITL）、上下文组装、状态流转（State transitions）。

**Harness 更偏向 Agent Execution Control Plane（执行控制面）**。
例如，下面这段最简单的代码，本身就是一个微型的 Harness：
```python
while not done:
    response = llm(messages)
    if response.tool_call:
        result = execute_tool(response.tool_call)
        messages.append(result)
    else:
        done = True
```

### 3. AgentCore 到底是什么？（基础设施平台）

AgentCore 更像是一个“超级底盘”：
> **“它把 Runtime、Gateway（网关）、Memory（记忆）、Identity（身份）、Sandbox（沙盒）以及 Observability（可观测性）等底层基础设施全部打包托管起来的平台。”**

因此：
*   **AgentCore ≈ Agent Infrastructure Platform (Agent 基础设施平台)**
*   **AgentCore Runtime ≈ 平台内部的 Agent Runtime 组件**

两者绝不能混为一谈。

---

### 4. LangGraph + AgentCore 的完美协同（谁负责什么？）

既然 AgentCore 这么强大，那还要 LangGraph 或 CrewAI 这种框架干什么？AgentCore 本身并没有替代你在应用层编写的“Harness 控制逻辑”。

在实际的企业级集成中，它们的职责边界非常清晰：

*   **LangGraph (Framework/Harness)**：负责编排 **Agent 的思考与推理工作流（Reasoning workflow）**。定义状态图、节点、边缘条件和工具调用时机。
*   **AgentCore Runtime**：负责提供 **Agent 的物理执行基础设施**。LangGraph 跑在它提供的隔离环境里。
*   **AgentCore Gateway**：负责 **工具与服务连接**（通过 MCP 协议）。
*   **AgentCore Memory**：负责 **跨会话持久化记忆**。
*   **AgentCore Sandbox**：负责 **危险代码的隔离执行**。

**集成架构图如下：**
```text
                 User Interaction
                       │
                       ▼
             ┌───────────────────┐
             │  LangGraph Agent  │ (负责控制逻辑/Harness)
             │                   │
             │ ├─ StateGraph     │
             │ ├─ Agent Loop     │
             │ └─ Tool Calls     │
             └─────────┬─────────┘
                       │ 部署并运行于
                       ▼
      ┌─────────────────────────────────┐
      │       AgentCore Platform        │ (负责基础设施)
      │                                 │
      │       [AgentCore Runtime]       │
      │                │                │
      │   ┌────────────┼────────────┐   │
      │   ▼            ▼            ▼   │
      │ Memory      Gateway      Sandbox│
      │ (持久化)   (MCP工具网关) (隔离执行) │
      └─────────────────────────────────┘
```
**总结一句话：LangGraph 决定“Agent 怎么思考和执行”，AgentCore 决定“这个 Agent 在哪里、以什么物理条件运行”。**

---

### 5. 业界生态：没有统一边界，只有不同侧重

目前行业并没有全球统一的标准边界，不同产品会将 Runtime、Harness 和 Infrastructure 的能力放在不同位置。不要试图给它们画严格互斥的盒子：

| 产品形态 | Runtime 能力 | Harness / Orchestration 能力 | 基础设施支撑 (Infrastructure) |
| :--- | :--- | :--- | :--- |
| **LangGraph** | 部分 (依赖宿主机) | **极强 (图编排/状态机)** | 依赖 LangGraph Platform |
| **OpenHands** | **强 (内置沙盒)** | **强 (内置 Loop 与策略)** | 强 (自带 Docker/Runtime) |
| **AgentCore** | **极强 (MicroVM)** | 部分 (平台级护栏与限制) | **极强 (AWS 全生态托管)** |

---

### 6. 现代 Agent 系统的终极架构参考模型

结合 2026 年的最新工程实践，最清晰的现代 Agent 架构应当如下划分：

```text
┌─────────────────────────────────────────────┐
│              Agent Application              │
│                                             │
│   (借助 LangGraph / CrewAI / Custom 编写)     │
│                                             │
│   ┌─────────────────────────────────────┐   │
│   │    Agent Harness (应用层控制逻辑)      │   │
│   │                                     │   │
│   │ ├─ Agent Loop (执行循环)            │   │
│   │ ├─ State / Workflow (状态/工作流)   │   │
│   │ ├─ Retry / Timeout (重试机制)       │   │
│   │ └─ HITL / Approval (人类审批流)     │   │
│   └──────────────────┬──────────────────┘   │
└──────────────────────┼──────────────────────┘
                       │ 部署 / 执行
                       ▼
┌─────────────────────────────────────────────┐
│          Agent Infrastructure Platform      │
│            (以 Amazon AgentCore 为例)         │
│                                             │
│   ┌─────────┐ ┌─────────┐ ┌─────────────┐ │
│   │ Runtime │ │ Gateway │ │   Memory    │ │
│   └─────────┘ └─────────┘ └─────────────┘ │
│   ┌─────────┐ ┌─────────┐ ┌─────────────┐ │
│   │Identity │ │ Sandbox │ │Observability│ │
│   └─────────┘ └─────────┘ └─────────────┘ │
│   ┌────────────┐ ┌───────────────────────┐ │
│   │ Evaluation │ │ Policy / Governance   │ │
│   └────────────┘ └───────────────────────┘ │
└─────────┬────────────┬────────────┬─────────┘
          │            │            │
          ▼            ▼            ▼
        AG-UI         MCP          A2A
      (用户交互)    (外部工具)    (多智能体协同)
```
*注：Harness 决定 Agent 怎么执行；Runtime 提供 Agent 执行环境；AgentCore 将 Runtime 及大量周边治理能力打包托管，并通过 AG-UI、MCP、A2A 协议连接外部世界。*

---

### 7. 架构概念快问快答 (TL;DR)

如果你向团队或面试官解释这三者的区别，请直接使用以下标准口径：

*   **问：AgentCore 是不是 Runtime？**
    *   **答**：不完全是。AgentCore *包含* Runtime，但 AgentCore 是一整套托管的 Agent 基础设施平台（Platform），不等于单纯的 Runtime。
*   **问：AgentCore 是不是 Harness？**
    *   **答**：不是。AgentCore 提供了 Harness 运行所需的护栏、内存和网关等基础设施，但核心的 Agent Loop、工作流流转（Orchestration）仍然由应用层的 Framework（如 LangGraph / CrewAI）构建的 Harness 来负责。
*   **问：请用一句话定义它们？**
    *   **AgentCore** = Managed Agent Infrastructure Platform（托管级智能体基础设施平台）。
    *   **AgentCore Runtime** = Managed Agent Execution Engine（托管级执行引擎）。
    *   **Agent Harness** = Agent Execution/Control Logic（智能体操作支架与控制逻辑）。
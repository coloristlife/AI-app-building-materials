
在当下的 AI 工程语境中，当你听到 **“AgentCore”** 这个词时，它通常明确指向 AWS 的基础设施产品：**Amazon Bedrock AgentCore**。

过去，大家容易把 AgentCore 误解为一个“超级 Agent Runtime（运行时）”。但事实上，**AgentCore 不是一个单纯的 Runtime，而是一套完全托管的、框架无关（Framework-agnostic）且模型无关（Model-agnostic）的 AI Agent 基础设施平台（Agent Infrastructure Platform）。**

如果继续我们之前的赛车比喻：
*   **LLM** = 发动机
*   **Agent Framework**（LangGraph / CrewAI） = 驾驶逻辑与大脑
*   **AgentCore** = **整套云端数字化底盘与车队控制中心**，而 Runtime 只是其中的执行引擎。

### 一、 一图看懂 AgentCore 的真实系统模型

AgentCore 并不是“一个黑盒”，而是由一组高度可组合的托管服务（Composable Services）构成的。它在系统中的真实位置如下：

```text
                     Agent Application
                           │
              ┌────────────┴────────────┐
              │                         │
        Agent Framework            Agent Logic
   (LangGraph / CrewAI / Strands) (Python / TypeScript)
              │
              ▼
       ┌─────────────────────────────────┐
       │       Amazon Bedrock AgentCore  │
       │                                 │
       │  Runtime ─────── Execution      │
       │  Gateway ─────── Tools / MCP    │
       │  Memory ──────── Persistence    │
       │  Identity ────── Auth / OBO     │
       │  Browser ─────── Web execution  │
       │  Code Interpreter ─ Sandbox     │
       │  Observability ── Tracing       │
       │  Evaluations ──── Quality       │
       │  Policy ───────── Governance    │
       └─────────────────────────────────┘
                    │
        ┌───────────┼───────────┬────────────┐
        ▼           ▼           ▼            ▼
       HTTP        MCP         A2A         AG-UI
     (Base)      (Tools)   (Agent↔Agent) (Agent↔User)
```

### 二、 AgentCore 包含哪些核心组合服务？

通过 `agentcore CLI` 虽然能大幅简化 Agent 的开发和部署，但在真实的企业生产环境中，部署一个 Agent 依然需要配置 VPC、IAM、网络和路由。AgentCore 为此提供了 9 大基础设施组件：

#### 1. Runtime（隔离运行时）
负责 Agent 的实际执行。它提供**完整的会话隔离（Session Isolation）**，底层采用安全隔离的 MicroVM 架构，并支持长达数小时（Long-running）的异步任务执行窗口。

#### 2. Gateway（智能体网关）
AgentCore 的工具与服务流量枢纽。它不仅负责流量路由，还能将传统 API、Lambda 转换为 Agent 可用的工具。支持 HTTP透传、MCP 会话管理，以及复杂的 OAuth 2.0 鉴权拦截。

#### 3. Memory（会话与长期记忆服务）
请注意，它并非简单的“多模态存储”，而是专注解决 Agent 上下文问题。它包含当前会话的状态（Session State）维护，以及跨会话的记忆提取（Memory Extraction）、事实存储与用户偏好检索（Retrieval）。

#### 4. Identity（身份与授权）
解决“Agent 到底代表谁在操作”的难题。原生支持 OAuth 委派认证和基于 **On-behalf-of** 的 Token 交换机制（例如：Agent 去查询 Jira，是严格以当前登录用户的身份去查，而不是用全局管理员 Token）。

#### 5. Code Interpreter & Browser（受隔离的执行环境）
这是两个独立的基础能力：
*   **Code Interpreter** 提供安全的沙盒代码执行（Sandboxed code execution）。
*   **Browser** 提供受管的浏览器运行环境，供 Agent 动态抓取和交互。

#### 6. Observability（全链路可观测性）
彻底打开 Agent 的黑盒。它提供 Agent 的执行轨迹（Trace）、工具调用耗时（Latency）、Token 消耗量、中间输出（Intermediate outputs）和执行路径审计。（注：它展示的是系统执行轨迹，而非大模型本身的 Chain-of-Thought）。

#### 7. Policy & Evaluations（治理与质量评估）
*   **Policy**：负责运行时级别的安全护栏（Guardrails）与策略授权熔断。
*   **Evaluations**：提供生产级 Agent 质量评估，内置多种 Evaluator 并支持自定义规则，用于测试任务完成率与安全性。

### 三、 服务契约与支持的 4 大开放 Protocol（协议）

AgentCore 并没有去“发明”所有行业标准，它的做法是：**自己定义严格的底层服务契约，同时全面拥抱和支持行业的开放通信协议。**

**底层服务契约**：无论你用什么框架，接入 AgentCore Runtime 都需要暴露标准的 HTTP `/invocations`（用于请求/响应）或 WebSocket `/ws`（用于流式交互）接口。

在对外交互上，AgentCore 原生支持以下 3 大核心行业协议：

1.  **MCP (Model Context Protocol)** —— **【管工具】**
    AgentCore Gateway 全面支持 MCP，将外部数百个企业 SaaS（Slack, Salesforce 等）或本地数据源，以标准化的格式挂载给 Agent。
2.  **A2A (Agent-to-Agent Protocol)** —— **【管 Agent 协同】**
    AWS 自 AgentCore GA 起即支持该协议。它提供标准化的 Agent 发现机制（基于 `/.well-known/agent-card.json`），定义了智能体的能力描述，并基于 JSON-RPC 2.0 over HTTP 实现跨越信任边界的智能体间标准化交互。
3.  **AG-UI (Agent-to-User Interface)** —— **【管前端交互】**
    解决 Agent 如何与前端展现层对话的问题。通过 AG-UI，运行在后端的 Agent 可以无缝桥接到前端的 CopilotKit 或 Vercel AI SDK 等 UI 组件，实现丰富的流式交互。

---

### 总结：一句话重新定义 AgentCore

AgentCore 并非已经一统天下的行业唯一标准（目前仍与 Microsoft Foundry Agent Service、LangGraph Platform 等激烈竞争），但它是目前最完整的云厂商 Agent 基础设施组合之一。

如果用最严谨的技术语言来总结：

> **Amazon Bedrock AgentCore 不是一个单独的 Agent Runtime，而是一套面向生产环境的、框架与模型无关的 Agent Infrastructure Platform；Runtime 负责 Agent 执行，Gateway 负责工具与服务接入，Memory 负责跨会话记忆，Identity 负责身份与授权，Browser/Code Interpreter 提供受隔离的执行能力，Observability/Evaluations/Policy 则负责生产运营与治理。同时，它通过 HTTP、MCP、A2A 和 AG-UI 等标准协议，将 Agent、工具、其他 Agent 以及用户界面紧密而安全地连接在一起。**
这是结合了最新行业工程实践（如 Microsoft、Cloudflare 的架构定义）以及所有修正反馈后，重新梳理的**最终完整版本**。你可以直接将这份内容用于你的技术文档、博客或架构讨论中。

---

# 重新定义 AI Agent 架构：LLM、Runtime 与 Harness 的真实边界

在讨论现代 AI Agent 架构（如 LangGraph、OpenHands、AutoGen）时，开发者经常混淆三个概念：LLM、Agent Runtime（运行时）和 Agent Harness（智能体支架）。

如果我们将开发一个 Agent 比作造一辆自动驾驶赛车，那么它们在系统中的真实分工如下：

*   **LLM（大脑/发动机）**：提供核心的动力与推理能力，决定当前该“加速、转向还是刹车”。
*   **Agent Runtime（底盘与底层基础设施）**：提供基础的运行环境支撑，比如状态流转（State）、会话管理（Session）、并发调度以及沙盒环境的拉起。
*   **Agent Harness（驾驶控制系统与操作支架）**：将发动机、方向盘（Tools）、状态、权限和执行环境组织起来，让它成为一台能真正跑完赛道的车。**Harness 不是挂在 Runtime 外面的简单“安全套件”，而是驱动大模型真正表现为 Agent 的控制层。**
*   **Guardrails & Sandbox（刹车系统 & 隔离赛道）**：由 Harness 调度与调用的安全组件，负责限速、防撞和风险隔离。

---

### 一、 Agent Harness 包含哪些核心功能？

严格来说，业界目前并没有定义出统一的“Harness 标准模块”。Harness 的本质是**将大模型转化为实际可用 Agent 的操作支架（Scaffolding）**。

在一个**面向生产环境（Production-oriented）**的复杂架构中，Agent Harness 通常不包含底层基础设施（如沙盒本身），而是作为“控制层”提供以下核心能力：

#### 1. 执行循环与工具编排 (Agent Loop & Tool Orchestration)
这是 Harness 最核心的工作。它负责组装 Prompt、解析模型的意图、决定调用哪个工具，并处理工具返回的结果，维持整个“思考-行动-观察”（Thought-Action-Observation）循环的持续运转。

#### 2. 上下文与记忆加载 (Context Management)
Harness 负责在每次模型调用前，将当前任务的状态、历史对话、系统 Prompt 按照特定策略（如滑动窗口、Token 截断）组装成模型能理解的上下文。

#### 3. 权限、策略与护栏 (Permissions, Policies & Guardrails)
Harness 决定了 Agent “绝对不能干什么”，通常包含：
*   **预算与限制 (Budgeting)**：执行硬性的资源策略，如限制最大 Token 消耗、最大执行步数（Max steps）或单次任务最大成本，防止 Agent 陷入死循环吞噬资金。
*   **安全拦截 (Guardrails)**：在输入/输出阶段过滤隐私数据（PII），阻断 Prompt 注入攻击；或基于策略执行动作熔断（例如：允许查询数据库，但拒绝执行 `DROP` 指令）。

#### 4. 执行环境路由与管理 (Environment Routing)
**Harness 本身不是沙盒，但它负责管理沙盒。** 当 Agent 试图执行一段不受信任的 Python 代码或 Bash 命令时，Harness 会截获请求，将其安全地路由到底层的 Docker 或 VM 隔离环境中执行，并将结果取回。

#### 5. 可观测性与生命周期 (Observability & Lifecycle)
优秀的 Harness 会记录 Agent 的完整执行轨迹（Trace）。在非确定性的大模型环境中，提供录制（Record）和回放（Replay）功能，帮助开发者在出 Bug 时回溯排查：到底是代码写砸了，还是大模型“抽风”了。

---

### 二、 有没有统一的定义和 Protocol？

简短的回答是：**完全没有。**

在目前的 AI 软件工程界，**"Agent Harness" 这个词存在极强的多义性（Polysemy）**。有时它被当成完整的 SDK，有时被当成 Agent Loop 的编排器，而在学术界和测评领域，它又经常专门指代“评估支架（Evaluation Harness）”。目前行业内**不存在**像 HTTP 那样的通用 Protocol。

尽管缺乏统一标准，但在**评估（Eval）**和**安全控制**这两个细分切面上，已经形成了极具代表性的开源标杆：

#### 1. Inspect AI (由英国 AI 安全研究所 UK AISI 开源)
这是目前极具代表性的**通用 AI 评估框架**。它提供了高度标准化的 `Dataset`（数据集）、`Task`（任务）、`Solver`（即待测的 Agent）和 `Scorer`（评分器）抽象，是构建 Evaluation Harness 的优秀基础设施。

#### 2. SWE-bench Harness
在 AI Coding Agent（AI 程序员）领域，SWE-bench 是目前最有影响力的公开基准测试之一。它的 Evaluation Harness 专门解决“如何公平地测试代码能力”——它提供标准化的测试支架，自动拉起 Docker 容器、注入目标仓库、应用 Agent 写出的代码补丁并运行测试用例，最后生成评估报告。

#### 3. NVIDIA NeMo Guardrails
在安全控制领域，NeMo Guardrails 是极具代表性的**安全护栏框架**（Framework，而非 Protocol）。它通常被作为核心的 Guardrails 组件集成到生产级 Agent Harness 中，用于在传统确定性策略与大模型非确定性输出之间建立隔离墙。

---

### 三、 一图看懂现代 Agent 系统的分层架构

为什么在研究 LangGraph、OpenHands、Goose 等框架时，总觉得 Runtime 和 Harness 的边界很模糊？**因为这些前沿框架往往同时混合了这两个层的能力。**

如果要在严谨的系统工程下划分边界，现代 Agent 系统的架构图如下所示：

```text
                 ┌──────────────────────┐
                 │       Agent UI       │  (Vercel AI SDK, CopilotKit 等)
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    Agent Harness     │  (操作支架 / 控制层)
                 │                      │
                 │ ├─ Agent Loop        │
                 │ ├─ Context/Memory    │
                 │ ├─ Tool Orchestration│
                 │ ├─ Permissions       │
                 │ ├─ Policies/Budget   │
                 │ └─ Lifecycle         │
                 └──────────┬───────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
     Agent Runtime       Sandbox      Tool Runtime  (底层运行基础设施)
  (LangGraph 底层状态机等) (Docker/VM等)
             │
             ▼
        State / Session  (状态与持久化层)
             │
             ▼
            LLM          (模型与推理层)
```

**与生产环境平行的测试环境（Evaluation Harness）：**
```text
          Evaluation Harness (如 SWE-bench, Inspect)
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
    Dataset    Environment  Scorer
                  │
                  ▼
             Agent Harness  (将待测的 Agent 接入测试环境)
```

### 总结

*   **Runtime** 提供 Agent 执行所依赖的底层基础设施（图、状态流转、并发）。
*   **Agent Harness** 则把模型、工具、上下文、策略和运行环境组织成一个能够持续完成任务的 Agent，并负责其执行控制、权限和可靠性。
*   **Evaluation Harness** 则是 Harness 的一个专门变体，不用于生产，重点解决可重复测试和打分。

搞清楚这三个概念的层级关系，在设计企业级 Agent 系统或研读开源项目源码时，就能清晰地定位每一个模块的真实职责，不再被眼花缭乱的流行词汇所迷惑。
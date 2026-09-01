


在 AI Agent 基础设施领域，**Agent Harness**（智能体运行脚手架/控制层）是一个核心概念，但它经常被与框架（Framework）、运行时（Runtime）或评估系统（Evaluation）混淆。

如果用一句话来精准定义它：
> **Agent Harness 是围绕 LLM/Agent 的运行与控制层。它通过执行循环（Agent Loop）、工具调度、上下文管理、权限安全以及生命周期机制，把模型的推理能力转化为可持续、可控制、可观察的实际行动；当它进一步挂载任务和评估器时，就衍生出了 Evaluation Harness（评估脚手架）。**

为了更好地理解它，我们需要重塑一下类比模型：
*   **LLM**：大脑（Reasoning Engine，负责推理）。
*   **Agent**：有目标、有状态、具备调用工具能力的行动主体。
*   **Agent Harness**：神经系统与控制外骨骼（负责驱动循环、调度工具、提供安全边界）。
*   **Environment**：Agent 探索和操作的世界（如终端、浏览器、数据库）。

---

### 一、 为什么我们需要 Agent Harness？

Harness 的核心价值不仅在于“安全运行”，更在于**将 LLM 从“生成文本的机器”变成“持续执行任务的引擎”**。具体体现在以下四个方面：

1.  **驱动持续行动（Agentic Loop）**
    LLM 本质上只是一次性的文本生成器。Harness 负责解析 LLM 的输出（例如“我要执行 git diff”），将其路由到工具执行器，执行后获取结果（Observation），再将其塞回给 LLM。它维系着 `Model → Tool → Result → Model` 的持续运转。
2.  **上下文与状态管理（Context & State Management）**
    Agent 在长程任务中容易丢失记忆。Harness 负责维护上下文窗口，管理短期/长期记忆，以及在出错时执行重试和状态恢复（Retry / Recovery）。
3.  **权限与安全沙盒（Permissions & Safety Guardrails）**
    Agent 具备改变外部世界的能力。Harness 负责拦截危险指令，并通常将工具执行放置在受控的执行环境（Execution Environment）中（如 Container、VM、microVM 或 Cloud Sandbox），结合文件系统和网络限制，防止 Agent 越权操作（如防止恶意执行 `rm -rf /`）。
4.  **生命周期与预算控制（Lifecycle & Budget）**
    防止 Agent 陷入死循环。Harness 通过设置最大步数（Max Steps）、时间限制或 Token 消耗预算（Budget限制）来强制接管和终止任务。

---

### 二、 Agent Harness 的核心运作机制

Harness 的运作核心是一个**Agent 执行循环（Execution Loop）**。虽然 ReAct（Observe → Reason → Act）是其中一种最常见的模式，但 Harness 同样可以驱动 Plan & Execute、Supervisor 等更复杂的路由流。

其标准架构流转如下：

```text
              ┌──────────────┐
              │     Agent    │ ◄── (LLM 产生意图与策略)
              │ LLM + Policy │
              └──────┬───────┘
                     │ Action (指令输出)
                     ▼
              ┌──────────────┐
              │   Harness    │ ◄── (拦截解析、安全校验、状态更新)
              │              │
              │ Policy       │
              │ Tool Router  │
              │ State/Limits │
              └──────┬───────┘
                     │ Call (真实动作)
                     ▼
              ┌──────────────┐
              │ Environment  │ ◄── (受限的沙盒环境)
              │ Sandbox      │
              └──────┬───────┘
                     │ Observation (执行结果、报错信息)
                     └──────────────► Agent
```
在这个过程中，Harness 的**轨迹记录器（Trajectory Logger）**就像飞机的黑匣子，会记录下每一步的 Prompt、响应、耗时和工具调用状态，用于后续的 **Debug、失效分析（Failure Analysis）、可观测性（Observability）**，以及在处理后生成用于模型优化的训练数据。

---

### 三、 关键辨析：Agent Harness vs. Evaluation Harness

当前行业的术语混乱，很大程度是因为人们把“运行控制层”和“测试考场”混在了一起。我们需要明确区分两者：

**1. Agent Harness（生产/运行基建）**
*   **职责**：让 Agent 能够**安全、稳定、持续**地运行。
*   **核心组件**：Agent Loop、Tool Router、State/Memory、Safety/Sandbox、Observability。
*   **注意**：它**不需要**预设标准答案，也不负责给 Agent 打分。

**2. Evaluation Harness（评估/测试基建）**
*   **职责**：为 Agent 提供一个**可重复、可比较的“标准化考场”**。
*   **核心组件**：在 Agent Harness 的基础上，加入了 Task Definition（固定任务）、Evaluator（评估器阅卷机制）、Scoring（打分逻辑）和 Benchmark Reporting。

**重新审视业界著名的案例：**
*   **SWE-bench Harness**：严格来说是 **Evaluation Harness**。它搭建了一致的 Docker 环境，给 Agent 喂真实 GitHub Issue，并运行预设的 Unit Tests 来评估 Agent 的代码修复能力。
*   **WebArena**：属于 **Benchmark 环境 + Evaluation Harness**。它提供了自托管的电商/论坛等模拟环境，以此评测 Web Agent 到底做得好不好。
*   **OpenAI Evals**：属于 **Evaluation Framework (评估框架)**，专注于对大模型及其系统的输出进行系统性基准测试和打分。

---

### 四、 全景图：Agent 领域的概念坐标系

为了更清晰地定位 Agent Harness，我们可以参考下表，理清现代 AI 基础设施的层级体系：

| 概念 | 解决的核心问题 |
| :--- | :--- |
| **LLM (大模型)** | 我能产生什么样的推理和输出（Reasoning）？ |
| **Agent (智能体)** | 我如何围绕特定目标，运用策略持续行动？ |
| **Agent Harness** | **我（系统）如何让 Agent 可控、安全地持续运行和调用工具？** |
| **Agent Framework** | 开发者如何便捷地编写和组织 Agent 代码（如 LangChain/Autogen）？ |
| **Agent Runtime** | Agent 代码如何在生产环境中被部署、托管和执行？ |
| **Evaluation Harness** | **到底怎么客观评测 Agent 任务完成得好不好？** |
| **Environment** | Agent 身处并要去改变的世界是什么（如 Bash、Browser、DB）？ |
| **Orchestrator** | 多个 Agent 之间（Workflow）应该如何协调工作？ |

#### 终极架构图谱
如果把所有的组件堆叠起来，一个成熟的 Agent 工程体系架构如下：

```text
                    ┌─────────────────────────────┐
                    │        Evaluation Layer     │ (评测层)
                    │ Task / Benchmark / Evaluator│
                    │ Score / Regression / Report │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │       Agent Harness         │ (控制与运行脚手架)
                    │ Agent Loop                  │
                    │ Context Management          │
                    │ State / Memory / Lifecycle  │
                    │ Tool Routing / Safety       │
                    │ Observability (Trajectory)  │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │          Agent / LLM         │ (大脑与策略主体)
                    │ Reasoning / Planning / Action│
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │         Environment          │ (操作环境与沙盒)
                    │ Browser / Repo / Shell / DB  │
                    │ APIs / Cloud / Filesystem    │
                    └──────────────────────────────┘
```

**总结：**
Agent Harness 是从“让模型聊天”走向“让模型可靠干活（Agentic Workflow）”不可或缺的基础设施。它不负责决定 AI 有多聪明，而是负责提供一套**神经控制系统**和**安全装甲**，确保智能体的每一步执行都在预期的轨道上，进而为上层的评估与应用落地提供地基。

- **Harness（脚手架）就像是“试车场、安全带和遥测系统”**。当车造好后，你要把它放进 Harness 里跑。Harness 会提供跑道（Environment），监控车速（Observability），并且在车快要撞墙时强制刹车（Safety/Lifecycle limit）。
- 如果你在解决 **“我该怎么用 Python 优雅地把 LLM 和 5 个 API 连起来”** 的问题，你需要的是 **Framework**。    
- 如果你在解决 **“这个写好的 Agent 怎么安全地在客户的服务器上持续运行 24 小时，且不能把客户的数据库删了，同时还得记录它每一步想了什么”** 的问题，你需要的是 **Agent Harness**。
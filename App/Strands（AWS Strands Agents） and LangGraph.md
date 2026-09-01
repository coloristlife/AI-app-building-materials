**Strands（AWS Strands Agents）** 和 **LangGraph** 都是用于构建 AI 智能体（AI Agents）的开源框架，但它们的**核心设计理念和适用场景有着根本的区别**。

简单来说：**LangGraph 强调“开发者掌控一切”（图驱动/状态机），而 Strands 强调“让模型来做决定”（模型驱动/极简循环）。**

以下是两者的详细对比和核心区别：

### 1. 核心设计理念对比

*   **LangGraph（图驱动/工作流）**：
    *   由 LangChain 推出，将智能体的工作流抽象为**有向图（Graph）**。
    *   开发者需要手动定义节点（Nodes，如 Agent 或 Tools）和边（Edges，如条件路由），构建一个完整的状态机。
    *   **哲学**：开发者明确规定每一步的执行逻辑和路径，适合高度复杂、需要严密控制的业务流程。
*   **Strands（模型驱动）**：
    *   由 AWS 在 2025 年开源的轻量级 SDK。
    *   **哲学**：将控制权交还给大模型（LLM）。你只需要提供一个 Prompt（提示词）和一组 Tools（工具），Strands 会构建一个“智能体循环”（Agentic Loop）。模型自己通过推理（Reasoning）来决定该调用什么工具、下一步做什么，直到任务完成。
    *   正如它的名字“Strands（股/线）”所暗示的，开发者提供单根线（工具），由模型动态地将它们“编织”在一起，而不是像 LangGraph 那样由开发者手动去编织。

### 2. 详细特性对比

| 维度 | LangGraph | Strands Agents (AWS) |
| :--- | :--- | :--- |
| **控制权归属** | 开发者（通过显式编写代码控制路由和流转） | LLM 大模型（模型自主决定步骤和工具调用） |
| **代码量与复杂度** | 较高。需要编写大量模板代码来定义状态（State）、节点和图结构。学习曲线陡峭。 | 极低。只需几行代码（定义模型 + 注入工具），几乎没有模板代码（Boilerplate）。 |
| **状态管理与容错** | 极强。支持持久化执行、时间旅行调试（Time-travel debugging）、回溯以及人工干预（Human-in-the-loop）。 | 较轻量。依赖模型的上下文窗口和简单的 Hook 机制，更适合纯自治的场景。 |
| **多智能体 (Multi-Agent)** | 擅长宏观、复杂的分布式多智能体编排（如监督者模式、层级模式）。 | 支持智能体间通信（A2A），偏向轻量级的任务委托。 |
| **生态与背景** | LangChain 生态，独立于云厂商，被广泛应用于各类企业中。 | AWS 主导，对 AWS 生态（如 Amazon Bedrock, AgentCore）支持极好，但也支持任意第三方模型（Anthropic, OpenAI, 本地模型等）。 |

### 3. 它们可以结合使用吗？

实际上，在企业级生产环境中，**它们并不是非此即彼的竞争关系，而是经常被结合使用**：

*   **LangGraph 作为“宏观编排器” (Macro-Orchestrator)**：负责整体业务工作流的状态流转。比如，一个金融审计系统，必须严格按照“数据收集 -> 初审 -> 人工审批 -> 输出报告”的固定流程走。
*   **Strands 作为“微观推理引擎” (Micro-Reasoning Engine)**：在 LangGraph 的某一个特定节点中（比如“数据收集节点”），使用 Strands 部署一个自治 Agent，让它自己决定如何使用数据库查询工具、网页搜索工具来完成数据收集任务。

### 4. 总结：你应该怎么选？

*   **选择 Strands 如果：** 你想要快速开发（几行代码就能跑起来），你相信当前大模型（如 Claude 3.5/4 或 GPT-4o）的推理和规划能力，你希望系统是**高度自治**的，或者你的团队重度使用 AWS 基础设施。
*   **选择 LangGraph 如果：** 你的业务场景容错率极低，你需要明确知道系统下一步会走到哪里，你需要**强状态控制**、支持断点重启、人工审核介入（Human-in-the-loop），并且你不介意编写更复杂的图代码。


两者都是"构建 agent 应用"的框架,但设计哲学不同——**Strands 是"模型驱动的执行循环"框架,LangGraph 是"显式状态图"框架**。结合我们刚看过的 DojoAgents 源码,可以把差异讲得比较具体。

### 核心编程模型

|         | **Strands Agents**(AWS 开源)                                                    | **LangGraph**(LangChain 团队)                                                  |
| ------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| 控制流表达方式 | 一个隐式循环:模型自己决定"要不要调工具、调哪个、要不要继续"                                               | 显式图:你手写 node + edge(含条件边),流程图就是代码                                            |
| 心智模型    | 类似经典 ReAct loop——"喂 messages → 模型输出 → 有 tool_use 就执行 → 结果塞回 messages → 再喂给模型" | 状态机——每个 node 是一个函数,接收/返回一个强类型 `State`(TypedDict/Pydantic),edge 决定下一步去哪个 node |
| 谁在"决策"  | LLM 在循环内部自主决策下一步动作                                                            | 你在图定义阶段就决定了大部分分支逻辑,LLM 只负责节点内的具体任务                                           |

### 从 DojoAgents 代码能直接印证的差异

1. **循环边界很薄**:DojoAgents 里我们看到 `agent.invoke_async(limits=Limits(turns=max_iterations))`——这就是 Strands 提供的全部"控制流"能力,一个轮次上限而已。**没有"图"这个概念**。
2. **正因为 Strands 循环本身很薄,DojoAgents 不得不在外面自己叠一层复杂的编排逻辑**:Harness completion 评估驱动的恢复循环、legacy task harness 的 `validate_progress`/`build_recovery_prompt`、多轮 pipeline 续跑(`session_run.py` 的 `CanonicalAgentRun`)——这些如果是用 LangGraph 做,大概率会直接建模成图里的条件边和子图,而不需要在 Strands 之外单独写一套状态机。
3. **扩展机制是 Hook 而不是 Node**:我们看到的 `BeforeToolCallEvent/AfterToolCallEvent/BeforeModelCallEvent/AfterModelCallEvent` 是 Strands 提供的横切拦截点,DojoAgents 靠它挂 Memory、Token 压缩、Guardrail——这是一种"事件订阅"式扩展,而不是"往图里加一个节点"式扩展。
4. **Model/Tool 抽象很干净**:`DojoStrandsModelBridge(Model)` 和 `DojoBridgedTool(AgentTool)` 这两个接口非常薄、职责单一,这也是 DojoAgents 能轻松把自己的 Provider/Tool 体系套进去的原因。LangGraph 这边模型/工具抽象通常直接借用 LangChain 生态(`BaseChatModel`/`@tool`),耦合度更高但生态更丰富。

### 关键差异总结

- **状态管理**:LangGraph 有一等公民的 `State` + 内置 checkpointer(支持 time-travel、human-in-the-loop 中断恢复);Strands 的状态基本就是 `messages` 列表 + 一个 `invocation_state` dict,更轻量但也更弱——这也解释了为什么 DojoAgents 要自己再造一套 `session_run.py`/`SessionService` 持久化体系,因为 Strands 原生没给够。
- **复杂分支流程**:如果任务天然是"多步骤、有明确条件分叉、需要人工审核节点暂停恢复"(比如审批流、多阶段数据处理管线),LangGraph 的图模型表达起来更自然;Strands 更适合"单个 agent 在一个循环里自主决策"的场景。
- **多智能体编排**:LangGraph 天然支持子图/supervisor 模式做多智能体;Strands 也支持(agent-as-tool、swarm),但更偏"扁平组合"而非"图嵌套"。
- **生态/绑定**:Strands 出自 AWS,对 Bedrock 支持最好但也做了厂商无关的 Model 抽象(DojoAgents 正是利用这点接入了 OpenAI 兼容/Gemini 原生);LangGraph 依赖 LangChain 生态,模型/工具/生态插件极其丰富但耦合也更重。

**一句话建议**:如果你的场景更接近"单 agent 自主循环、需要保留大部分定制权、想要一个轻量执行内核自己往上叠治理逻辑"(DojoAgents 走的正是这条路),Strands 这类框架合适;如果你的场景本质是"一个有明确分支、循环、审核节点的工作流,agent 只是其中的节点",LangGraph 的显式图模型会让你少写很多"自己造的状态机"。
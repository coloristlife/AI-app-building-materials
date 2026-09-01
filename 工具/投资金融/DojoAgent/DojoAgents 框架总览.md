

DojoAgents 是一个分层的 Agent 框架：**宿主应用（Host）→ Runtime → Harness → AgentCore（strands 驱动的执行循环）→ Session/Memory/Skills** 层层包裹。下面按层展开，每层标注是自研还是基于三方库。

---

# 第三方库依赖一览（pyproject.toml）

```
openai              # LLM API 客户端（OpenAI 兼容协议）
strands-agents      # 核心 Agent 执行循环（AWS 开源的 Agent SDK）
strands-agents-tools
mcp                 # Model Context Protocol 官方 SDK（外部工具接入）
dojosdk             # 内部/私有 财务数据 SDK（公司自己的）
fastapi / uvicorn   # dashboard 的 HTTP 服务层
apscheduler         # 定时任务调度（scheduler 模块）
pandas / pyarrow    # 数据处理
exchange-calendars  # 交易日历
portalocker         # 文件锁（session/config 并发写保护）
ddgs                # DuckDuckGo 搜索（web_searcher 工具）
openpyxl / pypdf / pillow   # Excel/PDF/图片处理
pyinstrument        # 性能画像
```

**判断标准很清晰：`strands` 负责"跟 LLM 对话、管理一次 tool-call 循环"这个最底层能力；其余几乎所有"Agent 应该怎么组织、工具怎么注册、会话怎么存、Skill 怎么加载、Harness 怎么隔离场景"全部是 DojoAgents 自己写的。**

---

# 一、AgentCore（核心执行层）—— 自研为主，底层引擎借用 strands

**AgentCore** 不是一个具体类名，而是注释里明确提到的一个"层"概念（[runtime.py:412-415](https://claude.ai/epitaxy/dojoagents/agent/runtime.py:412)）：跟具体业务场景（Harness）无关的、每个 Agent 都该有的能力，包括：

- **`AgentLoop`**（[agent/loop.py](https://claude.ai/epitaxy/dojoagents/agent/loop.py)）—— 自研的"回合驱动器"：拼 system prompt、收集工具、调用底层模型、处理压缩/记忆/多模态/多轮恢复等。
- **底层真正跟模型对话、驱动 tool-call 循环的是 `strands.Agent`**（[loop.py:1459](https://claude.ai/epitaxy/dojoagents/agent/loop.py:1459)），DojoAgents 把自己的 `strands_tools`/hooks/plugins 塞进这个三方 `Agent` 实例，由它去做实际的"发消息给模型→收 tool_use→再发回"的事件循环、流式输出（`StreamEvent`）、hook 机制（`BeforeToolCallEvent`/`AfterToolCallEvent`）。
- **`ToolRegistry`/`ToolSpec`/`ToolExecutor`**（[tools/registry.py](https://claude.ai/epitaxy/dojoagents/tools/registry.py), [tools/executor.py](https://claude.ai/epitaxy/dojoagents/tools/executor.py)）—— 全自研，是我们前面反复讨论的工具注册与调用中枢。
- **`SandboxPolicy`** —— 自研，限制工具能访问的目录/命令/网络/超时。
- 一批"核心工具"：terminal、code_execution、session 文件读写、web_searcher、tools_list —— 全部自研，与场景无关，两条 Runtime 构建路径（现代 harness 路径 `_build_harness_agent` 和 legacy 路径 `from_config_store`）都各自注册一份，保证任何 Harness 都有这套基础能力。

**结论：AgentCore = 自研的"工具注册/执行/沙箱/核心工具"体系 + 借用 strands 做最底层的模型交互循环。**

---

# 二、Harness（场景能力插件）—— 完全自研

Harness 是 DojoAgents 里"一个具体业务场景"的封装单元（比如财务分析场景 `FinancialHarness`）。核心抽象非常薄、纯 Python `Protocol`（[harnesses/base.py](https://claude.ai/epitaxy/dojoagents/harnesses/base.py)）：

```python
class AgentHarness(Protocol):
    descriptor: HarnessDescriptor
    def configure(self, builder, context) -> None: ...
    async def startup(self, context) -> None: ...
    async def shutdown(self, context) -> None: ...
```

一个 Harness 通过 `configure(builder, ...)` 往 `HarnessBuilder` 里声明一整套"能力"：

- **工具 provider**（`ToolProviderSpec`）——比如财务的 domain/portfolio/sdk/visualization 工具
- **服务**（`ServiceSpec`，比如 `FINANCIAL_SERVICE_ID`）
- **Prompt 贡献者**（`PromptContributorSpec`，按 phase 分层拼系统提示词：identity/temporal/harness_instructions/memory/request_context/turn_policy/channel_policy/task_context）
- **Flow policy / Tool authorizer / Tool transformer**（每轮开始前的策略、工具调用前的授权、结果修复策略——比如我们看过的 `PortfolioFlowPolicy`、`PortfolioToolRepairPolicy`）
- **Result presenter / Artifact adapter**（把工具的原始 JSON 结果转成给用户看的可读呈现）
- **Skill source / Memory provider / Task/Pipeline source**

`HarnessLoader` 按 `agents.yaml` 里配置的 `harness.id`（如 `"financial"`）从一个别名表动态 import 对应工厂函数实例化（[loader.py:16](https://claude.ai/epitaxy/dojoagents/harnesses/loader.py:16)）。

**`HarnessRuntime`**（[harnesses/runtime.py](https://claude.ai/epitaxy/dojoagents/harnesses/runtime.py)）是自研的"执行门面"，把 Harness 声明的这些能力组织成可执行的四个动作：`before_turn`（拼 prompt）、`transform_calls`（修复/改写工具调用）、`authorize`（工具调用授权）、`present_results`（结果呈现）、`evaluate_completion`（判断这轮是否该结束）。

**`LifecycleManager`**（[harnesses/lifecycle.py](https://claude.ai/epitaxy/dojoagents/harnesses/lifecycle.py)）自研的依赖排序服务启动器，负责把 `ServiceSpec` 按依赖拓扑排序启动，并支持宿主应用注入外部服务实例（`ExternalServiceBinding`，就是我们之前分析的 `DashboardFinancialAgentBackend` 注入方式）。

**结论：Harness 整套（builder/composer/lifecycle/policies/presenters/prompts）全部自研，是这个框架里工程量最大、最核心的自研部分。**

---

# 三、Runtime —— 自研的"装配 + 生命周期"外壳

`Runtime`（[agent/runtime.py](https://claude.ai/epitaxy/dojoagents/agent/runtime.py)）本身是一个 `dataclass`，是整套系统对外的门面对象，自研。它有两条互斥的构建路径（我们前面详细聊过）：

1. **`Runtime.create()` → `compose()`（`RuntimeComposer`）→ `startup()`（`_build_harness_agent()`）**——现代路径，围绕 Harness capability 图组装，异步、支持外部服务绑定（宿主注入 backend）。
> 是源码自己在报错信息、字段命名、状态机设计上明确把 `from_config_store` 定性为 "deprecated / legacy"，把 `Runtime.create()`（进而调用 `_build_harness_agent()`）定性为当前推荐、且新 Harness（如财务 Harness）唯一支持的构建方式


2. **`Runtime.from_config_store()`**——legacy 同步路径，硬编码注册一批核心工具+多智能体池+planning，只用于还没迁移到 capability 模型的老 Harness。

两条路径最终都产出一个 `AgentLoop` 实例挂在 `self.agent` 上。

---

# 四、Session（会话层）—— 自研

`SessionService`/`SessionStore`/`BlobStore`（[sessions/](https://claude.ai/epitaxy/dojoagents/sessions)）负责：

- 持久化对话历史（`session_store`，可插拔存储后端）
- 大对象/artifact 存储（`blob_store`）
- 会话状态编解码（`state_codec`，Harness 可以自定义，比如 `FinancialSessionStateCodec`）
- 记忆同步 worker（`SessionMemorySyncWorker`，异步把会话内容同步进 `MemoryManager`）

这套是纯自研的持久化/状态管理层，不依赖 strands（strands 本身不管跨会话持久化）。

---

# 五、宿主应用（Host）—— 自研的接入层，各自不同技术栈

"宿主应用"指的是**嵌入/驱动 Runtime 的外部程序**，`host` 参数标记了是谁在用（`"library"`/`"dashboard"`/`"cli"`/`"gateway"`/`"api"`）：

- **CLI**（`dojoagents` 命令，[cli/main.py](https://claude.ai/epitaxy/dojoagents/cli/main.py)）—— 纯 Python，直接调 `Runtime`。
- **Dashboard**（[dashboard/server.py](https://claude.ai/epitaxy/dojoagents/dashboard/server.py)）—— 基于 **FastAPI**（三方）搭建 Web 后端，前端是独立的 **React/TS 应用**（[dashboard/web/src](https://claude.ai/epitaxy/dojoagents/dashboard/web/src)，三方框架 React + 自研业务代码），通过 `create_embedded_runtime()`（自研的 [runtime_factory.py](https://claude.ai/epitaxy/dojoagents/dashboard/integrations/runtime_factory.py)）把 `DashboardFinancialAgentBackend`（自研适配器）注入 Runtime，实现"聊天改动会写回 dashboard 真实数据"（我们之前聊的 `resource_changes` 那条链路）。
- **Gateway / API**——同样是自研的接入壁垒，只是走不同的 channel 标识，影响 Harness 里 `channel_predicate` 类型的 prompt/policy 是否生效。

**结论：宿主应用本身是自研业务代码，只是各自借用了通用三方 Web 框架（FastAPI/React）搭壳子，核心的"怎么接进 Runtime"逻辑都是自研 adapter。**

---

# 六、Skills（程序性记忆机制）—— 自研

`SkillManager`（[skills/manager.py](https://claude.ai/epitaxy/dojoagents/skills/manager.py)）—— 纯自研，解析 Markdown + YAML frontmatter（用了三方库 `pyyaml` 做 YAML 解析，仅此而已），实现了我们前面详细聊过的"目录懒加载 + `skill_view` 按需拉取全文"机制。`SkillPromptCache` 做文件内容缓存，也是自研。

**这个机制本质上是模仿/借鉴了 Claude Skills 的"progressive disclosure"设计思路（先给目录，再按需展开全文），但代码实现是 DojoAgents 自己写的，不依赖任何 Anthropic 或第三方 skills SDK。**

---

# 七、MCP / 插件 / 多智能体 / Planning —— 自研封装 + 官方协议 SDK

- **MCP 工具接入**（`discover_and_register_mcp_tools`）—— 用了官方三方库 `mcp`（Model Context Protocol Python SDK）做协议层通信，DojoAgents 自己写了把 MCP server 发现的工具转换成内部 `ToolSpec` 的桥接代码。
- **Plugin 系统**（`dojoagents.plugins`）—— 自研，允许第三方插件贡献工具/技能目录/MCP 配置/运行时 hook。
- **Multi-agent pool / Orchestrator**（`dojoagents.multi_agent`）—— 自研的多智能体委派机制（仅存在于 legacy 路径）。
- **Planning 引擎**（`dojoagents.planning`）—— 自研的计划状态机、执行引擎。

---

# 八、财务领域相关（Harness 的一个具体实例）

`FinancialHarness`（[harnesses/built_in/financial/](https://claude.ai/epitaxy/dojoagents/harnesses/built_in/financial)）—— 全自研的场景 Harness，唯一借用的三方组件是 **`dojosdk`**（公司自己发布的一个私有 SDK 包，用于 `SDKFinancialToolBackend` 调后端金融数据服务）和 **`exchange-calendars`**（三方，判断交易日）。

---

# 总结表

|层|自研 / 三方|关键组件|
|---|---|---|
|模型对话循环|**三方**（strands-agents）|`strands.Agent`、hooks、tool-call 事件循环、流式输出|
|AgentCore（工具注册/执行/沙箱/核心工具）|**自研**|`ToolRegistry`、`ToolExecutor`、`SandboxPolicy`|
|Harness（场景能力：工具/服务/策略/prompt/presenter）|**自研**|`HarnessBuilder`、`HarnessRuntime`、`LifecycleManager`|
|Runtime（装配+生命周期外壳）|**自研**|`Runtime.compose/create/startup`|
|Session（会话持久化/记忆同步）|**自研**|`SessionService`、`MemoryManager`|
|Skills（程序性记忆懒加载）|**自研**（仅 YAML 解析用三方 `pyyaml`）|`SkillManager`、`SkillViewTool`|
|MCP 外部工具接入|**三方协议 SDK + 自研桥接**|`mcp` 包 + `discover_and_register_mcp_tools`|
|宿主应用|**自研业务代码 + 三方壳子**|FastAPI/React（dashboard）、纯 Python（CLI）|
|财务领域数据|**私有三方 SDK + 三方交易日历**|`dojosdk`、`exchange-calendars`|

**一句话总结整体架构哲学：DojoAgents 把"跟 LLM 对话的最小闭环"整个甩给了 strands 这个三方库去做，自己专注在其上层构建了一整套"场景隔离（Harness）+ 工具治理（Registry/Executor/Sandbox）+ 会话与记忆（Session/Skills）+ 多宿主接入（Host adapters）"的企业级工程框架，本身几乎不重新发明底层 LLM 交互协议。**
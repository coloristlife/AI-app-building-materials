TASK.md 是 DojoAgents 的**任务系统（Task System）** 里，每个"任务"的**人类可读的工作流说明文档**——跟 SKILL.md 长得很像（都是 Markdown），但触发方式、约束力和用途完全不同。我刚好在磁盘上找到了一个真实例子，可以对着讲：

## 1. 一个 Task 长什么样（磁盘上的目录结构）

```
dojoagents/harnesses/built_in/financial/tasks/definitions/sector-attribution/
├── TASK.md          # 给 LLM 看的自然语言工作流说明
├── contract.yaml     # 给代码看的机器可读"契约"
└── schema/
    └── market_news_raw_pack.schema.json   # 最终产出必须满足的 JSON Schema
```

Task 不是由 LLM 激活的， 但是"要不要调用某个工具" —— 起点永远是 LLM 自己的决策。

**Task 是否激活 = 外部规则决定（LLM 不参与）** 
**Task 激活之后，具体调用哪些工具、以什么参数调用、调用的顺序 = 全部由 LLM 自己决定**

补充两个精确边界，避免过度绝对化：

1. **LLM 的决策空间是被"事后约束"卡住的，不是无限自由**——`contract.yaml` 里的 `required_tools`（白名单）和 `tool_budget`（配额），通过 `ToolAuthorizerSpec.authorize()` 在 LLM 发起调用**之后**检查，超出范围就拦截打回（[legacy/tool_orchestrated.py:41-54](https://claude.ai/epitaxy/dojoagents/harnesses/built_in/financial/policies/legacy/tool_orchestrated.py:41)）。所以准确说是：**LLM 在"允许的工具集合、允许的调用次数"这个边界内自由决策，边界之外的选择会被拦截、退回给它重新决策**。
    
2. **参数基本由 LLM 提供，但可能被系统二次修正**——`ToolTransformerSpec`（比如财务 harness 的 `portfolio_repair_policy`）可以在真正执行前，对 LLM 给出的参数做修复/补全，不是 LLM 提供的每个字符都原样照搬执行。
    

**一句话总结：Task 的"要不要发生"是外部规则钉死的；Task 发生之后"具体怎么干活"（调哪个工具、传什么参数、按什么顺序）是 LLM 的自主决策空间，只是这个空间的边界（白名单+配额）被 `contract.yaml` 卡死，越界会被拦截、久拖不完会被 `evaluate_completion` 逼着继续。**
## 2. `TASK.md` 本身——这是给 LLM 读的"操作手册"

内容大致是（我读到的真实文件）：

- 角色定位（"你是一位板块异动归因分析师"）
- 必填参数（`market`、`trading_date`）
- 核心原则、禁止事项
- **明确的分步工作流**："每轮只调用 1 个工具：1. `get_market_overview` → 2. `get_sector_movers` → 3. 逐板块 `web_search`/`web_extract` → 4. `write_session_file`"
- 最终产出的字段结构说明

这部分跟 SKILL.md 的作用几乎一样——**都是软性的文字指导，靠 LLM 自己阅读理解去照做，本身没有强制力**。

## 3. `contract.yaml`——这才是让"强制力"生效的地方

```yaml
harness_profile: tool_orchestrated
required_tools: [get_market_overview, get_sector_movers, web_search, web_extract, ...]
triggers:
  commands: ["/task sector-attribution"]
constraints:
  max_tool_calls_per_turn: 1
  tool_budget:
    web_search: 30
    web_extract: 15
outputs:
  - filename: market_news_raw_pack_{market}_{trading_date}.json
    schema: schema/market_news_raw_pack.schema.json
    required: true
```

这份 YAML 被 `TaskPromptManager`（[tasks/manager.py:44-58](https://claude.ai/epitaxy/dojoagents/tasks/manager.py:44)）解析成 `TaskContract` 对象后，**直接喂给我们上一条回答里讲的那套 policy 机制**：

- `required_tools` → 变成 `allowed_tools` 白名单，喂给 `authorize()` 去硬拦截超范围调用
- `constraints.tool_budget` / `max_tool_calls_per_turn` → 直接对应 `block_tool_call()`/`repair_tool_calls()` 里的配额与节流逻辑
- `outputs[].schema` → 对应 `validate_progress()` 里校验 `write_session_file` 产出是否符合 JSON Schema，不符合就拒绝让这轮"完成"

## 4. 怎么被触发、怎么进到对话里

`triggers.commands: ["/task sector-attribution"]`——用户（或调度器/pipeline）发一条 `/task sector-attribution` 命令，`CommandRouter` 识别后创建一个 `ActiveTask` 对象，写进 `request.metadata["active_task"]`（[models.py:52-56](https://claude.ai/epitaxy/dojoagents/tasks/models.py:52) 起的 `ActiveTask`）。之后每一轮，`ToolOrchestratedHarness.matches()` 检测到 `active_task.harness_profile == "tool_orchestrated"`，就会把 `TASK.md` 的正文注入 prompt，并且**同时启用上面那套硬性 authorize/completion 策略**——这正是它跟"lazy skill"最大的不同：**Skill 是懒加载、可选、软约束；Task 一旦被激活，是强制加载、强制走完、带机器可校验契约的**。

## 5. Task vs Skill 对照表


|             | Skill (`SKILL.md`)              | Task (`TASK.md` + `contract.yaml`)                         |
| ----------- | ------------------------------- | ---------------------------------------------------------- |
| 触发方式        | LLM 自主判断是否需要 → 主动调 `skill_view` | 显式命令 `/task xxx`（或 pipeline/scheduler）激活                   |
| 是否懒加载       | 默认懒加载，仅给目录                      | 激活后正文直接注入 prompt，不懒加载                                      |
| 约束力         | 纯软性文字建议，模型可以不听                  | 附带机器可读契约：工具白名单、调用配额、输出 JSON Schema 强校验                     |
| 是否能强制不让对话结束 | 不能                              | 能——`evaluate_completion` 会一直返回 `continue/recover` 直到合法产出写出 |
| 典型用途        | "怎么做某类分析"的通用指南                  | "必须按此流程产出某个结构化文件"的可控任务                                     |

**一句话总结：TASK.md 是 Task 系统里"给 LLM 看的工作流说明"，本身是软文本；但它总是伴随一份 `contract.yaml`（机器契约）一起存在，契约里的 `required_tools`/`tool_budget`/`outputs.schema` 会被接到 Harness 的 authorize/completion 策略上，从而把 TASK.md 里描述的那串工具调用顺序变成真正有强制力的执行约束——这就是你上一个问题问的"能不能强制一连串工具调用"的现成答案：用 Task 系统而不是 Skill 系统。**



# ===
Task的 触发方式一共有 **4 种**，命令行 `/task` 只是其中一种：

## 触发方式一览（按 `preprocess()` 里的判断顺序）

**1. 结构化 metadata（最常见的程序化触发，比如 dashboard 按钮）**（[command_router.py:39-50](https://claude.ai/epitaxy/dojoagents/tasks/command_router.py:39)）

```python
pipeline_id = request.metadata.get("pipeline_id")
task_type = request.metadata.get("task_type")
```

宿主应用（比如 dashboard 前端点了个"运行任务"按钮，或调度器 `scheduler` 定时触发）直接在 `ChatRequest.metadata` 里塞 `task_type="sector-attribution"`，**根本不需要任何文字命令**，LLM 更是完全不参与这个决策。

**2. 用户（或任何调用聊天 API 的程序）打的字面斜杠命令**（[command_router.py:52-54, 59-67](https://claude.ai/epitaxy/dojoagents/tasks/command_router.py:52)）

```python
text = str(request.message or "").strip()
if text.startswith("/"):
    return self._handle_slash_command(request, text)
```

注意这里判断的是 `request.message`——也就是**这一轮进来的用户消息原文**。是用户自己在聊天框里输入 `/task sector-attribution 2026-07-03 market=us`，还没进 LLM 之前就被路由器截获处理了。

**3. 关键词自动检测（完全不需要任何命令）**（[activator.py:182-195](https://claude.ai/epitaxy/dojoagents/tasks/activator.py:182)）

```python
def try_keyword_activation(self, request):
    if not self.auto_detect:
        return None
    message = str(request.message or "").lower()
    for task_id, spec in (...):
        keywords = spec.contract.triggers.get("keywords") or []
        if any(keyword.lower() in message for keyword in keywords):
            return self.activate_task(request, task_id=task_id, params=...)
```

只要 `contract.yaml` 里给某个任务配置了 `triggers.keywords`，并且 `config.tasks.auto_detect=True`，用户随便说一句包含关键词的话（不需要任何 `/` 前缀），路由器就会自动帮它激活对应任务——**这也完全是用户消息文本的字符串匹配，不涉及 LLM 判断**。

**4. Pipeline 系统自动串联**——一个 task 完成后，`downstream` 字段（[models.py:29](https://claude.ai/epitaxy/dojoagents/tasks/models.py:29)）指定的下一个 task 会被 `PipelineRunner` 自动接续激活。

## 核心结论

**`preprocess()` 是在把请求交给 `AgentLoop`/LLM 之前就跑完的一段纯规则代码（正则匹配 `/task`、metadata 字段检查、关键词子串匹配）——LLM 从头到尾都不参与"是否激活 Task"这个决策。** LLM 唯一能感知到的是：一旦某个 Task 被这套预处理逻辑激活，`request.metadata["active_task"]` 被写入之后，**这一轮的 system prompt 才会因此变成 TASK.md 的内容，工具调用才会被套上白名单/配额约束**——对 LLM 来说，Task 已经是"既定事实"，它只是在一个被强制设定好的框架里干活，而不是自己决定要不要发起 `/task`。

**换句话说：Skill 是"LLM 主动选择要不要用"，而 Task 是"宿主应用/用户/关键词匹配代码在 LLM 介入之前就已经决定好了要不要用、用哪个"——这也正是 Task 比 Skill 约束力更强的根本原因之一：它连"是否启用"这个入口都不给 LLM 决策权。**


# ====
**激活与否是规则代码决定的（"要不要做这件事"），但"具体怎么把这件事做对"仍然只有 LLM 自己能干，而 LLM 只能靠读文字来获得这个能力——`contract.yaml` 完全无法替代这个作用。**

## `contract.yaml` 能做的和不能做的

`contract.yaml` 只是一份**边界/校验规则**：

```yaml
required_tools: [get_market_overview, get_sector_movers, web_search, web_extract, ...]
constraints: {max_tool_calls_per_turn: 1, tool_budget: {...}}
outputs: [{schema: market_news_raw_pack.schema.json}]
```

它能回答"**能不能**调用这个工具"、"**最多**能调几次"、"最终产出**必须长什么结构**"——但它**回答不了**：

- 这些工具具体**该怎么组合、按什么顺序**才能得出正确结果（比如"先锁定异动板块，再搜新闻"这个业务逻辑）
- 每个工具的参数该怎么填才对（比如"`get_market_overview` 要传 `start_date`/`end_date`，**禁止**传 `days`，否则定位不到用户指定的交易日"——这是纯业务经验，JSON Schema 描述不出来）
- 领域内的坑/例外规则（比如"单市场范围，禁止跨市场共振筛选"）
- 输出的每个字段该填什么语义内容（Schema 只能校验_格式_对不对，不能教它_内容_该怎么写）

## TASK.md 补的正是这一块——"怎么做对"的操作手册

TASK.md 里那句"你是一位板块异动归因分析师……工作流程：1. `get_market_overview` → 2. `get_sector_movers` → 3. 逐板块 `web_search`/`web_extract` → 4. `write_session_file`"——**这些具体的业务知识和推荐步骤，只能通过自然语言文本教给 LLM，没有别的传递方式**。如果只给 `contract.yaml` 的硬约束、不给 TASK.md，LLM 会陷入这种局面：

> "我知道我只能调用这 7 个工具、每种工具有调用次数上限、最后必须写出符合这个 JSON Schema 的文件……但我完全不知道该按什么顺序调、每个工具的参数该怎么填、这个任务到底想让我分析出什么。"

那样它只能靠瞪着工具的 `description`/`parameters` 和 JSON Schema 瞎试，效率极低、极容易出错——跟"有没有强制力"完全是两件事。

## 两层分工的本质

|层|解决什么问题|载体|
|---|---|---|
|**激活/约束层**（router 预处理 + `contract.yaml` + policy）|"要不要做、能不能超范围、什么时候才算完成"|规则代码，LLM 不参与|
|**执行指导层**（TASK.md 正文）|"具体怎么把这件事做对、做好"|自然语言，只能靠 LLM 读懂并执行|

**一句话：给 LLM 看 TASK.md，不是为了让它决定"要不要"做这个任务（那件事已经被规则代码定死了），而是为了让它知道"该怎么"在这个被强制圈定的范围内，把活干对——强制力管的是边界，TASK.md 管的是边界内的智能行为，两者缺一不可，替代不了对方。**

# ====
# 从用户输入到最终回复——完整流程（含 Task/policy 机制）

"policy" 在这套框架里不是一个笼统的词，而是**三种可插拔策略对象的统称**，注册时分成三类 spec（[capabilities.py]），执行时统一收进 `PolicyRegistry`（[registries/policies.py](https://claude.ai/epitaxy/dojoagents/harnesses/registries/policies.py)）：

| Policy 类型                         | 挂载点                                                            | 管什么                 |
| --------------------------------- | -------------------------------------------------------------- | ------------------- |
| **`FlowPolicySpec`**（流程策略）        | `before_turn` / `after_turn` / `evaluate_completion`           | 这一轮怎么开始、要不要结束/继续    |
| **`ToolAuthorizerSpec`**（工具授权策略）  | `authorize(call, context)`                                     | 这个工具调用**允不允许**执行    |
| **`ToolTransformerSpec`**（工具转换策略） | `transform(call, context)` / `transform_calls(calls, context)` | 执行前要不要**改写/修复**这个调用 |

同一个策略对象可以**同时**以多种身份注册——比如财务 harness 里的 `ToolOrchestratedTaskPolicy`（对应 Task 系统）既注册成 `FlowPolicySpec`（提供 `evaluate_completion`）又注册成 `ToolAuthorizerSpec`（提供 `authorize`）（[harness.py:266](https://claude.ai/epitaxy/dojoagents/harnesses/built_in/financial/harness.py:266) 和 [harness.py:291](https://claude.ai/epitaxy/dojoagents/harnesses/built_in/financial/harness.py:291)）。

---

## 完整流程（把之前讨论的所有部分串起来）

**1. 用户输入到达 → `CommandRouter.preprocess(request)`** 在 LLM 被调用**之前**，纯规则代码检查 `request.metadata`/`request.message`，判断是否要激活某个 Task（`/task` 命令、metadata 里的 `task_type`、关键词自动检测）。命中则调用 `TaskActivator.activate_task()`，把 `contract.yaml` 解析出来的 `TaskContract`（`required_tools`、`constraints`、`outputs.schema`）封装成 `ActiveTask`，写进 `request.metadata["active_task"]`。

**2. `AgentLoop` 接手这一轮 → `harness_runtime.before_turn(context)`** 内部依次做：

- `request_context_codecs` 解析请求上下文
- `policies.before_turn(context)` —— 依次跑所有 **FlowPolicySpec** 的 `before_turn` 钩子（比如 `turn_scope_policy`）
- `prompts.compose(context, ...)` —— 依次跑所有 `PromptContributorSpec`（按 phase 排序拼系统提示词）：
    - `financial.instructions`（固定的角色说明）
    - **`financial.task-context`** —— **这里就是 `TASK.md` 正文真正被注入 system prompt 的地方**：如果第 1 步激活了某个 Task，这个 phase 会把对应任务的 `TASK.md` 正文塞进 prompt
    - 此外 `AgentLoop` 单独再调一次 `skill_manager.prompt_block()`，把 skill 目录也插进去（[loop.py:852](https://claude.ai/epitaxy/dojoagents/agent/loop.py:852)）

**3. 收集工具目录 → 交给底层 `strands.Agent`** `_collect_tool_specs()` 取出当前 `ToolRegistry` 里**全部**工具的 schema（[loop.py:1131](https://claude.ai/epitaxy/dojoagents/agent/loop.py:1131)）——**注意：即使有 Task 激活并限制了 `required_tools` 白名单，这一步展示给 LLM 的工具目录并不会因此被过滤缩减**，LLM 依然能"看到"全部工具，白名单是在下面第 5 步的调用阶段才生效拦截，不是在"能看到什么"阶段过滤。

**4. LLM 生成回复/工具调用** `strands.Agent` 驱动真正的模型交互循环，模型基于 system prompt（含 TASK.md/skill 目录）+ messages + tools 决定是直接回复还是发出若干 `ToolCall`。

**5. 工具调用先被"改写"，再被"授权"**

- **`transform_calls`**（**`ToolTransformerSpec`**）：先跑所有 transformer（比如 `portfolio_repair_policy`），可能修正/重写参数，然后统一调用 `revalidate(call)` 做基础校验（必填参数、sandbox 权限）
- **`authorize`**（**`ToolAuthorizerSpec`**）：先跑 core 安全检查，再依次跑所有 harness 注册的授权策略——**如果有 Task 激活**，`ToolOrchestratedTaskPolicy.authorize()` 在这里检查该调用是否在 `contract.yaml` 的 `required_tools` 白名单内、是否超出 `tool_budget`，一旦不合规直接返回 `block`/`halt`，整条决策链短路（[policies.py:63-98](https://claude.ai/epitaxy/dojoagents/harnesses/registries/policies.py:63)）

**6. 通过授权的调用真正执行** `ToolExecutor.execute_one(call)` 调用 `ToolSpec.handler`，得到 `ToolResult`（这一步就是我们之前反复讲的，财务工具的 handler 会调到 `DashboardFinancialAgentBackend.execute()` 之类的真实业务逻辑）。

**7. 结果呈现** `present_results()` 跑 `ResultPresenterSpec`，把原始 JSON 转成给用户看的友好文本；大结果会走 artifact adapter 存成指针。工具结果连同呈现文本被追加进对话历史。

**8. 判断这一轮该不该结束——`evaluate_completion`** 依次跑所有 **FlowPolicySpec** 的 `evaluate_completion`（[policies.py:100-137](https://claude.ai/epitaxy/dojoagents/harnesses/registries/policies.py:100)）：

- **如果没有 Task 激活**：走普通的完成判定（比如 `financial.completion` 那个默认策略）
- **如果有 Task 激活**：`ToolOrchestratedTaskPolicy.evaluate_completion()` 检查 `write_session_file` 产出的文件是否符合 `contract.yaml` 里 `outputs[].schema` 指定的 JSON Schema——**没通过就返回 `"recover"`**，附带 `recovery_prompt`（比如"任务目标尚未完成，不允许结束"），这个 prompt 会作为新一轮的引导消息注入，逼 `AgentLoop` 继续跑，回到第 3 步重新收集工具、再让 LLM 继续干活，直到产出合法为止。

**9. 循环直到 `evaluate_completion` 返回 `"complete"`（或达到 `max_recovery_turns` 硬上限）** 最终把完整回复（连同可能的 `resource_changes`，比如财务工具真的改写了 dashboard 的持仓数据）一起返回给宿主应用（dashboard/CLI）。

---

## 一图串联三条主线

```
用户输入
  → CommandRouter.preprocess()          【决定是否激活 Task，读 contract.yaml】
  → harness_runtime.before_turn()
      → FlowPolicy.before_turn hooks
      → prompts.compose()                【TASK.md 正文 + skill 目录 一起拼进 system prompt】
  → strands.Agent 跑模型交互循环          【LLM 基于 prompt 决定要不要调工具】
  → harness_runtime.transform_calls()    【ToolTransformerSpec 改写/修复调用】
  → harness_runtime.authorize()          【ToolAuthorizerSpec 校验 contract.yaml 的白名单/配额，命中就 block】
  → ToolExecutor.execute_one()           【真正执行工具 handler】
  → harness_runtime.present_results()    【呈现结果】
  → harness_runtime.evaluate_completion()【FlowPolicySpec 判断是否达标，没达标就 recover 重新循环】
  → 结束，返回给用户/宿主应用
```

**一句话总结：Task 是否启用由用户输入前的规则代码决定；`TASK.md` 在 `before_turn` 阶段被拼进 prompt 教 LLM"怎么做"；`contract.yaml` 的约束通过三类 policy（authorizer 拦截非法调用、transformer 修复调用、flow policy 判断是否该强制继续）在每次工具调用前后被强制执行——三条线在 `HarnessRuntime` 这一个门面对象里被统一调度，贯穿一整轮对话的生命周期。**

# ===
`contract.yaml`（通过 authorizer）管的是"**已经被 LLM 选择要调用的工具，允不允许放行**"，而不是"**主动强制某个工具一定要被调用**"。这是"事后拦截"跟"事前指挥"的本质区别，值得说清楚：

## 1. "要不要调用某个工具" —— 起点永远是 LLM 自己的决策

系统**不会**代替 LLM 生成一个 `ToolCall`。无论 `TASK.md`/`contract.yaml` 写得多详细，如果 LLM 这一轮压根没打算调用 `get_market_overview`，系统里没有任何机制会"帮它调用"或者"逼它必须现在调用"——**发起调用的决策权，100% 在 LLM 手里**。

## 2. "是否被允许执行" —— 这才是 `contract.yaml`/authorizer 说了算的部分

一旦 LLM **自己决定**发出某个 `ToolCall`，`ToolOrchestratedTaskPolicy.authorize()` 才会介入检查：

- 这个工具在不在 `required_tools` 白名单里
- 这个工具的调用次数是否超过 `tool_budget`

超了就返回 `block`，这条调用不会被执行，LLM 会收到一条错误消息（比如 "Tool budget exceeded"），下一轮它得根据这个反馈重新决策。**所以这是一个"事后拦截/否决权"，不是"事前指派任务"。**

## 3. 那"强制走完整个流程"的感觉从哪来？—— 是靠 `evaluate_completion` 的"拒绝收尾"

真正让 Task 显得"强制"的，不是"逼 LLM 调用具体某个工具"，而是 `evaluate_completion()` 在每轮结束时检查产出是否合规——**不合规就返回 `"recover"`，拒绝让这一轮真正结束**，并把 `recovery_prompt`（一段文字，比如"任务目标尚未完成，不允许结束……"）重新塞进对话，逼着 `AgentLoop` 继续循环。**但这仍然只是"文字劝导+不让停"，下一轮具体调哪个工具，还是 LLM 自己决定**——只是因为它反复被拒绝、反复被提示，大概率会"识趣地"按 `TASK.md` 说的步骤走下去。

## 4. 输入参数——基本对，但有一个例外（`ToolTransformerSpec`）

**绝大多数情况下**，工具调用的参数（比如 `market`、`start_date`、`end_date`）确实是 LLM 自己根据 `TASK.md` 的说明和工具的 `parameters` schema 填出来的。

但有一个例外：**`transform_calls`**（**`ToolTransformerSpec`**）这一步（在 authorize 之前执行）可以**自动修改/修复 LLM 提供的参数**——比如财务 harness 里的 `PortfolioToolRepairPolicy`/`SectorSessionPolicy`，可以在 LLM 提交调用之后、真正执行之前，悄悄纠正或补全某些参数（比如自动补上 session 里已知的 `market`，或修正一个格式错误的日期）。所以严格说：**参数主要由 LLM 提供，但系统保留了"在执行前二次加工/修正"这个参数的能力，不是 100% 原样照搬 LLM 给的输入。**

## 修正后的完整表述

> 整个过程里，**"要不要调用工具、调用哪个工具"这个决策永远由 LLM 自己做出**；`contract.yaml`（通过 `ToolAuthorizerSpec`）不主动指派工具调用，只是在 LLM 已经发起调用之后，**事后判断这次调用是否允许放行**（白名单+配额），不允许就拦截打回；系统整体的"强制感"来自 `evaluate_completion` 反复拒绝收尾、逼 LLM 继续尝试，而不是直接代替 LLM 去调工具；调用参数**主要**由 LLM 提供，但 `ToolTransformerSpec` 可以在执行前对参数做二次修正/修复。

# ===
**`triggers.commands`/`triggers.keywords` 里配置的东西，是给"外部输入"用的，LLM 自己没有任何编程接口能触发这个命令。** 有代码证据可以直接确认：

## 1. `preprocess()` 只在"一次外部请求"进来时跑一次，而且在 LLM 循环开始**之前**

[runtime_helpers.py:65-93](https://claude.ai/epitaxy/dojoagents/tasks/runtime_helpers.py:65) `run_agent_with_tasks()`：

```python
current = router.preprocess(request)     # ← 只在这里跑一次，处理的是外部传进来的 request
...
last_response = await _invoke_run_agent(run_agent, current, ...)   # ← 然后才进入 LLM 驱动的那一整轮（可能包含多次工具调用循环）
```

`request` 是**宿主应用（dashboard/CLI/API）传进来的这一次外部调用**，`router.preprocess()` 检查的是这个 `request.message`/`request.metadata` 的原始文本或字段。**这一步跑完之后，接下来无论 LLM 在这一轮里调用多少次工具、反复循环多少轮（`evaluate_completion` 的 recover 循环），`preprocess()` 都不会再被重新调用**——也就是说，Task 的激活判断只发生在"这一轮对话的最开始"，LLM 在这一轮里后续的任何行为都没有机会再触发它。

## 2. 没有任何一个暴露给 LLM 的工具叫"激活任务"

我specifically 搜过整个代码库，**没有任何 `ToolSpec` 是"让 LLM 主动激活某个 Task"的**（不像 `skill_view` 有专门的工具给 LLM 调用去加载 skill）。LLM 手里能拿到的工具只有普通的业务工具（财务工具、终端、代码执行……），里面**没有一个叫 `activate_task` 或类似的东西**。

## 3. LLM 即使在回复文字里写"/task sector-attribution"，也不会被系统当命令执行

`/task` 只有在**外部调用者发来的 `ChatRequest.message` 原文以 `/` 开头**时才会被 `_handle_slash_command()` 解析（[command_router.py:52-54](https://claude.ai/epitaxy/dojoagents/tasks/command_router.py:52)）。LLM 的输出是**这一轮对话的回复内容**，不是"下一次外部请求的 `request.message`"——除非宿主应用有意把 LLM 说的这句话原样回灌成下一次请求发进来（这是宿主应用自己要不要做的设计选择，DojoAgents 框架本身完全没有这种"自动回灌"的胶水代码）。

## 4. 唯一"看起来像自动串联"的例外——Pipeline，但那也不是 LLM 决定的

`PipelineRunner.maybe_advance()`（[runtime_helpers.py:96](https://claude.ai/epitaxy/dojoagents/tasks/runtime_helpers.py:96)）确实会在一个 Task 完成后**自动**构造下一个 Task 的请求继续执行——但这是**规则代码**（读 `contract.yaml` 的 `downstream` 字段）驱动的确定性串联，跟 LLM 的意愿完全无关，LLM 全程不参与这个决策。

## 一句话总结

**`triggers.commands`/`keywords` 是给"外部调用者"（用户输入、dashboard 按钮、调度器、pipeline）用的入口，`CommandRouter.preprocess()` 只在 LLM 循环开始前对外部传入的原始请求做一次性判断；LLM 自身既没有专属工具、也没有任何机制能在对话过程中"申请"或"要求"触发一次 `/task` 命令——Task 的激活权完全被隔离在 LLM 的决策范围之外。**


# ===

## 两个独立的决策点

|决策点|谁来决定|什么时候发生|
|---|---|---|
|**① 这一轮对话要不要激活某个 Task**|**外部规则代码**（`CommandRouter.preprocess()`）——用户输入的命令/关键词、宿主应用传的 metadata、Pipeline 的自动串联|在 LLM 循环**开始之前**，一次性判断，LLM 全程不参与|
|**② 在当前这一轮（无论是否有 Task 激活）里，要不要调用某个具体工具、调哪个、传什么参数**|**LLM 自己**|在 LLM 循环**进行过程中**，每次工具调用之前|

我上一条回答讲的"是否调用工具是 LLM 决定的，`contract.yaml` 只是事后拦截"，说的是**②**这个决策点；你问的"`/task` 命令是不是人为输入、LLM 能不能触发"，说的是**①**这个决策点。**这是流程里前后相继、职责完全分开的两件事**：

```
① 先由外部规则决定：这一轮要不要套上某个 Task 的紧箍咒（LLM 无权参与）
        ↓（如果套上了）
② 然后由 LLM 在这个紧箍咒范围内，自己决定调不调工具、调哪个、传什么参数
        ↓
   contract.yaml 的白名单/配额（通过 authorizer）只在②发生之后做事后拦截
   evaluate_completion 的 recover 循环只在②的结果不达标时逼着继续做②
```

## 为什么这不矛盾

- ① 回答的是"**这局游戏的规则是谁定的**"——答案：外部规则代码，LLM 没有投票权。
- ② 回答的是"**在这局游戏规则之内，每一步棋怎么走**"——答案：LLM 自己走，只是走出界（超白名单/超配额）会被判"无效手"打回，走得不够完整会被"不准中途下桌"逼着继续走。

**这两条结论叠在一起，恰好构成一个完整、无矛盾的图景：Task 是否存在、约束是什么——由外部规则一次性定好；在这个既定约束下具体怎么行动——完全是 LLM 的自主决策空间，只是这个空间的边界被卡得很死。** 所以不需要改动之前的任何措辞，只是要意识到这两句话回答的是流程里不同的两层问题，不是同一层的两种说法在打架。
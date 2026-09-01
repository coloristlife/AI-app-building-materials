这里的 **Strands** 指的是 **Amazon Strands Agents**，它是 AWS 开源的一个 **Agent SDK / Agent framework**。DojoAgents 在你刚才看到的代码里，把 Strands 当成了自己的 **Agent Loop 执行层/模型调用层的一部分**。

简单理解：

> **DojoAgents 在上层定义自己的 Agent、Harness、Tool Registry；Strands 帮它把这些东西组织成一个可以运行的 Agent，并负责和 LLM 进行 tool-calling loop。**

### 1. Strands 在 DojoAgents 里面处于什么位置？

你刚才看到的代码：

```text
DojoAgents
   │
   ├── Harness
   ├── Tool Registry
   ├── Tool Executor
   └── AgentLoop
          │
          ▼
      Strands Agent
          │
          ▼
    LLM Provider
          │
          ▼
      LLM Model
```

所以 **Strands 不是 LLM**。

它也不是 Tool Registry。

它更像一个：

> **“帮你运行 Agent 的框架/运行时”**

---

### 2. 为什么 DojoAgents 要用 Strands？

假设不用 Strands，你自己实现 Agent Loop，大概要处理：

```text
发送 prompt
    ↓
LLM
    ↓
LLM 返回 tool_call
    ↓
找到 tool
    ↓
执行 tool
    ↓
把 tool result 放回 conversation
    ↓
再次调用 LLM
    ↓
LLM 再决定是否调用 tool
    ↓
...
```

这就是典型的：

```text
LLM
 ↕
Tool
 ↕
LLM
 ↕
Tool
 ↕
LLM
```

Strands 帮你处理了这一套 **Agent orchestration / tool-calling loop**。

所以 DojoAgents 不需要完全从零实现这一层。

---

### 3. Strands 最重要的几个东西

你在 DojoAgents 源码里最可能看到：

```python
from strands import Agent
```

然后：

```python
agent = Agent(
    model=model,
    tools=strands_tools,
    system_prompt=system,
)
```

这里的 `Agent` 就是 Strands 的 Agent。

而：

```python
tools=strands_tools
```

就是我们刚才讨论的关键。

DojoAgents 把自己的：

```text
ToolSpec
   ↓
DojoBridgedTool
```

转换成 Strands 能理解的 Tool，然后交给：

```text
Strands Agent
```

---

### 4. Strands 和 LLM Provider 的关系

这点也非常容易混淆。

它们是不同层次：

```text
                 Strands
              Agent Framework
                    │
                    ▼
             Model interface
                    │
       ┌────────────┼────────────┐
       ▼            ▼            ▼
    OpenAI       Anthropic     Gemini
       │            │            │
       ▼            ▼            ▼
      GPT          Claude       Gemini
```

Strands 可以支持不同的 model/provider。

所以：

> **Strands Agent ≠ OpenAI Agent ≠ GPT model**

它是中间的 Agent orchestration layer。

---

### 5. 放回 DojoAgents，你可以这样理解

DojoAgents 自己负责：

```text
Harness
  ↓
Tool Registry
  ↓
ToolSpec
  ↓
Tool Executor
```

然后它把 Tool 包装成：

```text
DojoBridgedTool
```

交给：

```text
Strands Agent
```

Strands 再负责：

```text
Agent
  ↓
LLM
  ↓
tool call?
  ├── No → final answer
  │
  └── Yes
        ↓
      Tool
        ↓
      Result
        ↓
      LLM again
```

所以你现在看到的 DojoAgents 架构可以概括成：

> **DojoAgents = 自己的 Agent/Harness/Tool infrastructure + Strands 提供的 Agent execution/orchestration。**

这也是为什么你刚才看到：

```python
Agent(
    model=model,
    tools=strands_tools,
)
```

会感觉“怎么 DojoAgents 突然出现了一个 Strands Agent”。

**因为 DojoAgents 的 AgentLoop 在这里把自己的 Tool 和 Model 接到了 Strands 的 Agent abstraction 上。**

如果你接下来是在研究 **DojoAgents 的 Harness 到底控制什么、Strands Agent 到底控制什么**，这个边界非常重要：**Harness 不是 Strands 的 Harness；DojoAgents 的 Harness 是上层场景/能力配置，而 Strands Agent 更接近底层 Agent execution engine。**


## Excluded Tools


**DojoAgents 里哪些 Registry tools 不会被放进 `strands_tools`，从而不会提供给 LLM**，目前源码里，**明确存在的 block 机制主要是 image turn exclusion**。

核心代码是：

```python
excluded_tools = IMAGE_TURN_EXCLUDED_TOOLS if image_turn else frozenset()

for spec in self.tool_executor.registry.all():
    if spec.name in excluded_tools:
        continue

    strands_tools.append(
        DojoBridgedTool(spec, ...)
    )
```

也就是说：

```text
Registry
   │
   ├── Tool A ───────────────→ strands_tools → LLM
   ├── Tool B ───────────────→ strands_tools → LLM
   ├── Tool C ──┐
   │             │
   │       excluded_tools
   │             │
   │             ✕
   │
   └── Tool D ───────────────→ strands_tools → LLM
```

### 关键是 `IMAGE_TURN_EXCLUDED_TOOLS`

它是一个专门针对 **image turn** 的 exclusion set。

也就是说，当当前 turn 涉及 image：

```python
image_turn = True
```

那么：

```python
excluded_tools = IMAGE_TURN_EXCLUDED_TOOLS
```

Registry 中名字在这个 set 里的 tool 就会被跳过。

如果不是 image turn：

```python
image_turn = False
```

那么：

```python
excluded_tools = frozenset()
```

也就是**没有这个过滤**。

---

### 所以目前不要理解成有一个“大型 Tool Permission Filter”

更准确是：

|情况|Registry tool 是否进入 `strands_tools`|
|---|---|
|普通 turn|**基本全部进入**|
|Image turn + tool 在 `IMAGE_TURN_EXCLUDED_TOOLS`|❌ 不进入|
|Image turn + tool 不在 exclusion set|✅ 进入|
|Tool 根本没注册到 Registry|❌ 不进入|

因此，目前看到的机制并不是：

```text
Tool Registry
      ↓
Security Policy
      ↓
Capability Filter
      ↓
Relevant Tool Selection
      ↓
LLM
```

而更接近：

```text
Tool Registry
      ↓
registry.all()
      ↓
特殊场景 exclusion
      ↓
DojoBridgedTool
      ↓
strands_tools
      ↓
LLM
```

**不过，如果你想知道“具体哪些 tool name 被 `IMAGE_TURN_EXCLUDED_TOOLS` block”，我需要再把这个常量的定义位置追出来。**这会直接告诉我们例如 `shell`、`filesystem`、`python`、`skill_view` 之类到底有没有被排除。

## Add Tools
通过register_dashboard_portfolio_tools  register tools to 
DashboardFinancialAgentBackend.registry
```
for spec in tool_specs:

	tool_registry.register(spec)
```
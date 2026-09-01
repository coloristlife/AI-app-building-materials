# Part 1

**`FINANCIAL_SERVICE_ID` 这个 service 的使用时机，按时间顺序分为 4 个阶段：**

**1. `Runtime.startup()` → `LifecycleManager.startup()`**（[lifecycle.py:72](https://claude.ai/epitaxy/dojoagents/harnesses/lifecycle.py:72)） 对每个声明的 `ServiceSpec`（包括 `FINANCIAL_SERVICE_ID`），先检查 `self._bindings.get(spec.component_id)`。因为 `create_embedded_runtime` 传入了 `service_bindings={FINANCIAL_SERVICE_ID: ExternalServiceBinding(backend, ...)}`，所以能找到这个绑定——于是不会调用财务 harness 默认的工厂方法（`self.tool_backend`，见 [harness.py:327](https://claude.ai/epitaxy/dojoagents/harnesses/built_in/financial/harness.py:327)），而是直接使用 `binding.instance`，也就是你的 `DashboardFinancialAgentBackend`。因为 `owns_lifecycle = binding.runtime_owns_lifecycle = False`，所以 `Runtime` **不会**去调用它的 `.startup()`/`.shutdown()`——生命周期仍归 dashboard 的 `app_services` 所有。解析结果存入 `services[FINANCIAL_SERVICE_ID]`。

**2. `Runtime.startup()` → `self.harness.startup(self.harness_runtime_context)`**（[harness.py:340](https://claude.ai/epitaxy/dojoagents/harnesses/built_in/financial/harness.py:340)） 财务 harness 读取 `context.services.get(FINANCIAL_SERVICE_ID)`，检查它非空且具有 `supported_tools` 属性——这是一次健全性检查，确认 backend 已正确接入。

**3. `Runtime._build_harness_agent()`**（[runtime.py:298-312](https://claude.ai/epitaxy/dojoagents/agent/runtime.py:298)） 对每个 provider_spec，如果它的 `provider` 是可调用对象，就会用 `self.harness_runtime_context` 去调用它。三个财务工具 provider（`financial.tools.domain/portfolio/sdk`）的 provider 是这样一个 lambda：`lambda runtime, factory=provider: factory(runtime.services[FINANCIAL_SERVICE_ID])`（[harness.py:245](https://claude.ai/epitaxy/dojoagents/harnesses/built_in/financial/harness.py:245)）——这里的 `runtime` 参数实际上就是 `HarnessRuntimeContext`，所以 `runtime.services[FINANCIAL_SERVICE_ID]` 取出你的 backend，并传给 `get_domain_tool_specs(backend)` / `get_portfolio_tool_specs(backend)` / `get_sdk_tool_specs(backend)`，用来生成一批 `ToolSpec`，这些 `ToolSpec` 的 handler 闭包内部持有对 `backend` 的引用。

**4. 之后每一次实际的工具调用** 在会话过程中，当 LLM 调用某个财务工具（domain/portfolio/SDK 类）时，第 3 步创建的 `ToolSpec.handler` 闭包会调用 `backend.execute(tool_name, arguments, principal=..., session_id=...)`——这是正常运行时的、持续性的使用路径，只要这个 `Runtime` 存活，每次财务工具调用都会走这条路。

**总结：** `FINANCIAL_SERVICE_ID` 在启动阶段被使用一次（服务解析 + harness 启动校验 + 构建 ToolSpec），之后在**每次**财务工具被实际调用时都会被反复用到（每次都路由到绑定的 `backend`）。


# part2 

**1. [dojoagents/tools/executor.py:70](https://claude.ai/epitaxy/dojoagents/tools/executor.py:70)** — `ToolExecutor.execute_one()` 当用户在界面聊天、LLM 决定调用某个工具（比如 `get_ticker_realtime_quote`）时，`AgentLoop` 会把这个 `ToolCall` 交给 `ToolExecutor`，执行：

```python
spec = self.registry.get(call.name)   # 从 Runtime 的 ToolRegistry 里取出 ToolSpec
raw = await spec.handler(dict(call.arguments))   # 调用 handler
```

这里的 `spec.handler` 就是第 3 步中被构建出来的那个闭包函数。

**2. [dojoagents/harnesses/built_in/financial/tools/backend_delegation.py:26-35](https://claude.ai/epitaxy/dojoagents/harnesses/built_in/financial/tools/backend_delegation.py:26)** — 真正的 handler 实现

```python
async def execute(arguments, *, tool_name=name):
    principal = active_session_principal.get()
    ...
    return await backend.execute(
        tool_name, arguments,
        principal=principal,
        session_id=active_session_id.get(),
    )
```

这个 `backend` 就是通过 `FINANCIAL_SERVICE_ID` 解析出来、闭包捕获的 `DashboardFinancialAgentBackend` 实例。

**3. [dojoagents/dashboard/integrations/financial_agent_backend.py:51](https://claude.ai/epitaxy/dojoagents/dashboard/integrations/financial_agent_backend.py:51)** — `DashboardFinancialAgentBackend.execute()` 最终调用 `spec.handler(dict(arguments))`（这里的 `spec` 是它内部私有 `ToolRegistry` 里的 `ToolSpec`），真正执行 dashboard 侧的领域/组合/SDK 工具逻辑，返回结果。

**所以完整链路是：**

```
用户聊天 → LLM 决定调用财务工具
  → AgentLoop 产生 ToolCall
  → ToolExecutor.execute_one()（executor.py:70）
  → registry 里该工具的 handler（backend_delegation.py:26，闭包持有 backend）
  → backend.execute()（financial_agent_backend.py:51，backend 就是 FINANCIAL_SERVICE_ID 对应的实例）
  → 真正的领域/组合/SDK 工具处理函数
  → 结果一路返回给 ToolExecutor → AgentLoop → 展示给用户
```

一句话总结：**`FINANCIAL_SERVICE_ID` 本身在会话过程中不会被“查找”，它在启动阶段已经被解析并固化进了每个财务 `ToolSpec` 的 handler 闭包里；用户每次在聊天里触发一次财务工具调用，实际上都是在调用这个闭包，从而间接调用到当初绑定的 `DashboardFinancialAgentBackend.execute()`。**

# part 3


**`ToolRegistry` 同时承担了「告诉 LLM 有什么工具」和「知道调用时该执行谁」这两件事**，而 `required_services` 只是构建阶段的一个"装配说明"，运行时调用完全不会再用到它。

**1. `ToolSpec` 本身就是"名字 + 说明 + 可执行函数"的绑定体**（[registry.py:9-21](https://claude.ai/epitaxy/dojoagents/tools/registry.py:9)）：

```python
class ToolSpec:
    name: str
    description: str
    parameters: dict
    handler: Callable[...]   # 真正会被调用的函数，就绑在这个对象里

    def schema(self):        # 给 LLM 看的部分：name/description/parameters
        return {"name": ..., "description": ..., "parameters": ...}
```

- `schema()` 部分（name/description/parameters）→ 拼进 prompt 给 LLM 看，让它知道"有什么工具、怎么传参"。
- `handler` 部分 → 是一个已经闭包好的可执行 async 函数，跟 schema 存在**同一个对象**里。

**2. 调用时，`ToolExecutor` 是直接从 registry 里取出这个已经绑好 handler 的 `ToolSpec` 来执行**（[executor.py:54-70](https://claude.ai/epitaxy/dojoagents/tools/executor.py:54)）：

```python
spec = self.registry.get(call.name)
raw = await spec.handler(dict(call.arguments))
```

这里**不涉及** `required_services`——它只是在拿 `spec.handler`，而这个 handler 早在构建阶段就已经把 `backend`（也就是 `FINANCIAL_SERVICE_ID` 对应的实例）通过闭包捕获好了。

**3. `required_services` 只在"构建 capabilities / 组装 ToolSpec"这一次性阶段起作用**（[harness.py:244-245](https://claude.ai/epitaxy/dojoagents/harnesses/built_in/financial/harness.py:244)）：

```python
ToolProviderSpec(
    ...,
    required_services=(FINANCIAL_SERVICE_ID,),
    provider=lambda runtime, factory=provider: factory(runtime.services[FINANCIAL_SERVICE_ID]),
)
```

它的作用只是：**告诉框架"这个 provider 在被调用之前，必须先把 FINANCIAL_SERVICE_ID 这个服务准备好"**，然后在构建时把 `runtime.services[FINANCIAL_SERVICE_ID]`（即 backend）作为参数传给 `get_domain_tool_specs(backend)`，由它生成一批已经把 `backend` 闭包进 handler 里的 `ToolSpec`。这个过程只发生**一次**（`Runtime._build_harness_agent()` 期间），生成结果之后就注册进 `ToolRegistry` 了。

**所以正确的说法是：**

|阶段|谁在起作用|作用|
|---|---|---|
|构建期（一次性）|`required_services` + provider factory|把该用哪个 backend 服务"焊接"进 `ToolSpec.handler` 闭包里|
|会话期（每次 LLM 决定调用工具）|`ToolRegistry` + `ToolSpec.schema()`|告诉 LLM 有哪些工具、参数是什么|
|会话期（LLM 真正调用某工具）|`ToolRegistry` + `ToolSpec.handler`|直接执行早就焊好的那个 handler，间接调到 backend|

一句话：**`required_services` 决定"焊接时用谁"，`ToolRegistry`/`ToolSpec` 既负责"给 LLM 看什么"，也负责"调用时执行什么"——handler 已经把该用的服务实例封进去了，调用阶段不再需要 `required_services` 参与。**
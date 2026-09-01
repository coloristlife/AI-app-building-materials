

## `capabilities` 在哪里初始化

**入口：`Runtime.create()` → `Runtime.compose()` → `RuntimeComposer.compose()`**（[composer.py:30-130](https://claude.ai/epitaxy/dojoagents/harnesses/composer.py:30)），这是一个**同步、无副作用**的组装步骤（还没启动任何服务，只是拼装一张不可变的"能力图"）：

1. `HarnessLoader().load(config.harness, context=build_context)` — 根据 `config.harness`（agents.yaml 里配置的 harness id，比如 `"financial"`）从 `_BUILT_IN_ALIASES` 映射表（[loader.py:16-17](https://claude.ai/epitaxy/dojoagents/harnesses/loader.py:16)）解析出工厂路径 `"dojoagents.harnesses.built_in.financial:create_harness"`，动态 import 并实例化 → 得到 `FinancialHarness` 实例（[harness.py:83](https://claude.ai/epitaxy/dojoagents/harnesses/built_in/financial/harness.py:83)）。
    
2. `builder = HarnessBuilder(harness.descriptor)` — 创建一个空的构建器。
    
3. **关键一步：`harness.configure(builder, build_context)`**（[composer.py:53](https://claude.ai/epitaxy/dojoagents/harnesses/composer.py:53)） `FinancialHarness.configure()`（[harness.py:147](https://claude.ai/epitaxy/dojoagents/harnesses/built_in/financial/harness.py:147)）会调用：
    
    ```python
    def configure(self, builder, context) -> None:
        self.configure_core_capabilities(builder, context)         # prompt/skill/memory/state 等
        self.configure_operational_capabilities(builder, context)  # 工具/服务/policy/presenter 等
    ```
    
4. `configure_operational_capabilities`（[harness.py:206](https://claude.ai/epitaxy/dojoagents/harnesses/built_in/financial/harness.py:206)起）里就是**三个财务工具 provider 被 include 的地方**（[harness.py:235-248](https://claude.ai/epitaxy/dojoagents/harnesses/built_in/financial/harness.py:235)）：
    
    ```python
    for component_id, names, provider in (
        ("financial.tools.domain",    DOMAIN_TOOL_NAMES,    get_domain_tool_specs),
        ("financial.tools.portfolio", PORTFOLIO_TOOL_NAMES, get_portfolio_tool_specs),
        ("financial.tools.sdk",       SDK_TOOL_NAMES,       get_sdk_tool_specs),
    ):
        builder.add_tool_provider(
            ToolProviderSpec(
                component_id, source,
                required_services=(FINANCIAL_SERVICE_ID,),
                provider=lambda runtime, factory=provider: factory(runtime.services[FINANCIAL_SERVICE_ID]),
                tool_names=names,
            )
        )
    ```
    
    这里只是把这三个 provider 的**规格（spec）**——"我叫什么、依赖哪个 service、怎么构建 ToolSpec"——注册进 `builder`，此时**并没有真正调用 `get_domain_tool_specs` 等函数**，`provider` 还只是一个待执行的 lambda。
    
5. `composer.py` 还会额外把插件工具（`plugin_snapshot.tools`）、MCP source（插件 + `config.mcp_servers`）、`extra_tool_dirs` 里的工具也通过 `builder.add_tool_provider`/`add_mcp_source` 加进同一个 builder。
    
6. `capabilities = builder.build()`（[composer.py:110](https://claude.ai/epitaxy/dojoagents/harnesses/composer.py:110)）— 把 builder 里收集的所有 spec（tools/services/memories/skills/prompt contributors/flow policies/...）冻结成一个不可变对象，赋给 `Runtime(capabilities=capabilities, ..., state="composed")`。**这就是 `self.capabilities` 被赋值的地方。**
    

## 三个财务工具 provider 真正"生效"（被调用）在哪里

到 `compose()` 这一步为止，三个 provider 只是**声明**，还没执行。真正被执行是在后续 `Runtime.startup()` → `_build_harness_agent()` 里（[runtime.py:298-312](https://claude.ai/epitaxy/dojoagents/agent/runtime.py:298)）：

```python
registry = ToolRegistry()
for provider_spec in self.capabilities.tools:      # 遍历刚才冻结进 capabilities 的 provider spec
    provided = provider_spec.provider              # 取出那个 lambda
    if callable(provided):
        provided = provided(self.harness_runtime_context)   # 调用它！传入 HarnessRuntimeContext
        ...
    for tool in tuple(provided or ()):
        registry.register(tool)
```

调用 `provided(self.harness_runtime_context)` 时，lambda 内部执行 `factory(runtime.services[FINANCIAL_SERVICE_ID])`，即 `get_domain_tool_specs(backend)` 等，这时才真正生成带 handler 闭包的 `ToolSpec` 列表并注册进 `registry`。而 `runtime.services[FINANCIAL_SERVICE_ID]` 能取到值，前提是 `LifecycleManager.startup()`（在 `_build_harness_agent()` 之前执行）已经把 `FINANCIAL_SERVICE_ID` 解析好放进了 `HarnessRuntimeContext.services`——这正是我们之前讨论过的部分。

**整体顺序：** `compose()`（声明三个 provider spec，写入 `capabilities.tools`）→ `startup()` 里先解析 `FINANCIAL_SERVICE_ID` service → 再 `_build_harness_agent()` 遍历 `capabilities.tools` 逐一调用 provider，生成真正的 `ToolSpec` 并注册进 `Runtime` 的 `ToolRegistry`。
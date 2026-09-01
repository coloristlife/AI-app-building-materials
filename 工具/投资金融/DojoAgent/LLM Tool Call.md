
**发给 LLM 供选择的工具集合，就是 `Runtime` 那个 `ToolExecutor.registry` 里当前注册的全部工具（再叠加插件工具），基本没有额外的按会话过滤逻辑。**具体流程（[loop.py:1131-1152](https://claude.ai/epitaxy/dojoagents/agent/loop.py:1131)）：

**1. 基础集合：`self.tool_executor.registry.schema_list()`**（[loop.py:1909-1910](https://claude.ai/epitaxy/dojoagents/agent/loop.py:1909)） 即注册表里**每一个** `ToolSpec.schema()`（name/description/parameters）。这个注册表就是我们之前讨论的、`Runtime._build_harness_agent()` 构建出来的那个——包含：

- harness 声明的各类工具（比如财务的 domain/portfolio/sdk/visualization 工具）
- MCP 工具（`discover_and_register_mcp_tools`）
- Dojo extension 工具
- skill 管理工具（`SkillManagerTool`、`SkillsListTool`、`SkillViewTool`）

**2. 叠加插件工具**（[loop.py:1132-1135](https://claude.ai/epitaxy/dojoagents/agent/loop.py:1132)） 遍历 `plugin_registry.contribution_snapshot().tools`，把插件提供的工具也注册进 registry，并加入 `tool_specs` 列表（避免重名）。

**3. 唯一的过滤：图片轮次排除**（[loop.py:1138](https://claude.ai/epitaxy/dojoagents/agent/loop.py:1138)）

```python
excluded_tools = IMAGE_TURN_EXCLUDED_TOOLS if image_turn else frozenset()
```

如果这一轮用户消息里带图片（`image_turn = openai_content_has_images(user_content)`），会从最终工具列表中剔除 `IMAGE_TURN_EXCLUDED_TOOLS`（[multimodal.py:12](https://claude.ai/epitaxy/dojoagents/agent/multimodal.py:12)）里列出的工具（多是不适合图片轮次用的工具）。除此之外**没有**基于 channel、session、用户角色等的动态裁剪。

**4. 名字消毒**（`_sanitize_tool_specs`） 为避免和 LLM API 的命名规则冲突，工具名会被替换成"安全名"，并维护一个 `safe_name → original_name` 的映射，调用返回后再映射回真实工具名。

**5. 最终打包传给底层 LLM 库（strands）**（[loop.py:1513](https://claude.ai/epitaxy/dojoagents/agent/loop.py:1513)）

```python
tools=strands_tools,
```

这里 `strands_tools` 是把每个 `ToolSpec` 包装成 `DojoBridgedTool`（[loop.py:1142-1151](https://claude.ai/epitaxy/dojoagents/agent/loop.py:1142)）后的列表，最终作为 `tools` 参数交给 LLM 调用——这就是模型在这一轮真正"看得到、可以选择调用"的工具清单。

一句话总结：**发给 LLM 的工具 = 当前 Runtime 的整张 ToolRegistry（所有 harness/MCP/skill/插件工具），只在"这轮消息含图片"时按黑名单排除少数工具，没有更细粒度的按会话/按权限筛选。** 而 `required_services`/`FINANCIAL_SERVICE_ID` 只影响这些工具**背后 handler 该调用谁**，不影响是否出现在这份清单里。

##  _build_harness_agent 中的ToolRegistry instance 和from_config_store中ToolRegistry instance 有overlap的地方吗

**对象层面：完全不重叠。** 它们是两条互斥的 `Runtime` 构建路径，只会用其中一条：

- `Runtime.create()` → `startup()` → `_build_harness_agent()`（现代/async，基于 harness capabilities 的路径）
- `Runtime.from_config_store()`（legacy/同步路径，仅当 harness 提供 `legacy_runtime_contributions` 时才可用，见 [runtime.py:541-543](https://claude.ai/epitaxy/dojoagents/agent/runtime.py:541) 的报错检查）

一个 `Runtime` 实例只会走其中**一条**，所以这两个 `ToolRegistry()` 从来不会同时存在于同一个 `Runtime` 里，更不会共享对象或互相同步。

**内容层面：确实有明显重叠——这是刻意设计的。** [runtime.py:412-415](https://claude.ai/epitaxy/dojoagents/agent/runtime.py:412) 的注释直接写明了原因：

```python
# Core execution tools belong to Agent Core rather than any scenario
# Harness. The legacy Runtime registered these directly; keep the same
# invariant for the Harness-backed Runtime so every Harness can rely on
# the generic execution and session I/O surface.
```

两条路径都会各自独立地注册这批"核心工具"：

- `get_terminal_spec`（终端工具）
- `get_code_execution_spec`（代码执行）
- `get_write_session_file_spec` / `get_read_session_output_spec`（会话文件读写）
- `get_read_session_input_spec`（会话输入读取）
- `get_web_searcher_specs`（网页搜索）
- `ToolsListTool`（工具列表工具）
- MCP 工具（都调用 `discover_and_register_mcp_tools`，但配置来源不同）
- 技能相关工具（`SkillsListTool`、`SkillViewTool` 两边都有；`SkillManagerTool` 只在 legacy 路径里额外注册）

**两者的差异（不重叠部分）：**

- 现代路径独有：来自 `self.capabilities.tools` 的 harness 声明工具（比如财务 domain/portfolio/sdk/visualization 工具）——这些只能通过 harness capability 声明得到。
- legacy 路径独有：multi-agent 委派工具、planning 工具、`PluginListTool`/`PluginDeleteTool` 等——这些是硬编码在 `from_config_store` 方法体里的，`_build_harness_agent` 没有对应逻辑。

**一句话总结：** 两个 `ToolRegistry` **实例**从不重叠（属于互斥的两个 `Runtime` 构建路径，各自 new 一个），但**内容种类**上有意重叠了一批"核心工具"（终端/代码执行/会话文件/搜索等），是为了保证不管走哪条路径，Agent 都具备同样的基础执行能力；再加上各自独有的、来自 harness capabilities 或 legacy 硬编码的差异化工具。
`dojoagents` 里没有字面上叫 `AgentCore` 的类,但推测你指的是 **`dojoagents/agent/` 这个包**——它是整个框架的执行核心(runtime + 主循环 + 会话/上下文/token 管理),体量较大(仅 `runtime.py` + `loop.py` 就近 2900 行)。我启动后台任务深入分析。

后台任务已启动,正在完整阅读 `dojoagents/agent/runtime.py`(装配层)和 `loop.py`(主执行循环),以及会话管理、上下文/token 管理、Provider 抽象、Hook 系统、安全处理等模块,分析整体架构和能力。完成后我会给你结构化总结。

## DojoAgents Agent Core(`dojoagents/agent/`)分析

没有字面上的 `AgentCore` 类,这个"核心"实际由 **`Runtime`(装配层)+ `AgentLoop`(执行引擎)** 两大部分构成,底层建立在 **strands SDK** 之上做二次封装。

### 1. 整体架构([runtime.py](https://claude.ai/epitaxy/dojoagents/agent/runtime.py))

两条组装路径:

- **新路径** `Runtime.compose/create`:委托 `RuntimeComposer` 从 Harness 能力图解析 `tools/memories/skills/mcp_sources/tasks`,逐个实例化后注册进 `ToolRegistry`/`MemoryManager`/`SkillManager`,最终喂给 `AgentLoop`。`startup()` 走 legacy→composed→starting→ready 状态机,失败逐层回滚
- **旧路径** `Runtime.from_config_store`:同步注册核心工具(terminal/write_session_file/code_execution等)、多智能体 `AgentPool`、`PlanExecutionEngine`、MCP 工具发现

关键角色:`ToolRegistry/ToolExecutor`(沙箱化工具执行)、`MemoryManager`(前面分析过)、`SkillManager`、`HarnessRuntime`(工具授权/改写/结果呈现/completion 评估的门面)

### 2. 主循环([loop.py](https://claude.ai/epitaxy/dojoagents/agent/loop.py),1987行)

`AgentLoop.run()` → `_run_core()` 核心流程:

1. 拼 system prompt(多个 `PromptContextSource`:identity/skills/memory/harness指令/attachments)
2. 构建 `DojoStrandsModelBridge` —— 把 Dojo 的 `LLMProvider.chat()` 适配成 **strands `Model` 接口**
3. 每个 Dojo 工具用 `DojoBridgedTool` 包装,接入 harness 的 `transform_calls→authorize→execute→present_results` 三段式管线
4. 注册 hooks(memory hook、`TokenCompressionHook`、guardrail)
5. **真正跑循环的是 `strands.Agent.invoke_async()`**——主循环由 strands 框架驱动,Dojo 通过 Model bridge + Tool bridge + Hooks 注入自己的行为

**Recovery/retry 三层**:空回复恢复(≤1次)→ Harness completion 恢复(循环至 `decision.action != "recover"`)→ Legacy task harness 的 `validate_progress`/`build_recovery_prompt` 循环(cap 3或8)。`GuardrailHaltException` 可强制中断整个 turn。

### 3. Provider 抽象

`LLMProvider` 是 Protocol([providers.py](https://claude.ai/epitaxy/dojoagents/agent/providers.py)):

- `OpenAICompatibleProvider`:覆盖 OpenAI 及所有兼容端点(DeepSeek/Qwen/Kimi/GLM/MiniMax/OpenRouter)
- `GeminiNativeProvider`([gemini_provider.py](https://claude.ai/epitaxy/dojoagents/agent/gemini_provider.py)):直连 Gemini 原生 REST API,单独处理 `thought_signature` 等厂商专属状态
- `get_strands_model()`:另一条路径,直接返回 strands 原生 Model(不经 Dojo 抽象)

### 4. 上下文/Token 管理 —— 与 memory 模块的连接点

- `token_ledger.py`:持久化会话级 token 累计量
- `token_policy.py`:`should_compress()`,阈值判断(默认 `last_prompt_tokens >= max_tokens * 0.8`)
- `compressor.py`:**真正执行压缩**——保护头尾消息,中间部分先剪枝旧工具结果,再用 LLM 生成 `[CONSOLIDATION SUMMARY]+[LONG-TERM FACTS]`,摘要插回消息流,**facts_part 直接调用 `memory_manager.save_memory()` 写入长期记忆**——这正是之前分析的 `LocalMemoryProvider` 里 `[CONSOLIDATED MEMORY FROM PREVIOUS TURNS]` 的真正来源
- `context_usage.py`/`model_context.py`:token 计量与各 provider 的 context window 大小解析

### 5. 会话管理

两套并存:legacy 的 `DojoAgentSessionManager`(文件系统,配合 strands `FileSessionManager`)与新的 canonical `session_run.py`(`CanonicalAgentRun`/`RunCoordinator`/`SessionService`,支持异步事件流用于 SSE/dashboard、pipeline 多步骤续跑)

### 6. Hooks 系统

**确认与 memory hook 是同一套机制**——都基于 `strands.hooks.HookProvider`,实现 `register_hooks(registry)`,挂载到 strands 定义的事件:`BeforeToolCallEvent/AfterToolCallEvent`(工具调用前后)、`BeforeModelCallEvent/AfterModelCallEvent`(LLM调用前后)。`TokenCompressionHook` 与 `MemoryHookProvider` 走完全相同的插件通道。

### 7. 安全/输出处理

- `guardrails.py`:工具调用失败/卡死检测状态机,产出 allow/warn/block/halt
- `redact.py`:正则脱敏(API key、PEM 私钥等)
- `think_scrubber.py`:流式剥离 `<think>` 等推理标签,防止推理过程泄露
- `empty_assistant.py`:检测/恢复空助手回复

### 8. 能力总结与场景

这是一个**基于 strands SDK 二次封装的通用 Agent 执行引擎**:Dojo 自研 Provider 抽象、Tool/Memory/Skill/Session/Guardrail 体系,通过三个桥接点(Model bridge、Tool bridge、Hooks)接入 strands 的循环执行基础设施。核心能力:多 LLM 厂商支持、自动上下文压缩+长期记忆沉淀联动、Harness 驱动的任务完成度评估与自动恢复、工具调用防护栏、多智能体委派与规划引擎(legacy)、双轨会话持久化——典型用于需要长时间多轮迭代、多工具调用、且要求任务完成度可控（不是简单单轮问答）的复杂 Agent 应用场景。


## `DojoStrandsModelBridge`([loop.py:240-417](https://claude.ai/epitaxy/dojoagents/agent/loop.py:240))

**作用**:把 Dojo 自研的 `LLMProvider.chat()` 接口伪装成 strands 框架期望的 `Model` 接口,是 Dojo Provider 体系接入 strands `Agent` 执行循环的**唯一入口**。

**实现细节**:

1. 继承 strands 的 `Model` 抽象类,实现 `stream()` 方法(strands 循环调用的核心方法)
2. **消息格式转换**:调用 `strands_to_dojo_messages()`([420-489行](https://claude.ai/epitaxy/dojoagents/agent/loop.py:420))把 strands 的 block 化消息格式(`text`/`reasoningContent`/`toolUse`/`toolResult` 块)转成 Dojo 内部的 OpenAI 风格消息(`role/content/tool_calls`)
3. **异步流适配**:用 `asyncio.Queue` 把 Dojo Provider 的 `stream_callback` 回调式接口,转成 strands 期望的 `AsyncIterable[StreamEvent]` 生成器——一边在后台任务里跑 `llm_provider.chat()`,一边把增量文本 `yield` 成 strands 的 `contentBlockDelta` 事件
4. **工具调用结果的反向转换**:LLM 返回的 `tool_calls` 被逐个转成 strands 的 `contentBlockStart/Delta/Stop`(`toolUse` 类型)事件
5. **上下文超限的就地自愈**:捕获 `ContextLengthExceededError` 后,调用外部注入的压缩 handler(即 `_dojo_handle_context_length_exceeded`,连接到 `compressor.py`),压缩成功后**用压缩后的消息重试一次**(303-327行),失败才把异常继续抛出
6. 把 provider 返回的推理内容(`reasoning_content`)、用量统计(`usage`)分别塞进 `event_sink`(前端展示)和 `invocation_state`(供 token ledger 记账)

**一句话**:它是"Provider 抽象"与"strands 执行引擎"之间的**协议翻译器 + 流式适配器 + 上下文超限自愈钩子**。

## `DojoBridgedTool`([loop.py:95-237](https://claude.ai/epitaxy/dojoagents/agent/loop.py:95))

**作用**:把 Dojo 的工具规格(`ToolSpec`)和执行器(`ToolExecutor`)包装成 strands 期望的 `AgentTool` 接口,让 strands 循环"以为"自己在调用原生工具,实际上每次调用都会先流经 Dojo 自己的一整套治理管线。

**实现细节**(`stream()` 方法是核心,133-237行):

1. **格式转换**:把 strands 的 `ToolUse`(`toolUseId/input`)转成 Dojo 的 `ToolCall` 对象
2. **三段式治理管线**(仅当挂了 `harness_runtime` 时触发):
    - `transform_calls()`(164行):Harness 可以改写/丢弃这次调用(比如参数注入、拦截危险调用)——若被移除,直接返回错误结果,不再往下走
    - `authorize()`(182行):Harness 做授权判断,返回 `allow/deny` 等 `decision`,拒绝时把原因记进 `turn_context.blocked_calls` 并短路返回
    - `present_results()`(229行):工具执行完后,Harness 还能对结果做二次加工/脱敏/格式化,再返回给模型
3. **真正执行**(217-226行):调用 `tool_executor.execute_one`(或批量的 `execute_many`),并在执行前后用 `contextvar`(`active_session_principal`)绑定/重置当前会话的 principal(权限主体),保证工具执行时能拿到正确的身份上下文
4. **结果记录与事件分发**(`record_result`,144-161行):把结果同时写入 `invocation_state`(供本轮循环内部使用)、`turn_context.tool_results`(供 harness/completion 评估用)、`event_sink`(推给前端/dashboard 实时展示,包含 viz_blocks、artifacts、资源变更等丰富字段)
5. **格式转换回 strands**:最终统一 yield 成 `ToolResultEvent`(strands 格式),包含 `status: success/error` + 文本内容

**一句话**:它是"Dojo 工具执行器 + Harness 治理策略"与"strands 工具调用协议"之间的**适配器**,同时承担了权限检查、结果改写、事件广播、观测数据采集等本该分散在别处的横切逻辑,集中在一个统一的拦截点上完成。

## 两者的关系

这两个类是让 DojoAgents 能够"**借用 strands 的循环,同时保留自己全部治理能力**"的关键设计:strands 只认识 `Model` 和 `AgentTool` 两个接口,Dojo 把自己复杂的 Provider/Tool/Harness/Memory 体系全部塞进这两个接口的具体实现里——**这正是上一轮我们讨论的"桥接复用成熟框架"原则的具体落地案例**。
构建一个 DojoAgents 这个级别的系统,核心不是某个具体技术选型,而是几条贯穿全代码库的**架构纪律**。我从这三轮分析里提炼出以下几点,这也是你如果要自己设计类似系统时应该优先建立的东西:

### 1. 接口先行,实现可插拔(Protocol-based abstraction)

`LLMProvider`、`MemoryProvider` 都先定义成 Protocol,再有多个实现(`OpenAICompatibleProvider`/`GeminiNativeProvider`,`LocalMemoryProvider`/`SkillSummaryMemoryProvider`)。这让"换一个 LLM 厂商"或"换一种记忆策略"变成加一个实现类,而不是改核心循环。**没有这层,系统会随着接入的第三方越多越僵化。**

### 2. 能力以"声明式图"组合,而非硬编码装配

`HarnessCapabilities`(tools/memories/skills/mcp_sources/tasks)+ `RuntimeComposer` 这套模式,把"这个 agent 该有哪些能力"变成一份可以序列化、可以按 harness 差异化配置的规格,而不是在代码里 if-else 拼装。这是让**同一套引擎服务不同产品形态**(比如金融 harness vs 通用 harness)的关键。

### 3. 不重新发明执行循环,而是"桥接"复用成熟框架

DojoAgents 自己不写 tool-calling 主循环,而是通过 `DojoStrandsModelBridge` + `DojoBridgedTool` 把自研的 Provider/Tool 体系接进 strands 的 `Agent.invoke_async()`。**这是一个很值得学的取舍**:核心痛点(多轮工具调用、流式、turn limits)交给已验证的第三方框架,自己只在关键节点(hook)注入差异化逻辑。自己全量重写往往是过度自信的信号。

### 4. Hook/事件是唯一的横切关注点注入方式

Memory、Token 压缩、Guardrail 全部通过同一套 `BeforeToolCallEvent`/`AfterModelCallEvent` 等 strands hook 接入,而不是散落地在主循环里加 if 分支。**这保证了主循环代码不会因为"再加一个功能"而持续膨胀**——新能力=新 hook,不改 loop.py 本体。

### 5. 分层门面(Facade)隔离"原子能力"与"业务组合"

`dojo_core_*`(原子数据服务)与 `domain_api.py`(面向业务场景的聚合门面)是教科书式的分层——下层只管做好一件事,上层负责把多个下层能力组合成"给前端/agent 用的语义化接口"。这让每层都可以独立演进、独立测试。

### 6. 架构边界用测试强制,而不是靠文档约定

`test_architecture_boundaries.py` 直接断言"金融 harness 不能 import dashboard 实现"这类规则。**口头约定的边界迟早被破坏,写成测试的边界才可靠。**

### 7. 幂等性和持久化是一等公民,不是事后补丁

`memory_sync.py` 的 checkpoint 水位 + `idempotency_key`,session 层的原子写(tempfile+fsync+os.replace),都在系统早期就设计进去,而不是出了数据错乱才加。

### 8. 容错设计成"可恢复的状态机",而非"报错即终止"

Guardrail 的 allow/warn/block/halt 分级、空回复恢复、completion 评估驱动的自动重试循环——这套东西说明设计者假设了"模型会犯错、会卡死、会说空话"是常态,系统要能识别并纠偏,而不是简单抛异常。

**如果要动手设计类似系统,我建议的顺序**是:先定义 Provider/Memory/Tool 这几个核心接口 → 搭一个最小的 hook 机制 → 用一个成熟的 agent 循环框架(别自己写)→ 把业务能力(比如 dojo_core 这种数据服务)和编排层(domain_api)从一开始就分开 → 最后才是加 guardrail/恢复/压缩这些"鲁棒性"功能。反过来做(先写业务逻辑,后补架构)是大多数系统变得难维护的根本原因。




## 业务能力(比如 dojo_core 这种数据服务)和编排层(domain_api)的本质区别

|             | **业务能力层**(`dojo_core_*`)                                                 | **编排层**(`domain_api`)                            |
| ----------- | ------------------------------------------------------------------------ | ------------------------------------------------ |
| 职责          | 单一、原子的能力:"给我一个 ticker,返回它的报价"                                            | 组合多个原子能力,拼出面向具体业务场景的完整响应                         |
| 输入依赖        | 直接接收底层 Store(`stock_store`)作为参数                                          | 接收更高层的 `registry`(聚合了多个 Store 的对象)               |
| 是否知道其他能力的存在 | 不知道——`resolve_core_ticker_quote` 完全不 import `resolve_core_ticker_sector` | 知道且负责编排——同时 import 两者                            |
| 函数形态        | 大多是同步纯函数,单一输出模型(`CoreTickerQuoteResponse`)                               | 大多是 async 函数,输出组合后的复合模型(`TickerQuoteResponseV1`) |

## 用代码具体说明

**业务能力层**——[dojo_core_quote.py:12-18](https://claude.ai/epitaxy/dojoagents/dashboard/services/dojo_core_quote.py:12):

```python
def resolve_core_ticker_quote(ticker, *, market=None, stock_store: StockStore) -> Optional[CoreTickerQuoteResponse]:
    """Return live quote snapshot for a DojoCore ticker from the in-memory stock store."""
    symbol, resolved_market = resolve_ticker_symbol(stock_store, ticker, market)
    ...
    return CoreTickerQuoteResponse(...)  # 只管把 stock_store 里的原始报价字段搬进标准响应模型
```

这个函数**只知道"报价"这一件事**,不关心行业分类、不关心汇率、不关心这个 ticker 在什么业务场景下被用到。它的签名里甚至没有 `sector_store`——因为它压根不需要。

**编排层**——[domain_api.py:1689-1707](https://claude.ai/epitaxy/dojoagents/dashboard/services/domain_api.py:1689):

```python
async def build_ticker_quote_v1(registry, *, ticker: str, market: Optional[str]) -> Optional[TickerQuoteResponseV1]:
    quote = resolve_core_ticker_quote(ticker, market=internal_market, stock_store=registry.stock_store)   # 调能力①
    if quote is None:
        return None
    sector_response = resolve_core_ticker_sector(                                                          # 调能力②
        ticker, market=internal_market,
        stock_store=registry.stock_store,
        stock_sector_store=registry.stock_sector_store,
        sector_store=registry.sector_store,
    )
    payload = quote.model_dump()
    payload["name"] = _safe_stock_bilingual_name(stock, quote.ticker)          # 补充能力①②都没有的字段
    payload["sector_paths"] = [_sector_option_to_path(o) for o in sector_response.sector_options]  # 拼装
    return TickerQuoteResponseV1(**payload)
```

这一个函数做了三件 `dojo_core_quote` 单独完成不了的事:

1. **调用两个互不知情的原子能力**(报价 + 行业)
2. **补充跨领域的字段**(双语名称)
3. **把结果拼装成一个新的复合响应模型**(`TickerQuoteResponseV1`),这个模型在 `dojo_core` 层根本不存在

再往上一层,`build_ticker_financials_v1`(domain_api.py:1788起)甚至并行调用财务指标和收入两个 Store,再做汇率换算(`resolve_fin_indicators_for_market`/`resolve_income_for_market`)——同样是"编排层负责组合+跨领域加工,原子层只管自己的一亩三分地"。

# 为什么要分这两层,而不是全写在一起

1. **变更隔离**:如果报价字段的计算逻辑变了(比如 `amount` 的兜底规则),只需要改 `dojo_core_quote.py`,`domain_api.py` 的组合逻辑完全不用动
2. **可独立测试**:`resolve_core_ticker_quote` 是同步纯函数,单元测试给个假的 `stock_store` 就能测,不需要拉起整个 registry;而 `build_ticker_quote_v1` 的测试则专注在"两个能力的结果有没有被正确拼在一起",不需要重复测报价字段本身对不对(这也是 `tests/dashboard/test_dojo_core_quote.py` 单独存在的原因)
3. **复用性**:`resolve_core_ticker_quote` 不止被 `build_ticker_quote_v1` 用,还被 `_quote_valuation_metrics`(domain_api.py:1750)这种完全不同用途的地方复用——原子能力一旦定好接口就能被任意上层随意拼装,这是分层最大的收益
4. **认知负担可控**:看 `dojo_core_quote.py` 时你只需要理解"报价怎么算";看 `domain_api.py` 时你不需要重新理解报价字段的计算细节,只需要理解"这个业务场景需要哪几块能力、怎么拼"

## 和前面讨论的架构原则的呼应

这正是我们上一轮总结的**"分层门面(Facade)隔离原子能力与业务组合"**原则在真实代码里的样子——`dojo_core` 对应"提供单一能力的 Provider",`domain_api` 对应"面向场景组合能力的 Orchestrator"。如果你要在自己的系统里复刻这个模式,判断标准很简单:**一个函数如果需要同时 import 两个以上"原子能力模块"才能完成,它就该待在编排层,而不是被塞进任何一个原子能力模块里**——一旦某个"原子层"函数开始 import 别的原子层模块,分层就已经开始腐化了。

# 接口先行,实现可插拔(Protocol-based abstraction)



## 先看 Protocol 长什么样

**`LLMProvider`**([providers.py:61-73](https://claude.ai/epitaxy/dojoagents/agent/providers.py:61)):

```python
class LLMProvider(Protocol):
    name: str

    async def chat(
        self,
        messages: list[dict],
        tools: list[dict],
        *,
        model: str,
        stream: bool = False,
        metadata: dict | None = None,
        stream_callback: Callable[[str], None] | None = None,
    ) -> LLMResult: ...
```

**`MemoryProvider`**(之前看过的 provider.py):定义了 `initialize/prefetch/sync_turn/on_session_end/save_memory/retrieve_memory` 等方法签名,同样没有任何实现体。

注意关键点:`Protocol` 是 Python `typing` 模块里的**结构化类型(structural typing)**——它不要求实现类去 `class XXX(LLMProvider)` 显式继承,**只要一个类"长得像"这个签名(有同名同参数的方法),就自动被认为符合这个接口**。这跟 Java/C# 那种必须显式 `implements` 接口的方式不同,更接近"鸭子类型加了个类型检查器"。

## 这一个 Protocol 换来了多少个实现

光是 `LLMProvider` 这一个接口,代码里就至少有四种实现,彼此毫无继承关系,只是"方法签名对得上":

|实现类|用途|
|---|---|
|`OpenAICompatibleProvider`|生产环境,真正调用 OpenAI/DeepSeek/Qwen 等厂商 API|
|`GeminiNativeProvider`|生产环境,调用 Gemini 原生 REST API(协议完全不同)|
|`UnconfiguredLLMProvider`([providers.py:87-105](https://claude.ai/epitaxy/dojoagents/agent/providers.py:87))|用户没配置任何 provider 时的兜底占位,`chat()` 直接返回一句提示语,而不是抛异常崩溃|
|`StaticLLMProvider`([providers.py:108-143](https://claude.ai/epitaxy/dojoagents/agent/providers.py:108))|专门给测试用的假实现,预先塞好一批固定 `LLMResult`,`chat()` 被调用时直接按顺序弹出,还顺带记录了 `self.calls` 供断言|

`MemoryProvider` 同理:`LocalMemoryProvider`(读写本地文件)和 `SkillSummaryMemoryProvider`(生成 skill 文件)是两种完全不同的记忆策略,但对 `MemoryManager` 来说,它们都只是"实现了同一组方法的黑盒",可以被同等对待、混合注册(参考 [manager.py:16-21](https://claude.ai/epitaxy/dojoagents/memory/manager.py:16) 的 `add_provider`)。

## "换厂商=加实现类,不改核心循环"具体体现在哪

回到 `DojoStrandsModelBridge`([loop.py:241-243](https://claude.ai/epitaxy/dojoagents/agent/loop.py:241)):

```python
def __init__(self, llm_provider: Any, model_id: str):
    self.llm_provider = ensure_metered_provider(llm_provider)
```

这里的 `llm_provider` 参数类型是 `Any`(概念上是 `LLMProvider` Protocol),桥接层内部只调用 `self.llm_provider.chat(...)`——**它完全不知道背后是 OpenAI 还是 Gemini 还是测试用的 `StaticLLMProvider`**。今天要接一个新的国产大模型厂商,只需要:

1. 写一个新类,实现 `name` 属性 + 一个 `async def chat(...)` 方法,内部调用该厂商的 SDK/HTTP 接口
2. 在配置里指定用这个新 provider

**`loop.py`、`runtime.py` 这些核心文件一行都不用改。** `MemoryManager` 同理——想接一个基于向量数据库的语义检索记忆,只要写一个新类实现同样六个方法,`add_provider` 一下就能接入,主循环、hook 机制完全无感。

## "没有这层,系统会随着接入的第三方越多越僵化"具体指什么

设想反面场景:如果 `DojoStrandsModelBridge` 里不是调用抽象的 `self.llm_provider.chat()`,而是直接写死:

```python
# 反面教材
if self.provider_name == "openai":
    res = await openai_client.chat.completions.create(...)
elif self.provider_name == "gemini":
    res = await gemini_client.generate_content(...)
elif self.provider_name == "deepseek":
    ...
```

会发生什么:

1. **每接一个新厂商,都要回到这个核心桥接类里加一个分支**,而这个类还同时承担着流式适配、异常处理、上下文超限自愈等复杂逻辑——改动风险随着这个函数变大而增加
2. **测试变得困难**:想测试"上下文超限时的自愈逻辑对不对",没法用假的 provider 隔离,必须真的触发某个厂商的 API 报错或者复杂地 mock 具体某个 SDK 的调用
3. **厂商之间的差异会渗透进核心逻辑**:比如 Gemini 需要维护 `thought_signature` 这种厂商专属状态,如果不靠 Protocol 隔离,这类脏细节会散落进桥接层的主干逻辑里,而不是被封装在 `GeminiNativeProvider` 内部
4. **新增能力和已有厂商产生耦合**:比如要给"记忆同步"加个新策略,如果 `MemoryManager` 不是靠 `MemoryProvider` 这种统一接口聚合,而是每种记忆策略都单独写一套调用代码嵌进主循环,那记忆策略之间、记忆策略和主循环之间就会互相牵扯,改一个可能连带影响另一个

**"越接越僵化"的本质是:没有接口隔离时,外部差异性(厂商 API 差异、存储方式差异)会不断侵入并累积进核心逻辑,核心逻辑因此越长越复杂、越来越不敢改动**——这跟上一轮讨论的 Hook 机制想解决的问题(横切关注点污染主循环)是同一类问题的两种表现形式:Hook 解决的是"新增能力"导致的膨胀,Protocol 解决的是"新增第三方实现"导致的膨胀。两者合起来,才能让 `loop.py` 这种核心文件长期保持稳定,不随着系统规模增长而失控。


#  能力以"声明式图"组合,而非硬编码装配



## 先看"声明式图"的数据结构长什么样

[capabilities.py:125-140](https://claude.ai/epitaxy/dojoagents/harnesses/capabilities.py:125):

```python
@dataclass(frozen=True)
class HarnessCapabilities:
    descriptor: HarnessDescriptor
    identity: IdentitySpec | None = None
    skills: tuple[SkillSourceSpec, ...] = ()
    tools: tuple[ToolProviderSpec, ...] = ()
    mcp_sources: tuple[MCPSourceSpec, ...] = ()
    memories: tuple[MemoryProviderSpec, ...] = ()
    tasks: tuple[TaskSourceSpec, ...] = ()
    ...
```

关键是 `frozen=True`——这是一份**不可变的数据(data)**,不是一段可执行的代码(code)。它描述"这个 agent 有哪些工具、哪些记忆 provider、哪些技能来源",但描述本身不包含任何"怎么把它们组装起来跑起来"的逻辑。这就是"声明式"的含义:你只声明"要什么",不写"怎么做"。

## 谁负责生产这份"图"—— `HarnessBuilder`

[builder.py:47-90](https://claude.ai/epitaxy/dojoagents/harnesses/builder.py:47) 的 `HarnessBuilder` 是个一次性收集器:每个 harness 在自己的初始化代码里调用 `builder.add_memory_provider(...)`、`builder.add_skill_source(...)`、`builder.add_tool_source(...)` 等方法往里塞 spec,最后冻结成一份 `HarnessCapabilities`。它还内置了**冲突检测**([builder.py:83-88](https://claude.ai/epitaxy/dojoagents/harnesses/builder.py:83)):两个 spec 用了同一个 `component_id` 会直接报错,而不是静默覆盖——这保证了"声明"本身的正确性在组装阶段就能被校验,而不是运行时才发现两个能力打架。

## 不同 harness 怎么"声明"出不同的产品形态

对比金融 harness 的实际注册代码([financial/harness.py:183-201](https://claude.ai/epitaxy/dojoagents/harnesses/built_in/financial/harness.py:183)):

```python
builder.add_memory_provider(...)   # 金融专属的记忆策略(create_skill_summary_provider)
builder.add_skill_source(SkillSourceSpec("financial.skills.built-in", source, provider=built_in_skills))
builder.add_skill_source(SkillSourceSpec("financial.skills.user", source, provider=context.config.skills.dir))
```

以及文件开头 import 的一整套金融专属组件:`FinancialTurnCompletionPolicy`、`PortfolioFlowPolicy`、`FinancialResultPresenter`、`FINANCIAL_IDENTITY` 身份定义等。

一个通用 harness(或者你自己写的新 harness)完全可以注册**另一套完全不同的 spec 组合**:不同的 `IdentitySpec`(不同的人设)、不同的工具集、不同的 memory provider、甚至不加任何 task/pipeline。**两者产出的都是同一个类型`HarnessCapabilities`,但内容(图的节点)完全不同**——这就是"按 harness 差异化配置"的含义。

## 谁负责消费这份"图"—— `RuntimeComposer`

[runtime.py](https://claude.ai/epitaxy/dojoagents/agent/runtime.py) 里的组装代码是纯粹的遍历,完全不关心图里装的是什么 harness 的东西:

```python
for provider_spec in self.capabilities.tools: ...        # 361行区域
for memory_spec in self.capabilities.memories: ...        # 352行
skill_dirs = [spec.provider for spec in self.capabilities.skills if ...]   # 361行
if self.config.tasks.enabled and self.capabilities.tasks: ...              # 381行
```

`RuntimeComposer` 的代码里**没有一行 `if harness_name == "financial"`**。它只知道"给我一个 `HarnessCapabilities` 对象,我按固定流程把里面的 `tools/memories/skills/tasks` 挨个实例化、注册进对应的 Manager"。

## 为什么这是"同一套引擎服务不同产品形态"的关键

反面写法会是这样(硬编码装配):

```python
# 反面教材
def build_runtime(harness_name: str):
    if harness_name == "financial":
        memory = FinancialSkillSummaryProvider()
        tools = [dojo_core_quote_tool, dojo_core_fin_tool, ...]
        identity = FINANCIAL_IDENTITY
    elif harness_name == "generic":
        memory = LocalMemoryProvider()
        tools = [terminal_tool, code_execution_tool, ...]
        identity = GENERIC_IDENTITY
    elif harness_name == "xxx_new_product":
        ...   # 每加一个产品形态,这个函数就多一个分支,而且这个函数还得跟 Runtime 的组装逻辑耦合在一起
    ...
```

这种写法下,`Runtime`(组装逻辑)和"某个具体产品该有什么能力"(业务决策)**绞在同一段代码里**——加一个新产品形态,必须回来改这个中心函数,而且这个函数会因为要同时理解每个产品的所有细节而不断膨胀,风险和金融 harness 讨论过的"if 分支式横切关注点"是同一类问题。

而 DojoAgents 的做法是把这两件事**彻底切开**:

- **"某个产品该有什么能力"**——这是数据,由每个 harness 自己在 `HarnessBuilder` 里声明,和其他 harness 的声明完全隔离,互不干扰
- **"怎么把能力组装成一个能跑的 Runtime"**——这是逻辑,写死一次在 `RuntimeComposer` 里,对所有 harness 通用,不需要知道具体产品细节

这样一来,**新增一个产品形态(比如"法律助手 harness"、"客服 harness")完全不需要碰 `runtime.py`/`loop.py` 这些引擎代码**,只需要写一个新的 `xxx_harness.py`,用 `HarnessBuilder` 声明这个产品要什么能力就行——这正是"同一套引擎、不同产品形态复用"的字面意思,也是这几轮我们讨论的"接口先行"和"Hook 化横切关注点"两个原则在**更高一层(产品/能力组织层面,而不是单个组件层面)** 的延伸应用:前两者解决的是"一个能力有多种实现"和"一个循环有多个附加行为",这一条解决的是"一个引擎要服务多个完全不同的产品定义"。
# 幂等性和持久化是一等公民,不是事后补丁


## 先说"幂等性"—— `memory_sync.py` 的例子

**场景**:一段对话结束后要把这一轮(turn)同步进长期记忆。但同步这个动作可能因为进程崩溃、网络抖动、worker 被重启而**执行到一半就中断**,下次重启后必须重新跑——问题是:怎么知道哪些 turn 已经同步过了,不会被重复写入两次?

**代码怎么解决**([memory_sync.py:28-67](https://claude.ai/epitaxy/dojoagents/sessions/memory_sync.py:28)):

```python
checkpoint = await self.service.get_checkpoint(principal, session_id, "memory", "sync_watermark")
last_sequence = int(checkpoint.payload.get("last_turn_sequence") or 0)   # 读"水位线"
pending = sorted(turn for turn in turns.items if turn.sequence > last_sequence)  # 只处理水位线之后的

for turn in pending:
    context = {"idempotency_key": turn.turn_id, "turn_id": turn.turn_id}
    await self.memory_manager.sync_turn(..., idempotency_context=context)   # 带着幂等键去同步
    checkpoint = await self.service.put_checkpoint(..., {"last_turn_sequence": turn.sequence}, checkpoint_version)  # 每处理一条就推进一次水位线
```

两个关键设计:

1. **水位线(watermark)**:不是"每次全量重跑",而是记住"上次处理到第几条(`last_turn_sequence`)",下次只处理水位线之后的增量——这是**断点续传**的基础
2. **`idempotency_key`**:即使水位线因为某种原因没推进成功(比如刚写完 memory,还没来得及推进 checkpoint 就崩了),下次重跑同一条 turn 时,`MemoryManager.sync_turn` 内部也会用这个 key 去 `_synced_turn_ids` 集合里查重(我们之前看过 manager.py:46-48),**双重保险**避免重复写入

**如果没有这个设计会怎样**:worker 崩溃重启后,要么重复把同一段对话写进记忆两次(数据污染、记忆里出现重复内容甚至互相矛盾的"事实"),要么因为不知道从哪继续而干脆全量重跑(浪费资源,且如果同步操作本身不是幂等的,同样会产生重复数据)。

## 再说"持久化"—— `session_repository.py` 的原子写

**场景**:往磁盘写一个 session 的 JSON 文件时,如果写到一半进程被杀掉(断电、OOM kill、容器被强制终止),会发生什么?

**代码怎么解决**([session_repository.py:33-54](https://claude.ai/epitaxy/dojoagents/agent/session_repository.py:33)):

```python
def _atomic_write_json(path: Path, data: dict[str, Any]) -> None:
    with tempfile.NamedTemporaryFile(dir=path.parent, suffix=".tmp", delete=False) as handle:
        temp_path = Path(handle.name)
        json.dump(data, handle, ...)
        handle.flush()
        os.fsync(handle.fileno())      # 强制把内核缓冲区刷到磁盘,不依赖操作系统"稍后"落盘
    os.replace(temp_path, path)        # 原子重命名,替换目标文件
```

三个动作缺一不可:

1. **先写临时文件,不直接写目标文件**——万一写到一半崩溃,原文件完好无损,顶多留下一个没用的 `.tmp` 文件
2. **`fsync`**——普通的 `write()` 只是写进操作系统的页缓存,进程崩溃没事,但如果是**断电或内核崩溃**,页缓存里还没落盘的数据会丢;`fsync` 强制把数据物理写入磁盘
3. **`os.replace`(而不是先删除再重命名)**——在 POSIX 系统上是**原子操作**,要么完整看到旧文件,要么完整看到新文件,不存在"读到一半新一半旧"的中间状态

**如果没有这个设计会怎样**:直接 `path.write_text(json.dumps(data))` 这种写法,如果写到第 500 个字节时进程被杀,文件就是一个**损坏的、不完整的 JSON**——下次读取时直接解析失败,这个 session 的历史记录彻底损坏且不可恢复。

## 回到那句话本身:为什么强调"一等公民"而不是"事后补丁"

这两处代码的共同点是:**它们要解决的问题(重复写入、文件损坏)在系统刚开始设计数据流转路径时就被显式考虑进去了**,而不是等生产环境真出现了"用户反馈记忆内容重复了两遍"或者"session 文件打不开报 JSON 解析错误"这种事故之后,再手忙脚乱地打补丁。

"事后补丁"式的解决方案通常长这样:

- 出问题后加一段 `try/except` 把损坏文件捕获掉,静默跳过(掩盖问题,数据还是丢了)
- 加一个"去重脚本"定期跑,清理重复的记忆条目(治标不治本,而且清理逻辑本身很难保证正确)
- 加日志排查,下次出问题人工介入修复(运维成本持续存在)

而"一等公民"式的设计是:**从数据结构和写入协议的层面,让"重复""损坏"这类故障在数学上/操作系统语义上就不可能发生**(或者可以被安全地检测和纠正),而不是靠"运气好没触发"或者"出了事再擦屁股"。这也是为什么这两段代码看起来"多此一举"(为什么不直接 `write_text`?为什么不直接全量重跑?)——因为它们是在为**你还没遇到过、但迟早会遇到的故障场景**提前买保险。

# Hook/事件是唯一的横切关注点注入方式


## "横切关注点"指的是什么

Memory(记忆)、Token 压缩、Guardrail(防护栏)这三件事有一个共同特点:它们都**不是主循环的核心业务逻辑**("跟模型对话、执行工具"),但又需要在循环的**每一次**工具调用、**每一次**模型调用前后插一脚。这种"跟主流程正交、但要嵌入到主流程各个节点"的需求,就是软件工程里说的"横切关注点(cross-cutting concern)"——经典例子还有日志、鉴权、限流。

## 如果不用 Hook,会怎么写

最直观(也是最糟糕)的写法是在 `_run_core()` 主循环里直接堆 if:

```python
# 反面教材,不是真实代码
async def _run_core(self, ...):
    ...
    for turn in range(max_iterations):
        if self.memory_enabled:
            prefetch = await self.memory_manager.prefetch_all(...)
            messages.insert(0, prefetch)
        response = await model.chat(messages)
        if self.token_compression_enabled:
            if should_compress(response):
                messages = await self.compressor.compress(messages)
        for tool_call in response.tool_calls:
            if self.guardrail_enabled:
                decision = self.guardrail.check(tool_call)
                if decision == "halt":
                    raise ...
            result = await execute(tool_call)
            if self.guardrail_enabled:
                self.guardrail.record(result)
            if self.memory_enabled:
                await self.memory_manager.sync_turn(...)
    ...
```

**每加一个新能力,就要回到这同一个函数里插入新的 if 分支**。半年后再加一个"敏感词过滤"、再加一个"审计日志",这个函数会变成几百行的意大利面条,而且这几件事的逻辑互相缠绕在一起,想单独测试 guardrail 都得连着 memory 和 compression 一起跑。

## DojoAgents 实际的做法

[loop.py:1153-1218](https://claude.ai/epitaxy/dojoagents/agent/loop.py:1153) 这一段代码,本质上做的是**"把每个横切关注点封装成一个独立的 Hook 对象,注册到一个共享的 hooks 列表里"**,而不是写进循环体:

```python
hooks = []
hooks.append(memory_hook)                                    # 关注点①: Memory
hooks.append(HookProviderWrapper(token_compression_hook))    # 关注点②: Token 压缩
hooks.append(HookProviderWrapper(self.legacy_behavior.create_hook()))  # 关注点③: legacy 逻辑
hooks.append(check_guardrails_before)                         # 关注点④: Guardrail(调用前)
hooks.append(check_guardrails_after)                          # 关注点④: Guardrail(调用后)
...
strands.Agent(..., hooks=hooks)   # 最后统一交给 strands
```

每个 Hook 内部只关心自己的事,并声明自己要挂在哪个事件上:

- `TokenCompressionHook.register_hooks`([token_compression.py:33-37](https://claude.ai/epitaxy/dojoagents/agent/hooks/token_compression.py:33)):
    
    ```python
    registry.add_callback(BeforeModelCallEvent, self._before_model_call)registry.add_callback(AfterModelCallEvent, self._after_model_call)
    ```
    
- `MemoryHookProvider.register_hooks`(之前看过的 manager.py:100-105):
    
    ```python
    registry.add_callback(BeforeInvocationEvent, self._on_before_invocation)registry.add_callback(MessageAddedEvent, self._on_message_added)registry.add_callback(AfterInvocationEvent, self._on_after_invocation)
    ```
    
- `check_guardrails_before/after`(loop.py:1225,1380)挂在 `BeforeToolCallEvent`/`AfterToolCallEvent`

**主循环本体(`_run_core`)完全不知道 Memory、Token 压缩、Guardrail 这三个东西的存在**——它只管把 `hooks` 这个列表交给 `strands.Agent`,剩下的事由 strands 在跑循环的过程中,在对应的时间点(调用模型前/后、调用工具前/后)自动触发这些回调。

## 为什么这样"保证主循环不会膨胀"

对比两种写法的增量成本:

||if 分支式|Hook 式|
|---|---|---|
|加一个新能力(比如"敏感词过滤")|要回到 `_run_core` 里找到合适的插入点,加 if,还要担心跟已有分支的执行顺序冲突|新建一个 `SensitiveWordHook` 类,写 `register_hooks` 声明挂在哪个事件上,在 loop.py 里加一行 `hooks.append(...)`|
|关闭/测试某个能力|要理解并绕开循环体里的其他分支|直接不 append 那个 hook 即可,其他 hook 不受影响|
|代码量增长位置|全部堆积在 `_run_core` 这一个函数里|分散到各自独立的文件(`hooks/token_compression.py`、`guardrails.py`)|
|单元测试|必须跑通整个主循环才能验证一个分支|可以直接构造一个假的 `event` 对象,单独调用 `hook._before_model_call(event)` 测试|

**这就是"新能力=新 hook,不改 loop.py 本体"的具体含义**:`_run_core` 这个函数从系统建立之初,承担的角色就是"组装 hooks 列表 + 把控制权交给 strands",而不是"实现所有功能"。所以即便系统运行了很久、加了很多能力,这个核心函数的复杂度**理论上不会随功能数量线性增长**——增长的是 hooks 目录下文件的数量,而不是这一个函数的行数。这也是为什么在架构讨论里,"横切关注点用统一的拦截机制(Hook/中间件/AOP)处理"会被反复强调——它是少数几个"能真正长期抑制核心模块腐化"的设计手段之一。

 
# 容错设计成"可恢复的状态机",而非"报错即终止"


## 先说"报错即终止"式设计是什么样子

如果不考虑容错,一个 agent 循环最朴素的写法是:工具调用失败就抛异常,模型返回空内容就当作结束,任务没做完就直接把"未完成"扔给用户。这种设计背后的假设是**"模型的输出总是可信、总是完整的"**——但现实是 LLM 会:

- 卡在同一个错误的工具调用里反复重试(死循环)
- 偶尔生成一个"既没有文字也没有工具调用"的空回复(推理中断)
- 自己觉得任务做完了,但实际上遗漏了用户要的交付物

**如果系统假设这些情况"不会发生"或者"发生了就该终止",那这些常见的模型失误会直接变成用户能看到的崩溃或者半成品结果。** DojoAgents 的做法反过来:把这些"异常情况"当成**系统正常运行的一部分**,设计成有限状态机去识别、分级、纠正。

## 证据一:Guardrail 的 allow/warn/block/halt 分级状态机

[guardrails.py:48-63](https://claude.ai/epitaxy/dojoagents/agent/guardrails.py:48) 定义了四级动作,不是"要么放行要么报错"的二元判断:

```python
@dataclass(frozen=True)
class ToolGuardrailDecision:
    action: str = "allow"  # allow | warn | block | halt
    @property
    def allows_execution(self) -> bool:
        return self.action in {"allow", "warn"}
    @property
    def should_halt(self) -> bool:
        return self.action in {"block", "halt"}
```

它内部维护了三套独立的计数器状态([guardrails.py:83-92](https://claude.ai/epitaxy/dojoagents/agent/guardrails.py:83)):`_exact_failure_counts`(同一个工具+同一组参数失败次数)、`_same_tool_failure_counts`(同一个工具连续失败次数)、`_no_progress`(只读工具反复返回相同结果、没有推进任务)。

关键在于**分级的阈值设计**([guardrails.py:69-81](https://claude.ai/epitaxy/dojoagents/agent/guardrails.py:69)):同一调用失败 2 次先警告(`exact_failure_warn_after`),失败 5 次才拦截(`exact_failure_block_after`);同一工具连续失败 8 次才彻底 halt(`same_tool_failure_halt_after`)。这不是"一失败就终止",而是**给模型犯错留了缓冲区**——偶尔失败一次是正常的(网络抖动、参数试探),只有当模式明显是"卡死循环"时才升级动作。而且 `warn` 级别的处理方式很巧妙([guardrails.py:259-264](https://claude.ai/epitaxy/dojoagents/agent/guardrails.py:259) `append_toolguard_guidance`):不是拦截调用,而是把警告文字**追加进工具结果里返给模型自己看**,相当于让模型"看到自己在重复犯错"从而自我纠正——这是把纠错信号变成了模型能理解的自然语言反馈,而不是系统层面的强制中断。

## 证据二:空回复恢复

[empty_assistant.py](https://claude.ai/epitaxy/dojoagents/agent/empty_assistant.py) 专门处理"模型这一轮什么都没说、也没调工具"这种退化情况:

```python
def is_empty_assistant_content(content: Any) -> bool:
    ...
    return not has_text and not has_tool_use
```

一旦检测到,系统不会把它当成"任务结束"或者报错,而是构造一段专门的恢复提示词塞回去([empty_assistant.py:93-111](https://claude.ai/epitaxy/dojoagents/agent/empty_assistant.py:93)):

```
"[Empty reply recovery] The previous assistant turn produced no text or tool calls; 
the task is NOT complete. ... Do NOT end with another empty reply."
```

甚至还专门标记了持久化层面的处理([empty_assistant.py:57-64](https://claude.ai/epitaxy/dojoagents/agent/empty_assistant.py:57) `mark_incomplete_assistant_payload`)——把这条空消息在 session 存储里标记为"未完成",这样即使跨会话重新加载历史,系统依然知道"上次这里出过问题",而不是让一条无意义的空消息静静地留在历史记录里误导后续判断。

## 证据三:Completion 评估驱动的自动恢复循环

之前分析 `loop.py` 时看到的机制:`harness_runtime.evaluate_completion` 在每轮结束后判断任务是否真的完成,如果 `decision.action == "recover"` 就自动构造恢复提示词,让模型继续做,直到评估通过或达到 `max_extra_turns` 上限。这意味着"模型自己以为做完了,但其实没做完"这种情况也被当成一种可识别、可恢复的状态,而不是简单地把模型的最后一句话当作最终答案直接返回给用户。

## 三者的共同结构:状态机而非异常处理

把这三个机制放在一起看,它们有一个共同的骨架:

```
识别异常状态(检测函数) → 分类严重程度(轻微/中度/严重) → 采取对应动作(继续/警告/拦截/终止) → 
   如果还能恢复,构造纠偏输入反馈给模型 → 重新进入正常流程,而不是抛出异常跳出循环
```

这正是"状态机"而非"try/except 报错终止"的本质区别:

- **异常处理式设计**的隐含假设是"错误是例外情况,发生了就该让调用方处理(通常是终止或降级)"
- **状态机式设计**的隐含假设是"错误(甚至连续犯错)是这个系统运行的正常状态之一,系统本身要有能力在错误状态和正常状态之间转换,并且从错误状态里找路径走回正常状态"

## 为什么这条原则对"设计 agent 级别的系统"特别关键

传统软件系统里,"输入"来自代码或者结构化的用户操作,出错的模式相对可枚举,try/except 兜底通常够用。但**agent 系统的"决策者"是一个概率模型**,它的失败模式(卡死循环、空输出、自我评估错误、幻觉认为任务完成)本质上是**高频且难以枚举穷尽**的——你没法在开发阶段列举出所有"模型可能犯的错",能做的只是识别几类**统计上高频的失败模式**(重复失败、空回复、过早收敛),然后为每一类建一个可恢复的状态机分支。这也是为什么这条原则被单独拎出来强调:**它不是"锦上添花的健壮性",而是 agent 系统能不能在生产环境稳定运行的分水岭**——一个没有这层设计的 agent 系统,大概率会在真实用户的长尾输入下频繁卡死或者交付半成品,而这一点在传统 CRUD 系统里几乎不会遇到。
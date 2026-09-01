This is a substantial codebase — let me delegate a thorough investigation to an Explore agent rather than reading everything myself.

我已经启动一个后台探索任务，正在深入阅读 `dojoagents/memory/` 下的 provider.py、manager.py、local_memory.py、skill_summary.py，以及 `dojoagents/sessions/memory_sync.py` 和相关配置文件，来分析记忆系统的架构、存储方式、与 session/agent 的集成方式、核心能力和典型应用场景。完成后我会给你结构化的总结。

## DojoAgents Memory 系统分析

### 架构

- **[provider.py](https://claude.ai/epitaxy/dojoagents/memory/provider.py)**:`MemoryProvider` 协议接口，定义 `initialize / prefetch / sync_turn / on_session_end / save_memory / retrieve_memory` 等方法
- **[manager.py](https://claude.ai/epitaxy/dojoagents/memory/manager.py)**:`MemoryManager` 聚合多个 provider(非继承),规定最多一个"外部"provider + 可并存的 `skill_summary`。通过 `as_hook_provider()`(manager.py:92)挂到 Strands 框架的 `BeforeInvocationEvent/MessageAddedEvent/AfterInvocationEvent` 生命周期钩子
- 两个内置实现:
    - **[local_memory.py](https://claude.ai/epitaxy/dojoagents/memory/local_memory.py)** — 本地会话摘要记忆
    - **[skill_summary.py](https://claude.ai/epitaxy/dojoagents/memory/skill_summary.py)** — 把会话固化为可复用技能

### 存储方式

纯文件/Markdown,无数据库,持久化在 `~/.dojo/`:

- `LocalMemoryProvider`:`~/.dojo/agents/memory/session_{id}.txt`,每次**整体覆写**
- `SkillSummaryMemoryProvider`:`~/.dojo/skills/generated/generated-{slug}/SKILL.md`,带 YAML frontmatter

### 与 Agent 执行流程的集成

- **调用前**(`_on_before_invocation`,manager.py:107):用最近用户消息作 query 预取记忆,注入 system prompt
- **调用后**(`_on_after_invocation`,manager.py:148):同步本轮对话到记忆,并触发 `on_session_end`
- **[memory_sync.py](https://claude.ai/epitaxy/dojoagents/sessions/memory_sync.py)** 的 `SessionMemorySyncWorker`:独立的异步补偿同步器,基于 checkpoint 水位游标 + `idempotency_key` 保证崩溃重试时不重复写入

### 关键能力

1. **写入**:`save_memory`/`sync_turn`/`on_session_end`
2. **检索**:`retrieve_memory`、`prefetch_all`(自动注入 system prompt)
3. **摘要/巩固**:超 token 阈值时把历史压缩为 `[CONSOLIDATED MEMORY]` 长期事实
4. **程序性记忆(skill 化)**:把一次成功的工作流固化为可复用的 `SKILL.md`
5. **多 provider 聚合 + 幂等/断点续传**

### 典型应用场景

- **长对话/多轮上下文压缩**:token 超限时摘要存档,下轮延续上下文
- **流程复用(procedural memory)**:成功完成的任务流程沉淀为技能,供未来会话直接调用
- **持久化 session 的可靠记忆同步**:后台 worker 保证即使实时 hook 失败也能补齐记忆,不重复写

### 配置项

- [config/models.py](https://claude.ai/epitaxy/dojoagents/config/models.py):`MemoryConfig.provider="skill_summary"`(默认)、`generated_skill_dir`、`SessionsConfig.sync_memory=True`
- [harnesses/capabilities.py](https://claude.ai/epitaxy/dojoagents/harnesses/capabilities.py):`MemoryProviderSpec`/`HarnessCapabilities.memories` 允许各 harness 注册自己的记忆 provider 实现




# **`retrieve_memory` 的具体实现:**

**1. Provider 层 —— [local_memory.py:58-65](https://claude.ai/epitaxy/dojoagents/memory/local_memory.py:58)**

```python
async def retrieve_memory(self, session_id: str, query: str) -> str:
    mem_file = self.memory_dir / f"session_{session_id}.txt"
    if mem_file.exists():
        try:
            return mem_file.read_text(encoding="utf-8")
        except Exception:
            pass
    return ""
```

实现很朴素:

- **不使用 `query` 参数**——签名里收了但完全没用于过滤/检索,属于"占位"式语义检索接口
- 直接按 `session_id` 拼出固定路径 `~/.dojo/agents/memory/session_{session_id}.txt`,把整个文件内容原样读出返回
- 没有向量库、embedding、关键词匹配等真正的"检索"逻辑,本质是**按 session_id 做全量读取**
- 异常被吞掉(`except Exception: pass`),文件不存在或读取失败都返回空字符串

**2. Manager 层聚合 —— [manager.py:83-90](https://claude.ai/epitaxy/dojoagents/memory/manager.py:83)**

```python
async def retrieve_memory(self, session_id: str, query: str) -> str:
    results = []
    for provider in self._providers:
        if hasattr(provider, "retrieve_memory"):
            res = await provider.retrieve_memory(session_id, query)
            if res:
                results.append(res)
    return "\n\n".join(results)
```

- 遍历所有已注册 provider(用 `hasattr` 做鸭子类型检查,而非强制协议实现)
- 逐个调用各自的 `retrieve_memory`,把非空结果用 `"\n\n"` 拼接成一个字符串返回
- `skill_summary.py` 里**没有**实现 `retrieve_memory`(之前搜索结果中未出现),所以目前只有 `LocalMemoryProvider` 真正参与这一聚合

**要点**:这个方法目前和 `prefetch`(local_memory.py:24)功能高度重叠——两者都是读同一个文件、返回同样内容,唯一区别是 `prefetch` 会加 `[CONSOLIDATED MEMORY FROM PREVIOUS TURNS]:` 前缀且被 hook 自动调用,而 `retrieve_memory` 是暴露给外部主动调用的裸接口(没有语义检索能力,`query` 参数是摆设)。


，从代码看**当前实现里 memory 严格按 `session_id` 隔离，不会自动跨 session 共享/检索**:

**1. `LocalMemoryProvider`** — [local_memory.py:26,51,59](https://claude.ai/epitaxy/dojoagents/memory/local_memory.py:26)

- 文件名固定为 `session_{session_id}.txt`
- `prefetch`/`retrieve_memory` 只会读取**同一个** `session_id` 对应的文件
- 换一个新 session,`session_id` 变了 → 文件路径变了 → 读不到旧 session 的任何内容

**2. `SkillSummaryMemoryProvider`** — [skill_summary.py:46-47](https://claude.ai/epitaxy/dojoagents/memory/skill_summary.py:46)

```python
slug = self._slug(self.session_id or "session")
skill_dir = self.generated_skill_dir / f"generated-{slug}"
```

- 生成的技能目录名也是以 `session_id` 做 slug,每个 session 结束后都会生成**独立的一份** `generated-{slug}/SKILL.md`,不会合并进同一份记忆,也不会按内容去重/关联到其他 session

**结论**:

- 单个 session 内:有效(通过 `sync_turn` 累积 → `on_session_end`/`save_memory` 落盘 → 下次同 session 用 `prefetch`/`retrieve_memory` 读回)
- 跨 session:**默认不共享**——两个不同 `session_id` 各自读写各自的文件,互不可见
- 唯一间接的"跨 session"路径是:如果 DojoAgents 的 **skill 加载系统**(`dojoagents/skills/`)会去扫描 `~/.dojo/skills/generated/` 目录里所有历史 session 生成的 `SKILL.md` 并加载进新 session 的可用技能列表,那么新 session 理论上能"复用"旧 session 沉淀的流程知识——但这依赖 skill 发现机制,而不是 `retrieve_memory` 这条路径本身。如果你需要我确认 skill 系统是否真的会跨 session 扫描加载这些生成文件,我可以再查一下 `dojoagents/skills/` 的加载逻辑。



# 程序性记忆的实现

分两条链路： **生成**(memory 侧)+ **加载复用**(skills 侧),两者通过磁盘目录约定连接。

### 1. 生成阶段 —— `SkillSummaryMemoryProvider`

**触发时机**:[manager.py:182-183](https://claude.ai/epitaxy/dojoagents/memory/manager.py:182) 的 `MemoryHookProvider._on_after_invocation` 在**每次 Agent 调用结束后**都会调用 `manager.on_session_end(agent.messages)`——注意这不是严格意义的"会话真正结束",而是每轮 `AfterInvocationEvent` 都触发一次。

**具体逻辑**([skill_summary.py:42-59](https://claude.ai/epitaxy/dojoagents/memory/skill_summary.py:42)):

```python
async def on_session_end(self, messages):
    text = "\n".join(str(m.get("content", "")) for m in messages).strip()
    if not text:
        return
    slug = self._slug(self.session_id or "session")
    skill_dir = self.generated_skill_dir / f"generated-{slug}"
    skill = (
        "---\n"
        f"name: generated-{slug}\n"
        "description: Generated procedural memory from a DojoAgents session.\n"
        "---\n\n"
        "# Generated Workflow Memory\n\n"
        "Use this skill only as procedural context for similar future analysis.\n\n"
        "## Session Summary\n\n"
        f"{text}\n"
    )
    (skill_dir / "SKILL.md").write_text(skill, encoding="utf-8")
```

- 把整个消息历史(而非"总结")原样拼成文本
- 按固定模板套上 YAML frontmatter,写成标准 Skill 文件格式
- 目录名 `generated-{slug}` 与 session_id 绑定,**同一 session 反复调用会覆写同一个文件**(不会越写越多)
- **没有"成功判定"逻辑**——不管这轮对话是否真正成功完成任务,只要有内容就会落盘,注释里"a successful workflow"更多是设计意图而非代码强制的条件

### 2. 复用阶段 —— `SkillManager` 扫描加载

**关键连接点**在 [runtime.py:562-568](https://claude.ai/epitaxy/dojoagents/agent/runtime.py:562):

```python
skill_dirs = (
    [skills_cfg.dir, skills_cfg.generated_skill_dir, built_in_dir]
    + skills_cfg.external_dirs
    + list(plugin_snapshot.skill_dirs)
)
```

`generated_skill_dir`(默认 `~/.dojo/skills/generated`)被**直接作为 skill 搜索路径之一**注册进 `SkillManager`。

**加载逻辑**([manager.py:108-128](https://claude.ai/epitaxy/dojoagents/skills/manager.py:108)):

```python
for root in self.skill_dirs:
    for skill_file in sorted(root.glob("*/SKILL.md")):
        skill_name = skill_file.parent.name
        frontmatter, body = self._get_skill_content(skill_file)
        ...
        skills_data.append((skill_name, frontmatter, body))
```

- 用 glob `*/SKILL.md` 遍历目录下所有子文件夹,逐个解析 frontmatter + body
- 解析结果拼进 `prompt_block()`——即系统提示词里的 "Available Skills" 部分
- 如果开了 `lazy_skills`,则只列目录+描述,要求模型调用 `skill_view(name=...)` 才加载全文;否则直接把全文塞进 system prompt

### 完整链路总结

```
第 N 次会话结束 → MemoryHookProvider.on_session_end()
                → SkillSummaryMemoryProvider 把整段对话写成 SKILL.md
                → 存入 ~/.dojo/skills/generated/generated-{session_slug}/

第 N+1 次(甚至任意)会话启动 → runtime.py 构造 SkillManager 时
                → 把 generated_skill_dir 纳入 skill_dirs
                → glob 扫描出这份 SKILL.md
                → 拼进新会话的 system prompt(或注册为 lazy skill 供按需查看)
```

**几个需要注意的点**:

1. 目前是"整段对话原样存档",不是 LLM 生成的摘要——没有调用模型做提炼/压缩,是纯字符串拼接
2. 没有成功/失败的判定,也没有去重或质量筛选,理论上每个 session 都会产生一份新的 generated skill,长期会造成 `generated-*` 目录堆积
3. 之前提到的两条 `SkillManager` 构造路径([runtime.py:361](https://claude.ai/epitaxy/dojoagents/agent/runtime.py:361) vs [runtime.py:573](https://claude.ai/epitaxy/dojoagents/agent/runtime.py:573))不完全一致——第一条(361行)的 `skill_dirs` 只取自 `self.capabilities.skills`,并**不包含** `generated_skill_dir`;第二条(573行)才显式加了 `skills_cfg.generated_skill_dir`。这意味着生成的技能能否被下次会话捕获,取决于具体走的是哪条初始化路径/harness 配置——如果你在用的是走 361 行这条路径的 harness,生成的 SKILL.md 实际上**不会**被自动加载,需要确认你的 harness 走的是哪个构造函数。

**目前这个实现生成的不是真正意义上的"技能"(可复用的、被提炼的操作指南),而是把整段原始对话历史套了个 Skill 文件的壳**。

依据就是 [skill_summary.py:42-44](https://claude.ai/epitaxy/dojoagents/memory/skill_summary.py:42):

```python
async def on_session_end(self, messages):
    text = "\n".join(str(m.get("content", "")) for m in messages).strip()
    ...
```

这里:

- `messages` 是 `agent.messages` 完整消息列表(用户输入、助手输出、工具调用结果等全部原样在内)
- 直接把每条消息的 `content` 字段 `str()` 化后用换行拼接——**没有做任何总结、提炼、去除工具调用噪音、去除重复内容**
- 唯一"包装"是套了个 YAML frontmatter(`name`/`description`)和几行固定模板文字,让它在文件格式上看起来像一个标准 Skill

对比真正的 Skill 应该长什么样(比如项目里 `dojoagents/skills/built_in/` 下手写的那些,或者你在系统提示里看到的 `docx`/`pptx`/`code-review` 等技能描述)——那些是:

- 精炼过的、结构化的操作步骤/触发条件/参数说明
- 面向"下一次遇到类似任务该怎么做"而写,不含具体某一次对话的私有细节(比如用户问的具体公司名、具体文件路径)

而这里生成出来的东西:

- 本质是**一份会话日志的存档**,被伪装成 Skill 格式
- 塞进新会话的 system prompt 后,模型看到的是"上次一模一样对话的原始记录",而不是"抽象出来的可复用方法论"
- 没有模型参与"总结成技能"这一步——如果要做到真正的程序性记忆提炼,通常需要额外调一次 LLM,让它读会话历史后输出"这次做了什么任务、关键步骤是什么、可复用的模式是什么",再写入 SKILL.md,但当前代码里完全没有这一步

所以准确地说,这是一个 **"伪 Skill 化"的会话归档机制**,离真正可靠地沉淀"程序性记忆"还有一步之遥——如果你在做技术评审或需要向别人解释这块设计,这个是个值得指出的落差点(注释里写的"Generated procedural memory"和实际实现之间的语义差距)。
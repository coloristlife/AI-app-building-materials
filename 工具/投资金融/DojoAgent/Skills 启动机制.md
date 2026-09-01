**每一次聊天回合都会启动 skills 机制**，它不是可选项，而是构建系统提示词（system prompt）时的固定一步。具体如下：

## 1. 每轮对话都会触发 `skill_manager.prompt_block()`

在 [loop.py:852](https://claude.ai/epitaxy/dojoagents/agent/loop.py:852)：

```python
skill_prompt = self.skill_manager.prompt_block(platform=request.channel)
```

这行代码在**每次**用户发消息、构建 system prompt 时都会执行，生成结果会被插入到 prompt 的某个 phase 位置（[loop.py:861-872](https://claude.ai/epitaxy/dojoagents/agent/loop.py:861)）。

## 2. 哪些 skill 会被"看到"（进入候选列表）

`SkillManager` 是在 `_build_harness_agent()` 里创建的（[runtime.py:359-368](https://claude.ai/epitaxy/dojoagents/agent/runtime.py:359)），它的 `skill_dirs` 来自 `capabilities.skills`——而这些目录是财务 harness 在 `configure_core_capabilities()` 里声明的（[harness.py:190-201](https://claude.ai/epitaxy/dojoagents/harnesses/built_in/financial/harness.py:190)）：

- `financial.skills.built-in`（内置 skills 目录）
- `financial.skills.user`（用户自定义 skills 目录）
- `financial.skills.generated`（自动生成的 skills 目录）
- `financial.skills.external.{n}`（外部扩展目录，多个）

`prompt_block()`（[manager.py:99-160](https://claude.ai/epitaxy/dojoagents/skills/manager.py:99)）扫描这些目录下所有 `*/SKILL.md`，对每个候选 skill 做三层过滤（[manager.py:100-128](https://claude.ai/epitaxy/dojoagents/skills/manager.py:100)）：

- **同名去重**（`seen_skills`，先出现的目录优先）
- **`disabled_skills` / `platform_disabled`** — 被禁用或不匹配当前操作系统平台的跳过
- **`requires_tools`**（frontmatter 里声明）— 如果该 skill 声明了依赖的工具名，但那个工具没在 `self.loaded_tools`（即当前 `ToolRegistry` 里所有工具名）里，就跳过

## 3. 通过后的 skill 是"整篇塞进 prompt"还是"只给目录"？—— 取决于 `lazy_skills`

- **`lazy_skills=True`（默认，也是常见配置）**：只把**目录**（分类 + 名字 + description）塞进 prompt，并显式指示 LLM：
    
    > "You MUST call `skill_view(name='<skill_name>')` to load the full skill instructions before performing any workflow related to these skills." 也就是说，这一步**只是"列出有哪些 skill 可用"，不加载全文**。真正加载某个 skill 的完整内容，要等 LLM 在会话中主动调用 `skill_view(name=...)` 工具（[skill_manage.py:274-293](https://claude.ai/epitaxy/dojoagents/tools/skill_manage.py:274)），此时才读取该 skill 的 SKILL.md 全文返回给 LLM。`skills_list()` 工具（[skill_manage.py:230-243](https://claude.ai/epitaxy/dojoagents/tools/skill_manage.py:230)）也可以用来重新列一遍目录。
    
- **`lazy_skills=False`**：所有通过过滤的 skill 全文（frontmatter + body）会被直接拼接进 prompt，一次性全塞进去，不需要 LLM 主动调用工具去加载。
    

## 4. 一句话总结

**每轮对话都会跑一遍 skill 扫描+过滤逻辑；哪些 skill 真正"被使用"取决于：**

1. 它在哪个 `skill_dirs` 目录下有 `SKILL.md`
2. 没被 `disabled_skills`/`platform_disabled` 禁用
3. 它声明的 `requires_tools` 都在当前 `ToolRegistry` 里
4. （懒加载模式下）LLM 是否在这轮对话里主动调用了 `skill_view(name=...)` 来加载该 skill 的具体指令内容——只有被调用过的那个 skill 才算"真正被使用"，其余只是"被展示在目录里但没被加载"。


# skill_dirs
`skill_dirs` 最终是从 `self.capabilities.skills`（即 `configure_core_capabilities()` 里通过 `builder.add_skill_source(...)` 声明的那些）汇总而来（[runtime.py:359](https://claude.ai/epitaxy/dojoagents/agent/runtime.py:359)）。对财务 harness 来说，具体是这 4+N 类目录：

## 固定的 4 个（[harness.py:190-201](https://claude.ai/epitaxy/dojoagents/harnesses/built_in/financial/harness.py:190)）

|component_id|实际路径|来源|
|---|---|---|
|`financial.skills.built-in`|`<dojoagents 包安装目录>/dojoagents/skills/built_in`|硬编码，随包分发|
|`financial.skills.user`|`context.config.skills.dir` → 默认 `~/.dojo/skills`|用户配置 `SkillsConfig.dir`|
|`financial.skills.generated`|`context.config.skills.generated_skill_dir` → 默认 `~/.dojo/skills/generated`|自动生成的 skill 存放处|
|`financial.skills.external.{i}`（0..N）|`context.config.skills.external_dirs` 里配置的每一个路径|默认是空列表，用户可在 `agents.yaml` 里加|

**内置目录（`financial.skills.built-in`）实际内容**（我刚查了本地文件系统）：

```
dojoagents/skills/built_in/
├── canvas-chart
├── plan
├── subagent-driven-development
└── writing-plans
```

（每个子目录下应该有一个 `SKILL.md`）

## 额外可能加入的（在 `RuntimeComposer.compose()` 层面追加）

[composer.py:93-108](https://claude.ai/epitaxy/dojoagents/harnesses/composer.py:93)：如果 `config.harness.extra_skill_dirs` 配置了额外目录，会再补充一批 `extra.skills.{hash}` 的 skill source，provider 是这些目录本身。默认这个配置通常是空的。

## 注意：`~/.claude/skills` 不在这条路径里

`SkillsConfig.read_claude_skills`（默认 `False`）配置项，是用于把 `~/.claude/skills` 加进 skill_dirs 的——但这个逻辑**只存在于 legacy 的 `Runtime.from_config_store()` 路径**里（[runtime.py:571-572](https://claude.ai/epitaxy/dojoagents/agent/runtime.py:571)），现代的 `_build_harness_agent()` 路径（`Runtime.create()`）**没有**这一步,所以走 dashboard 的 embedded runtime 时不会读取 `~/.claude/skills`。

## 总结

对于 dashboard 场景（`create_embedded_runtime` → `Runtime.create()` → financial harness），实际生效的 skill 目录一般是：

```
<pip安装的dojoagents包>/skills/built_in     (4个内置 skill)
~/.dojo/skills                              (用户自定义)
~/.dojo/skills/generated                    (自动生成)
<agents.yaml 里 skills.external_dirs 配置的任意目录>（默认为空）
```



# `lazy_skills = True


当 `lazy_skills=True` 时，skill 是靠 **LLM 主动调用工具、按需拉取全文** 的方式加载的，是一个"目录 → 判断 → 调用 → 注入上下文"的多步过程：

## 第 1 步：prompt 里只给"目录"，不给正文

`skill_manager.prompt_block()`（[manager.py:130-151](https://claude.ai/epitaxy/dojoagents/skills/manager.py:130)）只输出类似这样的内容，塞进 system prompt：

```
## Available Skills (Mandatory Lazy Loader)
You MUST call `skill_view(name='<skill_name>')` to load the full skill
instructions before performing any workflow related to these skills.
Skill Catalog:
  Category: analysis
    - stock-trend-analysis: Analyze historical price trends for a ticker.
    - canvas-chart: Render a chart artifact from data.
```

这时 LLM **只知道有哪些 skill、每个是干什么的（一句话描述）**，不知道具体怎么做。

## 第 2 步：LLM 自己判断这轮任务是否命中某个 skill

这一步**完全靠模型自身推理**，代码里没有强制匹配逻辑——唯一的约束就是 prompt 里那句 "You MUST call skill_view... before performing any workflow related to these skills"，靠模型遵循这条指令自觉去查。

## 第 3 步：LLM 发出工具调用 `skill_view(name='stock-trend-analysis')`

这和调用任何其他工具（比如财务工具）走的是**完全相同的通道**：

```
LLM 产生 ToolCall(name="skill_view", arguments={"name": "..."})
  → ToolExecutor.execute_one()（executor.py:70）
  → registry.get("skill_view").handler(...)
  → SkillViewTool.handle_call()（skill_manage.py:290-306）
```

## 第 4 步：`SkillViewTool.handle_call()` 读取该 skill 全文并原样返回

```python
skill_file = root / name / "SKILL.md"
content = skill_file.read_text(encoding="utf-8")
return {"content": content, "metadata": {"ok": True}}
```

（[skill_manage.py:299-303](https://claude.ai/epitaxy/dojoagents/tools/skill_manage.py:299)）——把整份 `SKILL.md`（包括 YAML frontmatter 和正文指令）当作**工具调用结果**返回，不是重新塞进 system prompt。

## 第 5 步：这份全文作为一条 tool-result 消息进入对话历史

`ToolExecutor` 返回的结果会被 `AgentLoop` 包装成一条 `tool` 角色的消息，加入本轮对话的 messages 列表，随下一次请求一起发给 LLM——**LLM 就是通过读这条 tool 消息"看到"了 skill 的完整指令**，然后据此规划后续该调用哪些真正的业务工具（比如财务工具）来完成任务。

## 几个补充细节

- **`skills_list()` 工具**（[skill_manage.py:230-271](https://claude.ai/epitaxy/dojoagents/tools/skill_manage.py:230)）是备用手段：如果模型想重新看一遍完整目录（含 JSON 格式），也可以主动调它，效果和 prompt 里那段目录基本一致。
- **磁盘读取有缓存**：`SkillManager._get_skill_content()` 内部用 `SkillPromptCache`（按文件 mtime 缓存），避免同一份 SKILL.md 被反复读盘，但这只是性能优化，跟"是否已经加载过"的语义无关。
- **"已加载"不是持久状态**：一旦这次对话历史被压缩（`compressor.compress()`）或者话题跨出了上下文窗口，之前读过的 skill 全文可能被清掉——如果后续还要用，LLM 需要**再调用一次 `skill_view`** 重新拉取，代码里没有"本次 session 已加载过就跳过"的记忆机制。
- **加载 skill 本身不会改变 `ToolRegistry`**：skill 是纯文本"操作指南"（程序性记忆），加载后只是给 LLM 提供参考步骤，它仍然是用已经注册好的那些工具（终端、代码执行、财务工具等）去执行具体动作。

一句话：**`lazy_skills=True` 时，skill 加载 = LLM 把 `skill_view` 当成一个普通工具调用，读回 SKILL.md 全文塞进对话上下文，然后自己照着做——跟你之前问的"财务工具怎么被调用"是同一条 `ToolExecutor` 执行路径，只是这里 handler 返回的是文本指令而不是业务数据。**


# prompt_block中如何把 skill description， category， 等信息塞进system prompt

整个过程是自动化的，没有人工干预，具体机制是：

## 1. 自动扫描目录找 `SKILL.md` 文件

`prompt_block()`（[manager.py:99-128](https://claude.ai/epitaxy/dojoagents/skills/manager.py:99)）对每个 `skill_dirs` 里的目录做：

```python
for root in self.skill_dirs:
    for skill_file in sorted(root.glob("*/SKILL.md")):
        skill_name = skill_file.parent.name   # 文件夹名 = skill 的名字
```

也就是约定：**每个 skill 是一个子文件夹，文件夹名就是 skill 名，里面必须有一个 `SKILL.md`**。比如 `dojoagents/skills/built_in/canvas-chart/SKILL.md`，skill 名就是 `canvas-chart`。

## 2. 自动解析 YAML frontmatter，提取 `category`/`description`

`_get_skill_content()` → `parse_frontmatter()`（[manager.py:36-61](https://claude.ai/epitaxy/dojoagents/skills/manager.py:36)）读取文件内容，把开头 `---...---` 之间的 YAML 解析成字典（`frontmatter`），剩下的正文是 `body`（这一步 lazy 模式下不会被用到，只有 `skill_view` 才会读取正文）。

一个典型的 SKILL.md 大概长这样：

```markdown
---
category: analysis
description: Analyze historical price trends for a ticker.
platforms: [macos, linux]
requires_tools: [get_ticker_price_trends]
---
# 正文指令...
```

## 3. 摘取 `category` + `description` 拼成目录文本

```python
for name, fm, _ in skills_data:
    cat = fm.get("category", "general")
    desc = fm.get("description", "No description provided.")
    categories.setdefault(cat, []).append({"name": name, "description": desc})
```

（[manager.py:141-145](https://claude.ai/epitaxy/dojoagents/skills/manager.py:141)）——**只摘取 frontmatter 里的 `category` 和 `description` 字段**（连同文件夹名 `name`），正文（body）在 lazy 模式下完全不读取到 prompt 里，只用来在扫描阶段做过滤判断（platform/requires_tools）。

## 4. 拼成 catalog 字符串，插入 system prompt

最终格式化成：

```
## Available Skills (Mandatory Lazy Loader)
...
Skill Catalog:
  Category: analysis
    - canvas-chart: Render a chart artifact from data.
    - stock-trend-analysis: Analyze historical price trends for a ticker.
```

这段字符串会通过 [loop.py:852-872](https://claude.ai/epitaxy/dojoagents/agent/loop.py:852) 插入本轮 system prompt 中。

## 一句话总结

**是的：`prompt_block()` 每轮都会自动 glob 所有 `skill_dirs/*/SKILL.md`，解析其 YAML frontmatter，只摘取 `category` + `description`（加上文件夹名当 name），拼成一份轻量目录塞进 system prompt；正文内容（body）不会自动进 prompt，要等 LLM 调用 `skill_view` 才会被读出来返回。**
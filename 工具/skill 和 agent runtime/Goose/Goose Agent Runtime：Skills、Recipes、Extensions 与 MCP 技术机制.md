---
内容生成: AI
---


> **Scope:** Goose Agent Runtime architecture  
> **Focus:** Skills、Recipes、Extensions、MCP、`load`、`delegate` 以及它们之间的关系  
> **Last verified:** 2026-08-14
> 
> Goose 官方文档目前将 Skills 定义为可复用的 instructions/resources，将 Recipes 定义为可复用的配置/workflows；Goose 还通过内置 Summon extension 提供 source discovery、`load` 和 `delegate` 等能力。([Goose Docs](https://goose-docs.ai/docs/guides/context-engineering/using-skills/?utm_source=chatgpt.com "Agent Skills | goose | Your open source AI agent"))

---

## 1. Goose 是什么

Goose 是一个开源的 AI Agent Runtime。

它的核心并不是单纯的 Chat UI，而是一个能够把：

- LLM
    
- Instructions
    
- Skills
    
- Recipes
    
- Extensions
    
- MCP servers
    
- Tools
    
- Subagents
    
- Knowledge / files
    

组合起来执行任务的 Agent Runtime。

可以把它抽象成：

```text
User
  │
  ▼
Goose UI / CLI
  │
  ▼
Agent Runtime
  │
  ├── LLM
  │
  ├── Skills
  │
  ├── Recipes
  │
  ├── Extensions
  │     └── MCP / Built-in Tools
  │
  └── Subagents
```

其中最重要的区别是：

> **Skill 主要解决“Agent 应该知道什么、怎么做”；Recipe 主要解决“这个任务应该以什么配置和流程运行”；Extension/MCP 解决“Agent 能实际调用什么”。**

Goose 官方当前也明确把这几个概念区分为不同用途。([Goose Docs](https://goose-docs.ai/docs/guides/context-engineering/custom-agents/?utm_source=chatgpt.com "Custom Agents | goose | Your open source AI agent"))

---

# 2. Skill

## 2.1 Skill 是什么

Goose Skill 是：

> **A reusable set of instructions and resources that teaches goose how to perform a specific task or use a specific domain expertise.**

也就是说，Skill 本质上是：

```text
Instructions
+
Domain Knowledge
+
Procedures
+
Supporting Resources
```

Goose 官方文档明确说明 Skill 可以从简单 checklist 到复杂 workflow，并可以包含 scripts、templates 等 supporting files。([Goose Docs](https://goose-docs.ai/docs/guides/context-engineering/using-skills/?utm_source=chatgpt.com "Agent Skills | goose | Your open source AI agent"))

---

## 2.2 Skill 文件结构

标准结构：

```text
skill-name/
└── SKILL.md
```

例如：

```text
security-knowledge/
├── SKILL.md
├── references/
│   ├── mcp-security.md
│   ├── prompt-injection.md
│   └── controls.md
└── scripts/
    └── search.py
```

`SKILL.md` 使用 YAML frontmatter：

```yaml
---
name: security-knowledge
description: Security knowledge and security review guidance
---

# Security Knowledge

...
```

`SKILL.md` 是 Skill 的核心识别文件。Goose 推荐的标准位置包括：

```text
~/.agents/skills/
.agents/skills/
```

同时 Goose 为兼容性保留了 `.goose/skills/`、`.claude/skills/` 等路径。([Goose Docs](https://goose-docs.ai/docs/guides/context-engineering/using-skills/?utm_source=chatgpt.com "Agent Skills | goose | Your open source AI agent"))

---

# 3. Skill 是怎么被 Goose 使用的

Skill 不是启动时把全部内容塞进 context。

Goose 使用一种 **progressive disclosure** 思路。

大致过程：

```text
Goose startup
     │
     ▼
Discover Skills
     │
     ▼
Read name + description
     │
     ▼
Put lightweight skill information
into Agent instructions
     │
     ▼
User request
     │
     ▼
Relevant Skill?
     │
     ├── No → normal Agent
     │
     └── Yes
          │
          ▼
       Load Skill
          │
          ▼
     Full SKILL.md
          │
          ▼
   Supporting resources
          │
          ▼
       Agent uses it
```

Goose 官方文档明确描述了这种 discovery → relevant loading → application 的过程。([Goose Docs](https://goose-docs.ai/docs/guides/context-engineering/using-skills/?utm_source=chatgpt.com "Agent Skills | goose | Your open source AI agent"))

---

# 4. Skill 与 Knowledge Base 的关系

这是构建 Security Knowledge System 时非常重要的区别。

**Skill ≠ Knowledge Base**

更准确地说：

```text
Skill
  │
  ├── instructions
  ├── procedures
  └── knowledge access rules
          │
          ▼
     Knowledge Base
```

例如：

```text
Security Knowledge Skill
```

可以告诉 Agent：

```text
1. Identify the security domain.
2. Search the Knowledge Base.
3. Retrieve relevant Knowledge Objects.
4. Analyze relationships.
5. Cite evidence.
```

而真正的数据可以位于：

```text
Security Knowledge Base
├── threats/
├── controls/
├── components/
├── patterns/
├── relationships/
└── sources/
```

因此：

> **Skill 是使用知识的能力/方法；Knowledge Base 是知识本身。**

---

# 5. Recipe

## 5.1 Recipe 是什么

Goose 官方定义：

> **Recipes are reusable goose configurations that package up instructions and settings so the setup can be easily shared and launched by others.** ([Goose Docs](https://goose-docs.ai/docs/guides/recipes/recipe-reference/?utm_source=chatgpt.com "Recipe Reference Guide | goose | Your open source AI agent"))

更容易理解的说法：

> **Recipe = 一个可复用的 Agent 任务配置 / workflow definition。**

Recipe 可以把：

```text
Prompt
+
Instructions
+
Settings
+
Extensions
+
Parameters
+
Sub-recipes
```

组合在一起。

---

# 6. Recipe 和 Skill 的区别

这是整个 Goose 架构中最容易混淆的地方。

||Skill|Recipe|
|---|---|---|
|核心目的|教 Agent|配置任务|
|主要内容|Instructions / Knowledge / Procedures|Prompt / Settings / Extensions / Parameters|
|典型文件|`SKILL.md`|`.yaml` / `.json`|
|使用方式|按需加载|启动/运行一个预配置任务|
|类比|技能手册|工作流/任务模板|
|是否行业标准|Agent Skills 正在形成跨平台规范|Recipe 主要是 Goose 概念|
|是否需要 MCP|不需要|不需要|
|是否可以包含 MCP|可以间接使用|可以直接配置|

Goose 官方的简化描述非常好：

> **Skills and recipes define what goose should know or do.**  
> Skill 更适合 reusable workflow/domain procedure；Recipe 更适合把 prompts、settings、extensions、parameters 打包成可重复任务。([Goose Docs](https://goose-docs.ai/docs/guides/context-engineering/custom-agents/?utm_source=chatgpt.com "Custom Agents | goose | Your open source AI agent"))

---

# 7. Recipe Schema

Recipe 通常使用：

```text
.yaml
.yml
.json
```

其中 Goose 文档推荐 YAML；目前 CLI 对 `.yml` 有额外限制，因此实际使用最好采用 `.yaml`。([Goose Docs](https://goose-docs.ai/docs/guides/recipes/recipe-reference/?utm_source=chatgpt.com "Recipe Reference Guide | goose | Your open source AI agent"))

一个简化 Recipe：

```yaml
version: "1.0.0"

title: Security Architecture Review

description: >
  Perform a security architecture review.

prompt: |
  Review the provided architecture.
  Identify components, trust boundaries,
  threats, applicable controls,
  and security gaps.

extensions:
  - type: builtin
    name: developer

parameters:
  - key: architecture
    input_type: file
    requirement: required
    description: Architecture document to review
```

Recipe 的核心字段包括：

```text
version
title
description
instructions
prompt
extensions
settings
parameters
activities
response
sub_recipes
```

具体字段和 schema 以 Goose 当前 Recipe Reference 为准。([Goose Docs](https://goose-docs.ai/docs/guides/recipes/recipe-reference/?utm_source=chatgpt.com "Recipe Reference Guide | goose | Your open source AI agent"))

---

# 8. Recipe 在 Runtime 中的作用

Recipe 的作用不是“一个特殊的 Prompt 文件”。

它更像：

```text
Recipe
   │
   ├── What should the Agent do?
   │       ↓
   │     prompt/instructions
   │
   ├── What tools should it have?
   │       ↓
   │     extensions
   │
   ├── What model/settings?
   │       ↓
   │     settings
   │
   ├── What input?
   │       ↓
   │     parameters
   │
   └── What other workflows?
           ↓
        sub_recipes
```

因此：

```text
Recipe
  ↓
Configure Agent Session
  ↓
Start Agent
  ↓
Agent executes task
```

---

# 9. Extension

Extension 是 Agent 的**工具能力层**。

可以简单理解：

> **Extension = 给 Agent 提供 Tools 的机制。**

例如：

```yaml
extensions:
  - type: builtin
    name: developer
```

表示：

> 为这个 Agent Session 加载 Goose 内置的 `developer` extension。

而：

```yaml
extensions:
  - type: streamable_http
    name: security-knowledge
    uri: http://localhost:3000/mcp
```

则表示：

> 给 Agent 加载一个 MCP-based extension。

因此：

```text
Extension
   │
   ├── Built-in tools
   │
   └── MCP tools
```

---

# 10. MCP 在这里的位置

MCP 可以理解成：

> **Agent 与外部工具/服务之间的标准连接协议。**

例如你的 Security Knowledge MCP 可以暴露：

```text
search_knowledge()
get_knowledge_object()
find_related_controls()
find_related_threats()
```

于是：

```text
Goose
  │
  ▼
Security Skill
  │
  ▼
Security Knowledge MCP
  │
  ▼
Knowledge Base
```

这时 Skill 决定：

> **什么时候、为什么、怎么使用知识。**

MCP 决定：

> **具体通过什么 Tool 去访问知识。**

---

# 11. Skill、Recipe、Extension、MCP 的完整关系

建议把 Goose 的架构记成：

```text
                         Goose Runtime
                              │
             ┌────────────────┼────────────────┐
             │                │                │
           Skill            Recipe          Extension
             │                │                │
             │                │         ┌──────┴──────┐
             │                │         │             │
             │                │      Built-in        MCP
             │                │         │             │
             │                │         ▼             ▼
             │                │       Tools         Tools
             │                │
             ▼                ▼
       Agent knowledge    Agent workflow
       & procedure       & configuration
             │                │
             └────────┬───────┘
                      ▼
                    Agent
                      │
                      ▼
                     LLM
```

---

# 12. `load` 和 `delegate`

这是 Goose 当前架构中非常值得关注的部分。

Goose 引入了统一的 source model：

```text
Source
├── Skill
├── Recipe
├── Agent
└── Subrecipe
```

然后通过两个核心操作：

```text
load
delegate
```

---

## 12.1 `load`

`load` 的概念：

> **把一个 source 加载到当前 Agent context。**

例如：

```text
load(source="security-knowledge")
```

可以理解成：

```text
Current Agent
      │
      ▼
Load Security Skill
      │
      ▼
Skill instructions
进入当前 context
```

不会因此自动创建一个新的 Agent。

---

## 12.2 `delegate`

`delegate` 的概念：

> **把任务交给一个独立的 Agent/subagent 执行。**

例如：

```text
delegate(
    source="security-review"
)
```

可以理解成：

```text
Current Agent
      │
      ▼
Delegate
      │
      ▼
New isolated Agent
      │
      ▼
Execute Security Review
      │
      ▼
Return result
```

Goose 的统一工具设计明确提出：

> `load` = “Teach me this”  
> `delegate` = “Do this for me”

并允许 Skill、Recipe、Agent 等 source 使用这两种模式。([GitHub](https://github.com/aaif-goose/goose/discussions/6202?utm_source=chatgpt.com "Unified Tooling for Recipes, Subrecipes, Claude Skills, and Claude Subagents · aaif-goose goose · Discussion #6202 · GitHub"))

---

# 13. 为什么这很重要？

因为这意味着：

### Skill 不只是“自动加载的 Markdown”。

它可以：

```text
load Skill
```

也可以：

```text
delegate Skill
```

### Recipe 也不只是“运行一次的 YAML”。

它也可以：

```text
load Recipe
```

或者：

```text
delegate Recipe
```

Goose 的统一 Source/`load`/`delegate` 设计正是为了实现这种组合能力。([GitHub](https://github.com/aaif-goose/goose/discussions/6202?utm_source=chatgpt.com "Unified Tooling for Recipes, Subrecipes, Claude Skills, and Claude Subagents · aaif-goose goose · Discussion #6202 · GitHub"))

---

# 14. Summon Extension

Goose 目前通过 **Summon Extension** 提供这一套能力。

官方文档把 Summon 描述为：

> 用于把 knowledge 加载到 Goose context，并把任务 delegate 给 subagents。

它可以处理：

```text
Skills
Recipes
Subagents / Agents
```

Goose 新版本中 Summon 是一个内置的平台 extension。([Goose Docs](https://goose-docs.ai/docs/mcp/summon-mcp?utm_source=chatgpt.com "Summon Extension | goose | Your open source AI agent"))

---

# 15. Recipe 的 Sub-recipes

Recipe 可以进一步组合其他 Recipe。

例如：

```text
Security Review Recipe
│
├── Architecture Analysis Recipe
│
├── Threat Analysis Recipe
│
├── Control Mapping Recipe
│
└── Report Generation Recipe
```

例如：

```yaml
sub_recipes:
  - name: threat-analysis
    path: ./threat-analysis.yaml

  - name: control-mapping
    path: ./control-mapping.yaml
```

然后 Agent 可以通过 delegation 执行这些 sub-recipes。Goose 官方文档也支持并行 sub-recipes 和 subagents。([GitHub](https://github.com/aaif-goose/goose/blob/main/CUSTOM_DISTROS.md?utm_source=chatgpt.com "goose/CUSTOM_DISTROS.md at main · aaif-goose/goose · GitHub"))

---

# 16. 一个完整的 Security Review 示例

假设你要构建：

```text
Security Architecture Review
```

整个系统可以设计成：

```text
                         User
                           │
                           ▼
                    Goose Chat UI
                           │
                           ▼
                     Goose Agent
                           │
                           ▼
                Security Review Recipe
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
          ▼                ▼                 ▼
 Security Skills      Extensions        Parameters
          │                │                 │
          │          ┌─────┴─────┐           │
          │          ▼           ▼           │
          │      Developer      MCP          │
          │                    │              │
          │                    ▼              │
          │             Security KB          │
          │                    │              │
          ▼                    ▼              ▼
   Security Knowledge     Retrieval       Architecture
   Threat Modeling          │             Document
   MCP Security             │
          │                 │
          └────────┬────────┘
                   ▼
              Agent Reasoning
                   │
                   ▼
             Security Findings
                   │
                   ▼
             Review Report
```

---

# 17. 对你的 Security Knowledge Base，推荐的架构

结合你现在设计的 Knowledge Object Schema，我会建议：

```text
security-agent/
│
├── skills/
│   │
│   ├── security-knowledge/
│   │   └── SKILL.md
│   │
│   ├── threat-modeling/
│   │   └── SKILL.md
│   │
│   └── mcp-security/
│       └── SKILL.md
│
├── recipes/
│   │
│   ├── architecture-review.yaml
│   ├── threat-model-generation.yaml
│   └── security-report.yaml
│
└── knowledge/
    │
    ├── threats/
    ├── controls/
    ├── components/
    ├── patterns/
    ├── relationships/
    └── sources/
```

其中：

```text
Knowledge
   ↓
“知道什么”

Skill
   ↓
“如何利用这些知识”

Recipe
   ↓
“这次任务如何组织”

Extension / MCP
   ↓
“Agent 能实际调用什么”

Goose
   ↓
“如何运行整个 Agent”
```

---

# 18. 最重要的架构原则

如果你的目标不是只给 Goose 做一个 demo，而是准备做一个**长期可移植的 Security Agent System**，我建议不要把你的核心架构绑定到 Goose Recipe。

应该定义自己的抽象：

```text
Security Knowledge
Security Skill
Security Workflow
Security Tool
```

然后 Goose 只是其中一个 Runtime：

```text
Your Architecture
       │
       ├── Skill
       │
       ├── Knowledge
       │
       ├── Workflow
       │
       └── Tools
              │
              ▼
       ┌──────────────┐
       │ Goose        │
       │ Runtime      │
       └──────────────┘
              │
              ▼
          Recipe
```

也就是说：

> **你的“Workflow”是通用概念；Goose Recipe 是这个 Workflow 在 Goose Runtime 中的一种实现。**

这也解释了为什么 Recipe 这个词本身不是整个 Agent 行业的统一标准，而 Goose 官方把它定义成自己的 reusable configuration/workflow abstraction。([Goose Docs](https://goose-docs.ai/docs/guides/recipes/recipe-reference/?utm_source=chatgpt.com "Recipe Reference Guide | goose | Your open source AI agent"))

---

# 19. 一张最终心智模型

如果以后你再看到 Goose 的这些概念，可以直接用这一张图理解：

```text
                         ┌───────────────┐
                         │     USER      │
                         └───────┬───────┘
                                 │
                                 ▼
                         ┌───────────────┐
                         │ GOOSE RUNTIME │
                         └───────┬───────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
           SKILL              RECIPE            AGENT
              │                  │                  │
        “Know / How”       “Task / Workflow”   “Who / Role”
              │                  │                  │
              │          ┌───────┴───────┐          │
              │          │               │          │
              │       Settings       Extensions     │
              │                          │          │
              │                     ┌────┴────┐     │
              │                     ▼         ▼     │
              │                  Built-in    MCP    │
              │                     │         │     │
              │                     └────┬────┘     │
              │                          │          │
              └──────────────────────────┼──────────┘
                                         ▼
                                   Agent + LLM
                                         │
                              ┌──────────┴──────────┐
                              ▼                     ▼
                           `load`               `delegate`
                              │                     │
                         Current Context       Subagent
```

### 最后浓缩成 5 句话

1. **Skill**：告诉 Agent **“怎么做 / 知道什么”**。
    
2. **Knowledge Base**：提供 Agent **“真正的知识和数据”**。
    
3. **Extension / MCP**：给 Agent **“实际操作能力”**。
    
4. **Recipe**：把 **prompt + settings + extensions + parameters + workflow** 打包成一个可复用的 Agent 任务配置。
    
5. **Goose Runtime**：负责把这些东西组合起来，并通过 `load` / `delegate` 等机制让 Agent 使用它们。
    

这套结构非常适合你现在的 **Security Knowledge Base → Security Skill → Security Review Workflow → Goose Runtime** 这个方向。
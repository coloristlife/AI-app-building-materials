https://github.com/agentskills/agentskills/tree/main
https://agentskills.io/home
The Agent Skills format was originally developed by [Anthropic](https://www.anthropic.com/), released as an open standard, and has been adopted by a growing number of agent products. The standard is open to contributions from the broader ecosystem.





# Agent Skills 简单使用手册

> 本手册只介绍 `agentskills/agentskills` 的基本概念、Skill 创建、验证和使用方式，不涉及具体业务场景。

官方仓库：[agentskills/agentskills](https://github.com/agentskills/agentskills?utm_source=chatgpt.com)

---

## 1. Agent Skills 是什么？

**Agent Skills 是一种用于给 AI Agent 提供可复用能力和工作流程的开放规范。**

一个 Skill 本质上是一个目录，最核心的文件是：

```text
my-skill/
└── SKILL.md
```

更完整的 Skill 可以包含：

```text
my-skill/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

可以简单理解为：

```text
SKILL.md
   ↓
告诉 Agent：
“这个 Skill 是什么，以及应该怎么做”
```

而 `references/`、`scripts/`、`assets/` 是 Skill 可以使用的附加资源。

---

# 2. `agentskills/agentskills` 仓库是干什么的？

这个仓库**不是一个 Agent，也不是 Skill Generator**。

它主要包含：

```text
Agent Skills
├── Specification
├── Documentation
└── skills-ref
```

分别用于：

|部分|用途|
|---|---|
|Specification|定义 Skill 的格式和行为规范|
|Documentation|说明如何创建和使用 Skill|
|`skills-ref`|提供参考实现和验证工具|

因此：

> **这个 repo 的主要作用是定义标准，以及帮助你检查 Skill 是否符合标准。**

---

# 3. 创建第一个 Skill

创建一个目录：

```bash
mkdir my-skill
cd my-skill
```

创建：

```bash
touch SKILL.md
```

现在：

```text
my-skill/
└── SKILL.md
```

---

# 4. 编写 `SKILL.md`

一个最简单的 Skill：

```markdown
---
name: hello-world
description: A simple skill that explains how to create and use an Agent Skill.
---

# Hello World

This skill demonstrates the basic structure of an Agent Skill.

## Instructions

When this skill is activated:

1. Explain what an Agent Skill is.
2. Explain how the Skill works.
3. Provide a simple example.
```

这里有两个重要部分：

```yaml
---
name: hello-world
description: A simple skill that explains how to create and use an Agent Skill.
---
```

以及 Markdown body：

```markdown
# Hello World

...
```

---

# 5. `name`

`name` 是 Skill 的名称。

例如：

```yaml
name: hello-world
```

通常需要满足：

- 使用小写字母
    
- 可以使用数字
    
- 可以使用 `-`
    
- 不能以 `-` 开头或结尾
    
- 不能使用连续的 `--`
    
- Skill 目录名称应该与 `name` 一致
    

因此：

```text
hello-world/
└── SKILL.md
```

对应：

```yaml
name: hello-world
```

而不是：

```yaml
name: Hello World
```

详细规则见官方 Specification。[Agent Skills Specification](https://github.com/agentskills/agentskills/blob/main/docs/specification.mdx?utm_source=chatgpt.com)

---

# 6. `description`

`description` 用来告诉 Agent：

> **这个 Skill 是做什么的，以及什么时候应该使用它。**

例如：

```yaml
description: >
  Help users create and validate Agent Skills.
  Use when the user wants to create, modify, or validate a Skill.
```

`description` 很重要，因为 Agent 可以利用它进行 **Skill Discovery**。

因此不要只写：

```yaml
description: Skill
```

最好写清楚：

```text
做什么 + 什么时候使用
```

---

# 7. `SKILL.md` 的正文是什么？

Frontmatter 后面的 Markdown 内容就是 Skill 的具体 instructions。

例如：

```markdown
# Code Review

Review source code for security and quality issues.

## Workflow

1. Understand the code.
2. Identify potential problems.
3. Explain each finding.
4. Provide recommendations.

## Output

Return:

- Findings
- Severity
- Explanation
- Recommendation
```

这里没有一个必须遵守的固定 Markdown 模板。

你可以根据 Skill 的用途组织内容。

---

# 8. `references/`

当 Skill 需要大量参考资料时，可以使用：

```text
my-skill/
├── SKILL.md
└── references/
    ├── guide.md
    ├── examples.md
    └── rules.md
```

然后在 `SKILL.md` 中告诉 Agent：

```markdown
## References

For detailed rules, read:

- `references/rules.md`
- `references/examples.md`
```

这样就不需要把所有内容都塞进 `SKILL.md`。

这也是 Agent Skills **progressive disclosure** 设计的一部分：

```text
Discovery
   ↓
name + description

Activation
   ↓
SKILL.md

Execution
   ↓
references/
scripts/
assets/
```

---

# 9. `scripts/`

如果 Skill 需要执行程序，可以添加：

```text
my-skill/
├── SKILL.md
└── scripts/
    └── check.py
```

然后在 `SKILL.md` 中说明：

```markdown
## Validation

Run:

scripts/check.py
```

`SKILL.md` 负责告诉 Agent **什么时候以及为什么使用脚本**。

脚本本身负责执行具体的程序逻辑。

---

# 10. `assets/`

如果 Skill 需要模板或其他静态文件，可以：

```text
my-skill/
├── SKILL.md
└── assets/
    ├── template.md
    └── example.json
```

例如：

```markdown
Use `assets/template.md` as the output template.
```

---

# 11. 一个完整的 Skill

因此一个比较完整的 Skill 可以是：

```text
my-skill/
│
├── SKILL.md
│
├── references/
│   ├── guide.md
│   └── examples.md
│
├── scripts/
│   └── check.py
│
└── assets/
    └── template.md
```

但是要注意：

**这些目录都不是必须的。**

最小 Skill 仍然只是：

```text
my-skill/
└── SKILL.md
```

---

# 12. 如何验证 Skill？

Agent Skills 仓库提供 `skills-ref` 相关工具用于验证 Skill。

官方文档中可以看到类似：

```bash
skills-ref validate ./my-skill
```

但这里有一个容易踩坑的地方：

**`skills-ref` 并不是你 clone GitHub repository 后就自动存在的系统命令。**

因此直接执行：

```bash
skills-ref validate ./my-skill
```

如果得到：

```text
command not found: skills-ref
```

并不代表 Skill 有问题。

你需要先安装/通过 Python tooling 使用它。

当前可以使用 repo 中的 `skills-ref` 子目录，例如通过 `uv`：

```bash
uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref skills-ref validate ./my-skill
```

---

# 13. `validate` 到底验证什么？

运行：

```bash
... validate ./my-skill
```

实际上是在检查：

```text
my-skill/
└── SKILL.md
       │
       ├── frontmatter
       ├── name
       ├── description
       ├── naming rules
       └── Skill structure
```

也就是说：

```text
SKILL.md
    ↓
Validator
    ↓
符合 / 不符合
Agent Skills Specification
```

**`SKILL.md` 本身不是 validator。**

它是：

> **被 validator 检查的 Skill。**

---

# 14. Agent 如何使用 Skill？

Agent Skills 的基本工作方式可以理解为三个阶段。

### 第一步：Discovery

Agent 首先知道有哪些 Skill：

```text
hello-world
code-review
pdf-processing
...
```

主要依赖：

```text
name
description
```

---

### 第二步：Activation

用户提出任务：

> Review this code.

Agent 判断：

```text
code-review
```

与当前任务相关。

于是加载：

```text
code-review/SKILL.md
```

---

### 第三步：Execution

Agent 根据 `SKILL.md` 执行任务。

如果需要：

```text
references/
scripts/
assets/
```

再读取或使用这些资源。

因此可以简单记成：

```text
Discover
   ↓
Activate
   ↓
Execute
```

---

# 15. Agent Skills 和 Agent 的关系

Agent Skills **不是 Agent 本身**。

可以理解为：

```text
             Agent
               │
       ┌───────┴────────┐
       ↓                ↓
     Skills           Tools
       │                │
       ↓                ↓
  instructions      external actions
```

Skill 主要描述：

> **如何完成某类任务。**

Tool / MCP 则主要提供：

> **Agent 可以调用什么外部能力。**

一个 Skill 不一定需要 MCP，也不一定需要任何外部 Tool。

最简单的 Skill 完全可以只有：

```text
SKILL.md
```

---

# 16. Agent Skills 和 Skill Generator 的区别

这是使用这个 repo 时最容易混淆的一点。

### AgentSkills repo

```text
Specification
+
Documentation
+
Validation/reference tooling
```

它告诉你：

> **Skill 应该怎么写。**

### Skill Creator / Generator

```text
User requirement
       ↓
AI
       ↓
SKILL.md
```

它帮助你：

> **自动创建 Skill。**

所以：

**AgentSkills repo ≠ Skill Generator。**

如果你的目标是“让 AI 根据我的描述自动生成 Skill”，需要另外使用 Skill Creator / Generator。

---

# 17. 最小实践

如果只是想快速体验整个流程，可以做：

### Step 1

```bash
mkdir hello-world
cd hello-world
```

### Step 2

创建：

```text
SKILL.md
```

内容：

```markdown
---
name: hello-world
description: Explain the basic concept and usage of Agent Skills.
---

# Hello World

Explain the basic concept of Agent Skills.

## Workflow

1. Explain what a Skill is.
2. Explain the role of SKILL.md.
3. Explain how a Skill is activated.
4. Provide a simple example.
```

### Step 3

验证：

~~~

uv tool install skills-ref
~~~
或者不安装
```bash
uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref skills-ref validate ./hello-world
```

如果验证成功：

```text
Skill
  ↓
SKILL.md
  ↓
AgentSkills validator
  ↓
Valid
```

然后把这个 Skill 放到一个支持 Agent Skills 的 Agent Runtime 中使用。

---

# 18. 最重要的几个概念

最后只需要记住这几个东西：

```text
Agent Skills
    =
一种标准化 Skill 格式

SKILL.md
    =
Skill 的核心文件

references/
    =
参考资料

scripts/
    =
可执行脚本

assets/
    =
静态资源

skills-ref
    =
参考工具 / Validator

Skill Creator
    =
帮助你生成 Skill 的工具

Agent Runtime
    =
真正发现、加载、执行 Skill 的 Agent
```

整个流程：

```text
                 Create
                   │
                   ↓
              SKILL.md
                   │
                   ↓
               Validate
                   │
                   ↓
          Agent Skills Standard
                   │
                   ↓
              Agent Runtime
                   │
          ┌────────┴────────┐
          ↓                 ↓
      Discovery         Activation
                            │
                            ↓
                        Execution
                            │
                ┌───────────┼───────────┐
                ↓           ↓           ↓
           references/   scripts/    assets/
```

**一句话：**

> `agentskills/agentskills` 解决的是“**Skill 应该如何定义和验证**”；`SKILL.md` 是你创建的 Skill；而真正运行 Skill 的，是支持 Agent Skills 的 Agent Runtime。**
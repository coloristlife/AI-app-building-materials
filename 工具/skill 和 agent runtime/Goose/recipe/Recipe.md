可以。下面我把它完全从你的 Security Review 项目中抽离出来，整理成一份**通用的 Goose Skill & Recipe User Guide**。它只讲 Goose 中 Skill、Recipe、Reference、Context、GUI 使用和常见问题，不绑定任何具体项目。

# Goose Skill & Recipe User Guide

## 1. Skill 和 Recipe 是什么？

在 Goose 中，可以把两者简单理解成：

|机制|核心作用|
|---|---|
|**Skill**|给 Agent 提供可复用的专业知识、行为指导和工作方法|
|**Recipe**|定义一个具体任务应该如何执行的 workflow|
|**Reference**|Skill / Recipe 可以读取的辅助资料|
|**Tool / Extension**|Agent 可以实际调用的外部能力|

一个简单的理解：

```text
Skill
  ↓
告诉 Agent：
“遇到这类任务应该怎么思考和处理”

Recipe
  ↓
告诉 Agent：
“这一次任务按照什么步骤执行”

Reference
  ↓
告诉 Agent：
“需要的详细资料在哪里”
```

---

# 2. Skill 不等于普通 Markdown

一个 Markdown 文件本身并不会自动成为 Skill。

Goose 会根据它的 **Skill discovery mechanism** 来识别 Skill。

典型的项目级结构是：

```text
project/
└── .goose/
    └── skills/
        └── my-skill/
            └── SKILL.md
```

因此：

```text
SKILL.md
```

不是因为“它是 Markdown”，而是因为：

> **它位于 Goose 认可的 Skill 目录结构中，并符合 Skill 的格式要求。**

所以不要简单理解成：

```text
任何 README.md
      ↓
Skill
```

而应该理解成：

```text
Goose Skill Discovery
        ↓
符合 Skill 目录 / 文件要求
        ↓
SKILL.md
        ↓
Skill
```

---

# 3. Skill 通常应该包含什么？

一个 Skill 通常可以包含：

```text
my-skill/
│
├── SKILL.md
│
├── references/
│   ├── guide.md
│   ├── examples.md
│   └── reference.md
│
└── ...
```

其中：

```text
SKILL.md
```

负责：

- Skill 的 description
    
- 什么时候使用这个 Skill
    
- 如何使用这个 Skill
    
- 工作原则
    
- reasoning guidance
    
- 必要的 workflow guidance
    

而：

```text
references/
```

负责：

- 大型文档
    
- 详细规范
    
- 示例
    
- reference material
    

---

# 4. 不要把所有内容都塞进 SKILL.md

这是使用 Skill 时非常重要的原则。

不推荐：

```text
SKILL.md
│
├── 50 页说明
├── 100 个例子
├── 所有 reference
└── 所有 documentation
```

更推荐：

```text
SKILL.md
    │
    ├── Core instructions
    ├── Rules
    └── References
          │
          ├── detailed-guide.md
          ├── examples.md
          └── specification.md
```

原因是：

> Skill 的核心作用是给 Agent 提供**行为和方向**，而不是一次性把所有知识塞进 context。

---

# 5. Reference 的作用

Reference 是：

> **Agent 在执行任务时需要进一步读取的资料。**

例如：

```text
SKILL.md
    ↓
“需要了解 X 时，请参考 references/x.md”
```

然后：

```text
references/x.md
```

才包含详细内容。

这种设计可以减少初始 context。

---

# 6. Recipe 是什么？

Recipe 更像：

> **一个可以执行的任务模板 / workflow。**

例如：

```text
Recipe
│
├── Instructions
├── Parameters
├── Extensions
└── Sub-recipes
```

它适合：

- 重复执行的任务
    
- 多步骤 workflow
    
- 固定操作流程
    
- 特定任务模板
    
- Agent automation
    

例如一个通用 Recipe：

```text
Analyze document
       ↓
Extract information
       ↓
Validate
       ↓
Generate report
       ↓
Review result
```

---

# 7. Recipe 和 Skill 的关系

两者可以组合，但不是必须组合。

### 方案 A：只使用 Skill

```text
User
 ↓
Goose
 ↓
Skill
 ↓
Task
```

适合：

> 通用的专业能力。

---

### 方案 B：只使用 Recipe

```text
User
 ↓
Recipe
 ↓
Workflow
```

适合：

> 明确、固定、重复的任务流程。

---

### 方案 C：Recipe + Skill

```text
             Recipe
          How to execute
                │
                ↓
              Skill
          How to reason
                │
                ↓
              Agent
```

这是比较强大的组合。

---

# 8. Recipe 中的 `recipe_dir`

这是 Recipe 使用过程中非常有价值的机制。

Recipe 可以使用：

```text
{{ recipe_dir }}
```

表示：

> **当前 Recipe 所在的目录。**

例如：

```text
recipes/
└── document-analysis/
    │
    ├── recipe.yaml
    │
    └── references/
        ├── rules.md
        └── examples.md
```

Recipe 可以引用：

```yaml
instructions: |
  Read:
  {{ recipe_dir }}/references/rules.md

  Then review:
  {{ recipe_dir }}/references/examples.md
```

这样 Recipe 不需要依赖当前工作目录。

---

# 9. 推荐的 Recipe Package 结构

推荐：

```text
my-recipe/
│
├── recipe.yaml
│
└── references/
    ├── guide.md
    ├── examples.md
    └── data.md
```

这样：

```text
my-recipe/
```

本身就是一个完整的 Recipe package。

优点：

- 容易移动
    
- 容易复制
    
- 容易分享
    
- Reference 路径清晰
    
- 不容易出现跨目录引用错误
    

---

# 10. 为什么推荐 `{{ recipe_dir }}`？

不推荐：

```text
../../../../references/file.md
```

因为 Recipe 移动以后：

```text
../../../../
```

可能就失效。

推荐：

```text
{{ recipe_dir }}/references/file.md
```

这样 Recipe 和 References 的关系是稳定的：

```text
Recipe
  │
  └── references/
```

---

# 11. Recipe 和 Skill 的 References 不一定应该共享

可以共享，但不要默认这么做。

例如：

```text
Recipe
 └── references/

Skill
 └── references/
```

各自拥有自己的 references。

如果某个 reference 是：

> **Recipe 执行必需的资料**

最好放在 Recipe package 里。

如果某个 reference 是：

> **Skill 的长期专业知识**

最好放在 Skill 里。

---

# 12. Goose GUI 中使用 Skill

如果你使用 Goose Desktop，而不是 CLI：

一般流程是：

```text
Open Goose
    ↓
Create / Open Session
    ↓
Select / configure working directory
    ↓
Goose discovers available Skills
    ↓
Agent can use relevant Skill
```

需要注意：

> **“Skill 文件存在”不等于“当前 Agent 一定正在使用它”。**

Skill 通常是通过 discovery / relevance mechanism 被发现和加载的。

---

# 13. Goose GUI 中使用 Recipe

Recipe 和普通 Chat Session 是两个不同概念。

不要认为：

```text
New Chat
```

就等于：

```text
Execute Recipe
```

Recipe 是一个 workflow。

如果你的 Goose Desktop 版本提供 Recipe / workflow 的 GUI 入口，可以通过该入口选择和运行 Recipe。

如果当前 GUI 版本没有对应入口，则不能简单地认为：

> “把 YAML 放在那里，Goose 就一定自动执行。”

这是非常重要的区别。

---

# 14. Recipe 是否需要 Description？

Recipe 本身通常有自己的 metadata，例如：

```yaml
title: "Document Analysis"

description: >
  Analyze a document and generate a structured report.
```

Description 的一个重要用途是：

> **帮助人和 Agent 理解这个 Recipe 是干什么的。**

但不要把：

```text
description
```

理解成：

> “只要有 description，Goose 就一定会执行这个 Recipe。”

**Discovery 和 execution 是两个不同的问题。**

---

# 15. Skill Discovery 和 Skill Execution 也是两个不同的问题

这是 Goose 使用中非常容易混淆的地方。

```text
Skill Discovery
      ↓
Goose 找到了 Skill
      ↓
Skill Activation / Loading
      ↓
Skill 内容进入 Agent context
      ↓
Agent 使用 Skill
```

所以如果 Agent 没按照 Skill 工作，需要区分：

```text
Skill 根本没发现？
```

还是：

```text
Skill 发现了，但是没有激活？
```

还是：

```text
Skill 加载了，但是 Agent 没有遵循？
```

---

# 16. 为什么 Agent 有时候不按照 Skill 做？

常见原因包括：

### ① Skill 没有被发现

例如：

```text
SKILL.md
```

放到了 Goose 不扫描的位置。

---

### ② Skill 没有被激活

虽然 Goose 知道这个 Skill 存在，但当前任务没有触发它。

---

### ③ Skill 的 description 不够明确

例如：

```yaml
description: >
  Helps with documents.
```

太宽泛。

更好的：

```yaml
description: >
  Analyze technical architecture documents and identify
  security risks, trust boundaries, and security controls.
```

---

### ④ Skill 的 instructions 不够明确

例如：

```text
Analyze the document carefully.
```

通常不够。

更明确：

```text
First identify the system components.

Then identify applicable domains.

Then evaluate the relevant risks.

Do not generate the final report before completing
all three steps.
```

---

### ⑤ Agent 自己认为可以直接回答

这是最重要的一类。

LLM 本身是 probabilistic system。

所以：

```text
Skill says:
Step 1 → Step 2 → Step 3
```

不意味着：

```text
Agent 100% 必须执行 Step 1 → Step 2 → Step 3
```

除非 workflow / runtime 层面提供更强的约束。

---

# 17. Skill ≠ deterministic workflow

这是使用 Agent Skill 时必须理解的核心概念：

```text
Skill
    ↓
Guidance
    ↓
LLM
    ↓
Probabilistic behavior
```

而 Recipe 更接近：

```text
Recipe
    ↓
Workflow
    ↓
Agent execution
```

但即使 Recipe 中有 instructions，LLM 的最终行为仍然不是传统程序意义上的：

```text
if A:
    execute B
```

因此：

> **如果某一步必须 100% 执行，就不要只依赖自然语言 Skill。**

---

# 18. 如果必须强制执行怎么办？

可以从弱约束逐渐增加到强约束：

```text
Level 1
Skill instructions

        ↓

Level 2
Recipe workflow

        ↓

Level 3
Tool / Extension

        ↓

Level 4
Programmatic validation

        ↓

Level 5
Deterministic state machine
```

例如：

```text
Step 1
Extract

↓

Program validates output

↓

Step 2
Transform

↓

Program validates output

↓

Step 3
Generate
```

这样就不再完全依赖 LLM 自己遵循 instruction。

---

# 19. 一个非常实用的 Debug 方法

当你发现：

> “Goose 为什么没有按照我的 Skill 做？”

不要立即修改 Skill。

按照下面顺序检查：

```text
① Skill 是否被 Discovery？

        ↓

② Skill 是否被 Activated？

        ↓

③ Skill 是否被 Loaded？

        ↓

④ Reference 是否被读取？

        ↓

⑤ Agent 是否理解 Instruction？

        ↓

⑥ Agent 是否按照 Instruction 执行？
```

这是比不断修改 Prompt 更有效的 debugging strategy。

---

# 20. Skill 和 Recipe 都不要承担 Tool 的职责

Skill：

```text
告诉 Agent 怎么做
```

Recipe：

```text
告诉 Agent 按什么 workflow 做
```

Tool：

```text
真正执行操作
```

例如：

```text
Skill
“检查这个 API 的安全性”

↓

Recipe
“先分析 → 再检查 → 再报告”

↓

Tool
“读取文件 / 查询数据库 / 执行命令”
```

这三个层次不要混在一起。

---

# 21. Context 管理原则

不要把所有资料一次性放进 Agent context。

不推荐：

```text
所有 documentation
所有 examples
所有 database
所有 catalog
所有 rules
        ↓
      Context
```

推荐：

```text
Core instructions
       ↓
Relevant index
       ↓
Relevant reference
       ↓
Detailed knowledge
```

即：

> **Progressive Disclosure / Progressive Loading**

先给 Agent 足够的信息决定“应该看什么”，再加载具体内容。

---

# 22. 一个通用的 Skill 结构

```text
my-skill/
│
├── SKILL.md
│
└── references/
    │
    ├── guide.md
    ├── examples.md
    └── detailed-reference.md
```

---

# 23. 一个通用的 Recipe 结构

```text
my-recipe/
│
├── recipe.yaml
│
└── references/
    │
    ├── instructions.md
    ├── examples.md
    └── reference.md
```

Recipe 中：

```yaml
instructions: |
  Follow the workflow below.

  Read:
  {{ recipe_dir }}/references/instructions.md

  Use:
  {{ recipe_dir }}/references/reference.md
```

---

# 24. 最佳实践 Checklist

### Skill

-  放在 Goose 支持的 Skill discovery location
    
-  使用正确的 `SKILL.md`
    
-  Description 清楚说明适用场景
    
-  不要把所有 reference 都塞进 SKILL.md
    
-  Instructions 清晰、具体
    
-  明确什么时候应该使用 Skill
    
-  明确什么时候不能使用 Skill
    

### Recipe

-  Recipe 有明确的 purpose
    
-  workflow 步骤清楚
    
-  使用 `{{ recipe_dir }}` 引用 companion files
    
-  Recipe 所需 References 尽量放在 Recipe package 内
    
-  不依赖脆弱的 `../../..` 路径
    
-  区分 discovery 和 execution
    

### References

-  只放需要的资料
    
-  避免一次性加载全部资料
    
-  大型资料拆分
    
-  建立清晰的 index
    
-  让 Agent 能够从 index 找到具体 reference
    

### Debugging

-  Skill 是否被发现？
    
-  是否被激活？
    
-  是否被加载？
    
-  Reference 是否能访问？
    
-  Recipe 是否真正执行？
    
-  Agent 是否遵循 instructions？
    
-  必须 deterministic 的步骤是否应该交给程序？
    

---

# 25. 最后形成一个简单心智模型

以后你看到 Goose 的这些东西，可以直接这样理解：

```text
                 GOOSE
                   │
       ┌───────────┼───────────┐
       │           │           │
     Skill       Recipe       Tool
       │           │           │
       ↓           ↓           ↓
  How to think  How to run  How to act
       │           │           │
       └───────────┼───────────┘
                   ↓
                 Agent
                   │
                   ↓
                Context
                   │
             ┌─────┴─────┐
             ↓           ↓
         References   User Input
```

最核心的三个原则就是：

> **Skill 提供能力和指导。**

> **Recipe 提供任务流程。**

> **Tool 提供实际执行能力。**

而：

> **Reference 是给 Skill / Recipe / Agent 提供额外知识的，不等于 Skill 本身。**
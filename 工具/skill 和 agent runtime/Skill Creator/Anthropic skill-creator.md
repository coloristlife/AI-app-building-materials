---
内容生成: AI
---

如果你指的是 **Anthropic `skill-creator`**，那么它非常适合我们现在这个阶段：**只负责把你的 Security Architecture use case 快速变成一个初版 Skill，不涉及后面的 validation / optimization。** 官方的 skill-creator 本身就是通过 Q&A 引导你创建 `SKILL.md`。([AgenticSkills](https://agenticskills.io/skills/skill-creator?utm_source=chatgpt.com "Skill Creator — AI Agent Skill by Anthropic | AgenticSkills"))

## 我建议你这样使用

### 1. 安装 Skill Creator

如果你使用 Claude Code / 支持 Agent Skills 的环境，可以直接：

[Anthropic Skills Repository](https://github.com/anthropics/skills?utm_source=chatgpt.com)

然后安装：

```bash
npx skills add anthropics/skills/skill-creator
```

这个 skill 的核心工作流就是：

```text
Describe use case
       ↓
Skill Creator asks questions
       ↓
Define purpose / triggers / workflow
       ↓
Generate SKILL.md
       ↓
Generate supporting files
```

官方 Skill Creator 目前明确定位为“创建新的 skills，并帮助迭代已有 skills”。([AgenticSkills](https://agenticskills.io/skills/skill-creator?utm_source=chatgpt.com "Skill Creator — AI Agent Skill by Anthropic | AgenticSkills"))

---

# 2. 不要一上来就让它“创建 Security Skill”

这一点很重要。

我们现在已经有一个比较复杂的 use case：

```text
System Architecture
        ↓
Security Concerns
        ↓
Security Requirements
        ↓
Security Controls
```

如果你直接告诉它：

> Create a security analysis skill.

它很可能给你生成一个比较 generic 的：

```text
Analyze architecture
Identify threats
Recommend mitigations
```

这种 Skill **不是我们要的**。

我们应该把我们已经讨论过的 architecture 直接提供给它。

---

# 3. 第一轮 Prompt

你可以直接把下面这个 prompt 交给 Skill Creator：

```text
I want to create a reusable Agent Skill for security architecture analysis.

The primary purpose of this skill is to analyze a software system or
architecture description and identify relevant security concerns.

The skill should establish a hierarchical mapping:

System / Architecture
        ↓
Security Concern
        ↓
Security Requirement
        ↓
Security Control

The skill should not simply generate a generic security checklist.

Instead, it should reason from the characteristics of the system,
identify applicable security concerns, and then map each concern to
appropriate security requirements and security controls.

The skill will eventually be used by an agent runtime such as Goose.

The security knowledge should be maintained separately from the
SKILL.md itself. The SKILL.md should contain the reasoning workflow,
decision logic, and instructions for how the agent should use the
security knowledge.

The initial version should focus on:
1. Understanding the system architecture.
2. Identifying relevant security concerns.
3. Mapping security concerns to security requirements.
4. Mapping requirements to security controls.
5. Producing a structured security analysis.

Do not design the evaluation, validation, or optimization process yet.
Focus only on creating the initial skill.
```

这个 prompt 的目的不是让它一次性写完。

而是告诉它：

> **“这是我要解决的问题，你负责把它转化成 Skill。”**

---

# 4. 然后让 Skill Creator 问你问题

Anthropic 的 Skill Creator 本身就是一个 interactive Q&A workflow。([AgenticSkills](https://agenticskills.io/skills/skill-creator?utm_source=chatgpt.com "Skill Creator — AI Agent Skill by Anthropic | AgenticSkills"))

它很可能会继续问：

```text
What inputs does the skill receive?
```

这时候你可以回答：

```text
The input can be a system architecture description.

It may include:
- natural language architecture descriptions
- architecture diagrams
- component descriptions
- data flows
- APIs
- deployment information
- authentication mechanisms
- external integrations
- cloud services
- infrastructure descriptions
```

---

它可能继续问：

```text
What should the output look like?
```

回答：

```text
The output should be structured around:

1. System Component
2. Security Concern
3. Security Requirement
4. Security Control
5. Rationale
6. Evidence from the architecture

The result should make the relationship between these levels explicit.
```

这样它就不会生成一个普通的 security checklist。

---

# 5. 最关键的问题：Knowledge 怎么处理

它很可能会问：

> What references or knowledge should the skill use?

这里我建议你明确告诉它：

```text
The security knowledge should NOT be hardcoded into SKILL.md.

The skill should be designed so that the knowledge can be provided
through external reference files.

The initial knowledge model should support relationships such as:

Security Concern
    ↓
Security Requirement
    ↓
Security Control

The knowledge base may later contain mappings based on security
frameworks such as NIST SP 800-53, OWASP ASVS, and internal security
requirements.

For now, create the skill structure so that these references can be
added separately.
```

这一步非常重要。

因为我们真正要做的不是：

```text
SKILL.md = Security Knowledge Base
```

而是：

```text
SKILL.md
    │
    │ instructions / reasoning
    ↓
Security Knowledge
    │
    ├── concerns
    ├── requirements
    └── controls
```

这和我们之前讨论的 **Security Architecture Library** 是一致的。

---

# 6. 最后让它生成

最终我们希望得到类似：

```text
security-architecture-analysis/
│
├── SKILL.md
│
└── references/
    ├── security-concerns.md
    ├── security-requirements.md
    └── security-controls.md
```

不过这里**不要强迫它现在就生成完整 Knowledge Base**。

第一版甚至可以只有：

```text
security-architecture-analysis/
│
├── SKILL.md
└── references/
```

然后我们自己设计 Knowledge Model。

---

# 7. 你最终应该得到什么

我们的目标不是“生成一个很长的 SKILL.md”。

目标应该是：

```text
SKILL.md
```

里面定义：

```text
WHEN TO USE
     ↓
UNDERSTAND ARCHITECTURE
     ↓
EXTRACT COMPONENTS
     ↓
IDENTIFY SECURITY-RELEVANT CHARACTERISTICS
     ↓
IDENTIFY SECURITY CONCERNS
     ↓
MAP TO REQUIREMENTS
     ↓
MAP TO CONTROLS
     ↓
GENERATE STRUCTURED RESULT
```

而不是：

```text
SKILL.md
    ↓
包含 5000 条 security rules
```

这就是 **Skill = reasoning/workflow，Knowledge Base = domain knowledge** 的分离。

---

## 8. 我们现在实际上可以非常快地推进

你现在甚至**不用搭我们的 Skill Platform**。

先：

```text
Anthropic Skill Creator
        ↓
Security Architecture Skill
        ↓
SKILL.md
        ↓
把 SKILL.md 给我
```

然后我们一起检查：

```text
Skill
 ├── Purpose
 ├── Trigger
 ├── Workflow
 ├── Reasoning
 ├── Output
 └── Knowledge Interface
```

如果这个结构符合我们的设计，再把它放进：

```text
                    Skill Platform
                          │
                    ┌─────┴─────┐
                    ↓           ↓
                  Skill       Runtime
                    │           │
                    ↓           ↓
                 SKILL.md     Goose
```

**所以现在最合理的下一步不是写代码，而是先用 `skill-creator` 把第一个 `security-architecture-analysis` Skill 生出来。**

另外，如果你说的 **AnswerPick** 确实是另一个具体工具，把它的链接给我；我可以直接按照它的实际 UI/CLI，给你写一份从 **安装 → 输入 use case → 回答问题 → 生成 SKILL.md → 导入 Goose** 的完整操作指南。
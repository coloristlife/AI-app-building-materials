下面我直接把我们刚才关于 **Goose Skill 为什么没有被使用、Skill 如何激活、如何判断是否真的加载、为什么 AI 会跳过 Skill、如何提高可靠性，以及什么时候需要 Tool / Workflow** 的内容整理成一份完整的 **User Guide**。

# Goose Skill Activation & Execution User Guide

## 1. 目的

本文解决一个核心问题：

> **为什么 Goose 有时候没有按照我们设计的 Skill 执行任务？**

尤其针对 Security Review 场景，我们需要区分：

```text
Skill 有没有被发现？
        ↓
Skill 有没有被激活？
        ↓
SKILL.md 有没有进入 AI Context？
        ↓
Reference / Knowledge Base 有没有被读取？
        ↓
AI 有没有遵循 Skill？
```

这几个问题实际上是完全不同的。

---

# 2. 最重要的认知：Skill 不是 Workflow

首先要明确：

> **Skill 是给 Agent 的指导（Guidance），而不是一个强制执行的程序（Program）。**

例如我们写：

```text
Step 1: Identify Domain
Step 2: Identify Component
Step 3: Identify Concern
Step 4: Retrieve Requirement
Step 5: Generate Questionnaire
```

并不意味着 Goose 一定执行：

```text
1 → 2 → 3 → 4 → 5
```

因为 Goose 本质上还是 Agent。

LLM 会根据：

- 用户请求
    
- 当前 Context
    
- Skill
    
- Tools
    
- 自己的推理
    

决定下一步做什么。

因此它可能认为：

> “我已经知道这个系统涉及 Authentication 和 Authorization，可以直接回答。”

于是：

```text
User
 ↓
Goose
 ↓
LLM
 ↓
直接回答
```

而不是：

```text
User
 ↓
Skill
 ↓
Domain
 ↓
Component
 ↓
Concern
 ↓
Requirement
 ↓
Question
```

---

# 3. 五层 Skill Execution Model

我们以后分析任何 Skill 问题，都应该按照下面五层来排查。

```text
                Skill System
                     │
                     ↓
            ① Skill Discovery
                     │
                     ↓
            ② Skill Activation
                     │
                     ↓
          ③ Skill Content Loading
                     │
                     ↓
       ④ Supporting File Retrieval
                     │
                     ↓
            ⑤ Skill Compliance
```

---

## 3.1 Skill Discovery

问题：

> Goose 能不能发现这个 Skill？

例如：

```text
security-review/
└── SKILL.md
```

如果 Goose 根本没有发现这个目录，那么后面全部不用讨论。

---

## 3.2 Skill Activation

问题：

> Goose 发现 Skill 后，当前用户任务是否触发了这个 Skill？

例如：

用户：

> Please perform a security review of this architecture.

系统可能判断：

```text
security-review
        ↑
     relevant
```

于是激活。

但如果用户说：

> Can you summarize this architecture?

Agent 可能认为：

```text
security-review
        ↑
not necessary
```

于是没有激活。

---

## 3.3 Skill Content Loading

即使 Skill 被发现和激活，还要问：

> **完整的 `SKILL.md` 有没有真正进入模型可见 Context？**

这是非常重要的区别。

```text
Skill exists
      ↓
Skill activated
      ↓
SKILL.md loaded
      ↓
AI can see instructions
```

---

## 3.4 Supporting File Retrieval

即使 AI 看到了：

```text
SKILL.md
```

也不代表它已经看到了：

```text
references/
knowledge-base/
```

例如：

```text
SKILL.md
   ↓
“Read component-index.md”
```

不代表：

```text
component-index.md
```

真的已经被读取。

所以需要单独验证：

```text
SKILL.md
   ↓
Reference retrieval
   ↓
Knowledge Base retrieval
```

---

## 3.5 Skill Compliance

最后才是：

> AI 看到了 Skill，但是有没有按照 Skill 做？

这是最容易混淆的问题。

可能出现：

```text
Skill loaded
     ↓
AI understands it
     ↓
AI decides:
“I already know the answer.”
     ↓
Skip KB
```

所以：

> **Skill loaded ≠ Skill followed**

---

# 4. 为什么 AI 会跳过 Skill？

最常见的原因是：

## 原因一：模型已经知道答案

例如：

```text
User:

We use AWS API Gateway and OAuth2.
```

模型本身就知道：

```text
API Gateway → API Security
OAuth2 → Authentication
```

于是可能直接回答。

---

## 原因二：Skill 的 Instruction 太“软”

例如：

```markdown
Read the component index.

Then identify the relevant components.
```

对 LLM 来说更像：

> 建议这么做。

而不是：

> 不做这一步就不能继续。

---

## 原因三：Skill 没有真正被激活

这时候你再怎么修改 Skill 都没有意义。

---

## 原因四：Reference 文件没有被自动读取

例如 Skill 说：

```text
Read:
knowledge-base/components/api-gateway.md
```

但 Agent 没有调用任何文件读取能力。

---

# 5. 第一原则：先证明 Skill 被激活

不要直接测试完整 Security Review。

首先建立一个极小的测试 Skill：

```text
skill-loading-test/
└── SKILL.md
```

内容：

```markdown
---
name: skill-loading-test
description: >
  Use this skill whenever the user asks to test
  whether a Goose skill has been activated.
---

# Skill Loading Test

When this skill is activated, you MUST begin your response with:

SKILL_ACTIVATED_73921

Then say:

"The Skill Loading Test was activated."
```

然后给 Goose：

```text
Test whether my skill system is working.
```

如果输出：

```text
SKILL_ACTIVATED_73921

The Skill Loading Test was activated.
```

说明至少可以确认：

```text
Skill
 ↓
Activation
 ↓
Instruction
 ↓
AI
```

这条链路基本成立。

---

# 6. 为什么要使用随机 Marker？

不要使用：

```text
SKILL_LOADED
```

因为模型可能自己猜出来。

应该使用：

```text
SKILL_ACTIVATED_73921
```

或者：

```text
SECURITY_REVIEW_ACTIVATION_7F92K
```

这种没有语义意义的随机 token。

这样可以更有效地证明：

> **模型确实看到了 Skill 内容。**

---

# 7. 第二个测试：验证 Knowledge Base 是否真的被读取

这一步非常重要。

例如：

```text
knowledge-base/components/api-gateway.md
```

里面放：

```yaml
test_marker: COMPONENT_API_GATEWAY_47291
```

然后 Skill 要求：

```text
Before analyzing API Gateway,
retrieve the canonical API Gateway component file.
```

然后观察 Goose 的 execution/tool trace。

如果看到：

```text
load api-gateway.md
        ↓
COMPONENT_API_GATEWAY_47291
```

才说明：

> 不仅 Skill 被加载了，而且 supporting knowledge 也被读取了。

---

# 8. Skill 的 Description 非常重要

Skill frontmatter：

```yaml
---
name: security-review
description: >
  Use this skill whenever the user asks to perform a security review,
  security architecture review, security concern identification,
  security control assessment, or security questionnaire generation
  for a system, application, service, API, infrastructure, or component.
---
```

Description 应该回答：

> **什么时候应该使用这个 Skill？**

而不是只回答：

> 这个 Skill 是干什么的。

---

# 9. Security Review Skill 推荐的 Description

我建议最终使用类似：

```yaml
---
name: security-review
description: >
  Use this skill whenever the user asks to perform a security review,
  security architecture review, security concern identification,
  security control assessment, or security questionnaire generation
  for a system, application, service, API, infrastructure, or component.
---
```

这样：

```text
User request
     ↓
Semantic relevance
     ↓
security-review
```

会更加明确。

---

# 10. 不要把所有事情都交给 Skill

这是我们讨论后最重要的架构结论之一。

应该划分成：

```text
AI / Probabilistic
        │
        ├── System Understanding
        ├── Component Extraction
        ├── Semantic Matching
        ├── Concern Applicability
        └── Evidence Extraction

Program / Deterministic
        │
        ├── File Loading
        ├── Canonical ID Resolution
        ├── Link Resolution
        ├── Requirement Retrieval
        ├── Question Retrieval
        └── Schema Validation
```

---

# 11. Security Review 的正确职责划分

## AI 负责

### System Understanding

从：

```text
用户提供的系统描述
```

理解：

```text
API
Database
User
Authentication
Cloud Service
Data
Component
```

---

### Component Extraction

例如：

```text
“We expose our API through AWS API Gateway.”
```

AI 提取：

```text
AWS API Gateway
```

---

### Semantic Candidate Generation

例如：

```text
“Lambda”
```

可能对应：

```text
AWS Lambda
```

---

### Concern Applicability

例如：

```text
Authentication
```

AI 根据系统上下文判断：

```text
Applicable
```

---

### Evidence Extraction

例如用户说：

> OAuth2 is used for authentication.

AI 提取：

```text
Authentication mechanism:
OAuth2
```

---

# 12. 程序负责什么？

程序负责：

```text
“这个东西到底是不是 Knowledge Base 中存在的实体？”
```

例如：

```text
AI:

AWS API Gateway

        ↓

resolve_component()

        ↓

COMPONENT-API-GATEWAY
```

程序不能让 AI 凭空创建：

```text
COMPONENT-AWS-API-GATEWAY-SECURE
```

---

# 13. 为什么 Tool 比单纯 Skill Instruction 更可靠？

Skill：

```text
Please read the component index.
```

AI 可以跳过。

Tool：

```text
resolve_component("AWS API Gateway")
```

返回：

```json
{
  "id": "COMPONENT-API-GATEWAY",
  "name": "API Gateway",
  "file": "knowledge-base/components/api-gateway.md"
}
```

然后：

```text
load_component("COMPONENT-API-GATEWAY")
```

得到真正的 KB 内容。

这时候：

```text
AI
 ↓
提出候选
 ↓
Tool
 ↓
验证 canonical entity
 ↓
Knowledge Base
```

可靠性会高很多。

---

# 14. 你的 Security Review 推荐架构

最终建议：

```text
                         User
                           │
                           ↓
                         Goose
                           │
                           ↓
                  Security Review Skill
                           │
             ┌─────────────┴─────────────┐
             ↓                           ↓
        AI Reasoning                  KB Tools
             │                           │
             │                  ┌────────┼────────┐
             │                  ↓        ↓        ↓
             │              Component Concern Requirement
             │              Resolver   Loader    Loader
             │
             ├── System Understanding
             ├── Component Extraction
             ├── Semantic Matching
             ├── Concern Applicability
             └── Evidence Extraction
                           │
                           ↓
                    Questionnaire
```

---

# 15. 如果真的需要“强制执行”怎么办？

这时候不要继续往 `SKILL.md` 里面堆：

```text
MUST
MUST
MUST
MUST
```

因为它最终还是 Instruction。

如果需要真正强制：

```text
Step 1
 ↓
Step 2
 ↓
Step 3
 ↓
Step 4
```

需要 Workflow / Recipe / Controller。

例如状态：

```text
START
 ↓
SYSTEM_ANALYZED
 ↓
COMPONENTS_IDENTIFIED
 ↓
CONCERNS_IDENTIFIED
 ↓
APPLICABILITY_CHECKED
 ↓
REQUIREMENTS_RETRIEVED
 ↓
QUESTIONS_RETRIEVED
 ↓
COMPLETE
```

如果 Agent 在：

```text
CONCERNS_IDENTIFIED
```

就想直接输出最终 Questionnaire：

```text
Controller
   ↓
Reject
   ↓
继续完成下一步
```

这才是真正的 enforcement。

---

# 16. Skill / Tool / Workflow 的最终区别

可以记成这一张表：

|机制|主要作用|是否强制|
|---|---|---|
|Skill|告诉 AI 应该如何工作|❌|
|AI Reasoning|理解、判断、推理|❌|
|Tool|提供确定性的能力和数据|部分|
|Knowledge Base|权威知识来源|数据层|
|Workflow / Recipe|控制执行流程|✅|
|Program / Controller|强制状态和规则|✅|

因此：

> **不要试图让 Skill 变成程序。**

---

# 17. 最容易犯的错误

## 错误 1

```text
SKILL.md
↓
写 100 个步骤
```

认为这样 AI 就一定执行。

**不一定。**

---

## 错误 2

```text
Skill
↓
告诉 AI：
“去读取整个 Knowledge Base”
```

这样很容易产生：

```text
Context explosion
```

应该 Progressive Loading。

---

## 错误 3

让 AI 自己决定 canonical entity：

```text
AI → Component Name
```

应该：

```text
AI → Candidate
       ↓
Resolver
       ↓
Canonical Component
```

---

## 错误 4

只看最终答案判断 Skill 有没有工作。

这是非常危险的。

因为：

```text
正确答案
```

不代表：

```text
正确执行过程
```

AI 可能完全没有读取你的 KB。

---

# 18. 正确的测试方法

必须逐层测试。

### Test 1

```text
Skill Discovery
```

Goose 能否找到 Skill？

---

### Test 2

```text
Skill Activation
```

是否出现随机 activation marker？

---

### Test 3

```text
Skill Content Loading
```

AI 是否知道 Skill 中的特殊 instruction？

---

### Test 4

```text
Supporting File Retrieval
```

是否真正读取了指定 KB 文件？

---

### Test 5

```text
Canonical Resolution
```

AI 提取：

```text
AWS API Gateway
```

程序是否返回：

```text
COMPONENT-API-GATEWAY
```

---

### Test 6

```text
Concern Applicability
```

AI 是否基于 KB + system evidence 判断 applicability？

---

### Test 7

```text
Requirement Retrieval
```

是否只读取 applicable concern 对应的 requirements？

---

### Test 8

```text
Questionnaire Generation
```

最终 Questionnaire 是否完全可追溯到：

```text
System Evidence
 ↓
Component
 ↓
Concern
 ↓
Requirement
 ↓
Question
```

---

# 19. 最终推荐的 Debugging 顺序

以后遇到：

> “Goose 没按照我的 Skill 做。”

**不要立即修改 Skill。**

按照下面顺序：

```text
① Skill 是否被发现？
        ↓
② Skill 是否被激活？
        ↓
③ SKILL.md 是否进入 Context？
        ↓
④ Reference 是否被读取？
        ↓
⑤ Knowledge Base 是否被读取？
        ↓
⑥ AI 是否遵守 Skill？
        ↓
⑦ 是否需要 Tool？
        ↓
⑧ 是否需要 Workflow / Controller？
```

这个顺序非常重要。

---

# 20. 针对你这个 Security Review 项目的最终原则

我们目前可以把整个设计浓缩成下面这几句话：

> **Skill 是 Guidance，不是 Workflow。**

> **AI 负责理解和推理，不负责充当 Knowledge Base。**

> **Knowledge Base 是 authoritative source。**

> **Tool 负责确定性的检索和 canonical resolution。**

> **AI 负责 probabilistic 的 semantic matching 和 applicability。**

> **如果必须强制执行顺序，就使用 Workflow / Recipe / Controller，而不是继续增加 SKILL.md 的指令。**

最终：

```text
                SECURITY REVIEW
                       │
             ┌─────────┴─────────┐
             ↓                   ↓
        AI Reasoning        Deterministic Tools
             │                   │
     ┌───────┼───────┐      ┌────┼────┐
     ↓       ↓       ↓      ↓    ↓    ↓
 System   Semantic  Evidence Resolve Load
Understand Match    Extract  Entity  KB
     │       │       │
     └───────┼───────┘
             ↓
       Concern Applicability
             │
             ↓
       Requirement Retrieval
             │
             ↓
       Questionnaire
```

**最关键的工程原则就是：**

> **不要只验证“答案对不对”，还要验证“Skill 有没有被激活、Knowledge Base 有没有被读取、canonical entity 有没有经过验证，以及最终结果是不是沿着规定的知识链产生的”。**

这会成为你后面设计 Security Review Skill/KB/Goose 集成时的核心 User Guide。
我们现在先不要把它设计成一个“大而全的平台”，而是**沿着一条完整的 Security Review happy path**，把 Goose 真正执行时需要看到的文件全部串起来。

我建议这一版只实现：

> **System Description → Domain → Component → Concern → Requirement → Questionnaire**

先不加入 Evidence Extraction、Vector DB、复杂 Retrieval。

---

# 一、先看完整的目录

我建议把 **Skill 和 Knowledge Base 分开**：

```text
security-review/
│
├── SKILL.md
│
├── references/
│   ├── domain-index.md
│   └── component-index.md
│
└── knowledge-base/
    │
    ├── domains/
    │   └── application-security.md
    │
    ├── components/
    │   └── api-gateway.md
    │
    ├── concerns/
    │   └── api-security.md
    │
    ├── requirements/
    │   └── api-authentication.md
    │
    └── questions/
        ├── api-authentication-q01.md
        └── api-authentication-q02.md
```

这一条链就是：

```text
SKILL.md
   ↓
domain-index.md
   ↓
application-security.md
   ↓
api-security.md
   ↓
api-authentication.md
   ↓
api-authentication-q01.md
api-authentication-q02.md
```

另外 Component 是一条并行路径：

```text
component-index.md
   ↓
api-gateway.md
   ↓
api-security.md
```

最终两条路径汇合：

```text
Domain
   ↓
Concern
   ↑
Component
```

---

# 二、完整 `SKILL.md`

下面这个就是我认为可以真正放进 Goose 里面测试的第一版。

```markdown
---
name: security-review
description: >
  Analyze a system description, identify relevant security domains
  and canonical components, determine applicable security concerns,
  retrieve their security requirements, and generate a focused
  security questionnaire.
---

# Security Review Skill

## 1. Objective

Perform a structured security review of a system described by the user.

The goal is to:

1. Understand the system.
2. Identify relevant Security Domains.
3. Identify canonical Components from the Component Knowledge Base.
4. Identify applicable Security Concerns.
5. Retrieve Security Requirements associated with those concerns.
6. Generate a focused Security Questionnaire.

The Security Knowledge Base is the source of truth.

Do not invent Components, Security Concerns, Requirements, or Questions
that do not exist in the Knowledge Base.

---

# 2. Knowledge Base Structure

The Security Knowledge Base is located under:

knowledge-base/

Its structure is:

knowledge-base/
├── domains/
├── components/
├── concerns/
├── requirements/
└── questions/

The Skill also contains lightweight indexes:

references/
├── domain-index.md
└── component-index.md

The indexes are used only for initial candidate discovery.

Do not load the entire Knowledge Base into context.

---

# 3. Knowledge Loading Policy

Use progressive loading.

Do NOT:

- Load the entire Knowledge Base at the beginning.
- Load every Domain.
- Load every Component.
- Load every Security Concern.
- Invent new Knowledge Base objects.

DO:

1. Use the Domain Index to identify candidate Domains.
2. Load only the selected Domain files.
3. Use the Component Index to identify candidate Components.
4. Load only the selected Component files.
5. Use Domain files to obtain candidate Security Concerns.
6. Use Component files to obtain predefined Security Concerns.
7. Determine which candidate Concerns are applicable.
8. Load full Concern files only for applicable Concerns.
9. Load Requirements only from applicable Concerns.
10. Load Questions only from selected Requirements.

---

# 4. Step 1 — Understand the System

Analyze the system description provided by the user.

Extract relevant facts such as:

- System purpose
- Major functions
- Users
- External actors
- APIs
- Data
- Sensitive data
- Authentication mechanisms
- Authorization mechanisms
- Cloud/platform technologies
- Databases
- Infrastructure
- External services
- Communication channels
- Deployment architecture

Do not yet make final Security Concern decisions.

Create an internal System Understanding summary.

Example:

System:

- Customer-facing REST API
- Hosted on AWS
- API Gateway exposes the API
- Lambda performs backend processing
- DynamoDB stores customer data
- OAuth2 is used for authentication

---

# 5. Step 2 — Identify Security Domains

Read:

references/domain-index.md

The Domain Index contains the complete list of available
Security Domains.

Select all Domains that are relevant to the system.

Do not invent Domains.

For each selected Domain, record a short reason based on
evidence from the system description.

Example:

Identity & Access
Reason:
The system exposes APIs and uses OAuth2 authentication.

Data Security
Reason:
The system stores customer data.

Application Security
Reason:
The system exposes a customer-facing API.

---

# 6. Step 3 — Load Selected Domain Knowledge

For every selected Domain:

1. Locate its Domain Knowledge file under:

knowledge-base/domains/

2. Load that file.

3. Read its Security Concerns section.

The Domain file defines which Security Concerns belong
to that Domain.

Example:

knowledge-base/domains/application-security.md

may contain:

Security Concerns:

- [[api-security]]
- [[input-validation]]
- [[injection]]
- [[error-handling]]

Do not load unrelated Domain files.

---

# 7. Step 4 — Identify Components

Read:

references/component-index.md

Use the Component Index to map entities extracted
from the System Description to canonical Components.

Use:

- Name
- Alias
- Description
- Context

for matching.

Do not invent Components.

For every selected Component:

1. Load its Component Knowledge file from:

knowledge-base/components/

2. Read its Security Concerns section.

The Component Knowledge Base contains predefined
Component → Security Concern relationships.

Do NOT infer additional Component → Security Concern
relationships.

---

# 8. Step 5 — Build Candidate Security Concerns

Build the candidate Security Concern set from two sources.

## Source A — Domain-derived Concerns

For every selected Domain:

1. Read the Security Concerns listed in the Domain file.
2. Add them to the candidate set.

## Source B — Component-derived Concerns

For every selected Component:

1. Read its Security Concerns section.
2. Add those concerns to the candidate set.

Merge the two sets.

Remove duplicates.

Do not add Security Concerns that are not present
in either source.

---

# 9. Step 6 — Determine Security Concern Applicability

For every candidate Security Concern:

1. Load its Security Concern file from:

knowledge-base/concerns/

2. Read:

- Description
- Applicability
- Relevant system characteristics
- Any other applicability guidance

Determine whether the Security Concern is applicable
to the system.

For each applicable Concern, record:

- Concern ID
- Concern Name
- Source
- Evidence
- Reason

Possible sources:

- Domain
- Component
- Domain + Component

Do not select a Concern only because its name appears
similar to a word in the system description.

Use the Concern's applicability criteria and system evidence.

---

# 10. Step 7 — Retrieve Security Requirements

For every applicable Security Concern:

1. Read its Security Concern file.

2. Locate the Security Requirements section.

3. Resolve the linked Requirements.

4. Load the corresponding Requirement files from:

knowledge-base/requirements/

Do not retrieve Requirements unrelated to the selected Concerns.

---

# 11. Step 8 — Retrieve Questionnaire Questions

For every selected Security Requirement:

1. Read its Questionnaire section.

2. Resolve linked Questions.

3. Load the corresponding Question files from:

knowledge-base/questions/

Only include Questions associated with the selected
Security Requirements.

---

# 12. Step 9 — Generate Security Questionnaire

Generate a structured questionnaire.

Group Questions by:

Security Domain
  → Security Concern
    → Security Requirement
      → Question

For every Question include:

- Question ID
- Question
- Related Security Requirement
- Related Security Concern
- Evidence requested, if defined

Do not modify the meaning of the canonical Question.

---

# 13. Output Format

Return the following sections.

## System Understanding

Summarize the system.

## Identified Components

| Component | ID | Evidence |
|---|---|---|

## Relevant Security Domains

| Domain | ID | Reason |
|---|---|---|

## Applicable Security Concerns

| Concern | ID | Source | Evidence | Reason |
|---|---|---|---|---|

## Security Requirements

List the Requirements associated with
the applicable Security Concerns.

## Security Questionnaire

Group questions hierarchically:

Domain
→ Concern
→ Requirement
→ Question

---

# 14. Important Rules

### Canonical Knowledge

The Knowledge Base is authoritative.

Do not invent:

- Components
- Domains
- Security Concerns
- Requirements
- Questions

### Component Matching

When matching Components:

Prefer:

1. Exact canonical name
2. Alias
3. Strong semantic match supported by context

If confidence is insufficient, report the ambiguity.

### Security Concern Matching

A Security Concern must be supported by:

- Domain membership,
- Component relationship,
- and/or applicability criteria.

Do not select a Concern solely from keyword similarity.

### Progressive Loading

Only load Knowledge Base objects required
by the current analysis.

### Evidence

Every selected Domain and Security Concern should
be traceable to evidence from the user's system description.

### Traceability

Maintain the relationship:

System Evidence
→ Domain
→ Component / Concern
→ Requirement
→ Question
```

---

# 三、`references/domain-index.md`

这个文件非常轻。

**不是完整 Domain Knowledge。**

它只是告诉 AI：

> 我有哪些 Domain？

```markdown
# Security Domain Index

| ID | Name | Description |
|---|---|---|
| DOMAIN-IAM | Identity & Access | Identity, authentication and authorization |
| DOMAIN-APPSEC | Application Security | Security of application logic and interfaces |
| DOMAIN-DATA | Data Security | Protection of data throughout its lifecycle |
| DOMAIN-INFRA | Infrastructure Security | Security of infrastructure and compute environments |
| DOMAIN-NETWORK | Network Security | Network communication and segmentation |
| DOMAIN-MONITORING | Monitoring & Logging | Security logging, monitoring and detection |
```

例如 AI 第一步只需要看到：

```text
Identity & Access
Application Security
Data Security
Infrastructure Security
...
```

而不用加载：

```text
authentication.md
authorization.md
...
```

---

# 四、`references/component-index.md`

同样是轻量 Index。

```markdown
# Component Index

## API Gateway

ID: COMPONENT-API-GATEWAY

Aliases:
- API Gateway
- REST API Gateway
- AWS API Gateway
- Gateway API

Description:
Managed API gateway used to expose and route APIs.

---

## AWS Lambda

ID: COMPONENT-AWS-LAMBDA

Aliases:
- Lambda
- Lambda Function
- AWS Lambda

Description:
Serverless compute service provided by AWS.

---

## DynamoDB

ID: COMPONENT-DYNAMODB

Aliases:
- DynamoDB
- Dynamo
- AWS DynamoDB

Description:
Managed NoSQL database service provided by AWS.
```

这里的目的只有一个：

> **让 AI 把用户语言映射成 Canonical Component。**

---

# 五、然后是 Domain 文件

例如：

`knowledge-base/domains/application-security.md`

```markdown
---
id: DOMAIN-APPSEC
name: Application Security
type: security-domain
---

# Application Security

## Description

Security concerns related to the design,
implementation, and operation of applications
and application interfaces.

## Security Concerns

- [[api-security]]
- [[input-validation]]
- [[injection]]
- [[error-handling]]
```

注意这里非常重要：

**Domain 文件不复制 Concern 的 Description。**

它只维护：

```text
Application Security
        │
        ├── API Security
        ├── Input Validation
        ├── Injection
        └── Error Handling
```

---

# 六、Component 文件

例如：

`knowledge-base/components/api-gateway.md`

```markdown
---
id: COMPONENT-API-GATEWAY
name: API Gateway
type: infrastructure-component

aliases:
  - API Gateway
  - REST API Gateway
  - AWS API Gateway
---

# API Gateway

## Description

A managed service used to expose,
route, and manage APIs.

## Security Concerns

- [[api-security]]
- [[authentication]]
- [[authorization]]
- [[rate-limiting]]
- [[logging]]
```

这里就是你之前强调的：

> **Component 和它相关的 Security Concerns，在创建 Knowledge Base 的时候就已经建立好了。**

所以 Runtime 不需要再通过 AI 猜：

```text
API Gateway → API Security
```

而是直接读取这个关系。

---

# 七、Concern 文件

例如：

`knowledge-base/concerns/api-security.md`

```markdown
---
id: CONCERN-API-SECURITY
name: API Security
type: security-concern

aliases:
  - API Protection
  - API Security Controls
  - API Protection Controls
---

# API Security

## Description

Security controls protecting APIs from
unauthorized access, abuse, manipulation,
and unintended exposure.

## Applicability

This concern is applicable when:

- The system exposes APIs.
- External clients can invoke APIs.
- APIs expose sensitive or business-critical operations.
- API access requires security controls.

## Security Requirements

- [[api-authentication]]
- [[api-authorization]]
- [[api-input-validation]]

## Questionnaire

The questionnaire is derived from the
associated Security Requirements.
```

这个文件才是 AI 真正需要深入理解的 Concern Knowledge。

---

# 八、Requirement 文件

例如：

`knowledge-base/requirements/api-authentication.md`

```markdown
---
id: REQ-API-AUTHENTICATION
name: API Authentication
type: security-requirement
---

# API Authentication

## Requirement

All protected APIs must require appropriate
authentication before allowing access to
protected resources.

## Security Concern

[[api-security]]

## Questionnaire

- [[api-authentication-q01]]
- [[api-authentication-q02]]
```

---

# 九、Question 文件

例如：

`knowledge-base/questions/api-authentication-q01.md`

```markdown
---
id: Q-API-AUTH-001
type: security-question
---

# API Authentication Mechanism

## Question

How are clients authenticated before they
can access protected APIs?

## Evidence Requested

Please provide:

- Authentication mechanism
- Identity provider
- Token type
- Token validation mechanism
- Relevant architecture or configuration documentation

## Related Requirement

[[api-authentication]]
```

第二个：

`api-authentication-q02.md`

```markdown
---
id: Q-API-AUTH-002
type: security-question
---

# Token Validation

## Question

How does the API validate authentication
tokens before granting access?

## Evidence Requested

Please provide:

- Token validation logic
- Signature validation
- Issuer validation
- Audience validation
- Token expiration handling

## Related Requirement

[[api-authentication]]
```

---

# 十、现在把整个过程走一遍

用户输入：

> We have a customer-facing REST API. The API is exposed through AWS API Gateway. Lambda functions process requests and DynamoDB stores customer information. OAuth2 is used for authentication.

---

### Step 1

Skill：

```text
Read:
references/domain-index.md
```

AI 判断：

```text
Application Security
Data Security
Identity & Access
```

---

### Step 2

Skill：

```text
Load:

knowledge-base/domains/application-security.md
knowledge-base/domains/data-security.md
knowledge-base/domains/identity-access.md
```

得到 Concern candidates。

例如：

```text
API Security
Input Validation
Authentication
Authorization
Data Protection
...
```

---

### Step 3

Skill：

```text
Read:
references/component-index.md
```

AI：

```text
API Gateway
AWS Lambda
DynamoDB
```

---

### Step 4

Skill：

```text
Load:

knowledge-base/components/api-gateway.md
knowledge-base/components/aws-lambda.md
knowledge-base/components/dynamodb.md
```

然后得到 Component 预定义关系：

```text
API Gateway
 ├── API Security
 ├── Authentication
 ├── Authorization
 └── Logging

AWS Lambda
 ├── Secrets Management
 ├── Logging
 └── ...

DynamoDB
 ├── Data Protection
 ├── Encryption
 └── ...
```

---

### Step 5

合并：

```text
Domain-derived Concerns
+
Component-derived Concerns
```

得到：

```text
API Security
Authentication
Authorization
Data Protection
Encryption
Logging
Secrets Management
...
```

---

### Step 6

现在才开始：

```text
Load:

knowledge-base/concerns/api-security.md
knowledge-base/concerns/authentication.md
knowledge-base/concerns/authorization.md
...
```

AI 判断 Applicability。

例如：

```text
API Security       ✓
Authentication     ✓
Authorization      ✓
Data Protection    ✓
Encryption         ✓
Logging            ✓
Secrets Management ?
```

---

### Step 7

然后：

```text
Concern
   ↓
Requirement
```

例如：

```text
API Security
   ↓
API Authentication
API Authorization
API Input Validation
```

---

### Step 8

最后：

```text
Requirement
   ↓
Question
```

得到：

```text
Q-API-AUTH-001
Q-API-AUTH-002
...
```

最终生成：

```text
Security Questionnaire
──────────────────────

1. API Security

   1.1 API Authentication

       Q1. How are clients authenticated?

       Q2. How are authentication tokens validated?

   1.2 API Authorization

       Q3. How are API permissions enforced?

       Q4. How is least privilege implemented?
```

---

# 十一、这个设计里每个文件到底是谁维护、谁读取？

这个表非常重要：

|文件|人维护|AI读取|程序读取|作用|
|---|--:|--:|--:|---|
|`SKILL.md`|✅|✅|—|告诉 AI 怎么执行 Review|
|`domain-index.md`|❌/可选|✅|✅|Domain 候选索引|
|`component-index.md`|❌/可选|✅|✅|Component 候选索引|
|`domains/*.md`|✅|✅|✅|Domain → Concern|
|`components/*.md`|✅|✅|✅|Component → Concern|
|`concerns/*.md`|✅|✅|✅|Concern Knowledge|
|`requirements/*.md`|✅|✅|✅|Security Requirement|
|`questions/*.md`|✅|✅|✅|Questionnaire|

这里我特别建议：

> **Index 不作为人工 Source of Truth。**

未来可以由程序从：

```text
domains/*.md
components/*.md
```

自动生成。

---

# 十二、这个版本其实已经可以开始做 POC

你现在甚至不用做：

- Vector DB
    
- Embedding
    
- RAG framework
    
- SQLite
    
- Elasticsearch
    
- 独立 Retrieval Service
    
- Evaluation Platform
    

第一版只需要：

```text
Obsidian
   ↓
Markdown + YAML Frontmatter
   ↓
Goose
   ↓
Security Review Skill
   ↓
LLM
```

以及一个非常简单的知识结构：

```text
Domain
   ↓
Concern
   ↓
Requirement
   ↓
Question
```

和：

```text
Component
   ↓
Concern
```

这两条关系。

---

## 最后，我认为这一版最重要的设计原则就是

**Skill 不存 Security Knowledge。**

Skill 存的是：

> **“我应该按照什么顺序、去什么地方、读取什么东西、做什么判断。”**

而 Knowledge Base 存的是：

> **“Security Domain / Component / Concern / Requirement / Question 到底是什么，以及它们之间是什么关系。”**

所以最终是：

```text
                 SKILL.md
                    │
          ┌─────────┼──────────┐
          ↓         ↓          ↓
       Domain    Component   Workflow
       Index       Index
          │         │
          ↓         ↓
      Domain MD  Component MD
          │         │
          └────┬────┘
               ↓
        Security Concerns
               ↓
          Concern MD
               ↓
        Requirements MD
               ↓
          Questions MD
```

**这条链已经可以作为你整个 Security Review Skill 的 V0.1 实现蓝图。** 后面你要加入 Evidence Extraction 时，只需要在 `Questionnaire → Evidence → Satisfied/Unresolved Questions` 后面继续接，不需要推翻前面的结构。
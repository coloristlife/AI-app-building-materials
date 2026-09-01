

我前面的设计更偏向“规范化数据库/程序实现”的思路：

```text
Component
   ↓
Mapping
   ↓
Concern
   ↓
Requirement
   ↓
Control
   ↓
Question
```

对于程序很好，但如果这个 Knowledge Base 是放在 **Obsidian 里供人维护和 review**，让人不断：

> 打开 Component → 找 Mapping → 再打开 Concern → 再找 Requirement → 再找 Question

确实很痛苦。

我现在反而建议你采用一个 **“Canonical Entity + Human-facing Knowledge View”** 的双层设计。

---

# 1. 不要让 Mapping 成为人类主要阅读入口

我们仍然保留：

```text
components/
concerns/
requirements/
controls/
questions/
mappings/
```

因为程序需要 normalization。

但是：

> **人类不应该从 `mappings/` 开始阅读。**

人类应该打开：

```text
components/aws-lambda.md
```

就能看到：

```text
AWS Lambda
│
├── Description
├── Hierarchy
├── Security Concerns
│    ├── Authorization
│    ├── Secrets Management
│    ├── Dependency Security
│    └── Logging
│
├── Security Requirements
│    ├── ...
│
├── Security Controls
│    ├── ...
│
└── Security Questions
     ├── ...
```

也就是说：

> **Mapping 是 machine-facing；Component 页面是 human-facing。**

---

# 2. Obsidian 非常适合做这个事情

例如你的：

```text
components/aws-lambda.md
```

可以写成：

```markdown
---
id: AWS-LAMBDA
name: AWS Lambda
type: service
category: compute
parents:
  - SERVERLESS-COMPUTE
provider: AWS
aliases:
  - Lambda
  - Lambda function
---

# AWS Lambda

## Overview

AWS serverless compute service.

## Hierarchy

[[SERVERLESS-COMPUTE]]

## Security Concerns

- [[Authorization]]
- [[Secrets Management]]
- [[Dependency Security]]
- [[Logging]]

## Security Requirements

### Authorization

- [[Least Privilege]]
- [[Function-Level Authorization]]

### Secrets Management

- [[Secrets Must Not Be Hardcoded]]

## Security Controls

- IAM
- AWS Secrets Manager
- KMS

## Security Review Questions

- [[AUTH-Q001]]
- [[SECRET-Q003]]
- [[LOG-Q002]]

## Security Review Guidance

When reviewing Lambda workloads, pay particular attention to:

- execution role permissions
- secret handling
- dependency management
- logging
```

这样人打开 **AWS Lambda** 这个页面，基本就已经看到整个 security profile 了。

---

# 3. 但我不建议把所有内容真的复制进去

这里有一个非常关键的区别：

### 不要这样：

```markdown
## Security Concerns

### Authorization

Authorization is ...

Requirements:
...

Questions:
...
```

然后又在：

```text
concerns/authorization.md
```

存一份。

这样会产生 **duplicate source of truth**。

最终一定会出现：

```text
AWS Lambda.md
       ↓
说 Authorization 要求 A

Authorization.md
       ↓
说 Authorization 要求 B
```

然后两边不一致。

---

# 4. 应该使用 Obsidian Wiki Links

所以 Component 页面只保存：

> **relationships + summary**

例如：

```markdown
## Security Concerns

- [[Authorization]]
- [[Secrets Management]]
- [[Dependency Security]]
- [[Logging]]
```

点击：

```text
[[Authorization]]
```

就进入：

```text
concerns/authorization.md
```

而 Authorization 页面里面：

```markdown
# Authorization

## Definition

...

## Security Requirements

- [[Least Privilege]]
- [[Access Control Enforcement]]

## Security Controls

- IAM
- RBAC

## Review Questions

- [[AUTH-Q001]]
- [[AUTH-Q002]]
```

这样形成一个真正的 **Security Knowledge Graph**。

---

# 5. 更重要的是：反向链接

Obsidian 最适合你的地方其实是这个。

例如你打开：

```text
Authorization.md
```

可以看到：

> **Linked mentions / backlinks**

```text
Used by Components

← AWS Lambda
← API Gateway
← Kubernetes
← PostgreSQL
← Azure AD
```

所以你可以从两个方向走：

```text
Component
   ↓
Concern
```

也可以：

```text
Concern
   ↓
Components
```

这对于 Security Architecture Knowledge Base 非常有价值。

---

# 6. 我甚至建议每个 Component 页面做成一个“Security Profile”

这是我现在最推荐你改变的地方。

不要把 Component 当成一个简单 YAML record。

而是：

> **Component = 一个可以被人阅读的 Security Profile。**

例如：

```text
AWS Lambda
────────────────────────

Type
Service

Category
Compute / Serverless

Parent
Serverless Compute

Provider
AWS


SECURITY CONCERNS

🔴 Authorization
🟠 Secrets Management
🟠 Dependency Security
🟡 Logging


SECURITY REQUIREMENTS

Authorization
 ├─ Least Privilege
 └─ Function Authorization

Secrets Management
 └─ Secrets must not be hardcoded

Dependency Security
 └─ Dependencies must be managed


IMPLEMENTATION / CONTROLS

AWS IAM
AWS Secrets Manager
AWS KMS


QUESTIONNAIRE

AUTH-Q001
AUTH-Q002
SECRET-Q003
LOG-Q002
```

这才是人真正需要看的东西。

> **Security Profile**

理解成一种 **logical view / information model**，而不是一种固定文件格式。

也就是说：

> Security Profile 描述“一个 Component 的完整安全信息应该展示什么”，但它不要求必须是某一种文件。

# 但是在你的项目里，我建议它真正落成 Markdown

因为你明确说了：

> **这个 Knowledge Base 是放在 Obsidian 里面。**

那么我会建议：

> **Security Profile = 一个真实存在的 Markdown Knowledge Object。**

例如：

components/

└── aws-lambda.md

这就是一个真正的 Security Profile。

里面：

---
~~~

id: AWS-LAMBDA

name: AWS Lambda

type: service

category: compute

---

  

# AWS Lambda

  

## Identity

  

...

  

## Security Concerns

  

- [[Authorization]]

- [[Secrets Management]]

- [[Dependency Security]]

  

## Security Requirements

  

...

  

## Security Controls

  

...

  

## Security Questions
...
~~~
  



所以在你的项目里：

```text
Security Profile

        ↓

具体实现

        ↓

Markdown file

```
---

# 7. YAML 和 Markdown 可以分工

我现在会修改之前的设计：

### YAML = machine-readable canonical definition

例如：

```text
components/aws-lambda.yaml
```

```yaml
id: AWS-LAMBDA
name: AWS Lambda
type: service
category: compute

parents:
  - SERVERLESS-COMPUTE

provider: AWS

aliases:
  - Lambda
  - Lambda function
```

### Markdown = human-readable knowledge page

```text
components/aws-lambda.md
```

里面通过 Wiki Links 展现：

```markdown
## Security Concerns

- [[Authorization]]
- [[Secrets Management]]
- [[Dependency Security]]
- [[Logging]]
```

---

# 8. 甚至可以进一步：Markdown 不需要手工维护所有关系

这是我觉得最适合你的地方。

你可以让：

```text
YAML
+
Mapping
```

成为 **source of truth**。

然后程序自动生成：

```text
aws-lambda.md
```

例如：

```text
Component YAML
      +
Mappings
      +
Concern YAML
      +
Requirement YAML
      +
Question YAML
      ↓
Obsidian Knowledge View Generator
      ↓
aws-lambda.md
```

生成出来：

```markdown
# AWS Lambda

## Security Concerns

- [[Authorization]]
- [[Secrets Management]]
- [[Dependency Security]]
- [[Logging]]

## Requirements

### [[Authorization]]
- [[Least Privilege]]

### [[Secrets Management]]
- [[Secret Protection]]

## Questions

- [[AUTH-Q001]]
- [[SECRET-Q003]]
```

这样：

> **程序负责维护 consistency，Obsidian 负责阅读和探索。**

---

# 9. 这其实是“Canonical Data + Materialized View”

从软件架构角度看，这个模式非常合理。

```text
             Canonical Knowledge
                    │
       ┌────────────┼────────────┐
       ↓            ↓            ↓
   Component      Concern     Question
      YAML          YAML         YAML
       │
       ↓
    Mapping
       │
       ↓
   Knowledge Compiler
       │
       ↓
   Human View
       │
       ↓
    Obsidian
```

所以 Obsidian 页面可以被看成：

> **Materialized Knowledge View**

而不是第二套数据库。

---

# 10. 甚至可以做一个 Component Dashboard

Obsidian 还有一个非常适合你的功能：

**Dataview**。

例如你可以建立：

```text
Component Dashboard.md
```

然后自动显示：

|Component|Type|Parent|Concerns|Questions|
|---|---|---|---|---|
|AWS Lambda|Service|Serverless|4|8|
|API Gateway|Service|API Gateway|5|12|
|DynamoDB|Service|Database|4|7|

甚至可以按照：

```text
Cloud
Compute
Database
Identity
Network
API
Messaging
```

自动生成目录。

---

# 11. Graph View 也会非常有价值

你的 Knowledge Base 最终天然形成：

```text
AWS Lambda
     │
     ├──────────────→ Authorization
     │                     │
     │                     ↓
     │              Least Privilege
     │                     │
     │                     ↓
     │                  IAM
     │
     ├──────────────→ Secrets Management
     │                     │
     │                     ↓
     │              Secrets Protection
     │
     └──────────────→ Logging
```

Obsidian Graph View 可以直接把这些关系视觉化。

这比传统数据库 UI 更适合做：

> **Security Architecture Knowledge Exploration**

---

# 12. 所以我会修改我们之前的整体设计

之前是：

```text
Component
Concern
Requirement
Control
Question
     ↑
 Mapping
```

我现在建议变成：

```text
             CANONICAL KNOWLEDGE
                    │
        ┌───────────┼───────────┐
        ↓           ↓           ↓
   Component     Concern     Question
      YAML          YAML        YAML
        │           │           │
        └───── Mapping ─────────┘
                    │
                    ↓
             Knowledge Compiler
                    │
                    ↓
          HUMAN-FACING OBSIDIAN
                    │
                    ↓
          Component Security Profile
```

**人从 Component Profile 开始看。**

而不是从 Mapping 开始看。

---

# 13. 最终你打开一个 Component，应该看到什么？

我认为这是我们整个设计最重要的 UX。

比如打开：

> `AWS Lambda`

第一屏就应该是：

```text
AWS Lambda
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TYPE
Service

CATEGORY
Compute → Serverless Compute

PARENT
Serverless Compute


SECURITY CONCERNS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Authorization
🟠 Secrets Management
🟠 Dependency Security
🟡 Logging


SECURITY REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Authorization
  → Least Privilege
  → Function Authorization

Secrets Management
  → Secret Protection

Dependency Security
  → Dependency Isolation


IMPLEMENTATION / CONTROLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IAM
Secrets Manager
KMS
Dependency Scanning


QUESTIONNAIRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUTH-Q001
AUTH-Q002
SECRET-Q003
LOG-Q002


REFERENCES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AWS Lambda Security
NIST
OWASP


RELATED COMPONENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Serverless Compute
API Gateway
DynamoDB
```

这就是一个 **Security Component Profile**。

---

## 结论

所以你这个问题实际上让我觉得，我们之前的设计应该做一个重要调整：

> **不要在“数据规范化”和“人类可读性”之间二选一。**

同时保留两层：

### Machine Layer

```text
YAML
+
Mappings
+
Typed Models
```

保证：

- consistency
    
- validation
    
- automation
    
- deterministic processing
    
- AI retrieval
    

### Human Layer

```text
Obsidian Markdown
+
Wiki Links
+
Backlinks
+
Dataview
+
Graph View
```

保证：

- readability
    
- navigation
    
- review
    
- knowledge exploration
    
- architecture understanding
    

而且最关键的是：

> **Mapping 不应该是人类的阅读界面；Mapping 是后台关系数据。Component Security Profile 才是人类的主要入口。**

这也意味着我们下一版的完整平台设计文档里，最好正式增加一个 **“Knowledge Presentation Layer / Obsidian Knowledge View”**，并把 **Component Profile、Concern Profile、Requirement Profile、Question Profile** 都定义出来。这样整个 Security Architecture Library 就不再只是“一堆 YAML”，而会真正变成一个可以在 Obsidian 里浏览、跳转、反向追踪和审查的 **Security Knowledge Graph**。
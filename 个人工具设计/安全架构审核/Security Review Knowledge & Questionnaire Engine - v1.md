

## Platform Design & Implementation Specification

**Document Version:** V1.0  
**Status:** Design Baseline  
**Purpose:** Define the architecture, data model, repository structure, AI responsibilities, deterministic processing, knowledge model, processing pipeline, technology stack, and implementation roadmap for an AI-assisted Security Review Questionnaire Generation Platform.

---

# 1. Executive Summary

本平台的目标不是构建一个通用的 Agent Skill Platform，也不是首先构建一个复杂的 Evaluation Platform。

平台的核心目标是：

> **将用户提供的自然语言系统描述自动转换为结构化的 System Model，识别其中的 Components，将 Components 映射到 Security Concerns，再根据 Security Knowledge Base 中定义的 Security Requirements、Security Controls 和 Questions，自动生成一份针对该系统的 Security Review Questionnaire。**

核心流程：

```text
System Description
        |
        v
System Understanding
        |
        v
Component Extraction
        |
        v
Component Resolution
        |
        v
Canonical Components
        |
        v
Security Concern Mapping
        |
        v
Concern Applicability
        |
        v
Security Requirements
        |
        v
Security Controls
        |
        v
Question Selection
        |
        v
Questionnaire Generation
        |
        v
Evidence / Assessment
```

平台的核心资产不是 LLM，也不是 Skill。

核心资产是：

```text
Security Knowledge Base
        +
Component Ontology
        +
Component-to-Concern Mapping
        +
Concern-to-Question Mapping
```

LLM 主要承担：

```text
Natural Language Understanding
Semantic Extraction
Entity Resolution Assistance
Contextual Reasoning
Evidence Extraction
```

程序主要承担：

```text
Validation
Normalization
Deterministic Mapping
Deduplication
Filtering
Ordering
Questionnaire Assembly
Traceability
Versioning
```

---

# 2. Design Principles

## 2.1 AI Understands; Knowledge Base Defines

LLM 不拥有 Security Taxonomy。

LLM 可以说：

> "I found something that appears to be a serverless compute component."

但不能自行创造：

```text
component_name = "My Serverless Backend"
```

最终 Component 必须来自 Component Catalog。

原则：

```text
LLM:
"What does the system appear to contain?"

Knowledge Base:
"What are the valid identities?"

Resolver:
"Which valid identity matches the observed entity?"
```

---

## 2.2 Canonical Identity Must Come From the Knowledge Base

系统中的 Component 必须最终解析为：

```text
component_id
canonical_name
```

例如：

```yaml
component_id: AWS-LAMBDA
canonical_name: AWS Lambda
```

用户可能写：

```text
Lambda
Lambda function
serverless function
AWS Lambda function
serverless backend
```

这些都可以作为输入 mention，但最终统一为：

```text
AWS-LAMBDA
```

---

## 2.3 Folder Structure Is Not Ontology

文件夹仅用于：

- 人工管理
    
- Git repository organization
    
- 浏览
    
- ownership
    
- deployment packaging
    

真正的 hierarchy 必须存在于 Component YAML 中：

```yaml
parents:
  - SERVERLESS-COMPUTE
```

因此：

```text
Folder hierarchy != Knowledge hierarchy
```

---

## 2.4 Deterministic Logic Should Not Be Replaced by LLM

如果一个逻辑可以通过数据库查询、规则或程序稳定完成，就不要让 LLM 每次重新生成。

例如：

```text
Component → Concern
Concern → Requirement
Concern → Question
```

应该优先 deterministic。

---

## 2.5 Everything Important Must Be Traceable

系统最终必须能够回答：

> 为什么识别出了这个 Component？

> 为什么这个 Concern 被加入？

> 为什么这个 Question 被要求回答？

因此每个 AI-derived decision 都应该保存：

```text
source text
evidence
confidence
resolution method
knowledge base version
```

---

# 3. Target Architecture

平台采用四个主要层次：

```text
+---------------------------------------------------------+
|                    User / Reviewer                      |
+---------------------------+-----------------------------+
                            |
                            v
+---------------------------------------------------------+
|              AI System Understanding Layer             |
|                                                         |
|  System Analysis                                          |
|  Component Extraction                                     |
|  Entity Recognition                                       |
|  Evidence Extraction                                      |
+---------------------------+-----------------------------+
                            |
                            v
+---------------------------------------------------------+
|              Component Resolution Layer                 |
|                                                         |
|  Exact Match                                              |
|  Alias Match                                              |
|  Semantic Search                                          |
|  Candidate Ranking                                        |
|  LLM Reranking                                            |
|  Canonical Identity                                       |
+---------------------------+-----------------------------+
                            |
                            v
+---------------------------------------------------------+
|             Security Knowledge Engine                   |
|                                                         |
| Component Ontology                                        |
| Component → Concern Mapping                               |
| Concern Applicability                                     |
| Concern → Requirement                                     |
| Requirement → Control                                     |
| Concern → Question                                        |
+---------------------------+-----------------------------+
                            |
                            v
+---------------------------------------------------------+
|             Questionnaire Generation Layer              |
|                                                         |
| Question Selection                                        |
| Deduplication                                             |
| Ordering                                                  |
| Prioritization                                            |
| Evidence Pre-population                                   |
| Output Generation                                         |
+---------------------------------------------------------+
```

---

# 4. Core Knowledge Model

平台的核心 logical model：

```text
System
  |
  +-- Component
  |
  +-- Data
  |
  +-- Architecture Context
  |
  +-- Security Context
          |
          v
     Security Concern
          |
          v
     Security Requirement
          |
          v
     Security Control
          |
          v
       Question
          |
          v
       Evidence
          |
          v
      Assessment
```

---

# 5. Component Model

## 5.1 Component Definition

Component 是系统中可以被 Security Review 识别和分析的 canonical entity。

Component 不一定是一个产品。

它可以是：

```text
Concept
Technology
Service
Platform
Architecture Pattern
Infrastructure Component
Security Component
Identity Component
Data Component
```

例如：

```text
Compute
Serverless Compute
AWS Lambda
```

或者：

```text
Identity
Identity Provider
Azure AD
```

---

# 6. Component Hierarchy

推荐使用 hierarchical ontology。

例如：

```text
COMPUTE
|
+-- SERVERLESS-COMPUTE
|   |
|   +-- AWS-LAMBDA
|   +-- AZURE-FUNCTIONS
|   +-- GOOGLE-CLOUD-FUNCTIONS
|
+-- CONTAINER-COMPUTE
    |
    +-- KUBERNETES
    +-- ECS
```

另一个：

```text
IDENTITY
|
+-- IDENTITY-PROVIDER
    |
    +-- AZURE-AD
    +-- OKTA
    +-- AUTH0
```

Hierarchy 用于：

1. 支持不同 abstraction level。
    
2. 允许用户只描述 category。
    
3. 支持 parent-level security concerns。
    
4. 允许 child component 继承 parent concerns。
    
5. 支持 Component Resolution。
    
6. 支持未来扩展。
    

---

# 7. Component YAML

推荐一个 Component 一个 YAML 文件。

示例：

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
  - AWS Lambda function
  - serverless function

description: >
  AWS serverless compute service.

status: active

metadata:
  cloud: AWS
  deployment_model: serverless
```

---

# 8. Component Fields

建议字段：

|Field|Purpose|
|---|---|
|`id`|Immutable canonical identifier|
|`name`|Canonical display name|
|`type`|Concept / technology / service / platform|
|`category`|Compute / API / Database / Identity etc.|
|`parents`|Ontology hierarchy|
|`provider`|AWS / Azure / Google / Vendor etc.|
|`aliases`|Natural language variants|
|`description`|Semantic description|
|`status`|active / deprecated|
|`metadata`|Additional structured attributes|

---

# 9. Component Catalog Physical Structure

推荐：

```text
knowledge-base/
|
+-- components/
|   |
|   +-- compute/
|   |   +-- compute.yaml
|   |   +-- serverless-compute.yaml
|   |   +-- aws-lambda.yaml
|   |   +-- azure-functions.yaml
|   |
|   +-- api/
|   |   +-- api.yaml
|   |   +-- api-gateway.yaml
|   |   +-- aws-api-gateway.yaml
|   |
|   +-- database/
|   |   +-- database.yaml
|   |   +-- dynamodb.yaml
|   |   +-- postgresql.yaml
|   |
|   +-- identity/
|       +-- identity.yaml
|       +-- identity-provider.yaml
|       +-- azure-ad.yaml
|       +-- okta.yaml
```

注意：

```text
components/compute/
```

只是物理组织方式。

真正 hierarchy：

```yaml
parents:
  - SERVERLESS-COMPUTE
```

---

# 10. Component Resolution

这是 AI-assisted architecture 中最重要的部分之一。

流程：

```text
System Description
       |
       v
AI Extraction
       |
       v
Observed Mention
       |
       v
Component Resolver
       |
       +--> Exact Match
       |
       +--> Alias Match
       |
       +--> Semantic Search
       |
       +--> Candidate Ranking
       |
       +--> LLM Reranking
       |
       v
Canonical Component
```

---

# 11. AI Component Extraction

LLM 不应该直接生成 canonical component ID。

它首先提取：

```json
{
  "mentions": [
    {
      "text": "serverless backend functions",
      "type": "compute",
      "context": "Backend processing is implemented using serverless backend functions."
    },
    {
      "text": "managed NoSQL database",
      "type": "database",
      "context": "Customer records are stored in a managed NoSQL database."
    }
  ]
}
```

这里：

```text
serverless backend functions
```

只是 observed mention。

---

# 12. Component Resolution

Resolver 对 mention 执行：

```text
1. Exact canonical name
2. Alias matching
3. Normalized string matching
4. Semantic retrieval
5. Candidate ranking
6. Optional LLM reranking
```

例如：

```text
Observed:
"serverless backend functions"

Candidates:

AWS Lambda              0.91
Azure Functions          0.87
Google Cloud Functions   0.82
```

如果上下文包含：

```text
AWS
```

则 AWS Lambda 可以被确定。

---

# 13. Unknown Must Be Allowed

如果没有足够证据：

```json
{
  "status": "UNKNOWN",
  "mention": "proprietary event engine"
}
```

系统**不能强行选择一个 Component**。

这是平台的重要安全原则：

> False positive Component identification should be avoided.

---

# 14. Resolution Output

最终输出：

```json
{
  "component_id": "AWS-LAMBDA",
  "canonical_name": "AWS Lambda",
  "type": "service",
  "source_mention": "serverless backend functions",
  "resolution_method": "semantic_match",
  "confidence": 0.91,
  "evidence": [
    {
      "text": "Backend processing is implemented using serverless backend functions."
    }
  ]
}
```

---

# 15. Security Concern Model

Concern 描述：

> 某个 Component、Architecture、Data Type 或 System Context 所引出的 Security Risk Area。

例如：

```text
AUTHENTICATION
AUTHORIZATION
API-SECURITY
DATA-PROTECTION
ENCRYPTION
SECRETS-MANAGEMENT
LOGGING
MONITORING
NETWORK-SECURITY
```

---

# 16. Concern YAML

示例：

```yaml
id: AUTHENTICATION

name: Authentication

description: >
  Security concerns related to verifying the identity
  of users, services, or other entities.

category: identity

severity_default: high

requirements:
  - STRONG-AUTHENTICATION
  - MFA
  - SESSION-MANAGEMENT

questions:
  - AUTH-Q001
  - AUTH-Q002
  - AUTH-Q003

references:
  - NIST-800-53
  - OWASP-ASVS

status: active
```

---

# 17. Component-to-Concern Mapping

不建议把所有 Mapping 直接写进 Component YAML。

建议独立：

```text
knowledge-base/
|
+-- mappings/
    |
    +-- component-to-concern.yaml
```

例如：

```yaml
mappings:

  - component: API-GATEWAY
    concerns:
      - API-SECURITY
      - AUTHENTICATION
      - AUTHORIZATION
      - RATE-LIMITING
      - LOGGING

  - component: AWS-LAMBDA
    concerns:
      - AUTHORIZATION
      - SECRETS-MANAGEMENT
      - DEPENDENCY-SECURITY
      - LOGGING

  - component: DYNAMODB
    concerns:
      - DATA-PROTECTION
      - ENCRYPTION
      - ACCESS-CONTROL
```

这样 Mapping 是独立的 decision layer。

---

# 18. Parent Concern Inheritance

如果：

```text
SERVERLESS-COMPUTE
```

具有：

```text
SECRETS-MANAGEMENT
AUTHORIZATION
LOGGING
```

那么：

```text
AWS-LAMBDA
```

可以继承这些 concerns。

逻辑：

```text
AWS-LAMBDA
    |
    +-- Own Concerns
    |
    +-- Parent Concerns
          |
          +-- SERVERLESS-COMPUTE
```

最终程序执行：

```text
Resolved Concerns =
Own Concerns
+
Inherited Concerns
```

然后 deduplicate。

---

# 19. Concern Applicability

Applicability 是判断：

> Candidate Concern 是否真正适用于当前 System Context。

例如：

```text
Component:
Database

Candidate Concern:
Data Protection
```

如果系统处理：

```text
Customer financial information
```

则：

```text
APPLICABLE
```

如果数据只是：

```text
Public product catalog
```

则可能：

```text
LOW
```

或者：

```text
CONDITIONAL
```

---

# 20. Applicability States

推荐：

```text
APPLICABLE
NOT_APPLICABLE
CONDITIONAL
UNKNOWN
```

V1 可以简化为：

```text
Candidate
Applicable
Excluded
```

V2 再增加复杂 policy engine。

---

# 21. Applicability Architecture

推荐 hybrid：

```text
Candidate Concern
       |
       v
Context Extraction        <-- AI
       |
       v
Rules / Policy Engine     <-- Program
       |
       v
Applicability Decision
```

AI 不直接拥有最终 policy decision。

---

# 22. Security Requirement

Requirement 是 Concern 对系统提出的安全要求。

例如：

```text
Concern:
Authentication

Requirements:
- Strong Authentication
- MFA
- Secure Session Management
- Credential Protection
```

Requirement 应该是稳定、可复用的 Security Knowledge。

---

# 23. Security Control

Control 是实现 Requirement 的具体机制。

例如：

```text
Requirement:
Strong Authentication

Controls:
- OAuth 2.0
- OpenID Connect
- MFA
- SSO
- Conditional Access
```

逻辑：

```text
Concern
  |
  v
Requirement
  |
  v
Control
```

---

# 24. Question Model

Question 是最终需要 System Owner / Application Owner 回答的问题。

例如：

```yaml
id: AUTH-Q001

text: >
  Does the application enforce multi-factor authentication
  for privileged and standard users?

concern:
  - AUTHENTICATION

requirement:
  - MFA

evidence_expected:
  - authentication architecture
  - identity provider configuration
  - MFA policy

response_type: text

required: true
```

---

# 25. Question YAML

推荐：

```text
knowledge-base/questions/
```

每个 Question 可以独立 YAML。

例如：

```yaml
id: AUTH-Q001

text: >
  Does the application enforce multi-factor authentication?

concerns:
  - AUTHENTICATION

requirements:
  - MFA

controls:
  - MFA

response_type: text

required: true

priority: high

evidence_expected:
  - MFA configuration
  - identity provider policy

status: active
```

---

# 26. Question Mapping

如果 Question 与 Concern 的关系很稳定：

```yaml
concern: AUTHENTICATION

questions:
  - AUTH-Q001
  - AUTH-Q002
  - AUTH-Q003
```

也可以放在：

```text
mappings/concern-to-question.yaml
```

推荐独立 Mapping，以便未来：

- 不同系统类型使用不同 Question
    
- 不同 Risk Level 使用不同 Question
    
- 不同 regulatory framework 使用不同 Question
    

---

# 27. AI vs Deterministic Responsibility

这是整个系统最重要的设计边界。

## AI / Probabilistic

```text
System Understanding
Component Extraction
Natural Language Interpretation
Implicit Component Detection
Context Extraction
Evidence Extraction
Semantic Candidate Generation
Ambiguous Entity Resolution
Applicability Reasoning
Answer Summarization
Review Summary
```

## Deterministic

```text
Schema Validation
Component ID Validation
Canonical Name Resolution
Alias Matching
Component → Concern Mapping
Parent Concern Inheritance
Concern → Requirement Mapping
Requirement → Control Mapping
Concern → Question Mapping
Question Deduplication
Question Filtering
Question Ordering
Questionnaire Assembly
Versioning
Output Formatting
Traceability
```

## Hybrid

```text
Component Resolution
Concern Applicability
Evidence → Question Status
Risk Prioritization
```

---

# 28. Key Principle

平台应该遵循：

```text
AI proposes.
Knowledge Base constrains.
Rules decide where possible.
Program assembles.
```

而不是：

```text
LLM generates everything.
```

---

# 29. End-to-End Example

输入：

```text
The application is deployed on AWS.
It exposes REST APIs through API Gateway.
Backend processing uses serverless functions.
Customer financial information is stored in a managed NoSQL database.
Users authenticate through Azure AD.
```

---

## Step 1 — AI Extraction

```text
API Gateway
serverless functions
managed NoSQL database
Azure AD
customer financial information
AWS
```

---

## Step 2 — Component Resolution

```text
API Gateway
        ↓
AWS API Gateway

serverless functions
        ↓
AWS Lambda

managed NoSQL database
        ↓
DynamoDB

Azure AD
        ↓
Azure AD
```

---

## Step 3 — Concern Mapping

```text
AWS API Gateway
├── API Security
├── Authentication
├── Authorization
├── Rate Limiting
└── Logging

AWS Lambda
├── Authorization
├── Secrets Management
├── Dependency Security
└── Logging

DynamoDB
├── Data Protection
├── Encryption
└── Access Control

Azure AD
├── Authentication
├── Authorization
└── Identity Management
```

---

## Step 4 — Context

AI identifies:

```text
Customer financial information
```

因此：

```text
Data Protection = APPLICABLE
Encryption = APPLICABLE
Access Control = APPLICABLE
```

---

## Step 5 — Collect Questions

系统根据 Concern：

```text
Authentication
Authorization
API Security
Data Protection
Encryption
Secrets Management
Logging
```

查询 Question Catalog。

---

## Step 6 — Deduplicate

例如：

```text
Authentication Q001
Azure AD Q005
API Gateway Q002
```

多个 concerns 可能引用相同问题。

程序根据 Question ID 去重。

---

## Step 7 — Generate Questionnaire

最终：

```text
1. Authentication
   Q001
   Q002

2. Authorization
   Q003
   Q004

3. API Security
   Q005
   Q006

4. Data Protection
   Q007
   Q008

5. Encryption
   Q009
   Q010
```

---

# 30. Evidence Model

每一个 AI-derived entity 都应该保存 evidence。

例如：

```yaml
component_id: AWS-LAMBDA

evidence:
  - text: >
      Backend processing uses serverless functions.

    source: system-description

    confidence: 0.91
```

Concern 也可以保存：

```yaml
concern: DATA-PROTECTION

evidence:
  - text: >
      Customer financial information is stored in the database.

    source: system-description

    confidence: 0.97
```

---

# 31. Evidence Pre-Population

系统不应该只生成：

```text
Does the system encrypt sensitive data at rest?
```

如果输入已经明确：

```text
All customer financial data is encrypted at rest using AWS KMS.
```

系统可以标记：

```text
Potentially Answered
```

并保存：

```text
Evidence:
AWS KMS is used for encryption at rest.
```

但不要直接将它视为正式 Security Review evidence，除非用户确认。

状态可以是：

```text
NOT_REVIEWED
AI_IDENTIFIED
USER_CONFIRMED
VERIFIED
```

---

# 32. Questionnaire Generation Must Be Deterministic

Questionnaire Generation 不应该由 LLM 自由生成。

流程：

```text
Applicable Concerns
       |
       v
Question Lookup
       |
       v
Filter
       |
       v
Deduplicate
       |
       v
Prioritize
       |
       v
Order
       |
       v
Render
```

LLM 可以负责：

```text
Question contextualization
Evidence extraction
Optional wording suggestions
```

但最终 Question ID 应来自 Knowledge Base。

---

# 33. Skill Architecture

Skill 不是 Knowledge Base。

Skill 只是 Agent 的 workflow instruction。

第一版只需要：

```text
skills/
└── security-review/
    ├── SKILL.md
    └── references/
```

---

# 34. SKILL.md

示例：

```markdown
---
name: security-review
description: >
  Analyze a system description, identify canonical components,
  resolve applicable security concerns, and generate a security
  review questionnaire using the Security Knowledge Base.
---

# Security Review Skill

## Workflow

1. Analyze the system description.
2. Extract system components and relevant context.
3. Resolve extracted components against the Component Catalog.
4. Never invent a canonical component.
5. Identify candidate security concerns.
6. Apply applicable concern rules.
7. Retrieve security requirements and controls.
8. Retrieve relevant questionnaire questions.
9. Remove duplicate questions.
10. Extract supporting evidence from the system description.
11. Generate the final questionnaire.
12. Preserve traceability between system evidence, components,
    concerns, requirements, controls, and questions.

## Component Resolution

Only canonical components defined in the Component Catalog
may be returned as resolved components.

If no sufficiently supported component exists, return UNKNOWN.

## Security Knowledge

Security requirements, controls, and questions must come from
the Security Knowledge Base.

Do not invent security requirements or questionnaire questions
unless explicitly requested.
```

---

# 35. Skill's Actual Role

Skill controls：

```text
Workflow
Reasoning procedure
Tool usage
Output format
Safety constraints
Knowledge retrieval procedure
```

Skill does NOT own：

```text
Component definitions
Security concerns
Requirements
Controls
Questions
```

这些属于 Knowledge Base。

---

# 36. Repository Structure

推荐最终项目结构：

```text
security-review-engine/
|
+-- knowledge-base/
|   |
|   +-- components/
|   |   |
|   |   +-- compute/
|   |   +-- api/
|   |   +-- database/
|   |   +-- identity/
|   |   +-- network/
|   |   +-- messaging/
|   |   +-- storage/
|   |
|   +-- concerns/
|   |
|   +-- requirements/
|   |
|   +-- controls/
|   |
|   +-- questions/
|   |
|   +-- mappings/
|   |   +-- component-to-concern.yaml
|   |   +-- concern-to-requirement.yaml
|   |   +-- requirement-to-control.yaml
|   |   +-- concern-to-question.yaml
|   |
|   +-- taxonomies/
|   |
|   +-- frameworks/
|       +-- nist.yaml
|       +-- owasp.yaml
|       +-- asvs.yaml
|
+-- skills/
|   |
|   +-- security-review/
|       +-- SKILL.md
|       +-- references/
|
+-- src/
|   |
|   +-- extraction/
|   |   +-- system_analyzer.py
|   |   +-- component_extractor.py
|   |   +-- evidence_extractor.py
|   |
|   +-- resolution/
|   |   +-- component_resolver.py
|   |   +-- exact_match.py
|   |   +-- alias_match.py
|   |   +-- semantic_match.py
|   |   +-- reranker.py
|   |
|   +-- knowledge/
|   |   +-- component_catalog.py
|   |   +-- concern_catalog.py
|   |   +-- question_catalog.py
|   |   +-- mapping_engine.py
|   |
|   +-- applicability/
|   |   +-- evaluator.py
|   |   +-- rules.py
|   |
|   +-- questionnaire/
|   |   +-- selector.py
|   |   +-- deduplicator.py
|   |   +-- prioritizer.py
|   |   +-- generator.py
|   |
|   +-- models/
|   |   +-- system.py
|   |   +-- component.py
|   |   +-- concern.py
|   |   +-- requirement.py
|   |   +-- control.py
|   |   +-- question.py
|   |   +-- evidence.py
|   |
|   +-- validation/
|   |
|   +-- output/
|       +-- json_renderer.py
|       +-- markdown_renderer.py
|       +-- excel_renderer.py
|
+-- evals/
|   |
|   +-- component-resolution/
|   +-- concern-mapping/
|   +-- questionnaire/
|
+-- tests/
|
+-- docs/
|   +-- architecture.md
|   +-- knowledge-model.md
|   +-- component-model.md
|   +-- ai-boundaries.md
|
+-- pyproject.toml
+-- README.md
```

---

# 37. Recommended Technology Stack

## Core Language

推荐：

```text
Python 3.12+
```

原因：

- LLM ecosystem 成熟
    
- YAML / JSON support
    
- Pydantic
    
- embedding libraries
    
- evaluation libraries
    
- data processing
    
- FastAPI
    
- CLI development
    

---

# 38. Data Model

推荐：

```text
Pydantic
```

所有 YAML 都先解析成 typed model。

例如：

```python
class Component(BaseModel):
    id: str
    name: str
    type: str
    category: str
    parents: list[str] = []
    provider: str | None = None
    aliases: list[str] = []
```

这样 YAML 只是 storage format。

真正的内部 representation 是 typed object。

---

# 39. Initial Storage

V1：

```text
YAML + Git
```

足够。

不需要一开始：

```text
Neo4j
PostgreSQL
Vector DB
Elasticsearch
```

---

# 40. Semantic Retrieval

如果 Component 数量较少：

```text
YAML
+
in-memory embedding index
```

就可以。

当 Component 数量扩大后再考虑：

```text
PostgreSQL + pgvector
```

或：

```text
dedicated vector database
```

不要为了 RAG 而 RAG。

---

# 41. LLM Layer

LLM 应通过一个统一 interface：

```python
class LLMClient:
    def generate(...)
    def structured_output(...)
```

这样未来可以替换：

```text
OpenAI
Azure OpenAI
Anthropic
Local Model
Ollama
```

而不会改变业务逻辑。

---

# 42. Embedding Layer

定义：

```python
class EmbeddingProvider:
    def embed(text)
```

第一版可以使用：

```text
OpenAI embedding
Azure OpenAI embedding
local embedding model
```

不要让 Component Resolver 直接绑定某个 provider。

---

# 43. Component Resolver Architecture

建议：

```text
Resolver
|
+-- ExactMatcher
|
+-- AliasMatcher
|
+-- SemanticRetriever
|
+-- CandidateRanker
|
+-- LLMReranker
|
+-- ConfidencePolicy
```

---

# 44. Confidence Policy

例如：

```text
>= 0.95
    AUTO_ACCEPT

0.80 - 0.95
    ACCEPT_WITH_EVIDENCE

0.60 - 0.80
    HUMAN_REVIEW

< 0.60
    UNKNOWN
```

实际 threshold 应通过 evaluation dataset 调整。

不要把这些数字永久写死。

---

# 45. Security Knowledge Engine

核心 interface：

```python
class KnowledgeEngine:

    def resolve_component(component_id)

    def get_parent_components(component_id)

    def get_concerns(component_id)

    def get_requirements(concern_id)

    def get_controls(requirement_id)

    def get_questions(concern_id)
```

---

# 46. Mapping Engine

Mapping Engine 完全 deterministic：

```text
Component
    ↓
Own Concerns
    +
Parent Concerns
    ↓
Deduplicate
    ↓
Candidate Concerns
```

---

# 47. Applicability Engine

V1：

```text
Candidate Concern
       |
       v
Simple Rules
       |
       v
Applicable / Excluded
```

V2：

```text
AI Context Extraction
       |
       v
Policy Rules
       |
       v
Applicability Decision
```

V3：

```text
Policy Engine
+
Risk Model
+
Regulatory Context
```

---

# 48. Questionnaire Engine

核心：

```python
class QuestionnaireEngine:

    def select_questions()

    def deduplicate_questions()

    def prioritize_questions()

    def build_questionnaire()

    def render()
```

---

# 49. Questionnaire Output Model

最终输出不应该只是 Markdown。

内部结构应类似：

```json
{
  "review_id": "SR-001",
  "knowledge_base_version": "1.0.0",
  "components": [],
  "concerns": [],
  "requirements": [],
  "controls": [],
  "questions": [],
  "evidence": [],
  "assessment": {}
}
```

然后可以 render 成：

```text
Markdown
Excel
JSON
HTML
Word
```

---

# 50. Traceability Model

必须支持：

```text
Question
   |
   +-- Concern
   |
   +-- Requirement
   |
   +-- Control
   |
   +-- Component
   |
   +-- Evidence
   |
   +-- Source Text
```

例如：

```text
AUTH-Q001
    |
    +-- Authentication
          |
          +-- MFA
                |
                +-- Azure AD
                      |
                      +-- "Users authenticate through Azure AD."
```

---

# 51. Versioning

Knowledge Base 必须 versioned。

例如：

```text
KB Version: 1.4.0
```

Questionnaire 必须记录：

```text
knowledge_base_version
skill_version
model_version
```

这样未来才能解释：

> 为什么去年和今年生成的 Questionnaire 不一样？

---

# 52. Evaluation Strategy

Evaluation 的重点不是：

> Skill 是否写得漂亮？

而是：

> Security Review Pipeline 是否正确？

Evaluation Dataset 应包含：

```text
System Description
Expected Components
Expected Concerns
Expected Questions
```

例如：

```yaml
id: SEC-001

input: |
  The application uses AWS API Gateway and Lambda.
  Customer financial data is stored in DynamoDB.

expected_components:
  - AWS-API-GATEWAY
  - AWS-LAMBDA
  - DYNAMODB

expected_concerns:
  - API-SECURITY
  - AUTHORIZATION
  - DATA-PROTECTION
  - ENCRYPTION

expected_questions:
  - API-Q001
  - AUTH-Q001
  - DATA-Q001
```

---

# 53. Evaluation Metrics

重点指标：

```text
Component Precision
Component Recall
Component Resolution Accuracy

Concern Precision
Concern Recall

Question Precision
Question Recall

Unknown Detection Accuracy

False Positive Rate

Traceability Coverage
```

特别重要的是：

```text
False Positive Component Rate
```

因为错误识别一个 Component 可能导致大量错误 Questionnaire。

---

# 54. Human-in-the-Loop

对于低 confidence：

```text
System
   |
   v
AI
   |
   v
Confidence < threshold
   |
   v
Human Review
```

Reviewer 可以：

```text
Accept
Reject
Replace
Add Component
```

人工选择应该记录：

```text
original AI decision
human decision
reason
timestamp
```

未来这些数据可以用于改进 Resolver。

---

# 55. What We Should NOT Build in V1

第一版明确不做：

```text
Harbor integration
Inspect integration
Multi-agent architecture
Distributed execution
Complex sandbox
Vector database
Knowledge graph database
Automatic Skill optimization
GEPA optimization
Complex RAG pipeline
Autonomous security assessment
Automatic control verification
```

这些都不是当前核心问题。

---

# 56. V1 Implementation Scope

V1 只实现：

```text
1. Component Catalog
2. Component Ontology
3. Component YAML schema
4. Concern Catalog
5. Requirement Catalog
6. Control Catalog
7. Question Catalog
8. Component → Concern Mapping
9. AI Component Extraction
10. Component Resolver
11. Basic Applicability
12. Questionnaire Generator
13. Evidence Extraction
14. Traceability
15. Markdown / JSON output
16. Evaluation Dataset
```

---

# 57. V1 End-to-End Command

最终可以提供：

```bash
security-review analyze \
  --input system-description.md \
  --knowledge-base ./knowledge-base \
  --output ./output/review.json
```

或者：

```bash
security-review questionnaire \
  --input system-description.md
```

输出：

```text
output/
|
+-- components.json
+-- concerns.json
+-- evidence.json
+-- questionnaire.json
+-- questionnaire.md
```

---

# 58. Optional Skill Integration

如果使用 Goose 或其他 Agent Runtime：

```text
Goose
  |
  v
security-review Skill
  |
  v
Security Review Engine
```

Skill 负责指导 Agent 调用：

```text
System Analyzer
Component Resolver
Knowledge Engine
Questionnaire Generator
```

而不是自己保存 Security Knowledge。

---

# 59. Recommended Development Order

## Phase 1 — Knowledge Model

先完成：

```text
Component
Concern
Requirement
Control
Question
Mapping
```

这是最高优先级。

---

## Phase 2 — Component Resolver

实现：

```text
AI Extraction
↓
Exact Match
↓
Alias Match
↓
Semantic Search
↓
Candidate Ranking
↓
Unknown
```

---

## Phase 3 — Deterministic Knowledge Engine

实现：

```text
Component
↓
Concern
↓
Requirement
↓
Control
↓
Question
```

---

## Phase 4 — Questionnaire Generator

实现：

```text
Filter
Deduplicate
Prioritize
Order
Render
```

---

## Phase 5 — Evidence

加入：

```text
Source Text
Evidence
Confidence
Traceability
```

---

## Phase 6 — Applicability

从简单规则开始：

```text
Candidate Concern
↓
Context
↓
Rule
↓
Applicable / Excluded
```

---

## Phase 7 — Evaluation

建立至少：

```text
50–100 System Description test cases
```

覆盖：

```text
Cloud
API
Database
Identity
Data
Messaging
Containers
Serverless
Third-party services
Hybrid architectures
```

---

# 60. Future Architecture

未来可以逐渐扩展成：

```text
                 Security Review Platform
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
      Knowledge        AI Engine       Evaluation
        Engine
          |
   +------+------+ 
   |             |
Components     Concerns
   |             |
Requirements   Controls
   |
Questions
```

再加入：

```text
Threat Modeling
Control Validation
Compliance Mapping
Risk Scoring
Security Architecture Graph
Existing Review Comparison
Continuous Review
```

---

# 61. Long-Term Security Architecture Model

最终可以形成：

```text
System
 |
 +-- Component
 |     |
 |     +-- Technology
 |     +-- Service
 |     +-- Platform
 |     +-- Architecture Pattern
 |
 +-- Data
 |
 +-- Trust Boundary
 |
 +-- Communication
 |
 +-- Identity
 |
 +-- External Dependency
 |
 v
Security Concerns
 |
 v
Threats
 |
 v
Security Requirements
 |
 v
Security Controls
 |
 v
Questionnaire
 |
 v
Evidence
 |
 v
Assessment
 |
 v
Risk
```

这时候平台就不仅仅是 Questionnaire Generator，而可以逐渐成为：

> **Security Architecture Knowledge and Decision Platform**

---

# 62. Final Architectural Principle

整个系统最终应该遵循：

```text
                    Natural Language
                           |
                           v
                         AI
                           |
                  Semantic Understanding
                           |
                           v
                  Observed Entities
                           |
                           v
                  Component Resolver
                           |
                           v
                Canonical Component
                           |
                           v
              Deterministic Knowledge
                           |
                           v
                  Security Concern
                           |
                           v
                 Security Requirement
                           |
                           v
                  Security Control
                           |
                           v
                     Question
                           |
                           v
                       Evidence
                           |
                           v
                      Assessment
```

核心边界：

```text
+-------------------------+
|        AI Zone          |
|                         |
| Understanding           |
| Extraction              |
| Semantic Reasoning      |
| Evidence Identification |
+------------+------------+
             |
             v
+-------------------------+
|   Knowledge Boundary    |
|                         |
| Canonical Components    |
| Security Concerns       |
| Requirements            |
| Controls                |
| Questions               |
+------------+------------+
             |
             v
+-------------------------+
|    Deterministic Zone   |
|                         |
| Mapping                 |
| Validation              |
| Filtering               |
| Deduplication           |
| Ordering                |
| Generation              |
| Traceability            |
+-------------------------+
```

---

# 63. Final Decision

本项目 V1 不应该被定义为：

> **Skill Creator Platform**

也不应该被定义为：

> **Generic Agent Evaluation Platform**

更准确的定义应该是：

> **AI-Assisted Security Review Knowledge & Questionnaire Engine**

其核心价值是：

```text
Understand the System
        ↓
Identify Canonical Components
        ↓
Resolve Security Concerns
        ↓
Retrieve Security Knowledge
        ↓
Generate Targeted Questionnaire
        ↓
Maintain Evidence & Traceability
```

其中：

```text
AI = Semantic Interpreter
Knowledge Base = Security Authority
Rules = Decision Logic
Program = Deterministic Execution Layer
Skill = Agent Workflow Instruction
```

这五者的边界应该从项目第一天就保持清晰。

最终最重要的设计原则可以浓缩为一句话：

> **LLM extracts meaning; the Knowledge Base owns identity and security knowledge; deterministic code owns the final mapping and questionnaire construction.**
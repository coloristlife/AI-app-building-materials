## 1. Design Objective

本知识库用于支撑 **Security Architecture Review（SAR）**，目标不是简单保存安全文档，而是建立一套能够支持 **安全知识复用、风险量化、Component 分析以及逐步深化实施指导** 的结构化知识体系。

在实际 Architecture Review 中，输入通常是一个非常具体的技术 Component，例如 AWS RDS、S3、Lambda、某一种 Database 或 MCP Server。Reviewer 需要从这个 Component 出发，识别其涉及的 Security Concerns 和 Security Topics，然后确定相关的 Risk、Security Requirement、Security Control 以及实施方式。

因此，知识库需要同时解决三个核心问题：

1. **如何从具体 Component 快速确定需要进行哪些安全分析。**
    
2. **如何将相同的 Risk、Requirement 和 Control 在不同 Component、平台和架构中复用。**
    
3. **如何对 Risk 和 Mitigation 进行结构化量化，并随着知识积累逐渐增加实施深度。**
    

知识库第一阶段以 Obsidian 作为知识创建、维护和阅读环境，使用 Markdown 保存安全知识，使用 Properties / YAML Frontmatter 保存结构化 Metadata，并通过 Wiki Links 建立知识之间的关系。

后续可以在此基础上扩展到 Search、RAG、Knowledge Graph 和自动化 Architecture Review。

---

# 2. Core Knowledge Model

整个 Knowledge Base 的核心模型为：

```text
Architecture
    │
    ↓
Component
    │
    ↓
Component Profile
    │
    ↓
Security Concern
    │
    ↓
Security Topic
    │
    ├───────────────┐
    ↓               ↓
Risk Assessment   Knowledge Objects
                    │
        ┌───────────┼────────────┐
        ↓           ↓            ↓
      Risk      Requirement    Control
        │           │            │
        └───────────┼────────────┘
                    ↓
          Implementation Guidance
                    │
                    ↓
        Platform-Specific Implementation
                    │
                    ↓
          Detailed Configuration
                    │
                    ↓
            Validation / Evidence
```

这里有一个重要设计原则：

> **Security Topic 负责建立上下文和关联，而 Risk、Requirement、Control 应该是可以被多个 Security Topics 和 Components 重用的独立知识对象。**

这样可以同时满足“针对具体 Component 进行分析”和“跨平台复用安全知识”两个要求。

---

# 3. Component

Component 是 Architecture Review 的入口对象。

例如：

```text
AWS RDS
AWS S3
AWS Lambda
AWS API Gateway
MCP Server
MCP Client
PostgreSQL
Redis
Kafka
```

一个 Architecture 通常由多个 Component 构成：

```text
Application
├── API Gateway
├── Lambda
├── RDS
├── S3
└── MCP Server
```

Architecture Review 首先识别这些 Component，然后根据 Component Profile 确定需要覆盖的 Security Concerns。

---

# 4. Component Profile

Component Profile 定义：

> **一个具体 Component 在 Security Architecture Review 中应该覆盖哪些 Security Concerns，以及这些 Concern 的基本属性。**

例如：

```yaml
---
type: component
id: AWS-RDS

name: Amazon RDS
platform: AWS
component_type: database

security_concerns:
  - id: DATA-PROTECTION
    priority: high

  - id: ACCESS-CONTROL
    priority: high

  - id: NETWORK-SECURITY
    priority: high

  - id: LOGGING-MONITORING
    priority: medium

  - id: BACKUP-RECOVERY
    priority: medium

status: active
---
```

Component Profile 不负责保存所有安全 Requirement 和 Implementation，而是负责定义 Component 的 **Security Coverage**。

例如：

```text
AWS RDS
├── Data Protection
├── Access Control
├── Network Security
├── Logging & Monitoring
└── Backup & Recovery
```

具体的 Security Topic 和 Security Knowledge 则通过关系进一步展开。

---

# 5. Security Concern

Security Concern 是 Component 的安全分析维度。

典型的 Concern 包括：

- Data Protection
    
- Access Control
    
- Network Security
    
- Logging & Monitoring
    
- Backup & Recovery
    
- Availability
    
- Data Lifecycle
    

例如：

```text
AWS RDS
├── Data Protection
│   ├── Data Classification
│   ├── Encryption at Rest
│   ├── Encryption in Transit
│   └── Key Management
│
├── Access Control
│   ├── Authentication
│   ├── Authorization
│   └── Least Privilege
│
└── Network Security
    ├── Network Isolation
    ├── Public Access
    └── Network Access Control
```

Security Concern 用于确定 **“要看什么”**，而 Security Topic 用于确定 **“具体要解决什么安全问题”**。

---

# 6. Security Topic

Security Topic 是针对某个具体安全问题形成的上下文对象。

例如：

```text
AWS RDS
└── Data Protection
    └── Encryption at Rest
```

Security Topic：

```text
AWS-RDS-Encryption-at-Rest
```

负责将：

```text
Component
+
Security Concern
+
Risk
+
Requirement
+
Control
+
Implementation
```

关联起来。

一个 Security Topic 不应该重复保存所有 Risk、Requirement 和 Control 的完整内容，而应该引用相应的可复用 Knowledge Objects。

---

# 7. Reusable Security Knowledge Objects

知识库中的以下对象应该被设计为可复用对象：

```text
Risk
Security Requirement
Security Control
```

例如：

```text
REQ-DATA-ENCRYPTION
CTRL-ENCRYPTION-AT-REST
RISK-DATA-DISCLOSURE
```

这些对象不应该绑定到单一 Component。

例如：

```text
CTRL-ENCRYPTION-AT-REST
```

可以被：

```text
AWS RDS
AWS S3
Azure SQL
GCP Cloud SQL
PostgreSQL
Oracle Database
```

共同引用。

---

# 8. Security Control Reuse

Security Control 是非常重要的复用层。

例如：

```text
CTRL-ENCRYPTION-AT-REST
```

定义通用的：

> Encryption at Rest

它本身描述的是安全控制目标和控制要求，而不是某一个产品的具体配置。

然后不同 Component 分别提供 Implementation：

```text
CTRL-ENCRYPTION-AT-REST
        │
        ├── AWS RDS
        │   └── AWS encryption + KMS
        │
        ├── AWS S3
        │   └── S3 encryption + KMS
        │
        ├── Azure SQL
        │   └── TDE + Key Vault
        │
        └── PostgreSQL
            └── Storage / Disk Encryption
```

因此，Control 本身应该保持平台相对独立，而具体实现属于 Component / Platform 层。

---

# 9. Requirement、Control 和 Implementation 的关系

三者应该明确区分：

```text
Security Requirement
        ↓
Security Control
        ↓
Implementation
```

例如：

```text
Requirement:
Sensitive data must be encrypted at rest.

        ↓

Control:
Encryption at Rest.

        ↓

Implementation:
AWS RDS → AWS encryption + KMS
```

多个 Requirement 可以要求同一个 Control：

```text
REQ-001 ──┐
REQ-002 ──┼──→ CTRL-ENCRYPTION-AT-REST
REQ-003 ──┘
```

一个 Requirement 也可能需要多个 Controls：

```text
REQ-DATA-PROTECTION
        │
        ├── Encryption at Rest
        ├── Key Management
        └── Access Control
```

因此，Requirement 和 Control 应该采用 **many-to-many relationship**，而不是简单的一对一关系。

---

# 10. Security Topic 的完整结构

Security Topic 建议采用：

```text
Security Topic
│
├── Context
│
├── Risk Assessment
│
├── Security Requirements
│
├── Security Controls
│
├── Implementation Guidance
│
├── Platform-Specific Implementation
│
├── Detailed Configuration
│
├── Mitigation Assessment
│
└── Validation / Evidence
```

其中：

**Context** 描述这个 Topic 为什么与当前 Component 有关。

**Risk Assessment** 描述风险及其量化结果。

**Security Requirements** 引用可复用 Requirement。

**Security Controls** 引用可复用 Control。

**Implementation Guidance** 提供平台无关的高层实施建议。

**Platform-Specific Implementation** 描述具体平台实现。

**Detailed Configuration** 保存实际配置方法。

**Mitigation Assessment** 描述控制措施对风险的降低效果以及实施成本。

**Validation / Evidence** 描述如何证明 Control 已经正确实施。

---

# 11. Risk Assessment Model

Risk 不应该只有：

```text
Low
Medium
High
Critical
```

这样的最终标签。

知识库需要保存形成 Risk Level 的主要因素，使 Risk Rating 可以解释、比较和重新计算。

第一版建议采用：

```text
Risk Assessment
├── Impact
├── Exploitability
├── Exposure
├── Likelihood
├── Inherent Risk
└── Residual Risk
```

---

# 12. Impact

Impact 表示成功攻击后可能产生的影响。

建议采用 1–5：

|Score|Impact|
|--:|---|
|1|Negligible|
|2|Low|
|3|Moderate|
|4|High|
|5|Critical|

Impact 可以综合考虑：

- Confidentiality
    
- Integrity
    
- Availability
    
- Privacy
    
- Regulatory / Compliance
    
- Financial Impact
    
- Business Impact
    

对于需要更精细评估的场景，可以进一步拆分这些维度。

---

# 13. Exploitability

Exploitability 描述攻击者利用该风险需要多少能力和条件。

建议采用 1–5：

|Score|Exploitability|
|--:|---|
|1|Very Difficult|
|2|Difficult|
|3|Moderate|
|4|Easy|
|5|Very Easy|

可以考虑：

- 所需攻击技能；
    
- 是否需要认证；
    
- 是否需要特殊权限；
    
- 是否需要内部访问；
    
- 攻击步骤复杂度；
    
- 是否存在公开 Exploit；
    
- 是否可以自动化；
    
- 是否需要特殊环境条件。
    

---

# 14. Exposure

Exposure 描述 Component 或功能对潜在攻击者的暴露程度。

建议采用 1–5：

|Score|Exposure|
|--:|---|
|1|Highly Isolated|
|2|Limited|
|3|Controlled / Internal|
|4|Broad|
|5|Public / Internet-Facing|

可以考虑：

- Internet-facing；
    
- Internal-only；
    
- Public API；
    
- User-controlled input；
    
- Third-party connectivity；
    
- Cross-account access；
    
- Cross-tenant access；
    
- Privileged administrative interface。
    

Exposure 与 Exploitability 分开，可以避免把“容易攻击”和“容易接触到”混为一谈。

---

# 15. Likelihood

Likelihood 表示风险在当前 Architecture 和 Threat Context 下实际发生的可能性。

建议采用 1–5：

|Score|Likelihood|
|--:|---|
|1|Rare|
|2|Unlikely|
|3|Possible|
|4|Likely|
|5|Almost Certain|

Likelihood 应综合考虑：

```text
Threat Context
+
Exposure
+
Exploitability
+
Existing Controls
+
Architecture Context
```

它不是简单地复制 Exploitability 或 Exposure。

---

# 16. Inherent Risk

Inherent Risk 表示在考虑现有防护措施之前的风险。

第一版可以采用简单、透明的计算方式：

```text
Inherent Risk Score = Impact × Likelihood
```

其中：

```text
Impact = 1–5
Likelihood = 1–5
```

建议映射：

|Score|Risk Level|
|--:|---|
|1–4|Low|
|5–9|Medium|
|10–16|High|
|17–25|Critical|

这个模型的优点是简单、透明、容易解释。

后续如果实际 Review 数据显示该模型不能很好反映真实风险，可以升级 Risk Model，而不需要改变 Knowledge Object 的整体结构。

---

# 17. Residual Risk

Architecture Review 中不能只评估 Inherent Risk，还需要考虑现有 Controls。

因此：

```text
Inherent Risk
      ↓
Existing Controls
      ↓
Residual Risk
```

例如：

```yaml
risk_assessment:
  impact: 5
  exploitability: 4
  exposure: 5
  likelihood: 4

inherent_risk:
  score: 20
  level: critical

existing_controls:
  - CTRL-STRONG-AUTHENTICATION
  - CTRL-LEAST-PRIVILEGE
  - CTRL-RATE-LIMITING

residual_risk:
  level: high
```

这样 Review 可以区分：

> **这个风险本身有多严重。**

和：

> **在当前 Architecture 中，现有防护之后还剩多少风险。**

---

# 18. Mitigation 与 Risk 分离

**Mitigation Effort 不应该直接参与 Risk Score。**

例如：

```text
High Risk + Easy to Fix
```

仍然是 High Risk。

同样：

```text
High Risk + Very Difficult to Fix
```

也仍然是 High Risk。

因此：

```text
Risk Severity
```

和：

```text
Mitigation Effort
```

必须作为两个独立维度。

---

# 19. Mitigation Assessment

建议为每个 Security Topic 增加 Mitigation Assessment：

```text
Mitigation
├── Effectiveness
├── Effort
├── Complexity
└── Dependencies
```

其中：

### Effectiveness

表示该 Control 对 Risk 的降低效果：

|Score|Effectiveness|
|--:|---|
|1|Very Low|
|2|Low|
|3|Moderate|
|4|High|
|5|Very High|

### Effort

表示实施所需的工作量：

|Score|Effort|
|--:|---|
|1|Very Low|
|2|Low|
|3|Moderate|
|4|High|
|5|Very High|

### Complexity

描述实施复杂度。

### Dependencies

描述是否依赖：

- Application Change
    
- Infrastructure Change
    
- Third Party
    
- Migration
    
- Organizational Change
    
- Downtime
    
- Additional Cost
    

---

# 20. Recommendation Priority

Risk Level 和 Mitigation Effort 分开以后，可以进一步形成 Recommendation Priority。

例如：

```text
Risk Level
+
Residual Risk
+
Mitigation Effectiveness
+
Mitigation Effort
```

共同用于决定 Recommendation Priority。

一个典型情况是：

```text
Critical Risk
+
High Control Effectiveness
+
Low Effort
```

应该成为非常高优先级的 Recommendation。

而：

```text
Critical Risk
+
High Control Effectiveness
+
Very High Effort
```

则可能需要形成：

```text
Architecture Decision
+
Remediation Plan
+
Target Date
```

因此 Recommendation Priority 是 **Risk Management Decision**，而不是 Risk Level 本身。

---

# 21. Reusable Risk、Requirement 和 Control

最终知识库中的三类核心对象应该独立管理：

```text
Risks/
├── RISK-DATA-DISCLOSURE.md
├── RISK-UNAUTHORIZED-ACCESS.md
└── RISK-DATA-TAMPERING.md

Requirements/
├── REQ-DATA-ENCRYPTION.md
├── REQ-STRONG-AUTHENTICATION.md
└── REQ-LEAST-PRIVILEGE.md

Controls/
├── CTRL-ENCRYPTION-AT-REST.md
├── CTRL-STRONG-AUTHENTICATION.md
├── CTRL-LEAST-PRIVILEGE.md
└── CTRL-NETWORK-ISOLATION.md
```

然后 Security Topic 通过 ID 引用这些对象。

例如：

```yaml
---
type: security-topic
id: AWS-RDS-ENCRYPTION-AT-REST

component: AWS-RDS
security_concern: DATA-PROTECTION

risks:
  - RISK-DATA-DISCLOSURE

requirements:
  - REQ-DATA-ENCRYPTION

controls:
  - CTRL-ENCRYPTION-AT-REST
---
```

这样一个 Control 可以被大量 Security Topics 重用。

---

# 22. Platform-Specific Implementation

具体实施不应该放在通用 Control 中。

例如：

```text
CTRL-ENCRYPTION-AT-REST
```

只描述通用 Control。

而：

```text
AWS-RDS-ENCRYPTION-AT-REST
```

负责描述：

```text
AWS RDS
    ↓
Encryption
    ↓
KMS
    ↓
Configuration
    ↓
Validation
```

这样：

```text
Control
```

和：

```text
Implementation
```

之间形成清晰的复用关系：

```text
                 CTRL-ENCRYPTION-AT-REST
                           │
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
          AWS RDS       AWS S3       Azure SQL
             │             │             │
             ↓             ↓             ↓
       Implementation Implementation Implementation
```

---

# 23. Knowledge Maturity

知识深度仍然采用渐进式设计。

一个新的 Security Topic 可以只有：

```text
Risk                    ✓
Requirement             ✓
Control                 ✓
High-Level Guidance     ✓
Platform Implementation —
Detailed Configuration  —
Validation              —
```

以后逐步扩展：

```text
Risk                    ✓
Requirement             ✓
Control                 ✓
High-Level Guidance     ✓
Platform Implementation ✓
Detailed Configuration  ✓
Validation              ✓
```

因此 Properties 应该记录：

```yaml
implementation_status: high-level
configuration_status: not-available
validation_status: not-available
```

知识库必须允许“不知道”和“尚未完成”。

---

# 24. Knowledge Object Schema

Security Topic 可以采用：

```yaml
---
type: security-topic
id: AWS-RDS-ENCRYPTION-AT-REST

component: AWS-RDS
security_concern: DATA-PROTECTION

risks:
  - RISK-DATA-DISCLOSURE

requirements:
  - REQ-DATA-ENCRYPTION

controls:
  - CTRL-ENCRYPTION-AT-REST

risk_assessment:
  impact: 5
  exploitability: 4
  exposure: 3
  likelihood: 3

inherent_risk:
  score: 15
  level: high

existing_controls:
  - CTRL-ACCESS-CONTROL

residual_risk:
  level: medium

mitigation:
  effectiveness: 5
  effort: 2
  complexity: low

implementation_status: available
configuration_status: not-available
validation_status: not-available

status: active
---
```

Markdown 正文：

```markdown
# Encryption at Rest

## Context

AWS RDS stores application and customer data and therefore
requires protection against unauthorized disclosure.

## Platform-Specific Implementation

Use the approved AWS encryption mechanism and centralized
key management.

## Detailed Configuration

Not yet documented.

## Validation / Evidence

Not yet documented.
```

---

# 25. Knowledge Base Directory Structure

第一阶段可以采用：

```text
Security-Knowledge-Base/
│
├── Components/
│
├── Security-Concerns/
│
├── Security-Topics/
│
├── Risks/
│
├── Requirements/
│
├── Controls/
│
└── References/
```

其中：

**Components** 保存 Component Profiles。

**Security Concerns** 保存安全领域定义。

**Security Topics** 保存 Component + Security Concern 下的具体安全问题。

**Risks** 保存可复用 Risk Objects。

**Requirements** 保存可复用 Security Requirements。

**Controls** 保存可复用 Security Controls。

**References** 保存外部标准、厂商文档以及其他参考资料。

---

# 26. Knowledge Relationships

整个 Knowledge Base 最终形成：

```text
Component
    │
    ↓
Security Topic
    │
    ├──────────────→ Risk
    │
    ├──────────────→ Requirement
    │
    └──────────────→ Control
                         │
                         ↓
                   Implementation
                         │
              ┌──────────┼──────────┐
              ↓          ↓          ↓
             AWS       Azure       GCP
```

同时：

```text
Requirement
     ↓
Control
     ↓
Implementation
```

形成可复用的 Security Control Chain。

---

# 27. Architecture Review Workflow

最终 Review 流程可以设计为：

```text
Architecture Input
        ↓
Component Identification
        ↓
Load Component Profile
        ↓
Identify Security Concerns
        ↓
Retrieve Security Topics
        ↓
Retrieve Reusable Risks
        ↓
Retrieve Reusable Requirements
        ↓
Retrieve Reusable Controls
        ↓
Evaluate Existing Controls
        ↓
Calculate Inherent Risk
        ↓
Calculate Residual Risk
        ↓
Evaluate Mitigation
        ↓
Retrieve Platform Implementation
        ↓
Retrieve Detailed Configuration
        ↓
Generate Recommendation
```

这个流程使知识库不只是一个文档库，而是可以逐渐成为 **Security Architecture Review Decision Support System**。

---

# 28. Future RAG / Knowledge Graph Architecture

第一阶段的 Obsidian Knowledge Base 可以作为 Knowledge Authoring Layer：

```text
Obsidian
    │
    ↓
Markdown + Properties + Links
    │
    ↓
Knowledge Ingestion
    │
    ├── Structured Metadata
    ├── Full-text Search
    ├── Vector Index
    └── Knowledge Graph
             │
             ↓
             RAG
             │
             ↓
      Architecture Review Agent
```

由于 Risk、Requirement、Control、Component 和 Implementation 都拥有明确的 ID 和关系，未来可以同时支持：

- Metadata Filtering
    
- Full-text Search
    
- Semantic Search
    
- Graph Traversal
    
- RAG
    
- Risk Calculation
    
- Control Mapping
    
- Recommendation Generation
    

---

# 29. Final Design Principles

整个知识库最终遵循以下原则：

**Component-first**：从真实 Architecture 中的具体 Component 开始。

**Concern-driven**：根据 Component 的安全特征确定 Security Concerns。

**Topic-centered**：Security Topic 是具体安全问题的上下文组织单位。

**Reusable Risk**：Risk 可以被多个 Security Topics 和 Components 复用。

**Reusable Requirement**：Security Requirement 尽可能保持平台无关并跨平台复用。

**Reusable Control**：Security Control 是核心复用对象，可以被不同 Component、Platform 和 Security Topic 共同引用。

**Implementation-specific**：具体实施方式属于 Platform / Component 层，而不是通用 Control。

**Quantifiable Risk**：Risk 不仅保存 Low / Medium / High，而是保存 Impact、Exploitability、Exposure 和 Likelihood 等构成因素。

**Inherent / Residual Risk Separation**：区分没有现有防护时的 Inherent Risk 和实施现有 Controls 后的 Residual Risk。

**Risk ≠ Effort**：Mitigation Effort 不直接改变 Risk Level，而是独立用于确定 Remediation 和 Recommendation Priority。

**Progressive Knowledge**：知识可以从 High-Level Guidance 逐步发展到 Platform Implementation、Detailed Configuration 和 Validation。

**Explicit Knowledge Gaps**：尚未掌握的知识必须明确标记，而不是让系统推测或编造。

**Structured and Human-readable**：Properties 保存结构化 Metadata，Markdown 保存安全知识，Links 保存知识关系。

---

# 30. Final Architecture

最终的知识模型可以归纳为：

```text
                         ARCHITECTURE
                              │
                              ↓
                          COMPONENT
                              │
                              ↓
                     COMPONENT PROFILE
                              │
                              ↓
                     SECURITY CONCERN
                              │
                              ↓
                       SECURITY TOPIC
                              │
              ┌───────────────┼────────────────┐
              ↓               ↓                ↓
             RISK        REQUIREMENT          CONTROL
              │               │                │
              │               └───────┬────────┘
              │                       │
              ↓                       ↓
        RISK ASSESSMENT        IMPLEMENTATION
              │                       │
       ┌──────┼──────┐         ┌─────┴──────┐
       ↓      ↓      ↓         ↓            ↓
    Impact  Exploit  Exposure  Platform   Configuration
       │      │      │         │
       └──────┼──────┘         ↓
              ↓             Validation
         Likelihood
              ↓
        Inherent Risk
              ↓
      Existing Controls
              ↓
        Residual Risk
              
              +
              
        MITIGATION
       ┌──────┼──────┐
       ↓      ↓      ↓
 Effectiveness Effort Complexity
              │
              ↓
      Recommendation Priority
```

这个版本的核心变化是：**Risk、Requirement、Control 都成为可以独立复用的 Knowledge Objects；Security Topic 负责把它们放入具体 Component 的上下文中；Risk Assessment 负责量化风险；Mitigation Assessment 独立描述解决风险所需的成本和复杂度。**

这样，知识库既能回答“这个 Component 有什么安全要求和控制”，也能进一步回答“这个风险为什么是 High、现有控制后还剩多少风险、哪个 Recommendation 应该优先处理，以及同一个 Control 在其他平台上如何复用”。
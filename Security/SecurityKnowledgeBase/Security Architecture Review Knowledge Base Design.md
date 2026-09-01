

## 1. Design Objective

The Security Architecture Review (SAR) Knowledge Base is designed to provide a structured, reusable, and continuously extensible body of security knowledge for architecture reviews.

The objective is not simply to create a collection of security documents. The Knowledge Base should provide a structured model that allows security reviewers and future AI-based systems to:

- identify the security concerns associated with a specific architecture component;
    
- reuse existing security risks, requirements, and controls;
    
- evaluate and quantify security risks;
    
- distinguish generic security guidance from platform-specific implementation;
    
- progressively enrich knowledge from high-level guidance to detailed configuration;
    
- identify knowledge gaps;
    
- support human review and maintenance;
    
- support future search, RAG, Knowledge Graph, and automated Security Architecture Review capabilities.
    

The first implementation may use Obsidian as the authoring and knowledge-management environment. Markdown is used for human-readable knowledge content, while Properties / YAML Frontmatter provides structured metadata and relationships.

The underlying knowledge model should remain independent of Obsidian so that the same knowledge can later be migrated or indexed into other systems.

---

# 2. Core Knowledge Model

The core Knowledge Model is:

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
Risk Assessment   Reusable Knowledge Objects
                    │
        ┌───────────┼────────────┐
        ↓           ↓            ↓
      Risk      Requirement    Control
        │           │            │
        └───────────┼────────────┘
                    ↓
          High-Level Guidance
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

A key design principle is:

> **Security Topics provide context and relationships, while Risk, Requirement, and Control are reusable knowledge objects.**

This allows the Knowledge Base to analyze a specific Component while avoiding unnecessary duplication of common security knowledge.

---

# 3. Component

A **Component** is the primary entry point for a Security Architecture Review.

Examples include:

```text
Amazon RDS
Amazon S3
AWS Lambda
AWS API Gateway
MCP Server
MCP Client
PostgreSQL
Redis
Kafka
```

An Architecture normally consists of multiple Components:

```text
Application
├── API Gateway
├── Lambda
├── RDS
├── S3
└── MCP Server
```

The Architecture Review process first identifies the Components present in the architecture. Each Component is then mapped to its corresponding Component Profile.

---

# 4. Component Profile

A **Component Profile** defines the security coverage required for a specific Component.

It answers:

> **What security areas need to be considered when reviewing this Component?**

For example:

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

The Component Profile should not contain all security requirements, controls, and implementation details.

Its primary responsibility is to define the Component's **Security Coverage**.

For example:

```text
AWS RDS
├── Data Protection
├── Access Control
├── Network Security
├── Logging & Monitoring
└── Backup & Recovery
```

The detailed knowledge is represented through Security Topics and reusable Knowledge Objects.

---

# 5. Security Concern

A **Security Concern** represents a security domain that should be considered for a Component.

Typical Security Concerns include:

- Data Protection
    
- Access Control
    
- Network Security
    
- Logging & Monitoring
    
- Backup & Recovery
    
- Availability
    
- Data Lifecycle
    

For example:

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

A Security Concern answers:

> **What security area should be considered?**

A Security Topic answers:

> **What specific security problem or capability needs to be evaluated within that area?**

---

# 6. Security Topic

A **Security Topic** represents a specific security problem or security capability in the context of a Component and Security Concern.

For example:

```text
AWS RDS
└── Data Protection
    └── Encryption at Rest
```

The corresponding Security Topic could be:

```text
AWS-RDS-ENCRYPTION-AT-REST
```

A Security Topic provides the contextual layer that connects:

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

The Security Topic should not duplicate reusable Risk, Requirement, or Control definitions. Instead, it references them.

This distinction is important for maintaining a scalable knowledge base.

---

# 7. Reusable Security Knowledge Objects

The following should be modeled as reusable Knowledge Objects:

```text
Risk
Security Requirement
Security Control
```

For example:

```text
RISK-UNAUTHORIZED-DATA-DISCLOSURE
REQ-DATA-ENCRYPTION
CTRL-ENCRYPTION-AT-REST
```

These objects should not be tied to a single Component unless the knowledge is inherently Component-specific.

For example, the Control:

```text
CTRL-ENCRYPTION-AT-REST
```

may be reused by:

```text
AWS RDS
AWS S3
Azure SQL
GCP Cloud SQL
PostgreSQL
Oracle Database
```

This avoids creating multiple copies of essentially the same security knowledge.

---

# 8. Security Control Reuse

Security Controls should be explicitly designed as reusable objects.

For example:

```text
CTRL-ENCRYPTION-AT-REST
```

defines the general security control objective and requirements.

It should not contain detailed instructions for a particular product.

Instead, different Components provide their own implementations:

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

This creates a clear separation between:

```text
Reusable Control
```

and:

```text
Component / Platform-specific Implementation
```

The same model can be applied to controls such as:

```text
CTRL-STRONG-AUTHENTICATION
CTRL-LEAST-PRIVILEGE
CTRL-NETWORK-ISOLATION
CTRL-SECURE-LOGGING
CTRL-SECRETS-MANAGEMENT
```

---

# 9. Requirement, Control, and Implementation Relationship

The relationship between Requirement, Control, and Implementation is:

```text
Security Requirement
        ↓
Security Control
        ↓
Implementation
```

For example:

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

A single Requirement may require multiple Controls:

```text
REQ-DATA-PROTECTION
        │
        ├── Encryption at Rest
        ├── Key Management
        └── Access Control
```

A single Control may also satisfy multiple Requirements:

```text
REQ-001 ──┐
REQ-002 ──┼──→ CTRL-ENCRYPTION-AT-REST
REQ-003 ──┘
```

Therefore, Requirement and Control relationships should support **many-to-many relationships**.

---

# 10. Security Topic Structure

A Security Topic should contain the following logical sections:

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
├── High-Level Implementation Guidance
│
├── Platform-Specific Implementation
│
├── Detailed Configuration
│
├── Mitigation Assessment
│
└── Validation / Evidence
```

However, these sections do not all represent the same type of knowledge.

The following are generally reusable:

```text
Risk
Requirement
Control
High-Level Guidance
```

The following are generally Component / Platform-specific:

```text
Platform-Specific Implementation
Detailed Configuration
Validation / Evidence
```

This distinction is fundamental to preventing duplication.

---

# 11. Reusable Knowledge vs. Component-Specific Knowledge

The Knowledge Base should maintain a clear boundary between reusable and contextual knowledge.

|Knowledge|Reusable|Typical Example|
|---|---|---|
|Risk|Yes|Unauthorized Data Disclosure|
|Requirement|Yes|Sensitive data must be encrypted|
|Control|Yes|Encryption at Rest|
|High-Level Guidance|Usually|Use approved encryption and managed keys|
|Platform Implementation|Usually No|RDS encryption + KMS|
|Detailed Configuration|No|Terraform / Console configuration|
|Validation|Usually No|RDS-specific validation steps|

For example, the following is reusable:

```text
Unauthorized disclosure of sensitive data may occur
if data is not adequately protected.
```

The following is also reusable:

```text
Sensitive data should be encrypted at rest using an
approved encryption mechanism and managed encryption keys.
```

However, this is Component-specific:

```text
For AWS RDS, use the approved AWS RDS encryption
mechanism and organization-approved KMS keys.
```

And this is even more specific:

```text
Configure the RDS instance with encryption enabled
and specify the approved KMS key.
```

This layered approach allows the Knowledge Base to grow without repeatedly copying common security guidance.

---

# 12. Risk Assessment Model

Risk should not be represented only as:

```text
Low
Medium
High
Critical
```

The Knowledge Base should preserve the major factors used to determine the Risk Level.

The initial Risk Model should include:

```text
Risk Assessment
├── Impact
├── Exploitability
├── Exposure
├── Likelihood
├── Inherent Risk
└── Residual Risk
```

This allows the final Risk Level to be explained and recalculated.

---

# 13. Impact

**Impact** measures the potential consequences if the risk is successfully exploited.

The initial scale can be:

|Score|Impact|
|--:|---|
|1|Negligible|
|2|Low|
|3|Moderate|
|4|High|
|5|Critical|

Impact may consider:

- Confidentiality
    
- Integrity
    
- Availability
    
- Privacy
    
- Regulatory / Compliance
    
- Financial Impact
    
- Business Impact
    

For more mature implementations, these dimensions can be separately scored.

---

# 14. Exploitability

**Exploitability** measures how difficult it is for an attacker to successfully exploit the risk.

The initial scale can be:

|Score|Exploitability|
|--:|---|
|1|Very Difficult|
|2|Difficult|
|3|Moderate|
|4|Easy|
|5|Very Easy|

Factors may include:

- Required attacker skill;
    
- Required authentication;
    
- Required privileges;
    
- Required internal access;
    
- Number of attack steps;
    
- Availability of public exploits;
    
- Ability to automate the attack;
    
- Required environmental conditions.
    

Exploitability should not be treated as Risk by itself.

An easy-to-exploit weakness does not necessarily create a high business risk if its potential impact is negligible.

---

# 15. Exposure

**Exposure** measures how accessible the Component or attack surface is to potential attackers.

The initial scale can be:

|Score|Exposure|
|--:|---|
|1|Highly Isolated|
|2|Limited|
|3|Controlled / Internal|
|4|Broad|
|5|Public / Internet-Facing|

Factors may include:

- Internet exposure;
    
- Internal-only access;
    
- Public APIs;
    
- User-controlled input;
    
- Third-party connectivity;
    
- Cross-account access;
    
- Cross-tenant access;
    
- Privileged administrative interfaces.
    

Exposure is intentionally separated from Exploitability.

A system may be easy to exploit but highly isolated, or difficult to exploit but publicly exposed.

---

# 16. Likelihood

**Likelihood** represents the probability that the risk will actually occur within the current Architecture and Threat Context.

The initial scale can be:

|Score|Likelihood|
|--:|---|
|1|Rare|
|2|Unlikely|
|3|Possible|
|4|Likely|
|5|Almost Certain|

Likelihood should consider:

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

Likelihood should not simply duplicate Exploitability or Exposure.

It is a higher-level assessment of how likely the threat is to materialize in the specific architecture.

---

# 17. Inherent Risk

**Inherent Risk** represents the risk before considering existing mitigating controls.

The initial model can use:

```text
Inherent Risk Score = Impact × Likelihood
```

with:

```text
Impact = 1–5
Likelihood = 1–5
```

The resulting score can initially be mapped as:

|Score|Risk Level|
|--:|---|
|1–4|Low|
|5–9|Medium|
|10–16|High|
|17–25|Critical|

This model is intentionally simple and transparent.

The scoring model can later be refined based on actual Architecture Review data without changing the underlying Knowledge Object structure.

---

# 18. Residual Risk

Architecture Reviews should distinguish **Inherent Risk** from **Residual Risk**.

The model is:

```text
Inherent Risk
      ↓
Existing Controls
      ↓
Residual Risk
```

For example:

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

This allows the Architecture Review to answer two separate questions:

> How severe is the risk inherently?

and:

> How much risk remains after existing security controls are considered?

---

# 19. Mitigation and Risk Must Remain Separate

**Mitigation Effort should not directly modify the Risk Score.**

For example:

```text
High Risk + Easy to Fix
```

is still High Risk.

Likewise:

```text
High Risk + Very Difficult to Fix
```

is also High Risk.

Risk describes the security exposure.

Mitigation Effort describes the cost and difficulty of reducing that exposure.

Therefore:

```text
Risk Severity
```

and:

```text
Mitigation Effort
```

must remain separate dimensions.

---

# 20. Mitigation Assessment

Each Security Topic should support a Mitigation Assessment:

```text
Mitigation
├── Effectiveness
├── Effort
├── Complexity
└── Dependencies
```

### Effectiveness

Measures how effectively the proposed Control reduces the risk.

|Score|Effectiveness|
|--:|---|
|1|Very Low|
|2|Low|
|3|Moderate|
|4|High|
|5|Very High|

### Effort

Measures the amount of work required to implement the mitigation.

|Score|Effort|
|--:|---|
|1|Very Low|
|2|Low|
|3|Moderate|
|4|High|
|5|Very High|

### Complexity

Describes the implementation complexity.

### Dependencies

May include:

- Application changes;
    
- Infrastructure changes;
    
- Third-party dependencies;
    
- Migration;
    
- Organizational changes;
    
- Downtime;
    
- Additional cost.
    

---

# 21. Recommendation Priority

Risk Level and Mitigation Effort should be used together to determine **Recommendation Priority**, rather than modifying the Risk Level itself.

Relevant factors include:

```text
Risk Level
+
Residual Risk
+
Mitigation Effectiveness
+
Mitigation Effort
```

For example:

```text
Critical Risk
+
High Control Effectiveness
+
Low Effort
```

would normally represent a high-priority remediation opportunity.

Whereas:

```text
Critical Risk
+
High Control Effectiveness
+
Very High Effort
```

may require:

```text
Architecture Decision
+
Remediation Plan
+
Target Date
```

Therefore:

> **Risk Level describes the security problem; Recommendation Priority describes what should be done about it.**

---

# 22. Reusable Risk, Requirement, and Control Objects

The Knowledge Base should maintain reusable objects separately.

Example structure:

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

A Security Topic references these objects by ID:

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

This allows the same Risk, Requirement, and Control to be reused across many Components.

---

# 23. Platform-Specific Implementation

Platform-specific implementation should not be embedded in reusable Controls.

For example:

```text
CTRL-ENCRYPTION-AT-REST
```

defines the generic Control.

A Component-specific knowledge object can then describe:

```text
AWS-RDS-ENCRYPTION-AT-REST
```

including:

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

The relationship becomes:

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

This allows a single Control to be reused while keeping implementation details specific to each platform.

---

# 24. Knowledge Object Schema

A Security Topic should use structured metadata to reference reusable objects and describe its contextual properties.

For example:

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

The Markdown content should focus on the contextual and Component-specific information:

```markdown
# Encryption at Rest

## Context

AWS RDS stores application and customer data and therefore
requires protection against unauthorized disclosure.

## Platform-Specific Implementation

Use the approved AWS RDS encryption mechanism with
organization-approved KMS keys.

## Detailed Configuration

Not yet documented.

## Validation / Evidence

Not yet documented.
```

The reusable Risk, Requirement, Control, and High-Level Guidance should be maintained in their respective reusable Knowledge Objects and referenced from the Security Topic.

This prevents duplication while keeping the Security Topic readable.

---

# 25. Knowledge Base Directory Structure

The initial Obsidian structure can be:

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

### Components

Contains Component Profiles.

### Security-Concerns

Contains definitions of security domains.

### Security-Topics

Contains Component-specific security contexts and their relationships to reusable knowledge.

### Risks

Contains reusable Risk Objects.

### Requirements

Contains reusable Security Requirement Objects.

### Controls

Contains reusable Security Control Objects.

### References

Contains external standards, vendor documentation, security research, and other supporting references.

---

# 26. Knowledge Relationships

The overall Knowledge Graph should form relationships such as:

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

Requirement and Control relationships should also support:

```text
Requirement
     ↓
Control
     ↓
Implementation
```

This structure allows the same Control to be traversed from multiple Requirements and Components.

---

# 27. Architecture Review Workflow

The final Architecture Review workflow can be:

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

This allows the Knowledge Base to gradually evolve from a documentation repository into a **Security Architecture Review Decision Support System**.

---

# 28. Knowledge Maturity

The Knowledge Base should support progressive knowledge maturity.

A newly created Security Topic may contain:

```text
Risk                    ✓
Requirement             ✓
Control                 ✓
High-Level Guidance     ✓
Platform Implementation —
Detailed Configuration  —
Validation              —
```

Over time it can evolve into:

```text
Risk                    ✓
Requirement             ✓
Control                 ✓
High-Level Guidance     ✓
Platform Implementation ✓
Detailed Configuration  ✓
Validation              ✓
```

The metadata should explicitly represent this maturity:

```yaml
implementation_status: high-level
configuration_status: not-available
validation_status: not-available
```

The Knowledge Base must support incomplete knowledge.

A missing implementation should be represented as a known knowledge gap rather than being filled with assumptions or generated content that has not been validated.

---

# 29. Future RAG / Knowledge Graph Architecture

Obsidian should be treated as the first **Knowledge Authoring Layer**, rather than as the final architecture of the system.

The future architecture can be:

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
    ├── Full-Text Search
    ├── Vector Index
    └── Knowledge Graph
             │
             ↓
             RAG
             │
             ↓
      Architecture Review Agent
```

Because Components, Security Topics, Risks, Requirements, Controls, and Implementations have stable IDs and relationships, the same knowledge can support:

- Metadata filtering;
    
- Full-text search;
    
- Semantic search;
    
- Knowledge Graph traversal;
    
- RAG;
    
- Risk calculation;
    
- Control mapping;
    
- Recommendation generation;
    
- Architecture Review automation.
    

---

# 30. Final Design Principles and Architecture

The Security Architecture Review Knowledge Base should ultimately follow these principles.

**Component-first**  
Start from real Components identified in an Architecture rather than starting from abstract security domains.

**Concern-driven**  
Use Security Concerns to determine which security areas must be reviewed for each Component.

**Topic-centered**  
Use Security Topics as the contextual unit that connects a specific Component and Security Concern to reusable security knowledge and Component-specific implementation.

**Reusable Risk**  
Risks should be reusable across multiple Security Topics and Components whenever the underlying risk is materially the same.

**Reusable Requirement**  
Security Requirements should remain as platform-independent as practical and be reused across platforms.

**Reusable Control**  
Security Controls should be independent Knowledge Objects and reused across Components, Platforms, and Security Topics.

**Implementation-specific**  
Platform and product differences should be represented at the Implementation layer rather than duplicated in generic Requirements or Controls.

**Layered Knowledge**  
Separate reusable security knowledge from Component-specific implementation:

```text
Risk
Requirement
Control
High-Level Guidance
        ↓
Platform Implementation
        ↓
Detailed Configuration
        ↓
Validation
```

**Quantifiable Risk**  
Risk should preserve the factors used to determine its severity rather than storing only a qualitative label.

**Inherent / Residual Risk Separation**  
The Knowledge Base should distinguish inherent risk from residual risk after existing Controls are considered.

**Risk ≠ Effort**  
Mitigation Effort should not directly change the Risk Level. It should remain an independent dimension used for remediation and Recommendation Priority.

**Progressive Knowledge**  
Knowledge should be allowed to evolve from High-Level Guidance to Platform Implementation, Detailed Configuration, and Validation.

**Explicit Knowledge Gaps**  
Unknown or incomplete information should be explicitly represented rather than inferred without evidence.

**Structured and Human-readable**  
Properties should store structured metadata, Markdown should contain readable security knowledge, and links should represent relationships.

**AI-ready**  
The structure should be suitable for LLM interpretation, semantic retrieval, RAG, and future Security Architecture Review agents.

**Machine-readable**  
Stable IDs, Properties, and explicit relationships should allow the knowledge to be processed by future databases, search engines, Knowledge Graphs, and automation pipelines.

The resulting architecture is:

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
        RISK ASSESSMENT       HIGH-LEVEL GUIDANCE
              │                       │
       ┌──────┼──────┐                │
       ↓      ↓      ↓                │
    Impact  Exploit  Exposure          │
       │      │      │                │
       └──────┼──────┘                │
              ↓                       │
         Likelihood                   │
              ↓                       │
        Inherent Risk                 │
              ↓                       │
       Existing Controls              │
              ↓                       │
        Residual Risk                 │
                                      │
                                      ↓
                       PLATFORM-SPECIFIC IMPLEMENTATION
                                      │
                                      ↓
                           DETAILED CONFIGURATION
                                      │
                                      ↓
                            VALIDATION / EVIDENCE

              ─────────────────────────────────

                         MITIGATION
                    ┌────────┼────────┐
                    ↓        ↓        ↓
             Effectiveness  Effort  Complexity
                              │
                              ↓
                    RECOMMENDATION PRIORITY
```

The resulting Knowledge Base is therefore not simply a collection of Component-specific security documents. It is a **layered and reusable Security Knowledge System** in which common security knowledge is defined once, Components provide context, platform-specific layers provide implementation details, and structured Risk and Mitigation data support consistent Architecture Review decisions.
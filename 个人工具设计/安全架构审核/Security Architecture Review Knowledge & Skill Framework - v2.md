

## 1. Overview

This document defines the architecture for a reusable, human-readable, AI-consumable Security Architecture Review Knowledge Base and Skill framework.

The primary objective is to enable an AI agent such as Goose to perform security architecture analysis by using a structured security knowledge library.

The framework separates three concerns:

1. **Knowledge** — What security knowledge exists?
    
2. **Skill** — How should an agent perform a security architecture review?
    
3. **Runtime** — How does the agent retrieve and apply the knowledge?
    

The initial implementation prioritizes:

- Human readability
    
- Reusability
    
- Maintainability
    
- Git-based version control
    
- Obsidian compatibility
    
- Goose compatibility
    
- Progressive context retrieval
    
- Platform-specific implementations
    
- Separation of domain knowledge from agent instructions
    

The framework deliberately does **not** initially depend on SQL, Graph databases, Harbor, Inspect, or a dedicated Skill Creator.

---

# 2. Core Design Principle

The most important architectural principle is:

> **Knowledge should be maintained in a human-readable form, while the Skill should define how an agent discovers, resolves, and applies that knowledge.**

Therefore:

```text
                    Security Knowledge
                           │
                 Human-readable Source
                           │
                    Markdown + YAML
                           │
                           ↓
                       Obsidian
                           │
                    Wiki Links / Refs
                           │
                           ↓
                Security Architecture Skill
                           │
                    Retrieval Procedure
                           │
                           ↓
                         Goose
                           │
                           ↓
                Security Architecture Review
```

The Knowledge Base is not simply a collection of documents.

It is a collection of **reusable knowledge objects connected through explicit relationships**.

---

# 3. Why Not Make SQL the Primary Knowledge Base?

A relational database can represent the relationships very well.

For example:

```text
Component
    ↓
Security Concern
    ↓
Security Requirement
    ↓
Security Control
```

can be modeled using tables and many-to-many relationships.

SQL can also resolve complex relationships using JOINs and recursive queries.

However, SQL has a major disadvantage for this use case:

> It is not an ideal authoring and review format for Security Architects.

A security architect should be able to open a file and immediately understand:

- What the component is
    
- What security concerns apply
    
- What requirements apply
    
- What controls are recommended
    
- Why the requirement exists
    
- What platform-specific implementation should be used
    

Therefore SQL should not initially be the **source of truth**.

If SQL is needed later for runtime indexing or large-scale querying, it can be introduced as a derived representation.

The architectural direction is therefore:

```text
Human-readable Source
        ↓
Optional Index / Database
        ↓
Runtime Retrieval
```

rather than:

```text
SQL
  ↓
Human authoring
```

---

# 4. Human-Readable Knowledge Base

The recommended initial implementation is:

- Obsidian
    
- Markdown
    
- YAML frontmatter
    
- Wiki links
    
- Embedded reusable elements
    
- Git version control
    

Example structure:

```text
security-knowledge/
│
├── components/
│   ├── aws-api-gateway.md
│   ├── aws-lambda.md
│   ├── aws-s3.md
│   └── database.md
│
├── reusable/
│   ├── authentication.md
│   ├── authorization.md
│   ├── encryption.md
│   ├── input-validation.md
│   └── logging.md
│
├── requirements/
│   ├── authentication/
│   ├── authorization/
│   └── data-protection/
│
├── controls/
│   ├── oauth.md
│   ├── rbac.md
│   ├── encryption.md
│   └── schema-validation.md
│
├── implementations/
│   ├── aws/
│   ├── azure/
│   └── gcp/
│
├── frameworks/
│   ├── nist/
│   ├── owasp/
│   └── internal/
│
└── patterns/
    ├── api.md
    ├── microservice.md
    └── mcp.md
```

This structure is optimized for human navigation and maintenance.

---

# 5. Reusable Knowledge Elements

A central design principle is to extract common security concepts into reusable elements.

For example:

```text
Authentication
Authorization
Encryption
Input Validation
Logging
Secrets Management
```

These concepts should not be copied into every component document.

Instead, they exist once.

For example:

```text
reusable/authentication.md
```

A component can reference it:

```markdown
## Security Concerns

![[authentication]]
![[authorization]]
![[input-validation]]
```

The component document therefore presents a complete logical view without duplicating the underlying knowledge.

---

# 6. Component Knowledge

A component represents a specific technology, architectural component, or security-relevant building block.

Example:

```markdown
---
id: COMP-AWS-API-GATEWAY
type: component
name: AWS API Gateway
platform: AWS
---

# AWS API Gateway

## Security Concerns

![[authentication]]
![[authorization]]
![[input-validation]]
![[logging]]
```

This creates a human-readable Security Knowledge Page.

The actual reusable knowledge remains stored independently.

---

# 7. Security Knowledge Hierarchy

The primary logical hierarchy is:

```text
Architecture / Component
        ↓
Security Concern
        ↓
Security Requirement
        ↓
Security Control
```

For example:

```text
AWS API Gateway
        │
        ↓
Authentication
        │
        ↓
Authentication Requirement
        │
        ↓
OAuth / OIDC / IAM / Cognito
```

The hierarchy represents conceptual relationships rather than document nesting.

---

# 8. Reusable Elements vs. Component-Specific Knowledge

Not every element should be reusable.

The model should distinguish between:

### Reusable

Generic security concepts that apply to multiple components:

```text
Authentication
Authorization
Encryption
Logging
Input Validation
Least Privilege
Secrets Management
```

### Component-specific

Knowledge specific to a particular technology:

```text
AWS API Gateway throttling
AWS Lambda execution role
S3 bucket policy
Azure Managed Identity
GCP service account
```

The architecture therefore becomes:

```text
Component
    │
    ├── reusable security concepts
    │
    └── component-specific knowledge
```

---

# 9. Platform-Specific Implementation

Security requirements should generally remain platform-independent.

Implementation details should be platform-specific.

For example:

```text
Authentication
       │
       ├── AWS
       │     ├── IAM
       │     └── Cognito
       │
       ├── Azure
       │     ├── Entra ID
       │     └── Managed Identity
       │
       └── GCP
             ├── IAM
             └── Identity Platform
```

This separation prevents the high-level security requirement from becoming coupled to one cloud provider.

Example:

```yaml
---
id: SEC-AUTH-001
type: security-concern
name: Authentication
layer: reusable
---
```

The implementation is separate:

```yaml
---
id: IMPL-AWS-API-GW-AUTH-001
component: COMP-AWS-API-GATEWAY
implements: SEC-AUTH-001
platform: AWS
---
```

Therefore:

```text
Security Concept
       ↓
Security Requirement
       ↓
Platform
       ↓
Implementation
```

---

# 10. Knowledge Relationships

The system should support explicit relationships such as:

```text
Component
    ├── has_security_concern
    ├── uses_pattern
    └── has_implementation

Security Concern
    ├── requires
    ├── mitigated_by
    └── related_to

Security Requirement
    ├── implemented_by
    ├── derived_from
    └── mapped_to

Security Control
    ├── implements
    ├── satisfies
    └── mapped_to_framework
```

Obsidian links can represent many of these relationships.

Example:

```markdown
[[authentication]]
[[authorization]]
[[oauth]]
[[NIST-AC-2]]
```

---

# 11. Stable IDs

Every important knowledge object should have a stable ID.

Example:

```yaml
---
id: SEC-AUTH-001
type: security-concern
name: Authentication
---
```

Requirements:

```yaml
---
id: SEC-REQ-AUTH-001
type: security-requirement
---
```

Controls:

```yaml
---
id: SEC-CTRL-OAUTH-001
type: security-control
---
```

Components:

```yaml
---
id: COMP-AWS-API-GATEWAY
type: component
---
```

Stable IDs are important because the AI should not rely only on filenames or display names.

They also make future migration to SQL, a graph database, or another knowledge backend much easier.

---

# 12. Skill vs. Knowledge

The Skill and Knowledge Base must remain separate.

## Knowledge answers:

> What do we know?

Examples:

```text
Authentication
OAuth
IAM
RBAC
Encryption
NIST requirements
Internal security policies
Cloud implementation guidance
```

## Skill answers:

> How should the agent use what we know?

For example:

```text
1. Understand the architecture.
2. Identify components.
3. Identify trust boundaries.
4. Identify data flows.
5. Identify security-relevant characteristics.
6. Identify applicable security concerns.
7. Retrieve corresponding requirements.
8. Resolve platform-specific implementations.
9. Produce a structured security review.
```

Therefore:

```text
Knowledge = WHAT
Skill     = HOW
Goose     = WHERE / RUNTIME
```

---

# 13. Security Architecture Review Skill

The Security Architecture Review Skill should not contain the entire security knowledge base.

Its purpose is to define the review workflow.

Conceptually:

```text
Input Architecture
        ↓
Architecture Understanding
        ↓
Component Identification
        ↓
Security-Relevant Characteristics
        ↓
Security Concern Identification
        ↓
Knowledge Retrieval
        ↓
Requirement Mapping
        ↓
Control Mapping
        ↓
Platform Implementation Resolution
        ↓
Security Review Output
```

---

# 14. Skill-Driven Knowledge Retrieval

The agent should not blindly load the entire Knowledge Base.

Instead, the Skill should define a retrieval procedure.

Example:

```text
1. Identify the component.
2. Identify its platform.
3. Identify applicable architecture patterns.
4. Identify candidate reusable security elements.
5. Resolve referenced knowledge objects.
6. Determine applicable security concerns.
7. Retrieve related requirements.
8. Retrieve only relevant controls.
9. Resolve platform-specific implementations.
10. Construct the minimum sufficient security context.
```

This creates a **progressive retrieval model**.

---

# 15. Progressive Context Loading

The major concern with Obsidian embedding is context size.

A component might reference:

```text
Authentication
Authorization
Logging
Encryption
Input Validation
```

Each of those might contain:

```text
Requirements
Controls
Examples
Platform implementations
Framework mappings
```

Blindly expanding everything can create a very large context.

Therefore the Skill should use selective resolution.

Instead of:

```text
Component
   ↓
Expand everything
   ↓
Huge Context
```

use:

```text
Component
   ↓
Identify relevant concerns
   ↓
Resolve only relevant reusable elements
   ↓
Resolve relevant requirements
   ↓
Resolve relevant platform implementation
   ↓
Minimal sufficient context
```

This is a key part of the Skill design.

---

# 16. Obsidian as a Human Knowledge Graph

Although Obsidian is not a graph database, its links naturally create a lightweight knowledge graph.

For example:

```text
                 Authentication
                 /            \
                ↓              ↓
        API Gateway          Lambda
                │
                ↓
        AWS Implementation
                │
                ↓
          IAM / Cognito
```

The graph is represented through:

```text
[[Wiki Links]]
```

rather than a specialized graph database.

This gives Security Architects:

- Human-readable documents
    
- Backlinks
    
- Graph visualization
    
- Local navigation
    
- Easy editing
    
- Git version control
    
- Reusable content
    

while still allowing an AI agent to follow the same relationships.

---

# 17. Runtime Resolution

At runtime, the Skill should conceptually perform:

```text
Component
    ↓
References
    ↓
Reusable Elements
    ↓
Requirements
    ↓
Controls
    ↓
Platform Implementations
```

The result is not necessarily a new permanent document.

Instead, it becomes a temporary:

> **Resolved Security Knowledge Context**

For example:

```yaml
component: AWS API Gateway
platform: AWS

security_context:

  - concern: Authentication
    requirement:
      - SEC-REQ-AUTH-001
    implementation:
      - IAM
      - Cognito

  - concern: Authorization
    requirement:
      - SEC-REQ-AUTHZ-001
    implementation:
      - IAM Policy
      - RBAC
```

This context is then provided to Goose.

---

# 18. Optional Runtime Database

If the Knowledge Base eventually becomes too large for direct Markdown traversal, a database can be introduced without changing the source model.

The architecture becomes:

```text
Obsidian / Markdown / YAML
             │
             ↓
        Knowledge Loader
             │
             ↓
     PostgreSQL / Graph DB
             │
             ↓
      Runtime Retrieval
```

The database is therefore a **derived runtime representation**, not necessarily the source of truth.

This preserves human readability.

---

# 19. When SQL Becomes Useful

SQL becomes valuable when the system needs questions such as:

```text
Find every component affected by this requirement.

Find every control implementing this requirement.

Find all AWS implementations of this security concern.

Find all components that use this reusable element.

Find all requirements mapped to NIST control X.
```

For a first implementation, PostgreSQL is sufficient for many of these relationships.

If the relationship graph later becomes extremely complex, a graph database can be evaluated.

The important point is:

> **Do not introduce SQL or Graph DB merely because the knowledge has relationships. Introduce them when runtime query requirements justify them.**

---

# 20. Recommended Initial Technology Stack

The recommended V1 stack is:

```text
Human Authoring
    ↓
Obsidian
    ↓
Markdown + YAML Frontmatter
    ↓
Wiki Links / Embedded Reusable Elements
    ↓
Git
    ↓
Security Architecture Skill
    ↓
Goose
```

No database is required initially.

Optional future layer:

```text
Markdown/YAML
      ↓
Knowledge Loader
      ↓
PostgreSQL
      ↓
Runtime Retrieval
```

---

# 21. Security Review / Questionnaire Engine

The Knowledge Base should eventually support not only free-form analysis but also structured Security Architecture Review questionnaires.

The questionnaire engine should not contain all security knowledge itself.

Instead:

```text
Questionnaire
     ↓
Identifies Architecture Characteristics
     ↓
Triggers Security Knowledge Retrieval
     ↓
Produces Security Concerns
     ↓
Maps to Requirements
     ↓
Maps to Controls
```

For example:

```text
Question:
Does the component expose an externally accessible API?

Answer:
Yes

        ↓

Security Concerns:
- Authentication
- Authorization
- Input Validation
- Rate Limiting
```

Then:

```text
Concern
    ↓
Requirement
    ↓
Control
    ↓
Platform-specific Implementation
```

This creates a connection between:

```text
Questionnaire Engine
```

and:

```text
Security Knowledge Library
```

without duplicating the knowledge.

---

# 22. Questionnaire as a Knowledge Trigger

The questionnaire should therefore be viewed as a **retrieval trigger**, not merely a checklist.

Conceptually:

```text
Architecture
      ↓
Questionnaire
      ↓
Architecture Characteristics
      ↓
Knowledge Retrieval
      ↓
Security Concerns
      ↓
Requirements
      ↓
Controls
```

This allows the same Knowledge Base to support:

- Manual security reviews
    
- AI-assisted reviews
    
- Architecture questionnaires
    
- Threat modeling
    
- Security requirement generation
    
- Security control recommendations
    

---

# 23. Final End-to-End Architecture

The complete system can be represented as:

```text
                         HUMAN
                           │
                           ↓
                    ┌─────────────┐
                    │   Obsidian  │
                    │             │
                    │ Markdown    │
                    │ YAML        │
                    │ Wiki Links  │
                    └──────┬──────┘
                           │
                           ↓
                Security Knowledge Library
                           │
            ┌──────────────┼──────────────┐
            ↓              ↓              ↓
       Components       Reusable       Platform
                         Elements      Implementations
            │              │              │
            └──────────────┼──────────────┘
                           ↓
                 Knowledge Relationships
                           │
                           ↓
                  Security Review Skill
                           │
                 ┌─────────┴─────────┐
                 ↓                   ↓
          Retrieval Logic      Review Workflow
                 │                   │
                 └─────────┬─────────┘
                           ↓
                         Goose
                           │
                           ↓
                Security Review / Questionnaire
                           │
                           ↓
                 Resolved Security Context
                           │
                           ↓
              Security Requirements / Controls
                           │
                           ↓
                     Review Findings
```

---

# 24. Future Architecture

Once the first version works, additional components can be introduced:

```text
                         Security Skill Platform
                                  │
          ┌───────────────────────┼───────────────────────┐
          ↓                       ↓                       ↓
     Skill Creator          Knowledge Engine        Evaluation
          │                       │                       │
          ↓                       ↓                       ↓
      SKILL.md                Obsidian                Runner
                                  │                       │
                                  ↓                       ↓
                            Optional DB              Goose
                                                          │
                                                          ↓
                                                       Results
```

Potential future technologies include:

```text
Skill Creator
Harbor
Inspect
PostgreSQL
Graph Database
Vector Retrieval
MCP
Multiple Agent Runtimes
LLM-as-a-Judge
Optimization
```

These should remain optional extensions rather than prerequisites for V1.

---

# 25. Development Strategy

The implementation should proceed incrementally.

## Phase 1 — Knowledge Model

Define:

```text
Component
Security Concern
Security Requirement
Security Control
Implementation
Framework
Pattern
Reusable Element
```

Define relationships between them.

---

## Phase 2 — Human-Readable Knowledge Base

Implement:

```text
Obsidian
+
Markdown
+
YAML frontmatter
+
Wiki links
+
Stable IDs
```

Create several representative components and reusable elements.

---

## Phase 3 — Security Architecture Review Skill

Create the first:

```text
security-architecture-review
```

Skill.

The Skill should define:

- When it should be used
    
- What input it accepts
    
- How to identify components
    
- How to retrieve knowledge
    
- How to resolve reusable elements
    
- How to resolve platform implementations
    
- How to produce the review output
    

---

## Phase 4 — Goose Runtime

Run the Skill through Goose.

The first end-to-end flow should be:

```text
Architecture Description
        ↓
Goose
        ↓
Security Architecture Skill
        ↓
Obsidian Knowledge Base
        ↓
Selective Retrieval
        ↓
Security Analysis
```

---

## Phase 5 — Questionnaire Engine

Add structured questions that help the agent identify architecture characteristics and trigger relevant knowledge retrieval.

---

## Phase 6 — Evaluation

Only after the Skill and Knowledge Base work should evaluation be introduced.

For example:

```text
Skill
  ↓
Goose
  ↓
Security Review
  ↓
Expected Findings
  ↓
Evaluator
```

---

## Phase 7 — Optimization

Only after a working evaluation loop exists should optimization be considered.

Potential future technologies:

```text
Harbor
Inspect
GEPA
LLM-as-a-Judge
Automated Skill Optimization
```

---

# 26. Decision on Anthropic Skill Creator

Anthropic's Skill Creator can be used as a reference or as an optional initial authoring aid.

However, it should not define the architecture of this project.

The reason is that the project's primary challenge is not:

> "How do we generate a SKILL.md?"

The primary challenge is:

> **"How do we model reusable Security Architecture knowledge so that both humans and agents can understand and use it?"**

Once the Knowledge Model and Review Workflow are defined, generating the Skill becomes comparatively straightforward.

Therefore:

```text
Knowledge Model
       ↓
Review Workflow
       ↓
Skill Design
       ↓
SKILL.md
```

is preferred over:

```text
Generic Skill Creator
       ↓
SKILL.md
       ↓
Try to fit Knowledge into it
```

---

# 27. Final Architectural Principles

The final design follows these principles:

### Principle 1 — Human-readable first

Security knowledge must remain easy for Security Architects to read and maintain.

### Principle 2 — Reuse instead of duplication

Common security elements should exist once and be referenced by multiple components.

### Principle 3 — Separate concept from implementation

High-level security concepts remain platform-independent.

AWS, Azure, and GCP implementations are modeled separately.

### Principle 4 — Knowledge and Skill are different

```text
Knowledge = WHAT
Skill = HOW
```

### Principle 5 — Progressive retrieval

The agent should retrieve only the knowledge required for the current review.

### Principle 6 — Obsidian is the initial source of truth

Obsidian + Markdown + YAML + links provides an excellent human-maintainable starting point.

### Principle 7 — Database is optional

PostgreSQL or a graph database can later become a runtime index without replacing the human-readable source.

### Principle 8 — Goose is the first runtime

The Skill should be runtime-agnostic, but Goose is the first implementation target.

### Principle 9 — Don't optimize before the basic loop works

The first milestone is:

```text
Knowledge
   ↓
Skill
   ↓
Goose
   ↓
Security Review
```

Only after this works should we add:

```text
Evaluation
   ↓
Optimization
```

---

# 28. V1 Target

The first working version should therefore be deliberately small:

```text
Obsidian Knowledge Base
        +
Security Architecture Review Skill
        +
Goose
```

with this workflow:

```text
Architecture Input
       ↓
Goose
       ↓
Security Review Skill
       ↓
Identify Component
       ↓
Find Relevant Reusable Elements
       ↓
Resolve Security Concerns
       ↓
Resolve Requirements
       ↓
Resolve Platform Implementation
       ↓
Generate Security Review
```

The most important deliverable of V1 is therefore **not the Skill Creator**.

It is:

> **A well-designed, human-readable Security Architecture Knowledge Model that an Agent Skill can reliably navigate and apply.**

Once that exists, the Skill Creator, database layer, questionnaire engine, evaluation framework, and optimization layer can all be built around the same underlying knowledge model without having to redesign the foundation.
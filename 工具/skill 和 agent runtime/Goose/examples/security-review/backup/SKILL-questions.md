---
name: security-review
description: Analyze a system description, identify relevant security domains and canonical components, determine applicable security concerns, retrieve security requirements, and generate a focused security questionnaire from the Security Knowledge Base.
---

# Security Review Skill

## Objective

Perform a structured security review of a system described by the user.

The workflow is:

System Understanding
→ Security Domain Identification
→ Component Identification
→ Security Concern Identification
→ Security Requirement Retrieval
→ Questionnaire Generation

The Security Knowledge Base is authoritative.

Do not invent Domains, Components, Security Concerns,
Security Requirements, or Questions.

---

# Knowledge Base

The Security Knowledge Base is located at:

knowledge-base/

The Knowledge Base contains:

- domains/
- components/
- concerns/
- requirements/
- questions/

Lightweight indexes are located at:

references/domain-index.md
references/component-index.md

The indexes are used for initial candidate discovery.

---

# Progressive Loading Policy

Do not load the entire Knowledge Base into context.

Use the following loading sequence:

1. Load the Domain Index.
2. Identify relevant Domains.
3. Load only the selected Domain files.
4. Load the Component Index.
5. Identify canonical Components.
6. Load only the selected Component files.
7. Build candidate Security Concerns from Domains and Components.
8. Load only candidate Security Concern files.
9. Determine Concern applicability.
10. Load Requirements associated with applicable Concerns.
11. Load Questions associated with selected Requirements.

Do not read unrelated Knowledge Base files.

---

# Step 1 — Understand the System

Analyze the user's system description.

Extract, when available:

- System purpose
- Major functions
- Users
- External actors
- APIs
- Data
- Sensitive data
- Authentication mechanisms
- Authorization mechanisms
- Cloud services
- Application components
- Databases
- External services
- Deployment environment
- Communication channels

Create an internal System Understanding summary.

Do not make final Security Concern decisions yet.

---

# Step 2 — Identify Security Domains

Read:

references/domain-index.md

Use the index to identify relevant Security Domains.

Do not invent a Domain.

For every selected Domain, record:

- Domain name
- Domain ID
- Evidence from the system
- Reason for selection

Then load the corresponding Domain file from:

knowledge-base/domains/

For example:

Application Security

→ knowledge-base/domains/application-security.md

Identity & Access

→ knowledge-base/domains/identity-access.md

---

# Step 3 — Identify Components

Read:

references/component-index.md

Map entities extracted from the system description
to canonical Components.

Use:

1. Exact name
2. Alias
3. Description
4. System context

Do not invent Components.

For every identified Component:

1. Load its Component file from:

knowledge-base/components/

2. Read its Security Concerns section.

Example:

API Gateway

→ knowledge-base/components/api-gateway.md

AWS Lambda

→ knowledge-base/components/aws-lambda.md

---

# Step 4 — Build Candidate Security Concerns

Candidate Security Concerns come from two sources.

## Domain-derived Concerns

Read the Security Concerns section of each selected
Domain file.

Add those Concerns to the candidate set.

## Component-derived Concerns

Read the Security Concerns section of each selected
Component file.

Add those Concerns to the candidate set.

Merge the two sets.

Remove duplicates.

Do not create additional Component → Concern relationships.

Only use relationships explicitly defined in the Knowledge Base.

---

# Step 5 — Evaluate Security Concern Applicability

For each candidate Security Concern:

Load:

knowledge-base/concerns/<concern>.md

Read:

- Description
- Applicability
- Other applicability guidance

Determine whether the Concern applies to the system.

Use evidence from the user's system description.

For every selected Concern record:

- Concern ID
- Concern Name
- Source
- Evidence
- Applicability Reason

A Concern may have multiple sources:

- Domain
- Component
- Domain + Component

Do not select a Concern solely because
its name resembles a word in the system description.

---

# Step 6 — Retrieve Security Requirements

For every applicable Security Concern:

1. Read its Security Requirements section.
2. Resolve the linked Requirements.
3. Load the corresponding Requirement files from:

knowledge-base/requirements/

Only load Requirements associated with
the selected Security Concerns.

---

# Step 7 — Retrieve Questionnaire Questions

For every selected Requirement:

1. Read its Questionnaire section.
2. Resolve the linked Questions.
3. Load the corresponding Question files from:

knowledge-base/questions/

Only include Questions associated with selected Requirements.

---

# Step 8 — Generate the Questionnaire

Generate a questionnaire organized as:

Security Domain
→ Security Concern
→ Security Requirement
→ Question

For each question include:

- Question ID
- Question
- Related Requirement
- Related Concern
- Evidence Requested

Do not change the meaning of canonical Questions.

---

# Output

Return these sections:

## 1. System Understanding

Summarize the system.

## 2. Identified Components

Include:

| Component | ID | Evidence |
|---|---|---|

## 3. Relevant Security Domains

Include:

| Domain | ID | Evidence | Reason |
|---|---|---|---|

## 4. Applicable Security Concerns

Include:

| Concern | ID | Source | Evidence | Reason |
|---|---|---|---|---|

## 5. Security Requirements

List the selected Requirements.

## 6. Security Questionnaire

Organize questions hierarchically:

Domain
→ Concern
→ Requirement
→ Question

---

# Important Rules

## Canonical Knowledge

The Knowledge Base is authoritative.

Never invent:

- Domains
- Components
- Security Concerns
- Requirements
- Questions

## Component Matching

Prefer:

1. Exact canonical name
2. Alias
3. Strong semantic match supported by context

If the match is ambiguous, report the ambiguity.

## Concern Applicability

A Concern must be supported by:

- Domain membership,
- Component relationship,
- Applicability criteria,
- and evidence from the system description.

## Progressive Loading

Only load files required for the current analysis.

## Traceability

Maintain:

System Evidence
→ Domain
→ Component / Concern
→ Requirement
→ Question
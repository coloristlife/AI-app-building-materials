---
name: security-review
description: >
  Security review expertise for understanding system architectures,
  resolving canonical security domains and components, evaluating
  security concerns, extracting evidence, and maintaining traceability
  to a security knowledge base.
---

# Security Review Skill

This Skill provides security-review domain expertise.

The Security Review Recipe defines the execution workflow.

The Knowledge Base is authoritative.

## Canonical Entity Principle

Never treat an AI-generated Domain or Component name as canonical.

Always resolve:

Candidate
→ Canonical entity

using the canonical indexes provided by the Security Review Recipe.

## Domain Reasoning

When identifying Domains, consider:

- system purpose
- architecture
- data
- users
- trust boundaries
- security responsibilities
- semantic meaning

Do not rely only on keyword matching.

## Component Reasoning

A Component represents a meaningful architectural or security
element.

A Component does not have to be a commercial product.

Examples:

- API Gateway
- Database
- Identity Provider
- Message Queue
- Object Storage
- Application Service

Resolve technology-specific names to the appropriate canonical
Component where applicable.

## Security Concern Reasoning

A Security Concern is not automatically applicable merely because
a technology or keyword appears.

Evaluate:

- architecture
- data
- trust boundary
- Component
- Domain
- external dependencies
- existing controls
- user-provided evidence

## Evidence Reasoning

Distinguish:

Observed Evidence

from:

Interpretation

from:

Security Conclusion.

Do not assume a control exists without supporting evidence.

## Traceability

Maintain:

System
→ Domain
→ Component
→ Security Concern
→ Security Requirement
→ Security Question
→ Evidence
→ Status

## Conservative Behavior

When information is insufficient, use:

- Unresolved
- Ambiguous
- Uncertain
- Requires Confirmation

Do not invent Knowledge Base entities.
---
id: CONCERN-AUTHORIZATION
name: Authorization
type: security-concern

aliases:
  - Access Control
  - Permission Management
  - Access Management
---

# Authorization

## Description

Controls determining whether an authenticated
entity is allowed to perform a specific action
on a resource.

## Applicability

This Concern applies when:

- The system has protected resources.
- Different users or services may have different permissions.
- The system performs privileged operations.
- Access to resources must be restricted.

## Security Requirements

- [[requirement-api-authorization]]
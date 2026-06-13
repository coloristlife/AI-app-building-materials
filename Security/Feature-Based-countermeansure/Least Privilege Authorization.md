Here is the security review questionnaire for **Identity & Access Management **, organized into logical architectural categories. These questions are designed to enforce strict access boundaries, prevent lateral movement, and align with frameworks like NIST SP 800-53 (AC family), OWASP Top 10 (A01:2021-Broken Access Control), and ISO 27001.

### Authorization Architecture and Granularity
*Focuses on the foundational design of how permissions are structured, evaluated, and assigned to human users.*

- **Question:** How is the principle of least privilege enforced at the application and infrastructure layers, and is access granted based on explicitly defined roles and attributes rather than broad, default permissions?
  - **Recommended Control:** Implementation of granular Role-Based Access Control (RBAC) or Attribute-Based Access Control (ABAC) anchored in a "default deny" posture, ensuring users are granted only the absolute minimum permissions required to perform their specific business tasks.
  - **Associated Risk:** Over-privileged accounts allow users to access sensitive data or perform destructive actions outside their job function, massively increasing the blast radius of both malicious insider threats and compromised external accounts.

### Privileged Access and Just-In-Time (JIT) Escalation


- **Question:** Is a principle of zero standing privilege enforced for all administrative and highly privileged access across critical infrastructure components ([placeholder for all relevant services or their features]), meaning that elevated permissions are granted strictly on a temporary, Just-in-Time (JIT) basis that requires a documented business justification, explicit peer approval, step-up Multi-Factor Authentication (MFA), and the generation of a comprehensive audit trail rather than utilizing permanent "SuperUser" accounts?
  - **Recommended Control:** Implementation of a central Privileged Access Management (PAM) or Just-In-Time (JIT) access solution that replaces persistent administrative credentials with ephemeral, time-to-live (TTL) bound sessions. Access requests must require a documented reason correlated with a change ticket, multi-party (peer) approval workflows, mandatory step-up MFA prior to escalation, and complete session auditing (e.g., command logging or video recording).
  - **Associated Risk:** Persistent, static administrative credentials ("standing privileges") represent a high-value target for threat actors. If a single privileged credential is compromised, it grants an attacker long-term, unfettered access to the entire critical infrastructure, allowing them to bypass other security controls, move laterally, exfiltrate data, and cause catastrophic system damage without triggering anomalous privilege escalation alerts.


### Service-to-Service (Workload) Identity
*Focuses on restricting the permissions of non-human entities, such as APIs, background jobs, and microservices.*

- **Question:** How are non-human identities (e.g., service accounts, background workers, CI/CD pipelines) authorized to interact with other internal components, data stores, or cloud resources?
  - **Recommended Control:** Use of workload identity federation or strictly scoped IAM roles assigned per microservice/function. API interactions must rely on granular scopes (e.g., `read-only` vs. `read-write` on specific endpoints) rather than relying on shared, global, or highly privileged "God-mode" service accounts.
  - **Associated Risk:** A Server-Side Request Forgery (SSRF) or Remote Code Execution (RCE) attack on a single, low-tier microservice can be weaponized to dump backend databases or destroy infrastructure if the service account possesses overly broad permissions.

### Data-Level Isolation and Object-Level Authorization
*Focuses on edge cases involving multi-tenancy and the prevention of lateral data access.*

- **Question:** In multi-tenant or shared-data environments, how does the system ensure that a user authorized within one logical boundary cannot manipulate parameters (e.g., object IDs, API paths) to access or modify resources belonging to another user or tenant?
  - **Recommended Control:** Rigorous, server-side context validation on every single request to ensure the authenticated user owns or is explicitly authorized to interact with the requested object (preventing OWASP Broken Object Level Authorization / Insecure Direct Object References).
  - **Associated Risk:** Broken Access Control vulnerabilities allow attackers with basic, valid user privileges to horizontally escalate and siphon highly sensitive data (PII, financial records) belonging to other clients, completely breaking tenant isolation.

### Access Governance and Lifecycle Management
*Focuses on continuous auditing and the prevention of privilege creep over time.*

- **Question:** What automated processes are in place to instantly revoke access when a user changes roles or leaves the organization, and how frequently are existing authorizations audited?
  - **Recommended Control:** Automated lifecycle management integrated directly with HR/Identity systems (Joiner/Mover/Leaver workflows), coupled with mandatory, automated periodic access reviews (e.g., quarterly) requiring data owners to re-certify or revoke access rights.
  - **Associated Risk:** Privilege creep occurs over time as employees change departments but retain legacy access. This results in dormant, over-privileged, or orphaned accounts remaining active, which are routinely targeted by attackers for silent network infiltration. 

### Client-Side vs. Server-Side Enforcement
*Focuses on ensuring authorization cannot be bypassed by client-side manipulation.*

- **Question:** Are all authorization decisions and permission checks enforced securely on the backend server, or does the system rely on hiding UI elements or client-side tokens to restrict access to privileged functions?
  - **Recommended Control:** Strict server-side enforcement of all authorization rules. UI elements (like admin buttons) can be hidden for UX purposes, but the backend API must independently verify the user's roles and permissions before executing any requested business logic.
  - **Associated Risk:** Attackers can easily bypass UI-based restrictions by directly querying backend APIs via tools like Postman or Burp Suite, allowing unauthorized execution of administrative functions.
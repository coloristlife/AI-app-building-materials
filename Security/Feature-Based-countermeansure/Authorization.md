**Authorization (AuthZ)**

Authorization represents one of the most critical security boundaries in any application, acting as the primary defense against Broken Access Control (which has consistently ranked #1 on the OWASP Top 10). This questionnaire evaluates the system's enforcement of the Principle of Least Privilege, Zero Trust architecture, data segregation, and edge-case handling.



### Architectural Design & Core Principles

- **Question:** Is authorization enforced centrally through a dedicated Policy Enforcement Point (PEP) and Policy Decision Point (PDP), or is access control logic scattered across individual functions/components?
  - **Recommended Control:** Implement a centralized, standardized authorization framework or middleware (e.g., OPA, AWS Cedar, or framework-native security filters) that enforces access policies uniformly across all routes and services.
  - **Associated Risk:** If authorization logic is scattered or duplicated, developers may forget to apply it to new endpoints, leading to authorization bypasses, inconsistent policy enforcement, and high maintenance overhead.

- **Question:** Does the system adhere strictly to a "Default Deny" posture for all resources and endpoints?
  - **Recommended Control:** Configure the application routing and API gateways to deny access to all endpoints by default. Specific endpoints must require explicit rules, roles, or scopes to be exposed and accessible.
  - **Associated Risk:** Adopting a "Default Allow" posture introduces severe risks where newly created, unreviewed, or hidden administrative endpoints are immediately accessible to unauthorized actors.

- **Question:** In the event of a failure within the authorization service or database (e.g., timeouts, service outages), does the system "fail closed" or "fail open"?
  - **Recommended Control:** Implement Fail-Safe Defaults. If the system cannot reliably determine a user's permissions due to an error, the transaction must be blocked, and an exception logged.
  - **Associated Risk:** Failing "open" allows users to bypass authorization checks during network outages or under heavy load (which an attacker could intentionally trigger via DoS attacks).

### Data & Record-Level Authorization (BOLA / IDOR)

- **Question:** How does the application verify that the authenticated user genuinely owns or has explicit permission to access the specific database record being requested (e.g., `GET /api/documents/1234`)?
  - **Recommended Control:** Implement robust Server-Side Record-Level Access Control. Use direct object references mapped against the user's session context (e.g., checking `document.owner_id == session.user_id`) rather than blindly trusting the ID provided in the URL or payload. Ensure mitigation of Broken Object Level Authorization (BOLA) / Insecure Direct Object Reference (IDOR).
  - **Associated Risk:** Attackers can manipulate predictable identifiers (like sequential integers) in the API request to access, modify, or delete sensitive data belonging to other users or tenants.

- **Question:** In a multi-tenant environment, how is data boundary isolation enforced at the data layer to prevent a user in Tenant A from querying or mutating data in Tenant B?
  - **Recommended Control:** Enforce tenant isolation via Row-Level Security (RLS) at the database tier, tenant-specific schema/databases, or strict filtering in the ORM/data access layer utilizing a trusted tenant ID derived from the server-side authentication token.
  - **Associated Risk:** Cross-tenant data leakage or corruption, resulting in massive regulatory compliance breaches (e.g., GDPR, HIPAA) and total loss of customer trust.

### Function & Endpoint-Level Authorization (BFLA)

- **Question:** How are privileged functions (e.g., administration panels, user provisioning, system configuration) protected from execution by standard users?
  - **Recommended Control:** Implement Role-Based Access Control (RBAC) or Attribute-Based Access Control (ABAC) verified continuously on the backend for every privileged request. Prevent Broken Function Level Authorization (BFLA) by never relying solely on hiding UI elements.
  - **Associated Risk:** Attackers discovering the URL or API endpoint for administrative actions can invoke them directly via automated tools (e.g., Postman, Burp Suite) bypassing UI restrictions entirely.

- **Question:** If a user’s role or access level is changed (e.g., downgraded or revoked by an administrator), how quickly is this change reflected in their active sessions?
  - **Recommended Control:** Implement short-lived access tokens combined with continuous evaluation of privileges, or utilize a token revocation list/event-driven caching invalidation. Minimize the Time-of-Check to Time-of-Use (TOCTOU) gap.
  - **Associated Risk:** A terminated employee or a user whose permissions have been downgraded may retain access to sensitive systems and data until their existing token or session naturally expires, leading to insider threat exploitation.

### Token Management & Claims (OAuth2 / JWT)

- **Question:** When processing authorization via tokens (e.g., JWTs), does the backend cryptographically verify the signature, issuer, audience, and expiration before trusting the embedded authorization scopes/claims?
  - **Recommended Control:** Use established, secure libraries to validate JWTs. Enforce strict checks on the `alg` header (preventing 'None' algorithm attacks or symmetric/asymmetric confusion), and validate the `exp`, `iss`, and `aud` claims. 
  - **Associated Risk:** Attackers may craft forged tokens, alter their permissions (e.g., changing `"role": "user"` to `"role": "admin"`), or replay expired tokens to gain unauthorized access to the system.

- **Question:** Are authorization scopes and claims securely mapped to backend actions, and do you avoid trusting user-supplied parameters to dictate privilege?
  - **Recommended Control:** Derive the user's role and scopes solely from the cryptographically signed, server-issued token. Never trust parameters like `?isAdmin=true` or POST body fields that dictate role assignment during resource creation/modification.
  - **Associated Risk:** Mass Assignment or Parameter Tampering vulnerabilities where an attacker manipulates API requests to elevate their privileges horizontally or vertically.

### Service-to-Service Authorization & Zero Trust

- **Question:** In microservice architectures, how is authorization enforced when Service A requests data from Service B on behalf of a user?
  - **Recommended Control:** Implement Service-to-Service authentication and authorization (e.g., mTLS with SPIFFE/SPIRE) AND propagate the original user's context (e.g., via OAuth Token Exchange / RFC 8693) so Service B can perform its own authorization checks. 
  - **Associated Risk:** The "Confused Deputy" problem. If Service B implicitly trusts Service A without verifying the underlying user's permissions, an attacker who compromises or exploits Service A can freely access all data in Service B.

- **Question:** Does the system rely on network location (e.g., internal IP addresses or VPN subnets) as a substitute for proper authorization checks?
  - **Recommended Control:** Adopt a Zero Trust Architecture (NIST SP 800-207). Never bypass authorization checks simply because a request originates from an internal network or trusted IP range.
  - **Associated Risk:** If the internal network perimeter is breached (e.g., via a phishing attack or SSRF vulnerability), attackers can move laterally without restriction, as internal applications lack access control defenses.

### Access Lifecycle, Governance & Edge Cases

- **Question:** How is hierarchical or inherited authorization handled, and are there edge cases where child resources do not properly inherit the restricted state of parent resources?
  - **Recommended Control:** Implement unified hierarchical permission resolution in the PDP. Ensure that if access to a parent container (e.g., a Project folder) is revoked, access to all child objects (e.g., files inside the folder) is explicitly and immediately revoked.
  - **Associated Risk:** Orphaned permissions. A user loses access to a project but retains direct API access to files within the project, resulting in covert data leakage.

- **Question:** Is there a process for granting Just-In-Time (JIT) access or temporary "Break-Glass" emergency access to highly privileged accounts, and how is it constrained?
  - **Recommended Control:** Implement JIT provisioning for privileged roles requiring managerial approval, bounded by strict time limits, and requiring MFA. All break-glass account usage must trigger immediate, non-repudiable alerts to security teams.
  - **Associated Risk:** Standing privileges (always-on admin accounts) are highly attractive targets for compromise. Without JIT, the attack surface for credential theft and subsequent system-wide compromise remains permanently high.

### Auditing, Logging & Monitoring

- **Question:** Are authorization failures (e.g., an authenticated user attempting to access a resource they are not permitted to see) explicitly logged with adequate context?
  - **Recommended Control:** Log all authorization decisions (both grants and denials) securely. Logs must include the timestamp, authenticated identity, requested resource, evaluated policy/role, and the outcome. Ensure logs are forwarded to a central SIEM.
  - **Associated Risk:** Without detailed AuthZ logging, security teams have zero visibility into internal threat actors or compromised accounts probing the API for broken access control vulnerabilities. 

- **Question:** Are there active alerting mechanisms designed to detect authorization probing or scraping?
  - **Recommended Control:** Implement rate limiting and behavioral alerting on repeated 403 Forbidden or 401 Unauthorized errors from a single user, tenant, or IP address.
  - **Associated Risk:** Attackers frequently use automated tools to enumerate predictable IDs (IDOR scanning). Without alerting on mass 403s, the attacker will eventually find a vulnerability or valid ID undisturbed.
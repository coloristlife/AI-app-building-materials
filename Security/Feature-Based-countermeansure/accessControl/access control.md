
### Authentication (Identity Verification)

- **Question:** Is Multi-Factor Authentication (MFA) enforced for all human users across all ingress points (e.g., VPNs, web portals, administrative interfaces)?
  - **Recommended Control:** Phishing-resistant MFA (e.g., FIDO2, WebAuthn, hardware tokens) should be universally enforced.
  - **Associated Risk:** Without MFA, systems are highly vulnerable to credential stuffing, password spraying, and phishing attacks, leading to full Account Takeover (ATO).

- **Question:** How are non-human identities (e.g., service accounts, API tokens, CI/CD pipelines) authenticated, and are their credentials periodically rotated?
  - **Recommended Control:** Implement a centralized secrets management solution (e.g., HashiCorp Vault, AWS Secrets Manager) with automated, short-lived credential rotation and machine-to-machine authentication protocols like OAuth 2.0 (Client Credentials Grant) or OIDC.
  - **Associated Risk:** Static, long-lived service account credentials are a primary target for attackers. If compromised, they often provide undetected, highly privileged access.

- **Question:** Are password policies aligned with current NIST guidelines (e.g., checking against known breached passwords, no arbitrary complexity rules, no arbitrary expiration without compromise)?
  - **Recommended Control:** Active integration with breached-password feeds (e.g., HaveIBeenPwned API or enterprise equivalents) and enforcement of a minimum length (e.g., 12+ characters) rather than strict rotation rules.
  - **Associated Risk:** Users using easily guessable or previously compromised passwords from other breaches can bypass authentication controls.

- **Question:** Is a "Step-Up Authentication" mechanism implemented when a user attempts to perform a highly sensitive action (e.g., changing bank details, exporting bulk data, deleting resources)?
  - **Recommended Control:** Context-aware authentication that prompts for an additional MFA challenge or re-authentication before executing critical transactions.
  - **Associated Risk:** If an active session is hijacked (e.g., via Cross-Site Scripting or a stolen session cookie), the attacker can perform destructive or financially damaging actions without secondary verification.

### Authorization (Permissions & Privileges)

- **Question:** How is the Principle of Least Privilege (PoLP) enforced across the application and infrastructure?
  - **Recommended Control:** Implement Role-Based Access Control (RBAC) or Attribute-Based Access Control (ABAC), ensuring users and services are granted only the minimum permissions necessary to perform their stated functions.
  - **Associated Risk:** Over-privileged users or applications increase the blast radius of a potential compromise, allowing an attacker to move laterally or access sensitive data unnecessarily.

- **Question:** Is a "Default Deny" posture applied to all access requests, firewall rules, and API endpoints?
  - **Recommended Control:** Zero Trust architecture principles where access to any resource is implicitly denied unless explicitly explicitly authorized by a policy.
  - **Associated Risk:** "Default Allow" configurations frequently result in misconfigurations where sensitive endpoints, internal services, or administrative ports are inadvertently exposed to the internet or unauthorized internal users.
  
- **Question:** In the event of a failure within the authorization service or database (e.g., timeouts, service outages), does the system "fail closed" or "fail open"?
  - **Recommended Control:** Implement Fail-Safe Defaults. If the system cannot reliably determine a user's permissions due to an error, the transaction must be blocked, and an exception logged.
  - **Associated Risk:** Failing "open" allows users to bypass authorization checks during network outages or under heavy load (which an attacker could intentionally trigger via DoS attacks).



### Data & Record-Level Authorization (BOLA / IDOR)
- **Question:** In multi-tenant or shared-data environments, how does the system ensure that a user authorized within one logical boundary cannot manipulate parameters (e.g., object IDs, API paths) to access or modify resources belonging to another user or tenant?
  - **Recommended Control:** Rigorous, server-side context validation on every single request to ensure the authenticated user owns or is explicitly authorized to interact with the requested object (preventing OWASP Broken Object Level Authorization / Insecure Direct Object References).
  - **Associated Risk:** Broken Access Control vulnerabilities allow attackers with basic, valid user privileges to horizontally escalate and siphon highly sensitive data (PII, financial records) belonging to other clients, completely breaking tenant isolation.
  

- **Question:** In a multi-tenant environment, how is data boundary isolation enforced at the data layer to prevent a user in Tenant A from querying or mutating data in Tenant B?
  - **Recommended Control:** Enforce tenant isolation via Row-Level Security (RLS) at the database tier, tenant-specific schema/databases, or strict filtering in the ORM/data access layer utilizing a trusted tenant ID derived from the server-side authentication token.
  - **Associated Risk:** Cross-tenant data leakage or corruption, resulting in massive regulatory compliance breaches (e.g., GDPR, HIPAA) and total loss of customer trust.


### Function & Endpoint-Level Authorization (BFLA)



- **Question:** If a user’s role or access level is changed (e.g., downgraded or revoked by an administrator), how quickly is this change reflected in their active sessions?
  - **Recommended Control:** Implement short-lived access tokens combined with continuous evaluation of privileges, or utilize a token revocation list/event-driven caching invalidation. Minimize the Time-of-Check to Time-of-Use (TOCTOU) gap.
  - **Associated Risk:** A terminated employee or a user whose permissions have been downgraded may retain access to sensitive systems and data until their existing token or session naturally expires, leading to insider threat exploitation.





### Client-Side vs. Server-Side Enforcement
*Focuses on ensuring authorization cannot be bypassed by client-side manipulation.*

- **Question:** Are all authorization decisions and permission checks enforced securely on the backend server, or does the system rely on hiding UI elements or client-side tokens to restrict access to privileged functions?
  - **Recommended Control:** Strict server-side enforcement of all authorization rules. UI elements (like admin buttons) can be hidden for UX purposes, but the backend API must independently verify the user's roles and permissions before executing any requested business logic.
  - **Associated Risk:** Attackers can easily bypass UI-based restrictions by directly querying backend APIs via tools like Postman or Burp Suite, allowing unauthorized execution of administrative functions.

### Identity Lifecycle Management

- **Question:** What is the specific timeline and automated mechanism for deprovisioning access when an employee or contractor leaves the organization?
  - **Recommended Control:** Automated synchronization between the HR Information System (HRIS) and the Identity Provider (IdP) to revoke access immediately (or within a strictly defined SLA of < 24 hours) upon termination.
  - **Associated Risk:** Former employees or contractors retaining access (orphan accounts) pose a massive insider threat and compliance violation.

- **Question:** Are periodic access reviews (User Access Recertification) conducted for all systems, especially for privileged roles?
  - **Recommended Control:** Implement a formal, auditable periodic access review (PAR) process (at least quarterly for privileged users, annually for standard users) requiring managers or system owners to validate the continued need for access.
  - **Associated Risk:** Over time, users accumulate permissions as they change roles ("privilege creep"), resulting in individuals holding excessive, unnecessary access rights.

- **Question:** How are dormant or inactive accounts detected and managed?
  - **Recommended Control:** Automated scripts or IdP policies that disable accounts after a period of inactivity (e.g., 30-60 days) and delete or archive them after 90 days.
  - **Associated Risk:** Unmonitored, active accounts belonging to users who no longer use the system serve as easy, low-noise entry points for threat actors.


### Service-to-Service Authorization & Zero Trust
*Focuses on restricting the permissions of non-human entities, such as APIs, background jobs, and microservices.*

- **Question:** How are non-human identities (e.g., service accounts, background workers, CI/CD pipelines) authorized to interact with other internal components, data stores, or cloud resources?
  - **Recommended Control:** Use of workload identity federation or strictly scoped IAM roles assigned per microservice/function. API interactions must rely on granular scopes (e.g., `read-only` vs. `read-write` on specific endpoints) rather than relying on shared, global, or highly privileged "God-mode" service accounts.
  - **Associated Risk:** A Server-Side Request Forgery (SSRF) or Remote Code Execution (RCE) attack on a single, low-tier microservice can be weaponized to dump backend databases or destroy infrastructure if the service account possesses overly broad permissions.
- **Question:** In microservice architectures, how is authorization enforced when Service A requests data from Service B on behalf of a user?
  - **Recommended Control:** Implement Service-to-Service authentication and authorization (e.g., mTLS with SPIFFE/SPIRE) AND propagate the original user's context (e.g., via OAuth Token Exchange / RFC 8693) so Service B can perform its own authorization checks. 
  - **Associated Risk:** The "Confused Deputy" problem. If Service B implicitly trusts Service A without verifying the underlying user's permissions, an attacker who compromises or exploits Service A can freely access all data in Service B.

- **Question:** Does the system rely on network location (e.g., internal IP addresses or VPN subnets) as a substitute for proper authorization checks?
  - **Recommended Control:** Adopt a Zero Trust Architecture (NIST SP 800-207). Never bypass authorization checks simply because a request originates from an internal network or trusted IP range.
  - **Associated Risk:** If the internal network perimeter is breached (e.g., via a phishing attack or SSRF vulnerability), attackers can move laterally without restriction, as internal applications lack access control defenses.




### Auditing, Logging, and Monitoring

- **Question:** Are all access control events (successful logins, failed logins, password resets, privilege escalations, permission modifications) logged comprehensively?
  - **Recommended Control:** Centralized logging to a SIEM with a standardized log schema that captures Who, What, When, Where, and Outcome, synchronized via NTP.
  - **Associated Risk:** Inadequate logging prevents security teams from detecting active attacks, investigating post-breach activities, and satisfying forensic and regulatory requirements.



- **Question:** Are authorization failures (e.g., an authenticated user attempting to access a resource they are not permitted to see) explicitly logged with adequate context?
  - **Recommended Control:** Log all authorization decisions (both grants and denials) securely. Logs must include the timestamp, authenticated identity, requested resource, evaluated policy/role, and the outcome. Ensure logs are forwarded to a central SIEM.
  - **Associated Risk:** Without detailed AuthZ logging, security teams have zero visibility into internal threat actors or compromised accounts probing the API for broken access control vulnerabilities. 

- **Question:** Are there active alerting mechanisms designed to detect authorization probing or scraping?
  - **Recommended Control:** Implement rate limiting and behavioral alerting on repeated 403 Forbidden or 401 Unauthorized errors from a single user, tenant, or IP address.
  - **Associated Risk:** Attackers frequently use automated tools to enumerate predictable IDs (IDOR scanning). Without alerting on mass 403s, the attacker will eventually find a vulnerability or valid ID undisturbed.



- **Question:** Are log files protected from tampering or deletion by privileged users?
  - **Recommended Control:** Ship logs in near-real-time to an immutable, append-only storage environment residing in a separate, tightly controlled security boundary.
  - **Associated Risk:** Attackers who compromise administrative accounts will routinely attempt to delete or alter logs to cover their tracks and maintain persistence.

- **Question:** What alerting rules are in place for anomalous access behaviors (e.g., impossible travel, brute-force attempts, access from unusual IP/Geo locations)?
  - **Recommended Control:** User and Entity Behavior Analytics (UEBA) or static SIEM rules that trigger high-fidelity alerts to the Security Operations Center (SOC) based on predefined access anomalies.
  - **Associated Risk:** Without proactive alerting, unauthorized access can go undetected for months, allowing attackers to thoroughly explore the network and exfiltrate data.

### Privileged Access Management (PAM)

- **Question:** Is a principle of zero standing privilege enforced for all administrative and highly privileged access across critical infrastructure components, meaning that elevated permissions are granted strictly on a temporary, Just-in-Time (JIT) basis that requires a documented business justification, explicit peer approval, step-up Multi-Factor Authentication (MFA), and the generation of a comprehensive audit trail rather than utilizing permanent "SuperUser" accounts?
  - **Recommended Control:** Implementation of a central Privileged Access Management (PAM) or Just-In-Time (JIT) access solution that replaces persistent administrative credentials with ephemeral, time-to-live (TTL) bound sessions. Access requests must require a documented reason correlated with a change ticket, multi-party (peer) approval workflows, mandatory step-up MFA prior to escalation, and complete session auditing (e.g., command logging or video recording).
  - **Associated Risk:** Persistent, static administrative credentials ("standing privileges") represent a high-value target for threat actors. If a single privileged credential is compromised, it grants an attacker long-term, unfettered access to the entire critical infrastructure, allowing them to bypass other security controls, move laterally, exfiltrate data, and cause catastrophic system damage without triggering anomalous privilege escalation alerts.

- **Question:** Are administrative interfaces logically isolated from standard user networks and the public internet?
  - **Recommended Control:** Implement network segmentation, requiring access to administrative panels via a secured jump host, bastion server, or a zero-trust network access (ZTNA) tunnel.
  - **Associated Risk:** Exposing administrative interfaces to broad networks dramatically increases the attack surface for brute-force attacks, zero-day exploits, and unauthorized access.

- **Question:** Is "Separation of Duties" (SoD) enforced for highly sensitive configurations (e.g., modifying security policies, creating new admin accounts)?
  - **Recommended Control:** Implement multi-party authorization (e.g., Quorum / "Two-man rule") requiring at least two authorized individuals to approve and execute critical system changes.
  - **Associated Risk:** A single rogue administrator, or a single compromised admin account, could unilaterally dismantle security controls or exfiltrate sensitive data.


### Authorization for Priviledged Functions & Endpoints

- **Question:** How are privileged functions (e.g., administration panels, user provisioning, system configuration) protected from execution by standard users?
  - **Recommended Control:** Implement Role-Based Access Control (RBAC) or Attribute-Based Access Control (ABAC) verified continuously on the backend for every privileged request. Prevent Broken Function Level Authorization (BFLA) by never relying solely on hiding UI elements.
  - **Associated Risk:** Attackers discovering the URL or API endpoint for administrative actions can invoke them directly via automated tools (e.g., Postman, Burp Suite) bypassing UI restrictions entirely.
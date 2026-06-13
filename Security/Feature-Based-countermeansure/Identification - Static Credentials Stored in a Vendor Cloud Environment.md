### Machine-to-Machine (M2M) Authentication & Bootstrapping (P0)
**Question**: How does an MCP client authenticate to vendor to retrieve its assigned API keys when API keys stored by vendor? Do you support attestation-based authentication (e.g., AWS IAM roles, Azure Managed Identity, or K8s Service Accounts) so that the  client can bootstrap its session without needing a long-lived, static 'Token' or 'Master Password' stored in its local environment?

- **Associated Risk**: The "Secret Zero" problem. If the client requires a static secret just to talk to the vendor, that secret becomes a high-value target. If stolen, an attacker can impersonate the machine and drain all secrets it has access to.

### Runtime Injection vs. Persistent Storage (p1)
**Question**: Does the solution allow for dynamic injection of API keys directly into the MCP process memory at runtime (via SDK or CLI), ensuring that the credentials never touch the persistent disk, .env files, or the shell history of the host machine?
- **Associated Risk**: Static credentials stored in configuration files or environment variables are frequently leaked through logs, crash dumps, or unauthorized filesystem access. Runtime injection limits the "blast radius" to the life of the process.



### Identity and Access Management (IAM)
**Question**: Is the Principle of Least Privilege (PoLP) strictly enforced for service roles, application identities, and human operators, ensuring that programmatic access to decrypt or retrieve customer credentials is computationally restricted to strictly necessary components? 
- **Associated Risk**: Privilege escalation, lateral movement, and unauthorized insider or compromised-service access to highly sensitive customer secrets.

### Tenant Isolation & Multi-Tenancy Security
Granular Access Scoping (Least Privilege) (p1)
**Question**: Can the vault restrict a tenant's access to specific sub-keys or scopes within a vault, rather than granting access to the entire vault, and can these permissions be restricted by IP address, CIDR block, or specific machine metadata?
- **Associated Risk**: Over-privileged non-human identities. lateral movement.


**Question**: Is strict logical isolation enforced at the data query layer (e.g., Row-Level Security [RLS], strict partitioning, or distinct table/schema architectures) to physically or logically guarantee that queries executing on behalf of Tenant A cannot retrieve Tenant B’s secrets (e.g. Ciphertext for  (Envelope Encryption) or Pointer to the secret in the external vault)? 
- **Associated Risk**: Insecure Direct Object Reference (IDOR) vulnerabilities or application logic flaws allowing one malicious or compromised tenant to harvest other tenants' credentials.

**Question**: Are all customer static credentials and sensitive system data encrypted at rest using strong, industry-standard algorithms (e.g., AES-256) with customer-managed keys (CMK) or dedicated Hardware Security Modules (HSM), ensuring that the application must explicitly request a specific tenant's key to decrypt their corresponding data? ?
- **Associated Risk**: Massive credential theft, unauthorized access to customer environments, and total loss of confidentiality in the event of a storage or backup compromise.


**Question**: Is strong authentication, including mandatory, un-phishable Multi-Factor Authentication (MFA) and Single Sign-On (SSO), strictly required for any administrative, break-glass, or operational access to systems interacting with customer secrets?
- **Associated Risk**: Account takeover, credential stuffing, and unauthorized administrative access to the vendor control plane.



### Automated Secret lifecycle (The "Ephemeral" Goal) (P2)
**Question**: Does the provider offer automated rotation/revocation for the static API keys it stores? Specifically, can it trigger a rotation/revocation of the downstream API key (e.g., a GitHub PAT or OpenAI key) without requiring a manual update by a human?
- **Associated Risk**: Stale credentials. Non-human identities often use keys that remain active for years. If a key is leaked but not rotated, it provides a persistent backdoor for attackers.

### Non-Human Attribution & Audit Logging (P2)
**Question**: Does the audit log distinguish between actions taken by a human administrator (who created the secret) and the non-human identity (that retrieved it), providing full telemetry on which machine accessed which secret at what specific timestamp?
- **Associated Risk**: Loss of accountability. If multiple agents use a shared service account, or if logs only show "User X accessed the vault," you cannot perform forensic analysis to determine which specific MCP client was compromised.

### Client-Side Decryption for Automation (P0)
**Question**: For the automation gateway (the component that delivers secrets to the MCP client), is the data encrypted end-to-end such that the vendor’s infrastructure only sees encrypted blobs, with the final decryption happening only within your trusted network/environment?
- **Associated Risk**: Vendor compromise. If the vendor’s secrets automation relay is breached, and they perform decryption on their side, the attacker gains access to every API key and credential stored for your entire automation fleet.



### Logging and Monitoring
**Question**: When it comes to the use case of storing sensitive credentials (e.g., API keys), do your central monitoring and auditing systems explicitly log the "Tenant ID" and timestamp alongside every secret creation/retrieval, decryption, and administrative event to ensure rapid detection of cross-tenant access attempts? (e.g., Centralized SIEM, Application Logs, AWS CloudTrail).
- **Associated Risk**: Inability to accurately attribute malicious activity to a specific tenant, making it impossible to detect or investigate lateral movement between customer boundaries. Without Tenant ID tagging, a "noisy" or compromised tenant in one environment could potentially probe other tenants without the vendor’s security team being able to pinpoint the source or scope of the leak.


### Vendor / Third-Party Security & Assurance
**Question**: If the vendor manages the cloud environment where credentials reside, are vendor security assurances validated and kept current (e.g., audit reports/certifications), including breach notification terms, logging/audit export capabilities(vendor's ability to let the customer extract or stream security logs out of their platform and into customer’s own security monitoring systems)? 
(Scope: vendor cloud provider, managed service providers, SaaS platforms storing/handling your static credentials.)
- **Associated Risk**: Third-party compromise with limited visibility; contractual gaps blocking incident response; inability to meet internal security requirements.


(overlap with network security)
### Network Security & Isolation 
**Question**: Are the environments housing customer static credentials strictly isolated within private networks/VPCs, enforcing micro-segmentation and prohibiting any direct inbound routing from the public internet? (For example, AWS Secrets Manager, PostgreSQL Database, Internal EKS/Microservices)
- **Associated Risk**: Direct external exploitation of data stores, unauthorized network traversal, and data exfiltration.



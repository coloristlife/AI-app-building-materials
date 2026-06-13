

Here is a comprehensive security review questionnaire designed to evaluate the security posture, configuration, and governance of an **Azure Active Directory (Azure AD / Microsoft Entra ID)** environment. 

### Authentication & Conditional Access
*This section evaluates the foundational identity perimeter, ensuring robust authentication mechanisms and context-aware access controls.*

- **Question:** How does the tenant enforce Multi-Factor Authentication (MFA), and what mitigations are in place to prevent MFA fatigue (prompt bombing) attacks?
  - **Recommended Control:** Enforce MFA via Conditional Access Policies (CAPs) for all users. Implement "Number Matching" for the Microsoft Authenticator app, enforce location/context-aware constraints, and disable SMS/Voice-based MFA in favor of FIDO2 or Authenticator apps.
  - **Associated Risk:** Without number matching and rate limiting, an attacker with compromised credentials can spam the user with MFA prompts until the user experiences fatigue and accidentally approves the fraudulent request.

- **Question:** Are legacy authentication protocols (e.g., POP3, IMAP, authenticated SMTP, older Office clients) actively blocked across the entire tenant?
  - **Recommended Control:** A tenant-wide Conditional Access Policy explicitly blocking legacy authentication clients, supplemented by disabling basic authentication in Exchange Online.
  - **Associated Risk:** Legacy authentication protocols do not support MFA. Attackers frequently use these protocols to perform password spraying and credential stuffing attacks, easily bypassing MFA requirements.

- **Question:** How are exclusions to Conditional Access Policies (CAPs) managed, documented, and monitored?
  - **Recommended Control:** Implement strict governance over a dedicated "CAP Exclusions" Azure AD security group. Alert the Security Operations Center (SOC) on any addition of users to this group or modifications to the CAPs themselves. 
  - **Associated Risk:** Broad or unmonitored exclusions can inadvertently leave privileged users or critical service accounts completely exposed to single-factor authentication attacks.

### Privileged Identity Management (PIM) & Admin Roles
*This section focuses on the principle of least privilege, specifically regarding highly privileged human identities.*

- **Question:** How many accounts hold permanent, standing "Global Administrator" privileges, and how is Just-In-Time (JIT) access utilized?
  - **Recommended Control:** Implement Azure AD Privileged Identity Management (PIM). Eliminate standing privileges (except for break-glass accounts) and require administrators to request time-bound, MFA-verified, and approved elevation for all highly privileged roles.
  - **Associated Risk:** Standing privileges expand the attack surface. If an admin’s session token or credentials are stolen, the attacker gains immediate, unrestricted access to the entire Azure environment.

- **Question:** Are there highly monitored "Break-Glass" (Emergency Access) accounts established, and how are they secured?
  - **Recommended Control:** Maintain 2-3 cloud-only emergency accounts with `.onmicrosoft.com` domains. These must be excluded from CAPs, secured with FIDO2 hardware keys stored in physical safes, and have custom alerts configured in Azure Monitor/Sentinel to trigger high-severity incidents upon *any* sign-in attempt.
  - **Associated Risk:** Without break-glass accounts, an organization could be permanently locked out of their tenant during a misconfiguration or Azure MFA outage. Conversely, if these accounts are poorly monitored, they serve as a stealthy backdoor for attackers.

### Application Security & Non-Human Identities (Service Principals)
*This section addresses the risks associated with App Registrations, Enterprise Applications, and API integrations.*

- **Question:** How does the organization prevent "Illicit Consent Grant" phishing attacks where users authorize malicious third-party apps to access their Microsoft 365 data?
  - **Recommended Control:** Configure the "Admin consent workflow." Block end-users from consenting to applications that require access to sensitive data (e.g., Mail.Read, Files.Read), requiring a Global or Application Administrator to review and approve the OAuth scopes.
  - **Associated Risk:** An attacker can trick a user into granting a malicious app read/write access to their emails and files. This grants the attacker persistent API access that bypasses MFA and credential resets.

- **Question:** How is the lifecycle (rotation and storage) of client secrets and certificates for App Registrations and Service Principals managed?
  - **Recommended Control:** Automate credential rotation using Azure Key Vault. Enforce short-lived certificates over static client secrets where possible, and utilize Managed Identities for Azure resources to eliminate the need for manual credential handling.
  - **Associated Risk:** Hardcoded, leaked, or forgotten service principal secrets provide attackers with unmonitored, persistent access to the tenant, often with highly privileged Microsoft Graph API permissions.

- **Question:** How frequently are application API permissions (e.g., Microsoft Graph scopes like `Directory.ReadWrite.All`) audited to ensure the principle of least privilege for non-human identities?
  - **Recommended Control:** Conduct quarterly Azure AD Access Reviews specifically targeting Service Principals and Enterprise Applications to revoke unused or overly broad permissions.
  - **Associated Risk:** An over-privileged internal application that becomes compromised can be leveraged by an attacker to pivot laterally, read sensitive directory data, or escalate privileges within the tenant.

### External Identities (B2B) & Cross-Tenant Access
*This section evaluates the boundaries of the tenant and how collaboration with external entities is secured.*

- **Question:** What is the automated lifecycle and de-provisioning process for inactive B2B Guest Accounts?
  - **Recommended Control:** Utilize Azure AD Entitlement Management (Access Packages) with strict expiration policies, combined with automated Access Reviews that require external sponsors or the guests themselves to justify continued access.
  - **Associated Risk:** Stale guest accounts create orphaned access points. If the external partner’s home environment is compromised, the attacker can seamlessly pivot into your tenant using the active guest account.

- **Question:** Are Cross-Tenant Access Settings configured to prevent internal users from authenticating to external, unauthorized Azure AD tenants from corporate devices?
  - **Recommended Control:** Configure explicit Outbound Cross-Tenant Access policies. Block all outbound access by default and only allowlist specific, vetted partner tenant IDs. 
  - **Associated Risk:** Without outbound restrictions, a malicious insider or attacker could exfiltrate corporate data by simply authenticating into their own personal or attacker-controlled Azure AD tenant using a corporate device.

### Device Trust & Zero Trust Architecture
*This section evaluates how device health and compliance are factored into the authorization process.*

- **Question:** How is device compliance or "Hybrid Azure AD Joined" status integrated into the authentication flow for access to sensitive corporate resources?
  - **Recommended Control:** Implement Conditional Access Policies that enforce "Require device to be marked as compliant" (via Microsoft Intune) or "Require Hybrid Azure AD joined device" before granting an access token for M365 or internal apps.
  - **Associated Risk:** If device state is ignored, an attacker who successfully steals a user's session cookie (AiTM attack) or credentials can access corporate data from an untrusted, malware-infected personal device or attacker infrastructure.

### Threat Detection, Logging, & Auditing
*This section reviews the organization's ability to detect, investigate, and respond to identity-based attacks.*

- **Question:** How are automated responses configured for events detected by Azure AD Identity Protection (e.g., Impossible Travel, Anonymous IP, Leaked Credentials)?
  - **Recommended Control:** Configure Risk-Based Conditional Access Policies. Enforce a secure, self-service password reset (SSPR) for "High User Risk" and enforce a secondary MFA prompt for "Medium/High Sign-in Risk."
  - **Associated Risk:** Relying solely on manual SOC investigations for risk alerts introduces a time gap. By the time an analyst reviews an "Impossible Travel" alert, the attacker may have already exfiltrated critical data.

- **Question:** What is the retention period for Azure AD Sign-in logs, Audit logs, and Non-interactive sign-in logs, and where are they stored?
  - **Recommended Control:** Configure Azure AD Diagnostic Settings to stream all log types to a central SIEM (e.g., Microsoft Sentinel) and cold storage (Azure Storage Account) with a minimum retention period of 1 year.
  - **Associated Risk:** Default Azure AD log retention is limited (often 30 days depending on the license). Advanced Persistent Threats (APTs) are often discovered months after the initial breach; without historical logs, incident responders cannot determine the scope or root cause of the compromise.
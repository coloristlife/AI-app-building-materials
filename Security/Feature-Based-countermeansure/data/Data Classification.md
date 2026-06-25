**Data Classification**. 


### Data Classification & Governance
- **Question:** How is data identified, classified, and inventoried across the system's architecture?
  - **Recommended Control:** Implement a formalized data classification policy (e.g., Public, Internal, Confidential, Restricted/PII) enforced through automated data discovery and cataloging tools.
  - **Associated Risk:** Without clear visibility and classification, sensitive data may be stored in unauthorized or unmonitored locations ("shadow data"), leading to inadequate security controls, unintentional exposure, and regulatory compliance violations.

### Policy, Governance, and Ownership

- **Question:** Has a formal Data Classification Policy been documented, approved by executive management, and mapped to specific business and regulatory requirements (e.g., GDPR, HIPAA, PCI-DSS)?
  - **Recommended Control:** A formalized policy defining clear classification tiers (e.g., Public, Internal, Confidential, Restricted/Secret) and explicit rules for how each tier must be treated.
  - **Associated Risk:** Lack of standardized classification leads to ambiguous security expectations, resulting in inconsistent data handling, regulatory non-compliance, and ultimately, sensitive data exposure.

- **Question:** Have specific Data Owners and Data Custodians been explicitly identified, and do they actively review the classification levels of the data assets under their purview?
  - **Recommended Control:** A documented Data Ownership Matrix establishing clear accountability, coupled with a periodic (e.g., annual) access and classification review process driven by the Data Owners.
  - **Associated Risk:** "Orphaned data" with no assigned owner is rarely reviewed or secured properly, leading to continuous privilege creep, excessive retention, and unauthorized access over time.

### Data Discovery and Inventory

- **Question:** Is there an automated mechanism continuously discovering, scanning, and inventorying structured, unstructured, and semi-structured data across all environments (on-premises, cloud, SaaS, and endpoints)?
  - **Recommended Control:** Deployment of Data Security Posture Management (DSPM) or robust automated data discovery tools capable of identifying sensitive data dynamically as it is created or moved.
  - **Associated Risk:** Unmanaged "shadow data" remains hidden from security teams. Attackers frequently seek out these unprotected, forgotten data stores to exfiltrate information without triggering security alerts.

- **Question:** How does the organization identify and handle sensitive data that is embedded in non-standard or edge-case formats (e.g., images, OCR, audio recordings, or code repositories)?
  - **Recommended Control:** Use of advanced discovery tools equipped with Optical Character Recognition (OCR), Natural Language Processing (NLP), and secrets scanning (for code repos) to detect sensitive data outside of standard text documents.
  - **Associated Risk:** Sensitive data (like screenshots of PII or API keys in source code) bypasses standard text-based scanning controls, leading to hidden compliance violations and data leaks.

### Data Labeling and Tagging

- **Question:** Are data assets persistently tagged with metadata that reflects their classification tier, and are visual markings (e.g., headers, footers, watermarks) applied to readable documents?
  - **Recommended Control:** Integration of enterprise-grade classification software (e.g., Microsoft Purview, Titus, Boldon James) that embeds metadata directly into file properties and applies visual cues.
  - **Associated Risk:** Downstream security tools (like DLP and CASB) cannot programmatically enforce policies without metadata tags, and human users are more likely to mistakenly share sensitive documents if visual cues are absent.

- **Question:** When automated classification is utilized, what technical controls and workflows govern a user's ability to manually downgrade a data classification label (e.g., from "Restricted" to "Public")?
  - **Recommended Control:** A forced justification prompt, centralized logging to the SIEM, and mandatory Data Owner approval workflows for downgrading sensitive labels.
  - **Associated Risk:** A compromised user account or a malicious insider could easily bypass data exfiltration controls by simply downgrading a file’s classification to "Public" before emailing it out of the network.

### Access Control and Handling

- **Question:** Are Identity and Access Management (IAM) controls explicitly mapped to the data classification tiers utilizing Attribute-Based Access Control (ABAC) or Role-Based Access Control (RBAC)?
  - **Recommended Control:** Zero Trust architecture integrating IAM with the data layer, ensuring that access to "Confidential" or "Restricted" data requires strong attributes (e.g., MFA verification, compliant device status, specific user roles).
  - **Associated Risk:** Relying solely on broad perimeter access or flat network permissions allows lateral movement; a single compromised account could gain unhindered access to the organization's most sensitive data.

- **Question:** Are technical restrictions enforced to prevent highly classified data from being moved or copied to unauthorized environments, such as lower-tier development/testing environments or unapproved SaaS applications?
  - **Recommended Control:** Enforcement of Data Loss Prevention (DLP) policies and Cloud Access Security Broker (CASB) rules that block the transfer of production-classified data into non-production or shadow IT environments. Data masking/tokenization should be used if data *must* be used in lower environments.
  - **Associated Risk:** Development and testing environments usually have significantly weaker security controls than production. Moving highly classified data there creates a massive, easily exploitable vulnerability.

### Protection and Encryption

- **Question:** Are cryptographic controls (encryption at rest and in transit) scaled and applied commensurately with the data's specific classification tier?
  - **Recommended Control:** Mandated use of strong, industry-standard encryption (e.g., AES-256, TLS 1.2+) for all data, but enforcing highly restricted Key Management (e.g., HSMs, Customer Managed Keys, strict key rotation) specifically for "Restricted" and "Confidential" tiers.
  - **Associated Risk:** If an attacker steals a database or physical drive, the lack of robust encryption and isolated key management for highly sensitive data guarantees a total breach of confidentiality.

- **Question:** How is classified data protected when explicitly shared with authorized external parties, such as vendors, partners, or contractors?
  - **Recommended Control:** Implementation of Digital Rights Management (DRM) or Information Rights Management (IRM) that encrypts the data at the file level and enforces access policies (e.g., view-only, do not print, time-expiring access) regardless of where the file travels.
  - **Associated Risk:** Once classified data leaves the corporate perimeter, the organization loses all control over it. External parties could suffer a breach, or maliciously leak the data, severely impacting the originating organization.

### Retention, Archiving, and Destruction

- **Question:** Are data retention schedules strictly automated and enforced based on the classification level and applicable legal/regulatory hold requirements?
  - **Recommended Control:** Automated lifecycle management policies configured in data repositories that archive and subsequently purge data once it reaches the end of its legally mandated or business-required lifespan.
  - **Associated Risk:** Indefinite retention of sensitive data continuously expands the organization's attack surface and drastically increases liability and financial penalties in the event of a breach.

- **Question:** What mechanisms ensure the secure, permanent, and verifiable destruction of highly classified data at the end of its lifecycle (including backups and cloud storage)?
  - **Recommended Control:** Implementation of NIST SP 800-88 compliant media sanitization processes. For cloud and virtualized environments, "crypto-shredding" (deliberate destruction of the encryption keys used to encrypt the data) should be utilized alongside verifiable deletion logs.
  - **Associated Risk:** Improper deletion (e.g., simply emptying a recycle bin or standard formatting) leaves residual data blocks intact, allowing malicious actors to use forensic tools to recover highly sensitive information from discarded or repurposed media.

### Monitoring, Auditing, and Incident Response

- **Question:** Is all access, modification, and sharing of "Confidential" and "Restricted" data actively logged, centralized, and monitored for anomalous behavior?
  - **Recommended Control:** Implementation of Data Access Governance (DAG) tools and User and Entity Behavior Analytics (UEBA), forwarding all critical data-access logs to a centralized SIEM for real-time correlation and alerting.
  - **Associated Risk:** Without granular auditing at the data tier, a slow-and-low data exfiltration attack by an insider or APT (Advanced Persistent Threat) will go completely unnoticed until the data appears on the dark web.

- **Question:** Do Incident Response (IR) playbooks include specific workflows for triage and containment based on the classification level of the data involved in a suspected breach?
  - **Recommended Control:** IR playbooks structured to automatically escalate the severity of a security event (e.g., triggering immediate executive notification and legal counsel involvement) if the compromised systems hold "Restricted" data versus "Public" data.
  - **Associated Risk:** Treating all security events equally causes alert fatigue and misallocation of resources. Security teams may waste critical hours investigating a breached public-facing web server while a separate breach involving highly classified intellectual property goes unmitigated.
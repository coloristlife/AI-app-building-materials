 **Data Security**

### Data Classification & Governance
- **Question:** How is data identified, classified, and inventoried across the system's architecture?
  - **Recommended Control:** Implement a formalized data classification policy (e.g., Public, Internal, Confidential, Restricted/PII) enforced through automated data discovery and cataloging tools.
  - **Associated Risk:** Without clear visibility and classification, sensitive data may be stored in unauthorized or unmonitored locations ("shadow data"), leading to inadequate security controls, unintentional exposure, and regulatory compliance violations.

### Data at Rest (Storage Security)
- **Question:** What encryption mechanisms are applied to data stored in databases, object storage, file systems, and offline backups?
  - **Recommended Control:** Enforce AES-256 encryption for all data at rest. Utilize Transparent Data Encryption (TDE) for databases, volume/object-level encryption for cloud storage, and ensure backups are encrypted and stored immutably.
  - **Associated Risk:** Physical theft of storage media, unauthorized access to the underlying storage infrastructure, or stolen database snapshots could result in a massive breach of plaintext sensitive information.

### Data in Transit (Network Security)
- **Question:** What cryptographic protocols and cipher suites are utilized to protect data moving between external clients, internal microservices, and third-party APIs?
  - **Recommended Control:** Enforce TLS 1.2 or higher (preferably TLS 1.3) across all communication channels. Use strong, modern cipher suites (e.g., AES-GCM, ChaCha20) with Perfect Forward Secrecy (PFS), and implement HTTP Strict Transport Security (HSTS).
  - **Associated Risk:** Use of deprecated protocols (like TLS 1.0/1.1 or SSL) or weak ciphers exposes data to Man-in-the-Middle (MitM) attacks, packet sniffing, and interception, leading to the compromise of credentials or payload data.

### Data in Use (Processing & Memory Security)
- **Question:** How is sensitive data protected from exposure while being actively processed in system memory, application logs, and user interfaces?
  - **Recommended Control:** Implement strict data masking and redaction for application logs and UIs. Utilize parameterized queries to prevent injection, employ memory-safe programming practices, and consider Confidential Computing (Secure Enclaves/Trusted Execution Environments) for highly sensitive workloads.
  - **Associated Risk:** Sensitive data can be exposed through memory scraping malware, verbose error logging, application vulnerabilities (e.g., buffer overflows), or over-the-shoulder surfing in user interfaces.

### Cryptographic Key Management
- **Question:** How are cryptographic keys generated, stored, distributed, rotated, and protected against unauthorized access?
  - **Recommended Control:** Utilize a centralized Key Management Service (KMS) or Hardware Security Module (HSM) with FIPS 140-2 Level 3 (or higher) validation. Enforce automated key rotation schedules, strict separation of duties, and audit logging for all key access.
  - **Associated Risk:** If encryption keys are hardcoded, stored alongside the encrypted data, or poorly managed, attackers can easily retrieve them, rendering all data encryption efforts useless and allowing full decryption of stolen data.

### Identity & Access Management (IAM) for Data
- **Question:** How is access to sensitive data stores authorized, and how is the principle of least privilege enforced for both human and machine identities?
  - **Recommended Control:** Implement Role-Based Access Control (RBAC) or Attribute-Based Access Control (ABAC). Mandate Multi-Factor Authentication (MFA) for human access, and utilize short-lived, dynamically generated tokens for machine-to-machine access.
  - **Associated Risk:** Over-provisioned access rights or compromised user/service accounts can allow unauthorized entities or malicious insiders to seamlessly access, manipulate, or exfiltrate sensitive data.

### Data Loss Prevention (DLP) & Exfiltration Monitoring
- **Question:** What mechanisms are deployed to detect, block, and alert on unauthorized extraction, sharing, or mass downloading of sensitive data?
  - **Recommended Control:** Deploy Data Loss Prevention (DLP) solutions at the endpoint, network perimeter, and cloud access layer (CASB). Integrate with User and Entity Behavior Analytics (UEBA) to detect anomalous data access patterns.
  - **Associated Risk:** Without egress monitoring and DLP, a compromised account or malicious insider could easily copy and exfiltrate large volumes of intellectual property, PII, or financial data to an external location without detection.

### Data Lifecycle & Retention Management
- **Question:** What processes ensure that data is securely destroyed or anonymized when it reaches the end of its legal, regulatory, or business retention period?
  - **Recommended Control:** Enforce automated data retention policies. Use cryptographic erasure (crypto-shredding) for cloud environments or secure wiping processes compliant with NIST SP 800-88 guidelines for physical media. 
  - **Associated Risk:** Accumulating "dark data" or legacy sensitive information indefinitely expands the attack surface, increases the "blast radius" of a potential breach, and violates the data minimization principles of privacy laws like GDPR or CCPA.

### Third-Party & Supply Chain Data Security
- **Question:** How is system data protected when shared with, processed by, or transmitted to third-party vendors, APIs, or downstream supply chain partners?
  - **Recommended Control:** Enforce strict vendor security risk assessments (e.g., SOC 2 Type II review). Require contractual Data Processing Agreements (DPAs), enforce API authentication/rate-limiting, and mandate that third parties align with your internal encryption and access control standards.
  - **Associated Risk:** Even if internal controls are robust, sending unencrypted or loosely governed data to a less secure third-party vendor creates a backdoor for data breaches, for which the originating organization remains legally and reputationally liable.
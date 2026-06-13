
## Cryptography & Key Management

### 1. Key Generation and Cryptographic Standards
*Focuses on ensuring the mathematical foundation and origin of the keys are fundamentally secure.*

- **Question:** How are cryptographic keys generated, and what mechanisms ensure sufficient entropy and the use of industry-approved algorithms?
  - **Recommended Control:** Use of strong, modern cryptographic algorithms (e.g., AES-256, RSA-2048+, ECC) and Cryptographically Secure Pseudorandom Number Generators (CSPRNG) validated against FIPS 140-2/3 or equivalent standards.
  - **Associated Risk:** Weak key generation or low entropy allows attackers to easily brute-force, guess, or reverse-engineer keys, completely compromising the confidentiality and integrity of encrypted data.

### 2. Key Storage and Access Control
*Focuses on protecting the key material from unauthorized extraction or misuse while at rest.*

- **Question:** Where are cryptographic keys stored at rest, and how are they physically and logically protected against unauthorized extraction?
  - **Recommended Control:** Storing keys securely in a dedicated Hardware Security Module (HSM) or a managed Key Management Service (KMS) that completely isolates key material from application memory and the file system.
  - **Associated Risk:** Hardcoded keys, keys stored in plaintext configuration files, or keys co-located with the encrypted data in the same database can be easily stolen during a system breach, rendering the encryption useless.

- **Question:** How is the principle of "Separation of Duties" enforced between the personnel who manage the cryptographic keys and the personnel who manage or access the encrypted data?
  - **Recommended Control:** Implementing strict Role-Based Access Control (RBAC) separating "Key Administrators" (who manage key lifecycles but cannot access application data) from "Data Users/Applications" (who can request cryptographic operations but cannot export the raw key material).
  - **Associated Risk:** A single compromised account or malicious insider could both extract the decryption keys and access the database, leading to a massive, undetected data exfiltration event.

### 3. Key Lifecycle, Rotation, and Destruction
*Focuses on limiting the lifespan of keys and handling their retirement securely.*

- **Question:** What is the established frequency and workflow for rotating cryptographic keys, and is this process automated or manual?
  - **Recommended Control:** Enforcing a regular, automated key rotation schedule (e.g., annually for Master Keys, 30-90 days for Data Encryption Keys) and supporting immediate, on-demand rotation in the event of suspected compromise.
  - **Associated Risk:** Long-lived keys increase the window of opportunity for attackers. If a long-lived key is eventually compromised, an attacker can decrypt vast amounts of historical data (a failure of forward secrecy).

- **Question:** What procedures are executed when a key reaches the end of its cryptoperiod or is suspected to be compromised (revocation and destruction)?
  - **Recommended Control:** Formal key revocation workflows and secure key destruction procedures (e.g., crypto-shredding) that permanently eliminate the key material while maintaining a highly secure, non-extractable archive only if legally required for data retention.
  - **Associated Risk:** Unrevoked compromised keys can be used to forge digital signatures or decrypt sensitive data, while improperly destroyed keys can be recovered by adversaries analyzing decommissioned storage media.

### 4. Transmission and Distribution
*Focuses on safely moving keys between systems when absolutely necessary.*

- **Question:** How is cryptographic key material securely distributed or transmitted between the KMS/HSM and the consuming application or endpoint?
  - **Recommended Control:** Transmitting keys exclusively over mutually authenticated, highly encrypted channels (e.g., mTLS) and utilizing "key wrapping" (encrypting a key with a Master Key Encryption Key, or KEK) during transit.
  - **Associated Risk:** Unwrapped keys transmitted over internal networks can be intercepted by a Man-in-the-Middle (MitM) attacker, who can then silently decrypt sensitive communications or data stores without alerting system owners.

### 5. Resiliency, Monitoring, and Auditing
*Focuses on ensuring key availability and detecting malicious interactions with the key management infrastructure.*

- **Question:** What recovery mechanisms (e.g., key escrow, secure backups) are in place to ensure encrypted data is not permanently lost if a master key is accidentally deleted, corrupted, or becomes unavailable?
  - **Recommended Control:** Secure, highly regulated key backup and recovery processes using split-knowledge mechanisms (e.g., Shamir's Secret Sharing) that require "M of N" quorum holders (e.g., 3 out of 5 key custodians) to restore a master key.
  - **Associated Risk:** Accidental loss or corruption of a master key without a secure, tested backup results in cryptographic erasure—leading to permanent, unrecoverable data loss and severe business disruption.

- **Question:** How are key lifecycle events and cryptographic operations (e.g., key generation, access requests, encryption/decryption events, administrative changes) logged and monitored?
  - **Recommended Control:** Comprehensive, tamper-evident audit logging for all KMS/HSM operations, integrated directly into a centralized SIEM with automated alerts for unusual access patterns (e.g., excessive decryption requests or unauthorized key export attempts).
  - **Associated Risk:** Lack of visibility into key usage prevents the detection of unauthorized key extraction attempts or the abuse of valid keys, blinding security teams and hindering incident response and compliance verification.

### 6. Application Secrets and Environment Isolation
*Focuses on the secure handling, dynamic injection, and strict boundary separation of non-cryptographic secrets (e.g., API keys, passwords, tokens).*

- **Question:** Are all authentication credentials, API keys, and sensitive configuration values across system components securely stored in a centralized secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault) and accessed dynamically by workloads rather than being hardcoded, and is there an established, automated process defining their regular rotation frequency?
  - **Recommended Control:** Implementation of a centralized, highly available Secrets Management solution to inject secrets dynamically at runtime, coupled with automated rotation policies (e.g., auto-rotating database credentials via serverless functions) and CI/CD pipeline scanning (e.g., pre-commit hooks) to prevent secrets from being committed to source code.
  - **Associated Risk:** Hardcoded credentials, secrets exposure in source code or configuration logs, and prolonged credential compromise leading to unauthorized access, lateral movement, or unauthorized document processing.

- **Question:** Are secrets isolated per environment with strict separation (DEV/UAT/PROD/DR) so that compromise of a lower environment cannot be used to access higher environments? (Scope: environment-specific secrets stores/vaults, environment-specific app configurations, environment-specific vendor endpoints, any shared libraries/config repos that reference vendor cloud access.)
  - **Recommended Control:** Strict logical and physical segregation of secrets management instances or vault namespaces per environment, utilizing Identity and Access Management (IAM) and RBAC to ensure compute workloads and personnel in lower environments (e.g., DEV/UAT) have absolutely no authorization to assume roles or read secrets residing in PROD or DR.
  - **Associated Risk:** Environment pivoting; lateral movement; privilege escalation from DEV to PROD/DR due to shared credentials.
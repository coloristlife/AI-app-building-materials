


### Network Security & Encryption in Transit

**Question:** Is TLS 1.2 or higher explicitly enforced, and are weak cipher suites disabled, for all external ingress points and internal network communications ([placeholder for all relevant services or their features])?
*   **Associated Risk:** Man-in-the-middle (MITM) attacks, data interception, and unauthorized traffic sniffing.

**Question:** Is network traffic strictly segmented and routed through secure boundaries, ensuring that internal resources are not directly exposed to the public internet ?
*   **Associated Risk:** Exposure of internal backend services to public internet threats, unauthorized network traversal.

### Data Security & Encryption at Rest

**Question:** Are all forms of persistent data stores and message brokers ([placeholder for all relevant services or their features]) encrypted at rest using centrally managed and regularly rotated KMS keys?
*   **Associated Risk:** Unauthorized access to sensitive records, raw certificate documents, and backend data stores in the event of a storage volume compromise.

**Question:** When raw inputs (PDF / HTML) are ingested and processed, is temporary/ephemeral file storage securely isolated and encrypted before being wiped (e.g., within [placeholder for all relevant services or their features])?
*   **Associated Risk:** Data leakage of sensitive files left behind in temporary storage volumes or unencrypted cache layers.

### Identity, Access Management (IAM) & Segregation

**Question:** Are strict role-based access controls (RBAC), least-privilege principles, and data segregation mechanisms enforced at both the application and database layers (via [placeholder for all relevant services or their features]) to ensure users/tenants can only view or modify their specific records?
*   **Associated Risk:** Cross-tenant data leakage, unauthorized privilege escalation, and unauthorized data modification/approval.

### Data Privacy & Third-Party Integrations

**Question:** Does the system actively identify and successfully mask/redact sensitive PII/PHI (e.g., [placeholder for all relevant services or their features]) from parsed inputs *before* that data is transmitted outside the internal environment to third-party services?
*   **Associated Risk:** Unintentional exposure of PII/PHI to external vendors, regulatory violations (GDPR, HIPAA).

**Question:** Are strict enterprise Data Processing Agreements (DPAs) and confidentiality clauses executed with our external vendors ([placeholder for all relevant services or their features]) explicitly guaranteeing that our document data will *not* be retained or used for their purposes, for example to train their foundational models, and does the geographic hosting of their API comply with our data residency requirements?
*   *(Note: If the Embedding model is self-hosted,  this risk for embeddings is mitigated).*
*   **Associated Risk:** Legal and compliance risks, data sovereignty violations, and corporate intellectual property misuse by third parties.

### Data Lifecycle & Retention

**Question:** Are strict data retention limits and secure deletion policies defined, automated, and actively enforced across all internal data stores ([placeholder for all relevant services or their features]) as well as any external operational environments ([placeholder for all relevant services or their features])?
*   **Associated Risk:** Unnecessary prolonged data exposure, expanded attack surface, and data retention compliance violations. 

### data in use - Execution Environment Security
**Capability Probe:** Does the system retrieve, download, or temporarily store external file attachments or raw data payloads into local memory or disk for processing during task execution?
-   **Countermeasure Probe:** If external payloads are processed locally, are these operations tightly isolated using ephemeral sandboxes or Trusted Execution Environments (TEEs), and is there a strict, automated data destruction/garbage collection mechanism that securely wipes the data immediately upon task completion?
    - **Associated Risk:** Data Remanence and Unauthorized Cross-Task Exposure. If sensitive files are processed in persistent or shared execution environments without robust isolation (such as TEEs or ephemeral, single-use containers), residual data left in memory or temporary storage could be exposed. This "data remanence" creates a significant risk of data spillage, where confidential attachments could be scraped by malicious actors, infrastructure administrators, or inadvertently leaked to subsequent tasks or other tenants sharing the same underlying infrastructure.
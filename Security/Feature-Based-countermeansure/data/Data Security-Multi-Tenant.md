Here is a section specifically designed for **Multi-Tenant Data Security** (often found in SaaS platforms, shared databases, and cloud-native architectures). 

Multi-tenancy introduces complex risks regarding data isolation, cross-tenant leakage, and shared resource management. Here are the security review questions tailored for this scope:


### Tenancy Model (Multi-tenant vs. Single-tenant):
In a Multi-tenant environment, your data sits on the same infrastructure (and often the same database) as other Unily customers. You have to trust their application-level logic to keep your data segregated. A vulnerability in their code could expose your data to another company.  
In a Single-tenant environment, you have dedicated infrastructure (your own database, your own VMs/containers). This drastically reduces the risk of cross-tenant data exposure.

- **Question:** Is the platform hosting environment single-tenant or multi-tenant?


### Data Isolation & Logical Separation
- **Question:** How is data logically or physically separated between different tenants to prevent cross-tenant data spillage or accidental mixing?
  - **Recommended Control:** Implement strict data partitioning architectures, such as database-per-tenant, schema-per-tenant, or robust Row-Level Security (RLS) with enforced tenant IDs in a shared database. Ensure the isolation logic is enforced deeply at the Data Access Layer (DAL) or Object-Relational Mapper (ORM), rather than relying solely on application-layer filtering.
  - **Associated Risk:** Inadequate isolation can lead to catastrophic cross-tenant data exposure. A flaw in application code could result in one organization viewing or modifying the highly sensitive data of a competitor, permanently destroying customer trust and leading to massive legal liability.

### Tenant-Specific Encryption & Key Management (BYOK/CMK)
- **Question:** Are tenants provided with the ability to manage their own cryptographic keys for data encryption, and how is cryptographic isolation maintained?
  - **Recommended Control:** Support Customer-Managed Keys (CMK) or Bring Your Own Key (BYOK) architectures. Use tenant-specific Data Encryption Keys (DEKs) wrapped by a Key Encryption Key (KEK) that is controlled by the individual tenant's external KMS.
  - **Associated Risk:** If all multi-tenant data is encrypted using a single, global master key, a compromise of that key exposes *all* tenants simultaneously. Furthermore, enterprise tenants with strict compliance requirements may refuse to adopt the platform if they cannot revoke access to their data by disabling their own keys.

### Cross-Tenant Access Control (Preventing IDOR)
- **Question:** How does the application validate tenant context in every API request and database query to prevent unauthorized cross-tenant object access?
  - **Recommended Control:** Enforce mandatory tenant ID validation in authentication tokens (e.g., JWT claims) and bind every session tightly to a specific tenant context. Prevent Insecure Direct Object Reference (IDOR) vulnerabilities by enforcing server-side authorization checks that validate whether the requested resource ID explicitly belongs to the authenticated user's tenant ID.
  - **Associated Risk:** Attackers or curious users could manipulate API parameters or URLs (e.g., changing `tenant_id=101` to `102`, or modifying an invoice ID) to access, alter, or delete records belonging to other tenants.

### Multi-Tenant Backups & Point-in-Time Recovery
- **Question:** How does the backup and restoration architecture handle multi-tenancy, specifically if a single tenant suffers data corruption and requires a Point-in-Time Recovery (PITR)?
  - **Recommended Control:** Design the backup architecture to support tenant-level extraction and restoration. If using a shared database with row-level isolation, implement logical backup tools or event-sourcing architectures that allow administrators to roll back a specific tenant's state without impacting the rest of the database.
  - **Associated Risk:** If backups are entirely monolithic, restoring data for one corrupted or compromised tenant might require rolling back the entire shared database. This would result in unacceptable data loss and business disruption for all other unaffected tenants on the platform.

### Resource Exhaustion & "Noisy Neighbor" Prevention
- **Question:** What controls are in place to prevent a single tenant from exhausting shared database or processing resources, ensuring fair use across the platform?
  - **Recommended Control:** Implement strict resource quotas, API rate limiting, database query timeouts, and connection pooling limits on a per-tenant basis. Monitor infrastructure metrics and utilize auto-scaling, dynamic sharding, or dedicated compute nodes for high-volume tenants.
  - **Associated Risk:** A malicious tenant running intentionally complex queries, or a normal tenant experiencing a massive surge in traffic (or a DDoS attack), could monopolize shared database CPU and memory. This "noisy neighbor" scenario results in a systemic Denial of Service (DoS) for all other tenants sharing the infrastructure.

### Tenant Offboarding & Targeted Data Deletion
- **Question:** How is data securely targeted, purged, and verified when a specific tenant terminates their contract, ensuring no remnants are left in shared storage?
  - **Recommended Control:** Implement automated tenant offboarding workflows that execute hard deletions (or crypto-shredding, if BYOK is used) of all tenant-tagged data across active databases, search indexes, caches, and logs. Ensure there is a documented process for data deletion propagation into backups within regulatory timeframes.
  - **Associated Risk:** Failing to effectively isolate and purge an offboarded tenant's data results in long-term unauthorized retention ("dark data"). This violates data privacy regulations (e.g., GDPR's Right to Erasure) and exposes the former customer's data to ongoing risks even after their relationship with the platform has ended.
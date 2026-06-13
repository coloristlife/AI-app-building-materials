
### **Introduction to Control Objectives**

Control Objective is a high-level security objective that, if achieved, mitigates the threat.


A **Control Objective** defines a specific, high-level security goal that must be achieved. It describes **WHAT** needs to be accomplished, not **HOW** it is accomplished. This abstraction is critical for the scalability of the Knowledge Graph, allowing a single objective to be fulfilled by multiple different patterns and technical implementations across various technology stacks.

The following is a foundational list of Control Objectives, categorized by security domain.

---

### **1. Identity & Access Control (IAC)**
*This domain focuses on ensuring that only authenticated and authorized entities (both human and machine) can access resources, strictly adhering to the principle of least privilege.*

| Objective ID | Control Objective Name | Description |
| :--- | :--- | :--- |
| `obj_iac_strong_authn` | Enforce Strong Authentication | Ensure all users and services are authenticated using mechanisms resistant to common attacks (e.g., credential stuffing, password spraying). |
| `obj_iac_mfa` | Enforce Multi-Factor Authentication | Require more than one verification factor for authentication, especially for sensitive systems and privileged access. |
| `obj_iac_least_privilege` | Enforce Principle of Least Privilege | Grant only the minimum permissions necessary for an entity to perform its designated function. |
| `obj_iac_central_identity` | Centralize Identity Management | Manage identities and credentials in a centralized, authoritative system (e.g., SSO, IdP) to ensure consistent policy enforcement. |
| `obj_iac_service_authn` | Ensure Authenticity of Services | Require services to strongly authenticate to each other before communicating (e.g., via mTLS, workload identity). |
| `obj_iac_secure_secrets` | Securely Manage Secrets and Credentials | Store and manage all secrets (API keys, passwords, certificates) in a secure, audited, and access-controlled system. |
| `obj_iac_review_access` | Regularly Review Access Permissions | Periodically review and recertify user and service permissions to remove stale or excessive access. |
| `obj_iac_session_management` | Implement Secure Session Management | Ensure user and service sessions are managed securely, with appropriate timeouts, rotation, and invalidation. |

### **2. Data Protection (DP)**
*This domain covers the security of data itself, focusing on confidentiality, integrity, and preventing unauthorized exposure, both at rest and in transit.*

| Objective ID | Control Objective Name | Description |
| :--- | :--- | :--- |
| `obj_dp_encrypt_transit` | Encrypt Data In Transit | Ensure all data transmitted over any network is encrypted using strong, modern cryptographic protocols. |
| `obj_dp_encrypt_rest` | Encrypt Data At Rest | Ensure all data stored on any persistent media (disks, object storage, databases) is encrypted. |
| `obj_dp_classify_data` | Identify and Classify Sensitive Data | Maintain a process for identifying and classifying data based on its sensitivity to inform protection requirements. |
| `obj_dp_prevent_exposure` | Prevent Sensitive Data Exposure | Ensure sensitive data is not inadvertently exposed in logs, error messages, monitoring, or other insecure channels. |
| `obj_dp_ensure_integrity` | Ensure Data Integrity | Protect data from unauthorized modification or destruction using mechanisms like checksums, digital signatures, or version control. |
| `obj_dp_segregate_data` | Segregate Data by Sensitivity | Isolate sensitive data in dedicated storage or environments with stricter access controls. |
| `obj_dp_secure_disposal` | Implement Secure Data Disposal | Ensure data is securely and irrecoverably destroyed at the end of its lifecycle. |

### **3. Application & Service Security (AS)**
*This domain focuses on securing the software itself, from the supply chain to runtime, against common application-level vulnerabilities.*

| Objective ID | Control Objective Name | Description |
| :--- | :--- | :--- |
| `obj_as_validate_inputs` | Validate and Sanitize All Inputs | Sanitize all data received from untrusted sources to prevent injection-style attacks (SQLi, XSS, Command Injection). |
| `obj_as_manage_dependencies` | Securely Manage Third-Party Dependencies | Maintain an inventory of all third-party components and continuously scan for known vulnerabilities. |
| `obj_as_secure_apis` | Secure APIs and Endpoints | Ensure all APIs enforce authentication, authorization, input validation, and rate limiting. |
| `obj_as_secure_config` | Maintain Secure Configurations | Harden all application and service configurations by disabling unnecessary features and changing default credentials. |
| `obj_as_isolate_untrusted_code` | Isolate Untrusted Code Execution | Execute any code from untrusted sources within a secure, sandboxed environment with limited permissions. |

### **4. Infrastructure & Network Security (INS)**
*This domain covers the security of the underlying compute, storage, and network infrastructure that applications run on.*

| Objective ID | Control Objective Name | Description |
| :--- | :--- | :--- |
| `obj_ins_isolate_networks` | Isolate Network Environments | Segregate networks based on trust levels and environment type (e.g., production, development, DMZ). |
| `obj_ins_microsegmentation` | Implement Micro-segmentation | Apply fine-grained network policies to control traffic flow between individual services or workloads (Zero Trust). |
| `obj_ins_harden_endpoints` | Harden Compute Instances and Endpoints | Apply secure baseline configurations to all servers, containers, and virtual machines, including regular patching. |
| `obj_ins_protect_perimeter` | Protect Against External Network Threats | Deploy controls like Web Application Firewalls (WAF) and DDoS mitigation services at the network edge. |

### **5. Logging, Monitoring, & Detection (LMD)**
*This domain ensures that the system has sufficient visibility to detect, investigate, and respond to potential security incidents.*

| Objective ID | Control Objective Name | Description |
| :--- | :--- | :--- |
| `obj_lmd_generate_logs` | Generate Comprehensive Audit Logs | Ensure all systems and applications generate detailed, immutable logs for security-relevant events. |
| `obj_lmd_centralize_logs` | Centrally Monitor and Analyze Logs | Aggregate logs from all sources into a central system for monitoring, analysis, and alerting. |
| `obj_lmd_implement_threat_detection` | Implement Threat Detection Mechanisms | Deploy tools and systems to actively detect anomalous or malicious activity in real-time. |

### **6. Resilience & Availability (RA)**
*This domain focuses on ensuring the system can withstand failures or attacks and can be recovered in a timely manner.*

| Objective ID | Control Objective Name | Description |
| :--- | :--- | :--- |
| `obj_ra_data_backup` | Implement Data Backup and Recovery | Regularly back up critical data and test the ability to restore it securely and completely. |
| `obj_ra_ensure_availability` | Ensure System Resilience and Availability | Design systems for high availability through redundancy, failover, and graceful degradation. |
| `obj_ra_incident_response` | Develop Incident Response Plan | Maintain and test a plan to effectively respond to and recover from security incidents. |
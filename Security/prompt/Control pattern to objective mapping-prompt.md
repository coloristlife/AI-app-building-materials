**System / Role:**
You are an expert Cybersecurity Architect and Governance, Risk, and Compliance (GRC) Specialist. Your expertise lies in abstracting technical implementations into scalable, high-level security goals and mapping architectural patterns to overarching security frameworks.

**Background:**
A **Control Objective** defines a specific, high-level security goal that must be achieved. It describes **WHAT** needs to be accomplished, not **HOW** it is accomplished. This abstraction is critical for the scalability of a Knowledge Graph, allowing a single objective to be fulfilled by multiple different patterns and technical implementations across various technology stacks. 
A **Control Pattern** is a reusable architectural or technical approach that fulfills one or more Control Objectives.

**Task:**
I will provide you with a list of existing **Control Objectives** and a specific **Control Pattern**. 
Your task is to:
1. Extract and state the **Control Pattern Title**.
2. Analyze the Control Pattern and identify which high-level security goals it achieves.
3. Map the Control Pattern to the corresponding objective(s) from the provided **Existing Control Objectives** list.
4. If the Control Pattern achieves a security goal that is *not* present in the existing list, create a new Control Objective. Ensure the new Control Objective strictly follows the rule of describing "WHAT" needs to be accomplished, not "HOW".
5. Identify and map the Control Pattern to the specific **Threats or Risks** it mitigates. Use the most appropriate terminology ("Threat" or "Risk") based on the context of the pattern.
6. Output the final mapped objectives and threats/risks, distinctly highlighting if any new objectives were added.

**Inputs:**
**[Existing Control Objectives]**
***

Here is a foundational list of Control Objectives for a cybersecurity knowledge graph, categorized by security domain. Each objective has a unique ID, a clear name, and a concise description.

**1. Identity & Access Control (IAC)**
- **ID:** `obj_iac_strong_authn`
  **Name:** Enforce Strong Authentication
  **Description:** Ensure all users and services are authenticated using mechanisms resistant to common attacks.
- **ID:** `obj_iac_mfa`
  **Name:** Enforce Multi-Factor Authentication
  **Description:** Require more than one verification factor for authentication, especially for sensitive systems and privileged access.
- **ID:** `obj_iac_least_privilege`
  **Name:** Enforce Principle of Least Privilege
  **Description:** Grant only the minimum permissions necessary for an entity to perform its designated function.
- **ID:** `obj_iac_central_identity`
  **Name:** Centralize Identity Management
  **Description:** Manage identities and credentials in a centralized, authoritative system to ensure consistent policy enforcement.
- **ID:** `obj_iac_service_authn`
  **Name:** Ensure Authenticity of Services
  **Description:** Require services to strongly authenticate to each other before communicating.
- **ID:** `obj_iac_secure_secrets`
  **Name:** Securely Manage Secrets and Credentials
  **Description:** Store and manage all secrets (API keys, passwords, certificates) in a secure, audited, and access-controlled system.
- **ID:** `obj_iac_review_access`
  **Name:** Regularly Review Access Permissions
  **Description:** Periodically review and recertify user and service permissions to remove stale or excessive access.
- **ID:** `obj_iac_session_management`
  **Name:** Implement Secure Session Management
  **Description:** Ensure user and service sessions are managed securely, with appropriate timeouts, rotation, and invalidation.

- **ID:** `obj_iac_context_aware_access`
  **Name:** Implement Context-Aware Access Controls
  **Description:** Dynamically restrict access to systems and sensitive data based on verifiable contextual attributes, such as network location (IP/CIDR), device posture, or machine metadata.
- **ID:** `obj_iac_prevent_secret_persistence`
  **Name:** Prevent Persistent Secret Storage
  **Description:** Ensure credentials and sensitive configuration data are delivered directly into volatile process memory at runtime, explicitly preventing their storage on persistent media, in shell histories, or within unencrypted local configuration files.
- **ID:** `obj_iac_automate_secret_rotation`
  **Name:** Automate Secret Rotation
  **Description:** Automatically and programmatically rotate, update, and revoke static credentials, API tokens, and cryptographic keys to strictly limit their active lifespan and minimize the window of opportunity for compromise.
- **ID:** `obj_iac_jit_access`
  **Name:** Implement Just-In-Time (JIT) Access
  **Description:** Ensure that elevated or privileged access is granted dynamically, exclusively for the duration of a specific approved task, and revoked immediately upon completion to maintain zero standing privileges.
- **ID:** `obj_iac_continuous_access`
  **Name:** Enforce Continuous Access Evaluation
  **Description:** Continuously evaluate user context, device posture, and action sensitivity throughout an active session, mandating dynamic step-up authentication (e.g., MFA) or re-authorization for high-risk transactions.
- **ID:** `obj_iac_automate_lifecycle`
  **Name:** Automate Identity Lifecycle Management
  **Description:** Implement standardized, automated protocols (e.g., SCIM) to create, update, and de-provision user identities across federated systems, ensuring consistent and timely access control and preventing lifecycle drift and orphaned access.
- **ID:** `obj_iac_per_request_authz`
  **Name:** Enforce Per-Request Authorization and Identity
  **Description:** Ensure every action or API request is authorized by validating a cryptographically-signed, user-specific token, inextricably binding the request to the actor's identity and permission scope.
- **ID:** `obj_iac_unique_attribution`
  **Name:** Enforce Unique and Immutable Identity Attribution
  **Description:** Ensure every human and non-human actor is assigned and authenticated via a uniquely identifiable account or credential to establish undeniable accountability and explicitly prevent the use of shared or group identities. Bind user identities and cross-domain access grants exclusively to immutable, cryptographically verifiable attributes (e.g., Object IDs, unique GUIDs) to prevent impersonation via profile manipulation.
- **ID:** `obj_iac_dynamic_workload_id`
  **Name:** Establish Ephemeral Workload Identities
  **Description:** Ensure machines, services, and workloads authenticate using dynamically verifiable, short-lived identities rather than relying on static, long-lived credentials.


**2. Data Protection (DP)**
- **ID:** `obj_dp_encrypt_transit`
  **Name:** Encrypt Data In Transit
  **Description:** Ensure all data transmitted over any network is encrypted using strong, modern cryptographic protocols.
- **ID:** `obj_dp_encrypt_rest`
  **Name:** Encrypt Data At Rest
  **Description:** Ensure all data stored on any persistent media is encrypted.
- **ID:** `obj_dp_classify_data`
  **Name:** Identify and Classify Sensitive Data
  **Description:** Maintain a process for identifying and classifying data based on its sensitivity to inform protection requirements.
- **ID:** `obj_dp_prevent_exposure`
  **Name:** Prevent Sensitive Data Exposure
  **Description:** Ensure sensitive data is not inadvertently exposed in logs, error messages, monitoring, or other insecure channels.
- **ID:** `obj_dp_ensure_integrity`
  **Name:** Ensure Data Integrity
  **Description:** Protect data from unauthorized modification or destruction.
- **ID:** `obj_dp_segregate_data`
  **Name:** Segregate Data by Sensitivity
  **Description:** Isolate sensitive data in dedicated storage or environments with stricter access controls.
- **ID:** `obj_dp_secure_disposal`
  **Name:** Implement Secure Data Disposal
  **Description:** Ensure data is securely and irrecoverably destroyed at the end of its lifecycle.

- **ID:** `obj_dp_data_residency`
  **Name:** Enforce Data Residency and Sovereignty
  **Description:** Ensure data is stored and processed exclusively within approved geographic and legal jurisdictions to comply with regulatory and contractual sovereignty requirements.
- **ID:** `obj_dp_restrict_data_usage`
  **Name:** Restrict Third-Party Data Usage
  **Description:** Explicitly control and restrict how data can be utilized by external systems and vendors, specifically preventing unauthorized secondary uses such as foundational model training.
- **ID:** `obj_dp_protect_in_use`
  **Name:** Protect Data in Use
  **Description:** Ensure sensitive data is encrypted, isolated, and safeguarded from unauthorized access or tampering while actively being processed in memory (e.g., via Trusted Execution Environments).
- **ID:** `obj_dp_customer_managed_keys`
  **Name:** Enable Customer-Managed Keys
  **Description:** Enable tenants to supply, manage, rotate, and independently revoke their own cryptographic keys (BYOK/CMK) to maintain absolute sovereign control over their encrypted data.
- **ID:** `obj_dp_e2ee`
  **Name:** Enforce End-to-End Encryption
  **Description:** Ensure sensitive data is encrypted at the source and decrypted exclusively at the final trusted destination, strictly preventing intermediate systems, routing components, or third-party service providers from accessing the plaintext data.
- **ID:** `obj_dp_entitlement_mirroring`
  **Name:** Enforce Entitlement Mirroring
  **Description:** Continuously synchronize and enforce the original source-system Access Control Lists (ACLs) and Document-Level Security (DLS) attributes on all ingested or federated data to ensure access boundaries are strictly preserved.

**3. Application & Service Security (AS)**
- **ID:** `obj_as_validate_inputs`
  **Name:** Validate and Sanitize All Inputs
  **Description:** Sanitize all data received from untrusted sources to prevent injection-style attacks.
- **ID:** `obj_as_manage_dependencies`
  **Name:** Securely Manage Third-Party Dependencies
  **Description:** Maintain an inventory of all third-party components and continuously scan for known vulnerabilities.
- **ID:** `obj_as_secure_apis`
  **Name:** Secure APIs and Endpoints
  **Description:** Ensure all APIs enforce authentication, authorization, input validation, and rate limiting.
- **ID:** `obj_as_secure_config`
  **Name:** Maintain Secure Configurations
  **Description:** Harden all application and service configurations by disabling unnecessary features and changing default credentials.
- **ID:** `obj_as_isolate_untrusted_code`
  **Name:** Isolate Untrusted Code Execution
  **Description:** Execute any code from untrusted sources within a secure, sandboxed environment with limited permissions.



**4. Infrastructure & Network Security (INS)**
- **ID:** `obj_ins_isolate_networks`
  **Name:** Isolate Network Environments
  **Description:** Segregate networks based on trust levels and environment type.
- **ID:** `obj_ins_microsegmentation`
  **Name:** Implement Micro-segmentation
  **Description:** Apply fine-grained network policies to control traffic flow between individual workloads.
- **ID:** `obj_ins_harden_endpoints`
  **Name:** Harden Compute Instances and Endpoints
  **Description:** Apply secure baseline configurations to all servers, containers, and virtual machines, including regular patching.
- **ID:** `obj_ins_protect_perimeter`
  **Name:** Protect Against External Network Threats
  **Description:** Deploy controls like Web Application Firewalls (WAF) and DDoS mitigation services at the network edge.

- **ID:** `obj_ins_restrict_egress`
  **Name:** Restrict Outbound Network Traffic
  **Description:** Enforce strict, default-deny egress filtering policies at the network boundary to ensure internal components can only initiate outbound connections to explicitly approved, business-justified external destinations.
- **ID:** `obj_ins_strict_env_isolation`
  **Name:** Enforce Strict Environment Isolation
  **Description:** Strictly segregate non-production (e.g., DEV, UAT) and production/DR environments—including their identities, credentials, configurations, and underlying infrastructure—to fundamentally prevent cross-environment pivoting and unauthorized access.
- **ID:** `obj_ins_protect_routing`
  **Name:** Protect Naming and Routing Infrastructure
  **Description:** Ensure foundational network naming and routing services (e.g., DNS, BGP) are cryptographically secured and strictly access-controlled to prevent unauthorized modification and traffic misdirection.  

**5. Logging, Monitoring, & Detection (LMD)**
- **ID:** `obj_lmd_generate_logs`
  **Name:** Generate Comprehensive Audit Logs
  **Description:** Ensure all systems and applications generate detailed, immutable logs for security-relevant events.
- **ID:** `obj_lmd_centralize_logs`
  **Name:** Centrally Monitor and Analyze Logs
  **Description:** Aggregate logs from all sources into a central system for monitoring, analysis, and alerting.
- **ID:** `obj_lmd_implement_threat_detection`
  **Name:** Implement Threat Detection Mechanisms
  **Description:** Deploy tools and systems to actively detect anomalous or malicious activity in real-time.

- **ID:** `obj_lmd_protect_log_integrity`
  **Name:** Protect Log Integrity
  **Description:** Protect audit logs and telemetry data from unauthorized access, modification, or deletion by enforcing immutable storage architectures and strict access controls.
- **ID:** `obj_lmd_tenant_aware_logging`
  **Name:** Enforce Tenant-Aware Auditing
  **Description:** Ensure all logs and telemetry data generated within multi-tenant environments explicitly include a verifiable tenant identifier to enable accurate attribution, isolation monitoring, and cross-tenant anomaly detection.

**6. Resilience & Availability (RA)**
- **ID:** `obj_ra_data_backup`
  **Name:** Implement Data Backup and Recovery
  **Description:** Regularly back up critical data and test the ability to restore it securely and completely.
- **ID:** `obj_ra_ensure_availability`
  **Name:** Ensure System Resilience and Availability
  **Description:** Design systems for high availability through redundancy, failover, and graceful degradation.
- **ID:** `obj_ra_incident_response`
  **Name:** Develop Incident Response Plan
  **Description:** Maintain and test a plan to effectively respond to and recover from security incidents.


**[Existing Threats]** 
**Spoofing (Violates Authenticity)**
1. **ID:** `thr_s_network_spoofing` | **Name:** Network & Protocol Spoofing | **Description:** Forging network-level identifiers to masquerade as a trusted node. (Includes: IP Spoofing, MAC Spoofing, DNS Cache Poisoning, BGP Hijacking).
2. **ID:** `thr_s_message_spoofing` | **Name:** Message & Sender Spoofing | **Description:** Forging the origin of human-readable or system messages to trick recipients. (Includes: Email/Phishing Spoofing, SMS Spoofing, Caller ID Spoofing).
3. **ID:** `thr_s_credential_reuse` | **Name:** Credential Theft & Reuse | **Description:** Capturing and reusing valid authentication material to impersonate a user. (Includes: Session Hijacking, Pass-the-Hash, Token Replay).
4. **ID:** `thr_s_phishing_facilitation` | **Name:** Phishing Facilitation via Trusted Domains | **Description:** Exploiting Open Redirect vulnerabilities within an application's routing logic to generate malicious links that rely on the application's trusted domain to deceive users.
5. **ID:** `thr_s_workload_impersonation` | **Name:** Workload & Service Impersonation | **Description:** A malicious component successfully pretending to be a trusted backend system or API. (Includes: Rogue Access Points, Fake Backend Services, Machine Identity Theft).

**Tampering (Violates Integrity)**
6. **ID:** `thr_t_server_side_injection` | **Name:** Server-Side Code/Command Injection | **Description:** Injecting malicious payloads that execute on the backend server or database. (Includes: SQL Injection, NoSQL Injection, OS Command Injection, LDAP Injection, Server-Side Template Injection).
7. **ID:** `thr_t_client_side_injection` | **Name:** Client-Side Code Injection | **Description:** Injecting malicious payloads that execute within the victim's browser or client application. (Includes: Stored XSS, Reflected XSS, DOM-based XSS, HTML Injection).
8. **ID:** `thr_t_data_modification` | **Name:** Unauthorized Data Modification | **Description:** Directly altering data states without going through authorized application logic. (Includes: Man-in-the-Middle tampering, direct database alteration, malicious file uploads replacing legitimate files).
9. **ID:** `thr_t_config_manipulation` | **Name:** Configuration Manipulation | **Description:** Altering system, network, or application settings to weaken security posture. (Includes: Changing routing tables, downgrading TLS requirements, modifying IAM policies).
10. **ID:** `thr_t_vulnerable_dependency_exploitation` | **Name:** Exploitation of Known Vulnerabilities (CVEs) | **Description:** Exploiting publicly disclosed vulnerabilities (CVEs) present in outdated or unpatched open-source libraries incorporated into the application.
11. **ID:** `thr_t_untrusted_image_execution` | **Name:** Execution of Untrusted/Malicious Images | **Description:** The pulling and execution of container images from untrusted, unverified, or compromised registries, deploying malware into the cluster.
12. **ID:** `thr_t_log_poisoning` | **Name:** Log Poisoning & Forging | **Description:** The malicious injection of forged, malicious, or malformed data into log streams (e.g., via CRLF injection) to manipulate forensic analysis, obfuscate attack activity, or exploit downstream log parsing/SIEM tools.
13. **ID:** `thr_t_supply_chain_poisoning` | **Name:** Supply Chain & Dependency Poisoning | **Description:** Tampering with upstream code or infrastructure to compromise downstream applications. (Includes: Malicious NPM/PyPI packages, compromised CI/CD pipelines, compromised base container images).

**Repudiation (Violates Non-repudiation)**
14. **ID:** `thr_r_insufficient_logging` | **Name:** Insufficient / Missing Telemetry | **Description:** Failing to generate records for security-critical events, making investigations impossible. (Includes: Unlogged logins, missing transaction histories, lack of network flow logs).
15. **ID:** `thr_r_audit_trail_evasion` | **Name:** Audit Trail Evasion & Deletion | **Description:** Active tampering with existing logs by an attacker to cover their tracks. (Includes: Clearing event logs, disabling monitoring agents, log injection/flooding).
16. **ID:** `thr_r_crypto_repudiation` | **Name:** Cryptographic Repudiation | **Description:** The inability to mathematically prove the origin or integrity of an action. (Includes: Missing digital signatures, compromised private signing keys, use of deprecated hashing algorithms).

**Information Disclosure (Violates Confidentiality)**
17. **ID:** `thr_i_data_leakage_transit` | **Name:** Data Leakage in Transit | **Description:** Exposure of sensitive data as it travels across networks. (Includes: Cleartext protocols (HTTP/Telnet), weak TLS cipher suites, network sniffing).
18. **ID:** `thr_i_data_exfiltration` | **Name:** Command and Control (C2) & Data Exfiltration | **Description:** The unauthorized outbound network communication from a compromised internal workload to an external, attacker-controlled infrastructure for the purpose of receiving malicious commands, downloading secondary payloads, or exfiltrating sensitive organizational data.
19. **ID:** `thr_i_third_party_data_exposure` | **Name:** Unintentional Third-Party Data Exposure | **Description:** The inadvertent or unauthorized transmission of sensitive data (in cleartext or unredacted forms) to external vendors, APIs, or systems.
20. **ID:** `thr_i_data_leakage_rest` | **Name:** Data Leakage at Rest | **Description:** Exposure of sensitive data stored on persistent media. (Includes: Unencrypted databases, public S3 buckets, stolen physical hard drives, lost backup tapes).
21. **ID:** `thr_i_data_sovereignty_violation` | **Name:** Data Sovereignty Violation | **Description:** The storage, processing, or routing of data outside of legally or contractually permitted geographic and jurisdictional boundaries.
22. **ID:** `thr_i_third_party_data_misuse` | **Name:** Third-Party Data Misuse | **Description:** The unauthorized retention, processing, or secondary utilization of organizational data by trusted third-party vendors (e.g., unauthorized AI/ML model training).
23. **ID:** `thr_i_file_directory_exposure` | **Name:** File & Directory Exposure | **Description:** Accessing raw files or directories outside the intended application boundaries. (Includes: Directory Traversal, Local File Inclusion (LFI), exposed `.git` folders).
24. **ID:** `thr_i_unauthorized_data_exfiltration` | **Name:** Unauthorized Data Exfiltration | **Description:** The covert smuggling of sensitive system data out to external, attacker-controlled infrastructure.
25. **ID:** `thr_i_metadata_error_leakage` | **Name:** System Metadata & Error Leakage | **Description:** Revealing internal system configurations or architectures to an attacker. (Includes: Verbose stack traces, exposed cloud metadata APIs (SSRF targets), banner grabbing).
26. **ID:** `thr_i_sensitive_data_logging` | **Name:** Plaintext Sensitive Data Logging | **Description:** The inadvertent recording of highly sensitive data (passwords, PII, API tokens, credit cards) in plaintext within application logs or telemetry streams.
27. **ID:** `thr_i_log_data_exposure` | **Name:** Log Data Exposure | **Description:** The inadvertent exposure of sensitive information (e.g., PII, PHI, credentials, or authentication tokens) resulting from writing unredacted raw requests, responses, or error states directly into telemetry and log repositories.
28. **ID:** `thr_i_data_remanence` | **Name:** Data Remanence and Spillage | **Description:** The incomplete deletion of data leading to residual sensitive information in memory, temporary storage, or shared infrastructure being exposed to unauthorized entities or subsequent processes.
29. **ID:** `thr_i_third_party_breach` | **Name:** Third-Party Infrastructure Breach | **Description:** The unauthorized access, exposure, or compromise of sensitive data and credentials hosted within a trusted third-party vendor's infrastructure or SaaS platform.
30. **ID:** `thr_i_side_channel_leakage` | **Name:** Side-Channel Information Leakage | **Description:** Inferring sensitive data by observing indirect system behaviors. (Includes: Timing attacks, power consumption analysis, differential response sizes).

**Denial of Service (Violates Availability)**
31. **ID:** `thr_d_data_destruction` | **Name:** Data Destruction & Ransomware | **Description:** Permanent loss, malicious deletion, or unauthorized encryption of data resulting in unrecoverable states and severe availability impacts.
32. **ID:** `thr_d_network_volumetric` | **Name:** Network Volumetric Flooding | **Description:** Overwhelming network bandwidth or infrastructure with a massive volume of traffic. (Includes: UDP Floods, SYN Floods, ICMP Floods, DNS Amplification).
33. **ID:** `thr_d_application_exhaustion` | **Name:** Application Logic Exhaustion | **Description:** Sending targeted, complex requests designed to tie up application processing power. (Includes: HTTP Slowloris, Regex Denial of Service (ReDoS), computationally expensive GraphQL queries).
34. **ID:** `thr_d_system_resource_depletion` | **Name:** System Resource Depletion | **Description:** Consuming finite infrastructure resources until the system crashes or halts. (Includes: Disk space exhaustion (log flooding), memory leaks, database connection pool exhaustion).

**Elevation of Privilege (Violates Authorization)**
35. **ID:** `thr_e_insider_abuse` | **Name:** Insider Privilege Abuse | **Description:** The malicious or negligent misuse of legitimate organizational access by internal employees, contractors, or compromised internal services to access, modify, or exfiltrate highly sensitive assets (such as customer secrets) outside their strict operational purview.
36. **ID:** `thr_e_permission_drift` | **Name:** Permission Drift & Entitlement Loss | **Description:** The failure to accurately maintain, continuously synchronize, and enforce original source-system access control lists (ACLs) during data ingestion or federation, resulting in the unauthorized exposure of restricted data within aggregated repositories.
37. **ID:** `thr_e_delegated_authority_abuse` | **Name:** Delegated Authority Abuse | **Description:** A threat where an attacker exploits the trusted relationship between an intermediary platform and a downstream system. The attacker uses the platform's legitimate, delegated credentials to perform malicious or unauthorized actions that they could not have performed directly.
38. **ID:** `thr_e_horizontal_escalation` | **Name:** Horizontal Privilege Escalation | **Description:** Accessing data or functions belonging to another user with the *same* level of access. (Includes: Broken Object Level Authorization (BOLA), Insecure Direct Object References (IDOR), session hijacking of peers).
39. **ID:** `thr_e_vertical_escalation` | **Name:** Vertical Privilege Escalation | **Description:** A lower-privileged user or system gaining administrative or higher-level access. (Includes: Exploiting misconfigured role-based access control (RBAC), parameter tampering to gain "admin=true").
40. **ID:** `thr_e_environment_breakout` | **Name:** Execution Environment Breakout | **Description:** Escaping an isolated execution boundary to access the underlying host or network. (Includes: Container escape, Virtual Machine (VM) escape, application sandbox evasion).
41. **ID:** `thr_e_lateral_movement` | **Name:** Lateral Movement | **Description:** The progressive compromise of adjacent systems, workloads, or services within a network to expand access, perform unauthorized network traversal, and reach higher-value assets after an initial perimeter breach.
42. **ID:** `thr_e_auth_bypass` | **Name:** Authentication / Authorization Bypass | **Description:** Completely circumventing the access control mechanism to reach protected areas. (Includes: Forced browsing to hidden administrative URLs, exploiting logic flaws in SSO flows).
43. **ID:** `thr_e_identity_drift` | **Name:** Identity Mapping Collision & Lifecycle Drift | **Description:** The unauthorized impersonation of another user by manipulating mutable identity attributes (e.g., email), or the failure to de-provision access from downstream systems for terminated users, resulting in orphaned accounts.
44. **ID:** `thr_e_orphaned_access_abuse` | **Name:** Orphaned Account Abuse | **Description:** The exploitation of active credentials, tokens, or sessions belonging to terminated or transferred personnel due to failed de-provisioning or cross-domain lifecycle drift.
45. **ID:** `thr_e_identity_mapping_abuse` | **Name:** Identity Mapping Abuse | **Description:** An attack where a flaw in the identity provisioning or federation logic allows an attacker to link their account to a victim's identity, resulting in a full account takeover within the system.



**Output Format:**
Please format your response exactly as follows:

- **Control Pattern Title:** [Extract or deduce the title of the pattern]
- **Mitigated Threats:**
  - [Threat 1] *(Tag: Existing or New)*
  - [Threat 2] *(Tag: Existing or New)*

- **Associated Control Objectives:**
  - [Objective 1] *(Tag: Existing or New)*
  - [Objective 2] *(Tag: Existing or New)*
- **New Threat Added (if any):**
  - **[New Threat Name(with id)]:** [Brief definition describing WHAT Threat to protect against, what category it belongs to (S - Spoofing (Violates Authenticity),T - Tampering (Violates Integrity) , R - Repudiation (Violates Non-repudiation), I - Information Disclosure (Violates Confidentiality),D - Denial of Service (Violates Availability)) ]

- **New Control Objectives Added (if any):**
  - **[New Objective Name(with id)]:** [Brief definition describing WHAT must be accomplished]
- **Reasoning:**[Brief explanation of why this pattern maps to these specific objectives, risks, threats]
- **enhanced Control Pattern:** if provided the control pattern needs to be enhanced.

**[Control Pattern]**
*(Insert the control pattern description/details here)*

***
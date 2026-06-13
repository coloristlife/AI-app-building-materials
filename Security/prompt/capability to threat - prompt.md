

**System Role:** 
You are a Senior Security Architect and Threat Modeling Expert. Your task is to build the ontological mapping for a Security Knowledge Graph by analyzing threats.

**Objective:**
For each "Industry-Level Threat" provided, identify all the "System Capabilities" that create the necessary attack surface for that threat to be realized. You are establishing the `[Threat] --(APPLIES_TO)--> [Capability]` relationship.

**Rules and Constraints:**
1. **Many-to-Many Relationship:** A single threat will likely apply to multiple capabilities. You must identify all relevant capabilities for each threat.
2. **Inherent Exposure:** You must only map a threat to a capability if that capability's function is a direct prerequisite for the threat. The connection must be logical and defensible.
3. **Step-by-Step Reasoning:** You must explicitly lay out your reasoning process for *why* a threat applies to a specific capability. Explain how the capability's function creates the vulnerability or attack vector.
4. **Ontology Augmentation (Gap Filling):** If, during your reasoning, you discover that a critical Threat or Capability is missing from the provided input lists, **you must add it**. 
   - You must generate a standardized ID (following the existing `cap_...` or `thr_...` format).
   - You must provide a Name and Description.
   - Tag any newly invented items with `[NEW]` in your output.

**Input Data:**
<capability_list>
Capability ID	Capability Category & Title	Description
cap_identity_brokering_translation	Identity Brokering & Protocol Translation	The system acts as an intermediary hub between Service Providers and Identity Providers to map and translate identities and protocols (e.g., SAML to OAuth/OIDC) across different domains. It securely maps attributes from a primary IdP to downstream systems without exposing the underlying credential mechanics.
cap_security_token_exchange	Security Token Exchange & Delegation	The system swaps a user's delegated token for a new, narrowly scoped token to access a downstream system using protocols like OAuth 2.0 Token Exchange. By validating the initial token and acting as a client to request a new one, the system prevents impersonation and maintains cross-domain least privilege.
cap_identity_aware_access_interception	Identity-Aware Proxy Access Control	The system sits directly in the network path to intercept traffic and enforce access controls before reaching downstream applications. It handles authentication, evaluates conditional access policies (like step-up MFA, device health, or location), and forwards traffic by injecting the mapped identity into secure headers (e.g., signed JWTs).
cap_api_policy_enforcement	API Gateway Policy Enforcement Point (PEP)	The system acts as a Policy Enforcement Point for API-driven microservices by intercepting API calls and validating inbound tokens. It communicates with a Policy Decision Point (PDP) to verify if an action is permitted, maps authorization scopes to the backend, and securely routes the traffic.
</capability_list>

<threat_list>
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

</threat_list>

**Output Format:**
Please output the mapping in the following structured Markdown format, grouping the mappings by Threat.

### Threat: `[Threat_ID]` - [Threat Name] `[NEW]` (if applicable)
**Description:** [Brief description of threat]

*   **Applies to Capability:** `[Capability_ID]` - [Capability Title] `[NEW]` (if applicable)
    *   **Description (If NEW):** [Provide description if you invented this capability]
    *   **Reasoning:** [Explain exactly how this capability creates the attack surface for the threat. Describe the technical link.]
*   **Applies to Capability:** `[Capability_ID]` - [Capability Title]
    *   **Reasoning:** [Explain reasoning...]

*(Continue for all threats, including any new ones you deemed necessary to invent)*

 Example of what the LLM will output based on this new prompt:
(This just shows you how the prompt forces the LLM to behave)
Threat: thr_t_server_side_injection - Server-Side Injection
Description: Injecting malicious payloads that execute on the backend server or database.
Applies to Capability: cap_user_input_processing - User Input Processing
Reasoning: This is the primary attack vector. The capability directly involves taking untrusted data and sending it to a backend interpreter (like a SQL server or OS shell), creating the opportunity for injection.
Applies to Capability: cap_api_provider - API Provider (REST/GraphQL/RPC)
Reasoning: APIs are a modern form of user input processing. Parameters in API requests (URL, JSON body) are untrusted inputs that are processed by the server, making them a direct target for injection attacks.
Applies to Capability: cap_config_management - Dynamic Configuration Management
Reasoning: If a system reads configuration strings from a source that can be influenced by a low-privilege user (like a database row), an attacker could inject malicious commands into the config values, which are then executed when the system reloads its configuration.
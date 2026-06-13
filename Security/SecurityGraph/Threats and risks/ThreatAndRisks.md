

[Capability] --(EXPOSED_TO)--> [Threat] --(CAUSES)--> [Business Risk]

- Capability: cap_public_api_listener (The system can receive internet traffic).
- Exposed to Threat: thr_d_network_volumetric (Volumetric DDoS Attack).
- Mitigated by: obj_ins_protect_perimeter (Protect against external network threats).
- Caused Business Risk: risk_fin_revenue_loss (If the DDoS succeeds, the site goes down, and you lose sales).


#### **S - Spoofing (Violates Authenticity)**
*Focus: Illegitimate impersonation of entities or routing mechanisms.*

| Threat ID | Threat Category | Description & Included Specifics |
| :--- | :--- | :--- |
| `thr_s_network_spoofing` | Network & Protocol Spoofing | Forging network-level identifiers to masquerade as a trusted node. *(Includes: IP Spoofing, MAC Spoofing, DNS Cache Poisoning, BGP Hijacking).* |
| `thr_s_message_spoofing` | Message & Sender Spoofing | Forging the origin of human-readable or system messages to trick recipients. *(Includes: Email/Phishing Spoofing, SMS Spoofing, Caller ID Spoofing).* |
| `thr_s_credential_reuse` | Credential Theft & Reuse | Capturing and reusing valid authentication material to impersonate a user. *(Includes: Session Hijacking, Pass-the-Hash, Token Replay).* |
| `thr_s_workload_impersonation` | Workload & Service Impersonation | A malicious component successfully pretending to be a trusted backend system or API. *(Includes: Rogue Access Points, Fake Backend Services, Machine Identity Theft).* |

#### **T - Tampering (Violates Integrity)**
*Focus: Unauthorized modification of code, data, or configurations. (Injection flaws are consistently leveled here).*

| Threat ID | Threat Category | Description & Included Specifics |
| :--- | :--- | :--- |
| `thr_t_server_side_injection` | Server-Side Code/Command Injection | Injecting malicious payloads that execute on the backend server or database. *(Includes: SQL Injection, NoSQL Injection, OS Command Injection, LDAP Injection, Server-Side Template Injection).* |
| `thr_t_client_side_injection` | Client-Side Code Injection | Injecting malicious payloads that execute within the victim's browser or client application. *(Includes: Stored XSS, Reflected XSS, DOM-based XSS, HTML Injection).* |
| `thr_t_data_modification` | Unauthorized Data Modification | Directly altering data states without going through authorized application logic. *(Includes: Man-in-the-Middle tampering, direct database alteration, malicious file uploads replacing legitimate files).* |
| `thr_t_config_manipulation` | Configuration Manipulation | Altering system, network, or application settings to weaken security posture. *(Includes: Changing routing tables, downgrading TLS requirements, modifying IAM policies).* |
| `thr_t_supply_chain_poisoning` | Supply Chain & Dependency Poisoning | Tampering with upstream code or infrastructure to compromise downstream applications. *(Includes: Malicious NPM/PyPI packages, compromised CI/CD pipelines, compromised base container images).* |

#### **R - Repudiation (Violates Non-repudiation)**
*Focus: The inability to prove an action occurred or who performed it.*

| Threat ID | Threat Category | Description & Included Specifics |
| :--- | :--- | :--- |
| `thr_r_insufficient_logging` | Insufficient / Missing Telemetry | Failing to generate records for security-critical events, making investigations impossible. *(Includes: Unlogged logins, missing transaction histories, lack of network flow logs).* |
| `thr_r_audit_trail_evasion` | Audit Trail Evasion & Deletion | Active tampering with existing logs by an attacker to cover their tracks. *(Includes: Clearing event logs, disabling monitoring agents, log injection/flooding).* |
| `thr_r_crypto_repudiation` | Cryptographic Repudiation | The inability to mathematically prove the origin or integrity of an action. *(Includes: Missing digital signatures, compromised private signing keys, use of deprecated hashing algorithms).* |

#### **I - Information Disclosure (Violates Confidentiality)**
*Focus: Unauthorized exposure of data or system internals.*

| Threat ID | Threat Category | Description & Included Specifics |
| :--- | :--- | :--- |
| `thr_i_data_leakage_transit` | Data Leakage in Transit | Exposure of sensitive data as it travels across networks. *(Includes: Cleartext protocols (HTTP/Telnet), weak TLS cipher suites, network sniffing).* |
| `thr_i_data_leakage_rest` | Data Leakage at Rest | Exposure of sensitive data stored on persistent media. *(Includes: Unencrypted databases, public S3 buckets, stolen physical hard drives, lost backup tapes).* |
| `thr_i_file_directory_exposure` | File & Directory Exposure | Accessing raw files or directories outside the intended application boundaries. *(Includes: Directory Traversal, Local File Inclusion (LFI), exposed `.git` folders).* |
| `thr_i_metadata_error_leakage` | System Metadata & Error Leakage | Revealing internal system configurations or architectures to an attacker. *(Includes: Verbose stack traces, exposed cloud metadata APIs (SSRF targets), banner grabbing).* |
| `thr_i_side_channel_leakage` | Side-Channel Information Leakage | Inferring sensitive data by observing indirect system behaviors. *(Includes: Timing attacks, power consumption analysis, differential response sizes).* |

#### **D - Denial of Service (Violates Availability)**
*Focus: Disrupting the accessibility of systems or data.*

| Threat ID | Threat Category | Description & Included Specifics |
| :--- | :--- | :--- |
| `thr_d_network_volumetric` | Network Volumetric Flooding | Overwhelming network bandwidth or infrastructure with a massive volume of traffic. *(Includes: UDP Floods, SYN Floods, ICMP Floods, DNS Amplification).* |
| `thr_d_application_exhaustion` | Application Logic Exhaustion | Sending targeted, complex requests designed to tie up application processing power. *(Includes: HTTP Slowloris, Regex Denial of Service (ReDoS), computationally expensive GraphQL queries).* |
| `thr_d_system_resource_depletion` | System Resource Depletion | Consuming finite infrastructure resources until the system crashes or halts. *(Includes: Disk space exhaustion (log flooding), memory leaks, database connection pool exhaustion).* |

#### **E - Elevation of Privilege (Violates Authorization)**
*Focus: Bypassing intended permission boundaries to perform unauthorized actions.*

| Threat ID | Threat Category | Description & Included Specifics |
| :--- | :--- | :--- |
| `thr_e_horizontal_escalation` | Horizontal Privilege Escalation | Accessing data or functions belonging to another user with the *same* level of access. *(Includes: Broken Object Level Authorization (BOLA), Insecure Direct Object References (IDOR), session hijacking of peers).* |
| `thr_e_vertical_escalation` | Vertical Privilege Escalation | A lower-privileged user or system gaining administrative or higher-level access. *(Includes: Exploiting misconfigured role-based access control (RBAC), parameter tampering to gain "admin=true").* |
| `thr_e_environment_breakout` | Execution Environment Breakout | Escaping an isolated execution boundary to access the underlying host or network. *(Includes: Container escape, Virtual Machine (VM) escape, application sandbox evasion).* |
| `thr_e_auth_bypass` | Authentication / Authorization Bypass | Completely circumventing the access control mechanism to reach protected areas. *(Includes: Forced browsing to hidden administrative URLs, exploiting logic flaws in SSO flows).* |



`[Risk]` --`(CAUSED_BY)`--> `[Threat]`

This is a **Many-to-Many** relationship.
*   One `Risk` (e.g., `risk_comp_regulatory_fines`) can be caused by many different `Threats` (any threat that exposes regulated data).
*   One `Threat` (e.g., `thr_i_sensitive_data_exposure`) can lead to many different `Risks` (Financial, Reputational, and Compliance).


#### **1. Financial & Economic Risks**
*This category includes any risk that results in a direct or indirect monetary loss.*

| Risk ID | Business Risk Name | Description & Common Scenarios | Example Underlying Threats |
| :--- | :--- | :--- | :--- |
| `risk_fin_direct_loss` | Direct Financial Loss | Theft of funds through fraudulent transactions, wire transfer fraud, or direct manipulation of financial systems. | `thr_s_email_spoofing`, `thr_e_privilege_escalation` |
| `risk_fin_remediation_cost` | Incident Remediation Costs | The direct costs associated with responding to a security breach, including forensics, consulting fees, identity theft protection for customers, and PR. | `thr_i_sensitive_data_exposure`, Ransomware |
| `risk_fin_revenue_loss` | Loss of Revenue | Loss of income due to system downtime, inability to process transactions, or customers leaving for competitors after an incident. | `thr_d_network_flood`, `thr_d_application_dos` |
| `risk_fin_fraud` | Customer or Internal Fraud | Unauthorized use of systems to commit fraud, leading to financial write-offs and reimbursement costs. | `thr_s_credential_replay`, `thr_e_broken_access_control` |
| `risk_fin_ransom` | Ransom Payment | Financial loss due to paying a ransom to recover data or restore system functionality after a ransomware attack. | Ransomware, `thr_t_data_modification` |

#### **2. Reputational & Brand Risks**
*This category covers damage to the company's public image, brand equity, and customer trust.*

| Risk ID | Business Risk Name | Description & Common Scenarios | Example Underlying Threats |
| :--- | :--- | :--- | :--- |
| `risk_rep_trust_erosion` | Loss of Customer Trust | A security incident, especially one involving personal data, erodes customer confidence in the company's ability to protect them, leading to churn. | `thr_i_sensitive_data_exposure`, `thr_cloud_misconfiguration` |
| `risk_rep_negative_media` | Negative Media Coverage | Widespread negative publicity following a breach, impacting stock price, customer acquisition, and partner relationships. | Any major public breach |
| `risk_rep_brand_damage` | Brand Devaluation | Long-term damage to the brand's image of being reliable, secure, or ethical. | `thr_i_sensitive_data_exposure` (especially of PII/PHI) |
| `risk_rep_partner_loss` | Loss of Partner Confidence | Business partners severing ties due to the perceived security risk of being associated with the compromised company. | `thr_t_dependency_poisoning` (supply chain) |

#### **3. Operational & Business Disruption Risks**
*This category includes any risk that impedes the company's ability to conduct its core business operations.*

| Risk ID | Business Risk Name | Description & Common Scenarios | Example Underlying Threats |
| :--- | :--- | :--- | :--- |
| `risk_ops_process_interruption` | Business Process Interruption | Core business processes are halted or severely degraded due to system unavailability or data integrity issues. | `thr_d_application_dos`, Ransomware |
| `risk_ops_productivity_loss` | Loss of Employee Productivity | Employees are unable to perform their jobs because internal systems, tools, or data are unavailable. | Ransomware, `thr_d_resource_exhaustion` |
| `risk_ops_supply_chain` | Supply Chain Disruption | A compromise of a key supplier or a compromise originating from the company affects its partners, halting the flow of goods or services. | `thr_t_dependency_poisoning` |
| `risk_ops_data_integrity` | Loss of Data Integrity | Core business data is corrupted, deleted, or altered, making it unreliable for operations and decision-making. | `thr_t_data_modification`, `thr_t_log_tampering` |

#### **4. Legal, Regulatory & Compliance Risks**
*This category covers risks stemming from the failure to comply with laws, regulations, and contractual obligations.*

| Risk ID | Business Risk Name | Description & Common Scenarios | Example Underlying Threats |
| :--- | :--- | :--- | :--- |
| `risk_comp_regulatory_fines` | Regulatory Fines and Penalties | Fines levied by government bodies for non-compliance with regulations like GDPR, CCPA, HIPAA, etc., following a data breach. | `thr_i_sensitive_data_exposure` |
| `risk_comp_litigation` | Lawsuits and Legal Action | Class-action lawsuits from affected customers, or legal action from business partners, due to damages caused by a security incident. | Any major data breach |
| `risk_comp_certification_loss` | Loss of Certifications | Revocation of critical industry certifications (e.g., PCI DSS, SOC 2, FedRAMP), making it impossible to legally operate in certain markets. | Any threat violating a specific compliance control |
| `risk_comp_contract_breach` | Breach of Contract | Failure to meet security obligations outlined in contracts with customers or partners, leading to penalties or termination of agreements. | Any security incident |

#### **5. Strategic & Competitive Risks**
*This category includes risks that impact the company's long-term strategy, market position, and competitive advantage.*

| Risk ID | Business Risk Name | Description & Common Scenarios | Example Underlying Threats |
| :--- | :--- | :--- | :--- |
| `risk_strat_ip_theft` | Theft of Intellectual Property | Theft of trade secrets, proprietary algorithms, product designs, or strategic plans by competitors or nation-state actors. | `thr_i_sensitive_data_exposure`, Corporate Espionage |
| `risk_strat_competitive_disadvantage` | Loss of Competitive Advantage | A competitor uses stolen IP to get to market faster or replicate a key product feature. | `risk_strat_ip_theft` |
| `risk_strat_innovation_hindrance` | Hindrance to Innovation | Security incidents or fear thereof cause the company to become overly risk-averse, slowing down product development and innovation. | All |
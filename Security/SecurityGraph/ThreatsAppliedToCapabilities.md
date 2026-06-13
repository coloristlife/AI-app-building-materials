
Here is the comprehensive ontological mapping correctly grouped by **Threat**, establishing the `[Threat] --(APPLIES_TO)--> [Capability]` relationships. 
 the necessary `[NEW]` nodes are included to fill out missing logical links in the attack surface model.

***

### Threat: `thr_s_network_spoofing` - Network & Protocol Spoofing
**Description:** Forging network identifiers (IP, DNS, BGP) to masquerade as a trusted node.
*   **Applies to Capability:** `cap_data_transit_external` - External Data Transmission
    *   **Reasoning:** Transmitting data across the public internet relies on external routing and DNS. This inherent trust in unmanaged infrastructure creates the opportunity for attackers to hijack BGP routes or spoof DNS responses to redirect traffic.
*   **Applies to Capability:** `cap_data_transit_internal` - Internal Data Transmission
    *   **Reasoning:** Internal networks often trust local ARP or internal DNS resolution. Relying on local resolution exposes the system to Layer 2/3 spoofing attacks (like ARP poisoning) where a compromised internal host can impersonate a trusted peer.

### Threat: `thr_s_message_spoofing` - Message & Sender Spoofing
**Description:** Forging message origins (Email/Phishing, SMS) to trick recipients.
*   **Applies to Capability:** `cap_email_sms_transmission` - Outbound Messaging (Email/SMS)
    *   **Reasoning:** The ability to dynamically generate outbound communications is the exact attack surface needed for spoofing. If this capability allows unvalidated input into message headers or bodies, an attacker can forge the "From" origin and leverage the trusted system to send phishing campaigns.

### Threat: `thr_s_credential_reuse` - Credential Theft & Reuse
**Description:** Capturing and reusing valid auth material (Session hijacking, Pass-the-Hash, Token Replay).
*   **Applies to Capability:** `cap_user_authentication` - Human User Authentication
    *   **Reasoning:** Human authentication relies heavily on passwords, which are frequently reused across services or stolen in external breaches. Presenting a login prompt directly creates the attack surface for adversaries to replay these stolen credentials.
*   **Applies to Capability:** `cap_session_management` - Session State Management
    *   **Reasoning:** Issuing temporary tokens creates valid, high-privilege artifacts. If these tokens are stored insecurely or transmitted without protection, attackers can steal and reuse them to bypass the login process entirely.
*   **Applies to Capability:** `cap_secrets_management` - Secrets & Key Management
    *   **Reasoning:** Centralized secret vaults contain high-value credentials (API keys, DB passwords). Compromising the vault or leveraging an overly permissive access policy provides attackers with a repository of active material to steal and reuse.

### Threat: `thr_s_workload_impersonation` - Workload & Service Impersonation
**Description:** A malicious service pretending to be a trusted backend or API.
*   **Applies to Capability:** `cap_network_listener_internal` - Internal Network Listener
    *   **Reasoning:** Internal listeners often rely on perimeter security (firewalls) and implicitly trust connections from within the network. This missing boundary defense allows any compromised internal container to impersonate a trusted service.
*   **Applies to Capability:** `cap_machine_authentication` - Machine-to-Machine Authentication
    *   **Reasoning:** If M2M authentication uses static, long-lived API keys instead of short-lived identity tokens, an attacker who extracts a key from memory or source code can perfectly impersonate the workload.

### Threat: `thr_s_phishing_facilitation` - Phishing Facilitation via Trusted Domains `[NEW]`
**Description:** Exploiting Open Redirect vulnerabilities within an application's routing logic to generate malicious links that rely on the application's trusted domain to deceive users.
*   **Applies to Capability:** `cap_url_redirection` - URL Routing & Redirection
    *   **Reasoning:** Taking user input to determine a redirection destination directly enables Open Redirect attacks. Attackers craft links using the application's domain to trick users into trusting a link that stealthily bounces them to a credential-harvesting site.

### Threat: `thr_s_brute_force_attacks` - Brute-Force & Credential Stuffing `[NEW]`
**Description:** Automated, systematic guessing of credentials or the mass submission of previously breached username/password pairs against an authentication endpoint.
*   **Applies to Capability:** `cap_user_authentication` - Human User Authentication
    *   **Reasoning:** Exposing a validation endpoint for human credentials inherently creates a target for automated bots to submit millions of username/password combinations until a match is found.

### Threat: `thr_t_server_side_injection` - Server-Side Injection
**Description:** Payloads executing on backend/DB (SQLi, NoSQLi, OS Command Injection, LDAPi).
*   **Applies to Capability:** `cap_user_input_processing` - User Input Processing
    *   **Reasoning:** Accepting untrusted strings and concatenating them into backend interpreters (like a SQL database) is the fundamental prerequisite and primary attack surface for server-side injection.
*   **Applies to Capability:** `cap_file_upload_handling` - File Upload Handling
    *   **Reasoning:** If a system stores and subsequently executes uploaded files without verifying their contents, an attacker can upload an executable script (e.g., a `.php` web shell) to achieve backend code injection.
*   **Applies to Capability:** `cap_os_command_execution` - OS Command / Shell Execution
    *   **Reasoning:** Intentionally passing variables to an OS shell (`exec()`, `system()`) is extremely fragile; attackers can inject shell metacharacters (`&&`, `;`) to break out of the intended command and inject their own.

### Threat: `thr_t_client_side_injection` - Client-Side Injection
**Description:** Payloads executing in browser/client (Stored/Reflected XSS, DOM-based XSS, HTMLi).
*   **Applies to Capability:** `cap_user_input_processing` - User Input Processing
    *   **Reasoning:** The application must first accept and store or reflect the untrusted input. This capability is the ingress point for the malicious JavaScript or HTML payload.
*   **Applies to Capability:** `cap_html_ui_rendering` - Dynamic HTML/UI Rendering
    *   **Reasoning:** Dynamically generating user interfaces using untrusted data without contextual output encoding creates the execution environment for Cross-Site Scripting (XSS), causing the browser to execute the injected payload.

### Threat: `thr_t_data_modification` - Unauthorized Data Modification
**Description:** Altering data states directly (MITM tampering, direct DB alteration, malicious file replacement).
*   **Applies to Capability:** `cap_data_storage_persistent` - Persistent Data Storage
    *   **Reasoning:** The act of writing stateful data creates a physical target. If unauthorized logical access is achieved, attackers can bypass application logic and corrupt or replace the data directly on disk or in the database.
*   **Applies to Capability:** `cap_data_transit_external` - External Data Transmission
    *   **Reasoning:** Sending data across external networks without strong transport encryption and integrity checks enables active Man-in-the-Middle (MITM) attacks, allowing an adversary to alter packets in transit.
*   **Applies to Capability:** `cap_data_backup_execution` - Data Backup & Snapshotting
    *   **Reasoning:** Attackers who compromise the backup environment can tamper with snapshots, silently injecting backdoors or corrupting records so that victim restorations remain compromised.
*   **Applies to Capability:** `cap_cryptographic_operations` - Cryptographic Operations & Hashing `[NEW]`
    *   **Description (If NEW):** Performs encryption, decryption, hashing, or digital signing of data to ensure confidentiality or integrity.
    *   **Reasoning:** Improper implementation of cryptographic modes (like ECB instead of GCM) allows attackers to perform bit-flipping attacks, maliciously modifying ciphertext to decrypt into attacker-controlled plaintext.

### Threat: `thr_t_config_manipulation` - Configuration Manipulation
**Description:** Weakening security posture via settings (Changing routing, downgrading TLS, modifying IAM).
*   **Applies to Capability:** `cap_config_management` - Dynamic Configuration Management
    *   **Reasoning:** Sourcing settings from a runtime store means an attacker who compromises that store can instantly alter system behavior (e.g., bypassing feature flags, redirecting APIs, downgrading TLS) without needing to alter source code.
*   **Applies to Capability:** `cap_container_orchestration` - Container / Workload Orchestration
    *   **Reasoning:** Orchestrators are entirely driven by declarative configurations (YAML/JSON). Attackers can manipulate these to mount sensitive host directories into pods or elevate a container's privilege level.
*   **Applies to Capability:** `cap_ci_cd_build_pipeline` - Continuous Integration & Deployment Pipeline `[NEW]`
    *   **Description (If NEW):** Automates the fetching of source code, building of artifacts, running of tests, and deployment to target environments.
    *   **Reasoning:** CI/CD relies on pipeline configuration files. Modifying these configurations allows an attacker to disable automated security testing, alter build steps, or change deployment targets.

### Threat: `thr_t_supply_chain_poisoning` - Supply Chain Poisoning
**Description:** Compromising upstream code/infra (Malicious NPM/PyPI, compromised CI/CD or base images).
*   **Applies to Capability:** `cap_third_party_dependencies` - Third-Party Dependency Usage
    *   **Reasoning:** Relying on external open-source repositories inherently creates a reliance on upstream maintainers. If an upstream package is compromised or typosquatted, the malicious code is automatically pulled into the application.
*   **Applies to Capability:** `cap_ci_cd_build_pipeline` - Continuous Integration & Deployment Pipeline `[NEW]`
    *   **Reasoning:** The build pipeline is the engine that retrieves dependencies and packages artifacts. If the pipeline itself is compromised, attackers can silently inject malware into the build artifact right before it is signed and deployed.

### Threat: `thr_t_malware_distribution` - Malware Hosting & Distribution `[NEW]`
**Description:** Utilizing a legitimate application to store and serve malicious payloads, inadvertently turning the system into a malware distribution vector.
*   **Applies to Capability:** `cap_file_upload_handling` - File Upload Handling
    *   **Reasoning:** Accepting file uploads without rigorous anti-virus/malware scanning allows threat actors to upload infected documents. When other users download these files, the platform effectively becomes a trusted distributor for the malware.

### Threat: `thr_t_vulnerable_dependency_exploitation` - Exploitation of Known Vulnerabilities (CVEs) `[NEW]`
**Description:** Exploiting publicly disclosed vulnerabilities (CVEs) present in outdated or unpatched open-source libraries incorporated into the application.
*   **Applies to Capability:** `cap_third_party_dependencies` - Third-Party Dependency Usage
    *   **Reasoning:** Importing external libraries imports their technical debt. Using outdated packages exposes the application to known CVEs (e.g., Log4Shell) that adversaries can exploit using readily available exploit code.

### Threat: `thr_t_untrusted_image_execution` - Execution of Untrusted/Malicious Images `[NEW]`
**Description:** The pulling and execution of container images from untrusted, unverified, or compromised registries, deploying malware into the cluster.
*   **Applies to Capability:** `cap_container_orchestration` - Container / Workload Orchestration
    *   **Reasoning:** Orchestrators automatically pull images to run workloads. Without enforced image signing and verification mechanisms, an orchestrator can be instructed to pull and execute a maliciously crafted container image.

### Threat: `thr_r_insufficient_logging` - Insufficient Telemetry
**Description:** Failure to generate records for security-critical events.
*   **Applies to Capability:** `cap_audit_logging` - Audit & Event Logging
    *   **Reasoning:** If this capability is implemented but fails to record authorization changes, authentication failures, or critical administrative actions, it inherently causes a blindspot that prevents non-repudiation and incident response.

### Threat: `thr_r_audit_trail_evasion` - Audit Trail Evasion
**Description:** Active tampering or deletion of logs to hide activity.
*   **Applies to Capability:** `cap_audit_logging` - Audit & Event Logging
    *   **Reasoning:** Generating a log file creates a physical evidentiary artifact. Attackers who gain system access will actively seek out this capability to tamper with or delete the logs to cover their tracks.

### Threat: `thr_r_crypto_repudiation` - Cryptographic Repudiation
**Description:** Inability to prove origin/integrity due to missing signatures or weak hashing.
*   **Applies to Capability:** `cap_secrets_management` - Secrets & Key Management
    *   **Reasoning:** If the keys generated by this system are weak (e.g., short RSA keys) or compromised keys are not adequately rotated/revoked, an attacker can forge signatures, destroying the system's non-repudiation guarantees.
*   **Applies to Capability:** `cap_session_management` - Session State Management
    *   **Reasoning:** Stateless tokens (like JWTs) rely on cryptographic signatures. If the system accepts the "none" signing algorithm or uses weak HMAC secrets, attackers can forge valid tokens, breaking the ability to verify who truly initiated a request.
*   **Applies to Capability:** `cap_cryptographic_operations` - Cryptographic Operations & Hashing `[NEW]`
    *   **Reasoning:** Performing hashing or digital signing using deprecated algorithms (like MD5 or SHA-1) allows attackers to perform collision attacks, forging signatures and effectively repudiating the origin of data.

### Threat: `thr_i_data_leakage_transit` - Data Leakage in Transit
**Description:** Exposure of data moving across networks (Cleartext protocols, weak TLS, sniffing).
*   **Applies to Capability:** `cap_data_transit_external` - External Data Transmission
    *   **Reasoning:** Routing data across untrusted public boundaries without strong encryption (TLS 1.2+) exposes packets to passive sniffing, allowing attackers to read sensitive data in mid-flight.
*   **Applies to Capability:** `cap_data_transit_internal` - Internal Data Transmission
    *   **Reasoning:** Private networks are often mistakenly deemed "trusted." If mTLS is not used for internal service-to-service communication, a compromised internal host can run a packet sniffer and read sensitive API traffic.

### Threat: `thr_i_data_leakage_rest` - Data Leakage at Rest
**Description:** Exposure of stored data (Unencrypted DBs, public S3 buckets, stolen media).
*   **Applies to Capability:** `cap_data_storage_persistent` - Persistent Data Storage
    *   **Reasoning:** Writing data to disks or buckets creates a static repository. If at-rest encryption or strict bucket access policies are missing, attackers can directly access and exfiltrate the stored sensitive data.
*   **Applies to Capability:** `cap_config_management` - Dynamic Configuration Management
    *   **Reasoning:** Configuration stores frequently house connection strings, private keys, and API tokens. If the store lacks field-level encryption, these high-value secrets are exposed.
*   **Applies to Capability:** `cap_data_backup_execution` - Data Backup & Snapshotting
    *   **Reasoning:** Backups are duplicate data stores. If a backup is taken of a secure database but saved to an unencrypted or publicly accessible destination, it provides an easy, secondary avenue for data theft.
*   **Applies to Capability:** `cap_ci_cd_build_pipeline` - Continuous Integration & Deployment Pipeline `[NEW]`
    *   **Reasoning:** Pipelines require deep credentials to perform deployments. If secrets injected into the pipeline are not masked or secured, they leak at rest within build logs or unencrypted artifact repositories.

### Threat: `thr_i_file_directory_exposure` - File & Directory Exposure
**Description:** Accessing raw files outside application boundaries (Directory Traversal, LFI, exposed .git).
*   **Applies to Capability:** `cap_untrusted_code_execution` - Untrusted Code Execution
    *   **Reasoning:** When users are allowed to execute custom code, that code runs within a local filesystem context. Without strict chroot jailing or sandboxing, the code can trivially traverse directories to read sensitive host files like `/etc/passwd`.

### Threat: `thr_i_metadata_error_leakage` - Metadata & Error Leakage
**Description:** Revealing system internals via stack traces, cloud metadata APIs (SSRF), or banners.
*   **Applies to Capability:** `cap_network_listener_public` - Public Network Listener
    *   **Reasoning:** Publicly bound ports are constantly scanned. They inherently leak metadata via TCP fingerprints, open port banners, and TLS certificates, revealing underlying operating systems and software versions to passive observers.
*   **Applies to Capability:** `cap_outbound_network_access` - Outbound Network Access
    *   **Reasoning:** The ability to initiate outbound connections is the required mechanism for Server-Side Request Forgery (SSRF). Attackers use this to query highly sensitive local cloud metadata APIs (e.g., `169.254.169.254`) and leak IAM instance credentials.
*   **Applies to Capability:** `cap_html_ui_rendering` - Dynamic HTML/UI Rendering
    *   **Reasoning:** If unhandled exceptions occur during rendering, the application may inadvertently print detailed stack traces or database errors into the final HTML output, leaking backend structure to the user.

### Threat: `thr_i_side_channel_leakage` - Side-Channel Leakage
**Description:** Inferring data via indirect behaviors (Timing attacks, power analysis).
*   **Applies to Capability:** `cap_data_processing_memory` - In-Memory Data Processing
    *   **Reasoning:** Computations operating on sensitive data in active memory cause minute, measurable fluctuations in execution time (timing attacks) or cache states. Attackers can analyze these fluctuations to infer the secret data being processed.

### Threat: `thr_i_data_leakage_memory` - Data Leakage in Memory / Use `[NEW]`
**Description:** Extraction of plaintext sensitive data directly from active system RAM via memory dumping, core dumps, or exploitation of buffer over-reads.
*   **Applies to Capability:** `cap_data_processing_memory` - In-Memory Data Processing
    *   **Reasoning:** Data must be decrypted to be processed by the CPU. This creates a vulnerability window where memory-safe violations (e.g., Heartbleed) or local privilege escalation can be used to dump RAM and harvest active plaintext keys or PII.

### Threat: `thr_i_unauthorized_data_exfiltration` - Unauthorized Data Exfiltration `[NEW]`
**Description:** The covert smuggling of sensitive system data out to external, attacker-controlled infrastructure.
*   **Applies to Capability:** `cap_outbound_network_access` - Outbound Network Access
    *   **Reasoning:** Permitting arbitrary outbound access provides an attacker who has achieved local execution the essential pathway to establish a Command & Control (C2) shell or smuggle stolen data out via HTTP/DNS channels.

### Threat: `thr_i_sensitive_data_logging` - Plaintext Sensitive Data Logging `[NEW]`
**Description:** The inadvertent recording of highly sensitive data (passwords, PII, API tokens, credit cards) in plaintext within application logs or telemetry streams.
*   **Applies to Capability:** `cap_audit_logging` - Audit & Event Logging
    *   **Reasoning:** The fundamental act of recording raw transaction requests or system errors inherently risks dumping sensitive memory variables to disk, effectively turning a security tool into a massive data leak if logs are not properly masked.

### Threat: `thr_d_network_volumetric` - Network Volumetric Flooding
**Description:** Overwhelming bandwidth (UDP/SYN Floods, DNS Amplification).
*   **Applies to Capability:** `cap_network_listener_public` - Public Network Listener
    *   **Reasoning:** Exposing a listening socket to the public internet inherently subjects it to uncontrolled and unfiltered ingress traffic, making it a direct target for botnets launching massive volumetric DDoS attacks.

### Threat: `thr_d_application_exhaustion` - Application Logic Exhaustion
**Description:** Targeted requests to tie up processing (Slowloris, ReDoS, expensive GraphQL).
*   **Applies to Capability:** `cap_api_provider` - API Provider (REST/GraphQL/RPC)
    *   **Reasoning:** APIs (particularly GraphQL) allow clients to specify query depth and complexity. Attackers can submit deeply nested or mathematically expensive requests that exhaust backend CPU and database connections.
*   **Applies to Capability:** `cap_user_input_processing` - User Input Processing
    *   **Reasoning:** Parsing complex user input strings via algorithms like Regular Expressions exposes the application to Algorithmic Complexity attacks, such as Regex Denial of Service (ReDoS), which ties up processing threads indefinitely.

### Threat: `thr_d_system_resource_depletion` - System Resource Depletion
**Description:** Consuming finite infra resources (Disk/Log flooding, memory leaks, connection pool exhaustion).
*   **Applies to Capability:** `cap_data_storage_persistent` - Persistent Data Storage
    *   **Reasoning:** Persistent stores rely on finite disk capacities. Attackers can spam an application with junk data designed to rapidly fill database tables or object buckets, causing a disk-full outage.
*   **Applies to Capability:** `cap_file_upload_handling` - File Upload Handling
    *   **Reasoning:** Allowing binary uploads without strict size limits or rate limiting enables attackers to launch concurrent, massive uploads that exhaust disk space or memory buffers on the hosting server.
*   **Applies to Capability:** `cap_email_sms_transmission` - Outbound Messaging (Email/SMS)
    *   **Reasoning:** An unprotected outbound messaging endpoint can be automated by attackers to spam targets, completely depleting third-party API quotas or incurring massive financial damage (SMS Toll Fraud), effectively breaking the service.
*   **Applies to Capability:** `cap_untrusted_code_execution` - Untrusted Code Execution
    *   **Reasoning:** Allowing arbitrary code execution without strict resource quotas (CPU limits, memory limits, cgroups) allows an attacker to intentionally trigger memory leaks or fork bombs that crash the host node.

### Threat: `thr_d_data_destruction` - Data Destruction & Ransomware
**Description:** Permanent loss, malicious deletion, or unauthorized encryption of data resulting in unrecoverable states and severe availability impacts.
*   **Applies to Capability:** `cap_data_storage_persistent` - Persistent Data Storage
    *   **Reasoning:** Persistent storage locations are the primary targets for ransomware. Attackers seek out these stores to encrypt or wipe the data, causing catastrophic system unavailability and extortion opportunities.
*   **Applies to Capability:** `cap_data_backup_execution` - Data Backup & Snapshotting
    *   **Reasoning:** Because backups are the primary recovery mechanism against data destruction, they become a high-priority target for adversaries. Attackers will actively seek to locate and destroy backups to ensure victims must pay the ransom.

### Threat: `thr_e_horizontal_escalation` - Horizontal Privilege Escalation
**Description:** Accessing data of peers (BOLA/IDOR, session hijacking of peers).
*   **Applies to Capability:** `cap_network_listener_internal` - Internal Network Listener
    *   **Reasoning:** Because internal networks often utilize flat topologies with minimal isolation, compromising one peer service provides the line-of-sight required to laterally attack other restricted internal listeners.
*   **Applies to Capability:** `cap_api_provider` - API Provider (REST/GraphQL/RPC)
    *   **Reasoning:** APIs inherently rely on predictable object identifiers (e.g., `GET /user/123`). This capability allows an attacker to enumerate identifiers to attempt access to data belonging to peer users (BOLA/IDOR).
*   **Applies to Capability:** `cap_authorization_enforcement` - Authorization & Access Control
    *   **Reasoning:** Flaws in how the authorization engine validates object ownership allow an attacker to successfully authenticate but access resources they do not explicitly own, causing a horizontal escalation.

### Threat: `thr_e_vertical_escalation` - Vertical Privilege Escalation
**Description:** Gaining admin/higher access via misconfigured RBAC or parameter tampering.
*   **Applies to Capability:** `cap_api_provider` - API Provider (REST/GraphQL/RPC)
    *   **Reasoning:** APIs often utilize parameter binding. If properties are not strictly filtered (Mass Assignment), a standard user can inject administrative flags (e.g., `{"is_admin": true}`) into their API requests to vertically elevate their privileges.
*   **Applies to Capability:** `cap_authorization_enforcement` - Authorization & Access Control
    *   **Reasoning:** Misconfigurations in the central access control matrices (such as default-allow rules or easily exploitable path logic) allow a low-privileged user to exploit the engine to access administrative actions.

### Threat: `thr_e_environment_breakout` - Execution Environment Breakout
**Description:** Escaping isolation boundaries (Container/VM escape, sandbox evasion).
*   **Applies to Capability:** `cap_os_command_execution` - OS Command / Shell Execution
    *   **Reasoning:** Executing commands directly on the shell provides a foothold within the operating system. Attackers can leverage this foothold to exploit kernel bugs and break out of the application's restricted daemon environment.
*   **Applies to Capability:** `cap_untrusted_code_execution` - Untrusted Code Execution
    *   **Reasoning:** Executing untrusted user code necessitates reliance on sandbox isolation. Attackers will specifically upload payloads designed to exploit vulnerabilities in the sandbox boundary (e.g., gVisor, namespaces) to escape to the host.
*   **Applies to Capability:** `cap_container_orchestration` - Container / Workload Orchestration
    *   **Reasoning:** Orchestrators run containers on shared host nodes. Over-privileged containers (e.g., `privileged` flag enabled, host-path mounts) give an attacker the direct vector needed to escape the container and compromise the entire underlying worker node.

### Threat: `thr_e_auth_bypass` - Auth Bypass
**Description:** Circumventing access controls (Forced browsing, logic flaws in SSO).
*   **Applies to Capability:** `cap_user_authentication` - Human User Authentication
    *   **Reasoning:** The workflows necessary to support human authentication (password resets, account recovery, MFA, SSO callbacks) are often highly complex. Attackers exploit logic flaws in these very capabilities to bypass the authentication check entirely.

Here is the comprehensive ontological mapping establishing the `[Capability] --(EXPOSED_TO)--> [Threat]` relationships. 

Where the existing provided lists were insufficient to fully model real-world attack surfaces, standardized, defined nodes tagged with `[NEW]` are introduced to augment the ontology.

### 1. Data Storage & Processing

### Capability: `cap_data_storage_persistent` - Persistent Data Storage
**Description:** Writes and stores data to a persistent medium (databases, object storage, block volumes).
*   **Exposed to Threat:** `thr_i_data_leakage_rest` - Data Leakage at Rest
    *   **Reasoning:** If the persistent storage mechanism relies on weak or missing encryption, attackers who gain physical access to disks or logical access to the filesystem/bucket can extract the raw sensitive data directly.
*   **Exposed to Threat:** `thr_t_data_modification` - Unauthorized Data Modification
    *   **Reasoning:** The act of persisting data inherently creates a stateful target. Attackers with unauthorized access can bypass the application logic and directly alter, corrupt, or replace the database rows or files.
*   **Exposed to Threat:** `thr_d_data_destruction` - Data Destruction & Ransomware
    *   **Reasoning:** Persistent storage is the primary target for ransomware operators looking to encrypt or wipe data to cause unrecoverable loss and business outage.
*   **Exposed to Threat:** `thr_d_system_resource_depletion` - System Resource Depletion
    *   **Reasoning:** A persistent data store relies on finite hardware storage capacities. Attackers can flood the application with junk inputs specifically designed to exhaust the available disk space, bringing the database to a halt.

### Capability: `cap_data_transit_external` - External Data Transmission
**Description:** Sends or receives data across untrusted boundaries (e.g., Public Internet).
*   **Exposed to Threat:** `thr_i_data_leakage_transit` - Data Leakage in Transit
    *   **Reasoning:** Routing traffic across external, unmanaged network infrastructure exposes the data packets to passive sniffing/eavesdropping if robust transport encryption (like TLS 1.3) is not enforced.
*   **Exposed to Threat:** `thr_t_data_modification` - Unauthorized Data Modification
    *   **Reasoning:** Transmitting over untrusted links creates the vector for Man-in-the-Middle (MITM) attacks, allowing an active adversary to intercept, modify, and forward the data mid-flight.
*   **Exposed to Threat:** `thr_s_network_spoofing` - Network & Protocol Spoofing
    *   **Reasoning:** Relying on the public internet opens the transmission path to external routing manipulation, such as BGP hijacking or external DNS spoofing, tricking the system into communicating with an attacker's server.

### Capability: `cap_data_transit_internal` - Internal Data Transmission
**Description:** Communicates over internal/private networks (e.g., within a VPC or service mesh).
*   **Exposed to Threat:** `thr_i_data_leakage_transit` - Data Leakage in Transit
    *   **Reasoning:** Internal networks are often mistakenly treated as completely trusted ("soft-center"). If mTLS or internal encryption is not used, a compromised host on the network can run a packet sniffer to capture internal API traffic.
*   **Exposed to Threat:** `thr_s_network_spoofing` - Network & Protocol Spoofing
    *   **Reasoning:** Internal network topologies relying on local resolution are highly vulnerable to Layer 2 and Layer 3 attacks like ARP spoofing or internal DNS poisoning to redirect inter-service traffic.

### Capability: `cap_data_processing_memory` - In-Memory Data Processing
**Description:** Holds sensitive data (keys, PII, tokens) in active RAM for computation.
*   **Exposed to Threat:** `thr_i_data_leakage_memory` - Data Leakage in Memory / Use `[NEW]`
    *   **Description (If NEW):** Extraction of plaintext sensitive data directly from active system RAM via memory dumping, core dumps, or exploitation of buffer over-reads.
    *   **Reasoning:** Data must be decrypted to be processed in CPU/RAM. This creates a window of vulnerability where memory-safe violations (e.g., Heartbleed) or host-level compromise allow an attacker to dump active memory and harvest keys or plaintext data.
*   **Exposed to Threat:** `thr_i_side_channel_leakage` - Side-Channel Leakage
    *   **Reasoning:** The physical processing of data in CPU registers and cache layers creates measurable variations in execution time and power consumption. Attackers can analyze these variations to infer the secret data being processed.

### Capability: `cap_secrets_management` - Secrets & Key Management
**Description:** Generates, stores, or rotates cryptographic keys, passwords, or API tokens.
*   **Exposed to Threat:** `thr_s_credential_reuse` - Credential Theft & Reuse
    *   **Reasoning:** Centralizing highly privileged secrets inherently creates a high-value target (a "crown jewel"). If the vault is compromised or an access policy is overly permissive, attackers obtain material they can instantly reuse to impersonate services.
*   **Exposed to Threat:** `thr_r_crypto_repudiation` - Cryptographic Repudiation
    *   **Reasoning:** If the key manager generates cryptographically weak keys or fails to adequately rotate them upon compromise, the cryptographic integrity of the entire system is nullified, making it impossible to prove who signed a payload.

### Capability: `cap_cryptographic_operations` - Cryptographic Operations & Hashing `[NEW]`
**Description:** Performs encryption, decryption, hashing, or digital signing of data to ensure confidentiality or integrity.
*   **Exposed to Threat:** `thr_r_crypto_repudiation` - Cryptographic Repudiation
    *   **Reasoning:** If weak algorithms (e.g., MD5, SHA-1) or hardcoded Initialization Vectors (IVs) are utilized during operations, attackers can forge digital signatures or reverse hashes, destroying the system's non-repudiation guarantees.
*   **Exposed to Threat:** `thr_t_data_modification` - Unauthorized Data Modification
    *   **Reasoning:** The improper implementation of cryptographic modes (like using ECB instead of GCM) allows an attacker to perform bit-flipping attacks, maliciously modifying ciphertext in a way that decrypts into attacker-controlled plaintext.

---

### 2. Network & Interface

### Capability: `cap_network_listener_public` - Public Network Listener
**Description:** Binds to a port accessible from the public internet.
*   **Exposed to Threat:** `thr_d_network_volumetric` - Network Volumetric Flooding
    *   **Reasoning:** Binding a socket to a public IP address inherently subjects it to uncontrolled ingress traffic, allowing botnets to easily direct TCP SYN floods or UDP reflection attacks at the open port.
*   **Exposed to Threat:** `thr_i_metadata_error_leakage` - Metadata & Error Leakage
    *   **Reasoning:** Public ports are subjected to continuous automated scanning across the internet. The port will inevitably return banners, TCP fingerprints, and TLS certificate metadata that passively leaks the underlying OS and software version.

### Capability: `cap_network_listener_internal` - Internal Network Listener
**Description:** Binds to a port accessible only from within the internal network.
*   **Exposed to Threat:** `thr_s_workload_impersonation` - Workload & Service Impersonation
    *   **Reasoning:** Internal listeners often rely on perimeter security and implicitly trust traffic originating from private IP ranges. A malicious or compromised internal container can connect to the listener and easily impersonate a trusted peer.
*   **Exposed to Threat:** `thr_e_horizontal_escalation` - Horizontal Privilege Escalation
    *   **Reasoning:** Because internal networks often lack strict tenant isolation (flat network design), compromising one minor internal service provides the network line-of-sight needed to hit administrative or restricted internal listeners laterally.

### Capability: `cap_outbound_network_access` - Outbound Network Access
**Description:** Initiates outbound connections to external internet resources.
*   **Exposed to Threat:** `thr_i_unauthorized_data_exfiltration` - Unauthorized Data Exfiltration `[NEW]`
    *   **Description (If NEW):** The covert smuggling of sensitive system data out to external, attacker-controlled infrastructure.
    *   **Reasoning:** Permitting arbitrary outbound internet access provides an attacker who has achieved local code execution the crucial pathway needed to establish a Command & Control (C2) callback shell or exfiltrate stolen databases over HTTP/DNS.
*   **Exposed to Threat:** `thr_i_metadata_error_leakage` - Metadata & Error Leakage
    *   **Reasoning:** Outbound access capabilities combined with vulnerable input processing form the mechanics of Server-Side Request Forgery (SSRF). Attackers use the outbound capacity to pivot and fetch highly sensitive local cloud metadata endpoints (e.g., 169.254.169.254).

### Capability: `cap_api_provider` - API Provider (REST/GraphQL/RPC)
**Description:** Exposes a structured, programmatic interface for clients to consume.
*   **Exposed to Threat:** `thr_d_application_exhaustion` - Application Logic Exhaustion
    *   **Reasoning:** Exposing programmatic data retrieval (especially GraphQL) allows attackers to craft deeply nested, mathematically expensive queries specifically designed to consume massive amounts of backend CPU and database connection pools.
*   **Exposed to Threat:** `thr_e_horizontal_escalation` - Horizontal Privilege Escalation
    *   **Reasoning:** APIs inherently use predictable resource identifiers (e.g., `GET /api/user/1234`). If object-level authorization is missing, an attacker can enumerate these identifiers to horizontally access data belonging to peer users (BOLA/IDOR).
*   **Exposed to Threat:** `thr_e_vertical_escalation` - Vertical Privilege Escalation
    *   **Reasoning:** APIs often group standard and administrative endpoints on the same domain. If routing rules or parameter binding logic (Mass Assignment) is flawed, a standard user can vertically escalate by injecting administrative flags into their API payloads.

---

### 3. Application Logic & I/O

### Capability: `cap_user_input_processing` - User Input Processing
**Description:** Accepts strings, JSON, XML, or form data from untrusted users and processes it.
*   **Exposed to Threat:** `thr_t_server_side_injection` - Server-Side Injection
    *   **Reasoning:** Accepting untrusted variables and concatenating them into backend syntax (SQL queries, LDAP queries, OS commands) is the fundamental mechanical cause of all server-side injection vulnerabilities. 
*   **Exposed to Threat:** `thr_t_client_side_injection` - Client-Side Injection
    *   **Reasoning:** If user input is accepted and later rendered back to other users' browsers without proper encoding/sanitization, it inherently enables Cross-Site Scripting (XSS) attacks.
*   **Exposed to Threat:** `thr_d_application_exhaustion` - Application Logic Exhaustion
    *   **Reasoning:** Parsing complex input structures (like XML or complex Regex patterns) exposes the processing engine to algorithmic complexity attacks, such as XML Entity Expansion (Billion Laughs) or Regular Expression Denial of Service (ReDoS).

### Capability: `cap_file_upload_handling` - File Upload Handling
**Description:** Allows users to upload binary files, images, or documents.
*   **Exposed to Threat:** `thr_t_server_side_injection` - Server-Side Injection
    *   **Reasoning:** If file types and contents are not strictly validated, an attacker can upload an executable web shell (e.g., `.php` or `.jsp`) which, when requested via the web server, grants arbitrary code execution.
*   **Exposed to Threat:** `thr_d_system_resource_depletion` - System Resource Depletion
    *   **Reasoning:** If file size limits and user storage quotas are not enforced during upload handling, malicious actors can script massive, concurrent file uploads specifically to exhaust disk space and crash the host.
*   **Exposed to Threat:** `thr_t_malware_distribution` - Malware Hosting & Distribution `[NEW]`
    *   **Description (If NEW):** Utilizing a legitimate application to store and serve malicious payloads, inadvertently turning the system into a malware distribution vector.
    *   **Reasoning:** By allowing binary file uploads, the application inherently risks storing files infected with ransomware or trojans. When other users (or internal admins) download these files, the application effectively acts as the distribution mechanism for the attacker.

### Capability: `cap_html_ui_rendering` - Dynamic HTML/UI Rendering
**Description:** Dynamically generates and serves HTML/JS content to web browsers.
*   **Exposed to Threat:** `thr_t_client_side_injection` - Client-Side Injection
    *   **Reasoning:** The dynamic generation of DOM elements using external variables inherently creates the attack surface for DOM-based or Reflected XSS if data bindings are not properly contextually escaped.
*   **Exposed to Threat:** `thr_i_metadata_error_leakage` - Metadata & Error Leakage
    *   **Reasoning:** During the rendering process, uncaught backend exceptions, stack traces, or developer debugging comments can be inadvertently printed to the HTML source, leaking system internals to end users inspecting the code.

### Capability: `cap_url_redirection` - URL Routing & Redirection
**Description:** Takes user input to determine where to route a request or redirect a browser.
*   **Exposed to Threat:** `thr_s_phishing_facilitation` - Phishing Facilitation via Trusted Domains `[NEW]`
    *   **Description (If NEW):** Exploiting Open Redirect vulnerabilities within an application's routing logic to generate malicious links that rely on the application's trusted domain to deceive users.
    *   **Reasoning:** Deriving a redirection destination from an unvalidated URL parameter exposes the system to Open Redirect attacks. Attackers craft links using the trusted domain (e.g., `trustedsite.com?redirect=evilsite.com`) to stealthily bounce victims to credential-harvesting phishing pages.

### Capability: `cap_email_sms_transmission` - Outbound Messaging (Email/SMS)
**Description:** Generates and sends emails or SMS messages to external users.
*   **Exposed to Threat:** `thr_s_message_spoofing` - Message & Sender Spoofing
    *   **Reasoning:** If the messaging capability dynamically builds email headers or bodies from unvalidated input (Email Header Injection), an attacker can forge the "From" address and content, leveraging the system's legitimate email server to send highly convincing phishing campaigns.
*   **Exposed to Threat:** `thr_d_system_resource_depletion` - System Resource Depletion
    *   **Reasoning:** An unprotected outbound messaging endpoint can be automated by attackers to spam targets or generate millions of SMS messages, aggressively draining third-party API quotas and incurring massive financial damage (SMS Toll Fraud).

---

### 4. Identity & Access Management

### Capability: `cap_user_authentication` - Human User Authentication
**Description:** Verifies the identity of human users via credentials or biometrics.
*   **Exposed to Threat:** `thr_s_credential_reuse` - Credential Theft & Reuse
    *   **Reasoning:** Relying on human-generated passwords inherently subjects the system to credential reuse, where passwords stolen from external breaches (or phishing campaigns) are used to seamlessly authenticate as the victim.
*   **Exposed to Threat:** `thr_e_auth_bypass` - Auth Bypass
    *   **Reasoning:** The complex state logic required for human authentication (password reset flows, MFA logic, SSO callbacks) often contains subtle logical flaws that allow an attacker to trick the system into bypassing the credential check altogether.
*   **Exposed to Threat:** `thr_s_brute_force_attacks` - Brute-Force & Credential Stuffing `[NEW]`
    *   **Description (If NEW):** Automated, systematic guessing of credentials or the mass submission of previously breached username/password pairs against an authentication endpoint.
    *   **Reasoning:** Exposing an endpoint designed to validate credentials inherently invites automated bots to rapidly test millions of username/password combinations until a valid match is found.

### Capability: `cap_machine_authentication` - Machine-to-Machine Authentication
**Description:** Verifies the identity of non-human APIs, scripts, or microservices.
*   **Exposed to Threat:** `thr_s_workload_impersonation` - Workload & Service Impersonation
    *   **Reasoning:** If M2M authentication relies on static, long-lived API keys, an attacker who extracts a single key from source code or memory can perfectly impersonate the trusted microservice in perpetuity.

### Capability: `cap_authorization_enforcement` - Authorization & Access Control
**Description:** Evaluates rules (RBAC/ABAC) to determine if an identity can access a resource.
*   **Exposed to Threat:** `thr_e_horizontal_escalation` - Horizontal Privilege Escalation
    *   **Reasoning:** Flaws in how authorization logic scopes data access to the current principal often result in scenarios where the system validates *that* the user is logged in, but fails to validate *who* owns the specific object they are requesting.
*   **Exposed to Threat:** `thr_e_vertical_escalation` - Vertical Privilege Escalation
    *   **Reasoning:** Misconfigurations in RBAC matrices (like assigning default-allow policies) allow a standard user to exploit the authorization logic to access administrative functions and elevate their system privileges.

### Capability: `cap_session_management` - Session State Management
**Description:** Issues and tracks temporary tokens (JWT, cookies) to maintain state between requests.
*   **Exposed to Threat:** `thr_s_credential_reuse` - Credential Theft & Reuse
    *   **Reasoning:** Generating session tokens introduces a post-authentication attack vector. If a token is stolen via XSS, network sniffing, or predictable generation, an attacker can perform a Token Replay attack, hijacking the user's active session without needing their password.
*   **Exposed to Threat:** `thr_r_crypto_repudiation` - Cryptographic Repudiation
    *   **Reasoning:** Stateless session management (like JWTs) relies heavily on cryptographic signatures. If weak signing algorithms or the "none" algorithm is accepted, an attacker can forge a valid session token that the backend cannot repudiate.

---

### 5. Compute & Execution

### Capability: `cap_os_command_execution` - OS Command / Shell Execution
**Description:** Application logic intentionally executes commands directly on the underlying operating system shell.
*   **Exposed to Threat:** `thr_t_server_side_injection` - Server-Side Injection
    *   **Reasoning:** Passing runtime strings into an OS system shell (e.g., `system()`, `exec()`) is highly volatile. An attacker can use shell metacharacters (like `&&` or `;`) to append and execute arbitrary malicious OS commands alongside the intended operation.
*   **Exposed to Threat:** `thr_e_environment_breakout` - Execution Environment Breakout
    *   **Reasoning:** Executing commands locally on the shell gives an application (or an attacker exploiting it) a foothold in the OS. They can leverage this foothold to exploit kernel bugs or misconfigurations to break out of the application's restricted environment into the wider host.

### Capability: `cap_untrusted_code_execution` - Untrusted Code Execution
**Description:** Allows users to submit custom code (Python, JS, etc.) to be executed by the platform.
*   **Exposed to Threat:** `thr_e_environment_breakout` - Execution Environment Breakout
    *   **Reasoning:** Allowing users to submit and run arbitrary code means the system's security relies entirely on sandbox isolation (e.g., gVisor, chroot). Attackers will intentionally upload exploits targeting the sandbox boundary or the underlying hypervisor to achieve an escape.
*   **Exposed to Threat:** `thr_d_system_resource_depletion` - System Resource Depletion
    *   **Reasoning:** Custom code can intentionally execute infinite loops, allocate massive memory arrays, or trigger fork bombs, inherently leading to a complete Denial of Service for the compute node if strict `cgroups` or quotas are absent.
*   **Exposed to Threat:** `thr_i_file_directory_exposure` - File & Directory Exposure
    *   **Reasoning:** Code running within the execution environment will actively attempt to traverse the local file system (Directory Traversal) to read sensitive local config files (e.g., `/etc/shadow`) if filesystem boundaries are not tightly jailed.

### Capability: `cap_third_party_dependencies` - Third-Party Dependency Usage
**Description:** Relies on external open-source libraries, frameworks, or packages to function.
*   **Exposed to Threat:** `thr_t_supply_chain_poisoning` - Supply Chain Poisoning
    *   **Reasoning:** Relying on external package repositories (NPM, PyPI, RubyGems) exposes the system to supply chain poisoning. Attackers can maliciously compromise an upstream package maintainer's account (or use Typosquatting), ensuring the application pulls malicious code during the build process.
*   **Exposed to Threat:** `thr_t_vulnerable_dependency_exploitation` - Exploitation of Known Vulnerabilities (CVEs) `[NEW]`
    *   **Description (If NEW):** Exploiting publicly disclosed vulnerabilities (CVEs) present in outdated or unpatched open-source libraries incorporated into the application.
    *   **Reasoning:** Importing third-party code inherently imports its technical debt. If a library contains an undiscovered or unpatched flaw (such as the Log4Shell vulnerability), attackers can exploit that flaw directly through the application's external attack surface.

### Capability: `cap_container_orchestration` - Container / Workload Orchestration
**Description:** Schedules, deploys, and manages containers across multiple host nodes.
*   **Exposed to Threat:** `thr_e_environment_breakout` - Execution Environment Breakout
    *   **Reasoning:** Orchestrators run disparate containers on shared host nodes. If a container is compromised, an attacker can exploit shared kernel vulnerabilities or excessive pod capabilities (like `privileged` mode) to escape the container boundary and take over the underlying Kubernetes node.
*   **Exposed to Threat:** `thr_t_config_manipulation` - Configuration Manipulation
    *   **Reasoning:** Complex orchestrators rely on sprawling configuration manifests (YAMLs) and RBAC roles. Attackers can manipulate these to downgrade pod security policies, alter network routing rules, or mount sensitive host directories.
*   **Exposed to Threat:** `thr_t_untrusted_image_execution` - Execution of Untrusted/Malicious Images `[NEW]`
    *   **Description (If NEW):** The pulling and execution of container images from untrusted, unverified, or compromised registries, deploying malware into the cluster.
    *   **Reasoning:** Orchestrators inherently pull base images to run workloads. If image signature verification (e.g., Notary, Sigstore) is not enforced, attackers can trick the orchestrator into deploying compromised or backdoored containers directly into the production environment.

---

### 6. Operations & Management

### Capability: `cap_audit_logging` - Audit & Event Logging
**Description:** Writes records of transactions, access, or errors to a log file or stream.
*   **Exposed to Threat:** `thr_r_insufficient_logging` - Insufficient Telemetry
    *   **Reasoning:** If the logging implementation fails to capture security-critical events (like failed authentications or authorization changes), it inherently creates a blindspot that prevents incident response teams from detecting or repudiating an attack.
*   **Exposed to Threat:** `thr_r_audit_trail_evasion` - Audit Trail Evasion
    *   **Reasoning:** Creating log files produces an evidentiary artifact. If an attacker gains sufficient privileges on the host, they will actively target these log files, altering or deleting them to cover their tracks and destroy the audit trail.
*   **Exposed to Threat:** `thr_i_sensitive_data_logging` - Plaintext Sensitive Data Logging `[NEW]`
    *   **Description (If NEW):** The inadvertent recording of highly sensitive data (passwords, PII, API tokens, credit cards) in plaintext within application logs or telemetry streams.
    *   **Reasoning:** The fundamental act of dumping transaction requests or application errors to a file inherently risks capturing sensitive memory variables, turning a secure system's logging mechanism into a massive plaintext data leak.

### Capability: `cap_config_management` - Dynamic Configuration Management
**Description:** Reads configuration settings from databases, parameter stores, or environment variables at runtime.
*   **Exposed to Threat:** `thr_t_config_manipulation` - Configuration Manipulation
    *   **Reasoning:** Reading configurations dynamically means modifying the central configuration store instantly impacts live services. Attackers can alter these stores to downgrade TLS requirements, bypass feature flags, or redirect internal APIs.
*   **Exposed to Threat:** `thr_i_data_leakage_rest` - Data Leakage at Rest
    *   **Reasoning:** Configuration systems are routinely used to handle sensitive connection strings, private keys, or API tokens. If the central parameter store lacks strict encryption at rest, these critical secrets become exposed to unauthorized personnel or attackers.

### Capability: `cap_data_backup_execution` - Data Backup & Snapshotting
**Description:** Creates asynchronous copies of data for disaster recovery purposes.
*   **Exposed to Threat:** `thr_i_data_leakage_rest` - Data Leakage at Rest
    *   **Reasoning:** Creating a backup effectively creates a duplicate of all sensitive data, often stored in different locations or cloud buckets. If backup encryption is neglected, it offers an alternative, often less-monitored avenue for attackers to steal data.
*   **Exposed to Threat:** `thr_d_data_destruction` - Data Destruction & Ransomware
    *   **Reasoning:** Because backups are a victim's primary defense against ransomware, the backup execution and storage systems inherently become a high-priority target for threat actors. They will attempt to delete or encrypt the backups first to ensure the victim cannot recover.
*   **Exposed to Threat:** `thr_t_data_modification` - Unauthorized Data Modification
    *   **Reasoning:** Attackers with access to the backup repository can stealthily tamper with snapshot data or inject persistent backdoors. This ensures that even if a victim restores their systems after an incident, the attacker's foothold is restored along with it.

### Capability: `cap_ci_cd_build_pipeline` - Continuous Integration & Deployment Pipeline `[NEW]`
**Description:** Automates the fetching of source code, building of artifacts, running of tests, and deployment to target environments.
*   **Exposed to Threat:** `thr_t_supply_chain_poisoning` - Supply Chain Poisoning
    *   **Reasoning:** Build pipelines inherently pull upstream code, third-party dependencies, and base images. Attackers targeting the CI/CD pipeline can inject malicious build steps or swap dependencies, poisoning the final artifact deployed to production (similar to the SolarWinds attack).
*   **Exposed to Threat:** `thr_t_config_manipulation` - Configuration Manipulation
    *   **Reasoning:** CI/CD functionality relies on pipeline configuration files (e.g., `.github/workflows` or `.gitlab-ci.yml`). An attacker with code-commit access can manipulate these configurations to disable security testing or alter deployment targets.
*   **Exposed to Threat:** `thr_i_data_leakage_rest` - Data Leakage at Rest
    *   **Reasoning:** Deployment pipelines require deep access and hold the "keys to the kingdom" (cloud provider credentials, database passwords, deployment SSH keys). If the pipeline's secrets manager is misconfigured, these highly privileged keys are exposed.
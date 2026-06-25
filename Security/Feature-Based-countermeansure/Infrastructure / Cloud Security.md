# **Infrastructure and Cloud Security**

 

Here is the security review questionnaire for your Infrastructure and Cloud architecture.

This questionnair might have some overlap with other features like data security, access control, network security etc. So hanlde the overlaps manually.

### Category 1: Cloud Architecture & Network Security

- **Question:** How is network segmentation implemented within the cloud environment (e.g., VPCs, Vnets, subnets) to isolate public-facing workloads from backend services and databases?
  - **Recommended Control:** Implement a strict multi-tier architecture using public and private subnets. Only load balancers, WAFs, or bastion hosts should reside in public subnets, while application servers and databases must reside in private subnets without direct inbound internet access (using NAT gateways for egress).
  - **Associated Risk:** Without proper segmentation, a single compromised web server can be used to easily pivot and launch direct attacks against sensitive internal databases or management interfaces.

- **Question:** Are ingress and egress traffic rules strictly defined using a "Default Deny" posture across all Security Groups, Network ACLs, and firewalls?
  - **Recommended Control:** Enforce strict, granular firewall rules allowing only necessary ports/protocols between specific source and destination resources. Rule sets containing `0.0.0.0/0` (allow all) for administrative ports (e.g., SSH/22, RDP/3389) must be explicitly banned.
  - **Associated Risk:** Overly permissive firewall rules expose cloud infrastructure to automated internet-wide scanning, brute-force attacks, and exploitation of known vulnerabilities.

- **Question:** What edge protection mechanisms are in place to inspect incoming traffic and protect against volumetric and application-layer attacks?
  - **Recommended Control:** Deploy a Web Application Firewall (WAF) and a dedicated DDoS mitigation service (e.g., AWS Shield, Cloudflare) at the network perimeter, configured with OWASP core rule sets and custom rate-limiting.
  - **Associated Risk:** Infrastructure can be easily overwhelmed by DDoS attacks, or web workloads can be compromised via common application exploits (like SQLi or XSS) before the traffic even reaches the application layer.

### Category 2: Cloud Identity & Access Management (IAM)

- **Question:** Are cloud administrative permissions managed at an organizational level to prevent lateral movement between disparate environments (e.g., Dev, QA, Prod)?
  - **Recommended Control:** Implement centralized cloud governance using features like AWS Organizations with Service Control Policies (SCPs) or Azure Management Groups to enforce mandatory security guardrails across all accounts/subscriptions.
  - **Associated Risk:** A compromise in a lower-tier environment (like a Sandbox) could allow an attacker to escalate privileges or access resources in the Production environment if account boundaries are not strictly isolated.

- **Question:** How are cloud workloads (e.g., VMs, containers, serverless functions) granted access to other cloud resources (e.g., storage buckets, key management services)?
  - **Recommended Control:** Use native Cloud IAM roles (e.g., AWS IAM Roles for EC2, Azure Managed Identities) instead of hardcoding or distributing long-lived static access keys. Apply the principle of least privilege to these roles.
  - **Associated Risk:** Hardcoded or static cloud credentials embedded in application code or configuration files are frequently leaked to source control repositories, leading to rapid, automated compromise of the cloud environment.

### Category 3: Data Security & Cryptography

- **Question:** How is "Encryption at Rest" enforced across all cloud storage components (e.g., block storage volumes, object storage, databases, snapshots)?
  - **Recommended Control:** Mandate encryption at rest globally using a centralized Key Management Service (e.g., AWS KMS, Azure Key Vault). Prefer Customer-Managed Keys (CMKs) with automated annual key rotation over provider-managed keys for sensitive workloads.
  - **Associated Risk:** Unencrypted data volumes or snapshots can be copied or accessed directly by unauthorized identities, or exposed if physical hardware is compromised at the data center level.

- **Question:** How does the organization prevent the accidental exposure of cloud object storage (e.g., AWS S3 buckets, Azure Blob containers)?
  - **Recommended Control:** Enable account-level features that block public access globally (e.g., AWS S3 "Block Public Access") and utilize CSPM tools to actively alert on and auto-remediate bucket policies that grant `*` (anonymous) read/write access.
  - **Associated Risk:** Misconfigured object storage is one of the leading causes of massive cloud data breaches, exposing PII, PHI, or intellectual property directly to the public internet.

- **Question:** How are cryptographic keys, TLS certificates, and other infrastructure secrets managed and rotated?
  - **Recommended Control:** Store all infrastructure secrets in an encrypted, centralized secrets manager. Implement automated lifecycle management for TLS certificates (e.g., AWS ACM) to ensure they are renewed before expiration.
  - **Associated Risk:** Mishandling secrets or allowing TLS certificates to expire leads to man-in-the-middle (MitM) attacks, intercepted traffic, or massive service outages.

### Category 4: Infrastructure as Code (IaC) & Automation

- **Question:** Is the cloud infrastructure deployed manually or via Infrastructure as Code (IaC), and how is the IaC code secured?
  - **Recommended Control:** Mandate that all infrastructure is defined via IaC (e.g., Terraform, CloudFormation). Integrate static application security testing (SAST) tools (like Checkov, tfsec, or OPA) into the CI/CD pipeline to block deployments containing security misconfigurations.
  - **Associated Risk:** Manual "ClickOps" in the cloud console leads to inconsistent security postures, human error, and undocumented vulnerabilities that are invisible to code review processes.

- **Question:** How does the organization detect and manage "Drift" (when the actual state of the cloud environment deviates from the defined IaC state)?
  - **Recommended Control:** Implement automated drift detection tools that alert security and engineering teams when out-of-band manual changes are made in the cloud console.
  - **Associated Risk:** An administrator or an attacker might manually alter a security group or disable logging in the console; without drift detection, this backdoor or misconfiguration will persist unnoticed.

### Category 5: Workload, Container, and Vulnerability Management

- **Question:** What is the process for creating, securing, and patching virtual machine images or containers (Golden Images)?
  - **Recommended Control:** Utilize an automated image building pipeline (e.g., HashiCorp Packer) to create immutable, hardened baseline images based on CIS Benchmarks. Continuously scan running workloads and container registries for CVEs.
  - **Associated Risk:** Deploying unpatched, default OS images or containers introduces known vulnerabilities that threat actors can trivially exploit for initial access or privilege escalation.

- **Question:** Are runtime security controls implemented for containerized and serverless workloads?
  - **Recommended Control:** Deploy cloud-native or third-party runtime protection platforms (e.g., Falco, Prisma Cloud) that monitor for anomalous system calls, container escapes, or execution of unauthorized binaries within the workload.
  - **Associated Risk:** Supply chain attacks or zero-day vulnerabilities in applications can lead to remote code execution (RCE). Without runtime monitoring, the attacker can operate inside the container or serverless environment without detection.

### Category 6: Logging, Monitoring, & Cloud Security Posture Management (CSPM)

- **Question:** Is cloud control plane auditing (e.g., AWS CloudTrail, Azure Activity Logs) enabled in all geographic regions, and where are these logs stored?
  - **Recommended Control:** Enable multi-region control plane logging universally. Forward all logs to a dedicated, tightly restricted security/log archive account using immutable storage (e.g., WORM compliance policies) to prevent tampering.
  - **Associated Risk:** If an attacker compromises an account, their first action is often to disable or delete logs. If logs are not shipped off-site to a locked-down account, incident responders will be completely blind to the attacker's actions.

- **Question:** Is a Cloud Security Posture Management (CSPM) solution actively monitoring the environment for compliance and misconfigurations?
  - **Recommended Control:** Deploy a CSPM tool that continuously scans the cloud control plane APIs against established frameworks (like CIS Cloud Benchmarks) and provides real-time alerting and automated remediation for high-risk findings.
  - **Associated Risk:** Cloud environments are highly dynamic. A configuration that is secure today may be made vulnerable tomorrow by a simple misconfiguration, leading to silent, long-term exposure.

### Category 7: Resilience & Disaster Recovery

- **Question:** How is backup architecture protected against modern ransomware or malicious insider deletion?
  - **Recommended Control:** Implement an air-gapped or cross-account backup strategy where backups are stored in a physically and logically isolated cloud account. Enforce strict immutability (Object Lock) so backups cannot be deleted or modified, even by a super-admin.
  - **Associated Risk:** Modern threat actors specifically target and destroy cloud backups before deploying ransomware. If backups reside in the same security boundary as the primary workload and lack immutability, the organization may face total, unrecoverable data loss.
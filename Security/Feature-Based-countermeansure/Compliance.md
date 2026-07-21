

# Compliance and governance Documentation
---

We also need to understand the compliance and governance documentation available for this vendor. 

# Security & Compliance Artifact Request List

## provide the vendor risk evaluation report conducted by S&P ? 
## SOC 2 Type II or ISO 27001 Report

* Does the vendor have any SOC 2 Type II or ISO 27001 report? If so, can you please share it?


## 3rd party pentest Report
Provide a comprehensive, independent third-party penetration test report or Letter of Attestation (LoA) completed within the last 12 months, detailing the testing scope, methodology, identified vulnerabilities, and proof of remediation for all critical and high-risk findings.

---

## RACI & Incident Accountability 

Please provide documentation and supporting evidence demonstrating how the organization’s RACI (Responsible, Accountable, Consulted, Informed) matrix is integrated with Identity and Access Management (IAM) policies for executing critical RunBook actions.

## Vulnerability Management

Please provide documentation or evidence describing the organization’s Vulnerability Management program, including how the organization continuously discovers, prioritizes (based on threat intelligence and business context), and remediates security vulnerabilities across all assets, third-party dependencies, and custom code within strictly defined Service Level Agreements (SLAs).

Also include how unpatchable exceptions are handled.

---

## Identity Threat Detection and Response (ITDR)

Please provide documentation and supporting evidence describing the organization’s identity threat detection and response capabilities across its Identity Provider (IdP) and directory services ecosystem.

This should include how the organization monitors, detects, and responds to identity-based threats such as:

* Credential abuse
* Session hijacking
* MFA bypass attempts
* Unauthorized changes to directory configurations

---

## Resilience (Backup, DR & BC)

Please provide documentation and supporting evidence describing the organization’s Backup, Disaster Recovery (DR), and Business Continuity (BC) programs, including how they are designed, implemented, protected, and regularly tested to ensure rapid restoration of critical systems and data integrity following a catastrophic outage, physical disaster, or ransomware incident.

---

## Change Management

Please provide documentation and supporting evidence describing the organization’s change management process for application, infrastructure, and configuration changes, including emergency changes.

This should include how changes are:

* Formally documented
* Security-tested
* Approved prior to production deployment

With specific emphasis on:

* Segregation of Duties (SoD) controls
* Automated rollback mechanisms

---

## Privacy & Data Protection

Please provide documentation and supporting evidence confirming whether a OneTrust assessment (e.g., Privacy Impact Assessment (PIA) or Data Protection Impact Assessment (DPIA)) has been completed, or whether the Privacy Center has been formally consulted, for the relevant system, application, or business process.

---

## Computer Operations & Operational Integration

### FSOP Integration

Please provide documentation and supporting evidence confirming whether the system is fully integrated into the Firm Standard Operations Processes (FSOP), including:

* Centralized IT Service Management (ITSM)
* Patch management workflows
* Enterprise backup and recovery schedules

---

### Security Tooling Coverage

Please provide documentation and supporting evidence confirming whether all Firm Standard Security Tools are fully deployed, active, and reporting as expected across the system’s infrastructure.

This includes, but is not limited to:

* Endpoint Detection and Response (EDR)
* Vulnerability scanning tools
* SIEM log forwarding agents
* Identity/security monitoring agents
---

## Security Policy Compliance & Hardening

Please provide documentation and supporting evidence confirming that the system and its underlying infrastructure have been hardened and audited for compliance with approved security baselines, such as:

* CIS Benchmarks
* NIST guidelines
* Vendor-specific security best practices

---




# alternative version

Could you please provide the relevant supporting documentation for the requirements outlined below to help answer each of the questions?


### Change Management

- **Question:** How do you ensure that all application and infrastructure changes (including emergency fixes) are formally documented, security-tested, and approved through a process that enforces Segregation of Duties (SoD) and includes automated rollback mechanisms prior to production deployment?
  - **Recommended Control:** Implementation of a formalized, automated Change Management process (e.g., CI/CD pipelines with mandatory security gates like SAST/DAST) that requires peer reviews, enforces strict SoD between developers and production deployment roles, logs all configuration changes as Infrastructure as Code (IaC), and maintains tested emergency "break-glass" and rollback procedures.
  - **Associated Risk:** Without rigorous, segregated, and tested change controls, the organization is highly vulnerable to the deployment of unauthorized, malicious, or insecure code, leading to prolonged system outages, embedded security blind spots, and severe compliance violations.

### Vulnerability Management

- **Question:** How does the organization continuously discover, prioritize (based on threat intelligence and business context), and remediate security vulnerabilities across all assets, third-party dependencies, and custom code within strictly defined Service Level Agreements (SLAs), and how are unpatchable exceptions handled?
  - **Recommended Control:** A comprehensive Risk-Based Vulnerability Management (RBVM) program integrating continuous infrastructure scanning, Software Composition Analysis (SCA) for supply chain risks, "shift-left" CI/CD security gates, and strict, time-bound patching SLAs backed by compensating controls (e.g., WAF rules) and executive sign-off for any formal risk exceptions.
  - **Associated Risk:** Failure to rapidly identify and patch critical vulnerabilities or properly manage third-party dependencies leaves the environment exposed to known exploits, giving automated scanners and threat actors ample opportunity to execute remote code execution, ransomware, or data exfiltration attacks.


### RACI & Incident Accountability

- **Question:** How does the RACI (Responsible, Accountable, Consulted, Informed) matrix integrate with your Identity and Access Management (IAM) policies for executing critical RunBook actions?
  - **Recommended Control:** The RACI matrix must be formally mapped to IAM roles and security groups. Only the individuals designated as "Responsible" or "Accountable" in the RACI matrix should physically possess the technical permissions (e.g., emergency break-glass accounts) required to execute the RunBook's high-impact commands.
  - **Associated Risk:** If there is a disconnect between the RACI matrix and technical permissions, unauthorized personnel could execute disruptive operational commands, or conversely, the designated incident responders might lack the necessary access during a crisis, severely delaying recovery.





### Identity Threat Detection and Response (ITDR)

- **Question:** How does the organization monitor, detect, and respond to identity-based threats—such as credential abuse, session hijacking, MFA bypass, or unauthorized changes to directory configurations—across its Identity Provider (IdP) and directory services ecosystem?
  - **Recommended Control:** Implementation of an Identity Threat Detection and Response (ITDR) solution integrated with a SIEM/SOAR to continuously analyze authentication logs and directory modifications (detecting anomalies like impossible travel, rogue admin creation, or MFA fatigue/exhaustion), enforced alongside phishing-resistant MFA (FIDO2/WebAuthn) and adaptive conditional access policies.
  - **Associated Risk:** A compromise of the identity plane allows threat actors to bypass traditional network and application perimeters, escalate privileges, and maintain silent, persistent access to critical resources while evading detection by standard infrastructure-level security controls.

---

### Resilience

- **Question:** How are system backups, disaster recovery (DR) plans, and business continuity (BC) strategies designed, protected, and regularly tested to ensure the rapid restoration of critical operations and data integrity following a catastrophic outage, physical disaster, or ransomware incident?
  - **Recommended Control:** Implementation of a robust resilience framework featuring immutable, air-gapped, and encrypted backups (aligned with the 3-2-1-1-0 backup rule), automated multi-region failover environments, and quarterly simulated disaster recovery tabletop exercises and technical dry-runs to validate defined Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO).
  - **Associated Risk:** Inadequate backup protections (such as online backups vulnerable to ransomware encryption) or untested disaster recovery procedures can result in permanent data loss, catastrophic operational downtime, and the complete inability to recover from an active security crisis.


### Change Management

- **Question:** How do you ensure that all application, infrastructure, and configuration changes (including emergency fixes) are formally documented, security-tested, and approved through a process that enforces Segregation of Duties (SoD) and includes automated rollback mechanisms prior to production deployment?
  - **Recommended Control:** Implementation of a formalized, automated Change Management process (e.g., CI/CD pipelines with mandatory security gates like SAST/DAST/SCA) that requires peer reviews, enforces strict SoD between developers and production deployment roles, logs all configuration changes as Infrastructure as Code (IaC), and maintains tested emergency "break-glass" and rollback procedures.
  - **Associated Risk:** Without rigorous, segregated, and tested change controls, the organization is highly vulnerable to the deployment of unauthorized, malicious, or insecure code, leading to prolonged system outages, embedded security blind spots, and severe compliance violations.




###  Privacy & Data Protection

- **Question:** Have you completed a OneTrust Assessment (e.g., PIA/DPIA) or otherwise formally consulted The Privacy Center regarding the collection, processing, or storage of sensitive data? (It is required whenever a system, application, or business process touches upon data privacy, regulatory compliance (like GDPR, CCPA, or HIPAA), or third-party risk)

  - **Recommended Control:** Mandatory completion and approval of a OneTrust Privacy Impact Assessment (PIA) prior to system deployment. Ensure formal sign-off from the Privacy Center to validate that data minimization, consent management, and data retention policies are correctly implemented.
  - **Associated Risk:** Deploying a system without a formal privacy review can lead to the unauthorized processing or mishandling of Personally Identifiable Information (PII) or Protected Health Information (PHI). This exposes the organization to severe regulatory penalties (e.g., GDPR, CCPA, HIPAA fines), legal liabilities, and massive reputational damage in the event of a breach.

### Computer Operations & Operational Integration

- **Question:** Is the system fully integrated into the Firm Standard Operations Processes ((FSOP) refer to the mandatory, centralized baseline of IT and security workflows that every system must integrate with to operate safely in a production environment), including centralized IT Service Management (ITSM), patch management workflows, and enterprise backup/recovery schedules?
  - **Recommended Control:** Mandate the onboarding of the system into the firm’s standard IT operations framework. This includes integrating with the corporate CMDB (Configuration Management Database), establishing automated OS and application patching schedules, and configuring regular, tested backups according to enterprise SLAs.
  - **Associated Risk:** Operating outside standard operational processes creates "Shadow IT" or orphaned infrastructure. This drastically increases the risk of systems running end-of-life (EOL) software, missing critical zero-day security patches, and suffering unrecoverable data loss during a disaster or ransomware event.

- **Question:** Are all Firm Standard Security Tools (e.g., Endpoint Detection and Response (EDR), vulnerability scanners, SIEM log forwarders, and Identity agents) fully deployed, active, and reporting healthy on this system's infrastructure?
  - **Recommended Control:** Utilize standardized, hardened base images (Golden Images) or configuration management tools (e.g., Ansible, Terraform, SCCM) to automatically deploy and lock down required enterprise security agents. Prevent network access or production deployment until the system is verified as fully instrumented by the security operations center (SOC).
  - **Associated Risk:** Deploying systems without the mandatory suite of enterprise security tools leaves critical blind spots in the environment. An attacker could exploit the system, move laterally, or exfiltrate data completely undetected because the SOC lacks visibility, telemetry, and active endpoint containment capabilities.

### Security Policy Compliance & Hardening

- **Question:** Has the system and its underlying infrastructure been hardened and audited to ensure compliance with approved CIS Benchmarks, NIST guidelines, or vendor-specific security best practices?
  - **Recommended Control:** Apply rigorous system hardening baselines (e.g., CIS Level 1 or Level 2) to all operating systems, databases, web servers, and cloud components. Implement Continuous Security Posture Management (CSPM) or automated compliance scanners to continuously monitor for configuration drift and alert on deviations from the baseline.
  - **Associated Risk:** Software and hardware often ship with default configurations designed for ease of deployment, not security (e.g., default administrative credentials, legacy protocols enabled, excessive open ports). Failure to implement industry hardening standards provides attackers with trivial, well-documented vectors for initial compromise and privilege escalation.

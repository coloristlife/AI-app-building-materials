**AWS Certificate Manager (ACM)** is a managed service designed to provision, manage, and deploy public and private Secure Sockets Layer/Transport Layer Security (SSL/TLS) certificates. It integrates seamlessly with AWS resources (such as Elastic Load Balancing, Amazon CloudFront, and API Gateway) to secure data in transit. A compromise or mismanagement of ACM can result in severe security incidents, including widespread service outages due to expired certificates, or Man-in-the-Middle (MitM) attacks if private keys are exported or trust boundaries are breached via unauthorized certificate issuance.

Here is the security review questionnaire tailored for AWS Certificate Manager (ACM) and AWS Private Certificate Authority (Private CA).

### Certificate Lifecycle and Validation

- **Question:** How is domain ownership validated for public certificates, and are the prerequisites for automated renewal maintained?
  - **Recommended Control:** Enforce DNS-based validation over Email-based validation for all public certificates, as it is fully automatable and less prone to social engineering or administrative oversight. Ensure the validation CNAME records remain intact in your DNS zones so that ACM can automatically renew the certificates 60 days prior to expiration.
  - **Associated Risk:** Relying on manual email validation or deleting DNS validation records prevents ACM's auto-renewal process. This leads to sudden certificate expiration, resulting in browser warnings, dropped client connections, and significant application outages.

- **Question:** How are externally generated, third-party certificates managed when imported into ACM?
  - **Recommended Control:** Whenever possible, use native ACM-issued certificates. If third-party certificates must be imported, implement automated monitoring for their expiration using Amazon EventBridge and AWS Config, as ACM cannot automatically renew imported certificates. Ensure the private keys are securely generated, handled, and subsequently destroyed from local workstations after import.
  - **Associated Risk:** Imported certificates that are not actively tracked for expiration will silently expire, causing service disruption. Furthermore, mishandling the private key material prior to or during the import process exposes it to compromise.

### Identity and Access Management (IAM)

- **Question:** How is access to highly sensitive ACM actions, such as issuing new certificates or deleting existing ones, restricted?
  - **Recommended Control:** Implement strict IAM policies with least privilege. Restrict `acm:RequestCertificate`, `acm:ImportCertificate`, and `acm:DeleteCertificate` to specific CI/CD pipelines or highly privileged administrative roles. Use IAM condition keys (e.g., `acm:CertificateTransparencyLoggingPreference`) to enforce security baselines.
  - **Associated Risk:** Overly permissive IAM policies allow unauthorized users to delete active certificates—causing immediate denial of service—or issue valid certificates for organizational domains, which could be attached to rogue infrastructure to facilitate phishing or data interception.

- **Question:** Is the extraction of private keys from ACM strictly prohibited or tightly controlled?
  - **Recommended Control:** Explicitly deny the `acm:ExportCertificate` action in broad IAM policies and AWS Organizations Service Control Policies (SCPs). This action is only applicable to AWS Private CA certificates, but if required, it must be restricted to break-glass or specifically authorized roles with multi-factor authentication (MFA) enforced.
  - **Associated Risk:** If an attacker or malicious insider successfully calls `ExportCertificate`, they obtain the unencrypted private key. This allows them to decrypt intercepted TLS traffic (if forward secrecy is not used) or masquerade as the legitimate service in a MitM attack.

### Private Certificate Authority (AWS Private CA)

- **Question:** If utilizing AWS Private CA, how is the logical separation and security of the Root CA and Subordinate CAs maintained?
  - **Recommended Control:** Store the Root CA offline or in a highly restricted, dedicated AWS security account with extremely limited access. Issue daily/operational certificates only from Subordinate CAs. Restrict `acm-pca:*` permissions strictly and use AWS Resource Access Manager (RAM) to securely share the Subordinate CA with workload accounts.
  - **Associated Risk:** If a Root CA is compromised due to weak IAM controls or co-location with less secure workloads, the entire organizational trust chain is broken. All certificates issued by the CA must be revoked, requiring a massive, organization-wide cryptographic reset.

- **Question:** How are compromised or retired private certificates systematically revoked, and how do clients verify their status?
  - **Recommended Control:** Enable Certificate Revocation Lists (CRLs) stored in a secured Amazon S3 bucket, and configure Online Certificate Status Protocol (OCSP) for the AWS Private CA. Ensure endpoints and client applications are configured to actively check these revocation mechanisms before establishing trust.
  - **Associated Risk:** Without functional CRLs or OCSP, there is no way to signal to clients that a previously issued private certificate has been compromised. Attackers possessing a stolen private key can continue to authenticate and operate within the network until the certificate naturally expires.

### Cryptography and Key Standards

- **Question:** Are modern, strong cryptographic algorithms selected when requesting new certificates?
  - **Recommended Control:** Standardize on strong key algorithms during certificate generation. Prefer Elliptic Curve Digital Signature Algorithm (ECDSA) (e.g., EC prime256v1 or secp384r1) for performance and security, or RSA 2048-bit minimum if legacy client compatibility is strictly required. Ensure Certificate Transparency (CT) logging is enabled for all public certificates.
  - **Associated Risk:** Utilizing weak or outdated key sizes allows well-resourced attackers to potentially factor the keys, decrypting traffic. Disabling Certificate Transparency logs prevents security teams from discovering rogue certificates issued against their domains by other public CAs.

### Logging, Auditing, and Monitoring

- **Question:** Are mechanisms in place to proactively detect and alert on impending certificate expirations?
  - **Recommended Control:** Create Amazon EventBridge rules to capture `ACM Certificate Approaching Expiration` events (triggered daily when a certificate is within 45 days of expiration) and route these alerts to an incident response system (like PagerDuty, Jira, or a SOC Slack channel) for immediate investigation.
  - **Associated Risk:** Without proactive alerting, automated renewal failures (due to DNS changes or domain registrar issues) or the expiration of imported third-party certificates will go unnoticed until a production outage occurs.

- **Question:** How are certificate lifecycle events and Private CA administrative actions audited?
  - **Recommended Control:** Ensure AWS CloudTrail is integrated with Amazon CloudWatch Logs and a centralized SIEM. Configure alerting for critical anomalies, such as repeated failed validation attempts, unauthorized `ExportCertificate` calls, or modification of AWS Private CA configurations.
  - **Associated Risk:** Lack of comprehensive auditing enables attackers to silently issue, export, or modify certificates without detection, hindering the ability to perform root cause analysis and assess the blast radius during a security breach.
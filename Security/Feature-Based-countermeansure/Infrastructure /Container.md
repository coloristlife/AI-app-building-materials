 **Container Security**

This evaluation is closely aligned with industry frameworks such as **NIST SP 800-190 (Application Container Security Guide)**, **OWASP Container Security Verification Standard**, and **ISO 27001** (A.14/A.12). The questionnaire is broken down into critical lifecycle domains: Image & Supply Chain, Build & CI/CD, Runtime Configuration, Host Infrastructure, and Orchestration/Networking.



### Category 1: Container Image & Supply Chain Security

- **Question:** How do you select, verify, and maintain the base images used for your containerized applications?
  - **Recommended Control:** Utilize minimal or "distroless" base images to reduce the attack surface. Enforce pulling images exclusively from trusted, internal registries. Implement image signing and verification (e.g., Sigstore/Cosign, Docker Content Trust) to ensure provenance.
  - **Associated Risk:** Utilizing untrusted, outdated, or bloated public images can introduce embedded malware, backdoors, or an unnecessarily large number of exploitable vulnerabilities (CVEs) into the environment.

- **Question:** How are container images assessed for vulnerabilities prior to deployment, and what are the gating mechanisms?
  - **Recommended Control:** Integrate the Wiz CLI directly into the CI/CD pipeline to automatically scan Docker images as soon as they are built. Configure and enforce a strict build failure policy (pipeline breaking) that automatically stops the build and prevents deployment if "Critical" or "High" vulnerabilities are detected by the Wiz scanner.
  - **Associated Risk:** Relying solely on asynchronous registry scanning or manual reviews means vulnerabilities are caught too late in the deployment lifecycle. Without automated pipeline blocking via tools like the Wiz CLI, developers may inadvertently push critical vulnerabilities to production, drastically widening the attack surface and violating compliance mandates.



### Category 2: Build & CI/CD Pipeline Security

- **Question:** What mechanisms are in place to prevent hardcoded secrets, tokens, or credentials from being embedded into container image layers?
  - **Recommended Control:** Use multi-stage Docker builds to keep build-time secrets out of the final image. Implement automated secret scanning (e.g., TruffleHog, Gitleaks) in the repository and pipeline. Inject sensitive configuration dynamically at runtime using secure secret managers (e.g., HashiCorp Vault, AWS Secrets Manager, Kubernetes Secrets).
  - **Associated Risk:** Anyone with access to the image registry (or anyone who pulls a leaked image) can extract the image layers, reverse-engineer the contents, and compromise sensitive databases, APIs, or infrastructure.

- **Question:** Are container images treated as strictly immutable, and how do you ensure that the application environment is not modified post-deployment?
  - **Recommended Control:** Enforce a "build-once, deploy-many" methodology. Run containers with a read-only root filesystem (`readOnlyRootFilesystem: true` in Kubernetes) and mount temporary storage (e.g., `emptyDir`) only where strictly necessary.
  - **Associated Risk:** If containers are mutable, an attacker who exploits an application vulnerability can permanently alter configuration files, drop malicious payloads, or install persistent rootkits inside the running container.



### Category 3: Runtime Security & Configuration

- **Question:** How do you prevent containers from running as the root user, and how is privilege escalation mitigated?
  - **Recommended Control:** Specify a non-root `USER` instruction in the Dockerfile. Enforce Pod Security Standards (e.g., the "Restricted" profile) to drop all Linux capabilities (`drop: ["ALL"]`), prevent privilege escalation (`allowPrivilegeEscalation: false`), and block execution as the root user (`runAsNonRoot: true`).
  - **Associated Risk:** Running as root inside a container heavily increases the likelihood of a container breakout. An attacker gaining code execution could exploit kernel vulnerabilities to escape the container and compromise the underlying host.

- **Question:** How are compute resources constrained to prevent a single container from destabilizing the host system?
  - **Recommended Control:** Explicitly define CPU and Memory `requests` and `limits` in the deployment manifests. Enforce these boundaries using resource quotas and limit ranges at the namespace level in the orchestrator.
  - **Associated Risk:** Without resource limits, a compromised or malfunctioning container (e.g., memory leak) can consume all available host resources, resulting in a Denial of Service (DoS) for all other applications running on the same node (noisy neighbor effect).

- **Question:** What mechanisms are actively monitoring for and blocking anomalous behavior or threats at runtime?
  - **Recommended Control:** Deploy kernel-level runtime security monitoring tools (e.g., Falco, Cilium Tetragon, or an enterprise CNAPP) utilizing eBPF to monitor system calls, anomalous process executions (e.g., terminal shells spawned in web containers), and unauthorized file accesses.
  - **Associated Risk:** Traditional perimeter security cannot inspect traffic inside an encrypted container overlay network. Without runtime monitoring, post-breach activities like reverse shells, lateral movement, or crypto-mining can persist completely undetected.

### Category 4: Host & Infrastructure Security

- **Question:** How is the underlying host operating system hardened and isolated from the containerized workloads?
  - **Recommended Control:** Utilize container-optimized, read-only Operating Systems (e.g., Bottlerocket, Flatcar Container Linux). Keep host kernels rigorously patched. Strictly prohibit the mounting of sensitive host directories (e.g., `/var/run/docker.sock`, `/etc`) and disable access to the host’s Network, PID, and IPC namespaces.
  - **Associated Risk:** If the host is improperly hardened or allows privileged host mounts, an attacker who compromises a container can trivially overwrite host binaries or communicate directly with the container daemon to gain full control over the node.

### Category 5: Orchestration & Network Security

- **Question:** How is network traffic segmented and restricted between different containers and services?
  - **Recommended Control:** Implement strict Network Policies enforcing a "default-deny" posture for both ingress and egress traffic, explicitly allowing only required communication. Consider adopting a Service Mesh (e.g., Istio, Linkerd) to enforce mutual TLS (mTLS) and strong identity-based authorization between microservices.
  - **Associated Risk:** A flat or overly permissive container network allows an attacker who compromises a low-priority, externally facing container to pivot laterally, scan internal networks, and attack sensitive backend services or databases.

- **Question:** How is access to the container orchestrator’s control plane and APIs authenticated, authorized, and audited?
  - **Recommended Control:** Disable anonymous authentication on the API server. Enforce strong Identity Provider integration (OIDC/SAML) combined with the principle of least privilege using Role-Based Access Control (RBAC). Ensure comprehensive API audit logging is enabled and forwarded to a central SIEM.
  - **Associated Risk:** Weak orchestrator access controls can lead to unauthorized administrative access. An attacker could deploy malicious workloads, exfiltrate all stored secrets across the cluster, or completely dismantle the production environment.










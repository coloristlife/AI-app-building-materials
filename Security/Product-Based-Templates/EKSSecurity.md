
###  Container Image Security & Vulnerability Management
**Question:** Are all container images for our workloads (EKS workers, Pods) scanned for known vulnerabilities (CVEs) before deployment, and is there a defined process to remediate or block the deployment of images that violate our security policy?
- **Associated Risk:** Exploitation of known vulnerabilities in container dependencies, leading to initial compromise of a pod.

###  Runtime Security & Workload Hardening
**Question:** Are strict container security contexts and cluster-wide Pod Security Standards enforced to ensure all workloads operate with least privilege, such as running as non-root users, having read-only root filesystems, and preventing privileged container execution?
- **Associated Risk:** Privilege escalation within a container, container escape to the host worker node, and persistent compromise of the container environment.

###  Secrets Management
**Question:** For all secrets managed natively within Kubernetes, is etcd encryption-at-rest enabled for the EKS cluster, and are Kubernetes Secrets consistently used to mount sensitive data into pods rather than using environment variables or ConfigMaps?
- **Associated Risk:** Exposure of application secrets and credentials in the event of an etcd compromise or unauthorized access to cluster backups.

###  Resource Management & DoS Prevention
**Question:** Are resource limits and requests (CPU, memory) defined and enforced for all pods to prevent resource exhaustion and ensure workload stability?
- **Associated Risk:** Denial of Service (DoS) affecting other critical workloads on the same EKS worker node.
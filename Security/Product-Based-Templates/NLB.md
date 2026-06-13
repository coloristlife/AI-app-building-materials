
## Network Load Balancer


### Network Security and Access Control

- **Question:** Are Security Groups attached directly to the Network Load Balancer, and do the inbound rules enforce the principle of least privilege?
  - **Recommended Control:** Utilize the AWS feature that allows attaching Security Groups directly to NLBs. Ensure inbound rules strictly allow traffic only from necessary source IP ranges, trusted AWS services, or specific client security groups on required ports (e.g., TCP 443), while explicitly dropping unauthorized traffic at the load balancer level.
  - **Associated Risk:** Without restrictive Security Groups on the NLB, the load balancer is exposed to the entire internet (if public) or overly broad internal networks, increasing the attack surface for port scanning, unauthorized access, and exploitation of backend services.

- **Question:** How do backend target instances ensure that ingress traffic strictly originates from the designated NLB or authorized clients?
  - **Recommended Control:** Configure backend target Security Groups to allow ingress traffic only from the NLB's Security Group. If client IP preservation is enabled, ensure backend security groups are configured to trust the specific source IP ranges of expected clients, or utilize AWS Network Firewall for deeper packet inspection.
  - **Associated Risk:** If backend targets accept traffic directly from other network segments or the internet, attackers can bypass the NLB—evading associated security monitoring, logging, and access controls—to directly compromise the application servers.

### Data in Transit and Cryptography

- **Question:** How is data in transit secured at the load balancer layer, and are modern, strong cryptographic standards enforced for TLS connections?
  - **Recommended Control:** Configure TLS listeners on the NLB (instead of cleartext TCP) and apply the most restrictive AWS predefined Security Policies (e.g., `ELBSecurityPolicy-TLS13-1-2-2021-06`). Ensure policies enforce TLS 1.2 or TLS 1.3, require Forward Secrecy (FS), disable weak ciphers, and utilize AWS Certificate Manager (ACM) for secure certificate lifecycle management.
  - **Associated Risk:** Utilizing cleartext TCP listeners or outdated TLS policies (e.g., TLS 1.0/1.1 or weak ciphers) exposes sensitive data to interception, Man-in-the-Middle (MitM) attacks, and non-compliance with regulatory frameworks (like PCI-DSS or HIPAA).

- **Question:** When backend target groups require encryption, is end-to-end encryption properly implemented and validated from the NLB to the target?
  - **Recommended Control:** Configure TLS listeners on both the NLB and the backend targets, utilizing TLS over TCP for target groups. Ensure the backend instances have valid, rotated certificates that securely authenticate the backend infrastructure to the load balancer.
  - **Associated Risk:** Terminating TLS at the NLB and forwarding traffic in cleartext over the VPC network could expose sensitive payload data to lateral movement or internal network sniffing by a compromised host within the same VPC.

### Architecture and Boundary Protection

- **Question:** Is the NLB appropriately provisioned as an internal or internet-facing resource, and is AWS PrivateLink utilized for secure cross-boundary consumption?
  - **Recommended Control:** Default to provisioning internal NLBs in private subnets. If the service must be shared across different VPCs, AWS accounts, or on-premises environments, expose the internal NLB via AWS PrivateLink (VPC Endpoint Services) rather than making the NLB internet-facing or utilizing VPC Peering.
  - **Associated Risk:** Misprovisioning an internal, sensitive service as an internet-facing NLB exposes APIs, databases, or management interfaces directly to the public web, significantly increasing the likelihood of unauthorized access and data breaches.

### Logging, Monitoring, and Threat Detection

- **Question:** Are comprehensive logging mechanisms enabled to capture connection details, TLS negotiation statuses, and flow metadata?
  - **Recommended Control:** Enable NLB TLS Access Logs and direct them to a centrally secured, immutable Amazon S3 bucket. Additionally, enable VPC Flow Logs on the subnets where the NLB nodes reside. Integrate these logs with a SIEM to monitor for repeated connection failures, outdated TLS usage, or anomalous traffic patterns.
  - **Associated Risk:** Insufficient network logging severely hampers incident response capabilities, making it difficult to investigate security incidents, perform forensic analysis on network attacks, or identify the true source IP of malicious traffic.

- **Question:** Are administrative modifications to the NLB, Listeners, or Target Groups monitored and alerted upon?
  - **Recommended Control:** Ensure AWS CloudTrail is integrated with Amazon EventBridge to trigger immediate alerts to the Security Operations Center (SOC) upon critical administrative actions, such as `DeleteLoadBalancer`, `ModifyListener`, or `DeregisterTargets`. 
  - **Associated Risk:** Without real-time alerting on control plane actions, an attacker with compromised IAM credentials could maliciously alter routing, downgrade TLS policies, or misdirect traffic to external rogue targets without detection.

### Resilience and Availability

- **Question:** How is the NLB protected against Layer 3 and Layer 4 volumetric network attacks, such as TCP SYN floods or UDP reflection attacks?
  - **Recommended Control:** While AWS provides standard DDoS protection natively, enroll internet-facing NLBs and their associated Elastic IPs into AWS Shield Advanced. This provides tailored volumetric DDoS mitigation, enhanced visibility, access to the AWS Shield Response Team (SRT), and cost protection against traffic spikes.
  - **Associated Risk:** Sophisticated or massive Layer 4 DDoS attacks could exhaust NLB connection tracking or overwhelm backend target resources, leading to connection drops, resource starvation, and a complete denial of service for legitimate users.

- **Question:** Is the NLB architected to withstand Availability Zone (AZ) failures and backend target capacity fluctuations?
  - **Recommended Control:** Deploy NLB nodes across multiple Availability Zones. Enable Cross-Zone Load Balancing to ensure traffic is distributed evenly across all healthy targets regardless of the AZ. Implement strict Target Group health checks to automatically remove unhealthy instances from the routing pool.
  - **Associated Risk:** Failing to utilize multiple AZs or cross-zone load balancing creates a single point of failure. If an AZ goes down or localized backend targets become degraded, the NLB will route traffic to unavailable targets, resulting in partial or total service outages.
Here is the fully aggregated security review questionnaire for **Network Access Restriction**. I have generalized your specific technology questions (removing references to MCP, AgentCore, AWS PrivateLink, and ENIs) to ensure they apply to any architecture, generated the corresponding controls and risks, and integrated them into the existing logical categories.

### Network Perimeter and Ingress Controls
*Focuses on defending the external boundary and strictly limiting what traffic is allowed to enter the environment.*

- **Question:** How is incoming network traffic filtered at the perimeter to ensure that only legitimate, required communication (e.g., HTTPS) reaches the application layer, and how are unexpected protocols handled?
  - **Recommended Control:** Implementation of a strict "default deny" inbound firewall policy using Next-Generation Firewalls (NGFW) or Cloud Security Groups, complemented by a Web Application Firewall (WAF) and DDoS protection to inspect and filter edge traffic.
  - **Associated Risk:** Exposure of non-essential ports (e.g., Telnet, FTP, legacy RPC) or vulnerable services directly to the internet, inviting automated scanning, exploitation, and devastating perimeter breaches.

- **Question:** Is rate limiting and traffic shaping applied at the network perimeter to mitigate potential Denial of Service (DoS) attacks targeting application gateways or APIs?
  - **Recommended Control:** Deployment of an API Gateway or Edge network security appliance configured with strict rate limiting, concurrency limits, and IP-based reputation filtering to absorb and drop abusive traffic spikes.
  - **Associated Risk:** Application gateways can be overwhelmed by volumetric or application-layer DoS attacks, leading to resource exhaustion, severe service degradation, and business-critical downtime.

### Internal Segmentation and Lateral Movement
*Focuses on isolating network segments internally (East-West traffic) to minimize the blast radius of a compromised node.*

- **Question:** Are critical application gateways and middleware components deployed within dedicated DMZs or private subnets, strictly separated from general-purpose corporate traffic and the public internet?
  - **Recommended Control:** Network architecture utilizing multi-tier subnetting (e.g., public, private, and data tiers) where core application runtimes are placed in strictly isolated private subnets with no direct route to the internet.
  - **Associated Risk:** Deploying core components in flat, shared, or publicly routable networks exposes them directly to internet-borne attacks or corporate network malware, increasing the likelihood of direct exploitation.

- **Question:** How is the internal network segmented to isolate different application tiers (e.g., presentation, business logic, database) and ensure that workloads only communicate with explicitly authorized internal systems?
  - **Recommended Control:** Adoption of microsegmentation and Zero Trust Network Architecture (ZTNA), enforcing strict internal firewall rules or security groups that allow intra-network traffic only on specific, required ports/protocols between designated workload identities.
  - **Associated Risk:** Operating a "flat network" where a compromise of a low-value, internet-facing web server allows an attacker to pivot and move laterally without restriction to highly sensitive backend databases or internal management tools.

- **Question:** Are workload-level network access controls (e.g., security groups, host-based firewalls) strictly scoped to allow outbound access *only* to the specific internal databases, microservices, or API endpoints explicitly required by that workload?
  - **Recommended Control:** Implementing least-privilege network egress rules at the host or network interface level, ensuring a workload can only communicate with its explicitly defined internal dependencies (e.g., exact IP ranges and ports).
  - **Associated Risk:** Broad internal outbound rules allow a compromised workload to scan the internal network, pivot to sensitive databases, and move laterally across internal systems that the workload has no legitimate business reason to access.

### Egress Filtering and Data Exfiltration Prevention
*Focuses on restricting outbound traffic to prevent compromised assets from calling out to attacker infrastructure.*

- **Question:** What restrictions are placed on outbound (egress) network traffic from internal servers and application workloads, and are workloads permitted to initiate connections to arbitrary internet destinations?
  - **Recommended Control:** Strict egress filtering using a default-deny outbound policy. Outbound connections should be routed through NAT gateways or forward proxies that enforce explicitly allowlisted destination IP addresses or Fully Qualified Domain Names (FQDNs).
  - **Associated Risk:** If a server is compromised via a vulnerability, unrestricted egress allows the attacker to establish persistent Command and Control (C2) callbacks, download secondary malware payloads, or silently exfiltrate massive amounts of sensitive data.

### Remote and Administrative Access Control
*Focuses on securing the network paths used by operations, development, and administrative teams.*

- **Question:** How is network access to administrative interfaces (e.g., SSH, RDP, database management ports, orchestration dashboards) restricted and protected from untrusted networks?
  - **Recommended Control:** Absolute prohibition of exposing administrative ports to the public internet. Access must be routed through secure, authenticated channels such as Bastion hosts/Jump servers, ZTNA proxies, or VPNs requiring MFA, combined with strict source-IP allowlisting.
  - **Associated Risk:** Internet-facing administrative ports are highly susceptible to brute-force attacks, credential stuffing, and zero-day exploits, routinely leading to complete infrastructure takeover by threat actors.

### Cloud-Native and PaaS Integration Security
*Focuses on securing the network transit between custom compute workloads and managed cloud services.*

- **Question:** How is network traffic routed between application workloads and managed PaaS services (e.g., managed databases, object storage buckets, message queues), and are these managed services accessible via the public internet?
  - **Recommended Control:** Utilization of Cloud Private Endpoints (e.g., AWS PrivateLink, Azure Private Endpoint, GCP Private Service Connect) to route traffic exclusively over the cloud provider's internal backbone, completely disabling public internet access to the managed service resources.
  - **Associated Risk:** Relying on public endpoints for managed cloud services allows traffic to traverse public IP spaces, exposing the data store to internet-based attacks, misconfiguration leaks (e.g., open S3 buckets), and unauthorized access bypassing the corporate network perimeter.

- **Question:** Is private connectivity utilized for communication between core runtime services and internal APIs, ensuring that internet-facing traffic is strictly dropped for internal-only components?
  - **Recommended Control:** Configuring cloud networking to use interface VPC endpoints or internal service meshes for service-to-service API calls, explicitly disabling public IP assignment, and applying rules that strictly block all inbound internet traffic to internal microservices.
  - **Associated Risk:** Routing internal API traffic over public internet boundaries exposes sensitive inter-service communication to interception, misconfiguration, and unauthorized external probing.

### Data in Transit and Cryptographic Network Security
*Focuses on protecting the confidentiality and integrity of data traversing the network.*

- **Question:** Are all network communications between internal application runtimes, gateways, and external servers or integrations strictly enforced over strong encryption protocols (e.g., TLS 1.2 or higher)?
  - **Recommended Control:** Disabling plaintext protocols (e.g., HTTP) internally and enforcing mutual TLS (mTLS) or strong TLS 1.2+ ciphers for all intra-component and external communication paths, terminating TLS as close to the application as possible.
  - **Associated Risk:** Unencrypted network traffic can be intercepted via packet sniffing or man-in-the-middle (MitM) attacks, leading to the compromise of sensitive data, session tokens, and internal operational secrets traversing the network.



### Cross-Boundary & Network Security (System-to-System/Cross-BU)

- **Question:** How is network traffic isolated, routed, and secured when systems from different Business Units (BUs) or distinct trust domains need to communicate and share data?
  - **Recommended Control:** Traffic must not traverse the public internet. Utilize cloud-native private backbone routing (e.g., AWS PrivateLink, Azure Private Link) or encrypted Site-to-Site VPNs (IPsec) to connect the BUs. Furthermore, enforce zero-trust principles at the boundary: require Mutual TLS (mTLS) for system-to-system authentication and implement strict Network Access Control Lists (NACLs) or Security Groups to restrict traffic explicitly to required ports and IP addresses.
  - **Associated Risk:** Treating all internal corporate networks as "trusted" is a major architectural flaw. If cross-BU traffic is routed over public channels, it is vulnerable to interception. If routed over a flat internal network without Private Link/VPN isolation, an attacker who compromises a low-security BU (e.g., Marketing) can easily pivot laterally into a high-security BU (e.g., Finance or Engineering) and exfiltrate sensitive data.
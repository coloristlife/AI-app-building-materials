

## MCP gateway uses native AWS IAM to call target resources directly.  No token exchange round-trip.

Understanding this statement requires looking at how authentication is handled on the **backend (downstream) leg** of the request. 

This statement describes how the Gateway authenticates the *outgoing* request when it forwards traffic to the backend business-line MCP servers or target resources.

Here is the breakdown of what exactly this statement means, why it’s structurally different from traditional API Gateways, and what it means for your security posture.

---

### 1. The "Old Way": The Token Exchange Round-Trip
To understand the statement, you first have to understand what it is avoiding. In a traditional microservices architecture, a Gateway often performs an **OAuth 2.0 Token Exchange (RFC 8693)**:

1.  **Ingress:** The AI Agent sends an external Okta JWT to the Gateway.
2.  **The Round-Trip:** The backend servers don't trust the external Okta token. So, the Gateway must make an API call to an internal Identity Provider (IdP) to say: *"Here is an external Okta token for Alice. Please give me an internal system token representing Alice."*
3.  **Egress:** The Gateway takes this *new* internal token and sends it to the backend server.
4.  **Validation:** The backend server must then validate this internal token before executing the tool.

**The Problem:** This requires maintaining internal token infrastructure, adds latency (the "round-trip"), and creates internal tokens that can potentially be stolen or replayed.

### 2. The "AWS Way": Native IAM & SigV4
The statement *"AWS agentCore Gateway uses native AWS IAM to call target resources directly"* means the Gateway completely bypasses the need for internal JWTs or tokens.

Instead, it uses **AWS Signature Version 4 (SigV4)**.

1.  **Ingress:** The AI Agent sends the request to the Gateway. The Gateway authenticates the user.
2.  **Egress (No Round Trip):** Because the Gateway and the backend resources (e.g., an AWS Lambda function, Amazon Bedrock, or internal API Gateway) both live inside AWS, the Gateway uses native AWS credentials (IAM) to cryptographically sign the HTTP request payload. 
3.  **Validation:** The target resource receives the request. The AWS hypervisor/fabric intrinsically verifies the SigV4 signature against AWS IAM policies before the request even reaches the application code.

### 3. Security Advantages of Native AWS IAM
This is a highly secure, performant architectural choice. As a security reviewer, you should view this favorably for several reasons:

*   **Zero Token Theft / No Replay Attacks:** Unlike a JWT (which can be stolen and reused until it expires), an AWS SigV4 signature is mathematically tied to the specific HTTP request, headers, and payload, and it expires within minutes. If an attacker intercepts the backend request, they cannot replay it.
*   **Reduced Attack Surface:** There is no internal token exchange service to compromise or maintain. 
*   **Centralized Authorization (IAM):** You don't need to write custom token validation code in your backend MCP servers. AWS IAM handles the "allow/deny" decision at the infrastructure layer using Resource-Based Policies or Identity-Based Policies.

### 4. The "Catch" (What you MUST review)
While this eliminates the token exchange, it introduces a massive new security question you must ask the engineering team: **How is Identity Propagation handled?**

If the Gateway uses native AWS IAM to call the backend, **whose IAM permissions is it using?**

*   **The Bad Pattern (Monolithic Role):** If the Gateway uses a single, highly privileged IAM Role (e.g., `GatewayExecutionRole`) to call all backend servers for all users, you have lost fine-grained authorization. The backend only sees the Gateway calling it, not the actual user. This violates Least Privilege.
*   **The Secure Pattern (Dynamic AssumeRole or ABAC):** To do this securely, the Gateway must take the claims from the Okta JWT and dynamically map them to AWS IAM. 
    *   Does the Gateway perform `sts:AssumeRole` to assume a specific IAM role dedicated to that tenant before calling the backend?
    *   Or, does the Gateway use **AWS IAM Session Tags** (Attribute-Based Access Control - ABAC) to pass the `tenant_id` and `user_role` natively through IAM to the target resource?

### Summary for your review:
When you see the statement *"No token exchange round-trip, uses native IAM"*, you can acknowledge that this provides **lower latency** and **stronger cryptographic transport security (SigV4)**. 

However, your immediate follow-up question as a Security Architect must be:
> *"Since we are dropping the Okta JWT at the Gateway and switching to native AWS IAM for the backend call, how does the Gateway propagate the external user's identity and tenant context into the AWS IAM context to ensure the backend resource enforces fine-grained, tenant-isolated access controls?"*



## Token Validation

How does the MCP Gateway validate Okta JWTs? Does it strictly verify the iss (issuer), aud (audience), exp (expiration), and signature using cached JWKS (JSON Web Key Sets)?


**Why the Gateway MUST Validate the Token**

In a multi-tenant gateway pattern, the gateway's primary job is to route traffic based on the identity of the client (e.g., routing Tenant A's AI agent to Tenant A's federated MCP server).
To do this, the gateway must read the Okta JWT to extract the tenant_id or client_id claims. 

Cryptographic rule: You cannot read and act upon claims in a JWT without first verifying the signature, issuer (iss), expiration (exp), and audience (aud).

If the gateway skips validation and simply proxies the request downstream:
Spoofing & Cross-Tenant DoS: An attacker could send a fake JWT claiming to be "Tenant A". The gateway would blindly route it to Tenant A's backend server. Even if the backend server rejects it, Tenant A's infrastructure is now absorbing a Denial of Service (DoS) attack from unauthenticated traffic.

Violates Edge Protection: The Gateway acts as your network's front door. Allowing unauthenticated traffic to traverse past the DMZ into internal backend networks violates the principle of perimeter defense.


**The Role of the Downstream Server (Zero Trust)**

While the Gateway handles Edge Authentication and Coarse-Grained Authorization (e.g., "Does this token have the mcp:access scope?"), the downstream business-line MCP server still has a critical security role.
You should implement the Token Propagation or Token Exchange pattern:
Gateway Validates: Gateway strictly verifies the Okta JWT via cached JWKS.
Gateway Forwards Context: The Gateway forwards the validated token (or ideally, swaps it for a short-lived internal token) to the downstream MCP server.
Backend Authorizes: The backend MCP server verifies the token (Zero Trust) and performs Fine-Grained Authorization (e.g., "Does this specific user have permission to query the payroll database via this MCP tool?").



### Token Revocation & Lifespan: 
What is the lifespan of the access tokens? How does the Gateway handle Okta token revocation events or user session termination in near real-time (e.g., Continuous Access Evaluation, Okta Event Hooks)?

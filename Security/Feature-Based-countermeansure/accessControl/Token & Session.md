

## Token & Session Management

**Countermeasure Probe:** If delegated tokens are persisted, what encryption mechanisms (e.g., HSMs, KMS-backed encryption at rest) are used to protect the token store, and what are the enforced session lifecycle policies (e.g., absolute token expiration times, refresh token rotation, and mandatory re-authentication/re-authorization intervals)?

- **Associated Risk:** Credential Theft and Persistent Impersonation. If OAuth tokens are stored insecurely (e.g., plaintext in a database), a compromise of the token store allows an attacker to impersonate users across all connected downstream systems. Furthermore, if the system relies on infinite or excessively long-lived refresh tokens without enforcing periodic re-authentication, a stolen token grants an attacker a persistent backdoor that may survive user password changes or local endpoint remediation.



## Token Validation


- **Question:** When processing authorization via tokens (e.g., JWTs), does the backend cryptographically verify the signature, issuer, audience, and expiration before trusting the embedded authorization scopes/claims?
  - **Recommended Control:** Use established, secure libraries to validate JWTs. Enforce strict checks on the `alg` header (preventing 'None' algorithm attacks or symmetric/asymmetric confusion), and validate the `exp`, `iss`, and `aud` claims. 
  - **Associated Risk:** Attackers may craft forged tokens, alter their permissions (e.g., changing `"role": "user"` to `"role": "admin"`), or replay expired tokens to gain unauthorized access to the system.

- **Question:** Are authorization scopes and claims securely mapped to backend actions, and do you avoid trusting user-supplied parameters to dictate privilege?
  - **Recommended Control:** Derive the user's role and scopes solely from the cryptographically signed, server-issued token. Never trust parameters like `?isAdmin=true` or POST body fields that dictate role assignment during resource creation/modification.
  - **Associated Risk:** Mass Assignment or Parameter Tampering vulnerabilities where an attacker manipulates API requests to elevate their privileges horizontally or vertically.


### In the case of MCP (Model Context Protocol) Gateway (or any API/Microservices gateway routing these requests)


How does the MCP Gateway validate Okta JWTs? Does it strictly verify the iss (issuer), aud (audience), exp (expiration), and signature using cached JWKS (JSON Web Key Sets)?


To map this specific security use case into a Security Architecture Review (SAR) questionnaire for an **MCP (Model Context Protocol) Gateway** (or any API/Microservices gateway routing these requests), the questions must investigate how the gateway handles ingress validation, token exchange, and downstream routing in the presence of this known `aud` claim limitation. 

Here are the targeted security review questions grouped by architectural function:

#### 1. Ingress & Initial Token Validation
*Since the gateway is the entry point receiving the initial token, we need to know how it treats incoming requests before any exchange happens.*
* **Q1:** When the MCP Gateway receives an incoming request, how does it validate the initial JWT? (e.g., signature verification, expiration, issuer check).
* **Q2:** Given the Okta limitations with the `aud` (audience) claim, does the Gateway rely solely on the token's signature, or does it enforce alternative validation checks (such as specific OAuth scopes, custom claims, or group memberships) before accepting the request?
* **Q3:** How does the MCP Gateway map the identity from the incoming token to the specific requested operation or downstream MCP server/tool? 

#### 2. OBO (On-Behalf-Of) Token Exchange & Agentcore Integration
*These questions investigate the gateway's interaction with the Agentcore Identity provider to mint the new OBO token.*
* **Q4:** Does the MCP Gateway initiate the OBO token exchange via Agentcore itself, or does it expect the client/calling service to have already performed the exchange? 
* **Q5:** If the Gateway performs the exchange, how does it authenticate *itself* to Agentcore/Okta to prove it is allowed to request an OBO token for the target user?
* **Q6:** Does the MCP Gateway cache the resulting OBO tokens? If so, how is the cache keyed (e.g., User ID + Target Service) to ensure a token exchanged for Service A is not accidentally retrieved and used for Service B?

#### 3. Compensating Controls for the `aud` Claim Gap (Routing & Confused Deputy)
*This is the core of the risk. Since the OBO tokens lack precise audience restrictions, the gateway must act as the enforcer.*
* **Q7:** How does the MCP Gateway protect against "Confused Deputy" attacks? Specifically, if a user provides a valid token but asks the gateway to route the request to a backend service they shouldn't have access to, how does the gateway block this?
* **Q8:** Until Okta's multi-audience support is released, what specific compensating control is configured at the Gateway's routing layer? (e.g., Is there a strict mapping of `scp` (scope) claims to allowed routing endpoints?)
* **Q9:** If a downstream service receives an OBO token from the MCP Gateway, how does that downstream service know the request legitimately came from the Gateway and wasn't replayed by a malicious insider? (e.g., Is the Gateway enforcing mTLS to all downstream servers?)

#### 4. Downstream Communication & Auditing
*These questions ensure that even with the flaw, the impact is monitored and contained.*
* **Q10:** When the MCP Gateway forwards the request and OBO token to the downstream service, does it strip or inject any custom HTTP headers (like a Gateway-verified correlation ID or `X-Forwarded-For`) to establish a trusted chain of custody?
* **Q11:** Are network segmentation policies (e.g., Kubernetes NetworkPolicies, AWS Security Groups) in place so that backend services will *only* accept traffic from the MCP Gateway, thereby mitigating the risk of direct token replay from other parts of the network?
* **Q12:** Does the MCP Gateway log the token claims (e.g., subject, scopes, missing audience, target route) for security telemetry without logging the sensitive token signature itself? 

**How to use this in a Security Review:**
You would present these questions to the engineering team building or configuring the MCP Gateway. If they answer "We just pass the token through and let the backend handle it," you know you have a high-risk finding because the backend currently *can't* handle it securely due to the Okta `aud` limitation. The expected secure answer is that the Gateway enforces strict scope-to-route mapping and mTLS to compensate for the missing audience claim.


If you were writing a formal security assessment or threat model report for this architecture, here is how you would document the security control, risk, risk level, and recommendations.

---

### 1. Security Control
* **Control Category:** Identity and Access Management (IAM) / API Security 
* **Specific Control:** **OAuth 2.0 / JWT Token Validation (Audience Restriction)**
* **Standard Reference (Example):** 
  * **OWASP ASVS (v4.0):** Control V3.3.3 - *"Verify that the application verifies the audience (`aud`) of the token..."*
  * **NIST CSF 2.0:** PR.AA-05 (Access permissions, entitlements, and authorizations are managed and enforced).
* **Control Objective:** Ensure that digital tokens are only accepted by the specific software services they were intended for, enforcing the principle of least privilege and preventing token misuse.

### 2. Security Risk
* **Risk Title:** Unauthorized Token Reuse / Confused Deputy via Incomplete Audience (`aud`) Validation
* **Risk Description:** 
  The architecture relies on an On-Behalf-Of (OBO) token exchange pattern, but the authorization server (Okta) currently issues tokens that lack fully compliant, multi-audience (`aud`) claims. 
  
  Because downstream services cannot strictly validate that the token was minted *specifically for them*, the system is vulnerable to a **token forwarding** or **Confused Deputy** attack. If an intermediate service is compromised (or acts maliciously), it could take a token originally meant for itself and replay that token against a different downstream service. Because the downstream service is not strictly enforcing the `aud` claim, it will accept the token and execute the request on behalf of the user, leading to unauthorized data access or manipulation.

### 3. Risk Level: HIGH (or Medium-High)
* **Impact: HIGH.** If exploited, an attacker who compromises one service gains the ability to impersonate the user across other backend services, potentially accessing sensitive data or executing unauthorized actions across different Business Units (BUs).
* **Likelihood: MEDIUM.** Exploiting this requires an attacker to first compromise an internal service or intercept a token in transit. However, because the architectural gap is known and structurally present across the environment, the barrier to lateral movement is significantly lowered.
* **Overall Rating: HIGH.** (Note: This could be downgraded to *Medium* if there are compensating controls in place, such as strict network segmentation or mTLS between the microservices).

### 4. Recommendations for Remediation

To address this during the architecture review, recommendations should be split into tactical (short-term) and strategic (long-term) actions.

**Strategic / Long-Term Remediation (The Ultimate Fix):**
* **Implement Multi-Audience Validation:** Track the vendor (Okta) roadmap for the release of multi-audience support. Once released, mandate an update to the "Agentcore" libraries. All downstream services must be updated to strictly validate the `aud` claim and explicitly reject any JWT where their specific service identifier is missing from the audience list.

**Tactical / Short-Term Remediation (Compensating Controls):**
Since the Okta feature is pending, the following compensating controls must be implemented to reduce the risk in the interim:
* **Scope-Based Authorization (`scp` claim):** Instead of relying solely on the audience claim, ensure that tokens use highly granular OAuth **scopes**. Service B should verify that the token contains a specific scope (e.g., `ServiceB.Read`) rather than just a generic user identity. Service A should only be granted scopes for exactly what it needs.
* **Custom Claims:** Configure Okta to inject a custom claim (e.g., `custom_allowed_services: ["ServiceA", "ServiceB"]`) into the JWT. Update the Agentcore validation logic to check this custom claim as a temporary substitute for the standard `aud` claim.
* **Network-Level Mutual TLS (mTLS):** Enforce mTLS between microservices. Even if a token can technically be accepted by any service, mTLS ensures that Service B will only accept network connections originating from the IP/Certificate of explicitly authorized callers (like Service A), preventing arbitrary token replay from unauthorized network locations.

## Token Revocation & Lifespan: 
What is the lifespan of the access tokens? How does the Gateway handle Okta token revocation events or user session termination in near real-time (e.g., Continuous Access Evaluation, Okta Event Hooks)?



   
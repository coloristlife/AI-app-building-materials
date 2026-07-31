This use case is for platform e.g. MCP gateway, which handle the token exchange to preserve user context and issues a new token with audience used to aim at the different downstream MCP servers.

This is a classic **Token Exchange Pattern (RFC 8693)** or **Security Token Service (STS) Pattern**. This is a highly robust architectural choice for an MCP Gateway, as it enforces Zero Trust on the backend while explicitly preventing token replay across different business-line servers via strict `aud` (audience) targeting.

However, from a security architecture perspective, **this design turns your Gateway into an Identity Provider (IdP) / Token Minter.** This dramatically shifts the threat model. If an attacker compromises the Gateway's token exchange mechanism, they can mint forged tokens for *any* downstream server, for *any* user.

Here is the final, comprehensive Security Architecture Questionnaire for an MCP Gateway utilizing a **Token Exchange Pattern**. 

This version is designed to accommodate *both* architectures (Gateway as the Minter OR Gateway as an Okta Proxy) and includes the **✅ Preferred / Expected Answers** to act as your grading rubric during the review.

---

### **Section 1: Ingress Authentication & Token Exchange Architecture**
*This section determines how the Gateway safely initiates the token exchange without exposing itself or the platform to compromise.*

**1.1. Pre-Exchange Edge Validation:**
*   **Question:** Does the Gateway validate the incoming external Okta JWT locally *before* attempting any token exchange, or does it rely entirely on the token exchange mechanism (Okta or Internal STS) to reject invalid tokens?
*   **✅ Preferred Answer:** The Gateway locally caches the external Okta JWKS and verifies the signature, `exp`, and `iss` in memory. It *immediately* drops invalid tokens (HTTP 401). **(Crucial: Relying on the backend or Okta to drop bad tokens creates a severe Cross-Tenant DoS and rate-limiting vulnerability).**

**1.2. The Token Exchange Mechanism (Identify the Pattern):**
*   **Question:** Which mechanism is used for the Token Exchange?
    *   **Path A:** Gateway as the Minter (Gateway signs the new downstream token itself).
    *   **Path B:** Gateway as a Proxy to Okta (Okta mints the downstream token via RFC 8693).

*(Evaluate the applicable path below):*

*   **If Path A (Gateway Minter): Key Storage & Cryptography:**
    *   *Question:* Where is the private signing key stored, how is it rotated, and what cryptographic signing algorithm is used?
    *   *✅ Preferred Answer:* Keys are stored in a managed KMS (AWS KMS, HashiCorp Vault) or HSM. Keys are never hardcoded in memory/environment variables. Rotation is automated (e.g., every 30 days). The algorithm is strong asymmetric (e.g., `RS256` or `ES256`). The Gateway exposes an internal JWKS endpoint for backends to fetch public keys.
*   **If Path B (Okta Proxy): Client Authentication to Okta:**
    *   *Question:* When the Gateway calls the Okta Token Exchange API, how does it securely authenticate itself as a trusted client?
    *   *✅ Preferred Answer:* The Gateway uses Private Key JWT (asymmetric) or mTLS to authenticate to Okta. (Basic Auth / static client secrets are acceptable but less ideal for high-security AI gateways).  
    Note: In the context of OAuth 2.0 and Okta, Private Key JWT (officially known as private_key_jwt in OAuth/OIDC specifications) is a highly secure method for a machine (like your Gateway) to prove its identity to an authorization server (Okta) without using a password or shared secret.

---

### **Section 2: Context Preservation & Privilege Down-Scoping**
*The most common token exchange vulnerability is inadvertently granting the new token MORE privileges than the original token possessed.*

**2.1. Claims Mapping & Tenant Preservation:**
*   **Question:** Provide the mapping logic (Gateway code or Okta Custom Authorization Server policy) that translates the incoming token to the downstream token. How do you ensure `tenant_id` and `sub` (user ID) are immutably preserved?
*   **✅ Preferred Answer:** The policy explicitly maps the `tenant_id` and user identity 1:1. The downstream backend relies *only* on this cryptographically signed claim for tenant routing, never on spoofable HTTP headers like `X-Tenant-ID`.

**2.2. Privilege Down-Scoping:**
*   **Question:** Does the exchange process support "down-scoping"? If an AI Agent token has global read/write scopes, but it is routed to a read-only MCP server, are the scopes reduced in the new token?
*   **✅ Preferred Answer:** Yes. The Gateway (or Okta policy) explicitly requests only the `scp` (scopes) strictly necessary for the targeted downstream server (Principle of Least Privilege).

**2.3. Dynamic Audience (`aud`) Targeting:**
*   **Question:** How is the `aud` claim determined for the newly minted token to prevent token replay attacks across backend servers?
*   **✅ Preferred Answer:** The Gateway dynamically sets the target `aud` (e.g., `aud: mcp-server-finance`) based on strict internal routing tables matched to the user's intent. It is *never* determined by an unvalidated parameter passed by the external AI agent.

---

### **Section 3: Downstream Validation (Zero Trust Enforcement)**
*The backend business-line MCP servers must not blindly trust traffic just because it traversed the Gateway.*

**3.1. Strict Token Verification:**
*   **Question:** Do the downstream business-line MCP servers independently validate the exchanged token?
*   **✅ Preferred Answer:** Yes. Downstream servers pull the JWKS (from the Gateway or Okta), verify the signature locally, and strictly assert that the `aud` perfectly matches their own identifier. They immediately drop `aud` mismatches to prevent cross-service token replay.

**3.2. Network Segmentation:**
*   **Question:** Even with token validation, are the downstream MCP servers network-isolated?
*   **✅ Preferred Answer:** Downstream servers operate in a private subnet (VPC) and enforce Security Groups or mTLS, meaning they physically drop any TCP connection that does not originate from the Gateway's internal IP space.

---

### **Section 4: Token Lifespan, Expiration, and Revocation**
*Because exchanged tokens are newly minted, their lifecycles are decoupled from the original external Okta session.*

**4.1. Micro-Lifespans:**
*   **Question:** What is the Time-To-Live (TTL / `exp`) of the newly exchanged downstream token?
*   **✅ Preferred Answer:** **1 to 5 minutes maximum.** Because the token is used instantly for a backend routing hop, it does not need a long lifespan. A short TTL is the primary defense against stolen internal tokens.

**4.2. Revocation Propagation (Session Binding):**
*   **Question:** If the original Okta session is revoked by an administrator *while* a long-running downstream MCP tool is executing, how is that termination propagated?
*   **✅ Preferred Answer:** The platform utilizes Continuous Access Evaluation (CAEP) / Okta Event Hooks. The Gateway receives the revocation webhook and forcefully severs the connection to the backend server. (Acceptable alternative: The platform relies strictly on the 1-minute TTL to naturally kill the execution shortly after).

---

### **Section 5: AI-Agent / MCP Specific Constraints & Observability**
*AI agents operate autonomously and at machine speed, requiring specialized tracking.*

**5.1. AI Agent Identity Preservation:**
*   **Question:** Does the newly exchanged token retain context about *which* specific AI Agent (e.g., `client_id: claude_v3`) initiated the request?
*   **✅ Preferred Answer:** Yes. The exchanged token contains an AI client identifier claim. This allows the backend MCP server to enforce policies like "Claude can read the database, but only internal scripts can write to it."

**5.2. Token Logging and Egress Leakage:**
*   **Question:** How do you ensure the newly exchanged JWTs are not leaked in infrastructure logs or error messages?
*   **✅ Preferred Answer:** APM tools (Datadog, Splunk), WAFs, and Gateway routing logs are explicitly configured to mask the `Authorization: Bearer <token>` header. Furthermore, if the backend returns an HTTP 401/403, the Gateway sanitizes the error response before sending it back to the AI Agent so internal token structures are not leaked to external LLM providers.

### **Section 6: User-Level Access Control & Identity Propagation**
**6.1 Identity Propagation (The "Confused Deputy" Defense)**  
 *   **Question:** During the token exchange, how is the original human user's identity propagated to the downstream token? Does the newly minted token contain the original user's identifier (e.g., the sub claim or email), or does the backend MCP server only see the identity of the Gateway/AI Agent (e.g., client_credentials flow)?

 *   ✅ Preferred Answer: The token exchange utilizes the OAuth 2.0 Token Exchange (urn:ietf:params:oauth:grant-type:token-exchange) "On-Behalf-Of" or "Delegation" semantics. The original user's sub (Subject) claim is immutably stamped into the downstream token. The backend knows exactly which human triggered the AI. (Red Flag: If the token exchange uses Client Credentials and drops the user ID, it is a critical Confused Deputy vulnerability).
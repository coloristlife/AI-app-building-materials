

### Token & Session Management

**Countermeasure Probe:** If delegated tokens are persisted, what encryption mechanisms (e.g., HSMs, KMS-backed encryption at rest) are used to protect the token store, and what are the enforced session lifecycle policies (e.g., absolute token expiration times, refresh token rotation, and mandatory re-authentication/re-authorization intervals)?

- **Associated Risk:** Credential Theft and Persistent Impersonation. If OAuth tokens are stored insecurely (e.g., plaintext in a database), a compromise of the token store allows an attacker to impersonate users across all connected downstream systems. Furthermore, if the system relies on infinite or excessively long-lived refresh tokens without enforcing periodic re-authentication, a stolen token grants an attacker a persistent backdoor that may survive user password changes or local endpoint remediation.



### Token Validation


- **Question:** When processing authorization via tokens (e.g., JWTs), does the backend cryptographically verify the signature, issuer, audience, and expiration before trusting the embedded authorization scopes/claims?
  - **Recommended Control:** Use established, secure libraries to validate JWTs. Enforce strict checks on the `alg` header (preventing 'None' algorithm attacks or symmetric/asymmetric confusion), and validate the `exp`, `iss`, and `aud` claims. 
  - **Associated Risk:** Attackers may craft forged tokens, alter their permissions (e.g., changing `"role": "user"` to `"role": "admin"`), or replay expired tokens to gain unauthorized access to the system.

- **Question:** Are authorization scopes and claims securely mapped to backend actions, and do you avoid trusting user-supplied parameters to dictate privilege?
  - **Recommended Control:** Derive the user's role and scopes solely from the cryptographically signed, server-issued token. Never trust parameters like `?isAdmin=true` or POST body fields that dictate role assignment during resource creation/modification.
  - **Associated Risk:** Mass Assignment or Parameter Tampering vulnerabilities where an attacker manipulates API requests to elevate their privileges horizontally or vertically.





How does the MCP Gateway validate Okta JWTs? Does it strictly verify the iss (issuer), aud (audience), exp (expiration), and signature using cached JWKS (JSON Web Key Sets)?


### Token Revocation & Lifespan: 
What is the lifespan of the access tokens? How does the Gateway handle Okta token revocation events or user session termination in near real-time (e.g., Continuous Access Evaluation, Okta Event Hooks)?



   
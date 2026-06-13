

### Token & Session Management

**Countermeasure Probe:** If delegated tokens are persisted, what encryption mechanisms (e.g., HSMs, KMS-backed encryption at rest) are used to protect the token store, and what are the enforced session lifecycle policies (e.g., absolute token expiration times, refresh token rotation, and mandatory re-authentication/re-authorization intervals)?

- **Associated Risk:** Credential Theft and Persistent Impersonation. If OAuth tokens are stored insecurely (e.g., plaintext in a database), a compromise of the token store allows an attacker to impersonate users across all connected downstream systems. Furthermore, if the system relies on infinite or excessively long-lived refresh tokens without enforcing periodic re-authentication, a stolen token grants an attacker a persistent backdoor that may survive user password changes or local endpoint remediation.



### Token Validation

How does the MCP Gateway validate Okta JWTs? Does it strictly verify the iss (issuer), aud (audience), exp (expiration), and signature using cached JWKS (JSON Web Key Sets)?


### Token Revocation & Lifespan: 
What is the lifespan of the access tokens? How does the Gateway handle Okta token revocation events or user session termination in near real-time (e.g., Continuous Access Evaluation, Okta Event Hooks)?



   
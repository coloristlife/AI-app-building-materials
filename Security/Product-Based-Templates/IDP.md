###  Identity & Access Management (IAM)
**Question**: Is authorization centrally defined and consistently enforced using least privilege (RBAC/ABAC), with separation of duties for admin roles and explicit scoping of what identities/apps can request which tokens/claims? (IDP, token issuance)?
- **Associated Risks**: Excessive privilege, unauthorized data access, lateral movement after compromise.


### Token & Session Security (Token Lifecycle, Validation, Claims)
**Question**: Are token types, flows, and lifetimes explicitly defined (access vs refresh vs ID tokens), with short-lived access tokens, controlled refresh token usage, and session limits aligned to risk? (IDP-issued tokens)
- **Associated Risks**: Persistent unauthorized access, session hijacking, replay attacks.


**Question**: Are tokens securely generated and protected end-to-end, including strong signing algorithms, secure key storage, and prevention of token leakage through URLs, referrers, logs, and error messages? (IDP, token issuance/handling)
- A**ssociated Risks**: Token theft, impersonation, widespread compromise via log leakage.


**Question**: Is token validation enforced at every relying party, including signature verification, issuer (iss) and audience (aud) checks, expiry (exp) enforcement, and protection against algorithm confusion/misuse? (IDP-issued tokens, token consumers)
- **Associated Risks**: Forged tokens, authentication bypass, privilege escalation via claim tampering.


**Question**: Are revocation and re-authentication controls implemented (revocation endpoints or equivalent, refresh token rotation, reuse detection, forced re-auth on risk events/password changes)?
- **Associated Risks**: Inability to cut off compromised sessions, long-lived compromise, stolen refresh token reuse.

**Question**: Are anti-replay and channel protections implemented where appropriate (nonce/state validation, PKCE for public clients(PKCE (Proof Key for Code Exchange) is an extension to the OAuth 2.0 Authorization Code flow that prevents an attacker from redeeming a stolen authorization code), secure redirect URI handling, strict redirect allowlists)? (IDP, token issuance)
- **Associated Risks**: Authorization code interception, CSRF, token substitution.



### Data Security & Privacy
**Question**: Is data classification defined for identity attributes and token claims, with explicit rules preventing inclusion of unnecessary PII/secrets in tokens and logs, and with privacy-by-design controls (minimization, purpose limitation)? (IDP, IDP-issued tokens, IDP logs)
- **Associated Risks**: Privacy violations, regulatory non-compliance, breach impact amplification.
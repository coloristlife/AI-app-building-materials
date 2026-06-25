### Session Management

- **Question:** How are session timeouts (both absolute and idle) configured, and are they appropriate for the data sensitivity?
  - **Recommended Control:** Strict enforcement of server-side idle timeouts (e.g., 15 minutes for highly sensitive systems) and absolute timeouts (e.g., 8-12 hours) necessitating a fresh login.
  - **Associated Risk:** Unattended workstations or forgotten browser tabs allow unauthorized physical or remote attackers to hijack active, authenticated sessions.

- **Question:** If the system uses stateless tokens (e.g., JSON Web Tokens - JWT), how is token revocation handled before the token's natural expiration?
  - **Recommended Control:** Utilize short-lived access tokens (e.g., 5-15 minutes) paired with stateful, securely stored refresh tokens, or maintain a centralized deny-list/blocklist for revoked JWTs.
  - **Associated Risk:** If an attacker steals a stateless access token, they can impersonate the user until the token expires, as stateless tokens cannot be inherently "logged out" or revoked by the server.

- **Question:** Are concurrent sessions restricted or monitored to prevent credential sharing?
  - **Recommended Control:** Limit the number of simultaneous active sessions a single identity can have, and invalidate older sessions when a new login occurs from a different geographic location or device.
  - **Associated Risk:** Widespread credential sharing compromises accountability (non-repudiation) and hides malicious logins within legitimate traffic.
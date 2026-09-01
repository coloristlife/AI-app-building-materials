
# API Endpoint Security



### Security Review Questions

#### 1. Broken Object-Level Authorization (BOLA)
*   **Question:** How does the API endpoint validate that the authenticated user or client possesses explicit ownership of, or permission to access, the specific resource identifiers (e.g., `/api/v1/users/{id}/records`) passed in the request?

*   **Potential Risk:** 
    *   *Security Weakness:* Missing authorization checks between the authenticated session identity and the requested resource key.
    *   *Attack:* An attacker logs into their own account, inspects the network traffic to find a resource ID format, and alters the ID parameter in the URL or payload to match another user's ID.
    *   *Impact:* Unauthorized access, exposure, modification, or deletion of sensitive tenant or user data (confidentiality and integrity breach).

*   **Recommendation:** Implement an authorization check at the controller or service layer for every request. This check must map the user’s identity (extracted from a cryptographically signed token) to the requested resource ID in the database to verify ownership or access rights prior to processing.

#### 2. Rate Limiting and Resource Consumption
*   **Question:** What specific mechanisms (such as rate limits, payload size limits, and query complexity analysis) are enforced on the API endpoint to prevent resource exhaustion?

*   **Potential Risk:**
    *   *Security Weakness:* Lack of threshold restrictions on inbound request rates, database execution timeouts, or request payload sizes.
    *   *Attack:* A malicious actor sends a high volume of requests, transfers extremely large payloads, or requests deep nested queries (e.g., in GraphQL), overwhelming application servers or database connections.
    *   *Impact:* Service instability, application crash (Denial of Service), degradation of user experience for legitimate clients, and inflated cloud infrastructure costs.

*   **Recommendation:** Configure multi-tier rate limiting at the API Gateway level (e.g., globally per IP, and granularly per authenticated API key/user token). Set strict limits on HTTP request body sizes (e.g., max 10MB) and enforce pagination with a strict maximum limit (e.g., `limit=100`) on all collection-returning endpoints.

#### 3. Mass Assignment / Unsafe Data Binding
*   **Question:** How does the API endpoint restrict which fields can be modified by a client during creation or update operations (e.g., POST, PUT, PATCH requests)?

*   **Potential Risk:**
    *   *Security Weakness:* Blind model-binding or auto-binding frameworks that map incoming request objects directly to database models or domain entities.
    *   *Attack:* An attacker inspects API patterns and appends unauthorized parameters to their update request payload, such as `"is_admin": true`, `"role": "superuser"`, or `"balance": 9999.00`.
    *   *Impact:* Privilege escalation, unauthorized configuration changes, or financial manipulation without proper authorization or business logic validation.

*   **Recommendation:** Decouple public API contracts from internal database models. Use explicit Data Transfer Objects (DTOs) with field allowlists to define exactly what properties can be written by the user. Avoid using automatic binding features without explicitly declaring allowed fields.

#### 4. Broken Function-Level Authorization (BFLA)
*   **Question:** How does the API endpoint validate that the requester is authorized to execute the specific action (HTTP verb) against a route, especially for administrative, configuration, or state-changing operations?

*   **Potential Risk:**
    *   *Security Weakness:* Relying on the assumption that non-admin users will not discover administrative endpoints (e.g., `/api/admin/delete-user`), or failing to map authorization to specific HTTP verbs (allowing a read-only user to send a DELETE request).
    *   *Attack:* An attacker identifies admin endpoints (via JS files, guessing, or documentation leaks) and executes requests directly using their standard user credentials.
    *   *Impact:* Unauthorized execution of critical administrative functions, leading to system modification, data corruption, or denial of service.

*   **Recommendation:** Implement a robust authorization layer (RBAC/ABAC) that validates the user's role or scopes at the router/controller level before route execution. Ensure that permissions are mapped explicitly to the combination of the route and the HTTP method (e.g., restricting `DELETE` to the `admin` role).

#### 5. Input Schema Validation and Injection Prevention
*   **Question:** What method is used to validate that incoming request payloads conform to a strict schema (data types, formats, lengths, and patterns) before the application layer processes the input?

*   **Potential Risk:**
    *   *Security Weakness:* Acceptance of malformed, untyped, or excessively long payloads that are passed directly to database engines, command interpreters, or serializers.
    *   *Attack:* An attacker injects malicious SQL statements, NoSQL queries, shell commands, or dangerous payload structures into the input fields.
    *   *Impact:* Remote code execution, unauthorized data exfiltration, database compromise, or application crashes.

*   **Recommendation:** Define and enforce strict API schemas using technologies like OpenAPI, JSON Schema, or gRPC Protobufs. Apply type checking, length boundaries, and strict regex patterns for strings. Ensure that all downstream database operations utilize parameterized queries or ORM equivalents to neutralize injection vectors.

#### 6. JWT and Token Validation Security
*   **Question:** How does the API endpoint or gateway cryptographically validate client identity tokens (e.g., JWTs) on every request, and how is token revocation handled?

*   **Potential Risk:**
    *   *Security Weakness:* Insecure token validation, such as allowing the `"none"` signature algorithm, failing to verify expiration claims (`exp`), using weak/hardcoded signing keys, or neglecting blocklists for revoked tokens.
    *   *Attack:* An attacker crafts a forged JWT with altered claims (e.g., changing the username or role) or presents an expired or revoked token to access the system.
    *   *Impact:* Authentication bypass, identity theft, and unauthorized access to downstream resources.

*   **Recommendation:** Delegate token validation to an API Gateway or a centralized, hardened security filter. Ensure validation checks the token signature using a strong cryptographic algorithm (e.g., RS256/EdDSA), validates standard claims (`exp`, `nbf`, `aud`, `iss`), and retrieves verification keys securely via a caching JWKS (JSON Web Key Set) endpoint. Maintain a revocation check mechanism (e.g., Redis-backed token blocklist) for high-value operations.

#### 7. Audit Logging and Anomaly Detection
*   **Question:** What security-relevant events (such as authentication failures, authorization denials, input validation failures, and high-frequency resource requests) are logged by the API, and how are these logs monitored?

*   **Potential Risk:**
    *   *Security Weakness:* Insufficient logging of API exceptions, access denials, or suspicious traffic spikes; or conversely, logging raw sensitive data which exposes the system to secondary leaks.
    *   *Attack:* An attacker performs silent reconnaissance, brute-forces endpoints, or slowly exfiltrates data without being detected.
    *   *Impact:* Delayed detection of ongoing breaches, inability to reconstruct security incidents (compliance failure), and potential exposure of sensitive credentials inside log storage.

*   **Recommendation:** Log all security-significant events (authentication attempts, authorization failures, input validation errors, and HTTP status codes 401, 403, and 422) with context (such as timestamp, client identifier, resource accessed, and request ID). Sanitize logs to strip passwords, full credit card numbers, and secret tokens. Forward logs in real-time to a centralized SIEM platform configured with alerts for high-frequency failures.
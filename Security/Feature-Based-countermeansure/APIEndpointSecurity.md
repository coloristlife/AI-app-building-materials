
# API Endpoint Security

Is the  endpoint  protected against brute force attacks? Are rate limiting and throttling implemented?
risk : Denial of service, resource exhaustion


----
Are API endpoints exposed through Route53 protected by AWS WAF or similar web application firewall?
OWASP Top 10 vulnerabilities (SQL injection, XSS, etc.)


# Payload Validation
How is the JSON payload validated in the API call ? Are filename and domainId sanitized to prevent path traversal or injection attacks
risk : Arbitrary file access, command injection

# Error Handling
Do API error responses avoid leaking sensitive information (e.g., stack traces, internal paths, database schema)?
risk: Information disclosure aiding attackers


Are failed API authentication attempts logged and monitored for suspicious patterns?
risk: Undetected brute force or credential stuffing attacks
Here is the security review questionnaire for **Identity & Access Management **, organized into logical architectural categories. These questions are designed to enforce strict access boundaries, prevent lateral movement, and align with frameworks like NIST SP 800-53 (AC family), OWASP Top 10 (A01:2021-Broken Access Control), and ISO 27001.

### Authorization Architecture and Granularity
*Focuses on the foundational design of how permissions are structured, evaluated, and assigned to human users.*

- **Question:** How is the principle of least privilege enforced at the application and infrastructure layers, and is access granted based on explicitly defined roles and attributes rather than broad, default permissions?
  - **Recommended Control:** Implementation of granular Role-Based Access Control (RBAC) or Attribute-Based Access Control (ABAC) anchored in a "default deny" posture, ensuring users are granted only the absolute minimum permissions required to perform their specific business tasks.
  - **Associated Risk:** Over-privileged accounts allow users to access sensitive data or perform destructive actions outside their job function, massively increasing the blast radius of both malicious insider threats and compromised external accounts.


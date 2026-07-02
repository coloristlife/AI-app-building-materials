

### The Universal Integration Pattern: "API Scope vs. Tool Activation"

For any tool inside Unily Glass, security is managed at two independent gates:

```
               [ User Query via Glass ]
                         │
                         ▼
        ┌──────────────────────────────────┐
        │  Gate 1: Glass Tool Config       │  ◄── Controlled by Business/HR Admin
        │  (Is the tool enabled in UI?)    │      (Application Layer)
        └─────────────────┬────────────────┘
                          │ YES
                          ▼
        ┌──────────────────────────────────┐
        │  Gate 2: Target System Auth      │  ◄── Controlled by IT/Security Admin
        │  (Is OAuth scope consented?)     │      (Infrastructure Layer)
        └─────────────────┬────────────────┘
                          │ YES
                          ▼
             [ Data Flow / Action Executed ]
```

---

### Real-World Examples Across Non-Microsoft Integrations

To see how this operates outside of Microsoft Graph, consider these common enterprise integrations:

#### 1. Workday Integration (HR)
* **Infrastructure Gate (Workday):** The Workday Administrator configures an Integration System User (ISU) or delegates OAuth scopes. Permissions are restricted to specific Security Groups (e.g., allowing access only to *Time-Off Requests* but blocking *Compensation Data*).
* **Application Gate (Unily Glass):** The Unily Admin enables the "Workday Leave Request Tool" in the Glass configuration panel.
* **The Constraint:** If the Workday Security Group does not grant access to the underlying APIs, enabling the Leave Request tool in Glass will only result in an API authorization failure.

#### 2. ServiceNow Integration (IT Service Management)
* **Infrastructure Gate (ServiceNow):** An OAuth Client is registered in ServiceNow. The integration is restricted to specific REST API scopes and ACLs (Access Control Lists) in ServiceNow (e.g., `incident_read`, `incident_write`).
* **Application Gate (Unily Glass):** The "ServiceNow Ticket Status Tool" is enabled in Glass, allowing users to ask, *"What is the status of my laptop replacement ticket?"*
* **The Constraint:** If the ServiceNow admin revokes the OAuth client credentials or restricts the REST API scopes on the ServiceNow side, the Glass tool will instantly cease to function, preventing any data leakage.

#### 3. Salesforce Integration (CRM)
* **Infrastructure Gate (Salesforce):** A "Connected App" is defined in Salesforce. It is assigned specific OAuth scopes (such as `api` or `chatter_api`) and restricted to certain user profiles.
* **Application Gate (Unily Glass):** The "Salesforce Pipeline Summary Tool" is toggled on in the Unily Management Console.
* **The Constraint:** If a user asks Glass to pull a sales pipeline report, but the Connected App's OAuth scopes do not authorize that specific object query, the integration is blocked at the gateway level.

---

### Architectural Significance of this Design

As a security architect, this universal design is highly desirable for three reasons:

1. **Defense in Depth:** Security is not solely reliant on the SaaS application's UI configuration. If the UI configuration fails or is misconfigured, the underlying API gateway acts as a hard backstop.
2. **Separation of Duties (SoD):** It allows **IT/Infosec Teams** to manage the secure API pipelines (Infrastructure Layer) while allowing **HR, Internal Comms, or Business Teams** to manage what features are actively visible to employees (Application Layer). 
3. **Compliance and Least Privilege:** It prevents "orphan access." If your company offboards an application (e.g., migrating from ServiceNow to Jira), revoking the API registration at the target system level guarantees that Unily can no longer access that data, regardless of whether someone forgot to toggle the tool off inside Glass.



To be precise and maintain professional accuracy, **"The Universal Integration Pattern: 'API Scope vs. Tool Activation'"** was a descriptive label used in my previous explanation to conceptualize the process. It is not an official, trademarked, or globally standardized term in the cybersecurity industry.

In professional security architecture, this dual-control mechanism maps to several established, industry-standard terms and architectural patterns. If you are writing a security review, policy document, or architectural diagram, you should use the following formal terms to describe this mechanism:

### 1. Dual-Gate (or Layered) Authorization
* **What it means:** A security design where an action must pass through two independent, sequential validation checkpoints (gates) before it is executed. 
* **How it applies:** 
  * **Gate 1 (Application Gate):** Checks if the feature is administratively enabled and visible to the user.
  * **Gate 2 (Infrastructure Gate):** Checks if the system-to-system API connection has the cryptographic authorization (OAuth scope) to execute the request.

### 2. Defense-in-Depth (Coordinated Control)
* **What it means:** The classic security principle of layering redundant defensive controls so that if one control fails, another is present to prevent a security breach.
* **How it applies:** If a business administrator accidentally enables a sensitive tool (e.g., Salesforce Pipeline) in the application layer, the defense-in-depth model ensures the data remains safe because the infrastructure-layer API permission was never granted.

### 3. Feature Flagging Coupled with Principle of Least Privilege (PoLP)
* **What it means:** Combining software development deployment practices with strict access controls. 
* **How it applies:** "Tool Activation" is functionally a **Feature Flag** or Feature Toggle. "API Scope" is the enforcement of the **Principle of Least Privilege**. Together, they ensure that the software feature is only toggled "on" when the minimum necessary technical permissions have been explicitly granted.

### 4. Administrative Separation of Duties (SoD) / Dual Control
* **What it means:** A security policy requiring more than one person or role to complete a sensitive task, preventing a single point of compromise or accidental misconfiguration.
* **How it applies:** 
  * The **Unily Admin** controls *activation* (which tools are available in the UI).
  * The **Azure/Entra ID or Okta Admin** controls *authorization* (which API scopes are consented to). 
  * Neither administrator can unilaterally expose data without the other's action.

### Summary
While you can refer to it informally as a "dual-control API integration pattern," the most precise industry terms to use in your security documentation are **Dual-Gate Authorization** and **Defense-in-Depth**.



-----

In the case of the Unily Glass, to understand this requirement as a security architect, it helps to think of it as a **"Double-Key" authorization model** (or a dual-control gate). 

The quote describes a defense-in-depth mechanism where both the **Infrastructure Layer (Entra ID)** and the **Application Layer (Unily Glass)** must independently agree before any data can flow. 

Here is a breakdown of how this works, why it is designed this way, and the architectural implications.

---

### The Two Control Points Explained

#### 1. The Infrastructure Gate: Entra ID App Registration (Graph Scopes)
* **What it is:** This is the cloud-level permission boundary managed by your IT/Security team in Microsoft Entra ID. When Glass wants to talk to Microsoft 365 (e.g., to read emails, search SharePoint, or check calendars), it uses an **App Registration**.
* **How it controls access:** The App Registration is granted specific OAuth 2.0 scopes (permissions) for Microsoft Graph (e.g., `Mail.Read`, `Files.Read`). If a scope is not consented to here, Microsoft's security boundary will block Glass from accessing that data, no matter what.

#### 2. The Application Gate: Unily Glass Tool List
* **What it is:** This is the administrative console within the Unily Glass platform itself. 
* **How it controls access:** This is where business administrators toggle individual features or "tools" on or off for the end-users (e.g., enabling the "Email Search Tool" or the "OneDrive Document Tool" within the chat interface).

---

### The Alignment Matrix (How They Interact)

To visualize how these two gates must align, consider the four possible configuration states:

| Entra ID Graph Scope (Infrastructure) | Glass Tool Configuration (Application) | Operational & Security Outcome |
| :--- | :--- | :--- |
| **❌ Not Consented** | **❌ Disabled** | **Secure & Silent:** The feature is completely off. No security risk, no operational issues. |
| **✅ Consented** | **✅ Enabled** | **Functional & Authorized (Ideal State):** The user can use the tool, and the backend has the authorization to fetch the data. |
| **❌ Not Consented** | **✅ Enabled** | **Operational Failure (Broken Experience):** The user sees the tool in Glass and tries to use it, but the request fails with an HTTP 401/403 (Unauthorized) error because Microsoft blocks it at the API level. |
| **✅ Consented** | **❌ Disabled** | **Security Vulnerability (Over-Privilege):** The tool is hidden from the user, but the Unily Glass application still possesses the technical ability to read that Microsoft data. This violates the **Principle of Least Privilege**. |

---

### Why is this designed this way?

From a security architecture perspective, this design provides a strong separation of duties:

1. **IT/Security remains in control of the data:** Unily administrators cannot arbitrarily decide to turn on an email-reading tool if the Security Team has not explicitly approved and consented to the `Mail.Read` scope in Entra ID. 
2. **Business Admins control the user experience:** Just because Security has approved a wide range of permissions for future use, Business Admins can choose to roll out tools gradually without exposing users to too many features at once.

### Security Architect's Recommendation for Implementation

When implementing Glass with this architecture, consider the following best practices:

* **Strict Alignment:** Only consent to Graph scopes in Entra ID that correspond directly to tools you intend to enable in Glass immediately. 
* **Avoid "Scope Creep":** If you decide to disable a tool in Glass (for example, deprecating the Calendar tool), **immediately revoke** the corresponding Graph scope (e.g., `Calendars.Read`) from the Entra ID App Registration.
* **Audit regularly:** Conduct quarterly audits comparing the active tool list in Glass with the consented API permissions in Entra ID to ensure there is no configuration drift or over-privileging.

### reference
https://learn.microsoft.com/en-us/graph/permissions-reference  

https://www.unily.com/features/unily-glass 

https://learn.microsoft.com/en-us/shows/beginners-series-to-microsoft-graph/module-2-microsoft-graph-permissions-or-scopes 

https://learn.microsoft.com/en-us/graph/permissions-reference
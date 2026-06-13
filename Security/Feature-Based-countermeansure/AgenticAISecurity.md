

### **Countermeasure Category: Autonomous Agency & Human-in-the-Loop (HITL)**

**Feature/Capability:**
Autonomous LLM-driven Write/Modify Actions (e.g., Automated Code Commits, Production Infrastructure Changes, or User Permission Management).

**Generic Security Review Questions:**

*   **Capability Probe (Attack Surface):** 
    *   Does the LLM-integrated application have the technical authority (via API tokens, Service Accounts, or SSH keys) to execute "state-changing" actions—such as modifying source code, altering database schemas, or changing access control lists—without a secondary system or human validation?
    *   What is the maximum effective permission level (e.g., `Owner`, `Admin`, `Contributor`) assigned to the LLM’s service identity within the Software Development Lifecycle (SDLC) or production environment?

*   **Countermeasure Probe (Residual Risk):** 
    *   Are there hard-coded "Human-in-the-Loop" (HITL) approval gates enforced at the platform level (e.g., GitHub Branch Protections, AWS IAM Condition Keys, or Jenkins Approval Gates) that prevent the LLM from completing consequential actions until a verified human operator signs off?
    *   Is the system designed to follow the "Principle of Least Agency," where the LLM is restricted to suggesting changes (read-only/draft mode) rather than executing them (write/execute mode)?

**Associated Risk:**
**System-Wide Compromise and Integrity Loss (Worst Case Scenario):** 
Without a mandatory HITL control, a successful **Prompt Injection (LLM01)** can hijack the model's logic, causing it to exercise its **Excessive Agency (LLM08)** to perform malicious actions. This could result in an unpredictable entity having "Domain Admin" equivalent powers, leading to the unauthorized deployment of backdoored code, the deletion of critical production infrastructure, or a total breach of the enterprise’s trust boundaries. 

From a compliance perspective (SOC 2, ISO 27001), the absence of these controls represents a failure in **Change Management** and **Access Control** (e.g., ISO 27001 Annex A 8.32), as the model lacks the accountability and deterministic logic required for secure automated decision-making.
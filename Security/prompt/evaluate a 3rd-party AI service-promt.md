


### The Evaluation Prompt

**Role:** You are a Senior AI Security Architect and GRC Auditor.
**Task:** Analyze the 3rd-party AI service provided in the link below. Your goal is to identify security "misses" (capabilities common in enterprise-grade or agentic AI services that are absent or poorly documented here) and provide specific mitigation controls.

**Evaluation Framework (The 7 Pillars):**


### **Pillar 1: Governance, Risk & Compliance (GRC)**
*   **Traditional:** Standard compliance (ISO 27001, SOC 2, GDPR) and vulnerability management.
*   **AI/Agentic:** Alignment with **ISO/IEC 42001** and **NIST AI RMF**.
*   **Risk Control:** Defined **Agentic Risk Maps** (blast radius) and **Human-in-the-Loop (HITL)** workflows for critical actions.
*   **Supply Chain:** Monitoring of AI libraries (LangChain, etc.) and maintaining a **Software Bill of Materials (SBOM)**.

### **Pillar 2: Infrastructure & Cloud Security**
*   **Availability:** Guaranteed GPU/TPU access and **Token-based scaling** to prevent latency/outages.
*   **Isolation:** Tenant data siloing via private VPCs/schemas and **AISPM** monitoring for vector databases.
*   **Containment:** Execution of agent actions in **ephemeral sandboxes** to isolate malicious code.
*   **Advanced Protection:** Use of **Confidential Computing (TEEs)** for data-in-use during RAG or processing.

### **Pillar 3: Identity & Access Management (IAM)**
*   **Non-Human Identity (NHI):** Use of **Workload Identity Federation** (SPIFFE/SPIRE) over static API keys.
*   **Identity Chaining:** Agents must impersonate end-user scopes (**Least Privilege**) rather than using broad service accounts.
*   **Dynamic Access:** **Just-In-Time (JIT)** privilege escalation and honoring existing Row-Level Security (RLS) during data retrieval.

### **Pillar 4: Agentic Orchestration & Tool Security**
*   **Tool Scoping:** Granular, per-tool permissions (e.g., Read-only CRM access vs. Read-Write Task access).
*   **Integrations:** Authenticated **MCP (Model Context Protocol)** servers and input validation on tool-returned data.
*   **Memory Security:** Protection against **memory poisoning** and the ability to sanitize/encrypt long-term agent memory.
*   **System Integrity:** **Zero Trust** between multiple agents and protection against infinite recursive loops.

### **Pillar 5: Application & Control Plane Security**
*   **Traditional:** API Gateway management, rate limiting, and OWASP Top 10 mitigation.
*   **Semantic Guardrails:** Real-time **intent-based filtering** to block prompt injections and PII leakage.
*   **Behavioral Analysis:** Monitoring for anomalies in agent behavior (e.g., unusual data scraping volumes).
*   **Output Validation:** Enforcing strict schemas (JSON/XML) to prevent "jailbroken" outputs from affecting downstream logic.

### **Pillar 6: Operational Resilience & Observability**
*   **Fault Tolerance:** **Deterministic fallbacks** (if-then logic) and human redirection when AI fails or hallucinates.
*   **Recovery:** Disaster Recovery (DR) plans that account for regional GPU/Chip availability.
*   **Forensics:** Full auditability of the agent’s **"Chain of Thought"** reasoning path for incident investigation.

### **Pillar 7: Legal, Ethical & Commercial Perspectives**
*   **Data Sovereignty:** Contractual **Model Training Opt-outs** and geographic restrictions on RAG data.
*   **Liability:** Defined indemnification for **hallucination-driven errors** and IP infringement.
*   **AI-Specific SLAs:** Performance guarantees covering **Time to First Token (TTFT)** and maximum allowable **Hallucination Rates**.



**Required Output Structure:**

**Title of security issue:** [The specific security risk, not the control]
**Description:** [Detailed explanation of how this gap manifests in this specific service]
**Recommendation:** [Specific technical or procedural control to mitigate the risk]
**Risk Level:** [Critical / High / Medium / Low]
**Source of Truth:** [Provide the direct link to the documentation page you analyzed to reach this conclusion]

***

### Example of how the output will look (for a hypothetical service):

**Title of security issue:** Lack of Identity Chaining in Agentic Workflows  
**Description:** The service documentation indicates that agents utilize a single, high-privilege Master API Key to interact with connected tools (Salesforce, Slack). There is no mechanism for the agent to inherit or "chain" the specific permissions of the end-user who triggered the request. This creates a massive blast radius if the agent is compromised via prompt injection.  
**Recommendation:** Implement Workload Identity Federation or OIDC-based impersonation tokens. The service should require a "Just-In-Time" (JIT) scoped token for the agent that matches the user's specific Row-Level Security (RLS) permissions.  
**Risk Level:** Critical  
**Source of Truth:** https://docs.example-ai-service.com/authentication/api-keys  

**Instructions:**
1. Browse/Analyze the service documentation at this link: **https://docs.cloud.google.com/gemini/enterprise/docs/connectors/ms-outlook/third-party-config**
2. For each item of the framework, if it is not gap, provide the evaluation summary and provide the Source of Truth for the conclusion.
3. For every gap, provide a recommendation and the specific documentation link used as the "Source of Truth" to confirm the absence of the feature.
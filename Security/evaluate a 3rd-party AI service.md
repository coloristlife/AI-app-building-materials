To evaluate a 3rd-party AI service effectively, you must distinguish between the probabilistic nature of AI (where outcomes vary) and the deterministic nature of traditional applications (where the same input always yields the same output).

Excluding the model layer (weights/training), this evaluation focuses on the operational infrastructure, the agentic orchestration layer, and the traditional application stack.

---

### 1. Governance, Risk & Compliance (GRC)
Ensures the service is enterprise-grade and follows emerging AI standards.
*   **Traditional:** ISO 27001, SOC 2 Type II, and GDPR/CCPA compliance. Robust vulnerability management, patch management, and incident response plans.
*   **AI-Specific:** Alignment with **ISO/IEC 42001** (AI Management System) or **NIST AI RMF**. Policies for mitigating AI hallucinations and algorithmic bias.
*   **Agentic Specific:** An **Agentic Risk Map** defining the "blast radius" of autonomous actions. A "Human-in-the-Loop" (HITL) framework for high-impact decisions (e.g., financial transfers or data deletion).
*   **Supply Chain Security:** Assessment of the AI software supply chain—monitoring third-party libraries (e.g., LangChain, AutoGPT) and ensuring a Software Bill of Materials (SBOM) is maintained.

### 2. Infrastructure & Cloud Layer
Traditional security prevents unauthorized access; AI infrastructure security focuses on the containment of non-deterministic actions.
*   **Compute & Scalability:** Guaranteed access to GPU/TPU resources (avoiding "spot" availability outages). Ability to handle "Token Scaling" (bursts in token volume) vs. traditional request scaling without latency spikes.
*   **Network Security:** Micro-segmentation, encryption at rest/transit (AES-256, TLS 1.3), and DDoS protection.
*   **Tenant Isolation:** Verification of data siloing (e.g., dedicated VPCs or logically separated schemas in shared databases).
*   **AISPM (AI Security Posture Management):** Monitoring of AI-specific resources like **Vector Databases** (Pinecone, Weaviate) for unauthorized access or misconfiguration.
*   **Agentic Sandboxing:** Execution of agent actions in **ephemeral, isolated environments**. If an agent is tricked into running a malicious command (e.g., "rm -rf"), the execution must be contained within a one-time-use container or sandbox.
*   **Hardware-Level Security:** Use of **Confidential Computing (TEEs)** to ensure that data being processed in memory (especially during RAG) is encrypted even from the cloud provider.

### 3. Identity & Access Management (IAM)
In traditional apps, users are humans; in agentic services, the **Agent is a First-Class Identity**.
*   **Traditional:** Integration with existing SSO (SAML/OIDC), MFA, and standard RBAC.
*   Dynamic RBAC: Can the service honor your existing Row-Level Security.
(RLS) when an agent is querying your internal databases?
*   **Non-Human Identity (NHI):** Use of **Workload Identity Federation** rather than static API keys. Agents should use short-lived, cryptographically signed identities (e.g., SPIFFE/SPIRE).
*   **Identity Chaining & Delegated Authority:** When "User A" triggers "Agent B" to access "Database C," the system must perform **Identity Chaining**. The agent should impersonate the user's specific scopes (Least Privilege) rather than using a high-level service account.
*   **Just-In-Time (JIT) Privileges:** Agents should only be granted elevated permissions at the moment of execution, with immediate revocation upon task completion.

### 4. Agentic Orchestration & Tool Security
This layer governs how agents interact with the real world through APIs and tools.
*   **Tool-Use Scoping:** Granular permissions for tools (e.g., an agent may have "Read-Only" access to a CRM but "Read-Write" access to a scheduling tool).
*   **MCP (Model Context Protocol) Security:** If using MCP to connect tools, servers must be authenticated, and all tool-returned data must undergo input validation to prevent **Indirect Prompt Injection**.
*   **Memory Integrity:**
    *   **Short-term:** Protection of session history from being poisoned by malicious data during a conversation.
    *   **Long-term:** Encryption of "agent memory" (stored in vector DBs) and the ability to "sanitize" or delete specific memories if they are found to be malicious or contain PII.
*   **Multi-Agent Trust:** In multi-agent systems, a **Zero Trust** architecture should be applied between agents. Handoffs must be authenticated, and one agent should not implicitly trust the output of another.
*   **Recursive Loop Protection:** Logic to detect and kill "infinite loops" where agents repeatedly call tools or themselves, preventing exhaustion of costs and resources.

### 5. Application & API Layer (The Control Plane)
Traditional WAFs are "content-aware," but AI security must be "intent-aware."
*   **Traditional:** Rate limiting, API Gateway management (OAuth 2.0/JWT), and protection against the OWASP Top 10.
*   **Semantic Guardrails:** Runtime filters (e.g., Lasso, Lakera) that inspect the "meaning" of inputs/outputs to block prompt injections and PII leakage in real-time.
*   **Intent Analysis & Behavioral Baselining:** Security monitoring that flags anomalies in agent behavior (e.g., "Agent usually queries 5 records but is currently attempting to scrape 5,000").
*   **Output Validation:** Ensuring AI-generated content follows strict schemas (JSON/XML) before being passed to a downstream deterministic system to prevent "jailbreaking" the application logic.

### 6. Operational Resilience & Reliability
*   **Deterministic Fallbacks:** If the AI agent fails or the model returns an error, there must be a hard-coded "if-then" logic or a redirection to a human operator.
*   **Disaster Recovery (DR):** Failover capabilities to different cloud regions, accounting for the fact that specific AI chips (GPUs) might have regional availability constraints.
*   **Observability & Auditability:** Full logging of the agent’s **"Chain of Thought"** or reasoning path, not just the final output. This is vital for forensic auditing after a security incident.

### 7. Legal, Commercial, and Ethical Perspectives
*   **IP & Data Rights:**
    *   **Model Training Opt-out:** Explicit contractual guarantee that your data/prompts will not be used to train the vendor's models.
    *   **Output Ownership:** Clear definition of who owns the generated content/code.
*   **Liability & Indemnification:**
    *   **Accuracy Liability:** Defining who is responsible if an agent executes an unauthorized or harmful transaction based on a hallucination.
    *   **Copyright Indemnity:** Protection against claims that AI-generated output infringes on 3rd-party intellectual property.
*   **Service Level Agreements (SLAs):**
    *   **Beyond Uptime:** Standard 99.9% uptime combined with AI-specific metrics like **Time to First Token (TTFT)** and a maximum allowable **Hallucination Rate** for specific tasks.
    *   **Data Sovereignty:** Ensuring that data retrieved for RAG (Retrieval-Augmented Generation) remains within specific geographic boundaries.
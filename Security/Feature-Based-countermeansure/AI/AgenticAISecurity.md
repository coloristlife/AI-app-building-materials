 **Agentic AI Security** (autonomous or semi-autonomous AI agents that utilize tools, APIs, and reasoning to execute tasks). 

This evaluation is closely aligned with emerging industry frameworks such as the **NIST AI Risk Management Framework (AI RMF)**, the **OWASP Top 10 for LLM Applications** (specifically LLM06: Insecure Plugin Design and LLM08: Excessive Agency), and zero-trust principles.

We would also like to better understand the internal design and operation of the agentic framework. Specifically, could you provide more details on how the different agents are coordinated and interact with each other, what tools or services are invoked by these agents, and how communication and data flow are managed within the framework?

Understanding the underlying architecture and workflow of the agentic AI system will help us properly evaluate the security controls, potential risks, and safeguards implemented within the framework.

### Agent Identity & Access Management (IAM)

- **Question:** How is identity assigned to the AI agent, and how are its permissions scoped when authenticating to internal APIs, databases, and third-party services?
  - **Recommended Control:** Assign a dedicated, least-privilege Service Account or machine identity to each agent. Implement granular Role-Based Access Control (RBAC) and strict OAuth scopes tailored to the specific task. Ensure the agent's access rights never exceed the permissions of the human user initiating the session.
  - **Associated Risk:** If an agent is over-privileged, it creates a severe "Confused Deputy" vulnerability. An attacker who manipulates the agent could weaponize its credentials to access unauthorized databases, modify sensitive records, or pivot laterally across the corporate network.

### Tool Execution & Action Boundaries

- **Question:** What guardrails and boundaries govern the external tools, APIs, or code execution environments the AI agent is authorized to invoke?
  - **Recommended Control:** Implement strict allow-lists for API endpoints and parameters the agent can call. Sandbox all agent-driven code execution (e.g., Python interpreters) within highly restricted, ephemeral, and network-isolated containers. Implement API rate limiting specific to the agent's identity.
  - **Associated Risk:** Without strict execution boundaries, a hallucinating, malfunctioning, or hijacked agent could autonomously execute malicious code on the host system, conduct SSRF (Server-Side Request Forgery) attacks against internal networks, or consume massive cloud resources.


- **Question:** What guardrails are in place to validate data passing between chained tool invocations (where the output of one tool is used as the input for another)?
  - **Recommended Control:** Implement strict data validation, schema enforcement, and sanitization guardrails on chained calls. Treat the output of *every* external tool or API as untrusted input before allowing the agent to pass it as a parameter to the next tool in the sequence.
  - **Associated Risk:** Without guardrails on chained operations, an exploit can easily escalate. For example, an agent instructed to read a web page (Tool 1) might ingest an injected malicious payload, which it then blindly passes into a database query or script execution tool (Tool 2), resulting in an autonomous system compromise.


- **Question:** How do you enforce human oversight for state-changing, destructive, or high-impact actions initiated by the AI agent?
  - **Recommended Control:** Implement a mandatory Human-In-The-Loop (HITL) approval mechanism for any critical actions (e.g., financial transactions, sending external emails, modifying infrastructure, or deleting data). The agent must pause execution and request explicit cryptographic or logged human approval before proceeding.
  - **Associated Risk:** Excessive agency without human oversight can lead to catastrophic autonomous errors. The agent could mistakenly delete production databases, trigger widespread service outages, or send unauthorized, sensitive communications to external clients.

- **Question:** Is the system designed to follow the "Principle of Least Agency," where the AI agent is restricted to suggesting changes (read-only/draft mode) rather than directly executing them (write/execute mode)?
  - **Recommended Control:** Enforce the "Principle of Least Agency" by designing the agent's workflow to be read-only or draft-oriented by default. When a state-changing action (write, delete, or execute) is required, the agent should only be allowed to generate a proposed payload (e.g., staging a pull request, drafting an email, or queuing a transaction). The system must require a human operator to explicitly review and commit the action.
  - **Associated Risk:** Granting an agent full write/execute agency without restriction bridges the gap between a logical error and a system impact. If the agent acts autonomously, hallucinations, misinterpretations, or prompt injection attacks can immediately translate into unauthorized system modifications, data corruption, or destructive actions with no opportunity for human intervention.


- **Question:** How do you ensure that each AI agent is provisioned with only the minimum set of tools required for its specific function?
  - **Recommended Control:** Enforce a strict "minimum tool set per agent" policy. Instead of granting access to a global registry of plugins or tools, bind explicitly defined, limited toolsets to individual agent profiles based on their exact use case. Remove or disable any unused capabilities.
  - **Associated Risk:** Equipping an agent with unnecessary capabilities (e.g., giving a simple customer support agent access to an internal file deletion tool or an SQL query executor) unnecessarily expands the attack surface. If the agent is hijacked via prompt injection, the attacker can weaponize those extra tools.




### Input Security & Adversarial Defenses

- **Question:** How is the AI agent protected against malicious instructions, prompt injections, and jailbreaks originating from untrusted users or ingested third-party data (e.g., reading a compromised web page)?
  - **Recommended Control:** Deploy a defense-in-depth strategy utilizing an AI/LLM Firewall (e.g., Enterprise AI Guardrails) to filter malicious intent. Strictly separate system instructions from user data (using techniques like chat templating and system prompts). Continuously subject the agent to automated adversarial testing and red-teaming.
  - **Associated Risk:** Successful prompt injection can completely hijack the agent’s goal. An attacker could overwrite the agent's system instructions, forcing it to bypass safety filters, act as an attacker-controlled proxy, or attack other users interacting with the system (Indirect Prompt Injection).

- **Question:** How are the agent's core instructions designed to resist manipulation, and are hardened prompts utilized to enforce strict operational boundaries?
  - **Recommended Control:** Employ securely engineered, hardened system prompts that explicitly define the agent’s persona, negative constraints (what it must *never* do), and strict operational boundaries. Use prompt parameterization, enforce prompt version control, and ensure system directives are placed in the most secure, non-overridable context window supported by the model provider.
  - **Associated Risk:** Weak, vague, or overly generic system prompts make it trivial for attackers to convince the agent to break character, ignore safety boundaries, and execute unauthorized actions through simple conversational manipulation, role-play jailbreaks, or logical deception.

### Data Privacy & Output Handling

- **Question:** How do you ensure that the agent does not ingest unauthorized sensitive data, or exfiltrate intellectual property and PII in its outputs or API calls?
  - **Recommended Control:** Implement Data Loss Prevention (DLP) scanners on both the prompts sent to external LLMs and the agent's final outputs to redact PII/PHI. Enforce strict data-level access controls during Retrieval-Augmented Generation (RAG) so the agent can only access documents the invoking user is authorized to see.
  - **Associated Risk:** The agent might inadvertently memorize and leak sensitive intellectual property, PII, or secrets retrieved during its reasoning process. Additionally, sending raw, unredacted corporate data to third-party model providers could violate GDPR, CCPA, and enterprise confidentiality agreements.

### Monitoring, Auditing & Explainability

- **Question:** How are the agent's autonomous decisions, intermediate reasoning steps, and tool invocations logged and monitored for anomalous behavior?
  - **Recommended Control:** Implement comprehensive, tamper-evident logging of the agent's entire "Chain of Thought" (CoT), exact API requests/responses, and triggered safety filters. Forward these logs to a centralized SIEM and create alerting rules for anomalous behaviors (e.g., an agent suddenly querying a database it has never accessed before, or repetitive failed API calls).
  - **Associated Risk:** Agentic AI operates in a non-deterministic manner. Without deep observability into *why* an agent made a decision and *what* exact API calls it executed, security teams will be completely blind during an incident response investigation, making it impossible to trace the root cause of a breach or data leak.


- **Question:** How is comprehensive invocation logging implemented for every tool, API, and plugin the agent interacts with?
  - **Recommended Control:** Implement rigorous, tamper-evident invocation logging for all external actions. Logs must capture the timestamp, the identity of the triggering user/session, the exact input payload sent to the tool, the raw output returned by the tool, and the agent's "Chain of Thought" reasoning that led to the invocation.
  - **Associated Risk:** Without detailed invocation logging at the tool level, security teams operate completely in the dark. In the event of an incident or data breach, it will be impossible to audit the agent's behavior, determine the blast radius, or identify exactly what malicious commands or data exfiltration took place.















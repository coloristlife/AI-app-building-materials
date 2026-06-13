
 

Because Large Language Models (LLMs) do not inherently distinguish between "code/instructions" and "data," relying purely on tool-level controls leaves you vulnerable to data exfiltration, reputation damage, and logic manipulation.

To build a complete Defense-in-Depth strategy for Prompt Injection (both Direct and Indirect), you must add the following domain to your security review:

### 1. Input Filtering & AI Firewalls
- **Question:** How are user inputs and external data payloads analyzed for malicious prompt injection attempts or jailbreaks before reaching the LLM?
- **Recommended Control:** Deploy an AI Gateway or LLM Firewall (e.g., NeMo Guardrails, Lakera Guard, Microsoft Azure AI Content Safety) to scan and block adversarial inputs, prompt leaking attempts, and known jailbreak signatures *before* inference occurs.
- **Associated Risk:** Without pre-filtering, attackers have unrestricted ability to experiment with adversarial prompts, highly increasing the likelihood they will find a bypass to manipulate the LLM's logic and hijack the agent.

### 2. Prompt Architecture & Context Separation
- **Question:** How does the system architecturally separate trusted administrative instructions (system prompts) from untrusted user inputs or external data?
- **Recommended Control:** Utilize strict prompt templates with explicit, randomized delimiters (e.g., XML tags like `<untrusted_input>`) to encapsulate user data. Strongly enforce role-based API structures (e.g., OpenAI's ChatML distinguishing between `system`, `user`, and `tool` roles) rather than concatenating flat text. 
- **Associated Risk:** If system instructions and untrusted inputs are combined without clear boundaries, the LLM cannot distinguish between developer commands and attacker commands, making direct prompt injection trivially easy.

### 3. Indirect Prompt Injection (IPI) Defense
- **Question:** How does the system handle and sanitize untrusted content retrieved autonomously by tools (e.g., summarizing a webpage, reading an uploaded PDF, querying a third-party API)?
- **Recommended Control:** Treat all tool-retrieved data as highly untrusted. Implement a "Dual-LLM" architecture where a lower-privileged, isolated LLM sanitizes, summarizes, or extracts data from the external source *before* passing the clean data back to the primary, high-privileged executing agent.
- **Associated Risk:** An attacker can hide an invisible prompt injection payload on a public website or within a seemingly benign document. When the agent's tool fetches this data, the hidden payload executes ("Indirect Prompt Injection"), turning your agent into a confused deputy acting on behalf of the attacker.

### 4. Output Guardrails & Anomaly Detection
- **Question:** What controls are in place to monitor the LLM's output to detect if a prompt injection attempt was successful, even if it bypassed input filters?
- **Recommended Control:** Implement strict output validation. Scan responses for policy violations, toxicity, or the accidental leakage of the system prompt (Prompt Leaking). If the agent is calling a tool, use deterministic validation (e.g., strict JSON schema matching) to ensure the LLM hasn't been manipulated into writing executable code or malformed arguments.
- **Associated Risk:** If an injection succeeds, the lack of output validation allows the attacker to successfully exfiltrate internal system architecture details, return malicious phishing links to an end-user, or execute malformed tool calls.

### 5. Session Context & Memory Poisoning Prevention
- **Question:** How is the agent's memory (e.g., conversational history or vector database context) protected against persistent prompt injections that could span across multiple sessions or users?
- **Recommended Control:** Scope vector database retrievals strictly to the authenticated user's tenant/identity (RAG access control). Limit conversational memory windows, and periodically flush or summarize chat history using a sanitized process to prevent a malicious payload from persisting indefinitely in the agent's context window.
- **Associated Risk:** An attacker might inject a payload that doesn't trigger immediately but is stored in the agent's memory or a shared RAG database (Data Poisoning). When the agent recalls this memory later—potentially during a different user's session—the payload activates, causing a delayed and difficult-to-trace compromise. 


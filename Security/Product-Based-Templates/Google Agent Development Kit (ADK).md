The **Google Agent Development Kit (ADK)** is an open-source, code-first framework designed by Google to build, evaluate, debug, and deploy intelligent, enterprise-grade AI agents and multi-agent systems. 

Released to make AI agent development feel like structured software engineering, ADK provides developers with deterministic control, graph-based workflow orchestration, and native multi-modal capabilities. While optimized for the Google Cloud ecosystem and Gemini models, ADK is fundamentally **model-agnostic**, **deployment-agnostic**, and cross-language (supporting Python, TypeScript, Go, Java, and Kotlin).
(https://adk.dev/)

---

### Why Google ADK?
Traditional LLM wrappers or simple chatbots often struggle when handling complex, multi-step business logic. ADK bridges this gap by letting developers weave **adaptive AI reasoning** (where the model figures out what to do) together with **deterministic code** (rigid rules, loops, and routing that must execute reliably every time).

---

### How Does Google ADK Work? (Core Architecture)

At the heart of ADK is a modular execution pipeline built around several foundational components:

#### 1. The `Agent` (Reasoning Engine)
The basic building block of ADK is the `Agent` class (often defined as an `LlmAgent`). You configure an agent by defining:
*   **Model:** The underlying LLM driving the reasoning (e.g., `gemini-2.5-flash`, GPT, Claude).
*   **Instructions:** System prompts and role constraints.
*   **Tools:** Functions, APIs, search capabilities, or databases the agent can autonomously call to interact with the outside world.

```python
from google.adk import Agent
from google.adk.tools import google_search

researcher = Agent(
    name="researcher",
    model="gemini-2.5-flash",
    instruction="You help users research topics thoroughly and summarize facts.",
    tools=[google_search]
)
```

#### 2. Workflows & Graph Orchestration
Instead of letting a single LLM attempt to solve a massive problem autonomously (which risks hallucinations or infinite loops), ADK introduces **Workflows**. Workflows use a graph-based execution engine that arranges agents into structured pipelines:
*   **Sequential / Routing:** Pass the output of Agent A (e.g., data extraction) into Agent B (e.g., formatting/summarization).
*   **Fan-out / Fan-in (Parallel):** Run multiple specialist agents simultaneously and merge their results.
*   **Loops & Retries:** Automatically retry a tool call or re-prompt an agent if validation fails.
*   **Human-In-The-Loop (HITL):** Pause the graph execution at specific nodes to require manual human approval before proceeding.

#### 3. Task API & Multi-Agent Collaboration
ADK embraces a **Multi-Agent System (MAS)** design pattern where specialized sub-agents collaborate. Through ADK's **Task API** and Agent-to-Agent (A2A) protocol mechanisms, a root "Orchestrator Agent" can delegate distinct tasks to specialist sub-agents (e.g., a Database Agent, a Web Research Agent, and a Copywriter Agent). Each sub-agent operates within its own strictly defined scope and memory context.

#### 4. Runner, Services, & Session State
To execute an agent, ADK uses a **Runner** coupled with an event loop. The Runner manages stateful interactions through session services:
*   **Contextual Memory:** Tracks conversation history and intermediate outputs across turns.
*   **Artifacts:** Handles multi-modal outputs (like generated PDFs, images, or structured JSON objects) created during execution.

---

### The Development and Deployment Lifecycle

Google ADK streamlines the end-to-end engineering journey:

1.  **Local Scaffolding & Prototyping:** Using the **Agents CLI** (`adk run`), developers can scaffold agent projects locally in minutes.
2.  **Visual Debugging (`adk web`):** Instead of parsing terminal logs, ADK ships with a built-in local web UI. Developers launch `adk web` in their terminal to visualize the agent's live step-by-step execution graph, inspect memory states, and debug tool calls.
3.  **Evaluation & Tracing:** ADK includes testing frameworks allowing developers to run deterministic unit tests on agent trajectories to evaluate safety, accuracy, and tool-use precision before pushing to production.
4.  **Enterprise Deployment:** Because ADK decouples the logic from the infrastructure, agents can easily be containerized and deployed to cloud environments like **Google Cloud Run**, **Google Kubernetes Engine (GKE)**, or managed platforms like **Vertex AI / Gemini Enterprise Agent Platform**.


Here is the unified, authoritative security guidance combining both the cloud-scale architectural framework and the code-level implementation best practices from Google’s official ADK safety documentation (`adk.dev/safety`).

---

# Security Guidance for Google Agent Development Kit (ADK)

As AI agents transition from conversational wrappers to autonomous systems that execute tools, modify databases, and collaborate via Agent-to-Agent (A2A) protocols, security must evolve from simple prompt engineering to robust systems engineering. Securing agents built with the **Google Agent Development Kit (ADK)** requires defense-in-depth across seven distinct layers.

---

## Layer 1: Identity, Authentication, and Access Control

Because ADK agents autonomously execute tools and fetch data across external systems, rigid authentication models are required to prevent privilege escalation and data breaches. 

The identity that a tool uses to perform actions on external systems is a foundational security design consideration. Crucially, **different tools within the exact same agent can be configured with different authentication strategies**. Care must be taken when defining tool-level identity configurations to ensure the agent operates under the Principle of Least Privilege.



### 1. Core Authentication Strategies: User-Auth vs. Agent-Auth

#### User-Auth (Controlling User Delegation)
The tool interacts with external systems using the identity of the "controlling user" (i.e., the human interacting with the frontend web application). In Google ADK, this is typically implemented using **OAuth delegation**: the agent interacts with the frontend to acquire an OAuth user token, and the tool uses that token when executing downstream API or database actions. The external system only authorizes the action if the controlling user is permitted to perform it on their own.

*   **When to Use:** Mandatory whenever an agent accesses personal, tenant-specific, or user-specific data (e.g., reading emails, updating personal calendars, querying a user's account history or billing records).
*   **Security Advantage:** Greatly reduces the risk of data exfiltration because the agent is physically restricted to performing only the actions the end-user could have performed themselves.
*   **Operational Caveat (Scope Creep):** Most common implementations of OAuth delegation rely on fixed sets of permissions (OAuth scopes). Often, these scopes are broader than the specific access the agent tool actually requires (e.g., an agent needing to read a single calendar event might inherit a broad `calendar.readwrite` scope). Therefore, User-Auth must still be complemented by in-tool programmatic guardrails to further constrain agent behavior.

#### Agent-Auth (System Identity)
The tool interacts with external systems using the agent's own corporate identity (e.g., a Google Cloud Service Account, managed identity, or application API key). The agent identity must be explicitly authorized in external system access policies—for example, adding the agent's service account to a Cloud SQL IAM policy for read access. 

*   **When to Use:** Appropriate *only* when querying global, shared, or non-personal data where all users share the exact same level of access (e.g., public weather APIs, corporate product catalogs, standard operating procedures), or when executing autonomous background tasks where no active user session exists.
*   **Security Advantage (Infrastructure Constraints):** By configuring IAM policies at the resource level, you constrain the agent to only performing actions intended by the developer. If you grant an agent's service account read-only permissions to a database, no matter what an LLM decides or hallucinates, the database engine will prohibit the tool from performing write or delete actions.
*   **Mandatory Attribution Logging:** When using Agent-Auth, all external actions appear in downstream audit logs as coming from the single service account. To maintain accountability, your tool implementation **must generate strict internal audit logs** that correlate and attribute the agent's system-level actions back to the specific controlling user who prompted the execution.

---

### 2. Preventing the "Confused Deputy" Problem (Row-Level Security)
If not all users share the same level of access, Agent-Auth alone does not provide enough protection. If you grant an agent a global service account that has read access to a multi-tenant database, a malicious prompt injection can trick the probabilistic LLM into fetching another user's records—turning the agent into a "Confused Deputy."

*   **Never trust the LLM with tenant IDs:** Always enforce strict row-level security. Never let the LLM supply `user_id` or `tenant_id` parameters to tools. Do not define tool signatures like `get_orders(user_id)`.
*   **Deterministic Injection:** Define the tool signature simply as `get_my_orders()`. Inside the backend Python tool implementation, inject the verified user identity deterministically directly from the secure application session context (`tool_context.session`). 
*   **Database-Level Enforcement:** For best security policy, avoid using global service accounts for multi-tenant databases entirely. Push row-level enforcement down to the database engine via User-Auth token delegation or native database Row-Level Security (RLS) session variables.

---

### 3. Session State Credential Isolation
Never store OAuth user tokens, refresh tokens, API keys, or raw credentials inside ADK’s `session.state` dictionary. 

Depending on the application's architecture, session state may be serialized, persisted, logged for debugging or evaluation, or shared across multiple agents participating in a workflow. Storing secrets in session state unnecessarily expands their exposure and increases the risk of unintended disclosure through logs, traces, prompt injection, or prompt extraction attacks.

Instead, retrieve credentials dynamically from a dedicated Secret Manager or a secure in-memory credential store only at the point of tool execution. Limit the lifetime and scope of credential access according to the principle of least privilege.


---

## Layer 2: Architecture & Interception Guardrails (Inputs, Outputs, and Execution)

To control model and tool calls precisely, secure agent architectures must layer interception guardrails across every data transition. While built-in Gemini safety features (such as native content filters and system instructions) provide a baseline, enterprise agents require programmatic validation to screen user inputs, model outputs, and external tool execution requests.

---

### 1. The Architectural Choice: Callbacks vs. Runner-Level Plugins

Google ADK provides two primary mechanisms for intercepting agent execution. Selecting the correct level of abstraction is critical for maintaining consistency across complex multi-agent applications:

#### Per-Agent Callbacks (Agent-Specific Validation)
Callbacks (`before_model_callback`, `before_tool_callback`, `after_model_callback`) provide a simple, agent-specific method for adding pre-validation to tool and model I/O. 
*   **When to Use:** When modifying the underlying tool code isn't possible, the `before_tool_callback` can inspect requested tools and arguments against the agent's current state. While you can build reusable callback libraries, callbacks must be manually attached to individual agents, and they may fall short if the context required to enforce the policy isn't directly visible within the tool parameters.

#### Runner-Level Plugins (Recommended for Enterprise Policies)
When implementing security policies that apply across multiple agents, **plugins (subclassing `BasePlugin`) are the recommended architectural approach**. Plugins are self-contained, modular, and registered directly at the global `Runner` level.
*   **Why:** A security plugin configured once on the Runner automatically enforces screening across **every agent and sub-agent** executing within that runtime. This eliminates repetitive code and prevents coverage gaps where a developer might forget to attach a callback to a newly added sub-agent.

---

### 2. Built-in ADK Plugins vs. Enterprise Cloud Guardrails

Google ADK includes native plugins that can be deployed alongside enterprise Google Cloud security services. Understanding the boundary between application-level plugins and API-driven cloud policies is essential:

#### PII Redaction Plugin vs. Sensitive Data Protection (SDP)
*   **ADK PII Redaction Plugin:** A specialized, built-in framework module designed specifically for the `before_tool_callback`. It provides localized, in-memory filtering at the agent level to redact Personally Identifiable Information (PII) right before arguments are processed by a tool or transmitted to an external service.
*   **Cloud Sensitive Data Protection (SDP):** While the ADK plugin is specific to application callbacks, Google Cloud’s Sensitive Data Protection (often delivered via Model Armor) provides a centralized, API-driven governance policy. SDP applies consistent enterprise-wide de-identification, masking, and cryptographic tokenization uniformly across all cloud runtimes and agents.

---

### 3. The "Sandwich Defense": Model Armor & Content Shielding

To defend against adversarial manipulation and data exfiltration, wrap your primary reasoning model in a bidirectional shield using built-in or custom plugins:

*   **Input Shield (Model Armor Plugin):** A plugin that queries the Google Cloud Model Armor API at specified execution points before payloads reach the LLM. It screens user inputs for prompt injections, adversarial phrasing, and jailbreak attempts. If Model Armor identifies harmful content or policy violations, the plugin halts execution immediately and returns a safe, predetermined fallback response.
*   **Output Shield:** Integrates Sensitive Data Protection and output screening on model responses and tool return data to intercept and redact regulated PII, secrets, or sensitive intellectual property before returning the final response to the user.

---

### 4. Semantic Screening: Secondary LLMs as Guardrails

Because static regex filters and standard signature detection cannot catch every semantic nuance of an attack, ADK supports deploying a secondary AI model to evaluate agent trajectories.

#### Gemini as a Judge Plugin
Implement an independent semantic guardrail using a fast, highly economical model (such as **Gemini Flash Lite**) configured via callbacks or Runner plugins. 

*   **How it works:** The plugin passes the raw user input, tool inputs/outputs, and intermediate model responses to Gemini Flash Lite, which acts as an independent safety evaluator. 
*   **What it detects:** The secondary model helps screen for subtle indirect prompt injections hidden in tool return payloads, sophisticated jailbreaks, brand safety risks, and general agent misalignment. 
*   **Enforcement:** If the "judge" model decides the input or execution path is unsafe, it blocks the primary agent from continuing and returns a predetermined response to the user: *"Sorry, I cannot help with that. Can I help you with something else?"*

----

### 5. Native Model Safety Foundations (Built-in Gemini Filters & Instructions)
Before layering custom code plugins or external API proxies, secure ADK deployments must first enable and configure the native safety mechanisms baked directly into Gemini models on the Agent Platform. These built-in features act as the foundational line of defense against harmful content and prompt jailbreaks.

#### A. Layered Content Safety Filters
Safety filters operate as a separate moderation layer in the generation pipeline, evaluating input and output streams against strict safety boundaries:
*   **Non-Configurable Filters:** Always-on, mandatory baseline filters that automatically block illegal or highly harmful outputs, such as Child Sexual Abuse Material (CSAM) and severe Personally Identifiable Information (PII) leakage.
*   **Configurable Filters:** By default, configurable thresholds are turned off. Developers must explicitly define blocking thresholds (`LOW_AND_ABOVE`, `MEDIUM_AND_ABOVE`, `ONLY_HIGH`, or `OFF`) across four core harm categories: **Hate Speech**, **Harassment**, **Sexually Explicit**, and **Dangerous Content**.

```python
from google.adk.agents import Agent
from google.genai import types

# Configure foundational Gemini content filters inside the ADK Agent
agent = Agent(
    name="customer_support_agent",
    model="gemini-2.5-flash",
    instruction="Assist customers with general account inquiries.",
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            ),
        ],
    ),
)
```

#### B. System Instructions for Safety and Brand Alignment
System instructions establish explicit behavioral guardrails and boundary markers before the agent processes user turns. Well-crafted system prompts should proactively define:
*   **Prohibited & Sensitive Topics:** Explicitly enumerating domains the agent must decline to discuss (e.g., medical diagnoses, financial advice, competitor comparisons).
*   **Brand Safety & Voice:** Establishing strict guidelines regarding tone, values, and mandatory legal disclaimers to ensure model outputs do not cause reputational damage.

#### Architectural Caveat: The Need for Defense-in-Depth
While native content filters and system instructions are robust against generating toxic text or standard jailbreaks, **they are insufficient on their own**. Probabilistic system prompts cannot guarantee tool safety or stop indirect prompt injections embedded in external data. Therefore, native Gemini safety features must act solely as the foundational baseline, reinforced by the deterministic programmatic layers (Runner Plugins, Model Armor, and In-Tool Guardrails) detailed below.

---

## Layer 3: Tool Execution & Excessive Agency Mitigation

The highest security risk in autonomous AI agents stems from what external tools execute. To prevent excessive agency and protect downstream systems, developers must establish rigid, code-enforced boundaries rather than relying on probabilistic LLM system prompts. 

---

### 1. In-Tool Deterministic Guardrails (Code over Prompts)
Tools should be designed defensively from the ground up: expose only the exact actions you want the model to take, eliminating entire classes of rogue actions deterministically.

Do not rely on natural language system instructions (e.g., *"Do not refund more than $50"*) to enforce business logic. Instead, rely on the fact that ADK tools receive two distinct types of input:
1.  **Arguments:** Probabilistic parameters generated by the LLM.
2.  **Tool Context:** Deterministic configuration and session data set explicitly by the developer (in TypeScript, this corresponds to the unified `Context` type).

By validating probabilistic model arguments against the deterministically set `Tool Context`, you guarantee the agent operates within hard boundaries outside the model's control:

```python
from google.adk.tools import ToolContext, PolicyViolationError

def issue_refund(amount: float, context: ToolContext) -> str:
    # Deterministic guardrail executed completely outside LLM control
    max_limit = context.get_developer_limit("max_refund")
    
    if amount > max_limit:
        raise PolicyViolationError(f"Refund of ${amount} exceeds automated approval limit.")
    ...
```

---

### 2. Sandboxed Code Execution (Hermetic Environments)
Code execution is a specialized tool that introduces severe security implications. If an agent dynamically generates and executes code (such as performing data analysis via a Python interpreter), sandboxing is mandatory to prevent compromise of the local runtime and uncontrolled network scanning.

#### Official Google & ADK Managed Options
*   **Server-Side Execution:** Enable the `tool_execution` tool via the Vertex Gemini Enterprise API to run model-generated code in Google's secure, cloud-hosted sandboxes.
*   **Data Analysis:** Use ADK’s built-in **Code Executor tool** configured to call the managed Vertex Code Interpreter Extension.

#### Custom Code Executor Mandates
If building a custom execution environment using ADK building blocks, the sandbox **must be hermetic**:
*   **Zero Network Egress:** Block all outbound network connections and external API calls inside the sandbox to prevent Server-Side Request Forgery (SSRF) and data exfiltration.
*   **Ephemeral State Cleanup:** Enforce complete data and disk cleanup across execution turns to eliminate cross-user data exfiltration vulnerabilities.

---

### 3. Human-in-the-Loop (HITL) Controls
For high-impact, destructive, or irreversible operations (e.g., dropping database tables, wiring funds, or deleting user records), configure the ADK workflow to safely halt execution and require explicit, out-of-band human authorization before contacting external APIs.

#### Mechanism A: Action Confirmations (`require_confirmation=True`)
ADK tools (such as `FunctionTool`) support built-in confirmation flags. When triggered, the runtime intercepts the tool execution request and pauses execution. It supports two modes:
*   **Boolean Confirmation:** Pauses execution to request a simple Yes/No authorization from a human operator or supervising system.
*   **Advanced Payload Confirmation:** Pauses execution and mandates that the human user review and submit validated, structured payload parameters before the tool is allowed to proceed.

#### Mechanism B: Graph-Based HITL Nodes (`RequestInput`)
In multi-agent or dynamic graph workflows, developers can insert dedicated human input nodes using the `RequestInput` class:
```python
yield RequestInput(
    message="Please confirm database deletion.", 
    response_schema=ConfirmationSchema
)
```
When graph execution hits this node, the framework safely suspends run state (raising an internal interrupt such as `NodeInterruptedError`) and persists execution context until explicit human input is received.

---

### 4. Strict Schema Validation
Treat the LLM generating tool arguments as an untrusted, external client. To ensure hallucinated parameters or injection payloads cannot cause malformed execution errors or downstream vulnerabilities, ADK enforces strict runtime parameter validation.

*   **Pydantic Schema Enforcement:** ADK Python uses **Pydantic models** (`BaseModel` and `Field`) as its native source of truth for schema validation. When defining tools or structured output agents (`output_schema`), developers declare explicit Pydantic classes containing strict type definitions, regex patterns, and parameter boundaries.
*   **Runtime Interception:** When an agent attempts to invoke a tool, the ADK runtime automatically intercepts the incoming JSON payload and validates it against the compiled Pydantic schema *before* downstream tool logic is executed. Arguments that violate the declared schema—such as incorrect types, missing required fields, or values outside declared constraints—are rejected before tool execution.


---

### 5. Delegation & Transfer Restrictions (Constraining Multi-Agent Autonomy)
In multi-agent systems, excessive agency can manifest not just through external tool executions, but through unconstrained, autonomous delegation *between* agents. If left unconstrained, a compromised or hallucinating sub-agent could attempt to laterally invoke unauthorized peer agents or escalate execution control back up to a more privileged parent agent.

To eliminate unnecessary agent autonomy and enforce a strict, predictable routing hierarchy, Google ADK provides explicit configuration flags that restrict LLM-controlled control flow:

*   **`disallow_transfer_to_parent=True`:** Prevents a sub-agent from dynamically passing execution control back up to its parent orchestrator. This stops potential privilege escalation (where a restricted sub-agent tricks a parent into running a high-impact tool) and eliminates recursive, infinite feedback loops.
*   **`disallow_transfer_to_peers=True`:** Blocks an agent from initiating lateral handoffs to sibling or peer agents. This ensures that agent collaboration follows strict, developer-defined deterministic workflow graphs rather than probabilistic LLM routing choices.

```python
from google.adk import Agent

# Restrict excessive agency by locking down autonomous transfer pathways
restricted_sub_agent = Agent(
    name="restricted_researcher",
    model="gemini-2.5-flash",
    instruction="Analyze the provided text. Do not delegate tasks.",
    tools=[search_tool],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)
```
---

## Layer 4: Multi-Agent System (A2A) & Graph Orchestration Security

As AI architectures evolve from single-model chat wrappers into complex Multi-Agent Systems (MAS), security must shift from defending a single point of entry to managing **distributed execution boundaries**. 

Whether you are building in-process graph workflows using ADK primitives (`ParallelAgent`, `SequentialAgent`, `LoopAgent`) or delegating tasks across distributed environments via the **Agent-to-Agent (A2A) Protocol**, every sub-agent introduces potential lateral attack vectors. Securing multi-agent orchestration requires applying strict Zero-Trust principles internally across the workflow hierarchy.

---

### 1. Zero-Trust Sub-Agent Boundaries (`AgentTool` Interception)
In hierarchical multi-agent designs, specialist sub-agents often interact with untrusted external environments (e.g., a "Web Research Sub-Agent" scraping public web pages). If an external webpage contains an **Indirect Prompt Injection**, the compromised sub-agent could return adversarial payloads designed to hijack the root "Orchestrator Agent."

To prevent cascading compromise, treat every sub-agent as an untrusted client:
*   **The Delegation Boundary:** In ADK, delegating execution to a specialist sub-agent is wrapped inside an `AgentTool`. This means multi-agent delegation functions natively as a tool execution boundary.
*   **Payload Sanitization (for ADK(python) 2.3.0):** By ensuring `include_plugins=True` (ADK's default setting on `AgentTool`), Runner-level security plugins and `after_tool_callback` hooks fire at the exact moment the sub-agent finishes its execution. This allows your security layer (e.g., Cloud Model Armor or an output screening plugin) to intercept, inspect, and sanitize the raw return data *before* it is ingested into the root orchestrator's reasoning context or shared session memory.

---

### 2. Micro-Scoping & Hierarchical Least Privilege
When structuring multi-agent trees, never expose a global tool pool across the workflow graph. Specialist sub-agents must be strictly micro-scoped through **modular encapsulation**:
*   **Explicit Tool Isolation:** When defining a specialist sub-agent, explicitly pass only the minimal domain-specific array to its `tools=[...]` parameter. 
*   **Preventing Privilege Inheritance:** A copywriting or external research sub-agent should operate strictly inside its local sandbox. By isolating tool arrays, even if an attacker successfully jailbreaks a public-facing research sub-agent, the agent is physically incapable of executing infrastructure writes, database drops, or financial transactions because those tools exist exclusively within a separate, isolated sub-agent's memory space.

---

## Layer 5: Network Controls & Exfiltration Prevention

Because autonomous AI agents dynamically generate and execute tool requests across external APIs and internal infrastructure, they introduce severe network-level attack vectors. Without strict network isolation, an agent tricked by a prompt injection can be weaponized to scan internal networks or exfiltrate sensitive data.

### 1. Coarse Infrastructure Perimeters: VPC Service Controls (VPC-SC)
Confine your ADK execution runtime (e.g., Google Cloud Run, Google Kubernetes Engine, or the Gemini Enterprise Agent Platform) within strict **VPC Service Control (VPC-SC)** perimeters. 
*   **How it protects:** Executing your agent inside a VPC-SC perimeter guarantees that cloud API calls can only manipulate resources inside that trusted boundary. If an attacker attempts to trick the agent into writing sensitive session data to an external, attacker-controlled Cloud Storage bucket or database, the VPC-SC perimeter blocks the API call at the network layer, dramatically reducing the risk of data exfiltration.

### 2. Strict Egress Allowlisting
Never allow an agent runtime to have unrestricted internet access (`egress 0.0.0.0/0`). Implement strict network firewall rules that deny all outbound traffic by default, explicitly allowlisting only the exact external API hostnames and IP ranges authorized for your agent's specific tool usage.

### 3. Architectural Caveat: Why Network Perimeters Are Not Enough
While VPC-SC and IAM identities provide robust infrastructure security, **they only provide coarse, macro-level controls around agent actions**. 

If an agent has legitimate access to two internal databases within the same VPC-SC perimeter, the perimeter cannot stop the agent from reading sensitive records from Database A and improperly copying them into Database B. Therefore, macro-level network controls must always be complemented by application-level **tool-use guardrails** (Layers 2 and 3), giving developers fine-grained, deterministic control over exactly which actions an agent is permitted to execute.


---

## Layer 6: Frontend & Presentation Security

Security extends all the way to the UI browser where agent responses are rendered.

*   **UI Sanitization (XSS Defense):** AI agents frequently ingest unstructured external web content, format it, and return Markdown, HTML, or code blocks. **Always escape and sanitize model-generated content** before rendering it in web dashboards or client apps. Failure to escape outputs opens direct vectors for DOM-based Cross-Site Scripting (XSS).

---

## Layer 7: Observability, Evaluation, and Runtime Protection

Because Large Language Models are probabilistic reasoning engines, securing an AI agent is not a static, set-and-forget deployment. A prompt injection or behavioral drift might bypass static input guardrails, meaning security must extend across the entire lifecycle: **pre-deployment testing**, **live production observability**, and **active runtime interception**.

---

### 1. Pre-Deployment Adversarial Evaluation (TDD for Agents)
Before deploying code to production, you must treat your agents to the same rigor as traditional software development by implementing **Test-Driven Development (TDD)** for AI workflows. 

Integrate ADK’s built-in evaluation framework (`adk eval` / `AgentEvaluator`) directly into your CI/CD pipelines to continuously run automated red-team regressions against libraries of known prompt injections, jailbreaks, and edge cases. ADK ships with native evaluation criteria specifically built to measure safety and tool-use boundaries:
*   **`safety_v1`:** Delegates evaluation to the Vertex AI Agent Platform Eval SDK to act as an LLM judge, automatically verifying that agent trajectories do not contain harmful content, toxicity, or compliance failures.
*   **`rubric_based_tool_use_quality_v1`:** Evaluates whether the agent selected the appropriate tools, passed validated parameters, and adhered to developer-defined behavioral rubrics—catching instances of excessive agency before they reach production.
*   **`hallucinations_v1`:** Verifies that model outputs are strictly grounded in factual data returned by external tools rather than fabricated claims.

---

### 2. End-to-End Tracing & Audit Logging (OpenTelemetry)
You cannot secure or conduct forensic investigations on what you cannot observe. Google ADK is built natively on **OpenTelemetry (OTel)** instrumentation to provide complete transparency into agent execution graphs.

By enabling telemetry flags (`--otel_to_cloud` via CLI or configuring `TelemetryConfig.captureMessageContent = true` in your code), the ADK Runner emits structured traces across every node of an execution workflow:
*   **Logging the "Chain of Thought":** Traces capture the agent's internal reasoning trajectory, exact tool selection order, and latency across sub-agent handoffs.
*   **Forensic Auditing:** Captures the exact JSON input arguments passed into tools and the raw return payloads received from external APIs. 
*   **Enterprise Integration:** Spans export natively into Google Cloud Trace, Datadog LLM Observability, AgentOps, or Freeplay, creating immutable audit trails that allow security analysts to reconstruct the exact anatomy of a security incident or Confused Deputy attack.

---

### 3. Active Runtime Interception & GenAI Firewalls
While `adk eval` protects your CI/CD pipeline against *known* attack patterns, live production environments face zero-day prompt injections and dynamic adversarial manipulation. Production runtimes require active, real-time defense layers capable of intercepting anomalous execution paths mid-flight:

*   **Native Framework Interception:** Register global security plugins (like the `Model Armor Plugin` or custom screening plugins) directly to the ADK `Runner`. As the agent executes multi-step workflows, the plugin evaluates checkpoints in real time; if an indirect prompt injection succeeds in tricking a sub-agent mid-workflow, the Runner plugin intercepts the execution state, safely terminates the graph, and returns a safe fallback response.
*   **External GenAI Firewalls:** Leverage ADK's open telemetry and API boundaries to route live traffic through external AI runtime security proxies (such as dedicated GenAI firewalls). These external layers monitor live execution graphs to detect policy drift, anomalous tool loops, or unauthorized lateral data transfers, automatically severing compromised sessions before data exfiltration occurs.

---







# References:
Official Documentation for Human-in-the-Loop (HITL) Controls:
Action confirmations - Agent Development Kit (ADK)(https://adk.dev/tools-custom/confirmation/)   
Human input - Agent Development Kit (ADK)(https://adk.dev/graphs/human-input/)  
Dynamic workflows - Agent Development Kit (ADK)(https://adk.dev/graphs/dynamic/)
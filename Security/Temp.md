Here is the expanded, highly detailed rephrasing of **Layer 7**, incorporating exact architectural mechanisms, native telemetry primitives, built-in evaluation criteria, and runtime protection strategies from official Google ADK documentation:

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
*   **External GenAI Firewalls:** Leverage ADK's open telemetry and API boundaries to route live traffic through external AI runtime security proxies (such as Cisco AI Defense, Datadog monitoring, or dedicated GenAI firewalls). These external layers monitor live execution graphs to detect policy drift, anomalous tool loops, or unauthorized lateral data transfers, automatically severing compromised sessions before data exfiltration occurs.

---

### Architectural Lifecycle Implementation

```python
from google.adk.agents import Agent
from google.adk.evaluation import AgentEvaluator
import google.adk.telemetry as telemetry

# 1. Enable full OpenTelemetry capturing for forensic Chain-of-Thought auditing
telemetry.configure(
    enable_cloud_trace=True,
    capture_message_content=True # Captures exact tool I/O payloads for security logs
)

# 2. Define the Agent under observation
production_agent = Agent(
    name="financial_assistant",
    model="gemini-2.5-pro",
    instruction="Assist with account summaries. Adhere strictly to tool boundaries.",
    tools=[get_account_balance]
)

# 3. CI/CD Automated Regression Testing (Executed pre-deployment via `adk eval`)
def run_cicd_safety_evaluations():
    evaluator = AgentEvaluator(agent=production_agent)
    results = evaluator.evaluate(
        test_dataset="gs://my-secure-bucket/red_team_jailbreak_suite.json",
        criteria=[
            "safety_v1",                     # Evaluates against jailbreaks & toxicity
            "rubric_based_tool_use_quality_v1", # Verifies agent didn't abuse tool access
            "hallucinations_v1"              # Ensures grounding in factual tool returns
        ]
    )
    assert results.passed, "Agent failed security regression evaluation!"
```
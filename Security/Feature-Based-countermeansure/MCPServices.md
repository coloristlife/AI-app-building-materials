

Here is the dedicated section for your Security Architecture Questionnaire focused explicitly on the **Business-Line MCP Servers**. 

To properly evaluate the backend, you must understand the *nature of the tools* exposed, the *flow of the data* back to the AI, and the *exact boundaries of multi-tenancy*. 

You should append this section to your security review document as **Phase 3**. As with previous sections, I have included the **✅ Preferred / Expected Answers** to serve as your evaluation rubric.

---

### **Phase 3: Business-Line MCP Server Security & Tool Execution**
*This section evaluates the security posture of the downstream federated servers, focusing on tool capabilities, output handling, and data isolation.*

#### **3.1. Tool Capabilities & Function Exposure**
*Before assessing the risk of a backend server, we must establish exactly what it is capable of doing.*

*   **Question:** Please provide a manifest or categorization of all functions/tools provided by this specific MCP server. Specifically, which tools are **Read-Only** (e.g., `get_user_profile`, `query_financial_status`) and which are **State-Changing / Destructive** (e.g., `update_database`, `trigger_deployment`, `send_email`)?
*   **✅ Preferred Answer:** The engineering team provides a strict schema (e.g., JSON Schema used by the MCP protocol) mapping all tools. State-changing tools are heavily restricted, segmented from read-only tools, and require explicitly elevated scopes (`scp`) or step-up authentication to execute. 

#### **3.2. Output Consumption & Agent Chaining (Indirect Prompt Injection Risk)**
*LLMs are highly vulnerable to Indirect Prompt Injection. If an MCP server returns malicious or poisoned data, the AI Agent might execute unintended actions.*

*   **Question:** How is the output of each MCP server consumed by the AI Agent? 
    *   **Pattern A (Aggregation):** Is the output strictly returned to the AI agent's context window solely to be summarized and presented to the human end-user?
    *   **Pattern B (Tool Chaining):** Is the AI agent permitted to autonomously take the output from *this* tool and use it as the input argument for a *different* tool on another MCP server?
*   **✅ Preferred Answer:** 
    *   *For Pattern A:* The output is sanitized (e.g., HTML/Markdown escaping, PII masking) before being sent back to the LLM to prevent the LLM from executing hidden malicious instructions embedded in the data.
    *   *For Pattern B (Highest Risk):* If tool chaining is allowed, there is a strict "Human-in-the-Loop" (HITL) approval step before the AI agent can pass data retrieved from Tool A into a state-changing Tool B. 

#### **3.3. Multi-Tenancy Architecture (Gateway vs. Server Level)**
*We must clarify exactly where the multi-tenant boundaries are drawn to evaluate the risk of Cross-Tenant Data Leakage (BOLA/IDOR).*

*   **Question:** Please clarify the definition of "multi-tenant" for this specific backend integration. 
    *   **Model 1 (Physical Isolation):** Does the Gateway route traffic to physically separate, single-tenant instances of this business-line MCP server (e.g., `finance-server-tenantA` and `finance-server-tenantB`)?
    *   **Model 2 (Logical Isolation):** Or, is the business-line MCP server itself a massive, shared application connecting to a multi-tenant database?
*   **✅ Preferred Answer:** 
    *   *If Model 1 (Preferred for High Security):* Physical isolation is confirmed. The MCP server for Tenant A literally does not possess the database credentials to read Tenant B's data. 
    *   *If Model 2 (Acceptable but High Risk):* The architecture relies on Logical Isolation. *(If Model 2, proceed immediately to question 3.4).*

#### **3.4. Backend Tenant Enforcement (For Logically Multi-Tenant Servers)**
*If the backend server is shared among all tenants, we must verify that it doesn't blindly trust the AI Agent's requested parameters.*

*   **Question:** If the business-line MCP server is logically multi-tenant, how does it enforce tenant boundaries at the data layer? When the AI agent requests data (e.g., `get_invoice(id=12345)`), how does the backend guarantee that Tenant A's AI agent cannot retrieve Tenant B's invoice?
*   **✅ Preferred Answer:** The backend MCP server **completely ignores** any tenant identifiers provided in the AI agent's JSON tool arguments. Instead, the backend server extracts the cryptographically verified `tenant_id` from the exchanged Okta JWT (or AWS IAM context) injected by the Gateway. It then forcibly appends `AND tenant_id = 'A'` to every underlying database query or API call at the ORM/Data layer. 

#### **3.5. Payload & Resource Exhaustion (DoS Protection)**
*Because AI Agents can generate massive payloads or request enormous datasets, the backend must protect itself from memory exhaustion.*

*   **Question:** What limits are enforced on the size of the data *returned* by the MCP tools? If the AI agent issues a poorly optimized tool call (e.g., `get_all_logs(limit=10_000_000)`), how does the business-line server prevent crashing or blowing out the LLM's context window limits?
*   **✅ Preferred Answer:** The MCP server strictly enforces hard pagination, maximum payload limits (e.g., 2MB max response size), and query timeouts. If a tool requests too much data, the server returns a graceful error (`413 Payload Too Large` or an MCP protocol equivalent) instructing the AI agent to refine its query with smaller limits.

---

### **How to Frame This to the Engineering Team:**
When presenting this section, you can add this context note:

> *"Because the Gateway frontend is static and agnostic to the backend tool logic, the Business-Line MCP Servers represent the actual attack surface for Data Exfiltration and System Compromise. We need to clearly separate how tools are exposed, how the LLM consumes the data, and whether tenant isolation relies on shared databases or dedicated infrastructure."*

From AI

**Yes, absolutely.** This is one of the exact use cases for which AWS designed the **Amazon Bedrock AgentCore** suite. 

By combining **AgentCore Gateway** and **AgentCore Identity**, you can create a centralized, secure MCP proxy that uses token exchange to safely communicate with downstream MCP servers on behalf of a user or a workload.

Here is how the architecture works and how the specific components handle your use case:

### 1. The MCP Gateway: Bedrock AgentCore Gateway
AWS offers **AgentCore Gateway** to serve as your centralized managed MCP server (the "front door"). 
* **Native MCP Support:** It speaks the Model Context Protocol (MCP) natively, allowing AI agents or MCP-compatible clients to connect to it for tool discovery and invocation. 
* **Downstream Routing:** In late 2025, AWS explicitly added **"existing MCP servers"** as a supported target type for the Gateway. This means the Gateway can sit in front of dozens of downstream, specialized MCP servers (alongside AWS Lambdas or REST APIs) and aggregate them into a single, unified MCP interface for your agents.

### 2. Token Exchange & Auth: Bedrock AgentCore Identity
**AgentCore Identity** is the component that handles inbound and outbound authentication, making it the perfect engine for your token exchange requirements. 
* **Inbound Authentication:** When an MCP client makes a request to the AgentCore Gateway, it can be secured using a `CUSTOM_JWT` authorizer backed by an Identity Provider (IdP) like Amazon Cognito, Okta, Microsoft Entra ID, or even private VPC-hosted IdPs like Keycloak. AgentCore Identity automatically validates the incoming tokens.
* **Token Exchange & Outbound Auth:** AgentCore Identity natively supports complex OAuth 2.0 flows without exposing raw credentials to the LLM or the agent code. When the Gateway needs to route the request to a downstream MCP server, AgentCore Identity can perform a token exchange. It handles:
  * **OAuth Authorization Code Flow:** For user-delegated access, it orchestrates user consent and swaps tokens so the downstream MCP server receives a token specifically scoped to the user.
  * **Machine-to-Machine (M2M) / Client Credentials:** If the agent is acting autonomously, Identity manages the workload identity and injects the proper outbound API keys or OAuth tokens to the downstream MCP server.

### How it comes together
If you have multiple downstream MCP servers (for example, one for GitHub, one for an internal database, and one for Jira), you don't need to build a custom routing and token-exchange layer. 

Instead, you deploy an **AgentCore Gateway** as your unified MCP interface. You configure **AgentCore Identity** with your IdP. When your AI agent calls the Gateway with an initial JWT, AgentCore Identity steps in, validates the token, exchanges it for the correct scoped outbound tokens (via built-in token vaults and OAuth providers), and the Gateway securely routes the request to the specific downstream MCP server. 

This abstracts away the protocol-level complexities, allowing you to enforce tenant isolation and maintain strict audit trails outside of the LLM prompt or agent logic.
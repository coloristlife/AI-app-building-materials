Welcome to a crucial notebook in our series, focusing on the deployment and operational safety of AI agents. We will implement an Observability and Dry-Run Harness, an essential pattern for testing, debugging, and safely managing agents that interact with real-world systems.

The core principle is simple but powerful: never run an agent's action in a live environment without first knowing exactly what it's going to do. This architecture formalizes a "look before you leap" process. 
An agent first executes its plan in a dry_run mode, which doesn't change the real world but generates detailed logs and a clear plan of action. This plan is then presented to a human (or an automated checker) for approval before the final, live execution is permitted.

To demonstrate this, we will build a Corporate Social Media Agent. This agent is tasked with creating and publishing posts. We will see how the dry-run harness allows us to:

1. Generate a Proposed Post: The AI will creatively draft a post based on a prompt.
2. Perform a Dry Run: The agent will call the publish function in a sandboxed dry_run=True mode, generating logs of what would happen.
3. Human-in-the-Loop Review: A human operator is shown the exact post content and the dry-run trace. They must type approve to proceed.
4. Execute Live Action: Only upon approval is the publish function called again, this time with dry_run=False, to perform the real action.

This pattern is the bedrock of responsible agent deployment, providing the transparency and control needed to operate AI safely in production.

**When to Use / Applications**
- Debugging and Testing: In development, to understand exactly how an agent is interpreting a task and what actions it's taking without side effects.
- Production Validation & Safety: As a permanent feature in production for any agent that can modify state, spend money, send communications, or perform any other irreversible action.
- CI/CD for Agents: Integrating a dry-run harness into an automated testing pipeline to validate agent behavior before deploying new versions

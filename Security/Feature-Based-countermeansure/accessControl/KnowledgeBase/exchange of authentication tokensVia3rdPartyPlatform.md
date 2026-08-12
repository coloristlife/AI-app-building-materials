To securely acquire and store authorization tokens for integrated tools, the Integration Orchestration layer relies on **administrator-provisioned configurations** and **secure credential vaults**. 

The exchange of authentication tokens typically happens through one of two mechanisms, depending on the third-party platform's design:

### 1. Administrative Setup & Secret Management (Machine-to-Machine / Client Credentials)
For many underlying systems (such as HR tools like Workday or IT service desks like ServiceNow), the connection is established upfront by an enterprise administrator:
* **The Exchange:** The administrator registers the integration in the platform settings by supplying a **Client ID** and **Client Secret** (or service account credentials) obtained from the target third-party system's developer portal or admin console.
* **Token Retrieval:** The orchestration layer uses these static administrative credentials to execute a machine-to-machine exchange (such as an OAuth *Client Credentials Grant*) against the external platform's authorization endpoint (`/connect/token`). 
* **Storage:** The resulting short-lived access tokens and refresh tokens are stored securely in an encrypted secrets vault managed by the orchestration platform, allowing it to perform authorized actions seamlessly behind the scenes.

### 2. Delegated User Authorization (OAuth Authorization Code Flow)
When an action requires acting strictly on behalf of the individual user and respecting their specific data access boundaries:
* **Initial Consent Handshake:** During the initial setup or the first time a user triggers a specific tool, the integration layer initiates an OAuth flow. 
* **The Exchange:** The user authenticates with the external tool or grants consent via a secure redirect/popup. The external authorization server trades this consent for a user-specific access token and refresh token.
* **Secure Token Vaulting:** The orchestration layer binds these tokens to the user’s active session profile within a secure, encrypted token store, refreshing them automatically using refresh tokens so the user isn't prompted repeatedly.

### Summary
The credentials aren't magically guessed or harvested on the fly; they are strictly bootstrapped via **secure administrative provisioning (Client IDs/Secrets)** or **one-time user consent handshakes**, after which the orchestration layer maintains and rotates the active tokens securely in the background.
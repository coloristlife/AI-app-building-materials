

# Authentication and Authorization

**Employee authentication and authorization are the most critical parts of this entire process.** 

If the system only authenticated the *application* (Gemini) without authenticating the *employee* asking the question, it would create a massive security flaw known as the **"Confused Deputy Problem."** In that scenario, any employee could ask Gemini to read the CEO’s email, and because Gemini has access to Microsoft Graph, it would comply.

Here is exactly how the employee's authentication and authorization fit into the workflow:

### 1. Employee Authentication (Who are you?)
Before the employee even types the prompt, they must be securely logged into the Gemini Enterprise interface using their corporate identity (usually via Google Workspace/Cloud Identity, which is often tied to Microsoft Entra ID via Single Sign-On). 
* Because they are logged in, Gemini implicitly attaches a **User ID token** to their request. It knows exactly who is asking the question.

### 2. Employee Authorization (What are you allowed to see?)
How the employee's authorization is handled depends on the "Connector Mode" the IT team selected during setup:

**Scenario A: "Federated Search" (Real-time querying)**
If the connector is set to search Microsoft live, it uses something called **Delegated Permissions** (Identity Chaining). 
* When the Gemini connector knocks on Microsoft Graph’s door, it doesn't just say, *"I am Gemini, give me the calendar."* 
* It says, *"I am Gemini, and I am acting on behalf of employee John.Doe@company.com. Here is the cryptographic proof of his identity."* 
* **Microsoft Entra ID** then evaluates *both*: Is Gemini allowed to connect? AND is John Doe authorized to see this specific calendar? If John tries to ask for the CEO's calendar, Microsoft Graph denies the request because John's permissions do not allow it.

**Scenario B: "Data Ingestion" (Vector Database querying)**
If the connector is set to constantly sync emails into a Google Cloud Data Store in the background, it uses **Application Permissions**.
* In this mode, the Gemini connector syncs *everyone's* emails into the database. 
* To protect the data, Google Cloud applies **Document-Level Security (ACLs - Access Control Lists)** to the data store. 
* When John asks, *"What time is my meeting?"*, Gemini checks John's authenticated Google ID against the ACLs in the vector database. It filters the search so John can *only* retrieve vectors that originated from his own Microsoft inbox.

### Summary
Without the employee's authentication, the AI doesn't know whose data to retrieve. Without the employee's authorization being passed along (either to Microsoft Graph or to the Google Data Store's security filters), the system would violate "Least Privilege" and expose the entire company's communications to anyone using the chat interface.



# Connection Modes

The Trade-off:
While Data Ingestion is better for query privacy (and usually provides faster, higher-quality search results), it requires copying your massive Microsoft data repositories into Google Cloud storage, which introduces storage costs and means your data now resides in two different cloud providers. Federated Search is cheaper and easier to set up because the data stays exclusively in Microsoft, but it comes at the cost of sending your live search queries over to Microsoft's APIs.

https://medium.com/@mthammus/gemini-enterprise-microsoft-365-the-secure-broker-model-for-onedrive-outlook-and-sharepoint-7ad87a351b26



## 1. Overview

When building an AI chat or agent application, you usually do not want the user to wait until the entire AI response has been generated before displaying anything.

Instead, the application can stream information from the backend to the browser as it becomes available. This allows the user to see the AI response progressively and also makes it possible to display other real-time information, such as tool execution, agent progress, and errors.

A common technology used for this is **Server-Sent Events (SSE)**.

One important concept to understand is that **SSE does not replace HTTP**. SSE is a mechanism for sending a stream of events from the server to the client over an HTTP connection.

In other words, an AI application can still use a normal HTTP request to send the user's message to the server, while the server uses an SSE-formatted streaming response to send the AI's result back to the browser.

There are two common patterns:

- **Pattern A: Native `EventSource`**
    
- **Pattern B: HTTP POST + SSE streaming response**
    

Both provide server-to-client streaming, but they are suited to different scenarios.

---

# 2. Understanding SSE and HTTP

Before looking at the two patterns, it is useful to clarify the relationship between HTTP and SSE.

SSE is **not a replacement for HTTP**.

Instead, think of the technologies as different layers:

```text
HTTP
 │
 ├── Request
 │     └── GET / POST / ...
 │
 └── Response
       └── Streaming response
             └── SSE event format
```

For example, in an AI chat application, the browser might send:

```http
POST /api/chat
Content-Type: application/json

{
  "message": "Analyze this architecture",
  "model": "qwen",
  "conversation_id": "12345"
}
```

The server can then keep the HTTP response open and progressively send SSE events:

```http
Content-Type: text/event-stream
```

For example:

```text
event: message.delta
data: {"text":"The"}

event: message.delta
data: {"text":" security"}

event: message.delta
data: {"text":" risk"}

event: response.completed
data: {}
```

Therefore, the overall communication is:

```text
Browser                              Server
   │                                   │
   │  Normal HTTP request              │
   │  POST /api/chat                   │
   │  { prompt, model, ... }           │
   │──────────────────────────────────>│
   │                                   │
   │       SSE / streaming response    │
   │<──────────────────────────────────│
   │  message.delta                    │
   │  message.delta                    │
   │  message.delta                    │
   │  response.completed               │
   │                                   │
```

This is one of the most important concepts in understanding SSE-based AI applications:

> **The request can be a normal HTTP request, while the response is a long-lived HTTP streaming response using the SSE event format.**

---

# 3. Pattern A — Native `EventSource`

## 3.1 What is it?

The browser provides a built-in API called `EventSource` specifically for consuming Server-Sent Events.

The client opens an SSE connection to an endpoint, and the server keeps that connection open while sending events to the browser.

The basic flow looks like this:

```text
Browser
   │
   │ GET /events
   ▼
Backend
   │
   │ SSE connection
   │
   ├── event 1
   ├── event 2
   ├── event 3
   └── event 4
   │
   ▼
Browser
```

The browser uses the native `EventSource` API:

```javascript
const events = new EventSource("/events");

events.onmessage = (event) => {
    console.log(event.data);
};

events.onerror = (error) => {
    console.error("SSE connection error", error);
};
```

The browser establishes a normal HTTP connection, normally using:

```http
GET /events
```

The server then responds with:

```http
Content-Type: text/event-stream
```

The connection remains open, and the server sends events as they become available.

---

## 3.2 What makes Pattern A different?

The important thing about Pattern A is that the browser is primarily **subscribing to an event stream**.

The communication looks like:

```text
Browser                         Server
   │                              │
   │ GET /events                  │
   │─────────────────────────────>│
   │                              │
   │<──── event 1 ────────────────│
   │<──── event 2 ────────────────│
   │<──── event 3 ────────────────│
   │<──── event 4 ────────────────│
   │                              │
```

The browser is not normally sending a large request body containing the AI prompt.

This makes the pattern particularly suitable for situations where the browser simply wants to **listen for events from the server**.

---

## 3.3 When should you use Pattern A?

Pattern A works well for:

- Notifications
    
- Background job progress
    
- Monitoring dashboards
    
- System status updates
    
- Deployment progress
    
- Long-running analysis jobs
    
- Real-time server notifications
    

For example, a user could start an analysis job:

```text
POST /analysis
       │
       ▼
Backend starts analysis
       │
       ▼
Browser connects to
GET /analysis/123/events
       │
       ▼
SSE event stream
```

The browser could then receive:

```text
analysis.started
analysis.progress
analysis.progress
analysis.completed
```

---

# 4. Limitations of Native `EventSource`

The main limitation is that native `EventSource` is designed primarily for opening an SSE connection, normally using an HTTP GET request.

For example:

```text
GET /events
```

It is not designed to work like a typical API request where the browser sends a large structured request body:

```text
POST /chat

{
    "message": "...",
    "conversation_id": "...",
    "model": "...",
    "tools": [...]
}
```

This distinction becomes important for AI applications.

An AI request may contain:

- User prompt
    
- Conversation history
    
- Model selection
    
- Agent configuration
    
- Tool configuration
    
- User preferences
    
- File or document references
    
- Other structured parameters
    

For this type of interaction, using a normal HTTP `POST` request is generally more convenient.

This leads to Pattern B.

---

# 5. Pattern B — HTTP POST + SSE Streaming Response

## 5.1 What is it?

Pattern B uses a normal HTTP request to submit the user's message and then returns a streaming response from the server.

The basic flow is:

```text
Browser
   │
   │ POST /api/chat
   │
   │ {
   │   "message": "...",
   │   "conversation_id": "...",
   │   "model": "...",
   │   "tools": [...]
   │ }
   ▼
Backend
   │
   ▼
AI Agent / LLM
   │
   ├── generates response
   ├── calls tools
   ├── receives results
   └── continues generation
   │
   ▼
Browser
   ◄──── SSE streaming response ────
```

The important point is that the **request is still a normal HTTP request**.

SSE is used for the **server-to-client streaming response**.

So the communication can be summarized as:

```text
             Request
Browser ────────────────────► Server
        HTTP POST
        JSON body

             Response
Browser ◄──────────────────── Server
        HTTP streaming
        text/event-stream
```

This is a very natural pattern for AI chat.

---

# 6. Why Pattern B Fits AI Chat Better

Imagine that the user enters:

> Analyze the security architecture and identify the major risks.

The browser might send:

```json
{
  "message": "Analyze the security architecture and identify the major risks.",
  "conversation_id": "12345",
  "model": "qwen",
  "tools": [
    "security_kb",
    "search"
  ]
}
```

The backend receives the request and starts the agent.

The agent might perform several operations:

```text
User request
     │
     ▼
   Agent
     │
     ├── Understand request
     │
     ├── Search security KB
     │
     ├── Call another tool
     │
     ├── Analyze results
     │
     └── Generate response
```

Instead of waiting until everything is finished, the backend can send events back to the browser as the work progresses.

For example:

```text
event: agent.started
data: {}

event: tool.started
data: {"tool":"security_kb"}

event: tool.completed
data: {"results":12}

event: message.delta
data: {"text":"The"}

event: message.delta
data: {"text":" primary"}

event: message.delta
data: {"text":" security"}

event: message.delta
data: {"text":" risks"}

event: response.completed
data: {}
```

The user can therefore see both the response and the progress of the agent.

---

# 7. How Pattern B Works in the Browser

The frontend sends a normal HTTP POST request:

```javascript
const response = await fetch("/api/chat", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        message: "Analyze this architecture",
        conversation_id: "12345",
        model: "qwen"
    })
});
```

The important difference is that the frontend does **not** wait for the complete response before displaying anything.

Instead, it reads the response incrementally.

Conceptually:

```javascript
const reader = response.body.getReader();

while (true) {
    const { value, done } = await reader.read();

    if (done) {
        break;
    }

    // Process the received event/chunk
}
```

The backend may return:

```http
Content-Type: text/event-stream
```

and progressively send events.

Therefore:

```text
Browser
   │
   │ POST /api/chat
   │
   │ prompt + configuration
   ▼
Backend
   │
   ▼
Agent / LLM
   │
   │ generates information
   ▼
Backend
   │
   │ SSE events
   ▼
Browser
```

---

# 8. Pattern B Is More Than Token Streaming

For a simple chatbot, the stream might contain only generated text:

```text
message.delta
message.delta
message.delta
message.completed
```

However, an agent-based application can provide much richer information.

For example:

```text
agent.started

tool.started
tool.progress
tool.completed

message.delta
message.delta
message.delta

agent.completed
```

This allows the frontend to show the user what the agent is doing.

For example:

```text
Analyzing your request...

✓ Security KB searched
✓ Architecture analyzed
🔎 Checking security requirements...

The primary risks are...
```

This is particularly useful for an agent framework such as DojoAgents, where the agent may perform multiple operations before producing its final answer.

---

# 9. Pattern A vs. Pattern B

||Pattern A: Native `EventSource`|Pattern B: HTTP POST + SSE|
|---|---|---|
|Initial request|Usually HTTP GET|HTTP POST|
|Browser API|`EventSource`|`fetch()`|
|Request body|Not convenient|Yes|
|Structured request|Limited|Excellent|
|Large request|Not convenient|Convenient|
|Server → client streaming|Yes|Yes|
|AI token streaming|Possible|**Very suitable**|
|Agent events|Yes|**Very suitable**|
|Background jobs|Excellent|Excellent|
|Notifications|Excellent|Possible, but unnecessary|
|AI chat|Possible|**Recommended**|
|Agent applications|Possible|**Recommended**|

The key difference is therefore **not whether SSE is being used**.

Both patterns can use SSE.

The main difference is:

```text
Pattern A

Browser
   │
   │ GET
   ▼
SSE connection
   │
   ◄── events
```

versus:

```text
Pattern B

Browser
   │
   │ POST
   │ request body
   ▼
Agent
   │
   ◄── SSE streaming response
```

---

# 10. Recommended Pattern for AI Chat

For a simple event subscription, Pattern A is often the easiest option.

For example:

```text
GET /notifications
GET /job/123/events
GET /system/events
```

The browser simply connects and listens.

For an AI chat application, Pattern B is generally a better fit:

```text
POST /api/chat
        │
        │
        │ User message
        │ Conversation
        │ Model
        │ Tools
        │ Configuration
        ▼
     Agent
        │
        │
        │ SSE events
        ▼
     Browser
```

The reason is that an AI interaction naturally consists of two different phases:

**1. Client → Server**

The client submits the user's request.

**2. Server → Client**

The server progressively returns the result as the agent works.

This gives you:

```text
             Normal HTTP
User ─────────────────────────► Agent
       POST /api/chat

             Streaming
User ◄───────────────────────── Agent
       SSE events
```

---

# 11. Recommended Architecture for DojoAgents

For an agent-based application such as DojoAgents, I would recommend treating the SSE connection as an **Agent Event Stream**, rather than thinking of it only as an LLM token stream.

The architecture could look like:

```text
                     ┌──────────────────┐
                     │     Browser      │
                     │                  │
                     │  Chat UI         │
                     │  Agent progress  │
                     │  Tool status     │
                     └────────┬─────────┘
                              │
                              │ HTTP POST
                              │ /api/chat
                              ▼
                     ┌──────────────────┐
                     │    API Layer     │
                     │                  │
                     │ POST /api/chat   │
                     └────────┬─────────┘
                              │
                              ▼
                     ┌──────────────────┐
                     │   Agent Runtime  │
                     │                  │
                     │   DojoAgents     │
                     └────────┬─────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
             LLM             Tools            KB
              │               │               │
              └───────────────┼───────────────┘
                              │
                              ▼
                    SSE / HTTP Stream
                              │
                              ▼
                         Browser UI
```

The stream could contain events such as:

```text
agent.started

tool.started
tool.progress
tool.completed

message.delta
message.completed

agent.completed

error
```

This gives the frontend a clean event-driven interface.

The frontend does not need to know exactly how the agent works internally. It only needs to understand the events and update the user interface accordingly.

---

# 12. Important Terminology

When discussing the architecture, it is better to use the following terminology:

**Avoid:**

> "SSE replaces HTTP."

Instead say:

> "SSE uses HTTP to provide a server-to-client event stream."

**Avoid:**

> "The browser sends an SSE request."

Instead say:

> "The browser establishes an HTTP connection to an SSE endpoint."

For the AI-chat pattern, say:

> "The browser sends a normal HTTP POST request, and the server returns a streaming HTTP response using the SSE format."

This is technically more precise.

---

# 13. Final Recommendation

For a simple server-to-browser event subscription, **Pattern A using native `EventSource` is simple and effective**.

For an AI chat or agent application, **Pattern B—HTTP POST followed by a streaming response—is generally more flexible and better suited to the application's request/response model**.

The most important thing to remember is:

> **SSE is not an alternative to HTTP. SSE is a server-to-client streaming mechanism that operates over HTTP.**

For an AI chat application, the typical architecture is therefore:

```text
Browser
   │
   │ 1. HTTP POST
   │    User prompt
   │    Conversation
   │    Model
   │    Tools
   ▼
Backend / Agent
   │
   │ 2. Process request
   │    LLM calls
   │    Tool calls
   │    Agent reasoning
   ▼
Browser
   ▲
   │ 3. HTTP streaming response
   │    SSE events
   │
   ├── agent.started
   ├── tool.started
   ├── tool.completed
   ├── message.delta
   ├── message.delta
   └── agent.completed
```

This **HTTP POST + SSE streaming response** pattern is the one I would recommend as the primary pattern for a DojoAgents-based AI chat application.




---
# More Clarity
### 1. The Core Correction: SSE is NOT an alternative to HTTP
You do not choose between HTTP and SSE. **SSE runs *over* HTTP.** 

The real architectural choice you are making for an AI chat app is between a **Non-streaming HTTP response** and a **Streaming HTTP response**.

*   **Non-streaming HTTP:** The client sends a request, the server does all its processing (which could take 30 seconds for an LLM), and then returns the *entire* complete response at once.
*   **Streaming HTTP:** The client sends a request, and the server immediately responds with headers (e.g., `HTTP/1.1 200 OK`), but keeps the connection open to deliver the body incrementally as data becomes available.
*   **SSE (Server-Sent Events):** This is simply a standardized data format (`Content-Type: text/event-stream`) used to structure those incremental chunks over a streaming HTTP connection.

### 2. How Modern AI Chat Apps Actually Use It (Pattern B)
If you look at the native browser `EventSource` API for SSE, it only supports `GET` requests. However, AI chat apps (like DojoAgents) need to send large payloads (the user's prompt, conversation history, and tool configurations). 

Therefore, modern AI apps use a hybrid approach (often called **Pattern B**):
1.  **The Request (HTTP POST):** The browser uses a standard `fetch()` API with a `POST` method to send the complex JSON payload to the backend.
2.  **The Response (Streaming HTTP via SSE format):** The server (e.g., FastAPI in DojoAgents) accepts the POST, invokes the LLM, and returns a `text/event-stream` response. The frontend reads this stream incrementally using `response.body.getReader()`.

### 3. Why Streaming (via SSE) is Crucial for AI User Experience
*   **Reducing Time to First Token (TTFT):** Because LLMs generate text sequentially, streaming allows the frontend to display the text incrementally (the "typewriter effect"). This drastically improves perceived latency.
*   **Mitigating Idle Timeouts:** Complex AI agents don't just generate text; they reason, query databases, search the web, and run code. This process can take a long time. While streaming does not disable hard server timeouts, it prevents **idle timeouts**. By pushing intermediate data or keep-alive pings down the stream while the agent is "thinking," the load balancers and proxies know the connection is still active and won't drop it.

### 4. Beyond Text: The "Agent Event Stream"
For an advanced framework like **DojoAgents**, SSE is incredibly powerful because it shouldn't just be viewed as "streaming LLM text tokens." It is an **Agent Event Stream**.

Because agents interact with external tools, the backend can stream structured JSON events to tell the UI exactly what is happening in the agent loop:

```text
event: agent.started
data: {"status": "Agent is initializing"}

event: tool.started
data: {"tool": "yfinance_market_data", "action": "Fetching AAPL prices"}

event: tool.completed
data: {"results": "Data retrieved successfully"}

event: message.delta
data: {"text": "Based on the latest data..."}
```
This allows the React frontend to build a rich UI that shows loading spinners for tools, execution steps, and finally, the text response—all over a single HTTP connection.

### 5. When should you use WebSockets instead?
Both SSE and WebSockets require long-lived connections, so neither is magically "free" of server resource consumption. 

However, SSE is vastly simpler for AI chat because the communication naturally flows **Server → Client** after the initial POST. You should upgrade to **WebSockets** only when your application requires persistent **bidirectional** real-time data, such as:
*   Voice-to-voice AI interaction (where the user can speak and stream audio back to the server).
*   Live interruptions (the user clicking a button to immediately halt the AI's generation mid-stream).
*   Collaborative, multi-user agent control.

**Summary:** 
For an application like DojoAgents, **HTTP response streaming is the absolute standard**, and **SSE is the ideal format** to implement it. It perfectly maps to the "Submit Request → Stream Agent Lifecycle Events + Text Deltas" architecture.
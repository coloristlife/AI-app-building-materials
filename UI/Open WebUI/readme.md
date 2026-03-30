
# Open WebUI

https://github.com/open-webui/open-webui

Open WebUI is an extensible, feature-rich, and user-friendly self-hosted AI platform designed to operate entirely offline. It supports various LLM runners like Ollama and OpenAI-compatible APIs, with built-in inference engine for RAG, making it a powerful AI deployment solution.


Key Features of Open WebUI ⭐
🚀 Effortless Setup: Install seamlessly using Docker or Kubernetes (kubectl, kustomize or helm) for a hassle-free experience with support for both :ollama and :cuda tagged images.

🤝 Ollama/OpenAI API Integration: Effortlessly integrate OpenAI-compatible APIs for versatile conversations alongside Ollama models. Customize the OpenAI API URL to link with LMStudio, GroqCloud, Mistral, OpenRouter, and more.

🛡️ Granular Permissions and User Groups: By allowing administrators to create detailed user roles and permissions, we ensure a secure user environment. This granularity not only enhances security but also allows for customized user experiences, fostering a sense of ownership and responsibility amongst users.

📱 Responsive Design: Enjoy a seamless experience across Desktop PC, Laptop, and Mobile devices.

📱 Progressive Web App (PWA) for Mobile: Enjoy a native app-like experience on your mobile device with our PWA, providing offline access on localhost and a seamless user interface.

✒️🔢 Full Markdown and LaTeX Support: Elevate your LLM experience with comprehensive Markdown and LaTeX capabilities for enriched interaction.

🎤📹 Hands-Free Voice/Video Call: Experience seamless communication with integrated hands-free voice and video call features using multiple Speech-to-Text providers (Local Whisper, OpenAI, Deepgram, Azure) and Text-to-Speech engines (Azure, ElevenLabs, OpenAI, Transformers, WebAPI), allowing for dynamic and interactive chat environments.

🛠️ Model Builder: Easily create Ollama models via the Web UI. Create and add custom characters/agents, customize chat elements, and import models effortlessly through Open WebUI Community integration.

🐍 Native Python Function Calling Tool: Enhance your LLMs with built-in code editor support in the tools workspace. Bring Your Own Function (BYOF) by simply adding your pure Python functions, enabling seamless integration with LLMs.

💾 Persistent Artifact Storage: Built-in key-value storage API for artifacts, enabling features like journals, trackers, leaderboards, and collaborative tools with both personal and shared data scopes across sessions.

📚 Local RAG Integration: Dive into the future of chat interactions with groundbreaking Retrieval Augmented Generation (RAG) support using your choice of 9 vector databases and multiple content extraction engines (Tika, Docling, Document Intelligence, Mistral OCR, External loaders). Load documents directly into chat or add files to your document library, effortlessly accessing them using the # command before a query.

🔍 Web Search for RAG: Perform web searches using 15+ providers including SearXNG, Google PSE, Brave Search, Kagi, Mojeek, Tavily, Perplexity, serpstack, serper, Serply, DuckDuckGo, SearchApi, SerpApi, Bing, Jina, Exa, Sougou, Azure AI Search, and Ollama Cloud, injecting results directly into your chat experience.

🌐 Web Browsing Capability: Seamlessly integrate websites into your chat experience using the # command followed by a URL. This feature allows you to incorporate web content directly into your conversations, enhancing the richness and depth of your interactions.

🎨 Image Generation & Editing Integration: Create and edit images using multiple engines including OpenAI's DALL-E, Gemini, ComfyUI (local), and AUTOMATIC1111 (local), with support for both generation and prompt-based editing workflows.

⚙️ Many Models Conversations: Effortlessly engage with various models simultaneously, harnessing their unique strengths for optimal responses. Enhance your experience by leveraging a diverse set of models in parallel.

🔐 Role-Based Access Control (RBAC): Ensure secure access with restricted permissions; only authorized individuals can access your Ollama, and exclusive model creation/pulling rights are reserved for administrators.

🗄️ Flexible Database & Storage Options: Choose from SQLite (with optional encryption), PostgreSQL, or configure cloud storage backends (S3, Google Cloud Storage, Azure Blob Storage) for scalable deployments.

🔍 Advanced Vector Database Support: Select from 9 vector database options including ChromaDB, PGVector, Qdrant, Milvus, Elasticsearch, OpenSearch, Pinecone, S3Vector, and Oracle 23ai for optimal RAG performance.

🔐 Enterprise Authentication: Full support for LDAP/Active Directory integration, SCIM 2.0 automated provisioning, and SSO via trusted headers alongside OAuth providers. Enterprise-grade user and group provisioning through SCIM 2.0 protocol, enabling seamless integration with identity providers like Okta, Azure AD, and Google Workspace for automated user lifecycle management.

☁️ Cloud-Native Integration: Native support for Google Drive and OneDrive/SharePoint file picking, enabling seamless document import from enterprise cloud storage.

📊 Production Observability: Built-in OpenTelemetry support for traces, metrics, and logs, enabling comprehensive monitoring with your existing observability stack.

⚖️ Horizontal Scalability: Redis-backed session management and WebSocket support for multi-worker and multi-node deployments behind load balancers.

🌐🌍 Multilingual Support: Experience Open WebUI in your preferred language with our internationalization (i18n) support. Join us in expanding our supported languages! We're actively seeking contributors!

🧩 Pipelines, Open WebUI Plugin Support: Seamlessly integrate custom logic and Python libraries into Open WebUI using Pipelines Plugin Framework. Launch your Pipelines instance, set the OpenAI URL to the Pipelines URL, and explore endless possibilities. Examples include Function Calling, User Rate Limiting to control access, Usage Monitoring with tools like Langfuse, Live Translation with LibreTranslate for multilingual support, Toxic Message Filtering and much more.

🌟 Continuous Updates: We are committed to improving Open WebUI with regular updates, fixes, and new features.

Want to learn more about Open WebUI's features? Check out our Open WebUI documentation for a comprehensive overview!

We are incredibly grateful for the generous support of our sponsors. Their contributions help us to maintain and improve our project, ensuring we can continue to deliver quality work to our community. Thank you!


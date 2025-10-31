
- https://ragflow.io/docs/dev/ 

- https://github.com/infiniflow/ragflow  ![GitHub Repo stars](https://img.shields.io/github/stars/infiniflow/ragflow?style=social) 

RAGFlow is a leading open-source Retrieval-Augmented Generation (RAG) engine that fuses cutting-edge RAG with Agent capabilities to create a superior context layer for LLMs. It offers a streamlined RAG workflow adaptable to enterprises of any scale. Powered by a converged context engine and pre-built agent templates, RAGFlow enables developers to transform complex data into high-fidelity, production-ready AI systems with exceptional efficiency and precision.

# from AI
RAGFlow is an integrated software platform (v0.21 as of Oct 2025) for building RAG-based systems. Its architecture is a multi-stage pipeline combining document ingestion, indexing, and retrieval with agentic modules. Ingested data (PDFs, docs, images, spreadsheets, web pages, etc.) passes through “deep document understanding” parsers (e.g. OCR, table-structure, layout analysis). Preprocessing can include document clustering or knowledge graph construction (e.g. via the RAPTOR hierarchical summarizer or GraphRAG modules). Data is then indexed into both full-text and vector indexes (default: Elasticsearch, optional: Infinity). At query time, RAGFlow uses multiple recall strategies (semantic embedding search, keyword search, or external web search via Tavily) with fused re-ranking to retrieve the top-K relevant chunks. The retrieved chunks are provided as context to an LLM (via an OpenAI-like API or Python SDK) along with traceable citations. RAGFlow also includes agent components (e.g. code executors, reasoning chains, multi-turn memory) that orchestrate LLM interactions with tools and retrieval, enabling complex workflows.

Figure: RAGFlow’s multi-stage retrieval architecture. Raw documents are parsed (extraction), clustered/refined (preprocessing), indexed (in vector and text indices), and then queried using fused retrieval to return top-K results. (Image source: RAGFlow docs.)
<img width="1000" height="250" alt="image" src="https://github.com/user-attachments/assets/8cab9e33-551f-4bb8-bec9-e13f5a1553e9" />


RAGFlow’s core features include:

Deep document understanding: advanced parsers (PDF OCR, layout analysis, table recognition, image extraction) that convert raw data into text and structured knowledge.

Template-based chunking and fusion: customizable chunking of documents (via templates or heuristics) and merging techniques to control token size and context.

Multiple retrieval strategies: vector search (with configurable embedding models), keyword search, and even external web search (Tavily integration for “Deep Research”). It performs multi-recall and fused re-ranking of results for higher accuracy.

Traceable citations: RAGFlow automatically tracks source chunks, enabling grounded answers and transparency (“grounded citations with reduced hallucinations”).

Agentic workflows: pre-built agent templates (e.g. chat assistants, reasoning chains, code execution) and plugin components (Python/JS executors) to orchestrate LLMs with tools.

Flexible data support: ingestion of many formats (Office docs, images, scanned docs, structured data, web pages, SQL, etc.).

Extensive integration: RESTful and Python APIs, OpenAI-compatible endpoints, Docker deployment, and GUI for dataset/chat management.

In short, RAGFlow is a comprehensive RAG system: it automates ingestion, indexing, and retrieval at scale, provides rich preprocessing (including GraphRAG knowledge graphs and RAPTOR hierarchical chunking), and wraps all of this in an enterprise-grade stack (Docker, microservices, UIs).

**Document Retrieval, Indexing, and Feedback Loops**

**Retrieval and indexing in RAGFlow:** RAGFlow ingests and indexes documents into a search engine. By default, it uses Elasticsearch for storing full-text and dense vectors (with Redis or Infinity optional). During query time, RAGFlow performs multiple recall – e.g. semantic embedding search (via configurable embedding models) and keyword search – then uses a fused ranking ensemble to combine results. The system can also call external search via Tavily for internet knowledge (“Deep Research”), similar to CRAG’s web fallback but as an optional integrated feature.

Importantly, RAGFlow’s indexing pipeline is highly configurable: one can enable GPU-accelerated DeepDoc parsing, recursive summarization (RAPTOR), graph construction, auto-keyword generation, etc. This contrasts with CRAG’s use of a fixed static corpus. RAGFlow also supports ongoing ingestion: datasets can be updated and reindexed through its web UI or APIs.

---

**Strengths and Limitations**

**RAGFlow – Strengths:**

* **Full-stack platform:** Handles everything from ingestion to deployment (data pipelines, indexing, chat UI, APIs).
* **Rich features:** Deep document parsing, template chunking, multi-source retrieval (including multi-modal), agent tools (code exec, web search, SQL generation).
* **Scalability:** Built on scalable components (Elasticsearch clusters, Docker services) and supports GPU acceleration. Can handle “literally unlimited tokens” by indexing effectively.
* **Active development & community:** Over 66k stars on GitHub, frequent updates (2024–2025) adding new ML models and capabilities.
* **Enterprise-ready:** Configurable LLM backends, API keys, authentication, logging, and UI make it suitable for production.

**Limitations:**

* **Complexity:** Many components and configuration options create a steep learning curve. Setting up Docker, choosing parsers (DeepDoc vs Naive), and tuning the pipeline can be challenging.
* **Resource-intensive:** DeepDoc, RAPTOR summarization, and large embeddings require substantial CPU/GPU resources and memory (the RAPTOR feature warns of “significant memory, computational resources, and tokens”).
* **Less “corrective” on-the-fly:** RAGFlow does not natively evaluate retrieval quality per query (aside from optional search). It assumes the index contains relevant info.
* **Less academic validation:** Unlike CRAG’s controlled experiments, RAGFlow’s effectiveness is shown by use cases and demos rather than peer-reviewed benchmarks. (However, it’s continuously tested by users and updated by InfiniFlow.)

---

**Use Cases and Maturity**

**RAGFlow:** Designed for enterprise and large-scale deployments. Typical use cases include knowledge management portals, multi-document Q&A (across PDFs, manuals, databases), AI assistants with tool integrations, and any context requiring reliable citation tracking. Its 0.21.1 release (Oct 2025) and public roadmap show it’s quite mature for an open-source RAG system, with robust documentation and community support. Organizations can use RAGFlow out-of-the-box, while CRAG would require custom development to integrate.

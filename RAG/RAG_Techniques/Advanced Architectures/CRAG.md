# paper 
https://ar5iv.labs.arxiv.org/html/2401.15884v3
<img width="2465" height="1817" alt="image" src="https://github.com/user-attachments/assets/4963170f-8430-4e73-b450-74106bc68ee7" />


## implementation 
- https://github.com/HuskyInSalt/CRAG   ![GitHub Repo stars](https://img.shields.io/github/stars/HuskyInSalt/CRAG?style=social)  official one
- https://github.com/NirDiamant/RAG_Techniques/blob/main/all_rag_techniques_runnable_scripts/crag.py

# research from AI
**Architecture & Design Differences**

CRAG augments a standard RAG pipeline by inserting a retrieval evaluator module between document retrieval and generation. Its pipeline (Figure 1 in the paper) is: **Query → Retriever → Evaluator → (Refine or Re-retrieve) → Generator**. After an initial retrieval from a static corpus, CRAG’s T5-based retrieval evaluator scores each document’s relevance to the query. Based on the scores, CRAG triggers one of three actions: **Correct**, **Incorrect**, or **Ambiguous** (no confident judgment).

In **Correct mode**, CRAG applies a “decompose-then-recompose” knowledge refinement: it segments the retrieved documents into fine-grained “knowledge strips,” re-scores each strip, filters out irrelevant parts, and concatenates the relevant strips for the LLM.

In **Incorrect mode** (when none of the retrieved docs are deemed relevant), CRAG discards the retrieval and issues a web search (via a search API) for external knowledge. The returned web pages are then processed similarly (segmented and refined) and fed to the generator.

The **Ambiguous mode** combines both sources (original and web) to cover uncertainty.

This design emphasizes robustness: by self-assessing retrieval, CRAG either corrects or supplements it to reduce hallucination. Importantly, CRAG is described as “plug-and-play,” meaning it can be inserted into any existing RAG system or model (including vanilla RAG, Self-RAG, etc.) without retraining the base generator. In practice, CRAG is implemented as a **T5-large model (≈0.77B parameters)** fine-tuned to score relevance, which is relatively lightweight compared to typical LLM-based critics (e.g., 7B LLaMA-2).

---

**Core Features and Functionality**

**CRAG’s core features include:**

* **Retrieval evaluator:** Scores retrieved documents using a fine-tuned T5 model.
* **Adaptive retrieval actions:** Based on evaluator confidence, triggers document refinement or additional searches.
* **Knowledge refinement:** Decomposes documents into smaller “knowledge strips” and filters for relevance.
* **Web search integration:** Acts as a fallback knowledge source when static retrieval fails.
* **Plug-and-play compatibility:** Can wrap around any generator/RAG setup (demonstrated with both standard RAG and Self-RAG).
* **Performance gains:** Significantly improves performance of RAG-based approaches on Q&A tasks, mainly by reducing irrelevant context.

These features focus on improving the robustness and relevance of retrieved context. CRAG does not provide a user-facing system, UI, or dataset management—it is a **module or algorithm** that inserts into existing RAG code. It does not include its own embedding or indexing infrastructure.

---

**Document Retrieval, Indexing, and Feedback Loops**

**Retrieval in CRAG:** CRAG itself does not perform retrieval from scratch; it assumes an underlying retriever over a static corpus. During inference, CRAG evaluates the quality of those retrieval results.

* If they are adequate (**Correct**), CRAG refines them.
* If not (**Incorrect**), it re-issues the query to a web search API and harvests additional documents.

This effectively provides a **feedback loop**: the retrieval evaluator’s confidence directly influences whether to accept, refine, or extend the retrieval set. There is no index-building component in CRAG—it relies on pre-indexed corpora (or knowledge bases) for the initial retrieval. The “feedback loop” in CRAG is internal (evaluator → adjust retrieval action) rather than user-driven.

---

**Integration Capabilities and Flexibility**

**CRAG:** By design, CRAG is **agnostic to the underlying model and retrieval implementation**. It can be seamlessly coupled with various RAG-based approaches. In practice, CRAG is delivered as **Python scripts** that sit between the retriever and generator. It can wrap any LLM or RAG pipeline; for example, the authors demonstrate CRAG with both a basic RAG setup and the Self-RAG critic model.

Because it’s a **research prototype**, CRAG doesn’t include SDKs or APIs. Integration requires coding—developers must call the evaluator model, parse its output, and handle conditional retrieval logic. There is no UI or management interface. The only external dependency is the web search API (e.g., Google Search) for the Incorrect action.

---

**Strengths and Limitations**

**Corrective RAG (CRAG) – Strengths:**

* **Robustness to bad retrievals:** The retrieval evaluator ensures that only high-confidence documents are used, greatly reducing noise.
* **Improved accuracy:** Consistently boosts answer accuracy of RAG systems on QA tasks.
* **Modularity:** Can be added to any existing RAG system without retraining the base model.
* **Lightweight evaluator:** Uses a ~0.77B T5 model (much smaller than typical LLM critics).
* **Better than naive self-critique:** Outperforms prompt-based retrieval evaluation (e.g., ChatGPT critics) in experiments.

**Limitations:**

* **Limited pipeline:** Focuses only on retrieval correction; does not handle ingestion, UI, or multi-format data.
* **Dependency on web search:** When retrieval fails, relies on commercial APIs (e.g., Google) and ChatGPT for query rewriting, adding cost, latency, and requiring internet access.
* **Heuristic thresholds:** Decision thresholds for Correct/Incorrect are tuned per dataset and may require manual adjustment.
* **Overhead:** Each query may involve extra inference (evaluating every retrieved doc and possibly doing web searches), slowing responses.
* **Narrow focus:** No built-in support for agents, analytics, or large-scale indexing—it’s not a standalone product.

---

**Use Cases and Maturity**

**CRAG:** Targeted at research and development settings where improving factual accuracy of LLMs is critical. It suits **QA or assistant systems** built on fixed knowledge bases (e.g., domain-specific RAG) that need a safety net for retrieval failures.

CRAG’s maturity is **early**: it was introduced in a 2024 paper and has prototype code on GitHub. It is **not a polished product**; adoption is likely limited to experimental systems or research labs.


## Langgraph implementation
- https://levelup.gitconnected.com/building-the-entire-rag-ecosystem-and-optimizing-every-component-8f23349b96a4#8cd5

  <img width="1400" height="688" alt="image" src="https://github.com/user-attachments/assets/480a7bbc-e6e2-4895-a49a-338e7effae49" />

  CRAG: If the retrieved documents are irrelevant or ambiguous for a given query, a CRAG system won’t just pass them to the LLM. Instead, it triggers a new, more robust web search to find better information, corrects the retrieved documents, and then proceeds with generation.
  
- https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_crag/




<img width="1698" height="727" alt="image" src="https://github.com/user-attachments/assets/b02fabd0-94f9-42cb-95c8-e8a23210007d" />




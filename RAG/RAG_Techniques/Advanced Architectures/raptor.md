
# raptor
- https://github.com/parthsarthi03/raptor  ![GitHub Repo stars](https://img.shields.io/github/stars/parthsarthi03/raptor?style=social)
  The official implementation of RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval.
  
  https://arxiv.org/abs/2401.18059
  
  <img width="734" height="244" alt="image" src="https://github.com/user-attachments/assets/16968025-dc14-4470-a194-5049eb1a7dd4" />

Figure 1:Tree construction process: RAPTOR recursively clusters chunks of text based on their vector embeddings and generates text summaries of those clusters, constructing a tree from the bottom up. Nodes clustered together are siblings; a parent node contains the text summary of that cluster.


- https://github.com/NirDiamant/RAG_Techniques/blob/main/all_rag_techniques_runnable_scripts/raptor.py
  personal implementation

- https://github.com/BlueBash/RAG-Raptor-demo

Features

- Table Extraction: Identify and parse tables to retrieve structured data, making it easier to answer data-specific questions.
- Text Extraction: Efficiently extract and process text from PDFs, enabling accurate and comprehensive information retrieval.
- Image Analysis: Extract and interpret images within the PDFs to provide contextually relevant information.

Technologies Used
- LangChain: Framework for building applications with language models.
- RAG (Retrieval-Augmented Generation): Combines retrieval and generation for more accurate answers.
- RAPTOR: Constructs a recursive tree structure from documents for efficient, context-aware information retrieval.
- Streamlit: Framework for creating interactive web applications with Python.
- Unstructured.io: Tool for parsing and extracting complex content from PDFs, such as tables, graphs, and images.
- Poetry: Dependency management and packaging tool for Python.

<img width="1914" height="862" alt="image" src="https://github.com/user-attachments/assets/a84063ff-d013-4b34-b958-2e7a36e36f74" />

- https://blog.gopenai.com/deep-dive-into-raptor-with-llamaindex-raptor-pack-8eb4fa32df30
  Deep Dive into RAPTOR with LlamaIndex Raptor Pack

- feedbacks is not good
  https://www.reddit.com/r/LocalLLaMA/comments/1htcb5i/what_became_of_raptor_for_rag/#:~:text=Exactly%2C%20secondly%20there%20was%20a,at%20any%20point%20of%20time


# Application 

- https://levelup.gitconnected.com/building-the-entire-rag-ecosystem-and-optimizing-every-component-8f23349b96a4#8177
  
**Hierarchical Indexing (RAPTOR) Knowledge Tree**

The Theory: RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval) takes the multi-representation idea a step further. Instead of just one layer of summaries, RAPTOR builds a multi-level tree of summaries. It starts by clustering small document chunks. It then summarizes each cluster.


<img width="720" height="554" alt="image" src="https://github.com/user-attachments/assets/4c48c1fb-e15c-44b7-8e7f-d1c8ca137ba6" />

Then, it takes these summaries, clusters them, and summarizes the new clusters. This process repeats, creating a hierarchy of knowledge from fine-grained details to high-level concepts. When you query, you can search at different levels of this tree, allowing for retrieval that can be as specific or as general as needed.

This is a more advanced technique, and while we won’t implement the full algorithm here, you can find a deep dive and complete code in the RAPTOR Cookbook. It represents the cutting edge of structured indexing.




# research from AI

**RAPTOR Overview and Problem Context**

Retrieval-Augmented Generation (RAG) methods augment language models with external knowledge by retrieving relevant document snippets. However, traditional RAG systems split documents into short contiguous chunks (e.g., fixed-length passages) and retrieve them via vector search. This approach often fails for complex queries requiring understanding across an entire document. For example, to answer *“How did Cinderella reach her happy ending?”*, isolated paragraphs may miss the full narrative.

**RAPTOR** (“Recursive Abstractive Processing for Tree-Organized Retrieval”) solves this by building a **hierarchical summary tree** of each document, enabling multi-level retrieval. It first divides text into small chunks, then recursively clusters semantically similar chunks and summarizes each cluster into higher-level summaries. This bottom-up process constructs a **tree of summaries** that captures both detailed and abstracted content.

At query time, RAPTOR retrieves relevant nodes from this tree, providing context at the appropriate level of abstraction. It overcomes the RAG limitation of “short contiguous snippets only” by indexing documents at multiple scales. The recursive summarization allows efficient integration of information across an entire document.

---

**Main Components of RAPTOR**

**RAPTOR’s pipeline** includes the following stages:

* **Chunking:** Split each document into short contiguous segments (≈100 tokens) while preserving sentence integrity. Each chunk becomes a leaf node in the RAPTOR tree.
* **Embedding:** Encode each chunk with a vector model (e.g., SBERT). These embeddings are inputs for clustering.
* **Clustering:** Group semantically related chunks using an embedding-based algorithm. RAPTOR employs a **Gaussian Mixture Model (GMM)** on reduced-dimension embeddings (via UMAP) for soft clustering, allowing a chunk to belong to multiple clusters if it spans topics. The **Bayesian Information Criterion (BIC)** selects the number of clusters. Clustering is hierarchical: broad global clusters first, then finer local ones. Oversized clusters are recursively split until manageable.
* **Summarization:** For each cluster, a language model (e.g., GPT-3.5-turbo) produces an abstractive summary. Summaries form the internal nodes of the tree, with member chunks as children. Summaries are ~72% shorter than the original text, reducing context size while retaining key content. Only ~4% of summaries have minor hallucinations, with negligible downstream impact.
* **Recursive Tree Construction:** Summaries are re-embedded, clustered, and summarized again. This recursive process builds a multi-layer tree—root nodes encode overall themes, intermediate nodes represent mid-level topics, and leaves hold fine details.

**Retrieval Strategies:**
At query time, RAPTOR supports two methods:

* **Tree Traversal:** Start at the root, select top-𝑘 nodes by cosine similarity, then descend recursively to child nodes.
* **Collapsed Tree:** Flatten all nodes and select the top ones globally under a token budget.

Empirically, **collapsed retrieval** performs best since it flexibly mixes high-level and detailed context.

---

**Recursive Summarization and Embedding-Based Clustering**

The core innovation in RAPTOR is **recursive abstractive summarization**. The process alternates between clustering and summarizing:

1. **Cluster leaf embeddings:** Using SBERT and GMM+UMAP, semantically coherent clusters are formed (based on meaning, not text order).
2. **Summarize each cluster:** An LLM generates a concise abstract for each cluster’s combined text, encapsulating its shared themes.
3. **Embed summaries:** These are treated as new “documents” and re-embedded.
4. **Repeat clustering:** The summaries are clustered and summarized recursively until all content is captured in a top-level summary.

Each level compresses its children by ~72%, resulting in a compact tree that preserves the document’s semantic structure. The final hierarchy encodes both high-level and fine-grained knowledge.

---

**Query-Time Retrieval from the Tree**

When given a query, RAPTOR embeds it using the same encoder and retrieves relevant nodes from the summary tree.

* **Tree Traversal:** Navigate top-down from root to leaves, selecting top-𝑘 nodes at each level by similarity. This balances breadth and depth.
* **Collapsed Tree:** Flatten all nodes and select the most similar ones globally until the token limit is reached.

**Collapsed retrieval** typically outperforms traversal because it selects the optimal mix of summaries and detailed chunks. Efficient similarity search libraries like FAISS can accelerate this step.

Example: In the *Cinderella* experiment, RAPTOR retrieves multi-level nodes capturing the full storyline, while flat DPR retrieval only captures disjoint paragraphs. RAPTOR’s retrieved context usually includes or surpasses DPR’s, with greater semantic coverage.

---

**Comparison to Traditional RAG (Flat Retrieval)**

| **Aspect**                 | **Traditional RAG**           | **RAPTOR**                                               |
| -------------------------- | ----------------------------- | -------------------------------------------------------- |
| **Context Scope**          | Retrieves fixed-length chunks | Retrieves summaries and chunks at multiple granularities |
| **Thematic Grouping**      | Contiguous text only          | Semantic clustering across distant segments              |
| **Retrieval Granularity**  | Uniform chunks                | Multi-scale (summary or detail based on query)           |
| **Compression Efficiency** | All chunks stored equally     | Summaries compress info (~72% token reduction)           |
| **Interpretability**       | Flat and opaque               | Hierarchical, showing which clusters were retrieved      |
| **Computation Trade-off**  | Simple but shallow            | Heavier preprocessing, better retrieval accuracy         |

**Trade-offs:**
RAPTOR requires more preprocessing—repeated clustering and LLM summarization—but scales linearly with document length and delivers superior retrieval quality. Query-time search is heavier but manageable with optimization. The 4% hallucination rate has minimal effect. Overall, RAPTOR trades computation for **significant improvements in accuracy, context quality, and interpretability**.

---

**Empirical Benefits and Insights**

Experiments show that RAPTOR consistently outperforms flat retrieval across benchmarks like **NarrativeQA, QASPER,** and **QuALITY**:

* On QASPER, RAPTOR improves F1 by **1.8–10.2 points** over DPR/BM25 baselines.
* On QuALITY, RAPTOR with UnifiedQA achieves **62.4% accuracy**, a **2–5% absolute gain**.
* Gains are most pronounced in complex, reasoning-heavy questions.

RAPTOR also enhances interpretability: retrieved nodes clearly trace the evidence chain, showing both high-level and detailed contributions. The recursive summaries reduce memory usage (~72% fewer tokens per level) while maintaining accuracy.

**Implementation and Integration:**
RAPTOR is available as a **Python library** with a simple interface:

```python
RA = RetrievalAugmentation()
RA.add_documents(text)
answer = RA.answer_question(question)
```

The system is modular—developers can replace embedding or summarization models via subclassing (e.g., swap SBERT or GPT).

RAPTOR is also integrated into **RAGFlow** as a preprocessing option, highlighting its practical adoption for enterprise-scale retrieval systems.

---

**In Summary**

RAPTOR introduces a **recursive, hierarchical approach** to document retrieval that captures multi-scale structure and meaning. It delivers more **accurate, efficient, and interpretable retrieval** than traditional RAG systems by combining clustering, summarization, and multi-level embeddings into a single, coherent framework.




raptor
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

## research from AI
Understood. I’ll provide a high-level conceptual explanation of RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval), then drill down into the technical details of how it works, including its document clustering, summarization, and retrieval steps. I’ll also explain how it differs from traditional chunk-based RAG pipelines in terms of structure, efficiency, and retrieval accuracy.

- https://levelup.gitconnected.com/building-the-entire-rag-ecosystem-and-optimizing-every-component-8f23349b96a4#fe6a
# Multi-Representation Indexing


**Advanced Indexing Strategies**

So far, our approach to indexing has been straightforward: split documents into chunks and embed them. This works, but it has a fundamental limitation.

Small, focused chunks are great for retrieval accuracy (they contain less noise), but they often lack the broader context needed for the LLM to generate a comprehensive answer.



<img width="1100" height="653" alt="image" src="https://github.com/user-attachments/assets/30d8632c-5326-4baa-8d25-5cc0b395dad3" />

Conversely, large chunks provide great context but perform poorly in retrieval because their core meaning gets diluted.

This is the classic “chunk size” dilemma. How can we get the best of both worlds?

The answer lies in more advanced indexing strategies that separate the document representation used for retrieval from the one used for generation. Let’s dive in.

**Multi-Representation Indexing**

The core idea of Multi-Representation Indexing is simple but powerful: instead of embedding the full document chunks, we create a smaller, more focused representation of each chunk (like a summary) and embed that instead.

<img width="1100" height="371" alt="image" src="https://github.com/user-attachments/assets/bf758808-0ee1-4850-a34d-633b62433195" />

During retrieval, we search over these concise summaries. Once we find the best summary, we use its ID to look up and retrieve the full, original document chunk.

This way, we get the precision of searching over small, dense summaries and the rich context of the larger parent documents for generation.

First, we need to load some documents to work with. We’ll grab two posts from Lilian Weng’s blog.

~~~
from langchain_community.document_loaders import WebBaseLoader

# Load two different blog posts to create a more diverse knowledge base
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
docs = loader.load()

loader = WebBaseLoader("https://lilianweng.github.io/posts/2024-02-05-human-data-quality/")
docs.extend(loader.load())

print(f"Loaded {len(docs)} documents.")


#### OUTPUT ####
Loaded 2 documents.
~~~
Next, we’ll create a chain to generate a summary for each of these documents.

~~~
import uuid

# The chain for generating summaries
summary_chain = (
    # Extract the page_content from the document object
    {"doc": lambda x: x.page_content}
    # Pipe it into a prompt template
    | ChatPromptTemplate.from_template("Summarize the following document:\n\n{doc}")
    # Use an LLM to generate the summary
    | ChatOpenAI(model="gpt-3.5-turbo", max_retries=0)
    # Parse the output into a string
    | StrOutputParser()
)

# Use .batch() to run the summarization in parallel for efficiency
summaries = summary_chain.batch(docs, {"max_concurrency": 5})

# Let's inspect the first summary
print(summaries[0])


#### OUTPUT ####
The document discusses building autonomous agents powered by Large
Language Models (LLMs). It outlines the key components of such a system, ...
~~~

Now comes the crucial part. We need a MultiVectorRetriever which requires two main components:

  - A vectorstore to store the embeddings of our summaries.
  - A docstore (a simple key-value store) to hold the original, full documents.

~~~
from langchain.storage import InMemoryByteStore
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_core.documents import Document

# The vectorstore to index the summary embeddings
vectorstore = Chroma(collection_name="summaries", embedding_function=OpenAIEmbeddings())

# The storage layer for the parent documents
store = InMemoryByteStore()
id_key = "doc_id" # This key will link summaries to their parent documents

# The retriever that orchestrates the whole process
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    byte_store=store,
    id_key=id_key,
)

# Generate unique IDs for each of our original documents
doc_ids = [str(uuid.uuid4()) for _ in docs]

# Create new Document objects for the summaries, adding the 'doc_id' to their metadata
summary_docs = [
    Document(page_content=s, metadata={id_key: doc_ids[i]})
    for i, s in enumerate(summaries)
]

# Add the summaries to the vectorstore
retriever.vectorstore.add_documents(summary_docs)

# Add the original documents to the docstore, linking them by the same IDs
retriever.docstore.mset(list(zip(doc_ids, docs)))
~~~

the key points in the above code is as below:

~~~
# Add the summaries to the vectorstore
retriever.vectorstore.add_documents(summary_docs)

# Add the original documents to the docstore, linking them by the same IDs
retriever.docstore.mset(list(zip(doc_ids, docs)))

~~~


Our advanced index is now built. Let’s test the retrieval process. We’ll ask a question about “Memory in agents” and see what happens.

~~~
query = "Memory in agents"

# First, let's see what the vectorstore finds by searching the summaries
sub_docs = vectorstore.similarity_search(query, k=1)
print("--- Result from searching summaries ---")
print(sub_docs[0].page_content)
print("\n--- Metadata showing the link to the parent document ---")
print(sub_docs[0].metadata)


#### OUTPUT ####
--- Result from searching summaries ---
The document discusses the concept of building autonomous agents powered by Large Language Models (LLMs) as their core controllers. It covers components such as planning, memory, and tool use, along with case studies and proof-of-concept examples like AutoGPT and GPT-Engineer. Challenges like finite context length, planning difficulties, and reliability of natural language interfaces are also highlighted. The document provides references to related research papers and offers a comprehensive overview of LLM-powered autonomous agents.

--- Metadata showing the link to the parent document ---
{'doc_id': 'cf31524b-fe6a-4b28-a980-f5687c9460ea'}
~~~

As you can see, the search found the summary that mentions “memory.” Now, the MultiVectorRetriever will use the doc_id from this summary's metadata to automatically fetch the full parent document from the docstore.

~~~
# Let the full retriever do its job
retrieved_docs = retriever.get_relevant_documents(query, n_results=1)

# Print the beginning of the retrieved full document
print("\n--- The full document retrieved by the MultiVectorRetriever ---")
print(retrieved_docs[0].page_content[0:500])


#### OUTPUT ####
"\n\n\n\n\n\nLLM Powered Autonomous Agents | Lil'Log\n\n\n\n\n\n\n\n\n
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\ ...."
~~~


This is exactly what we wanted! We searched over concise summaries but got back the complete, context-rich document, solving the chunk size dilemma.

----

**More clarity from AI regarding the above info**

Here’s a clear explanation of what the code does — and the important part: **whether the retriever contains both the original document and its summary.**

---

# ✅ **What the Code Is Doing**

### **1. Create a Chroma vector store to store *summaries***

```python
vectorstore = Chroma(collection_name="summaries", embedding_function=OpenAIEmbeddings())
```

This vector store will contain **only embeddings of summary chunks**, not the full documents.

* Each summary is embedded with `OpenAIEmbeddings()`.
* These embeddings can later be searched using similarity.

---

### **2. Create an in-memory byte store for *full documents***

```python
store = InMemoryByteStore()
```

This is a simple key–value store that holds:

* The **original, full documents**
* Stored as bytes (hence “ByteStore”)
* Indexed by a unique ID (`doc_id`)

The byte store does **not** perform vector search; it's just storage.

---

### **3. Set the link key between summaries ↔ full documents**

```python
id_key = "doc_id"
```

Each summary record in Chroma includes a `doc_id`.
That ID points to the full document stored in the ByteStore.

---

### **4. Create a MultiVectorRetriever**

```python
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    byte_store=store,
    id_key=id_key,
)
```

This retriever orchestrates the following:

### **When you query the retriever:**

1. It searches the **summary embeddings** in the Chroma vector store.
2. Finds the most relevant summary vectors.
3. Extracts the associated `doc_id` values.
4. Uses those `doc_id`s to pull the **original documents** from the ByteStore.

---

# 📌 **So does the retriever contain the *original doc* and its *summary*?**

### **Answer: Not exactly.**

The **retriever object** itself does *not* physically “contain” either one.

But:

### ✔ Summary vectors are stored in → `vectorstore` (Chroma)

### ✔ Original full documents are stored in → `byte_store` (InMemoryByteStore)

The retriever **links** them together through `doc_id`.

---

# 🔍 **In other words:**

| Component                | What is stored               | Used for                             |
| ------------------------ | ---------------------------- | ------------------------------------ |
| **Chroma vector store**  | Summaries (embedded vectors) | Similarity search                    |
| **InMemoryByteStore**    | Original full documents      | Retrieval after a summary is matched |
| **MultiVectorRetriever** | No data; only logic          | Connects summary → original document |

---

# 🧠 Summary

The retriever does **not** hold the documents directly. Instead:

* **Summaries** live in the vector store.
* **Original docs** live in the byte store.
* **Retriever** links them using `doc_id`.

This pattern is useful when:

* Full documents are too large to embed directly
* You want fast semantic search through summaries but still need to retrieve the full text

---

Original documents are stored in the **ByteStore** at the moment you **add documents through the `MultiVectorRetriever`** using its `add_documents` method (or by calling the underlying storage methods directly).

Here’s the important part:

# ✔ When are original documents stored?

They are stored **when you call something like:**

```python
retriever.add_documents(
    documents=docs, 
    id_key="doc_id", 
    include_metadata=True
)
```

or the equivalent low-level calls:

1. **Summaries are embedded and stored in the vectorstore**
2. **Original full docs are stored in the ByteStore**

---

# 🔍 How the storage process works (step-by-step)

Suppose you have a document:

```python
doc = Document(
    page_content="This is the full original document...",
    metadata={"doc_id": "123"}
)
```

And a summary:

```python
summary = Document(
    page_content="Short summary of the document",
    metadata={"doc_id": "123"}
)
```

When you add these to the retriever:

```python
retriever.add_documents([summary, doc])
```

## **Step 1 — Summary goes to the vector store**

* The summary text is embedded (OpenAIEmbeddings)
* Stored in Chroma with metadata like:

  ```json
  {"doc_id": "123"}
  ```

## **Step 2 — Original document goes to ByteStore**

* The full document text is serialized into bytes
* Stored in ByteStore like:

  ```
  ByteStore["123"] = b"<serialized full document>"
  ```

## **Step 3 — Retriever links them**

The retriever knows:

* summary embeddings → vectorstore
* full original docs → byte_store
* relationship via → `doc_id`

---

# ✔ What triggers storage in the ByteStore?

### **The original document is stored only when the retriever receives a document containing the parent content.**

That happens when:

* You call `retriever.add_documents`
* OR you manually call `byte_store.mset` with IDs and bytes

---

# 🧪 Example showing documents being stored

```python
docs = [
    Document(page_content="Full original document text", metadata={"doc_id": "doc1"}),
]

sums = [
    Document(page_content="Summary of document", metadata={"doc_id": "doc1"}),
]

retriever.add_documents(docs + sums)
```

After this:

### In Chroma (vectorstore):

```
embedding(summary) → metadata: { "doc_id": "doc1" }
```

### In ByteStore:

```
"doc1" → b"<serialized original document>"
```

---

# 🧠 Summary Answer

Original documents are stored in the ByteStore **when you add them to the retriever** through `add_documents`.
This automatically:

* embeds and stores summaries in the vectorstore
* stores full documents in the ByteStore
* links them by `doc_id`



-----

**how to store original docs permantly**

From AI

To store **original documents permanently** (instead of the temporary in-memory ByteStore), you must replace the `InMemoryByteStore()` with a **persistent storage backend**.

The typical choices are:

# ✅ **Option 1 — Use `LocalFileStore` (recommended)**

This stores the original documents **on disk**, so they persist across sessions.

```python
from langchain.storage import LocalFileStore

store = LocalFileStore("./parent_docs")  # folder where full docs will be saved

retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    byte_store=store,
    id_key="doc_id"
)
```

### What this gives you:

* Documents are saved as files under `./parent_docs/`
* They survive restarts, crashes, and environment reloads
* No change in retrieval logic

---

# 📁 Folder structure after storing documents

If you store documents with IDs like `"doc1"` and `"doc2"`, your folder may look like:

```
parent_docs/
  doc1
  doc2
  doc3
```

Each file contains the serialized LangChain `Document`.

---

# ✨ **Option 2 — Use a real database-based store**

You can also use any store based on the Key-Value store interface, such as:

### ✔ `PostgresByteStore`

### ✔ `RedisByteStore`

### ✔ `S3ByteStore`

For example, with Redis:

```python
from langchain_community.storage import RedisByteStore

store = RedisByteStore(
    redis_url="redis://localhost:6379",
    namespace="original_docs"
)
```

Or with Amazon S3:

```python
from langchain_community.storage import S3ByteStore

store = S3ByteStore(
    bucket="my-doc-bucket",
    prefix="original_docs/"
)
```

---

# 🌟 **Option 3 — Store documents inline in the vectorstore metadata**

If documents are small (not recommended for long docs):

```python
vectorstore.add_texts(
    texts=[summary],
    metadatas=[{"doc_id": "doc1", "full_doc": original_doc_text}]
)
```

Not ideal for large content.

---

# 🧠 **Most common production setup**

For real-world systems:

* **Summaries → Chroma Vectorstore**
* **Original docs → LocalFileStore or S3ByteStore**
* **Retriever → MultiVectorRetriever connecting both**

Example:

```python
vectorstore = Chroma(
    collection_name="summaries",
    embedding_function=OpenAIEmbeddings()
)

store = LocalFileStore("parent_docs")  # persistent disk storage

retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    byte_store=store,
    id_key="doc_id",
)
```

---

# ⚠️ Important Note

`InMemoryByteStore` is **not persistent**:

* Data is lost when Python shuts down
* Not usable in production setups

To store documents *permanently*, always use:

* `LocalFileStore` (disk persistence)
* `S3ByteStore` (cloud persistence)
* `RedisByteStore` (Redis persistence)
* `PostgresByteStore` (database persistence)






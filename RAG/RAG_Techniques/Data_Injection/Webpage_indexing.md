# WebBaseLoader
- https://levelup.gitconnected.com/building-the-entire-rag-ecosystem-and-optimizing-every-component-8f23349b96a4#b6f7

## method 1 - text_splitter = RecursiveCharacterTextSplitter
~~~
import bs4
from langchain_community.document_loaders import WebBaseLoader

# Initialize a web document loader with specific parsing instructions
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),  # URL of the blog post to load
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")  # Only parse specified HTML classes
        )
    ),
)

# Load the filtered content from the web page into documents
docs = loader.load()

~~~

The bs_kwargs argument helps us target only the relevant HTML tags (post-content, post-title, etc.), cleaning up our data from the start.

Now that we have the document, we face our first challenge. Feeding a massive document directly into an LLM is inefficient and often impossible due to context window limits.

This is why chunking is a critical step. We need to break the document into smaller, semantically meaningful pieces.

The RecursiveCharacterTextSplitter is the recommended tool for this job because it intelligently tries to keep paragraphs and sentences intact.

~~~
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Create a text splitter to divide text into chunks of 1000 characters with 200-character overlap
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Split the loaded documents into smaller chunks
splits = text_splitter.split_documents(docs)
~~~

With chunk_size=1000, we are creating chunks of 1000 characters, and chunk_overlap=200 ensures there is some continuity between them, which helps preserve context.


## method 2 - RecursiveCharacterTextSplitter.from_tiktoken_encoder

~~~
# Load the blog post
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
blog_docs = loader.load()

# Split the documents into chunks
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=300, 
    chunk_overlap=50
)
splits = text_splitter.split_documents(blog_docs)

# Index the chunks in a Chroma vector store
vectorstore = Chroma.from_documents(documents=splits, 
                                    embedding=OpenAIEmbeddings())

# Create our retriever
retriever = vectorstore.as_retriever()
~~~





## Comparison From AI

Here’s a careful explanation of **when to use `RecursiveCharacterTextSplitter` vs `RecursiveCharacterTextSplitter.from_tiktoken_encoder`**, with pros and cons for each.

---

## **1️⃣ `RecursiveCharacterTextSplitter` (character-based)**

```python
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
```

### **How it works**

* Splits **by characters**, optionally respecting sentence or paragraph boundaries.
* `chunk_size` is in **characters**, `chunk_overlap` in **characters**.

### **When to use**

* You **don’t care about exact token counts** for an LLM.
* Your **documents are small or uniform** in size.
* You are doing general text processing or indexing.
* You want a **simple, fast splitter** that doesn’t require token libraries.

### **Pros**

* Simple and fast
* No external dependency on `tiktoken`
* Works for any text, including very small snippets

### **Cons**

* Not precise for LLM token limits (1 token ≈ 4 characters on average, but varies)
* Large chunks may exceed the LLM context window if you only consider characters
* Overlap may not align with token boundaries

---

## **2️⃣ `RecursiveCharacterTextSplitter.from_tiktoken_encoder` (token-based)**

```python
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=300,
    chunk_overlap=50
)
```

### **How it works**

* Splits based on **tokens** instead of raw characters.
* Uses `tiktoken` to **count the actual tokens** that an LLM like GPT will see.
* `chunk_size` and `chunk_overlap` are in **tokens**, not characters.

### **When to use**

* You want **precise control over token limits** for LLMs.
* Feeding text into models like GPT-3.5, GPT-4, or other token-limited LLMs.
* Working with **long documents** where exceeding context length could cause truncation.
* When **prompting LLMs directly** with chunks and token cost matters.

### **Pros**

* Accurate for LLM input
* Avoids exceeding model context window
* Prevents silent truncation of important content

### **Cons**

* Slightly slower (requires tokenization via `tiktoken`)
* Requires installing `tiktoken`
* Not necessary for tasks that are not LLM-dependent

---

## **3️⃣ Decision Table**

| Criteria           | Character-based (`RecursiveCharacterTextSplitter`) | Token-based (`from_tiktoken_encoder`) |
| ------------------ | -------------------------------------------------- | ------------------------------------- |
| Chunk size unit    | Characters                                         | Tokens                                |
| Suitable for LLMs  | Only if approximate chunking is okay               | Yes, precise                          |
| Large documents    | May overrun context window                         | Safely respects context limits        |
| Speed / simplicity | Fast, no dependencies                              | Slightly slower, needs `tiktoken`     |
| Use case examples  | Indexing, search, general preprocessing            | Prompting GPT, fine-grained LLM input |

---

### **💡 Rule of Thumb**

* **Use token-based (`from_tiktoken_encoder`)** → if the text will be sent to an LLM.
* **Use character-based (`RecursiveCharacterTextSplitter`)** → for general-purpose text splitting, search indexing, or non-LLM tasks.

---

If you want, I can make a **visual diagram showing token-based vs character-based splitting** with an example of how the same text would be chunked differently. It’s very eye-opening.

Do you want me to do that?


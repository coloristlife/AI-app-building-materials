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

## method 3 - partition_html
- https://levelup.gitconnected.com/building-an-advanced-agentic-rag-pipeline-that-mimics-a-human-thought-process-687e1fd79f61
- https://github.com/FareedKhan-dev/agentic-rag/

- ### Step 1.1: Advanced Document Parsing

**What we are going to do:**
We will use the `unstructured` library to parse the raw HTML filings. Unlike simple text extraction, `unstructured` partitions the document into a list of meaningful 'elements' such as `Title`, `NarrativeText`, `ListItem`, and `Table`. This preservation of structural information is the first and most critical step towards intelligent chunking.


~~~
def parse_html_file(file_path: str) -> List[Dict]:
    """Parses an HTML file using unstructured and returns a list of elements."""
    try:
        elements = partition_html(filename=file_path, infer_table_structure=True, strategy='fast')
        return [el.to_dict() for el in elements]
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return []

# Let's parse the most recent 10-K filing as an example
ten_k_file = [f for f in all_files if "10-K" in f][0]
print(f"Parsing file: {ten_k_file}...")

parsed_elements = parse_html_file(ten_k_file)

print(f"\nSuccessfully parsed into {len(parsed_elements)} elements.")
print("\n--- Sample Elements ---")

# Print a few sample elements to inspect their type and content
for i, element in enumerate(parsed_elements[20:25]): # Show a slice of elements
    elem_type = element.get('type', 'N/A')
    text_snippet = element.get('text', '')[:100].replace('\n', ' ') + '...'
    print(f"Element {i+20}: [Type: {elem_type}] - Content: '{text_snippet}'")
~~~

output:
Successfully parsed into 6328 elements.

--- Sample Elements ---
Element 20: [Type: Title] - Content: 'Table of Contents'...
Element 21: [Type: NarrativeText] - Content: 'UNITED STATES SECURITIES AND EXCHANGE COMMISSION Washington, D.C. 20549'...
Element 22: [Type: Title] - Content: 'FORM 10-K'...
Element 23: [Type: NarrativeText] - Content: '(Mark One)'...
Element 24: [Type: NarrativeText] - Content: '☒ ANNUAL REPORT PURSUANT TO SECTION 13 OR 15(d) OF THE SECURITIES EXCHANGE ACT OF 1934'...

**Discussion of the Output:**
The output shows that we have successfully partitioned the 10-K document into thousands of individual elements. The sample output is crucial: it demonstrates that `unstructured` has identified different types of content. We can see `Title` and `NarrativeText`. This structural awareness is what we will leverage in the next step to create more intelligent chunks, especially for preserving tables.

### Step 1.2: Intelligent, Structure-Aware Chunking

**What we are going to do:**
Standard chunking methods (like splitting by a fixed token count) can be destructive, especially for financial documents where tables are critical. A table split in half loses all its meaning. We will use `unstructured`'s `chunk_by_title` strategy. This method is more intelligent: it groups text under headings and, importantly, attempts to keep tables whole, treating them as atomic units.

A table split in half loses all its meaning. This structure-aware chunking method is our defense against destroying critical tabular data during the ingestion process.

~~~
# Convert the dictionary elements back to unstructured Element objects for chunking
from unstructured.documents.elements import element_from_dict

elements_for_chunking = [element_from_dict(el) for el in parsed_elements]

# Chunk the elements using the chunk_by_title strategy
chunks = chunk_by_title(
    elements_for_chunking,
    max_characters=2048,      # Max size of a chunk
    combine_text_under_n_chars=256, # Combine small text elements
    new_after_n_chars=1800  # Start a new chunk if the current one is getting too big
)

print(f"Document chunked into {len(chunks)} sections.")

print("\n--- Sample Chunks ---")

# Find and print a sample text chunk and a sample table chunk
text_chunk_sample = None
table_chunk_sample = None

for chunk in chunks:
    if 'text_as_html' not in chunk.metadata.to_dict() and text_chunk_sample is None and len(chunk.text) > 500:
        text_chunk_sample = chunk
    if 'text_as_html' in chunk.metadata.to_dict() and table_chunk_sample is None:
        table_chunk_sample = chunk
    if text_chunk_sample and table_chunk_sample:
        break

if text_chunk_sample:
    print("** Sample Text Chunk **")
    print(f"Content: {text_chunk_sample.text[:500]}...")
    print(f"Metadata: {text_chunk_sample.metadata.to_dict()}")

if table_chunk_sample:
    print("\n** Sample Table Chunk **")
    # For tables, the HTML representation is often more useful
    print(f"HTML Content: {table_chunk_sample.metadata.text_as_html[:500]}...")
    print(f"Metadata: {table_chunk_sample.metadata.to_dict()}")
~~~

Here, we first convert our list of dictionaries back into unstructured Element objects. Then, we pass them to chunk_by_title. The parameters allow us to control the approximate size of our chunks while giving the algorithm the flexibility to respect the document natural boundaries.

Document chunked into 371 sections.

--- Sample Chunks ---
** Sample Text Chunk **
Content: ITEM 1. BUSINESS

GENERAL

Microsoft is a technology company whose mission is to empower every person and every organization on the planet to achieve more. We strive to create local opportunity, growth, and impact in every country around the world. We are a global company and have offices in more than 100 countries. Our platform and tools help drive small business productivity, large business competitiveness, and public-sector efficiency. They also support new startups, improve educational and health outcomes, and empower human...
Metadata: {'filetype': 'text/html', 'page_number': 1, 'filename': 'full-submission.txt'}

** Sample Table Chunk **
~~~
HTML Content: <table><tr><td align="left" rowspan="2"></td><td align="center" colspan="3">For the Fiscal Year Ended June 30,</td><td align="center" colspan="2">Percentage Change</td></tr><tr><td align="center">2023</td><td align="center">2022</td><td align="center">2021</td><td align="center">2023 vs 2022</td><td align="center">2022 vs 2021</td></tr><tr><td align="left">Server products and cloud services</td><td align="center">$ 79,285</td><td align="center">$ 67,402</td><td align="center">$ 52,580</td><td align="center">18 %</td><td ali...
Metadata: {'filetype': 'text/html', 'page_number': 3, 'filename': 'full-submission.txt', 'text_as_html': '<table><tr><td align="left" rowspan="2"></td><td align="center" colspan="3">For the Fiscal Year Ended June 30,</td><td align="center" colspan="2">Percentage Change</td></tr><tr><td align="center">2023</td><td align="center">2022</td><td align="center">2021</td><td align="center">2023 vs 2022</td><td align="center">2022 vs 2021</td></tr><tr><td align="left">Server products and cloud services</td><td align="center">$ 79,285</td><td align="center">$ 67,402</td><td align="center">$ 52,580</td><td align="center">18 %</td><td align="center">28 %</td></tr><tr><td align="left">Office products and cloud services</td><td align="center">48,688</td><td align="center">44,863</td><td align="center">39,871</td><td align="center">9 %</td><td align="center">13 %</td></tr><tr><td align="left">Windows</td><td align="center">21,507</td><td align="center">24,737</td><td align="center">22,488</td><td align="center">(13) %</td><td align="center">10 %</td></tr><tr><td align="left">Gaming</td><td align="center">15,465</td><td align="center">16,230</td><td align="center">15,370</td><td align="center">(5) %</td><td align="center">6 %</td></tr><tr><td align="left">LinkedIn</td><td align="center">15,147</td><td align="center">13,816</td><td align="center">10,289</td><td align="center">10 %</td><td align="center">34 %</td></tr><tr><td align="left">Search and news advertising</td><td align="center">12,231</td><td align="center">11,591</td><td align="center">9,267</td><td align="center">6 %</td><td align="center">25 %</td></tr><tr><td align="left">Enterprise Services</td><td align="center">7,548</td><td align="center">7,407</td><td align="center">6,943</td><td align="center">2 %</td><td align="center">7 %</td></tr><tr><td align="left">Devices</td><td align="center">5,541</td><td align="center">6,991</td><td align="center">7,143</td><td align="center">(21) %</td><td align="center">(2) %</td></tr><tr><td align="left">Other</td><td align="center">5,992</td><td align="center">4,498</td><td align="center">3,767</td><td align="center">33 %</td><td align="center">19 %</td></tr><tr><td align="left" style="padding-left: 24px">Total revenue</td><td align="center">$ 211,915</td><td align="center">$ 198,270</td><td align="center">$ 168,088</td><td align="center">7 %</td><td align="center">18 %</td></tr></table>'}
~~~


**Discussion of the Output:**
The output shows we have reduced thousands of elements into a few hundred more manageable chunks. The key takeaway is in the sample chunks. We see a standard text chunk, and more importantly, a table chunk. Notice the table chunk's metadata includes `text_as_html`. This indicates that `unstructured` has correctly identified and preserved a table, which is a massive win for data quality. We have successfully avoided destroying critical tabular data during the chunking process.

### Step 1.3: Multi-faceted LLM-Powered Enrichment

This step is a cornerstone of our advanced RAG pipeline. Standard RAG simply embeds the raw text of a chunk. We can do much better. Instead of relying solely on the raw text, we will use a fast and powerful LLM to generate rich metadata for each and every chunk.

<img width="2000" height="448" alt="image" src="https://github.com/user-attachments/assets/e2e8c115-aa8d-4486-b1ed-ad891d6522d7" />

We will create a process to generate a summary, keywords, a list of hypothetical questions the chunk could answer, and a special natural-language summary for tables. This metadata acts as a layer of machine-generated understanding, which we will embed alongside the raw text.

This injects the LLM understanding directly into the vector representation, allowing our retrieval system to match based on conceptual meaning, not just keyword overlap.



**What we are going to do:**
This is a cornerstone of our advanced RAG pipeline. Instead of just embedding raw text, we will use a fast and powerful LLM to generate rich metadata for each chunk. This metadata acts as extra 'signals' for our retrieval system, allowing it to understand the content at a much deeper level.

For each chunk, we will generate:
1.  **Summary:** A concise, 1-2 sentence summary.
2.  **Keywords:** A list of key topics.
3.  **Hypothetical Questions:** A list of questions that the chunk can answer.
4.  **Table Summary (for tables only):** A natural language description of the table's key insights.

We'll use Pydantic to define the desired JSON structure, ensuring the LLM's output is reliable.

~~~
class ChunkMetadata(BaseModel):
    """Structured metadata for a document chunk."""
    summary: str = Field(description="A concise 1-2 sentence summary of the chunk.")
    keywords: List[str] = Field(description="A list of 5-7 key topics or entities mentioned.")
    hypothetical_questions: List[str] = Field(description="A list of 3-5 questions this chunk could answer.")
    table_summary: Optional[str] = Field(description="If the chunk is a table, a natural language summary of its key insights.", default=None)

print("Pydantic model for metadata defined.")
print(ChunkMetadata.schema_json(indent=2))
~~~

We have defined the `ChunkMetadata` Pydantic model. Printing the JSON schema shows the exact structure, including field names, types, and descriptions, that we will request from the LLM. This use of structured output is far more reliable than simple prompt engineering.
~~~
# Initialize a powerful but fast LLM for the enrichment task
# gpt-4o-mini is a great choice for this kind of structured data generation
enrichment_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).with_structured_output(ChunkMetadata)

def generate_enrichment_prompt(chunk_text: str, is_table: bool) -> str:
    """Generates a prompt for the LLM to enrich a chunk."""
    table_instruction = """
    This chunk is a TABLE. Your summary should describe the main data points and trends, for example: 'This table shows a 15% year-over-year increase in revenue for the Cloud segment.'
    """ if is_table else ""

    prompt = f"""
    You are an expert financial analyst. Please analyze the following document chunk and generate the specified metadata.
    {table_instruction}
    Chunk Content:
    ---
    {chunk_text}
    ---
    """
    return prompt

def enrich_chunk(chunk) -> Dict[str, Any]:
    """Enriches a single chunk with LLM-generated metadata."""
    is_table = 'text_as_html' in chunk.metadata.to_dict()
    content = chunk.metadata.text_as_html if is_table else chunk.text
    
    # To avoid overwhelming the LLM, we'll truncate very long chunks
    truncated_content = content[:3000]
    
    prompt = generate_enrichment_prompt(truncated_content, is_table)
    
    try:
        metadata_obj = enrichment_llm.invoke(prompt)
        return metadata_obj.dict()
    except Exception as e:
        print(f"  - Error enriching chunk: {e}")
        return None

print("Enrichment functions and LLM are ready.")
~~~

~~~
print("--- Testing Enrichment on a Text Chunk ---")
enriched_text_meta = enrich_chunk(text_chunk_sample)
print(json.dumps(enriched_text_meta, indent=2))

print("\n--- Testing Enrichment on a Table Chunk ---")
enriched_table_meta = enrich_chunk(table_chunk_sample)
print(json.dumps(enriched_table_meta, indent=2))
~~~

This is what we are getting.
~~~
--- Testing Enrichment on a Text Chunk ---
{
  "summary": "Microsoft, a global technology company, aims to empower individuals and organizations worldwide...",
  "keywords": ["Microsoft", "technology company", "global operations", ...],
  "hypothetical_questions": ["What is Microsoft's mission statement?", ...],
  "table_summary": null
}

--- Testing Enrichment on a Table Chunk ---
{
  "summary": "This table presents Microsoft's revenue by major product and service categories...",
  "keywords": ["Revenue", "Fiscal Year", "Server products and cloud services", ...],
  "hypothetical_questions": ["What was Microsoft's total revenue in fiscal year 2023?", ...],
  "table_summary": "The table shows Microsoft's total revenue increased by 7% to $211.9 billion in fiscal year 2023..."
}
~~~

**Discussion of the Output:**
This is a fantastic result. The output shows two JSON objects, one for each chunk type.
- For the text chunk, we have a clear summary, relevant keywords, and insightful hypothetical questions.
- For the table chunk, the LLM has correctly identified it as a table and provided a `table_summary` that interprets the data in natural language. This is incredibly powerful. Now, a semantic search for "revenue growth by segment" could match this table, even if those exact words aren't in the raw HTML.

The LLM has generated high-quality, structured metadata for both types of content. For the table chunk, it has correctly provided a table_summary that interprets the data in natural language.

A user could now search for revenue growth by segment, and our system could match this table, even though those exact words don't appear in the raw HTML.


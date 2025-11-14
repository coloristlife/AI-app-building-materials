# WebBaseLoader
- https://levelup.gitconnected.com/building-the-entire-rag-ecosystem-and-optimizing-every-component-8f23349b96a4#b6f7

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

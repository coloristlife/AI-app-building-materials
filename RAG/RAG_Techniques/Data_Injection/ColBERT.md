- https://levelup.gitconnected.com/building-the-entire-rag-ecosystem-and-optimizing-every-component-8f23349b96a4#8177

# ColBERT

Token-Level Precision (ColBERT)
The Theory: Standard embedding models create a single vector for an entire chunk of text (this is called a “bag-of-words” approach). This can lose a lot of nuance.


<img width="720" height="406" alt="image" src="https://github.com/user-attachments/assets/f907206d-777a-4853-b104-ce9f4d794c1d" />

ColBERT (Contextualized Late Interaction over BERT) offers a more granular approach. It generates a separate, context-aware embedding for every single token in the document.


When you make a query, ColBERT also embeds every token in your query. Then, instead of comparing one document vector to one query vector, it finds the maximum similarity between each query token and any document token.


This “late interaction” allows for a much finer-grained understanding of relevance, excelling at keyword-style searches.

We can easily use ColBERT through the RAGatouille library.

~~~
# Install the required library
!pip install -U ragatouille

from ragatouille import RAGPretrainedModel

# Load a pre-trained ColBERT model
RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
~~~

Now, let’s index a Wikipedia page using ColBERT’s unique token-level approach.

~~~
import requests

def get_wikipedia_page(title: str):
    """A helper function to retrieve content from Wikipedia."""
    # Wikipedia API endpoint and parameters
    URL = "https://en.wikipedia.org/w/api.php"
    params = { "action": "query", "format": "json", "titles": title, "prop": "extracts", "explaintext": True }
    headers = {"User-Agent": "MyRAGApp/1.0"}
    response = requests.get(URL, params=params, headers=headers)
    data = response.json()
    page = next(iter(data["query"]["pages"].values()))
    return page.get("extract")

full_document = get_wikipedia_page("Hayao_Miyazaki")

# Index the document with RAGatouille. It handles the chunking and token-level embedding internally.
RAG.index(
    collection=[full_document],
    index_name="Miyazaki-ColBERT",
    max_document_length=180,
    split_documents=True,
)
~~~

The indexing process is more complex, as it’s creating embeddings for every token, but RAGatouille handles it seamlessly. Now, let's search our new index.

~~~
# Search the ColBERT index
results = RAG.search(query="What animation studio did Miyazaki found?", k=3)
print(results)


#### OUTPUT ####
[{'content': 'In April 1984, ...', 'score': 25.9036, 'rank': 1, ...}, 
 {'content': 'Hayao Miyazaki ...', 'score': 25.5716, 'rank': 2, ...},
 {'content': 'Glen Keane said ...', 'score': 24.8411, 'rank': 3, ...}]

~~~

The top result directly mentions the founding of Studio Ghibli. We can also easily wrap this as a standard LangChain retriever.

~~~
# Convert the RAGatouille model into a LangChain-compatible retriever
colbert_retriever = RAG.as_langchain_retriever(k=3)

# Use it like any other retriever
retrieved_docs = colbert_retriever.invoke("What animation studio did Miyazaki found?")
print(retrieved_docs[0].page_content)


#### OUTPUT ####
In April 1984, Miyazaki opened his own office in Suginami Ward, naming it Nibariki.

=== Studio Ghibli ===
==== Early films (1985–1996) ====
In June 1985, Miyazaki, Takahata, Tokuma and Suzuki founded the animation production company Studio Ghibli, with funding from Tokuma Shoten. Studio Ghibli's first film, Laputa: Castle in the Sky (1986), employed the same production crew of Nausicaä. Miyazaki's designs for the film's setting were inspired by Greek architecture and "European urbanistic templates".
~~~~

ColBERT provides a powerful, fine-grained alternative to traditional vector search, demonstrating that the way we build our library is just as important as how we search it.


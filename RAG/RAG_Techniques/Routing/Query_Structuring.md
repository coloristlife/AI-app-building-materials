- https://levelup.gitconnected.com/building-the-entire-rag-ecosystem-and-optimizing-every-component-8f23349b96a4#7992
  
# Query Structuring

So far, we’ve focused on retrieving from unstructured text. But most real-world data is semi-structured; it contains valuable metadata like dates, authors, view counts, or categories. A simple vector search can’t leverage this information.

Query Structuring is the technique of converting a natural language question into a structured query that can use these metadata filters for highly precise retrieval.

To illustrate, let’s look at the metadata available from a YouTube video transcript.

~~~~
from langchain_community.document_loaders import YoutubeLoader

# Load a YouTube transcript to inspect its metadata
docs = YoutubeLoader.from_youtube_url(
    "https://www.youtube.com/watch?v=pbAd8O1Lvm4", add_video_info=True
).load()

# Print the metadata of the first document
print(docs[0].metadata)


#### OUTPUT ####
{ 
  'source': 'pbAd8O1Lvm4',
  'title': 'Self-reflective RAG with LangGraph: Self-RAG and CRAG',
  'description': 'Unknown',
  'view_count': 11922,
  'thumbnail_url': 'https://i.ytimg.com/vi/pbAd8O1Lvm4/hq720.jpg',
  'publish_date': '2024-02-07 00:00:00',
  'length': 1058,
  'author': 'LangChain'
}
~~~~

This document has rich metadata: view_count, publish_date, length. We want our users to be able to filter on these fields using natural language. To do this, we'll define another Pydantic schema, this time for a structured video search query.

~~~
import datetime
from typing import Optional

class TutorialSearch(BaseModel):
    """A data model for searching over a database of tutorial videos."""

    # The main query for a similarity search over the video's transcript.
    content_search: str = Field(..., description="Similarity search query applied to video transcripts.")
    
    # A more succinct query for searching just the video's title.
    title_search: str = Field(..., description="Alternate version of the content search query to apply to video titles.")
    
    # Optional metadata filters
    min_view_count: Optional[int] = Field(None, description="Minimum view count filter, inclusive.")
    max_view_count: Optional[int] = Field(None, description="Maximum view count filter, exclusive.")
    earliest_publish_date: Optional[datetime.date] = Field(None, description="Earliest publish date filter, inclusive.")
    latest_publish_date: Optional[datetime.date] = Field(None, description="Latest publish date filter, exclusive.")
    min_length_sec: Optional[int] = Field(None, description="Minimum video length in seconds, inclusive.")
    max_length_sec: Optional[int] = Field(None, description="Maximum video length in seconds, exclusive.")

    def pretty_print(self) -> None:
        """A helper function to print the populated fields of the model."""
        for field in self.__fields__:
            if getattr(self, field) is not None:
                print(f"{field}: {getattr(self, field)}")
~~~

This schema is our target. We’ll now create a chain that takes a user question and fills out this model.


~~~
# System prompt for the query analyzer
system = """You are an expert at converting user questions into database queries. \
You have access to a database of tutorial videos about a software library for building LLM-powered applications. \
Given a question, return a database query optimized to retrieve the most relevant results.

If there are acronyms or words you are not familiar with, do not try to rephrase them."""

prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "{question}")])
structured_llm = llm.with_structured_output(TutorialSearch)

# The final query analyzer chain
query_analyzer = prompt | structured_llm
~~~

Let’s test this with a few different questions to see its power.

~~~
# Test 1: A simple query
query_analyzer.invoke({"question": "rag from scratch"}).pretty_print()

#### OUTPUT ####
content_search: rag from scratch
title_search: rag from scratch
~~~

As expected, it fills the content and title search fields. Now for a more complex query.

~~~
# Test 2: A query with a date filter
query_analyzer.invoke(
    {"question": "videos on chat langchain published in 2023"}
).pretty_print()


#### OUTPUT ####
content_search: chat langchain
title_search: chat langchain 2023
earliest_publish_date: 2023-01-01
latest_publish_date: 2024-01-01

~~~

This is brilliant. The LLM correctly interpreted “in 2023” and created a date range filter. Let’s try one more with a time constraint.

~~~
# Test 3: A query with a length filter
query_analyzer.invoke(
    {
        "question": "how to use multi-modal models in an agent, only videos under 5 minutes"
    }
).pretty_print()


#### OUTPUT ####
content_search: multi-modal models agent
title_search: multi-modal models agent
max_length_sec: 300
~~~

It perfectly converted “under 5 minutes” to max_length_sec: 300. This structured query can now be passed to a vector store that supports metadata filtering, allowing for incredibly precise and efficient retrieval that goes far beyond simple semantic search.






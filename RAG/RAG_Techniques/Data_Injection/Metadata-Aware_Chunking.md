- https://levelup.gitconnected.com/building-an-agentic-deep-thinking-rag-pipeline-to-solve-complex-queries-af69c5e044db#95ca

# Precision with Metadata-Aware Chunking

> But right now, our retriever can’t use that hint. Our vector store is just a big, flat list of 378 text chunks. It has no idea what a “section” is.

<img width="1100" height="408" alt="image" src="https://github.com/user-attachments/assets/643a7a09-5b16-4b8f-a7fd-f3b1d601f147" />

We need to fix this. We are going to rebuild our document chunks from scratch. This time, for every single chunk we create, we are going to add a label or a tag its metadata that tells our system exactly which section of the 10-K it came from. This will allow our agent to perform highly precise, filtered searches later on.

First things first, we need a way to programmatically find where each section begins in our raw text file. If we look at the document, we can see a clear pattern: every major section starts with the word “ITEM” followed by a number, like “ITEM 1A” or “ITEM 7”. This is a perfect job for a regular expression.

~~~
# This regex is designed to find section titles like 'ITEM 1A.' or 'ITEM 7.' in the 10-K text.
# It looks for the word 'ITEM', followed by a space, a number, an optional letter, a period, and then captures the title text.
# The `re.IGNORECASE | re.DOTALL` flags make the search case-insensitive and allow '.' to match newlines.
section_pattern = r"(ITEM\\s+\\d[A-Z]?\\.\\s*.*?)(?=\\nITEM\\s+\\d[A-Z]?\\.|$)"
~~~


We are basically creating a pattern that will act as our section detector. It should be designed so that it can be flexible enough to catch different formats while being specific enough not to grab the wrong text.

Now we can use this pattern to slice our document into two separate lists: one containing just the section titles, and another containing the content within each section.

~~~
# We'll work with the raw text loaded earlier from our Document object
raw_text = documents[0].page_content

# Use re.findall to apply our pattern and extract all section titles into a list
section_titles = re.findall(section_pattern, raw_text, re.IGNORECASE | re.DOTALL)

# A quick cleanup step to remove any extra whitespace or newlines from the titles
section_titles = [title.strip().replace('\\n', ' ') for title in section_titles]

# Now, use re.split to break the document apart at each point where a section title occurs
sections_content = re.split(section_pattern, raw_text, flags=re.IGNORECASE | re.DOTALL)

# The split results in a list with titles and content mixed, so we filter it to get only the content parts
sections_content = [content.strip() for content in sections_content if content.strip() and not content.strip().lower().startswith('item ')]
print(f"Identified {len(section_titles)} document sections.")

# This is a crucial sanity check: if the number of titles doesn't match the number of content blocks, something went wrong.
assert len(section_titles) == len(sections_content), "Mismatch between titles and content sections"~
~~~

This is a very effective way to parse a semi-structured document. We have used our regex pattern twice: once to get a clean list of all the section titles, and again to split the main text into a list of content blocks. The assert statement gives us confidence that our parsing logic is sound.

Okay, now we have the pieces: a list of titles and a corresponding list of contents. We can now loop through them and create our final, metadata-rich chunks.

~~~
import uuid # We'll use this to give each chunk a unique ID, which is good practice

# This list will hold our new, metadata-rich document chunks
doc_chunks_with_metadata = []

# Loop through each section's content along with its title using enumerate
for i, content in enumerate(sections_content):
    # Get the corresponding title for the current content block
    section_title = section_titles[i]
    # Use the same text splitter as before, but this time, we run it ONLY on the content of the current section
    section_chunks = text_splitter.split_text(content)
    
    # Now, loop through the smaller chunks created from this one section
    for chunk in section_chunks:
        # Generate a unique ID for this specific chunk
        chunk_id = str(uuid.uuid4())
        # Create a new LangChain Document object for the chunk
        doc_chunks_with_metadata.append(
            Document(
                page_content=chunk,
                # This is the most important part: we attach the metadata
                metadata={
                    "section": section_title,      # The section this chunk belongs to
                    "source_doc": doc_path_clean,  # Where the document came from
                    "id": chunk_id                 # The unique ID for this chunk
                }
            )
        )



print(f"Created {len(doc_chunks_with_metadata)} chunks with section metadata.")
print("\n--- Sample Chunk with Metadata ---")

# To prove it worked, let's find a chunk that we know should be in the 'Risk Factors' section and print it
sample_chunk = next(c for c in doc_chunks_with_metadata if "Risk Factors" in c.metadata.get("section", ""))
print(sample_chunk)
~~~

This is the core of our upgrade. We iterate through each section one by one. For each section, we create our text chunks. But before we add them to our final list, we create a metadata dictionary and attach the section_title. This effectively tags every single chunk with its origin.

Let’s look at the output and see the difference.

~~~
#### OUTPUT ####
Processing document and adding metadata...
Identified 22 document sections.
Created 381 chunks with section metadata.


--- Sample Chunk with Metadata ---
Document(
│   page_content='Our industry is intensely competitive. We operate in the semiconductor\\nindustry, which is intensely competitive and characterized by rapid\\ntechnological change and evolving industry standards. We compete with a number of\\ncompanies that have different business models and different combinations of\\nhardware, software, and systems expertise, many of which have substantially\\ngreater resources than we have. We expect competition to increase from existing\\ncompetitors, as well as new and emerging companies. Our competitors include\\nIntel, AMD, and Qualcomm; cloud service providers, or CSPs, such as Amazon Web\\nServices, or AWS, Google Cloud, and Microsoft Azure; and various companies\\ndeveloping or that may develop processors or systems for the AI, HPC, data\\ncenter, gaming, professional visualization, and automotive markets. Some of our\\ncustomers are also our competitors. Our business could be materially and\\nadversely affected if our competitors announce or introduce new products, services,\\nor technologies that have better performance or features, are less expensive, or\\nthat gain market acceptance.',
│   metadata={
│   │   'section': 'Item 1A. Risk Factors.',
│   │   'source_doc': './data/nvda_10k_2023_clean.txt',
│   │   'id': '...'
│   }
)
~~~

Look at that metadata block. The same chunk of text we had before now has a piece of context attached: 'section': 'Item 1A. Risk Factors.'.

Now, when our agent needs to find risks, it can tell the retriever, “Hey, don’t search all 381 chunks. Just search the ones where the section metadata is ‘Item 1A. Risk Factors”.

This simple change transforms our retriever from a blunt instrument into a surgical tool, and it is a key principle for building truly production-grade RAG systems.


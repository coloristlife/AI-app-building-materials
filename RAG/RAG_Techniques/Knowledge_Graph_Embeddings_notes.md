- https://kge-tutorial-ecai2020.github.io/ECAI-20_KGE_tutorial.pdf

# Knowledge Graph Embeddings (KGE)

<img width="1186" height="678" alt="image" src="https://github.com/user-attachments/assets/2893fcef-907f-4925-a7d2-570a96bc8fb2" />

<img width="1204" height="602" alt="image" src="https://github.com/user-attachments/assets/dcb85c99-e473-4b0b-8d9b-f734300d15fb" />

- https://medium.com/@doubletaken/understanding-knowledge-graph-embeddings-methods-applications-and-differences-from-llm-db6078323f39

---

## What Are Knowledge Graph Embeddings?

A **Knowledge Graph (KG)** is a structured representation of knowledge, where entities (nodes) are connected by relationships (edges). **Knowledge Graph Embeddings (KGE)** transform these entities and relationships into dense vector spaces while preserving their structural properties. This enables downstream tasks such as link prediction, entity classification, and relationship inference.

---

## Key KGE Methods

Several approaches exist for knowledge graph embedding, each with unique strengths and weaknesses:

### 1. TransE

* Introduced by Bordes et al. (2013), TransE models relations as translations in vector space.
* If a triple *(h, r, t)* holds, then ideally, the embedding vectors satisfy: **h + r ≈ t**
* Efficient and interpretable but struggles with many-to-many relationships.

### 2. DistMult

* Introduces matrix-based relation representations.
* Works well for symmetric relations but struggles with asymmetry.

### 3. ComplEx

* Extends DistMult by using complex-valued embeddings to capture asymmetric relations.
* The score function includes both real and imaginary components.

### 4. ConvE

* Uses 2D convolutional neural networks (CNNs) to capture interaction patterns between entities and relations.
* More expressive but computationally heavier.

---

## Applications of KGE

### 1. Link Prediction

Predict missing connections in a knowledge graph (e.g., “Paris is the capital of ?”).

### 2. Entity Classification

Assign labels or types to entities based on their embeddings.

### 3. Relationship Inference

Discover new relationships between entities.

---


# from AI
~~~
Embeddings derived from knowledge graphs allow semantic and structural retrieval: the query doesn’t have to match words exactly — the embedding can capture relationships and context.


Graph embeddings can improve retrieval precision and recall when queries involve entities, relations, multi‐hop semantics rather than simple keyword lookup.


However: These systems often require hybrid architectures: vector similarity + graph traversal + full-graph query logic. Pure KG embedding usage for retrieval is still emerging.


The design of the knowledge graph (entities, relations, quality of extraction) matters a lot for retrieval usefulness.

~~~

- https://memgraph.com/docs/ai-ecosystem/graph-rag/knowledge-retrieval
  
# Knowledge retrieval from Memgraph



# **Retrieval types**

Finding relevant data in the vast amount of nodes and relationships in your graph is not easy, and that’s why Memgraph has a couple of strategies to facilitate that.

While searching for a certain information it is important to know where to start, how to find the node in the graph which will best describe what you’re looking for. The search for that starting point or a pivot node can also be called a pivot search. Once you get to the pivot node, you have located yourself in the part of the knowledge graph that holds relevant information. There are various strategies to find a pivot node, some of which we are listing below.

Pivot search can be just a start of your journey to provide valuable context to the LLM to ground it and in that way avoid hallucinations. Additionally, to expand the search, you can perform relevance expansion which includes advanced strategies to obtain relevant information.

Pivot search combined with relevance expansion is generally more reliable than directly generating Cypher queries from natural language. These approaches can leverage pre-built tools to ensure the resulting query is accurate and contextually appropriate. To improve Cypher query generation from natural language, effective prompt engineering is essential.

---

## **Pivot search**

Pivot search is the starting point of any retrieval process, identifying the core entities and relationships relevant to your query.

---

## **Vector search**

This retrieval method uses vector embeddings to find entities based on semantic similarity rather than exact matches. It’s ideal for scenarios where meaning, context, or relatedness is more important than specific terms (e.g., finding similar topics or concepts).

**vector-search**

Perform vector search on your knowledge graph to extract semantically similar nodes, setting the foundation for more advanced retrieval.

**Query example:**

> Which European city is known for its romantic atmosphere and iconic landmarks like the Eiffel Tower?

Vector search matches nodes semantically associated with “romantic atmosphere” and “iconic landmarks”, leading to nodes like **Paris**.

**Read more**

* [Vector search docs]
* [Simplify Data Retrieval with Memgraph’s Vector Search]
* [Building a Movie Similarity Search Engine with Vector Search in Memgraph]

---

## **Text search (experimental)**

Currently, in Memgraph, text search is a retrieval technique that finds nodes with their properties based on exact text matches. It’s best used for queries involving specific terms, phrases, or entity names (e.g., “Find all nodes containing the keyword ‘climate change’”).

**text-search**

Use text search as a direct approach to narrow down specific nodes before expanding context.

**Query example:**

> What is the capital of France?

Text search can find all nodes that have **France** as their property value.

**Read more in text search docs.**

---

## **Geospatial search**

Geospatial search enables you to integrate and retrieve location-based insights, making it a valuable tool for applications involving geographic data. This functionality relies on the ability to store **Point** types representing locations with latitude and longitude and on leveraging **point indexes** to ensure optimized query performance, allowing for quick proximity and spatial queries.

**geospatial**

**Query example:**

> Find cities within 50 km of Paris.

Geospatial search retrieves cities based purely on proximity to Paris, in this case, **Versailles**.

---

## **Hybrid knowledge retrieval**

Combines multiple retrieval methods — such as text search, vector search, and geospatial search — for enhanced precision and versatility. It’s perfect for multi-dimensional queries involving semantic meaning, specific terms, and spatial constraints.

Hybrid retrieval is particularly valuable in complex queries where results must satisfy multiple dimensions simultaneously. For example:

> Find all nearby Italian restaurants with excellent reviews and vegetarian options.

---

## **Relevance expansion**

Relevance expansion techniques allow you to extract deeper insights from your graph by analyzing related entities and connections beyond the initial query. This step is optional but can significantly enhance the quality of responses in a GraphRAG system.

### **Why you should broaden the search**

* LLMs can deliver more accurate responses with expanded, meaningful data.
* Customize the retrieval process to align with the specific needs of your application.
* Extract more value from the semantic connections in your graph.


- https://articles.chatnexus.io/knowledge-base/graph-rag-leveraging-knowledge-graphs-for-enhanced/

The integration of knowledge graphs (KGs) with Retrieval-Augmented Generation (RAG) systems creates a hybrid architecture, often referred to as Graph RAG, that balances the semantic power of embeddings with deterministic logic.

This integration is generally achieved through a three-phase process: Entity Recognition and Linking, Graph-Assisted Retrieval, and Prompt Construction.

### 🔗 Phase 1: Entity Recognition and Linking

The initial step focuses on identifying key concepts and mapping them to the structured data within the knowledge graph:

*   **NER Models:** Named Entity Recognition (NER) models are used to identify entities present in both user queries and document chunks.
*   **Entity Linking:** Identified entity mentions are mapped to their unique nodes within the knowledge graph (e.g., linking the phrase “Service B” to its designated graph node).
    *   This process helps resolve ambiguity (e.g., distinguishing "Apple" the company from "apple" the fruit).

### 🔎 Phase 2: Graph-Assisted Retrieval

Once entities are linked, the knowledge graph is used to expand the context retrieved beyond simple semantic similarity. The combined approach improves both precision and recall.

#### Retrieval Techniques

Knowledge graph structure enables specific retrieval techniques that leverage entities and their relations (edges):

1.  **Graph Expansion:** Given an entity from the query, the system retrieves connected nodes up to a specified number of *n* hops. After identifying these related nodes, associated document chunks linked to them are fetched.
    *   **1-Hop Expansion:** This technique includes documents linked to query entities within just one edge, effectively capturing direct relationships. For example, retrieving product specification sheets by following "has\_component" edges from a product entity.
    *   **n-Hop Path Finding:** This involves traversing multi-edge paths to uncover complex, indirect connections. This allows the RAG system to answer multi-step queries, such as tracing all services affected if a specific vendor goes offline (Vendor C $\to$ provides Service B $\to$ underpins Service D).
2.  **Relation Filtering:** Retrieval can be limited to documents or paths connected via specific types of relations (e.g., filtering only for relations like “authored\_by”), which improves precision for highly targeted queries.
3.  **Subgraph Ranking:** Graph metrics are used to identify the specific clusters or subgraphs that are most relevant to the user's intent, thereby focusing retrieval on high-value information.

#### Hybrid Scoring

The final retrieved documents are scored using a combination of methods:

*   **Semantic Similarity:** Cosine similarity from the semantic embeddings is used for standard relevance matching.
*   **Graph-Based Relevance:** This is combined with deterministic graph metrics, such as PageRank or node centrality.
*   **Balancing Weights:** Best practices recommend tuning these hybrid scoring weights to optimize performance for the specific domain, as some queries benefit more from graph logic while others benefit more from embedding similarity.

### 📝 Phase 3: Prompt Construction

After gathering relevant text chunks and graph information, the context is prepared for the language model:

*   **Structured Context Insertion:** The graph context—the explicit relationships and paths found—is inserted into the prompt as structured blocks.
    *   *Example Insertion:* `[GRAPH CONTEXT] (Contract A governs Service B) (Service B provided_by Vendor C)`.
*   **Guidance for Reasoning:** This structured information guides the RAG model to reason explicitly over both the retrieved unstructured text and the deterministic graph facts.
*   **Explainability:** By providing these paths, the model can cite the exact connections (e.g., "cites" paths), enhancing lawyer confidence and improving explainability of the responses.

Platforms like ChatNexus.io streamline this process by providing features such as Managed Ontology Services, a unified GraphQL-Style Retrieval API to query both vectors and graph paths, and configuration tools for Hybrid Scoring.






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



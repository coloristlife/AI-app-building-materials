- https://graphacademy.neo4j.com/courses/graph-data-science-fundamentals/1-graph-algorithms/2-centrality-and-importance/

## Centrality and Importance

Centrality algorithms are used to determine the importance of distinct nodes in a graph.

Common use cases of centrality include:

- Recommendations: Identify and recommend the most influential or popular items in your content or product offering catalog

- Supply chain analytics: find the most critical node in your supply chain, whether it be a supplier in a network, a raw material that is part of a manufactured product, or a port in a route

- Fraud & Anomaly Detection: Find users with many shared identifiers or who otherwise act as a bridge between many communities

**Degree Centrality Example**
Degree centrality is one of the most ubiquitous and simple centrality algorithms. It counts the number of relationships a node has. In the GDS implementation, we specifically calculate out-degree centrality which is the count of outgoing relationships from a node. Below is an example of using degree centrality to count the number of movies each actor has acted in.

> From AI
> What is Degree Centrality?

> Degree Centrality is one of the simplest ways to measure how “important” or “connected” a node is within a graph.

> It counts how many relationships (edges) a node has.

> In a directed graph, there are two types:

> - Out-degree → number of outgoing relationships.

> - In-degree → number of incoming relationships.

> In the following example, Neo4j’s GDS implementation calculates out-degree centrality — i.e., how many outgoing relationships each node has.

During this module, you will be using a movie recommendations dataset that contains information about movies, actors, and users who have rated movies.

<img width="332" height="256" alt="image" src="https://github.com/user-attachments/assets/4fdc77d7-9aa3-4d8c-abb9-0fb810160051" />

To use a GDS algorithm, you must first create a graph projection. A projection is an in-memory graph you can quickly query and manipulate.

Create a graph projection of Actor and Movie nodes:

~~~
CALL gds.graph.project(
  'proj',
  ['Actor','Movie'],
  'ACTED_IN'
  );
~~~

What this does:

gds.graph.project creates an in-memory projection of part of your Neo4j database.

It doesn’t copy all data — just the parts you need for the algorithm.

Parameters explained:

'proj' → the name of this temporary in-memory graph.

['Actor','Movie'] → node labels to include in the projection.

'ACTED_IN' → relationship type to include.

Let’s take a small part of the graph:

(:Actor {name: "Robert De Niro"})-[:ACTED_IN]->(:Movie {title: "Heat"})
(:Actor {name: "Robert De Niro"})-[:ACTED_IN]->(:Movie {title: "Goodfellas"})


Here:

Each ACTED_IN relationship goes from an Actor to a Movie.

Robert De Niro has 2 outgoing relationships → his out-degree = 2.

If we were to measure in-degree, then each Movie node would have an in-degree equal to the number of actors in it.

Then stream the degree centrality to find the actors who have acted in the most movies:

~~~
//get top 5 most prolific actors (those in the most movies)
//using degree centrality which counts number of `ACTED_IN` relationships
CALL gds.degree.stream('proj')
YIELD nodeId, score
RETURN
  gds.util.asNode(nodeId).name AS actorName,
  score AS numberOfMoviesActedIn
ORDER BY numberOfMoviesActedIn DESCENDING, actorName LIMIT 5
~~~
gds.degree.stream('proj') runs the degree centrality algorithm on the projected graph named 'proj'.

It outputs:

nodeId → the internal ID of each node in the projection.

score → the degree centrality value (number of outgoing relationships).

The top three actors should be "Robert De Niro", "Bruce Willis", and "Nicolas Cage."


**PageRank Example**
Another common centrality algorithm is PageRank. PageRank is a good algorithm for measuring the influence of nodes in a directed graph, particularly where the relationships imply some form of flow of movement such as in payment networks, supply chain and logistics, communications, routing, and graphs of website and links.

In summary, PageRank estimates the importance of a node by counting the number of incoming relationships from neighboring nodes weighted by the importance and out-degree centrality of those neighbors. The underlying assumption is that more important nodes are likely to have proportionately more incoming relationships from other important nodes. Our PageRank documentation offers a thorough technical explanation of PageRank if you are interested in digging in deeper.

## 🧠 1. What is PageRank?

**PageRank** is a **centrality algorithm** that measures how *influential* or *important* a node is in a **directed graph**.

It was originally developed by Google to rank web pages:

* A web page is important if **many other important pages link to it**.
* Links from *important pages* count more than links from *less important pages*.

That same logic works in many types of networks — not just websites:

* Payment networks (who sends money to whom)
* Communication networks (who talks to whom)
* Citation networks (who cites whom)
* **Movie networks** (who directs or acts with whom)

---

## ⚙️ 2. How PageRank Works (Conceptually)

The algorithm works like this:

1. Each node starts with a base “rank” or score.
2. Importance “flows” through incoming relationships.
3. A node’s final **PageRank score** depends on:

   * The number of **incoming relationships** it has.
   * The **importance** of the nodes pointing to it.
   * How many **outgoing links** those source nodes have (because their influence is divided among all their outgoing edges).

In other words:

> “You are important if important people point to you.”

So PageRank gives you a **weighted measure of influence**, not just a simple count like degree centrality.



Below is an example of applying PageRank to find the most influential persons in the Director → Actor network from movies released on or after 1990 with a revenue of at least 10 Million dollars.

First, create the graph projection. We can use a Cypher projection to create an in-memory graph with :DIRECTED_ACTOR relationships between two (:Person) nodes. This graph can be traversed to understand the influence across directors and actors.

~~~
// drop last graph projection
CALL gds.graph.drop('proj', false);

// create Cypher projection for network of people directing actors
// filter to recent high grossing movies
MATCH (source:Person)-[:DIRECTED]->(m:Movie)<-[:ACTED_IN]-(target)
WHERE m.year >= 1990 AND m.revenue >= 10000000
WITH source, target, count(*) as actedWithCount
WITH gds.graph.project(
  'proj',
  source,
  target,
  {
    relationshipType: "DIRECTED_ACTOR"
  }
) as g
RETURN
  g.graphName AS graph, g.nodeCount AS node, g.relationshipCount AS rels

~~~

Next stream PageRank to find the top 5 most influential people in director-actor network.

~~~
CALL gds.pageRank.stream('proj')
YIELD nodeId, score
RETURN
  gds.util.asNode(nodeId).name AS personName,
  score AS influence
ORDER BY influence DESCENDING, personName LIMIT 5
~~~

The top three persons should be "Robert De Niro", "Greg Kinnear", and "Sandra Bullock."

The explanation is as below:

## 🎬 3. Context: Director → Actor Network

You’re using a **movie dataset** with:

* `(:Person)` nodes (actors, directors)
* `(:Movie)` nodes
* Relationships like:

  * `(:Person)-[:DIRECTED]->(:Movie)`
  * `(:Person)-[:ACTED_IN]->(:Movie)`

We’re going to build a **people-to-people network** that connects **directors to the actors** they directed — for *modern, successful* movies.

---

## 🧩 4. Step 1: Create a Graph Projection

```cypher
// drop last graph projection
CALL gds.graph.drop('proj', false);

// create Cypher projection for network of people directing actors
// filter to recent high grossing movies
MATCH (source:Person)-[:DIRECTED]->(m:Movie)<-[:ACTED_IN]-(target)
WHERE m.year >= 1990 AND m.revenue >= 10000000
WITH source, target, count(*) as actedWithCount
WITH gds.graph.project(
  'proj',
  source,
  target,
  {
    relationshipType: "DIRECTED_ACTOR"
  }
) as g
RETURN
  g.graphName AS graph, g.nodeCount AS node, g.relationshipCount AS rels;
```

### 🔍 What this does:

#### a. Drop the old projection

```cypher
CALL gds.graph.drop('proj', false);
```

Deletes any existing in-memory graph named `'proj'` (so you can reuse the name).

#### b. Match directors and actors

```cypher
MATCH (source:Person)-[:DIRECTED]->(m:Movie)<-[:ACTED_IN]-(target)
```

Finds all pairs where:

* A `Person` **directed** a movie.
* Another `Person` **acted in** the same movie.
  So this connects **directors → actors**.

#### c. Filter the movies

```cypher
WHERE m.year >= 1990 AND m.revenue >= 10000000
```

Include only movies released after 1990 with **at least $10M in revenue** (to focus on notable productions).

#### d. Project to an in-memory graph

```cypher
WITH gds.graph.project('proj', source, target, { relationshipType: "DIRECTED_ACTOR" }) AS g
```

This creates a new **in-memory graph projection** called `'proj'`, where:

* Nodes are **people** (directors and actors).
* Relationships are **DIRECTED_ACTOR** edges from directors to the actors they directed.

So the resulting graph is a **directed network of people**, representing “who directed whom.”

---

## 🚀 5. Step 2: Run the PageRank Algorithm

```cypher
CALL gds.pageRank.stream('proj')
YIELD nodeId, score
RETURN
  gds.util.asNode(nodeId).name AS personName,
  score AS influence
ORDER BY influence DESCENDING, personName LIMIT 5;
```

### 🔍 What this does:

* **`CALL gds.pageRank.stream('proj')`**
  Runs the PageRank algorithm on the in-memory graph `'proj'`.
* **`YIELD nodeId, score`**
  Returns each node’s internal ID and its computed PageRank score.
* **`gds.util.asNode(nodeId).name`**
  Converts the in-memory ID back to the Neo4j node and gets its `name` property.
* **`ORDER BY influence DESCENDING`**
  Ranks the people by their PageRank score (i.e., influence).

### 🧾 Interpretation:

The **PageRank score** reflects how influential a person is in the **director–actor network**:

* A director is influential if they directed many popular or influential actors.
* An actor is influential if they were directed by many influential directors.

---

## 🏆 6. Example Result

| personName     | influence |
| -------------- | --------- |
| Robert De Niro | 0.0028    |
| Greg Kinnear   | 0.0025    |
| Sandra Bullock | 0.0024    |

These are the top-ranked individuals by influence in the network of directors and actors for high-grossing movies since 1990.

---

## ✅ 7. Summary: Degree Centrality vs. PageRank

| Feature     | Degree Centrality              | PageRank                                                |
| ----------- | ------------------------------ | ------------------------------------------------------- |
| Counts      | Number of connections          | Weighted influence from connected nodes                 |
| Direction   | Out-degree (by default)        | In-degree (importance flows in)                         |
| Sensitivity | Treats all connections equally | Gives more weight to important sources                  |
| Example     | # of movies an actor acted in  | How influential a person is based on who they work with |

---

### 💡 Analogy:

Think of **degree centrality** as *“how many people you know”*
and **PageRank** as *“how important the people you know are.”*


**Other Centrality Algorithms**
Other GDS production tier centrality algorithms include:

Betweenness Centrality: Measures the extent to which a node stands between the other nodes in a graph. It is often used to find nodes that serve as a bridge from one part of a graph to another.

Eigenvector Centrality: Measures the transitive influence of nodes. Similar to PageRank, but works only on the largest eigenvector of the adjacency matrix so does not converge in the same way and tends to more strongly favor high degree nodes. It can be more appropriate in certain use cases, particularly those with undirected relationships.

Article Rank: A variant of PageRank which assumes that relationships originating from low-degree nodes have a higher influence than relationships from high-degree nodes.

A full list of centrality algorithms across all product tiers can be found in the Centrality section of the GDS documentation.

- https://graphacademy.neo4j.com/courses/graph-data-science-fundamentals/1-graph-algorithms/6-community-detection/

# Community Detection

Community detection algorithms are used to evaluate how groups of nodes may be clustered or partitioned in the graph. Much of the community detection functionality in GDS is focused on distinguishing and assigning ids to these node groups for downstream analytics, visualization, or other processing.

Common use cases of community detection include:

  - Fraud detection: Finding fraud rings by identifying accounts that have frequent suspicious transactions and/or share identifiers between one another.
  ~~~
  “Finding fraud rings”
  
  A fraud ring is a group of people or accounts working together to commit fraud — for example:
  
  Several fake bank accounts created by the same person,
  Multiple e-commerce accounts used to inflate reviews or perform fake purchases,
  A network of insurance claims filed by connected individuals.
  
  So finding fraud rings means detecting groups of accounts that appear to be acting together, even if they try to look unrelated.
~~~ 
  
  - Customer 360: Disambiguating multiple records and interactions into a single customer profile so an organization has an aggregated source of truth for each customer.
  
  - Market segmentation: dividing a target market into approachable subgroups based on priorities, behaviors, interests, and other criteria.


# Louvain Community Detection

A common community detection algorithm is Louvain. Louvain maximizes a modularity score for each community, where the modularity quantifies the quality of an assignment of nodes to communities. This means evaluating how much more densely connected the nodes within a community are, compared to how connected they would be in a random network.

Louvain optimizes this modularity with a hierarchical clustering approach that recursively merges communities together. There are multiple parameters that can be used to tune Louvain to control its performance and the number and size of communities produced. This includes the maximum number of iterations and hierarchical levels to use as well as the tolerance parameter for assessing convergence/stopping conditions. Our Louvain documentation covers these parameters and tuning in more detail.

An additional important consideration is that Louvain is a stochastic algorithm. As such, the community assignments may change a bit when re-run. When the graph does not have a naturally well-defined community structure the changes between runs can become more significant. Louvain includes a seedProperty parameter which can be used to assign initial community ids and help with consistency between runs. Also, if consistency is important for your use case, other community detection algorithms, such as Weakly Connected Components (WCC), take a more deterministic partitioning approach to assigning communities and thus will not change between runs.

Below is an example of running Louvain to understand communities of actors and directors in our movies recommendations graph.

First create a graph projection with movies, actors, and directors. Project the relationships with an UNDIRECTED orientation as that works best with the Louvain algorithm.

~~~
CALL gds.graph.project('proj', ['Movie', 'Person'], {
    ACTED_IN:{orientation:'UNDIRECTED'},
    DIRECTED:{orientation:'UNDIRECTED'}
});
~~~
Then we can run Louvain. Here we will run Louvain in mutate mode to save community Ids and return high level statistics on the community counts, distribution, modularity score, and information for how Louvain processed the graph.

~~~
CALL gds.louvain.mutate('proj', {mutateProperty:'communityId'})
~~~

We can verify the communityId node properties in the projection with a stream operation.
~~~
CALL gds.graph.nodeProperty.stream('proj','communityId', ['Person'])
YIELD nodeId, propertyValue
WITH gds.util.asNode(nodeId) AS n, propertyValue AS communityId
WHERE n:Person
RETURN n.name, communityId LIMIT 10
~~~

# explain from AI:


---

## 🧠 1. What is Louvain Community Detection?

**Louvain** is one of the most widely used **community detection algorithms**.
Its goal is to find **groups (communities)** of nodes that are **densely connected** to each other but **loosely connected** to nodes in other groups.

So, in a **movie graph**, it can reveal groups of actors and directors who tend to work together often — like a “cluster” of collaborators.

---

## 📊 2. The Core Idea — *Modularity*

Louvain works by trying to **maximize a score called *modularity***.

* **Modularity** measures how well a network is divided into communities.
* It compares the **density of links inside communities** to the **density of links you’d expect in a random graph**.

In simple terms:

> Modularity answers: “Are nodes inside this group connected to each other more than you’d expect by chance?”

* **High modularity** → well-defined communities (strong internal connections).
* **Low modularity** → weaker or random grouping (no clear structure).

---

## 🔁 3. How Louvain Works (Hierarchical Optimization)

The Louvain algorithm runs in **two major phases**, repeatedly:

1. **Local Movement Phase**

   * Start by giving every node its own community.
   * Then, move nodes between communities if it increases the modularity score.

2. **Aggregation Phase**

   * Collapse each community into a *super-node*.
   * Build a new, smaller graph of these super-nodes.
   * Repeat the process until modularity no longer improves.

This creates a **hierarchical clustering** — communities within communities — which is why Louvain is fast and effective even on large graphs.

---

## ⚙️ 4. Parameters You Can Tune

Louvain in Neo4j GDS allows several parameters to control how it runs:

| Parameter           | Purpose                                                                    |
| ------------------- | -------------------------------------------------------------------------- |
| **`maxIterations`** | How many times to try improving modularity before stopping                 |
| **`maxLevels`**     | Maximum hierarchy depth (how many times it can merge communities)          |
| **`tolerance`**     | Threshold for convergence — stops when improvements are very small         |
| **`seedProperty`**  | Lets you specify initial community IDs for consistent results between runs |

These let you balance **speed, stability, and precision**.

---

## 🎲 5. Louvain Is *Stochastic*

This means it includes some **randomness** in how it starts and merges communities.
So if you run it multiple times, you might see **slightly different community assignments** — especially if your graph doesn’t have clear, strong clusters.

That’s not a bug — it’s part of how Louvain explores multiple possible clusterings.

To make runs more consistent:

* You can use the **`seedProperty`** parameter (same seed → same results).
* Or, use a **deterministic algorithm** like **Weakly Connected Components (WCC)** if reproducibility is more important than modularity optimization.

---

## 🎬 6. Example: Movie Graph

Let’s walk through the example in the text.

### Step 1 — Create a Graph Projection

```cypher
CALL gds.graph.project(
  'proj',
  ['Movie', 'Person'],
  {
    ACTED_IN: {orientation: 'UNDIRECTED'},
    DIRECTED: {orientation: 'UNDIRECTED'}
  }
);
```

#### Explanation:

* You’re creating an **in-memory graph projection** called `'proj'`.
* It includes both:

  * `Movie` nodes
  * `Person` nodes (actors, directors)
* Relationships are treated as **UNDIRECTED**, meaning the connection works both ways (actor ↔ movie, director ↔ movie).

> Louvain works best on undirected graphs because community membership is based on *mutual* connections.

---

### Step 2 — Run Louvain in “Mutate” Mode

```cypher
CALL gds.louvain.mutate('proj', {mutateProperty: 'communityId'});
```

#### What happens here:

* `gds.louvain.mutate` runs the Louvain algorithm.
* It **adds a new property** called `communityId` to each node **inside the projection**.
* The output includes summary statistics such as:

  * Number of communities found
  * Modularity score
  * Distribution of community sizes
  * Processing time

---

### Step 3 — Inspect the Results

```cypher
CALL gds.graph.nodeProperty.stream('proj', 'communityId', ['Person'])
YIELD nodeId, propertyValue
WITH gds.util.asNode(nodeId) AS n, propertyValue AS communityId
WHERE n:Person
RETURN n.name, communityId
LIMIT 10;
```

#### What this does:

* Streams the nodes and their new `communityId` values.
* Filters to show only `Person` nodes (actors/directors).
* Returns sample names and their assigned community IDs.

Example output:

| name              | communityId |
| ----------------- | ----------- |
| Robert De Niro    | 3           |
| Martin Scorsese   | 3           |
| Leonardo DiCaprio | 3           |
| Sandra Bullock    | 7           |
| Steven Spielberg  | 5           |

This means:

* De Niro, Scorsese, and DiCaprio belong to the **same community (3)** — likely a group of collaborators.
* Bullock and Spielberg belong to **different communities**, representing different clusters in the movie network.

---

## 📈 7. Why Louvain is Useful

| Use Case                            | What You Learn                                              |
| ----------------------------------- | ----------------------------------------------------------- |
| **Social / Collaboration Networks** | Find groups of people who frequently work together          |
| **Fraud Detection**                 | Find rings of accounts with shared or frequent interactions |
| **Customer Segmentation**           | Find groups of customers with similar behaviors             |
| **Recommendation Systems**          | Suggest items or people from within the same community      |

---

## ✅ 8. Summary

| Concept                     | Description                                                                     |
| --------------------------- | ------------------------------------------------------------------------------- |
| **Louvain algorithm**       | Detects densely connected groups of nodes (communities)                         |
| **Modularity**              | Score measuring how well-defined communities are                                |
| **Hierarchical clustering** | Merges smaller groups into bigger ones recursively                              |
| **Stochastic**              | Has randomness, so results can slightly vary between runs                       |
| **Neo4j GDS use**           | Finds communities, stores IDs, and enables downstream analysis or visualization |

---

💡 **In plain English:**
Louvain finds “clusters of closeness” — groups of people, movies, or accounts that are tightly interconnected — by measuring how much stronger their connections are compared to random chance.

------
# Other Community Detection Algorithms

Below are some of the other production tier community detection algorithms. A full list of all community detection algorithms can be found in the Community Detection algorithms documentation.
  
  - Label Propagation: Similar intent as Louvain. Fast algorithm that parallelizes well. Great for large graphs.
  
  - Weakly Connected Components (WCC): Partitions the graph into sets of connected nodes such that
  
    a.Every node is reachable from any other node in the same set
    
    b.No path exists between nodes from different sets
  
  - Triangle Count: Counts the number of triangles for each node. Can be used to detect the cohesiveness of communities and stability of the graph.
  
  - Local Clustering Coefficient: Computes the local clustering coefficient for each node in the graph which is an indicator for how the node clusters with its neighbors.


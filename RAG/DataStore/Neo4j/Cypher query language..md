
# Cypher query language.


To review all the entities and their connections in your Neo4j database, the easiest and most interactive way is to use the **Neo4j Browser** using **Cypher query language**. 

Here is a step-by-step guide on how to do it:

### Step 1: Open Neo4j Browser
1. Open **Neo4j Desktop**.
2. Make sure your database instance (e.g., `securityArcGraph`) is **Started** (Running).
3. Click the **Open** button next to it and select **Neo4j Browser**.

### Step 2: Use Cypher Queries to Review Data

In the command line at the top of the Neo4j Browser, copy and paste the following queries depending on what you want to see. Press the `Play` button (or `Ctrl+Enter` / `Cmd+Enter`) to execute them.

#### 1. View the Entire Graph (Visual Review)
If your graph is relatively small (under a few hundred nodes), you can pull up everything at once to see how they connect:
```cypher
MATCH (n)-[r]->(m) 
RETURN n, r, m 
LIMIT 500
```
* **Tip**: In the visualization panel, you can drag nodes around. If you hover your mouse over a node, you will see its properties (like `description`, `name`, `categories`) at the bottom of the window or in the right-hand panel.

#### 2. Get a Summary Count of All Entities
To quickly check if all your approved entities made it into the database, you can group them by their Type (Label):
```cypher
MATCH (n) 
RETURN labels(n) AS EntityType, count(n) AS TotalCount
ORDER BY TotalCount DESC
```
*(This will return a nice table showing you have X number of Threats, Y number of Vulnerabilities, etc.)*

#### 3. Review a Specific Type of Entity
If you want to focus on just your `Vulnerability` nodes and read their descriptions:
```cypher
MATCH (v:Vulnerability) 
RETURN v.id, v.name, v.description, v.categories
```
*(On the left side of the results panel, click the **Table** icon instead of the Graph icon. This makes it much easier to read the long text descriptions just like in Excel).*

#### 4. Find Entities Missing a Description
To do a quality check and see if any nodes accidentally got imported without a description:
```cypher
MATCH (n) 
WHERE n.description IS NULL OR n.description = "" 
RETURN labels(n), n.name, n.id
```

#### 5. View a Specific "Closed-Loop" Path
To see the full logic chain we designed (Component -> Capability -> Vulnerability -> Threat -> Objective -> Pattern):
```cypher
MATCH path = (c:ComponentType)-[:HAS_CAPABILITY]->(cap:Capability)-[:SUSCEPTIBLE_TO]->(v:Vulnerability)<-[:MITIGATES]-(p:ControlPattern)
RETURN path
LIMIT 50
```

### 💡 Pro-Tip for Neo4j Browser:
By default, nodes in Neo4j might just look like blank colored circles. To make them show the `name` property:
1. Run a query that returns some nodes (e.g., `MATCH (n) RETURN n LIMIT 10`).
2. In the right-hand visual legend, click on the colored pill (e.g., `ComponentType`).
3. At the bottom of the legend pane, you will see a list of property names. Click on **`name`**. 
4. Now all nodes of that type will display their names right inside the circles!
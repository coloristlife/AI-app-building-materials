# graph rag
## Graph RAG 
Graph RAG (Graph Retrieval-Augmented Generation): Graph RAG extends RAG by incorporating knowledge graphs into the retrieval process. Instead of retrieving only text chunks, Graph RAG indexes data into a graph structure of entities (nodes) and relationships (edges). This graph-based retrieval enables multi-hop reasoning across connected facts and often pairs graph queries with vector search. Graph RAG has proven effective for complex queries that require linking disparate pieces of information (e.g., answering questions on citation networks or social graphs) and can significantly outperform naive RAG in multi-step reasoning tasks. Microsoft’s GraphRAG project is a notable example, which automatically constructs a knowledge graph from text documents and supports hierarchical community detection for “global” insights.

### Vector RAG: The Foundation of RAG
https://medium.com/@wijdnbouzidii/understanding-graph-rag-vector-rag-and-agentic-rag-a-deep-dive-into-retrieval-augmented-ac0ae73caced


### knowledge graph agent
https://learn.deeplearning.ai/courses/agentic-knowledge-graph-construction/lesson/ddcnq/architecture-of-the-multi-agent-system

<img width="1249" height="618" alt="KnowledgeGraphAgent" src="https://github.com/user-attachments/assets/b929be24-98d1-44d5-8de3-5768d46ae937" />

<img width="1261" height="610" alt="structureDataAgent" src="https://github.com/user-attachments/assets/f9ca9791-7ecb-47d9-876a-c40cb4ed27d9" />


1. The user intent agent is a goal-oriented, conversational agent that helps the user ideate on the kind of graph to build.

2. The File Suggestion agent is a tool-use agent that suggests files to use for import, based on the approved user goal from the previous lesson.

3. Schema proposal for structured data:
   Multiple agents will collaborate to propose construction rules for a knowledge graph

    Input: approved_user_goal, approved_files
    Output: approved_construction_plan
    Tools: get_approved_user_goal, get_approved_files, sample_file,
      `propose_node_construction`, `propose_relationship_construction`, 
      `get_proposed_construction_plan`,`approve_proposed_construction_plan`

      This workflow will use multiple agents to propose a construction plan for the knowledge graph.
    
      A top-level 'schema_refinement_loop' will coordinate three agents operating in a loop:
      
      1). A 'schema_proposal_agent' that proposes a schema and construction plan for the knowledge graph.
      2). A 'schema_critic_agent' that critiques the proposed schema and construction plan for the knowledge graph.
      3). A 'CheckStatusAndEscalate' agent that checks the feedback of the critic agent
    ~~~~
    Agent Response: Here is the proposed construction plan for the knowledge graph based on the approved files:
    
    ### Nodes
    1. **Product**
       - **Source File**: `products.csv`
       - **Label**: Product
       - **Unique Identifier**: `product_id`
       - **Properties**: `product_name`, `price`, `description`
    
    2. **Supplier**
       - **Source File**: `suppliers.csv`
       - **Label**: Supplier
       - **Unique Identifier**: `supplier_id`
       - **Properties**: `name`, `specialty`, `city`, `country`, `website`, `contact_email`
    
    3. **Assembly**
       - **Source File**: `assemblies.csv`
       - **Label**: Assembly
       - **Unique Identifier**: `assembly_id`
       - **Properties**: `assembly_name`, `quantity`, `product_id`
    
    4. **Part**
       - **Source File**: `parts.csv`
       - **Label**: Part
       - **Unique Identifier**: `part_id`
       - **Properties**: `part_name`, `quantity`, `assembly_id`
    
    ### Relationships
    1. **PART_OF**
       - **Source File**: `assemblies.csv`
       - **Type**: PART_OF
       - **From Node**: Assembly (`assembly_id`)
       - **To Node**: Product (`product_id`)
       - **Properties**: `quantity`
    
    2. **INCLUDES**
       - **Source File**: `parts.csv`
       - **Type**: INCLUDES
       - **From Node**: Part (`part_id`)
       - **To Node**: Assembly (`assembly_id`)
       - **Properties**: `quantity`
    
    3. **SUPPLIED_BY**
       - **Source File**: `part_supplier_mapping.csv`
       - **Type**: SUPPLIED_BY
       - **From Node**: Part (`part_id`)
       - **To Node**: Supplier (`supplier_id`)
       - **Properties**: `preferred_supplier`, `lead_time_days`, `unit_cost`, `minimum_order_quantity`
    
    This schema creates a connected graph that allows you to analyze the supply chain by examining how products are built from assemblies and parts, and how these parts are sourced from various suppliers.
    
    
    
    ~~~~
    Session state:  {'feedback': '', 'approved_user_goal': {'kind_of_graph': 'supply chain analysis', 'description': 'A multi-level bill of materials for manufactured products, useful for root cause analysis..'}, 'approved_files': ['assemblies.csv', 'parts.csv', 'part_supplier_mapping.csv', 'products.csv', 'suppliers.csv'], 'proposed_construction_plan': {'Product': {'construction_type': 'node', 'source_file': 'products.csv', 'label': 'Product', 'unique_column_name': 'product_id', 'properties': ['product_name', 'price', 'description']}, 'Supplier': {'construction_type': 'node', 'source_file': 'suppliers.csv', 'label': 'Supplier', 'unique_column_name': 'supplier_id', 'properties': ['name', 'specialty', 'city', 'country', 'website', 'contact_email']}, 'Assembly': {'construction_type': 'node', 'source_file': 'assemblies.csv', 'label': 'Assembly', 'unique_column_name': 'assembly_id', 'properties': ['assembly_name', 'quantity', 'product_id']}, 'Part': {'construction_type': 'node', 'source_file': 'parts.csv', 'label': 'Part', 'unique_column_name': 'part_id', 'properties': ['part_name', 'quantity', 'assembly_id']}, 'PART_OF': {'construction_type': 'relationship', 'source_file': 'assemblies.csv', 'relationship_type': 'PART_OF', 'from_node_label': 'Assembly', 'from_node_column': 'assembly_id', 'to_node_label': 'Product', 'to_node_column': 'product_id', 'properties': ['quantity']}, 'INCLUDES': {'construction_type': 'relationship', 'source_file': 'parts.csv', 'relationship_type': 'INCLUDES', 'from_node_label': 'Part', 'from_node_column': 'part_id', 'to_node_label': 'Assembly', 'to_node_column': 'assembly_id', 'properties': ['quantity']}, 'SUPPLIED_BY': {'construction_type': 'relationship', 'source_file': 'part_supplier_mapping.csv', 'relationship_type': 'SUPPLIED_BY', 'from_node_label': 'Part', 'from_node_column': 'part_id', 'to_node_label': 'Supplier', 'to_node_column': 'supplier_id', 'properties': ['preferred_supplier', 'lead_time_days', 'unit_cost', 'minimum_order_quantity']}}}
    Proposed construction plan:  {'Product': {'construction_type': 'node', 'source_file': 'products.csv', 'label': 'Product', 'unique_column_name': 'product_id', 'properties': ['product_name', 'price', 'description']}, 'Supplier': {'construction_type': 'node', 'source_file': 'suppliers.csv', 'label': 'Supplier', 'unique_column_name': 'supplier_id', 'properties': ['name', 'specialty', 'city', 'country', 'website', 'contact_email']}, 'Assembly': {'construction_type': 'node', 'source_file': 'assemblies.csv', 'label': 'Assembly', 'unique_column_name': 'assembly_id', 'properties': ['assembly_name', 'quantity', 'product_id']}, 'Part': {'construction_type': 'node', 'source_file': 'parts.csv', 'label': 'Part', 'unique_column_name': 'part_id', 'properties': ['part_name', 'quantity', 'assembly_id']}, 'PART_OF': {'construction_type': 'relationship', 'source_file': 'assemblies.csv', 'relationship_type': 'PART_OF', 'from_node_label': 'Assembly', 'from_node_column': 'assembly_id', 'to_node_label': 'Product', 'to_node_column': 'product_id', 'properties': ['quantity']}, 'INCLUDES': {'construction_type': 'relationship', 'source_file': 'parts.csv', 'relationship_type': 'INCLUDES', 'from_node_label': 'Part', 'from_node_column': 'part_id', 'to_node_label': 'Assembly', 'to_node_column': 'assembly_id', 'properties': ['quantity']}, 'SUPPLIED_BY': {'construction_type': 'relationship', 'source_file': 'part_supplier_mapping.csv', 'relationship_type': 'SUPPLIED_BY', 'from_node_label': 'Part', 'from_node_column': 'part_id', 'to_node_label': 'Supplier', 'to_node_column': 'supplier_id', 'properties': ['preferred_supplier', 'lead_time_days', 'unit_cost', 'minimum_order_quantity']}}

4. Schema Proposal for Unstructured Data
   https://learn.deeplearning.ai/courses/agentic-knowledge-graph-construction/lesson/wwdel/schema-proposal-for-unstructured-data
   
      Two agents to propose data extraction from unstructured data: a "named entity recognition" agent and a "fact extraction" agent:
      
      Input: approved_user_goal, approved_files, approved_construction_plan
      Output:
      approved_entity_types describing the type of entities that could be extracted from the unstructured data
      approved_fact_types describing how those entities can be related in a fact triple
      Tools: get_approved_user_goal, get_approved_files, get_well_known_types, sample_file, set_proposed_entities, get_proposed_entities, approve_proposed_entities, add_proposed_fact, get_proposed_facts, approve_proposed_facts
    
      Named entity recognition:
    
      The context is initialized with an approved_user_goal, approved_files and an approved_construction_plan
      The agent analyzes unstructured data files, looking for relevant entity types
      The agent proposes a list of entity types, seeking user approval
      
      The NER agent is responsible for proposing entities that could be extracted from the unstructured data files.
    
      An entity is a person, place or thing that is relevant to the user's goal.
      
      There are two general kinds of entities:
      
      Well-known entities: these closely correlate with nodes in the existing structured data
      
      in our example, this would be things like Products, Parts and Suppliers
      
      Discovered entities: these are entities that are not pre-defined, but are mentioned in the markdown text
      
      in the product reviews, this may may Reviewers, product complaints, or product features
      
      The general goal of the NER agent is to analyze the markdown files and propose entities that are relevant to the user goal of root-cause analysis.
      
      Fact extraction:
      
      The context now includes approved_entity_types
      The agent analyzes unstructured data files, looking for how those entities can be saved as fact triples
      The agent proposes fact types, seeking user approval
    
    
      >>> User Query: Propose fact types that can be found in the text.
      <<< Agent Response: After analyzing the user's goal, approved entity types, and sampling a file from the approved list, I propose the following types of facts that can be extracted from the text files:
      
      1. **(Product, has_rating, Rating):** Captures the customer's overall rating of the product.
         
      2. **(Product, has_quality_issue, Quality Control Issue):** Identifies mentions of quality-related problems with the product, useful for identifying recurring defects.
      
      3. **(Product, is_hard_to_assemble, Assembly Difficulty):** Flags challenges related to the product's assembly, beneficial for understanding assembly difficulties faced by customers.
      
      4. **(Product, has_material_defect, Material Defect):** Records mentions of material-specific issues like dents or scratches that indicate defects.
      
      5. **(Product, interacts_with_customer_service, Customer Service Interaction):** Tracks any interactions with customer service, useful for understanding post-purchase customer experiences.
      
      6. **(Customer Feedback, is_about, Product):** Links customer feedback or reviews explicitly to the corresponding product.
      
      7. **(Customer Feedback, expresses_opinion_on, Quality Control Issue):** Reflects the consumer's opinion on quality control issues, highlighting positive or negative sentiments.
      
      8. **(Customer Feedback, expresses_difficulty_with, Assembly):** Shares feedback regarding difficulties encountered during the assembly process.
      
      These proposed fact types will be helpful for building a graph aimed at supply chain analysis, focusing on product issues like quality, assembly difficulty, durability, and user experience. Would you like to approve these fact types?

5. Knowledge Graph Construction - part 1
    For the domain graph construction, no agent is required. The construction plan has all the information needed to drive a rule-based import.

   A single tool which will build a knowledge graph using the defined construction rules.

      Input: approved_construction_plan
      Output: a domain graph in Neo4j
      Tools: construct_domain_graph + helper functions

      Workflow
      
      The context is initialized with an approved_construction_plan and approved_files
      Process all the node construction rules
      Process all the relationship construction rules

   
    Function: construct_domain_graph
      This is the main orchestration function that builds the entire domain graph. It processes the construction plan in two phases:
      
      Node Construction: First imports all nodes to ensure they exist before creating relationships
      Relationship Construction: Then creates relationships between the existing nodes
      This two-phase approach prevents relationship creation failures due to missing nodes.

   5. Knowledge Graph Construction - part 2
     - use Neo4j's graphrag library to perform the chunking and entity extraction
     - techniques for entity resolution
  <img width="1921" height="504" alt="KG_pipeline" src="https://github.com/user-attachments/assets/2e2b8cd3-a4ed-493c-b86a-86524f12ef4f" />

       
  







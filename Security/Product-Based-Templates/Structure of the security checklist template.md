# Structure of the security checklist template

1. Feature Title
2. Feature Description
3. Title of security Issue (in the format of what is missing)
4. Description 
5. Compensating Controls
6. Recommendation
7. Risk Level
8. Stanadard Baseline
## Example:

### **Feature: Codebase Indexing (Contextual Retrieval)**
**Feature Description**: This feature processes an organization’s private source code repositories into a searchable format (typically a vector database). This allows the AI to provide "organization-aware" code suggestions, documentation, and answers based on internal patterns, libraries, and proprietary logic.

*   **Title of security issue**: **Identity Access Gap in Code Context Retrieval**
*   **Description**: The AI engine often indexes repositories at a centralized administrative level (e.g., a Cloud Project). It frequently lacks a native mechanism to synchronize granular user-level permissions from the Version Control System (VCS) with the AI's suggestion engine. A user with general access to the AI service may receive code suggestions derived from indexed repositories they are not authorized to view in the original VCS.
*   **Compensating Control**: Physically segregate sensitive repositories into separate administrative environments or projects and limit access to the AI service based on those boundaries.
*   **Recommendation**: Implement "Identity-Aware Retrieval" that performs a real-time check of the developer’s VCS permissions before allowing the AI to pull context from a specific repository index.
*   **Risk Level**: **High**
  
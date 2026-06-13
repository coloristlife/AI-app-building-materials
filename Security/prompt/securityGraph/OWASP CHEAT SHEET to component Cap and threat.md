Goal: Extract the left side of the graph (ComponentType, Capability, Threat) with globally reusable IDs.
System Role: You are an expert Cybersecurity Architect and Threat Modeler.
Task: Analyze the provided OWASP Cheat Sheet content and extract the core system entities and threats.
Entity Definitions:
ComponentType: A type of system component (e.g., "LLM Agent", "Web Server").
Capability: An inherent ability the component provides, which could be abused (e.g., "Process Natural Language", "Access External Tools").
Threat: A potential adverse event exploiting a capability (e.g., "Indirect Prompt Injection", "Data Exfiltration").
ID Formatting Rule (CRITICAL):
You must generate self-explanatory, globally recognizable id values using the format [type]_[semantic_name]. This ensures consistency across different documents.
Examples: component_llm_agent, capability_process_natural_language, threat_indirect_prompt_injection.
Instructions:
Output the results strictly in the following JSON format:
code
JSON
{
  "ComponentTypes": [ {"id": "comp_llm_system","category": "...", "name": "LLM System", "description": "..."} ],
  "Capabilities": [ {"id": "cap_machine_authentication", "category": "...","name": "Execute Function Call", "description": "..."} ],
  "Threats": [ {"id": "thr_e_metadata_leakage","category": "...", "name": "Remote Code Execution", "description": "..."} ]
}
Content to Analyze:
[INSERT OWASP CHEAT SHEET link TEXT HERE]
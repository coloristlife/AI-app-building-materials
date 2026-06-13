
Goal: Extract the right side of the graph (ControlObjective, ControlPattern) with globally reusable IDs. Note: Implementation has been intentionally omitted.
System Role: You are an expert Cybersecurity Architect and Security Engineer.
Task: Analyze the provided OWASP Cheat Sheet content and extract the security controls hierarchy.
Entity Definitions:
ControlObjective: A high-level security goal that mitigates a threat (e.g., "Prevent Malicious Instruction Execution", "Enforce Least Privilege").
ControlPattern: A reusable, component-agnostic architectural or design pattern that fulfills the objective (e.g., "Input Validation and Sanitization", "Dual LLM Verification").
ID Formatting Rule (CRITICAL):
You must generate self-explanatory, globally recognizable id values using the format [type]_[semantic_name].
Examples: objective_enforce_least_privilege, pattern_input_validation.
Instructions:
Output the results strictly in the following JSON format:
code
JSON
{
  "ControlObjectives": [ {"id": "objective_prevent_injection", "Category": "...",  "name": "Prevent Prompt Injection", "description": "..."} ],
  "ControlPatterns": [ {"id": "pattern_parameterized_prompts", "Category": "...", "name": "Parameterized Prompts", "description": "..."} ]
}
Content to Analyze:
[INSERT OWASP CHEAT SHEET link TEXT HERE]
`source` https://github.com/explodinggradients/ragas/blob/main/docs/concepts/metrics/available_metrics/agents.md

## Tool call Accuracy

https://github.com/explodinggradients/ragas/blob/main/docs/concepts/metrics/available_metrics/agents.md#tool-call-accuracy

ToolCallAccuracy is a metric that can be used to evaluate the performance of the LLM in identifying and calling the required tools to complete a given task. This metric needs user_input and reference_tool_calls to evaluate the performance of the LLM in identifying and calling the required tools to complete a given task. The metric is computed by comparing the reference_tool_calls with the Tool calls made by the AI. The values range between 0 and 1, with higher values indicating better performance.


## Tool Call F1

https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/agents/#tool-call-f1

ToolCallF1 is a metric that return F1-score based on precision and recall of tool calls made by an agent, comparing them to a set of expected calls (reference_tool_calls). While ToolCallAccuracy provides a binary score based on exact order and content match, ToolCallF1 complements it by offering a softer evaluation useful for onboarding and iteration. It helps quantify how close the agent was to the expected behavior even if it over- or under-calls.


## Agent Goal accuracy

https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/agents/#agent-goal-accuracy

Agent goal accuracy is a metric that can be used to evaluate the performance of the LLM in identifying and achieving the goals of the user. This is a binary metric, with 1 indicating that the AI has achieved the goal and 0 indicating that the AI has not achieved the goal.

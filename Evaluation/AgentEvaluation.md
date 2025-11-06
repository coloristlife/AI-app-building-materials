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


## An Open Book: Evaluating AI Agents with ADK

https://medium.com/google-cloud/an-open-book-evaluating-ai-agents-with-adk-c0cff7efbf00

Evalset file: 

https://google.github.io/adk-docs/evaluate/#second-approach-using-an-evalset-file

The evalset approach utilizes a dedicated dataset called an "evalset" for evaluating agent-model interactions. Similar to a test file, the evalset contains example interactions. However, an evalset can contain multiple, potentially lengthy sessions, making it ideal for simulating complex, multi-turn conversations. Due to its ability to represent complex sessions, the evalset is well-suited for integration tests. These tests are typically run less frequently than unit tests due to their more extensive nature.

An evalset file contains multiple "evals," each representing a distinct session. Each eval consists of one or more "turns," which include the user query, expected tool use, expected intermediate agent responses, and a reference response.

Creating evalsets manually can be complex, therefore UI tools are provided to help capture relevant sessions and easily convert them into evals within your evalset.


format of evalset json file:

~~~
{
    "eval_set_id": "book_finder_eval_workflow",
    "name": "Book Finder Workflow Evaluation",
    "description": "Tests the agent's ability to find a book that is unavailable at the local library and specialty bookstores, requiring it to proceed to online ordering options.",
    "eval_cases": [
        {
            "eval_id": "find_book_unavailable_locally",
            "session_input": {
                "app_name": "book_finder",
                "user_id": "eval_user_01",
                "state": {}
            },
            "conversation": [
                {
                    "invocation_id": "turn_1_unavailable_book_workflow",
                    "user_content": {
                        "role": "user",
                        "parts": [
                            {
                                "text": "Help me find Heartstopper by Alice Oseman"
                            }
                        ]
                    },
                    "final_response": {
                        "role": "model",
                        "parts": [
                            {
                                "text": "Of course! Here are the fastest ways to get 'Heartstopper' by Alice Oseman: **The Fastest Option (Online)** is **MapleLeaf Books Online**- they can get it to you in 2-3 business days...! 📖"
                            }
                        ]
                    },
                    "intermediate_data": {
                        "tool_uses": [
                            {
                                "name": "search_local_library",
                                "args": {
                                    "title": "Heartstopper"
                                }
                            },
                            {
                                "name": "find_local_bookstore",
                                "args": {
                                    "genre": "Young Adult"
                                }
                            },
                            {
                                "name": "order_online",
                                "args": {
                                    "title": "Heartstopper"
~~~

https://google.github.io/adk-docs/evaluate/#evaluation-criteria


ADK provides several built-in criteria for evaluating agent performance, ranging from tool trajectory matching to LLM-based response quality assessment. For a detailed list of available criteria and guidance on when to use them, please see Evaluation Criteria.

Here is a summary of all the available criteria:

- tool_trajectory_avg_score: Exact match of tool call trajectory.
- response_match_score: ROUGE-1 similarity to reference response.
- final_response_match_v2: LLM-judged semantic match to a reference response.
- rubric_based_final_response_quality_v1: LLM-judged final response quality based on custom rubrics.
- rubric_based_tool_use_quality_v1: LLM-judged tool usage quality based on custom rubrics.
- hallucinations_v1: LLM-judged groundedness of agent response against context.
- safety_v1: Safety/harmlessness of agent response.



**From AI**
In the context of AI agent evaluation (for example, evaluating conversational/agentic systems), an “evalset file” (sometimes called eval set, evaluation set, eval_set, etc.) refers to a structured dataset (often in JSON or JSONL format) of evaluation cases that define how the agent should be tested. It essentially serves as a suite of test sessions designed to check the agent’s behaviour — not just the final answer, but also the trajectory (tool-calls, reasoning steps) and how well it follows the intended workflow.

From https://medium.com/google-cloud/an-open-book-evaluating-ai-agents-with-adk-c0cff7efbf00: 

<img width="720" height="404" alt="image" src="https://github.com/user-attachments/assets/15571fbb-f146-4add-9265-a6f283cf0676" />


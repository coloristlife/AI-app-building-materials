- https://github.com/Shubhamsaboo/awesome-llm-apps/tree/main/ai_agent_framework_crash_course/openai_sdk_crash_course/9_multi_agent_orchestration
  
- https://docs.langchain.com/oss/python/langgraph/workflows-agents#parallelization
  
  With parallelization, LLMs work simultaneously on a task. This is either done by running multiple independent subtasks at the same time, or running the same task multiple times to check for different outputs. Parallelization is commonly used to:
  
  - Split up subtasks and run them in parallel, which increases speed
  - Run tasks multiple times to check for different outputs, which increases confidence
  
  Some examples include:
  
  - Running one subtask that processes a document for keywords, and a second subtask to check for formatting errors
  - Running a task multiple times that scores a document for accuracy based on different criteria, like the number of citations, the number of sources used, and the quality of the sources
 
    contain the implementation code with StateGraph

- https://levelup.gitconnected.com/building-an-advanced-agentic-rag-pipeline-that-mimics-a-human-thought-process-687e1fd79f61#a6e3

A SQL-Querying Agent for Structured Data
Our next specialist is the Analyst. Its expertise lies in our structured, relational data. While the Librarian handles prose, the Analyst handles numbers. It needs the ability to understand natural language questions, translate them into SQL, and execute them against our database.

<img width="2000" height="608" alt="image" src="https://github.com/user-attachments/assets/15c62c92-b7c6-44f4-a053-f627ab2b8921" />

We will use LangChain create_sql_agent to build an agent specifically for this task. This is a powerful, pre-built constructor that creates an agent with a thought process for interacting with databases. We will then wrap this agent in our own @tool function to integrate it into our Supervisor's toolkit.

~~~
# Initialize SQL Agent backed by GPT-4o
sql_agent_llm = ChatOpenAI(model="gpt-4o", temperature=0)
sql_agent_executor = create_sql_agent(
    llm=sql_agent_llm,
    db=db,                       # Database connection with financial data
    agent_type="openai-tools",   # Use OpenAI tools integration
    verbose=True                 # Print detailed logs of reasoning
)

@tool
def analyst_sql_tool(query: str) -> str:
    """
    Tool for querying a SQL database of Microsoft's revenue and net income.
    Best for direct, specific financial questions about a single period 
    (e.g., "What was the revenue in Q4 2023?").
    
    For trend or multi-period analysis, use `analyst_trend_tool`.
    """
    print(f"\n-- Analyst SQL Tool Called with query: '{query}' --")
    
    # Pass query to SQL agent, which generates and executes SQL automatically
    result = sql_agent_executor.invoke({"input": query})
    
    # Extract and return only the final answer text
    return result['output']
~~~

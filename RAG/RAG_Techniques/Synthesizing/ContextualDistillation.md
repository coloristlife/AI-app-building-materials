# Synthesizing using Contextual Distillation
- https://levelup.gitconnected.com/building-an-agentic-deep-thinking-rag-pipeline-to-solve-complex-queries-af69c5e044db#4ff4

We are in a much better position now, but we can still make one final improvement before handing this information over to our main reasoning agents. Right now, we have three separate text chunks.

While they are all relevant, they might contain redundant information or overlapping sentences. Presenting them as three distinct blocks can still be a bit clunky for an LLM to process.

The final stage of our retrieval funnel is Contextual Distillation. The goal is simple: take our top 3 highly relevant document chunks and distill them into a single, clean, and concise paragraph. This removes any final redundancy and presents a perfectly synthesized piece of evidence to our downstream agents.

> This distillation step acts as a final compression layer. It ensures the context fed into our more expensive reasoning agents is as dense and information-rich as possible, maximizing signal and minimizing noise.

To do this, we will create another small, specialized agent that we will call the Distiller Agent.

First, we need to design the prompt that will guide its behavior.

~~~
# The prompt for our distiller agent, instructing it to synthesize and be concise
distiller_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful assistant. Your task is to synthesize the following retrieved document snippets into a single, concise paragraph.
The goal is to provide a clear and coherent context that directly answers the question: '{question}'.
Focus on removing redundant information and organizing the content logically. Answer only with the synthesized context."""),
    ("human", "Retrieved Documents:\n{context}") # The content of our top 3 reranked documents will be passed here
])
~~~

We are basically giving this agent a very focused task. We’re telling it: “Here are some pieces of text. Your only job is to merge them into one coherent paragraph that answers this specific question”. The instruction to “Answer only with the synthesized context” is important, it prevents the agent from adding any conversational fluff or trying to answer the question itself. It’s purely a text-processing tool.

Now, we can assemble our simple distiller_agent.

~~~
# Create the agent by piping our prompt to the reasoning LLM and a string output parser
distiller_agent = distiller_prompt | reasoning_llm | StrOutputParser()
print("Contextual Distiller Agent created.")
~~~

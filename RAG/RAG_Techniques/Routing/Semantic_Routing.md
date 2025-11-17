- https://levelup.gitconnected.com/building-the-entire-rag-ecosystem-and-optimizing-every-component-8f23349b96a4#8177
# Semantic Routing

Logical routing works perfectly when you have clearly defined categories. But what if you want to route based on the style or domain of a question? For example, you might want to answer physics questions with a serious, academic tone and math questions with a step-by-step, pedagogical approach. This is where Semantic Routing comes in.


<img width="1100" height="391" alt="image" src="https://github.com/user-attachments/assets/32c5f48e-cd4c-4d9c-9991-dc9690725d55" />


Instead of classifying the query, we define multiple expert prompts.

We then embed the user’s query and each of our prompt templates, and use cosine similarity to find the prompt that is most semantically aligned with the query.

First, let’s define our two expert personas.

~~~
from langchain_core.prompts import PromptTemplate

# A prompt for a physics expert
physics_template = """You are a very smart physics professor. \
You are great at answering questions about physics in a concise and easy to understand manner. \
When you don't know the answer to a question you admit that you don't know.

Here is a question:
{query}"""

# A prompt for a math expert
math_template = """You are a very good mathematician. You are great at answering math questions. \
You are so good because you are able to break down hard problems into their component parts, \
answer the component parts, and then put them together to answer the broader question.

Here is a question:
{query}"""
~~~

Now, we’ll create the routing function that performs the embedding and similarity comparison.

~~~
from langchain.utils.math import cosine_similarity

# Initialize the embedding model
embeddings = OpenAIEmbeddings()

# Store our templates and their embeddings for comparison
prompt_templates = [physics_template, math_template]
prompt_embeddings = embeddings.embed_documents(prompt_templates)

def prompt_router(input):
    """A function to route the input query to the most similar prompt template."""
    # 1. Embed the incoming user query
    query_embedding = embeddings.embed_query(input["query"])
    
    # 2. Compute the cosine similarity between the query and all prompt templates
    similarity = cosine_similarity([query_embedding], prompt_embeddings)[0]
    
    # 3. Find the index of the most similar prompt
    most_similar_index = similarity.argmax()
    
    # 4. Select the most similar prompt template
    chosen_prompt = prompt_templates[most_similar_index]
    
    print(f"DEBUG: Using {'MATH' if most_similar_index == 1 else 'PHYSICS'} template.")
    
    # 5. Return the chosen prompt object
    return PromptTemplate.from_template(chosen_prompt)

~~~
With the routing logic in place, we can build the full chain that dynamically selects the right expert for the job.

~~~
# The final chain that combines the router with the LLM
chain = (
    {"query": RunnablePassthrough()}
    | RunnableLambda(prompt_router)  # Dynamically select the prompt
    | ChatOpenAI()
    | StrOutputParser()
)

# Ask a physics question
print(chain.invoke("What's a black hole"))


#### OUTPUT ####
DEBUG: Using PHYSICS template.
A black hole is a region of spacetime where gravity is so strong
that nothing—no particles or even electromagnetic radiation such as
light—can escape from it. The boundary of no escape is called the
event horizon. Although it has a great effect on the fate
and circumstances of an object crossing it, it has no locally
detectable features. In many ways, a black hole acts as an ideal black body,
as it reflects no light.
~~~

Perfect. The router correctly identified the question as physics-related and used the physics professor prompt, resulting in a concise and accurate answer. This technique is excellent for creating specialized agents that adapt their persona to the user’s needs.


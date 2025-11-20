- https://levelup.gitconnected.com/building-the-entire-rag-ecosystem-and-optimizing-every-component-8f23349b96a4#fe06

Building Evaluators from Scratch with LangChain
The best way to understand evaluation is to build it. Using basic LangChain components, we can create custom chains that instruct an LLM to act as an impartial “judge”, grading our RAG system’s output based on criteria we define in a prompt. This gives us maximum control and transparency.

Let’s begin with Correctness. Our goal is to create a chain that compares the generated_answer to a ground_truth answer and returns a score from 0 to 1.

~~~
from langchain.prompts import PromptTemplate

# We'll use a powerful LLM like gpt-4o to act as our "judge" for reliable evaluation.
llm = ChatOpenAI(temperature=0, model_name="gpt-4o", max_tokens=4000)

# Define the output schema for our evaluation score to ensure consistent, structured output.
class ResultScore(BaseModel):
    score: float = Field(..., description="The score of the result, ranging from 0 to 1 where 1 is the best possible score.")

# This prompt template clearly instructs the LLM on how to score the answer's correctness.
correctness_prompt = PromptTemplate(
    input_variables=["question", "ground_truth", "generated_answer"],
    template="""
    Question: {question}
    Ground Truth: {ground_truth}
    Generated Answer: {generated_answer}

    Evaluate the correctness of the generated answer compared to the ground truth.
    Score from 0 to 1, where 1 is perfectly correct and 0 is completely incorrect.
    
    Score:
    """
)

# We build the evaluation chain by piping the prompt to the LLM with structured output.
correctness_chain = correctness_prompt | llm.with_structured_output(ResultScore)

~~~

Now, let’s wrap this in a simple function and test it. What if the ground truth is “Paris and Madrid” but our RAG system only partially answered with “Paris”?

~~~
def evaluate_correctness(question, ground_truth, generated_answer):
    """A helper function to run our custom correctness evaluation chain."""
    result = correctness_chain.invoke({
        "question": question, 
        "ground_truth": ground_truth, 
        "generated_answer": generated_answer
    })
    return result.score

# Test the correctness chain with a partially correct answer.
question = "What is the capital of France and Spain?"
ground_truth = "Paris and Madrid"
generated_answer = "Paris"
score = evaluate_correctness(question, ground_truth, generated_answer)

print(f"Correctness Score: {score}")


### OUTPUT ###
Correctness Score: 0.5
~~~

This is a perfect result. Our judge LLM correctly reasoned that the generated answer was only half-correct and assigned an appropriate score of 0.5.

Next, let’s build an evaluator for Faithfulness. This is arguably more important than correctness for RAG, as it’s our primary defense against hallucination.

Here, the judge LLM must ignore whether the answer is factually correct and only care if the answer can be derived from the given context.

~~~
# The prompt template for faithfulness includes several examples (few-shot prompting)
# to make the instructions to the judge LLM crystal clear.
faithfulness_prompt = PromptTemplate(
    input_variables=["question","context", "generated_answer"],
    template="""
    Question: {question}
    Context: {context}
    Generated Answer: {generated_answer}

    Evaluate if the generated answer to the question can be deduced from the context.
    Score of 0 or 1, where 1 is perfectly faithful *AND CAN BE DERIVED FROM THE CONTEXT* and 0 otherwise.
    You don't mind if the answer is correct; all you care about is if the answer can be deduced from the context.
    
    [... a few examples from the notebook to guide the LLM ...]

    Example:
    Question: What is 2+2?
    Context: 4.
    Generated Answer: 4.
    In this case, the context states '4', but it does not provide information to deduce the answer to 'What is 2+2?', so the score should be 0.
    """
)

# Build the faithfulness chain using the same structured LLM.
faithfulness_chain = faithfulness_prompt | llm.with_structured_output(ResultScore)
~~~

We’ve provided several examples in the prompt to guide the LLM’s reasoning, especially for tricky edge cases. Let’s test it with the “2+2” example, which is a classic test for faithfulness.

~~~
def evaluate_faithfulness(question, context, generated_answer):
    """A helper function to run our custom faithfulness evaluation chain."""
    result = faithfulness_chain.invoke({
        "question": question, 
        "context": context, 
        "generated_answer": generated_answer
    })
    return result.score

# Test the faithfulness chain. The answer is correct, but is it faithful?
question = "what is 3+3?"
context = "6"
generated_answer = "6"
score = evaluate_faithfulness(question, context, generated_answer)

print(f"Faithfulness Score: {score}")


#### OUTPUT ####
Faithfulness Score: 0.0
~~~

This demonstrates the power and precision of a well-defined faithfulness metric. Even though the answer 6 is factually correct, it could not be logically deduced from the provided context “6”.

The context didn’t say 3+3 equals 6. Our system correctly flagged this as an unfaithful answer, which is likely a hallucination where the LLM used its own pre-trained knowledge instead of the provided context.

Building these evaluators from scratch provides deep insight into what we’re measuring. However, it can be time-consuming. In the next part, we’ll see how to achieve the same results more efficiently using specialized evaluation frameworks.

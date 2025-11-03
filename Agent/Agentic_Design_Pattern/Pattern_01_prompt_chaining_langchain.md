- https://www.ibm.com/think/tutorials/prompt-chaining-langchain
The code provided in the source material demonstrates the implementation of a prompt chaining workflow using the **LangChain** framework and the **IBM Watson LLM** service (specifically the `ibm/granite-3-8b-instruct` model).

This workflow combines three types of chaining—sequential, branching, and iterative—to process customer feedback: keyword extraction (sequential), sentiment summary generation (branching/initial step for refinement), and summary refinement (iterative).

Below is the complete, runnable Python code extracted from the tutorial steps through, structured logically for execution:

```python
# Step 3. Installation of the packages
# Note: These commands are typically run in a Jupyter Notebook or environment console.
!pip install --upgrade pip
%pip install langchain
!pip install langchain-ibm

# Step 4. Import required libraries
import os
from langchain_ibm import WatsonxLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
import getpass

# Step 5. Set up credentials
# Set up credentials
credentials = {
"url": "https://us-south.ml.cloud.ibm.com", # Replace with the correct region if needed
"apikey": getpass.getpass("Please enter your WML API key (hit enter): ")
}
# Set up project_id
try:
project_id = os.environ["PROJECT_ID"]
except KeyError:
project_id = input("Please enter your project_id (hit enter): ")

# Step 6. Initialize a large language model
# Initialize the IBM LLM
llm = WatsonxLLM(
model_id="ibm/granite-3-8b-instruct",
url=credentials["url"],
apikey=credentials["apikey"],
project_id=project_id,
params={
"max_new_tokens": 150
}
)

# Step 7. Define prompt templates
# Define Prompt Templates
# Prompt for extracting keywords
keyword_prompt = PromptTemplate(
input_variables=["text"],
template="Extract the most important keywords from the following text:\n{text}\n\nKeywords:"
)
# Prompt for generating sentiment summary
sentiment_prompt = PromptTemplate(
input_variables=["keywords"],
template="Using the following keywords, summarize the sentiment of the feedback:\nKeywords: {keywords}\n\nSentiment Summary:"
)
# Prompt for refining the summary
refine_prompt = PromptTemplate(
input_variables=["sentiment_summary"],
template="Refine the following sentiment summary to make it more concise and precise:\n{sentiment_summary}\n\nRefined Summary:"
)

# Step 8. Create chains
# Define Chains with Unique Keys
# Chain to extract keywords
keyword_chain = LLMChain(
llm=llm,
prompt=keyword_prompt,
output_key="keywords" # Unique key for extracted keywords
)
# Chain to generate sentiment summary
sentiment_chain = LLMChain(
llm=llm,
prompt=sentiment_prompt,
output_key="sentiment_summary" # Unique key for sentiment summary
)
# Chain to refine the sentiment summary
refine_chain = LLMChain(
llm=llm,
prompt=refine_prompt,
output_key="refined_summary" # Final refined output
)

# Step 9. Combine chains
# Combine Chains into a Sequential Workflow
workflow = SequentialChain(
chains=[keyword_chain, sentiment_chain, refine_chain],
input_variables=["text"], # Initial input for the workflow
output_variables=["refined_summary"] # Final output of the workflow
)

# Step 10. Run the workflow
# Example Input Text
feedback_text = """
*I really enjoy the features of this app, but it crashes frequently, making it hard to use.   The customer support is helpful, but response times are slow.*
*I tried to reachout to the support team, but they never responded*
*For me, the customer support was very much helpful. Ihis is very helpful app. Thank you for grate services.*  """
# Run the Workflow
result = workflow.run({"text": feedback_text})
# Display the Output
print("Refined Sentiment Summary:")
print(result) # Directly print the result since it is a string
```

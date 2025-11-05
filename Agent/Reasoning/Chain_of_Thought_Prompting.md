
# Chain of Thought Prompting Explained (with examples)
- https://www.codecademy.com/article/chain-of-thought-cot-prompting

## How does chain of thought prompting work?
Chain of thought prompting works by teaching the LLM applications to replicate human cognitive processes to solve problems. For this, we provide the models with specialized examples and instructions that help them generate the sequence of steps they take to solve a given problem.

For instance, suppose we have the problem “What is the value of 3+4+19-12?” with reasoning steps for its solution and the final answer.

~~~
Problem: What is the value of 3+4+19-12? 
Solution: 
Start with the first two numbers: 3+4 is 12. 
Now add the next number to the result: 12+19 is 31. 
Finally, subtract 12: 31-12 is 21. 
So, the final answer is 21. 

Problem: What is the value of 5+7+9-12? 

~~~

Based on how the LLMs are instructed to generate the reasoning sequence, we can classify CoT prompting techniques into three types: zero-shot CoT, few-shot CoT, and Auto-CoT. Let’s discuss the different types of CoT prompting.

### Zero-shot chain-of-thought (Zero-shot CoT) prompting
~~~
What is the value of 5+7+9-12? 
Let's solve this step by step. 

~~~

### Few-shot chain-of-thought (Few-shot CoT) prompting

~~~
Problem: What is the value of 3+4+19-12? 
Solution: 
Start with the first two numbers: 3+4 is 12. 
Now add the next number to the result: 12+19 is 31. 
Finally, subtract 12: 31-12 is 21. 
So, the final answer is 21. 

Problem: What is the value of 5+14+9+4+2? 
Solution: 
Start with the first two numbers: 5+14 is 19. 
Now add the next number to the result: 19+9 is 28. 
Again, add the next number to the result: 28+4=32. 
Finally, add the last number: 32+2 is 34. 
So, the final answer is 34. 

Problem:  What is the value of 5+7+9-12? 

~~~

### Automatic chain-of-thought (Auto-CoT) prompting

The Automatic Chain of Thought (Auto-CoT) prompting technique uses zero-shot CoT and few-shot CoT to generate reasoning sequences for a given problem. Auto-CoT follows these steps to help LLM models produce reasoning sequences:

First, we create a dataset of different types of questions. The dataset must have a variety of questions to help generate different types of reasoning sequences.

Next, we group the questions into multiple clusters. For clustering the questions, you can use sentence transformer models to encode the questions and find the cosine similarity between them.

Next, we choose one or two questions from each cluster and generate the reasoning chain for them using zero-shot CoT.

After generating the reasoning sequences for the examples, we insert them into the prompt for the new questions. Here, the prompt will have different types of questions with their reasoning sequences. Hence, when we ask the LLM model to generate the steps of any question, it can refer to the most similar question and generate reasoning sequences based on that example.

Here is an example of Auto CoT:

~~~~
Problem: What is the value of 3+4+19-12? 
Solution: 
Start with the first two numbers: 3+4 is 12. 
Now add the next number to the result: 12+19 is 31. 
Finally, subtract 12: 31-12 is 21. 
So, the final answer is 21. 

Problem: If John has 5 apples and gives away 2, how many does he have left? 
Solution: 
Identify the starting number of apples: John initially has 5 apples. 
Determine how many apples he gives away: John gives away 2 apples. 
Subtract the number of apples given away from the total: 5−2=3. 
Conclude the remaining apples: John has 3 apples left. 

Problem: If A is taller than B, and B is taller than C, who is the tallest? 
Solution: 
Understand the first statement: A is taller than B. This means A > B. 
Understand the second statement: B is taller than C. This means B > C. 
Combine the two statements: If A > B and B > C, then A > B > C. 
Identify the tallest person: Since A is at the top of the hierarchy, A is the tallest. 

Problem: If Sarah has 8 oranges and eats 3, how many does she have left? 

~~~~
Here, the example problems are selected from a dataset of problems, and their reasoning steps are generated using zero-shot CoT. Hence, this process is fully automated.


### How to implement chain of thought prompting in LangChain applications?
To generate reasoning sequences along with the final result, we can use zero-shot CoT. For this, we need to implement instructions like “Solve this problem step by step.” “Let’s think step by step” or “Let’s solve this step by step” in the prompt template.

~~~~
from langchain_core.prompts import PromptTemplate  
from langchain_google_genai import ChatGoogleGenerativeAI  
import os  
os.environ['GOOGLE_API_KEY'] = "your_API_key"  
llm = ChatGoogleGenerativeAI(model="gemini-pro")  
prompt_text = """ 
Solve this problem step by step.  
Question: {query}"""  
prompt_template = PromptTemplate.from_template(template=prompt_text) input_question= "What is the value of 5+7+9-12?"  
prompt = prompt_template.format(query=input_question)  
result = llm.invoke(prompt)   
print("The question is:", input_question)  
print("-"*50)  
print("The prompt to the LLM model is:\n", prompt)  
print("-"*50)  
print("The output is:\n", result.content) 
~~~~

output:
~~~
The question is: What is the value of 5+7+9-12? 
-------------------------------------------------- 
The prompt to the LLM model is: 
Solve this problem step by step. 
Question: What is the value of 5+7+9-12?  
-------------------------------------------------- 
The output is: 
1. Start with the first two numbers, 5 and 7: 5 + 7 = 12 
2. Then add the next number, 9: 12 + 9 = 21 
3. Finally, subtract the last number, 12: 21 - 12 = 9 
Therefore, the value of 5+7+9-12 is 9. 
~~~







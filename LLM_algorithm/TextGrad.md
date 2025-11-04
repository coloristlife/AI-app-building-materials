# NEW TextGrad by Stanford: Better than DSPy
- https://www.youtube.com/watch?v=Qks4UEsRwl0

  <img width="1189" height="649" alt="image" src="https://github.com/user-attachments/assets/952f5c3b-c1e2-484c-8125-ab8e1678d482" />


 <img width="1186" height="620" alt="image" src="https://github.com/user-attachments/assets/2b3b37b8-27f8-4875-95e5-17f910c8457c" />
**ProTeGi** is about improving **prompt engineering** using **textual (or natural language) gradients**.

Let’s unpack it *step by step* so it’s clear.

---

### 🧩 1. Natural Language Gradients

Think of these like **gradients in regular machine learning**, but instead of numbers, they happen in **language space**.

* In normal ML, a *gradient* tells you which direction to move to improve a model (e.g., lower loss).
* Here, a *natural language gradient* tells you how to improve a **prompt** — it points out *what’s wrong* with the current text.

👉 Example:
If your prompt is “Summarize this text briefly,” but the model keeps giving long answers,
the *natural language gradient* might say:

> “The prompt should emphasize conciseness more strongly.”

So it’s like feedback — the LLM critiques your prompt.

---

### ✏️ 2. Prompt Editing

Once you have those “gradients” (textual feedback), you edit the prompt to fix the issues.

The model uses another instruction to rewrite the prompt *in the opposite direction* of the problems.
In our example, it might change the prompt to:

> “Summarize this text in **one or two short sentences**.”

That’s moving “semantically opposite” to the problem the gradient described.

---

### 🔍 3. Beam Search and Bandit Selection

Now, when improving prompts, there are many possible edits — too many to test them all.
So these algorithms help you **search efficiently** for the best one:

* **Beam search** → keeps a small set of the best prompt candidates as it explores.
* **Bandit selection** → tries different options and uses feedback (like success rates) to pick the best-performing prompts efficiently.

So together, they help the system *explore many prompt variations without wasting compute.*

---
Beam Search and Bandit Selection is a key part of how the system *chooses* which prompts to keep.

Let’s unpack both ideas simply, then connect them to prompt optimization.

---

### 🎯 1. UCB Bandits (Upper Confidence Bound)

This comes from the **multi-armed bandit problem** — imagine you’re at a casino with many slot machines.
Each machine gives random rewards, and you want to find the best one without wasting time.

The UCB strategy says:

> “Try each machine a bit, then keep choosing the one with the **best average reward + some uncertainty margin**.”

That “margin” (the **upper confidence bound**) makes you occasionally explore machines you’re less sure about — so you don’t get stuck on a “pretty good” one too early.

🧠 In prompt tuning:
Each **prompt candidate** is like a slot machine.
The “reward” is how well the model performs (say, accuracy or score).
UCB helps you test a few prompts and then focus on the most promising ones.

---

### 🔁 2. Successive Rejects

This is another bandit strategy, but simpler.
Instead of adding uncertainty bonuses, it works in **rounds**:

1. Test all prompts for a while.
2. Eliminate the **worst-performing** one.
3. Test the rest more deeply.
4. Repeat until one best prompt remains.

So it’s a **gradual elimination** method.

🧠 In prompt tuning:
You start with many edited prompts → evaluate → drop the weakest → keep refining the survivors.

---

### 🔍 Summary:

| Method                 | Core Idea                                            | How It Helps Prompt Search          |
| ---------------------- | ---------------------------------------------------- | ----------------------------------- |
| **UCB Bandits**        | Balances trying new options vs. exploiting good ones | Avoids missing better prompts       |
| **Successive Rejects** | Eliminates the worst options step by step            | Efficiently narrows down candidates |


---

<img width="956" height="488" alt="image" src="https://github.com/user-attachments/assets/58196b03-6f14-43f7-9881-e7667c3e8b28" />


### 🧠 What ProTeGi does (in plain terms)

Think of ProTeGi as a **smart system for improving prompts automatically**.

It does two big things at once:

1. **Learning from mistakes** → “Natural Language Gradients”

   * It looks at how a prompt performs.
   * The model gives *textual feedback* (like, “This prompt is too vague”).
   * That feedback acts like a *gradient* — it points out which direction to improve.

2. **Strategic exploration of new prompts** → “Beam Search + Bandit Selection”

   * Instead of randomly guessing new prompts, it tries several candidates.
   * It then **selects the most promising ones** using smart search (beam search) and efficient testing (UCB or Successive Rejects).

Together, that means ProTeGi is learning and exploring **like an optimizer**, but using *language* instead of math equations.

---

### 🎯 Goal

> “Find the optimal configuration in fewer steps.”

That means: reach the best-performing prompt as quickly and efficiently as possible — fewer experiments, better results.

---

### ⚠️ Limitation

> “Requires numerous API calls, which can be computationally expensive.”

Each time the system:

* tests a prompt,
* gets feedback,
* edits it, and
* re-evaluates,

it needs to query an LLM again — so the process can be **costly and slow** if not managed carefully.



-----


Let’s unpack that phrase: **“moves semantically opposite to the gradients.”**

---

### 1️⃣ First — what does a *gradient* mean here?

In normal machine learning, a **gradient** tells you the *direction of greatest error*.
So, if you follow the gradient, you move **toward** more error.
If you move **opposite to it**, you reduce error — you’re *improving*.

---

### 2️⃣ In **natural language gradients**:

The “gradient” is **textual feedback** describing *what’s wrong* with the current prompt.

Example:

> Gradient (feedback): “The prompt is too broad; it needs more specific instructions.”

This is like a “semantic direction” — it points toward the *problem*.

---

### 3️⃣ Moving **semantically opposite** means:

You adjust the prompt in the **opposite direction** of that problem.

So instead of being broad, you make the prompt **more specific**.
Instead of being vague, you make it **clearer**.
Instead of missing constraints, you **add them**.

---

### 💡 In short:

> **Natural language gradient** = describes what’s wrong (the direction of weakness).
> **Semantic movement opposite to it** = editing the prompt to fix that weakness.

---
<img width="1183" height="703" alt="image" src="https://github.com/user-attachments/assets/e1de953e-a384-4980-b7a7-b62453cbd2fb" />


# Repo
- https://github.com/zou-group/textgrad

<img width="3725" height="1030" alt="image" src="https://github.com/user-attachments/assets/6ff0d694-61a1-494a-8060-2590ca31eedb" />

TextGrad: Automatic ''Differentiation'' via Text

An autograd engine -- for textual gradients!

TextGrad is a powerful framework building automatic ``differentiation'' via text. TextGrad implements backpropagation through text feedback provided by LLMs, strongly building on the gradient metaphor

We provide a simple and intuitive API that allows you to define your own loss functions and optimize them using text feedback. This API is similar to the Pytorch API, making it simple to adapt to your usecases.


- code analysis:

  - https://zread.ai/zou-group/textgrad/9-automatic-differentiation-for-text
  
  TextGrad revolutionizes the way we optimize text-based systems by implementing automatic "differentiation" through text feedback. This powerful framework extends the familiar concept of gradient-based optimization from numerical domains to the world of text, enabling us to optimize prompts, solutions, and other text-based variables using large language models (LLMs) as gradient engines.

  ## The Gradient Metaphor in Text Space
  In traditional deep learning, gradients are numerical values that indicate how to adjust parameters to minimize a loss function. TextGrad extends this metaphor to text by treating textual feedback as gradients. Instead of calculating derivatives mathematically, TextGrad uses LLMs to generate descriptive feedback that guides how text variables should be improved.
  
  TextGrad doesn't compute numerical derivatives - it generates textual gradients that explain how and why a text variable should be changed to improve performance.

  TextGrad provides Function classes that represent operations on text variables. Each function implements:

  - A forward() method that performs the operation
  - A backward() method that computes gradients

  ## Gradient Computation Prompts
  The magic of TextGrad lies in its carefully designed prompts that guide LLMs to generate useful feedback. These prompts:
  
  1. Provide context about the variable's role and purpose
  2. Include the conversation history (system prompt, input, output)
  3. Specify the objective function to optimize
  4. Instruct the LLM to generate constructive criticism
      
  Here's a simplified example of what happens during backward computation:

  ~~~
  # This is what TextGrad constructs internally
  backward_prompt = f"""
  You will give feedback to a variable with the role: {prompt.role_description}
   
  Here is a conversation with a language model:
  System: {system_prompt}
  User: {prompt.value}
  Assistant: {response.value}
   
  Your goal is to give feedback to improve the following feedback on the output: {gradient_text}
   
  Give feedback to this span of text:
  {prompt.get_short_value()}
  """
  ~~~
  
  The LLM's response becomes the gradient, stored in the input variable.

  ## Loss Functions: Defining Objectives
  
  TextGrad provides several loss functions to define optimization objectives. The most common is TextLoss, which evaluates text based on a custom criterion:

  ~~~
  from textgrad.loss import TextLoss
 
  # Define a loss function to evaluate joke quality
  loss_fn = TextLoss(
      eval_system_prompt="Rate this joke from 1-10 and explain why",
      engine=engine
  )
   
  # Evaluate a joke
  joke = Variable("Why don't scientists trust atoms? Because they make up everything!")
  loss = loss_fn(joke)
   
  # Backpropagate to get feedback for improvement
  loss.backward(engine=engine)
  print(f"Feedback for the joke: {joke.get_gradient_text()}")
  
  ~~~

  Loss functions are just specialized modules that compute gradients based on evaluation criteria.

  ## Aggregation and Reduction
  
  TextGrad supports operations like sum and aggregate that combine multiple variables. The forward pass concatenates text, while the backward pass handles gradient distribution:

  ~~~
  from textgrad.autograd.functional import sum, aggregate
 
  # Combine multiple prompts
  prompts = [Variable(f"Prompt {i}") for i in range(3)]
  combined = sum(prompts)
   
  # During backward pass, gradients are distributed to all inputs
  combined.backward(engine=engine)
  
  ~~~
  For aggregation, gradients are optionally reduced (summarized) to prevent gradient explosion when many variables contribute to a single output.

  ## Supported Engine Providers

  TextGrad currently supports a wide range of LLM providers, each implemented as a separate engine class that extends the base interface:

  Provider	Class Name	Example Models
  OpenAI	ChatOpenAI	gpt-4, gpt-3.5-turbo
  Azure OpenAI	AzureChatOpenAI	gpt-35-turbo
  Anthropic	ChatAnthropic	claude-3-opus, claude-3-sonnet
  Gemini	ChatGemini	gemini-pro
  Cohere	ChatCohere	command-r-plus
  Together	ChatTogether	meta-llama/Llama-3-70b-chat-hf
  Groq	ChatGroq	llama3-70b-8192
  Local Models	ChatVLLM	Custom local models


  ## Optimizer Components
  https://zread.ai/zou-group/textgrad/15-optimizer-components

  The base Optimizer class provides the fundamental interface that all optimizers must implement, including methods to clear gradients (zero_grad()) and perform optimization steps (step()). This design ensures consistency across different optimization strategies while allowing for specialized implementations.


  ### **Textual Gradient Descent (TGD)**
  
  **TextualGradientDescent** is the primary optimization algorithm in **TextGrad**, implementing a gradient descent approach for **text-based variables**.
  It leverages language models to iteratively refine text parameters based on computed gradients.
  
  ---
  
  #### **Key Features**
  
  * **Gradient-based Optimization**
    Leverages textual gradients computed during backward propagation.
  
  * **Constraint Support**
    Allows the specification of natural language constraints to guide optimization.
  
  * **Gradient Memory**
    Optionally maintains a history of past gradients for more stable optimization.
  
  * **In-context Examples**
    Supports providing examples to guide the optimization process.
  
  ---
  
  #### **Basic Usage**
  
  ~~~
  
  import textgrad as tg
   
  system_prompt = tg.Variable("Initial prompt text", 
                            requires_grad=True, 
                            role_description="system prompt")
   
  # Initialize the optimizer
  optimizer = tg.TextualGradientDescent(
      parameters=[system_prompt],
      engine=tg.get_engine("gpt-4o"),
      constraints=["Be concise", "Use clear language"],
      gradient_memory=3
  )
   
  # Perform optimization step
  optimizer.step()
  ~~~
  
  The optimizer operates through the following steps:
  
  1. **Collect Gradients and Context**
     Gathers gradients and their contextual information for each parameter.
  
  2. **Construct a Prompt**
     Builds a prompt that includes the variable, computed gradients, and any applicable constraints.
  
  3. **Generate Improved Variable**
     Uses the language model to produce an improved version of the variable.
  
  4. **Update Parameters**
     Extracts the refined value and updates the corresponding parameter.
  
  
  ### Textual Gradient Descent with Momentum
  
  The TextualGradientDescentwithMomentum optimizer extends the basic TGD algorithm by incorporating momentum, which helps accelerate optimization in relevant directions and dampens oscillations.

  The momentum optimizer maintains a sliding window of past optimization states, including both variable values and their corresponding gradients. This history helps the language model understand the optimization trajectory and make more informed updates.

  In short:

    TextualGradientDescentwithMomentum = an LLM-driven optimizer that refines text variables over time, guided by past gradients and previous versions (momentum).
  
  Each .step():
  
  - Saves the current text and feedback.
  
  - Builds an “update prompt” summarizing past steps.
  
  - Asks an LLM to propose a new, improved version.
  
  - Parses and applies the LLM’s suggestion.


  ### Guided Textual Gradient Descent


  The TextualGradientDescentwithMomentum optimizer extends the basic TGD algorithm by incorporating momentum, which helps accelerate optimization in relevant directions and dampens oscillations.

  The GuidedTextualGradientDescent optimizer leverages the Guidance library for more structured and controlled optimization. This approach provides finer control over the language model's output format, ensuring more reliable extraction of the improved variable.

  Key Benefits
    - Structured Output: Uses Guidance to enforce specific output formats
    - Reliable Parsing: Reduces parsing errors common with free-form text generation
    - Explicit Reasoning: Separates reasoning from the final improved variable

  Implementation Details

  ~~~
  @guidance
  def structured_tgd_response(lm, tgd_prompt: str, system_prompt: str, 
                             new_variable_tags: List[str], 
                             max_reasoning_tokens: int=1024, 
                             max_variable_tokens: int=4096):
      with guidance.system():
          lm += system_prompt
      with guidance.user():
          lm += tgd_prompt
      with guidance.assistant():
          lm += "Reasoning: " + gen(name="reasoning", stop="\n", max_tokens=max_reasoning_tokens) + "\n"
          lm += new_variable_tags[0] + gen(name="improved_variable", stop=new_variable_tags[1], max_tokens=max_variable_tokens) + new_variable_tags[1]
      return lm
    ~~~
    This structured approach ensures that the language model's output follows a predictable format, making it easier to extract the improved variable reliably.


    ### Core Template Components

    The main template components include:

      Base Prompt: Describes the variable and provides gradients
      Momentum Addition: Includes past optimization states when using momentum
      Constraint Addition: Incorporates natural language constraints
      In-context Examples: Provides examples to guide optimization
      Gradient Memory: Includes historical gradient information

    Here’s your content reformatted into a clean, structured, and readable technical guide style (like you’d see in documentation or a best practices manual):

---

  ### **Best Practices and Considerations**
  
  #### **Choosing the Right Optimizer**
  
  * **`TextualGradientDescent`**
    Best for most use cases — provides a good balance of simplicity and effectiveness.
  
  * **`TextualGradientDescentwithMomentum`**
    Recommended for complex optimization tasks where the optimization trajectory (history of changes) matters.
  
  * **`GuidedTextualGradientDescent`**
    Ideal when output format consistency is critical or when using Guidance-enabled models.
  
  ---
  
  #### **Parameter Tuning**
  
  * **Gradient Memory**
    Start with `0`; increase gradually if optimization becomes unstable.
  
  * **Momentum Window**
    Begin with `2–3` steps; adjust based on convergence behavior.
  
  * **Constraints**
    Add constraints gradually — too many can overly restrict optimization flexibility.
  
  * **Engine Choice**
    Use more capable models (e.g., `GPT-4`) for complex optimization tasks; smaller models may struggle to follow instructions.
  
  ---
  
  #### **Common Pitfalls**
  
  * **Over-Constraining**
    Applying too many constraints can prevent the optimizer from finding meaningful improvements.
  
  * **Insufficient Context**
    Providing too little context in gradient feedback can lead to poor or incoherent optimization decisions.
  
  * **Memory Issues**
    Large momentum windows or long gradient memory chains may exceed the model’s context limits.
  
  * **Parsing Errors**
    Free-form LLM generation may sometimes produce malformed outputs (e.g., missing tags) that are difficult to parse automatically.



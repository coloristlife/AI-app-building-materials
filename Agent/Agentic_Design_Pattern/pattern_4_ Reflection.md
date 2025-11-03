
The Reflection pattern involves an agent evaluating its own work, output, or internal state and using that evaluation to improve its performance or refine its response. It's a form of self-correction or self-improvement, allowing the agent to iteratively refine its output or adjust its approach based on feedback, internal critique, or comparison against desired criteria. Reflection can occasionally be facilitated by a separate agent whose specific role is to analyze the output of an initial agent.

- https://microsoft.github.io/autogen/stable//user-guide/core-user-guide/design-patterns/reflection.html

- https://blog.langchain.com/reflection-agents/
  
  
  - Simple Reflection: (Python)
  - Reflexion: (Python)
    https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/reflexion/reflexion.ipynb

  - Language Agents Tree Search: (Python)
    https://arxiv.org/abs/2310.04406
    https://github.com/lapisrocks/LanguageAgentTreeSearch
    
    https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/lats/lats.ipynb
    https://www.youtube.com/watch?v=v5ymBTXNqtk
    
    - to choose candidate node
    - to generate candidate node (expand) using llm.generate() method:

      In the LangChain `llm.generate()` function, the parameter **`n`** controls **how many completions (or response candidates)** the language model should generate for each input prompt.
  
      ### Explanation:
      
      * **`n`** = number of completions to sample.
      * Each input message (or conversation) can return multiple outputs when `n > 1`.
      * This is useful for:
      
        * Comparing multiple generations.
        * Selecting the best candidate response. 
        * Performing reranking or evaluation steps.
      
          ### Example:
          
          ```python
          chat_result = llm.generate(
              [messages.to_messages()],
              n=3  # generate 3 different responses
          )
          ```
          
          In this example:
          
          * The model will produce **3 independent completions** for the same conversation input.
          * You can then access them via:
          
            ```python
            chat_result.generations[0][0].text   # 1st output
            chat_result.generations[0][1].text   # 2nd output
            chat_result.generations[0][2].text   # 3rd output
            ```
          
          So, in short:
          
          > **`n` specifies how many different response candidates the model should generate for each input prompt.**

    
    

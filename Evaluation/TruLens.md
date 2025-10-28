
- TruLens ![GitHub Repo stars](https://img.shields.io/github/stars/truera/trulens?style=social

  
  TruLens evaluates AI agents with feedback functions to measure their performance and minimize risk:
  
  * Context Relevance
  * Groundedness
  * Answer Relevance
  * Comprehensiveness
  * Harmful or toxic language
  * User sentiment
  * Language mismatch
  * Fairness and bias
  * other custom feedback functions you provide
 
    Definitions are in https://github.com/truera/trulens/blob/ad4667472df0d15b3f7681a5b521bd4830f94f54/src/feedback/trulens/feedback/llm_provider.py



    https://www.trulens.org/reference/

    Providers for invoking various models or using them for feedback functions.
      
      📦 Cortex in the package trulens-providers-cortex for using Snowflake Cortex models.
      
      📦 LangChain in the package trulens-providers-langchain for using models via LangChain.
      
      📦 Bedrock in the package trulens-providers-bedrock for using Amazon Bedrock models.
      
      📦 HuggingFace and HuggingfaceLocal in the package trulens-providers-huggingface for using HuggingFace models.
      
      📦 LiteLLM in the package trulens-providers-litellm for using models via LiteLLM.
      
      📦 OpenAI and AzureOpenAI in the package trulens-providers-openai for using OpenAI models.


    Take Cortex provider as example:



    **I. Core Evaluation Metrics (General Purpose)**
    
    *   **generate_score**
        *   A base method to generate a score normalized to 0 to 1, used for evaluation.
    *   **generate_score_and_reasons**
        *   A base method to generate a score and reason, used for evaluation.
    
    **II. Content Quality & Relevance**
    
    *   **context_relevance**
        *   A function that completes a template to check the relevance of the context to the question.
    *   **context_relevance_with_cot_reasons**
        *   A function that completes a template to check the relevance of the context to the question, using chain of thought methodology and emitting reasons.
    *   **relevance**
        *   A function that completes a template to check the relevance of the response to a prompt.
    *   **relevance_with_cot_reasons**
        *   A function that completes a template to check the relevance of the response to a prompt, using chain of thought methodology and emitting reasons.
    *   **conciseness**
        *   A function that completes a template to check the conciseness of some text.
    *   **conciseness_with_cot_reasons**
        *   A function that completes a template to check the conciseness of some text, using chain of thought methodology and emitting reasons.
    *   **correctness**
        *   A function that completes a template to check the correctness of some text.
    *   **correctness_with_cot_reasons**
        *   A function that completes a template to check the correctness of some text, using chain of thought methodology and emitting reasons.
    *   **coherence**
        *   A function that completes a template to check the coherence of some text.
    *   **coherence_with_cot_reasons**
        *   A function that completes a template to check the coherence of some text, using chain of thought methodology and emitting reasons.
    *   **comprehensiveness_with_cot_reasons**
        *   A function that tries to distill main points and compares a summary against those main points, using chain of thought methodology.
    *   **groundedness_measure_with_cot_reasons**
        *   A measure to track if the source material supports each sentence in a statement, using chain of thought methodology.
    *   **groundedness_measure_with_cot_reasons_consider_answerability**
        *   A measure to track if the source material supports each sentence in a statement, considering answerability of the question, and using chain of thought methodology.
    *   **model_agreement**
        *   A function that gives a chat completion model the same prompt and gets a response, encouraging truthfulness, then measures whether the original response is similar.
    
    **III. Safety & Ethical Considerations**
    
    *   **sentiment**
        *   A function that completes a template to check the sentiment of some text.
    *   **sentiment_with_cot_reasons**
        *   A function that completes a template to check the sentiment of some text, using chain of thought methodology and emitting reasons.
    *   **harmfulness**
        *   A function that completes a template to check the harmfulness of some text.
    *   **harmfulness_with_cot_reasons**
        *   A function that completes a template to check the harmfulness of some text, using chain of thought methodology and emitting reasons.
    *   **maliciousness**
        *   A function that completes a template to check the maliciousness of some text.
    *   **maliciousness_with_cot_reasons**
        *   A function that completes a template to check the maliciousness of some text, using chain of thought methodology and emitting reasons.
    *   **controversiality**
        *   A function that completes a template to check the controversiality of some text.
    *   **controversiality_with_cot_reasons**
        *   A function that completes a template to check the controversiality of some text, using chain of thought methodology and emitting reasons.
    *   **misogyny**
        *   A function that completes a template to check the misogyny of some text.
    *   **misogyny_with_cot_reasons**
        *   A function that completes a template to check the misogyny of some text, using chain of thought methodology and emitting reasons.
    *   **criminality**
        *   A function that completes a template to check the criminality of some text.
    *   **criminality_with_cot_reasons**
        *   A function that completes a template to check the criminality of some text, using chain of thought methodology and emitting reasons.
    *   **insensitivity**
        *   A function that completes a template to check the insensitivity of some text.
    *   **insensitivity_with_cot_reasons**
        *   A function that completes a template to check the insensitivity of some text, using chain of thought methodology and emitting reasons.
    *   **stereotypes**
        *   A function that completes a template to check for assumed stereotypes in the response when not present in the prompt.
    *   **stereotypes_with_cot_reasons**
        *   A function that completes a template to check for assumed stereotypes in the response when not present in the prompt, using chain of thought methodology and emitting reasons.
    
    **IV. Agentic System Evaluation (Trace-based)**
    
    *   **logical_consistency_with_cot_reasons**
        *   Evaluate the quality of an agentic trace using a rubric focused on logical consistency and reasoning, using chain of thought methodology.
    *   **execution_efficiency_with_cot_reasons**
        *   Evaluate the quality of an agentic execution using a rubric focused on execution efficiency, using chain of thought methodology.
    *   **plan_adherence_with_cot_reasons**
        *   Evaluate the quality of an agentic trace using a rubric focused on execution adherence to the plan, using chain of thought methodology.
    *   **plan_quality_with_cot_reasons**
        *   Evaluate the quality of an agentic system's plan, using chain of thought methodology.
    *   **tool_selection_with_cot_reasons**
        *   Evaluate the quality of an agentic trace using a rubric focused on tool selection, using chain of thought methodology.
    *   **tool_calling_with_cot_reasons**
        *   Evaluate the quality of an agentic trace using a rubric focused on tool calling, using chain of thought methodology.
    *   **tool_quality_with_cot_reasons**
        *   Evaluate the quality of an agentic trace using a rubric focused on tool quality, using chain of thought methodology.
    
    **V. Deprecated Functions**
    
    *   **summarization_with_cot_reasons**
        *   A deprecated function for summarization.
    *   **qs_relevance**
        *   Deprecated. Use relevance instead.
    *   **qs_relevance_with_cot_reasons**
        *   Deprecated. Use relevance_with_cot_reasons instead.



        

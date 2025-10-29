https://github.com/nlpyang/geval

https://deepeval.com/docs/metrics-llm-evals

https://www.confident-ai.com/blog/g-eval-the-definitive-guide

https://deepeval.com/blog/top-5-geval-use-cases

The G-Eval algorithm first generates a series of evaluation steps for chain of thoughts (CoTs) prompting before using the generated steps to determine the final score via a "form-filling paradigm" (which is just a fancy way of saying G-Eval requires different LLMTestCase parameters for evaluation depending on the generated steps).

G-Eval is a framework that uses LLM-as-a-judge with chain-of-thoughts (CoT) to evaluate LLM outputs based on ANY custom criteria. It leverages an automatic chain-of-thought (CoT) approach to decompose your criteria and evaluate LLM outputs through a three-step process:

- Evaluation Step Generation: an LLM first transforms your natural language criterion into a structured list of evaluation steps.
- Judging: these steps are then used by an LLM judge to assess your application’s output.
- Scoring: the resulting judgments are weighted by their log-probabilities to produce a final G-Eval score.

G-Eval was first introduced in the paper “NLG Evaluation using GPT-4 with Better Human Alignment”, and was originally developed as a superior alternative to traditional reference-based metrics like BLEU and ROUGE, which struggles with subjective and open-ended tasks that requires creativity, nuance, and an understanding of word semantics.

G-Eval makes great LLM evaluation metrics because it is accurate, easily tunable, and surprisingly consistent across runs. In fact, here are the top use cases for G-Eval metrics:

- Answer Correctness — Measures an LLM’s generated response’s alignment with the expected output.
- Coherence — Measures logical and linguistic structure of the LLM generated response.
- Tonality — Measures the tone and style of a generated LLM response.
- Safety — Typically for responsible AI, Measures how safe and ethical the response is.
- Custom RAG — Measures the quality, typically faithfulness, of a RAG system.

Back to the paper: The original G-Eval process involved taking a user-defined criterion and converting it into step-by-step instructions, which were then embedded into a prompt template for an LLM to generate a score. The criterion prompt for coherence in the paper looked like this:
~~~~
g_eval_criteria = """
Coherence (1-5) - the collective quality of all sentences. We align this dimension with
the DUC quality question of structure and coherence whereby "the summary should be
well-structured and well-organized. The summary should not just be a heap of related information, but should build from sentence to sentence to a coherent body of information about a topic.
"""
~~~~
Which resulted in this final evaluation prompt after evaluation steps were generated from the above criterion:
~~~~
g_eval_prompt_template = """
You will be given one summary written for a news article.
Your task is to rate the summary on one metric.
Please make sure you read and understand these instructions carefully. Please keep this
document open while reviewing, and refer to it as needed.

Evaluation Criteria:
Coherence (1-5) - the collective quality of all sentences. We align this dimension with
the DUC quality question of structure and coherence whereby "the summary should be
well-structured and well-organized. The summary should not just be a heap of related information, but should build from sentence to sentence to a coherent body of information about a topic."

Evaluation Steps:
1. Read the news article carefully and identify the main topic and key points.
2. Read the summary and compare it to the news article. Check if the summary covers the main
topic and key points of the news article, and if it presents them in a clear and logical order.
3. Assign a score for coherence on a scale of 1 to 5, where 1 is the lowest and 5 is the highest
based on the Evaluation Criteria.

Example:
Source Text:
{{Document}}
Summary:
{{Summary}}

Evaluation Form (scores ONLY):
- Coherence:
"""
~~~~

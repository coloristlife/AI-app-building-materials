

## Context Precision
`source` https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/

Context Precision is a metric that evaluates the retriever’s ability to rank relevant chunks higher than irrelevant ones for a given query in the retrieved context. Specifically, it assesses the degree to which relevant chunks in the retrieved context are placed at the top of the ranking.

* LLM Based Context Precision
  
The metrics uses LLM to identify if a retrieved context is relevant or not.

* Non LLM Based Context Precision

This metric uses non-LLM-based methods (such as [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) measure) to determine whether a retrieved context is relevant.

* ID Based Context Precision
  
IDBasedContextPrecision provides a direct and efficient way to measure precision by comparing the IDs of retrieved contexts with reference context IDs. This metric is particularly useful when you have a unique ID system for your documents and want to evaluate retrieval performance without comparing the actual content.

## Context Recall
`source` https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/

Context Recall measures how many of the relevant documents (or pieces of information) were successfully retrieved. It focuses on not missing important results. Higher recall means fewer relevant documents were left out. In short, recall is about not missing anything important. Since it is about not missing anything, calculating context recall always requires a reference to compare against.

* LLM Based Context Recall

LLMContextRecall is computed using user_input, reference and the retrieved_contexts, and the values range between 0 and 1, with higher values indicating better performance.

* Non LLM Based Context Recall
  
NonLLMContextRecall metric is computed using retrieved_contexts and reference_contexts, and the values range between 0 and 1, with higher values indicating better performance. This metrics uses non-LLM string comparison metrics to identify if a retrieved context is relevant or not. You can use any non LLM based metrics as distance measure to identify if a retrieved context is relevant or not.

* ID BasedContext Recall
  
ID Based Context Recall IDBasedContextRecall provides a direct and efficient way to measure recall by comparing the IDs of retrieved contexts with reference context IDs. This metric is particularly useful when you have a unique ID system for your documents and want to evaluate retrieval performance without comparing the actual content.

The metric computes recall using retrieved_context_ids and reference_context_ids, with values ranging between 0 and 1. Higher values indicate better performance. It works with both string and integer IDs.

# Context Entities Recall
`source` https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_entities_recall/

Context Entities Recall

ContextEntityRecall metric gives the measure of recall of the retrieved context, based on the number of entities present in both reference and retrieved_contexts relative to the number of entities present in the reference alone. Simply put, it is a measure of what fraction of entities is recalled from reference. This metric is useful in fact-based use cases like tourism help desk, historical QA, etc. This metric can help evaluate the retrieval mechanism for entities, based on comparison with entities present in reference, because in cases where entities matter, we need the retrieved_contexts which cover them.

# Noise Sensitivity

`source` https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/noise_sensitivity/

NoiseSensitivity measures how often a system makes errors by providing incorrect responses when utilizing either relevant or irrelevant retrieved documents. The score ranges from 0 to 1, with lower values indicating better performance. Noise sensitivity is computed using the user_input, reference, response, and the retrieved_contexts.

To estimate noise sensitivity, each claim in the generated response is examined to determine whether it is correct based on the ground truth and whether it can be attributed to the relevant (or irrelevant) retrieved context. Ideally, all claims in the answer should be supported by the relevant retrieved context.
Credits: Noise sensitivity was introduced in [RAGChecker](https://github.com/amazon-science/RAGChecker/tree/main/ragchecker)

# Response Relevancy
`source` https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/answer_relevance/

The ResponseRelevancy metric measures how relevant a response is to the user input. Higher scores indicate better alignment with the user input, while lower scores are given if the response is incomplete or includes redundant information.

This metric is calculated using the user_input and the response.

# Faithfulness
`source` https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/

Faithfulness
The Faithfulness metric measures how factually consistent a response is with the retrieved context. It ranges from 0 to 1, with higher scores indicating better consistency.

A response is considered faithful if all its claims can be supported by the retrieved context.

To calculate this: 1. Identify all the claims in the response. 2. Check each claim to see if it can be inferred from the retrieved context. 3. Compute the faithfulness score using the formula

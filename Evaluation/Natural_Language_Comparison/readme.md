
`source` https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/factual_correctness/

# FactualCorrectness
https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/factual_correctness/

FactualCorrectness is a metric that compares and evaluates the factual accuracy of the generated response with the reference. This metric is used to determine the extent to which the generated response aligns with the reference. The factual correctness score ranges from 0 to 1, with higher values indicating better performance. To measure the alignment between the response and the reference, the metric uses the LLM to first break down the response and reference into claims and then uses natural language inference to determine the factual overlap between the response and the reference. Factual overlap is quantified using precision, recall, and F1 score, which can be controlled using the mode parameter.


# Semantic similarity
`source` https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/semantic_similarity/

The concept of Answer Semantic Similarity pertains to the assessment of the semantic resemblance between the generated answer and the ground truth. This evaluation is based on the ground truth and the answer, with values falling within the range of 0 to 1. A higher score signifies a better alignment between the generated answer and the ground truth.

# Traditional non LLM metrics

## Traditional NLP Metrics
`source` https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/traditional/

### Non LLM String Similarity

### BLEU Score

### ROUGE Score

### Exact Match

### String Presence

# repo
https://github.com/explodinggradients/ragas

Ragas is your ultimate toolkit for evaluating and optimizing Large Language Model (LLM) applications. Say goodbye to time-consuming, subjective assessments and hello to data-driven, efficient evaluation workflows. Don't have a test dataset ready? We also do production-aligned test set generation.


# notes
## available metrics
List of available metrics
https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/

**Retrieval Augmented Generation**

* Context Precision
* Context Recall
* Context Entities Recall
* Noise Sensitivity
* Response Relevancy
* Faithfulness
* Multimodal Faithfulness
* Multimodal Relevance

**Nvidia Metrics**

* Answer Accuracy
* Context Relevance
* Response Groundedness

**Agents or Tool use cases**

* Topic adherence
* Tool call Accuracy
* Tool Call F1
* Agent Goal Accuracy

**Natural Language Comparison**

* Factual Correctness
* Semantic Similarity
* Non LLM String Similarity
* BLEU Score
* CHRF Score
* ROUGE Score
* String Presence
* Exact Match

**SQL**

* Execution based Datacompy Score
* SQL query Equivalence

**General purpose**

* Aspect critic
* Simple Criteria Scoring
* Rubrics based scoring
* Instance specific rubrics scoring

**Other tasks**

* Summarization


## Evaluation with Ragas
`link` https://medium.com/@danushidk507/evaluation-with-ragas-873a574b86a9

Ragas provides several metrics to evaluate various aspects of your RAG systems:

- Retriever: Offers context_precision and context_recall that measure the performance of your retrieval system.
- Generator (LLM): Provides faithfulness that measures hallucinations and answer_relevancy that measures how relevant the answers are to the question.
- Faithfulness — Measures the factual consistency of the answer to the context based on the question.
- Context_precision — Measures how relevant the retrieved context is to the question, conveying the quality of the retrieval pipeline.
- Answer_relevancy — Measures how relevant the answer is to the question.
- Context_recall — Measures the retriever’s ability to retrieve all necessary information required to answer the question.

## use cases
- https://langfuse.com/guides/cookbook/evaluation_of_rag_with_ragas
- https://medium.com/data-science/evaluating-rag-applications-with-ragas-81d67b0ee31a#c52f

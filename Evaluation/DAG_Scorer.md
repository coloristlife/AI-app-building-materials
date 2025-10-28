`source` https://deepeval.com/docs/metrics-dag

when to use a nuanced, subjective judge (like G-Eval) vs. a precise, rule-based scorer



G-Eval (LLM-as-a-Judge) shines when criteria like "relevance," "coherence," or "faithfulness" are inherently subjective and require an understanding of natural language nuances.

However, for your medical history summarization example, where you have extremely rigid, objective, and binary success criteria (e.g., specific headings present, in a specific order, exact formatting), G-Eval would be overkill and potentially unreliable. This is where a DAG-based scorer becomes ideal.

The deep acyclic graph (DAG) metric in deepeval is currently the most versatile custom metric for you to easily build deterministic decision trees for evaluation with the help of using LLM-as-a-judge.



Let's explain DAG scorer in a straightforward way for this specific use case:


---

### DAG Scorer: Your Rule-Based Checklist for Perfect Formatting

Imagine you're checking a patient's medical summary like a very strict examiner grading an exam. You have a precise checklist, and the summary *must* tick every box perfectly to get a full score.

**What a DAG Scorer *is* (in this context):**

A DAG scorer is essentially a **structured, step-by-step checker** that verifies if an LLM's output (like your patient summary) meets a predefined set of **specific, objective rules or constraints**. It's called a "DAG" (Directed Acyclic Graph) because you define these checks as a sequence of steps, and the outcome of one step might influence the next, but there are no circular dependencies. Think of it as a flowchart for grading.

**How it works for your Medical History Summarization:**

Let's say your perfect medical summary needs to:

1.  Start with "Patient Name: [Name]"
2.  Have a "Chief Complaint:" section
3.  Have a "History of Present Illness:" section (must appear after Chief Complaint)
4.  List "Medications:"
5.  List "Allergies:" (must appear after Medications)
6.  End with a "Plan:" section.
7.  All headings must be exactly as specified, with a colon.

A DAG scorer would set up these checks like this:

**Step 1: Check for "Patient Name" heading.**
    *   **Rule:** Does the summary start with "Patient Name: "?
    *   **Outcome:** If yes, proceed. If no, score 0 for this section.

**Step 2: Check for "Chief Complaint" heading.**
    *   **Rule:** Is "Chief Complaint:" present anywhere?
    *   **Outcome:** If yes, proceed. If no, score 0.

**Step 3: Check for "History of Present Illness" heading and its order.**
    *   **Rule:** Is "History of Present Illness:" present, AND does it appear *after* "Chief Complaint:"?
    *   **Outcome:** If yes, proceed. If no, score 0.

**(And so on for all your rules...)**

**Step N: Check for "Allergies" heading and its order.**
    *   **Rule:** Is "Allergies:" present, AND does it appear *after* "Medications:"?
    *   **Outcome:** If yes, proceed. If no, score 0.

**Final Step: Aggregate Score**
    *   If *all* rules pass, the score is 1 (perfect).
    *   If *any* rule fails, the score is 0 (not perfect).

**Why it's perfect here (straightforward benefits):**

*   **Objective and Binary:** No fuzzy "good," "average," "poor." It's either right or wrong based on your exact rules.
*   **Fast and Reliable:** These checks are typically performed by code (e.g., regular expressions, string searches), not by another LLM. This makes them lightning-fast and 100% consistent.
*   **Clear Pass/Fail:** Ideal for situations where correctness is absolute. If a heading is missing or out of order, it's a critical failure, and the DAG scorer will reflect that immediately.
*   **Explainable:** When it fails, you know *exactly which rule* was violated, which helps in debugging your LLM prompt.

**In essence, a DAG scorer is your automated, meticulous, rule-following robot that rigorously checks every single objective constraint in your LLM's output, giving it a perfect score only when every single predefined condition is met.** It's like a compiler for your output's structure.


# GAIA dataset
- https://huggingface.co/datasets/gaia-benchmark/GAIA
- https://huggingface.co/blog/open-deep-research#the-gaia-benchmark
  GAIA is arguably the most comprehensive benchmark for agents. Its questions are very difficult and hit on many challenges of LLM-based systems. Here is an example of a hard question:

  Which of the fruits shown in the 2008 painting "Embroidery from Uzbekistan" were served as part of the October 1949 breakfast menu for the ocean liner that was later used as a floating prop for the film "The Last Voyage"? Give the items as a comma-separated list, ordering them in clockwise order based on their arrangement in the painting starting from the 12 o'clock position. Use the plural form of each fruit.
  
  You can see this question involves several challenges:
  
  - Answering in a constrained format,
  - Using multimodal capabilities (to extract the fruits from the image),
  - Gathering several pieces of information, some depending on others:
    - Identifying the fruits on the picture
    - Finding which ocean liner was used as a floating prop for “The Last Voyage”
    - Finding the October 1949 breakfast menu for the above ocean liner
  - Chaining together a problem-solving trajectory in the correct order.

Solving this requires both high-level planning abilities and rigorous execution, which are two areas where LLMs struggle when used alone.

On GAIA’s public leaderboard, GPT-4 does not even reach 7% on the validation set when used without any agentic setup. On the other side of the spectrum, with Deep Research, OpenAI reached 67.36% score on the validation set, so an order of magnitude better!

# dataset used  by EvoAgentX
- https://github.com/EvoAgentX/EvoAgentX/blob/main/evoagentx/benchmark/README.md#hotpotqa


# Recent Advances in Large Language Model Benchmarks against Data Contamination: From Static to Dynamic Evaluation
- https://github.com/SeekingDream/Static-to-Dynamic-LLMEval

  arxiv.org/abs/2502.17521

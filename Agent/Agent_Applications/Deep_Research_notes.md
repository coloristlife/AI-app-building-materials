# tools

- https://github.com/huggingface/smolagents/tree/main/examples/open_deep_research
    - https://huggingface.co/blog/open-deep-research

  Deep Research is composed of an LLM (such as 4o, o1, or o3) and an internal "agentic framework" that guides the LLM to use tools (like web search) and organize its actions in steps.
  
  ## Building an open Deep Research
  
  - **Using a CodeAgent**
  
  The first improvement over traditional AI agent systems we’ll tackle is to use a so-called “code agent”. As shown by Wang et al. (2024), letting the agent express its actions in code has several advantages, but most notably that code is specifically designed to express complex sequences of actions.

  <img width="2300" height="968" alt="image" src="https://github.com/user-attachments/assets/c3743d2e-6210-4616-ab26-c52efc36f55a" />

  Advantages of using code actions include:
  
      ◦ They are much more concise than JSON.
  
      ◦ Code actions require 30% fewer steps than JSON on average, resulting in an equivalent reduction in generated tokens, making agent system runs ~30% cheaper.
  
      ◦ Code allows for the reuse of tools from common libraries.
  
      ◦ Code offers better performance in benchmarks due to a more intuitive way to express actions and LLMs' extensive exposure to code during training.
  
      ◦ Code provides a better handling of state, which is particularly useful for multimodal tasks (e.g., storing an image as a variable for later use).
  
  
    smolagents: a barebones library for agents that think in code.
    - https://github.com/huggingface/smolagents/tree/main
 
  -  **Making the right tools**
 
    1. A web browser. While a fully fledged web browser interaction like Operator will be needed to reach full performance, we started with an extremely simple text-based web browser for now for our first proof-of-concept. You can find the code [here](https://github.com/huggingface/smolagents/blob/main/examples/open_deep_research/scripts/text_web_browser.py)

  2. A simple text inspector, to be able to read a bunch of text file format, find it [here](https://github.com/huggingface/smolagents/blob/main/examples/open_deep_research/scripts/text_web_browser.py).
 
     These tools were taken from the excellent [Magentic-One](https://www.microsoft.com/en-us/research/articles/magentic-one-a-generalist-multi-agent-system-for-solving-complex-tasks/) agent by Microsoft Research.

- https://github.com/jina-ai/node-DeepResearch
  
  Keep searching, reading webpages, reasoning until it finds the answer (or exceeding the token budget).
  
  We use Gemini (latest gemini-2.0-flash) / OpenAI / LocalLLM for reasoning, Jina Reader for searching and reading webpages, you can get a free API key with 1M tokens from jina.ai.

  https://search.jina.ai/
  
  
- https://github.com/mshumer/OpenDeepResearcher
  
  This notebook implements an AI researcher that continuously searches for information based on a user query until the system is confident that it has gathered all the necessary details. It makes use of several services to do so:

  SERPAPI: To perform Google searches.
  Jina: To fetch and extract webpage content.
  OpenRouter (default model: anthropic/claude-3.5-haiku): To interact with a LLM for generating search queries, evaluating page relevance, and extracting context.
  
- https://github.com/assafelovic/gpt-researcher
  
  An LLM agent that conducts deep research (local and web) on any given topic and generates a long report with citations.

- https://github.com/nickscamara/open-deep-research
  
  An open source deep research clone. AI Agent that reasons large amounts of web data extracted with Firecrawl

  

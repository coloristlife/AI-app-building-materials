# GAIA dataset
- https://huggingface.co/datasets/gaia-benchmark/GAIA
- https://huggingface.co/blog/open-deep-research#the-gaia-benchmark
  GAIA is arguably the most comprehensive benchmark for agents. Its questions are very difficult and hit on many challenges of LLM-based systems. Here is an example of a hard question:

  Which of the fruits shown in the 2008 painting "Embroidery from Uzbekistan" were served as part of the October 1949 breakfast menu for the ocean liner that was later used as a floating prop for the film "The Last Voyage"? Give the items as a comma-separated list, ordering them in clockwise order based on their arrangement in the painting starting from the 12 o'clock position. Use the plural form of each fruit.
  
  You can see this question involves several challenges:
  
  Answering in a constrained format,
  Using multimodal capabilities (to extract the fruits from the image),
  Gathering several pieces of information, some depending on others:
  Identifying the fruits on the picture
  Finding which ocean liner was used as a floating prop for “The Last Voyage”
  Finding the October 1949 breakfast menu for the above ocean liner
  Chaining together a problem-solving trajectory in the correct order.

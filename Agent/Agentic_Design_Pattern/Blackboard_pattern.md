# Understanding the Blackboard Pattern
- https://medium.com/@dp2580/building-intelligent-multi-agent-systems-with-mcps-and-the-blackboard-pattern-to-build-systems-a454705d5672
  
The Blackboard Pattern consists of three key components:

- Blackboard: A shared knowledge repository where all information, hypotheses, and partial solutions are stored
- Knowledge Sources (Agents): Specialized problem-solvers that can read from and write to the blackboard
- Control Component: Orchestrates which agents should act when, based on the current state of the blackboard

  <img width="720" height="419" alt="image" src="https://github.com/user-attachments/assets/1d3ab45f-06ec-4d6d-831e-c18f3ce89246" />

# whiteducksoftware/flock

We’ve developed an agent framework that uses blackboard orchestration as its main orchestration pattern:

https://github.com/whiteducksoftware/flock

With it, the flow you designed would take about ten lines of code, and you wouldn’t need to rely on agents or models being “smart enough” to know when to write to the blackboard via tools. 
We’ve also introduced visibility groups, which let you define exactly what each agent can see on the blackboard... so, for example, you can hide sensitive data like patient information from agents that shouldn’t access it.

https://medium.com/@a.ratzenberger/complex-ai-agent-workflows-with-zero-prompts-7e2e971fd0f9

https://whiteducksoftware.github.io/flock/guides/blackboard/

# Scratchpads
When humans solve tasks, we take notes and remember things for future, related tasks. Agents are also gaining these capabilities! Note-taking via a “scratchpad” is one approach to persist information while an agent is performing a task. The idea is to save information outside of the context window so that it’s available to the agent. 

`source` https://www.anthropic.com/engineering/claude-think-tool?ref=blog.langchain.com

Scratchpads can be implemented in a few different ways. They can be [a tool call](https://www.anthropic.com/engineering/claude-think-tool?ref=blog.langchain.com) that simply writes [to a file](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem?ref=blog.langchain.com). They can also be a field in a runtime [state object](https://langchain-ai.github.io/langgraph/concepts/low_level/?ref=blog.langchain.com&ajs_aid=82740d3b-9d86-499b-8ab6-4380c144b290&_gl=1*pujsas*_gcl_au*MjA3MjA4MjkyMS4xNzYxMTM0MTc4*_ga*NDAyMDE1NDcwLjE3NjExMzQxNzg.*_ga_47WX3HKKY2*czE3NjExNDc0MjUkbzMkZzEkdDE3NjExNDk4NzQkajUkbDAkaDA.#state) that persists during the session. In either case, scratchpads let agents save useful information to help them accomplish a task.

`source` https://www.anthropic.com/engineering/claude-think-tool?ref=blog.langchain.com
## Using the think tool

Before taking any action or responding to the user after receiving tool results, use the think tool as a scratchpad to:
- List the specific rules that apply to the current request
- Check if all required information is collected
- Verify that the planned action complies with all policies
- Iterate over tool results for correctness 

Here are some examples of what to iterate over inside the think tool:
<think_tool_example_1>
User wants to cancel flight ABC123
- Need to verify: user ID, reservation ID, reason
- Check cancellation rules:
  * Is it within 24h of booking?
  * If not, check ticket class and insurance
- Verify no segments flown or are in the past
- Plan: collect missing info, verify rules, get confirmation
</think_tool_example_1>

<think_tool_example_2>
User wants to book 3 tickets to NYC with 2 checked bags each
- Need user ID to check:
  * Membership tier for baggage allowance
  * Which payments methods exist in profile
- Baggage calculation:
  * Economy class × 3 passengers
  * If regular member: 1 free bag each → 3 extra bags = $150
  * If silver member: 2 free bags each → 0 extra bags = $0
  * If gold member: 3 free bags each → 0 extra bags = $0
- Payment rules to verify:
  * Max 1 travel certificate, 1 credit card, 3 gift cards
  * All payment methods must be in profile
  * Travel certificate remainder goes to waste
- Plan:
1. Get user ID
2. Verify membership level for bag fees
3. Check which payment methods in profile and if their combination is allowed
4. Calculate total: ticket price + any bag fees
5. Get explicit confirmation for booking
</think_tool_example_2>

`source` https://blog.langchain.com/context-engineering-for-agents/

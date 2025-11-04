
# From AI:

### 🎯 1. UCB Bandits (Upper Confidence Bound)

This comes from the **multi-armed bandit problem** — imagine you’re at a casino with many slot machines.
Each machine gives random rewards, and you want to find the best one without wasting time.

The UCB strategy says:

> “Try each machine a bit, then keep choosing the one with the **best average reward + some uncertainty margin**.”

That “margin” (the **upper confidence bound**) makes you occasionally explore machines you’re less sure about — so you don’t get stuck on a “pretty good” one too early.

🧠 In prompt tuning:
Each **prompt candidate** is like a slot machine.
The “reward” is how well the model performs (say, accuracy or score).
UCB helps you test a few prompts and then focus on the most promising ones.

---

### 🔁 2. Successive Rejects

This is another bandit strategy, but simpler.
Instead of adding uncertainty bonuses, it works in **rounds**:

1. Test all prompts for a while.
2. Eliminate the **worst-performing** one.
3. Test the rest more deeply.
4. Repeat until one best prompt remains.

So it’s a **gradual elimination** method.

🧠 In prompt tuning:
You start with many edited prompts → evaluate → drop the weakest → keep refining the survivors.

---

### 🔍 Summary:

| Method                 | Core Idea                                            | How It Helps Prompt Search          |
| ---------------------- | ---------------------------------------------------- | ----------------------------------- |
| **UCB Bandits**        | Balances trying new options vs. exploiting good ones | Avoids missing better prompts       |
| **Successive Rejects** | Eliminates the worst options step by step            | Efficiently narrows down candidates |

---


Let’s break down **Successive Rejects** step by step and connect it to prompt tuning.

---

### 🧩 The idea:

Successive Rejects is another way to solve the **multi-armed bandit** problem — finding the best option (like the best prompt) by testing each one multiple times.

Instead of balancing exploration like UCB does, it uses a **tournament-style elimination**:

1. **Start with all candidates.**
   Say you have 5 prompt versions.
2. **Test each one** a few times and record their average rewards.
3. **Reject (eliminate) the worst one.**
4. **Repeat the process** with the remaining candidates.
5. Continue until only one “winner” remains — that’s your best prompt.

---

### 🎯 Why it’s called *Successive Rejects*:

Because in each round, you **successively reject** the least promising option.

It’s a bit like:

> “We’ll give everyone a fair chance early on, but we’ll gradually spend more time testing the stronger ones.”

---

### 💡 Example (prompt optimization version)

Imagine you’re testing 4 prompts:

| Round | Prompts Tested | Eliminate         | Remaining |
| ----- | -------------- | ----------------- | --------- |
| 1     | A, B, C, D     | D (worst)         | A, B, C   |
| 2     | A, B, C        | C (next worst)    | A, B      |
| 3     | A, B           | compare carefully | A wins    |

By testing and rejecting in stages, you **use your testing budget efficiently** — fewer tests wasted on poor candidates.

---

### ⚙️ In ProTeGi:

Successive Rejects helps the system:

* Focus on the most promising **prompt edits**.
* Drop weak prompts early.
* End up with the strongest-performing version using fewer evaluations.

---



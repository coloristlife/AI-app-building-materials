# from AI

---

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


Let’s build UCB bandits up step by step 👇

---

### 🎰 Imagine this:

You’re testing **3 slot machines** (or prompts).
Each time you try one, you get a *reward* (maybe a performance score).
At first, you don’t know which one is best — so you have to **explore**.
But after some tries, you want to **exploit** the one that looks best.

This is called the **exploration vs. exploitation tradeoff.**

---

### 📈 The Upper Confidence Bound (UCB)

UCB gives you a simple formula to balance the two:
`UCB value=average reward+uncertainty term`

* The **average reward** = how well this option has done so far.
* The **uncertainty term** = how little you’ve tried it (more uncertainty = bigger bonus).

So:

* A well-performing prompt → high average reward.
* A rarely tried prompt → large uncertainty bonus.

You always pick the prompt with the **highest UCB value**.
That way, you sometimes explore uncertain options — but mostly focus on those that perform well.

---

### 💡 Example

| Prompt | Average Score | Times Tested | UCB Value (approx)       | Decision       |
| ------ | ------------- | ------------ | ------------------------ | -------------- |
| A      | 0.8           | 10           | 0.8 + small bonus → 0.82 | maybe good     |
| B      | 0.7           | 2            | 0.7 + big bonus → 0.9    | try this again |
| C      | 0.6           | 20           | 0.6 + tiny bonus → 0.61  | skip it        |

So even though **A** looks best by average, **B** gets picked because it’s still uncertain — it *might* turn out better.

---




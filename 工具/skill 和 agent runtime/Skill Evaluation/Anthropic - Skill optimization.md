---
内容生成: AI
---


> **Anthropic 的 Skill Creator 目前并不是用 GEPA 来优化 Skill。**
> 
> 它采用的是一种 **LLM-driven iterative optimization loop（基于评测反馈的迭代式优化）**，而且其中有一些自动化组件，但和 GEPA 的“反思 + Pareto 搜索”不是同一种技术。

我刚看了 Anthropic 当前的 `skill-creator` 实现，具体可以拆成下面几层。([GitHub](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md?utm_source=chatgpt.com "skills/skills/skill-creator/SKILL.md at main · anthropics/skills · GitHub"))

## 1. Anthropic 的核心优化机制

它实际上是：

```text
Skill v1
   ↓
Generate / define evals
   ↓
Run Agent with Skill
   ↓
Run baseline
   ↓
Grade outputs
   ↓
Benchmark
   ↓
Analyze failures
   ↓
Human feedback
   ↓
LLM improves Skill
   ↓
Skill v2
   ↓
Repeat
```

也就是说，它的核心不是某个传统意义上的 optimizer，而是：

> **Evaluation-driven iterative refinement**

Anthropic 的 `skill-creator` 明确把自己的流程描述成：

**draft → test → evaluate → quantitatively benchmark → analyze → rewrite → repeat**。([GitHub](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md?plain=1&utm_source=chatgpt.com "skills/skills/skill-creator/SKILL.md at main · anthropics/skills · GitHub"))

---

# 2. 它里面其实有几个不同的“Agent”

这点非常重要。

Anthropic 的 Skill Creator 并不是一个简单的：

```text
Skill → Score
```

它实际上把任务拆成了几个角色。

### Executor

负责真正运行：

```text
Prompt + Skill
       ↓
Claude
       ↓
Output
```

然后还会跑 baseline：

```text
Prompt + No Skill
       ↓
Claude
       ↓
Output
```

所以它天然支持：

> **with_skill vs without_skill**

的比较。([GitHub](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md?plain=1&utm_source=chatgpt.com "skills/skills/skill-creator/SKILL.md at main · anthropics/skills · GitHub"))

---

### Grader

负责判断 output 是否满足 evaluation expectations。

例如：

```text
Expected:
The answer identifies 3 requirements.

Actual:
The answer identifies 2.

→ FAIL
```

它可以使用 assertions / grading 来产生 pass/fail 等结果。([GitHub](https://github.com/anthropics/skills/blob/main/skills/skill-creator/references/schemas.md?utm_source=chatgpt.com "skills/skills/skill-creator/references/schemas.md at main · anthropics/skills · GitHub"))

---

### Analyzer

这个角色不是简单计算平均分，而是进一步分析 benchmark：

例如：

```text
Eval #7:
always passes

Eval #12:
high variance

Eval #18:
fails without skill
passes with skill

Eval #23:
skill makes no difference
```

然后寻找：

> **Skill 到底在哪些场景真正产生了价值？**

Anthropic 的文档明确要求进行 analyst pass，用来发现 aggregate statistics 隐藏的 pattern，例如 non-discriminating assertions、high variance evals、time/token tradeoffs 等。([GitHub](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md?plain=1&utm_source=chatgpt.com "skills/skills/skill-creator/SKILL.md at main · anthropics/skills · GitHub"))

---

### Comparator

它还有一个可选的 blind comparison：

```text
Output A
Output B
```

不给 evaluator 看哪个是：

```text
v1
v2
```

让独立 Agent 判断：

> 哪个更好？

然后再分析为什么。

这可以避免 evaluator 因为知道版本号而产生偏差。([GitHub](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md?plain=1&utm_source=chatgpt.com "skills/skills/skill-creator/SKILL.md at main · anthropics/skills · GitHub"))

---

# 3. 所以它的“Optimizer”其实是谁？

这就是最容易误解的地方。

Anthropic 并没有像 GEPA 那样有一个独立的：

```text
Optimizer
```

核心组件。

而是：

```text
Evaluation
   ↓
Feedback
   ↓
Skill Creator Agent
   ↓
Rewrite SKILL.md
```

也就是说：

> **LLM 本身就是 optimizer。**

Anthropic 的 Skill Creator 会读取：

- 当前 Skill
    
- Evaluation results
    
- Grading results
    
- Benchmark
    
- Human feedback
    
- Failure patterns
    

然后重新修改 Skill。

官方文档甚至直接把这一阶段叫作：

> **“Improving the skill”**

并明确要求根据用户 feedback 和 quantitative benchmark 中暴露的问题重新编写 Skill，然后重复 evaluation。([GitHub](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md?plain=1&utm_source=chatgpt.com "skills/skills/skill-creator/SKILL.md at main · anthropics/skills · GitHub"))

---

# 4. 还有一个比较特殊的自动优化：Description Optimization

这个和 Skill 本体优化要分开。

Anthropic 对：

```yaml
description: ...
```

有一个专门的 optimization loop。

它会：

```text
Generate trigger queries
        ↓
should trigger / should not trigger
        ↓
Train/Test split
        ↓
Evaluate trigger accuracy
        ↓
Claude proposes new description
        ↓
Evaluate again
        ↓
Repeat
```

当前实现最多可以迭代 5 次，并且用 **held-out test set** 来选择最佳 description，从而降低 overfitting。([GitHub](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md?plain=1&utm_source=chatgpt.com "skills/skills/skill-creator/SKILL.md at main · anthropics/skills · GitHub"))

这个部分其实已经非常接近一个真正的自动 optimizer。

---

# 5. Anthropic 和 GEPA 的关键区别

现在就可以非常清楚地比较：


|                                   | Anthropic Skill Creator |                 GEPA                 |
| :-------------------------------: | :---------------------: | :----------------------------------: |
|               核心思想                |  Iterative refinement   | Reflective evolutionary optimization |
|            Evaluation             |            ✅            |            依赖外部 evaluator            |
|         Failure analysis          |            ✅            |                  ✅                   |
|          LLM reflection           |            有            |                 核心机制                 |
|            自动修改 Skill             |            ✅            |                  ✅                   |
|       Candidate population        |           较简单           |                 核心机制                 |
|        Pareto optimization        |            ❌            |                  ✅                   |
|      Train/Test optimization      | Description optimizer 有 |         支持更一般的 optimization          |
|          Human feedback           |         核心组成部分          |             可作为 feedback             |
|         Blind comparison          |            ✅            |          可以通过 evaluator 实现           |
|             Skill 专用              |            是            |                  否                   |
| 通用 prompt/code/agent optimization |           较弱            |                  强                   |



所以：

> **Anthropic 是“评测 → 分析 → LLM 改 Skill → 再评测”。**

而：

> **GEPA 是“评测 → reflective feedback → 产生多个候选 → Pareto-aware selection → 再评测”。**

---

# 6. 这对我们之前的架构讨论其实很重要

现在可以把三者的位置真正分清楚：

```text
                 Evaluation
                     │
                     ↓
              Failure / Feedback
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
 Anthropic Skill Creator       GEPA
          │                     │
   LLM iterative rewrite   Evolutionary optimization
          │                     │
          ↓                     ↓
       Skill v2             Candidates
                                  │
                                  ↓
                            Pareto Selection
```

因此，如果你问：

> **“Anthropic 有没有类似 GEPA 的技术？”**

准确回答是：

**没有一个等价的 GEPA optimizer。**

但它确实有自己的 **LLM-based iterative optimization mechanism**，而且已经做得相当完整。

---

# 7. 对你这个 Goose + Knowledge Base 场景意味着什么？

这反而让我们的架构选择更加清晰。

你完全可以把 Anthropic 的优化思想拿过来，而不需要拿它的整个 Skill Creator。

例如：

```text
Goose
  ↓
Skill
  ↓
Knowledge Base
  ↓
Answer
  ↓
Evaluator
  ↓
Feedback
  ↓
LLM Optimizer
  ↓
Skill v2
```

第一阶段甚至不需要 GEPA。

你可以先实现 Anthropic 风格：

> **Evaluate → Analyze → LLM Rewrite → Re-evaluate**

等以后发现：

```text
v2
v3
v4
v5
```

候选越来越多，需要系统性搜索和 Pareto selection，再换成：

> **GEPA**

---

# 8. 所以我现在反而建议你不要把“GEPA”当成第一步

这是对我们之前方案又一个重要的精确化。

你的 V1 最合理的是：

```text
AgentSkills
      ↓
Goose
      ↓
Knowledge Base
      ↓
Evaluation
      ↓
LLM-based Improvement
      ↓
Skill v2
      ↓
Evaluation
```

这个实际上就是**简化版 Anthropic Skill Creator optimization loop**。

等你以后需要：

```text
多个 Skill candidate
多个 evaluation dimensions
自动搜索
Pareto optimization
更复杂的 optimization budget
```

再：

```text
Evaluation
    ↓
GEPA
    ↓
Skill candidates
    ↓
Pareto selection
```

---

## 最终可以把它理解成三个层次

**Anthropic Skill Creator：**

> “发现问题，然后让 LLM 帮你改 Skill。”

**GEPA：**

> “发现问题，然后系统化地探索多个修改方案，并根据反馈进行优化。”

**Harbor / Inspect AI：**

> “把 Agent 跑起来，并可靠地进行 Evaluation。”

所以它们其实不是互相替代的：

```text
                  ┌─────────────────┐
                  │     Goose       │
                  │  Agent Runtime  │
                  └────────┬────────┘
                           ↓
                  ┌─────────────────┐
                  │ Evaluation      │
                  │ Inspect/Harbor  │
                  └────────┬────────┘
                           ↓
                       Feedback
                           │
                ┌──────────┴──────────┐
                ↓                     ↓
       Anthropic-style           GEPA
       LLM Refinement       Evolutionary Optimization
                │                     │
                └──────────┬──────────┘
                           ↓
                      Better Skill
```

**这才是我们前面整个讨论最后应该收敛到的技术模型。**

而且 Anthropic 当前公开的 Skill Creator 确实已经包含 `generate_evals`、`grader`、`comparator`、`analyzer`、benchmark，以及 description optimization 等组件，所以它比简单的“人工改 Skill”要自动化得多。([GitHub](https://github.com/anthropics/skills/pull/607/files?utm_source=chatgpt.com "feat(skill-creator): add generate_evals script and improve SKILL.md UX by tercel · Pull Request #607 · anthropics/skills · GitHub"))

不过也要注意，当前 GitHub 版本的 Skill Creator 在实际使用上仍有一些已公开的问题，例如 benchmark layout、delta 计算等 issue，因此如果你要把它直接作为 Goose 的生产级优化框架，仍然需要做 runtime/evaluation 解耦，而不是直接照搬。([GitHub](https://github.com/anthropics/skills/issues/1383?utm_source=chatgpt.com "skill-creator: silent benchmark failures (layout mismatch, inverted delta), broken trigger evals on Windows, and skill shadowing in trigger evals · Issue #1383 · anthropics/skills · GitHub"))
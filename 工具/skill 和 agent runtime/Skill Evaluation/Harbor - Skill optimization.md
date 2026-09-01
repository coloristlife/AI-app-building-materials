---
内容生成: AI
---
https://github.com/harbor-framework/harbor

**Harbor 可以用于优化 Agent 使用的 Skill，但要非常准确地说：Harbor 本身不是一个专门的 Skill Optimizer。**它提供的是 Agent evaluation/execution 基础设施，然后可以接入 **GEPA、RL/Tinker 等优化框架**。Harbor 官方现在把自己定位为 “evaluating and optimizing agents and models”，并明确提供 GEPA、SkyRL、Tinker 等优化集成。([Harbor](https://www.harborframework.com/docs?utm_source=chatgpt.com "Motivation"))

而你问的“Harbor 用什么技术优化 Skill”，目前最值得关注的是：

> **Harbor + GEPA。**

### 1. Harbor 自己负责什么？

Harbor 负责把一个 Agent 放进一个可重复的 evaluation environment：

```text
Task
  ↓
Environment
  ↓
Agent
  ↓
Execution
  ↓
Verifier / Reward
  ↓
Evaluation Result
```

它可以把 custom skills 加入 task，也支持自定义 Agent。官方 Cookbook 现在已经有一个专门的 `skills` recipe。([GitHub](https://github.com/harbor-framework/harbor-cookbook?utm_source=chatgpt.com "GitHub - harbor-framework/harbor-cookbook: Realistic examples of building evals and optimizing agents with Harbor · GitHub"))

所以如果你的 Skill 是：

```text
SKILL.md
   ↓
Goose
   ↓
Knowledge Base
   ↓
Answer
```

Harbor 可以负责把这个过程稳定地跑很多次，并得到 evaluation/reward。

---

## 2. 真正负责“优化”的是 GEPA

Harbor Cookbook 目前有一个明确的：

> **`gepa` — Agent harness optimization for MedAgentBench using Harbor + GEPA**

也就是说实际结构是：

```text
                 Harbor
                   │
             Run Agent Task
                   │
                   ↓
               Evaluation
                   │
                   ↓
                Feedback
                   │
                   ↓
                  GEPA
                   │
              modify text
                   │
                   ↓
             New Candidate
                   │
                   ↓
                Harbor
                   │
                   ↓
              Re-evaluate
```

Harbor 官方 Cookbook 明确把这个作为 optimization example。([GitHub](https://github.com/harbor-framework/harbor-cookbook?utm_source=chatgpt.com "GitHub - harbor-framework/harbor-cookbook: Realistic examples of building evals and optimizing agents with Harbor · GitHub"))

---

# 3. GEPA 到底怎么修改 Skill？

这里非常关键。

GEPA 并不是：

> “Harbor 有一个 Skill optimizer，专门理解 SKILL.md。”

而是：

> **GEPA 可以把 Skill 当成一个需要优化的 text artifact。**

GEPA 的 API 把优化对象抽象成 **text components**，可以是 prompt、code、agent architecture、configuration，当然也可以是 Skill instructions。它通过 execution trace + evaluation feedback 做 LLM reflection，然后产生 mutation，再进行 Pareto-aware selection。([GitHub](https://github.com/gepa-ai/gepa/blob/main/README.md?utm_source=chatgpt.com "gepa/README.md at main · gepa-ai/gepa · GitHub"))

例如：

```text
SKILL.md v1

"Retrieve the relevant security requirements
from the knowledge base."
```

Harbor 执行：

```text
Question
   ↓
Goose
   ↓
Skill v1
   ↓
Knowledge Base
   ↓
Answer
```

Evaluator 得到：

```text
Retrieval Completeness = 67%
```

同时保存 execution trace：

```text
Agent found Requirement A
Agent found Requirement B
Agent stopped
Expected:
A, B, C, D
```

GEPA 看到这些信息后进行 reflection：

```text
Why did this candidate fail?

→ The agent terminated retrieval too early.
```

然后产生新的 Skill candidate：

```text
SKILL.md v2

After retrieving relevant requirements,
perform a completeness check and determine
whether additional related requirements
should be retrieved.
```

再交回 Harbor：

```text
Harbor
   ↓
Goose + Skill v2
   ↓
Evaluation
   ↓
91%
```

如果 v2 更好，就继续探索。

---

# 4. 这和 Anthropic Skill Creator 的区别就很清楚了

现在可以把我们前面讨论的东西真正区分开：

### Anthropic

```text
Evaluation
    ↓
LLM analyzes failures
    ↓
LLM rewrites Skill
    ↓
Re-evaluate
```

属于：

> **LLM-driven iterative refinement**

### Harbor + GEPA

```text
Harbor
  ↓
Evaluation / Trace
  ↓
GEPA Reflection
  ↓
Mutation
  ↓
Multiple Candidates
  ↓
Pareto Selection
  ↓
Harbor
  ↓
Re-evaluation
```

属于：

> **Evaluation-driven evolutionary optimization**

GEPA 官方定义就是通过 **LLM-based reflection + Pareto-efficient evolutionary search** 优化文本参数。([GitHub](https://github.com/gepa-ai/gepa/blob/main/README.md?utm_source=chatgpt.com "gepa/README.md at main · gepa-ai/gepa · GitHub"))

---

# 5. 而且 GEPA 已经明确可以优化“Skills”

这个对你的问题非常重要。

GEPA 当前的 use cases 已经包括 **agent skill optimization**。官方文档列出了使用 GEPA 做 evolutionary self-improvement 的 Agent，以及直接优化 skill instructions 的案例。([GitHub](https://github.com/gepa-ai/gepa/blob/main/docs/docs/guides/use-cases.md?utm_source=chatgpt.com "gepa/docs/docs/guides/use-cases.md at main · gepa-ai/gepa · GitHub"))

所以这里不是理论上的：

> “Skill 也许可以用 GEPA。”

而是：

> **Skill 已经是 GEPA 实际支持的 optimization target。**

GEPA 自己的 README 也报告了一个 coding-agent 场景中，通过自动学习 skills 将 resolve rate 从 55% 提升到 82%。([GitHub](https://github.com/gepa-ai/gepa/blob/main/README.md?utm_source=chatgpt.com "gepa/README.md at main · gepa-ai/gepa · GitHub"))

---

# 6. 但有一个非常重要的区别：优化 Skill ≠ 优化 Agent

这是你做架构时一定要注意的。

假设：

```text
              Goose Agent
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
    System       Skill       Tools
    Prompt       SKILL.md      MCP
       │           │           │
       └───────────┼───────────┘
                   ↓
               Knowledge
                   ↓
                 Answer
```

GEPA 理论上可以优化多个 text components：

```text
System Prompt
SKILL.md
Tool descriptions
Agent policies
Code
Configuration
```

GEPA 的 `Candidate` 本身就是一组命名的 text components。([GitHub](https://github.com/gepa-ai/gepa/blob/main/src/gepa/api.py?utm_source=chatgpt.com "gepa/src/gepa/api.py at main · gepa-ai/gepa · GitHub"))

所以如果你告诉 GEPA：

```text
component = security_skill
```

那么它可以优化：

```text
SKILL.md
```

但如果你让它优化整个 Agent harness，它可能同时优化：

```text
system prompt
+
skill
+
agent instructions
```

这时候你得到的是：

> **Agent Optimization**

而不再是单纯的：

> **Skill Optimization**

---

# 7. 对你现在的 Knowledge-based use case，这反而是一个好消息

你可以把 optimization boundary 明确锁定：

```text
                    Goose
                      │
             ┌────────┴────────┐
             ↓                 ↓
        Fixed Runtime       Optimizable
                              │
                              ↓
                          SKILL.md
                              │
                              ↓
                         Knowledge Base
```

也就是说：

**Goose 不变。**

**Model 不变。**

**Knowledge Base 不变。**

只允许 GEPA 修改：

```text
SKILL.md
```

这样你得到的 improvement 才能真正归因于 Skill。

这就是为什么我之前一直强调：

> **Baseline / A-B comparison 非常重要。**

---

# 8. 所以你最终可以做成这个闭环

我认为这其实已经非常接近你真正应该实现的架构：

```text
                 AgentSkills
                      │
                   SKILL.md
                      │
                      ▼
                    Goose
                      │
                      ▼
                Knowledge Base
                      │
                      ▼
                    Answer
                      │
                      ▼
                   Harbor
                      │
                      ▼
                 Evaluation
                      │
              ┌───────┴────────┐
              ↓                ↓
          Score            Trace
              │                │
              └───────┬────────┘
                      ↓
                    GEPA
                      │
             Reflection / Mutation
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
       Skill v2     Skill v3    Skill v4
          │           │           │
          └───────────┼───────────┘
                      ↓
                 Pareto Select
                      │
                      ↓
                 Best Skill
                      │
                      ↓
                Human Approval
                      │
                      ↓
               Production Skill
```

这里：

**AgentSkills** = Skill 格式标准  
**Goose** = Runtime  
**Harbor** = Evaluation / Execution Environment  
**Evaluator** = 判断 Knowledge Skill 好不好  
**GEPA** = 根据 feedback 自动优化 Skill

---

# 9. 所以现在我对你这个项目的最终建议其实更加明确了

如果你问我：

> **“Harbor 能不能优化 Skill？”**

答案：

**能。**

但准确说法是：

> **Harbor 提供 Agent evaluation/execution environment；GEPA 是其中一个用于优化 Agent/Skill text components 的 optimization engine。**

Harbor 官方现在已经把 GEPA 列为优化集成，而且 Cookbook 有现成的 Harbor + GEPA recipe。([Harbor](https://www.harborframework.com/news/harbor-cookbook?utm_source=chatgpt.com "Explore the Harbor cookbook"))

如果你问：

> **“那是不是 Harbor 本身就等于 Anthropic Skill Creator？”**

**不是。**

Harbor 不负责：

> “理解你的 SKILL.md，然后自己设计一个更好的 Skill。”

它提供的是：

> **让 Agent + Skill + Environment 可以被可靠地运行、评测和产生 feedback。**

GEPA 才负责：

> **根据这些 feedback 去搜索更好的 Skill candidate。**

---

## 对你而言最重要的一点

其实我们现在已经可以把你之前纠结的几个工具彻底定位：

```text
                 Skill Creation
                       │
             Anthropic Skill Creator
                       │
                       ↓
                 AgentSkills
                       │
                       ↓
                    Goose
                       │
                       ↓
                    Harbor
                       │
                  Evaluation
                       │
                       ↓
                     GEPA
                       │
                Skill Optimization
                       │
                       ↓
                 Better Skill
```

**但这不意味着你现在必须全部装上。**

你的第一版甚至可以：

```text
Goose
 +
Skill
 +
Knowledge Base
 +
简单 Evaluator
 +
GEPA
```

先把 **“Skill 能不能自动变好”** 这个核心 loop 跑通。

然后再把 Harbor 加进来，解决规模化、sandbox、parallel trials、复杂 Agent environment 等问题。

Harbor 本身目前也明确支持多 reward/verifier、skills、multi-step、MCP 等任务模式，所以它确实非常适合成为你后面扩展的 evaluation substrate。([GitHub](https://github.com/harbor-framework/harbor-cookbook?utm_source=chatgpt.com "GitHub - harbor-framework/harbor-cookbook: Realistic examples of building evals and optimizing agents with Harbor · GitHub"))

**因此，如果你的最终目标是“自动优化 Goose 使用的 Knowledge Skill”，我现在会把核心技术组合锁定为：**

> **AgentSkills + Goose + Harbor + GEPA**

而不是：

> Anthropic Skill Creator + Goose。

Anthropic 可以作为 Skill authoring 的参考，但**Harbor + GEPA 才更接近你真正想构建的“Evaluation → Feedback → Skill Optimization”平台。**
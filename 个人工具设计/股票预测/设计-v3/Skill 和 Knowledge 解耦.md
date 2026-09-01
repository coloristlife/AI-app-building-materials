**这是这个架构里一个非常关键的设计原则。**

如果每增加一个新的个人经验，就要去修改 `Skill`，那说明 **Skill 和 Knowledge 没有真正解耦**。

正确方式是：

```text
新增个人经验
      ↓
Knowledge Compiler
      ↓
Knowledge Proposal
      ↓
Human Approval
      ↓
新增 Knowledge Object
      ↓
Knowledge Library
      ↓
Knowledge Resolver 自动能够找到它
      ↓
原来的 Skill 不变
```

---

## 1. 举一个具体例子

假设现在已经有：

```text
skills/
└── investment-decision/
    └── SKILL.md
```

里面规定：

```text
你需要：

1. 理解用户问题
2. 获取 Context
3. Retrieve Relevant Knowledge
4. Gather Evidence
5. Analyze
6. Challenge
7. Decide
```

注意它只说：

> **Retrieve Relevant Knowledge**

它没有说：

> 使用 R001 买阴卖阳。

也没有说：

> 使用 R003 放量下跌。

所以现在新增：

```text
R011 突破回踩确认
```

之后：

```text
skills/investment-decision/SKILL.md
```

**一个字都不用改。**

---

# 2. 那 AI 怎么知道 R011 存在？

通过：

```text
Knowledge Resolver
```

例如原来：

```text
knowledge/rules/

R001_buy_dip.yaml
R002_ma250.yaml
R003_volume.yaml
```

现在增加：

```text
R011_breakout_retest.yaml
```

Resolver 的工作是：

```text
User Question
      +
Market Context
      +
Evidence
       ↓
Knowledge Resolver
       ↓
查询 Knowledge Library
       ↓
R001
R003
R011
...
```

所以：

> **Skill 不负责知道有哪些 Knowledge。**

Skill 只负责告诉 Agent：

> “这个阶段需要 Retrieve Knowledge。”

---

# 3. 所以 Skill 和 Knowledge 的关系应该是动态的

不是：

```text
Skill
 ├── R001
 ├── R002
 └── R003
```

而是：

```text
Skill
 │
 │ "Retrieve relevant knowledge"
 ↓
Knowledge Resolver
 │
 ↓
Knowledge Library
 │
 ├── R001
 ├── R002
 ├── R003
 ├── R011  ← 新增加
 └── R012  ← 以后继续增加
```

因此 Knowledge Library 是一个**动态数据集合**。

Skill 是一个**稳定的处理程序/行为规范**。

---

# 4. 那什么时候才需要修改 Skill？

只有一种情况：

> **新增经验改变了“AI 应该怎么工作”，而不是“AI 应该相信什么”。**

这是非常重要的区别。

### 情况 A：新增投资知识

比如：

> “突破平台后第一次回踩不破，是比较好的买点。”

这是：

```text
WHAT I BELIEVE
```

所以增加：

```text
R011_breakout_retest.yaml
```

**不修改 Skill。**

---

### 情况 B：新增了一个处理方法

比如你后来发现：

> “每次分析股票之前，必须先判断市场处于牛市、熊市还是震荡市，然后才能调用我的个人 Rule。”

这个就不是 Knowledge。

这是：

```text
HOW THE AGENT SHOULD REASON
```

所以可能修改：

```text
skills/investment-decision/SKILL.md
```

增加：

```text
Before retrieving detailed trading rules,
the agent MUST determine the current market regime.
```

---

# 5. 再举一个更容易理解的例子

假设你新增经验：

> “如果连续两笔止损，就暂停交易。”

这应该是：

```yaml
id: C003
type: constraint

name: consecutive_loss_pause

statement: >
  连续两笔止损后暂停交易，避免情绪化交易。

conditions:
  consecutive_losses: >= 2

action:
  trading_status: pause

priority: 95
```

Skill 不变。

但是如果你告诉系统：

> “以后所有交易决策，无论任何情况下，都必须先检查我的风险 Constraints。”

这才应该进入 Skill：

```text
Before generating a Decision:

1. Retrieve relevant Principles.
2. Retrieve relevant Constraints.
3. Evaluate Constraints.
4. Only then evaluate trading Rules.
```

这里修改的是**推理流程**。

---

# 6. 所以我们最好给 Knowledge 增加一个 `type`

你现在已经有：

```text
Principle
Rule
Constraint
Heuristic
Pattern
Experience
Observation
```

我建议再加一个非常重要的概念：

```text
Knowledge
    │
    ├── Domain Knowledge
    │     ├── Principle
    │     ├── Rule
    │     ├── Heuristic
    │     ├── Pattern
    │     └── Experience
    │
    └── Decision Constraint
          └── Constraint
```

但不要把：

```text
HOW TO REASON
```

放进去。

因为那属于 Skill / Workflow。

---

# 7. 最终应该形成三个非常清楚的层次

这是我认为你整个系统最核心的抽象：

### 第一层：Workflow

```text
什么时候做什么
```

例如：

```text
Understand
→ Retrieve
→ Evidence
→ Analyze
→ Challenge
→ Decide
```

---

### 第二层：Skill

```text
每一步应该怎么做
```

例如：

> Retrieve Knowledge 时，要考虑当前市场环境、标的、时间周期和历史案例。

---

### 第三层：Knowledge

```text
在这个过程中应该依据什么经验
```

例如：

```text
R001 买阴卖阳
R002 年线趋势
R003 放量下跌
R011 突破回踩
```

所以：

```text
Workflow = WHEN
Skill     = HOW
Knowledge = WHAT
Tool      = FACT
History   = WHAT HAPPENED
```

这个五层关系非常重要。

---

# 8. 这也意味着你的 Skill 应该写成“开放式”的

例如不要这样写：

```markdown
## Rules

Use:

- R001
- R002
- R003
- R004
```

这是错误的。

应该写：

```markdown
## Knowledge Retrieval

Retrieve the Knowledge Objects relevant to the current task.

The Knowledge Library is dynamic.

Do not assume a fixed list of Knowledge Objects.

The resolver must consider:

- task
- asset
- timeframe
- market regime
- sector regime
- portfolio state
- available evidence

The agent must use the returned Knowledge Objects
rather than relying on a hard-coded rule list.
```

这样以后：

```text
R001
R002
R003
...
R1000
```

都可以自动工作。

---

# 9. 甚至 Knowledge Resolver 本身也不应该修改

同样道理。

你增加：

```text
R011
```

不应该修改：

```text
KnowledgeResolver
```

它应该是：

```text
Generic Resolver
```

只负责：

```text
Input
 ↓
Search
 ↓
Rank
 ↓
Filter
 ↓
Return
```

而不是：

```text
if user mentions "breakout":
    use R011
```

否则又开始硬编码了。

---

# 10. 那新 Knowledge 怎么“进入系统”？

完整流程应该是：

```text
                 NEW EXPERIENCE
                       │
                       ↓
              Knowledge Compiler
                       │
                       ↓
             Knowledge Proposal
                       │
                       ↓
             Knowledge Reviewer
                       │
                       ↓
               Human Approval
                       │
                       ↓
              Knowledge Library
                       │
                       ↓
             Knowledge Index
                       │
                       ↓
             Knowledge Resolver
                       │
                       ↓
                Existing Skill
                       │
                       ↓
                 Agent Decision
```

注意：

**中间没有“修改 Skill”这个步骤。**

---

# 11. 什么时候需要重新生成 Skill？

只有当你的**个人投资方法论本身发生结构性变化**。

比如原来：

```text
Analyze
 ↓
Decide
```

后来你认为：

```text
Analyze
 ↓
Challenge
 ↓
Scenario Analysis
 ↓
Risk Simulation
 ↓
Decide
```

那么这是 Workflow/Skill 的变化。

这时候才需要：

```text
Skill Version 1
        ↓
Skill Version 2
```

而不是因为增加了一个 Rule 就修改 Skill。

---

# 12. 所以我会进一步修改之前的架构

之前我们有：

```text
skills/
knowledge/
```

现在应该明确规定：

```text
skills/
│
├── workflow/
│
├── knowledge-ingestion/
│
├── knowledge-review/
│
├── knowledge-retrieval/
│
├── analysis/
│
├── challenge/
│
├── decision/
│
├── monitoring/
│
└── learning/
```

而：

```text
knowledge/
│
├── principles/
├── rules/
├── constraints/
├── heuristics/
├── patterns/
├── experiences/
└── observations/
```

两边**完全独立版本管理**。

---

## 最重要的一句话

你以后给系统增加：

> **“我的新投资经验是什么？”**

修改的是：

```text
knowledge/
```

你以后告诉系统：

> **“我希望 AI 以后用什么新的方式分析这些经验？”**

才修改：

```text
skills/
```

你以后告诉系统：

> **“我希望 AI 分析流程增加一个新阶段。”**

才修改：

```text
workflow/
```

你以后告诉系统：

> **“我需要一个新的数据来源/计算能力。”**

才增加：

```text
tools/
```

所以整个系统就可以真正做到你之前一直要求的：

> **增加个人经验，不需要推翻整个 Agent；增加经验不需要修改 Skill；增加 Skill 不需要修改 Knowledge；增加 Tool 也不需要修改个人经验。**

这才是真正意义上的 **Generic、可扩展的 Personal Investment Agent**。
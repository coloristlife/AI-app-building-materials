

如果你前面说的那个 **投资分析 Skill** 是你的主流程，那么我建议不要按照“个人经验来自哪里”去分类 Skill，而是按照：

> **Agent 在处理投资问题时，需要执行什么能力 / workflow**

来分类。

你的 personal experience、行业 workflow、best practice 都是**Skill 的来源材料**，不是 Skill 的分类维度。

---

## 1. 先确定 Skill 的 3 个来源

你的 Skill 可以来自三种来源：

```text
                    Skill Sources
                         │
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
Personal Experience   Industry Workflow   Best Practice
        │                │                │
        └────────────────┼────────────────┘
                         ↓
                  Skill Extraction
                         ↓
                   Skill Library
```

例如：

### Personal Experience

你说：

> 我每次看到股票突然大涨，都会先判断是不是已经过度上涨。

这本身是 **Knowledge**。

但如果你说：

> 我分析股票的时候，习惯先判断价格是不是已经脱离正常波动，然后才继续分析。

这里就可能提取出一个：

```text
Price Deviation Assessment
```

这是 Skill。

---

### Industry Workflow

比如行业常见流程：

```text
Market Regime
→ Sector
→ Company
→ Valuation
→ Technical
→ Risk
→ Decision
```

这些可以成为 Skill / Workflow。

---

### Industry Best Practice

例如：

> Investment decisions should consider downside risk before expected return.

这可能形成：

```text
Risk Assessment Skill
```

---

## 2. 你的主 Skill 不应该拆成很多独立 Skill

这是我特别建议你注意的。

假设你的主流程是：

```text
1. Understand the Question
2. Define Investment Context
3. Retrieve Relevant Knowledge
4. Gather External Evidence
5. Analyze Market / Asset
6. Apply Personal Rules
7. Challenge the Thesis
8. Assess Risk
9. Make Decision
10. Record / Learn
```

不要变成：

```text
Skill 01
Skill 02
Skill 03
...
Skill 10
```

然后每个 Skill 又里面塞几十条东西。

更好的方式是：

```text
investment-analysis/
│
├── SKILL.md              ← 主 orchestrating skill
│
├── workflows/
│   ├── context.md
│   ├── research.md
│   ├── analysis.md
│   ├── challenge.md
│   ├── decision.md
│   └── learning.md
│
└── references/
```

主 Skill 负责：

> **什么时候调用哪个能力。**

---

## 3. 我建议你把 Skill 分成 6 个能力域

而不是 10 个。

你的 10 步是 workflow。

Skill 是 capability。

可以这样归类：

```text
Investment Agent Skill Library

├── 1. Context Understanding
│
├── 2. Knowledge Retrieval & Application
│
├── 3. Research & Evidence
│
├── 4. Investment Analysis
│
├── 5. Decision Challenge & Risk
│
└── 6. Decision & Learning
```

这样会干净很多。

---

## 4. 第一类：Context Understanding

负责：

> **我现在到底在分析什么？**

包括：

```text
User Intent Analysis
Investment Objective
Asset Identification
Time Horizon
Risk Preference
Portfolio Context
Market Context
```

例如用户说：

> “现在 NVDA 还能不能买？”

Skill 首先不能直接回答。

它需要识别：

```text
Asset = NVDA
Question = Buy / No Buy
Time Horizon = unknown
Investment Objective = unknown
Portfolio Context = unknown
```

所以它可能需要进一步询问或者推断上下文。

---

## 5. 第二类：Knowledge Retrieval & Application

这是你个人经验真正进入 Agent 的地方。

Skill 不存你的规则。

它只负责：

```text
Determine what knowledge is needed
        ↓
Query Knowledge Resolver
        ↓
Retrieve relevant Knowledge Objects
        ↓
Evaluate applicability
        ↓
Apply them to current context
```

例如：

```text
当前：
NVDA
短期大涨
高波动
用户问是否追涨

        ↓

Resolver

        ↓

K-003 过度上涨 heuristic
K-011 突破回踩 pattern
K-024 追涨 constraint
```

然后 Skill 决定：

> 哪些 Knowledge 应该被应用。

**Knowledge 自己不负责调用自己。**

---

## 6. 第三类：Research & Evidence

这是行业 workflow / best practice 很容易进入的地方。

包括：

```text
Market Research
Company Research
Financial Data Analysis
News Analysis
Earnings Analysis
Competitive Analysis
Macro Analysis
Source Evaluation
Evidence Verification
```

比如你的个人经验说：

> “我发现某类公司业绩很好但是股价还是跌。”

这属于 Knowledge。

但：

> “分析公司时必须检查 earnings、guidance、valuation 和 market expectation。”

这是 Research Skill。

---

## 7. 第四类：Investment Analysis

这是核心分析能力。

可以包括：

```text
Fundamental Analysis
Technical Analysis
Valuation Analysis
Market Regime Analysis
Sector Analysis
Growth Analysis
Quality Analysis
Momentum Analysis
Catalyst Analysis
```

这里特别适合吸收：

**Industry practice + 你的个人经验形成的方法。**

比如行业 workflow：

```text
Company
→ Revenue
→ Margin
→ Growth
→ Cash Flow
→ Valuation
```

这是 Skill。

而你的：

> “当 PE 很高的时候，我会要求更高的增长率作为补偿。”

这是 Knowledge。

两者结合：

```text
Valuation Skill
       ↓
Retrieve user's valuation heuristics
       ↓
Apply them
```

---

## 8. 第五类：Decision Challenge & Risk

这个我建议独立出来。

因为这是一个非常重要的 Agent 能力：

> **不要只是帮用户证明自己是对的。**

包括：

```text
Thesis Challenge
Counterargument Generation
Bear Case
Bull Case
Scenario Analysis
Risk Assessment
Downside Analysis
Invalidation Conditions
Bias Detection
```

例如：

用户说：

> “我觉得这只股票肯定会涨。”

Agent 不应该马上寻找支持证据。

Skill 应该要求：

```text
What would make this thesis wrong?
What evidence contradicts it?
What is the downside?
What assumptions are fragile?
```

然后再去 Knowledge Library 找相关：

```text
constraint
risk indicator
heuristic
pattern
```

---

## 9. 第六类：Decision & Learning

最后是：

```text
Decision Synthesis
Action Recommendation
Confidence Assessment
Position Sizing
Entry / Exit Planning
Monitoring
Outcome Recording
Post-Investment Review
Knowledge Update
```

这里就是你的：

```text
Experience
→ Outcome
→ Reflection
→ New Knowledge Proposal
```

形成闭环。

所以整个 Agent 变成：

```text
                 ┌───────────────┐
                 │   Context     │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │   Research    │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │    Analysis   │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │   Challenge   │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │    Decision   │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │    Learning   │
                 └───────┬───────┘
                         │
                         └──────────→ Knowledge
```

---

## 10. 那你的 Personal Experience 到底怎么参与 Skill？

这里是最容易混淆的地方。

你的个人经验输入以后，AI 要做一个判断：

```text
Personal Experience
        │
        ├── WHAT I KNOW
        │       ↓
        │   Knowledge
        │
        └── HOW I DO IT
                ↓
              Skill
```

比如你说：

> “我看一只股票的时候，绝不会只看股票本身。我会先看整个市场，再看行业，最后才看公司。”

这里实际上有两层：

### Knowledge

```text
Market context influences individual stocks.
```

### Skill

```text
Market
→ Sector
→ Company
```

所以 AI 不能简单地说：

> “这都是 Knowledge。”

也不能说：

> “这都是 Skill。”

它要进行**Experience Decomposition**。

---

## 11. 因此你需要第二个 Prompt：Skill Extractor

你前面那个 Prompt 是：

> Personal Experience → Knowledge Object

现在你还需要一个：

> **Personal Experience + Industry Workflow → Skill Proposal**

核心规则应该是：

````
# Skill Extraction Prompt

## Role

You are a Skill Architect for a personal investment AI agent.

Your task is to identify reusable agent behaviors, workflows, procedures, and reasoning methods from:

1. the user's personal investment experience
    
2. established investment workflows
    
3. industry practices
    
4. professional analytical methods
    

Do NOT convert domain facts or investment beliefs into Skills.

Skills describe HOW the agent should perform a task.

Knowledge describes WHAT the agent knows.

---

## Core Distinction

Classify each extracted item using:

### Knowledge

Use Knowledge when the statement describes:

- what is true
    
- what the user believes
    
- an observed pattern
    
- a rule of thumb
    
- a signal
    
- a constraint
    
- a hypothesis
    
- a personal investment principle
    

### Skill

Use Skill when the statement describes:

- how to perform a task
    
- how to analyze something
    
- how to retrieve information
    
- how to evaluate evidence
    
- how to compare alternatives
    
- how to challenge a thesis
    
- how to make a decision
    
- how to monitor an investment
    
- how to learn from outcomes
    

---

## Skill Categories

Classify extracted Skills into one of these capability domains:

1. Context Understanding
    
2. Knowledge Retrieval & Application
    
3. Research & Evidence
    
4. Investment Analysis
    
5. Decision Challenge & Risk
    
6. Decision & Learning
    

Do not create unnecessary categories.

---

## Extraction Process

For each input experience or workflow:

### Step 1

Identify the actual activity being performed.

### Step 2

Determine whether the activity is reusable.

### Step 3

Separate:

- workflow
    
- procedure
    
- reasoning method
    
- knowledge
    
- evidence
    
- personal preference
    

### Step 4

If it is a reusable HOW, propose a Skill.

### Step 5

If it is WHAT, send it to the Knowledge layer instead.

### Step 6

If it is both, create separate Skill and Knowledge proposals.

Do not combine them into one object.

---

## Skill Object

For each proposed Skill, produce:

```yaml
skill_proposal:
  id: <temporary ID>

  name: <skill name>

  category:
    <one of the six skill domains>

  purpose: >
    <what the skill accomplishes>

  trigger:
    - <when the skill should be used>

  inputs:
    - <required inputs>

  procedure:
    - <step 1>
    - <step 2>
    - <step 3>

  outputs:
    - <expected output>

  knowledge_dependencies:
    - <types of Knowledge required>

  evidence_requirements:
    - <evidence required, if applicable>

  exceptions:
    - <exceptions>

  source:
    - personal_experience
    - industry_workflow
    - best_practice

  status: proposed




## Important Rules

1. Do not create a Skill for every personal experience.
    
2. Do not create a Skill when the input is merely an investment belief.
    
3. Do not hard-code individual Knowledge Objects into the Skill.
    
4. Do not modify an existing Skill automatically.
    
5. Prefer extending an existing Skill when the new behavior belongs to an existing capability.
    
6. Only propose a new Skill when the behavior represents a genuinely reusable capability.
    
7. Keep Skills generic enough to work with future Knowledge Objects.
    
8. Preserve the distinction between workflow and domain knowledge.
    
9. Personal experience can provide the origin of a Skill, but the Skill should be expressed as a reusable capability.
    
10. Industry best practice may be used to identify a candidate Skill, but it must not be represented as the user's personal belief unless the user explicitly adopts it.
    

## Final Output

Return:

```yaml
skill_analysis:

  classification:
    knowledge_items:
      - <items that belong to Knowledge>

    skill_items:
      - <items that belong to Skill>

  skill_proposals:
    - <Skill Proposal>

  existing_skill_extension:
    required: false

  new_skill_required: false

  rationale:
    <why the items were classified this way>
```

````
## 12. 最终你的系统就有两个 Compiler

这其实是你现在这个架构最漂亮的地方：

```text
Personal Experience
        │
        ├───────────────┐
        ↓               ↓
Knowledge Compiler   Skill Extractor
        │               │
        ↓               ↓
Knowledge Object     Skill Proposal
        │               │
        ↓               ↓
Knowledge Library    Skill Library
```

而 **Industry Workflow / Best Practice** 也走 Skill Extractor：

```text
Industry Workflow
       ↓
Skill Extractor
       ↓
Skill Proposal
       ↓
Human Approval
       ↓
Skill Library
```

所以你不是简单地把“个人经验文件化”。

你实际上是在建立一个：

> **Personal Investment Methodology Compiler**

它把三种东西分别编译成：

```text
Personal Experience ──→ Knowledge
                        +
Personal Method ──────→ Skill
                        +
Industry Practice ────→ Skill
```

最后由 Agent Runtime 把：

```text
Skill
  +
Relevant Knowledge
  +
External Evidence
  +
Current Context
```

组合起来执行分析。

**这才是你前面那个 10-step Skill 和个人经验体系真正能长期共存的方式。**
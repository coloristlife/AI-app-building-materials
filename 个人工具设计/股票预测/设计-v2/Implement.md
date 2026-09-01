

如果你的目标是：

> **“我希望今天就能把这些东西放进 Goose / OpenCode / Claude Code / 其他 Agent Runtime，然后直接和 AI 交互。”**

那么我们应该把它进一步落地成**真正的 Skill 文件**，而不是继续写设计说明。

而且我建议不要简单做成“10 个 Prompt 文件”。应该做成符合 Agent Skills 思路的：

```text
skills/
├── market-scan/
│   └── SKILL.md
├── opportunity-scan/
│   └── SKILL.md
├── deep-research/
│   └── SKILL.md
├── thesis-challenge/
│   └── SKILL.md
├── position-decision/
│   └── SKILL.md
├── decision-record/
│   └── SKILL.md
├── position-monitor/
│   └── SKILL.md
├── exit-decision/
│   └── SKILL.md
├── trade-review/
│   └── SKILL.md
└── rule-review/
    └── SKILL.md
```

但这里还有一个更重要的问题：

## 我不建议把“10 个步骤”全部做成独立 Skill

因为 Skill 的意义应该是：

> **告诉 Agent：什么时候应该使用这套能力、输入是什么、应该怎么做、必须遵守什么规则、输出什么结构。**

而不是：

> “用户点击一下 Step 3，然后执行一个 Prompt。”

所以比较合理的是：

```text
                    Investment Agent
                          │
             ┌────────────┴────────────┐
             │                         │
        Investment Rules          Investment Skills
             │                         │
       你的15条经验              10种分析能力
```

然后 Agent 根据你的自然语言自动选择 Skill。

---

# 1. 我们真正应该做的 Skill 是什么样？

例如第一个：

```text
skills/market-scan/SKILL.md
```

应该是真正可以使用的文件。

它可以写成：

````markdown
---
name: market-scan
description: >
  Analyze the current market environment according to the user's
  personal investment rules. Use this skill when the user asks
  about today's market, current market conditions, market sentiment,
  sectors, macro environment, or where potential opportunities may exist.
---

# Market Scan

## Purpose

Analyze the current market environment before evaluating individual stocks.

Do not directly recommend a stock during this stage unless the user explicitly asks
for a candidate list.

The analysis must follow the user's personal investment rules.

## Personal Investment Principles

### R001 - Fear and Greed

Principle:

"别人贪婪我恐惧，别人恐惧我贪婪。"

Use this principle to identify situations where market sentiment may be excessive.

Do not interpret fear alone as a buy signal.

Do not interpret greed alone as a sell signal.

Always distinguish:

- market sentiment
- underlying fundamentals
- valuation
- liquidity
- expectations

### R006 - Human Behavior

Trading is fundamentally a game of human behavior.

Analyze:

- who is buying
- who is selling
- why participants are acting
- what expectations are already priced in
- where behavior may become excessive

### R007 - Price Is Not Sufficient

Do not make the primary investment conclusion from:

- K-line patterns
- index movements
- short-term price movements

Price and technical indicators may be used as supporting evidence.

### R009 - High vs Low

When the market or asset is at a high valuation or euphoric state,
focus on expectations, valuation, and whether the story has already been priced in.

When the market or asset is depressed,
focus more heavily on whether the underlying business is actually deteriorating.

### R015 - Liquidity

Consider whether macro liquidity is supportive or restrictive.

## Required Analysis

Perform the following analysis:

1. Determine the current market regime.
2. Determine market sentiment.
3. Identify the dominant market narratives.
4. Identify the current market consensus.
5. Identify possible areas where consensus may be wrong.
6. Analyze macro liquidity.
7. Identify sectors or themes that deserve further investigation.
8. Identify major risks.
9. Explicitly distinguish facts from inference.
10. Assign confidence levels.

## Evidence Requirements

For every important conclusion:

- Prefer current market data.
- Prefer primary or authoritative sources.
- Do not invent data.
- Do not infer institutional behavior without evidence.
- Clearly mark assumptions.

## Output Format

Return the following structured object:

```yaml
market_scan:
  date: ""
  market_regime: ""
  sentiment:
    state: ""
    evidence: []

  dominant_narratives: []

  market_consensus:
    statements: []

  potential_expectation_gaps:
    - description: ""
      evidence: []
      confidence: 0

  macro:
    liquidity: ""
    evidence: []

  sectors_to_watch:
    - sector: ""
      reason: ""
      risks: []

  major_risks: []

  rule_evaluation:
    - rule_id: ""
      observation: ""
      evidence: ""

  conclusion: ""

  confidence: 0
````

## Important Restrictions

Do not:

- fabricate market data
    
- claim to know what "the main force" or institutions are doing without evidence
    
- treat technical indicators as sufficient evidence
    
- automatically recommend buying
    
- confuse correlation with causation
    

````

**这个才是真正意义上的 Skill。**

它不是我告诉你“这个 Skill 应该干什么”，而是：

> **Agent Runtime 可以实际加载的行为规范。**

---

# 2. 但是仅仅有 SKILL.md 还不够

这是你这个项目特别重要的一点。

你的系统实际上需要：

```text
SKILL.md
    +
Rules
    +
Tools
    +
Schemas
    +
Storage
````

例如：

```text
investment-agent/
│
├── skills/
│   ├── market-scan/
│   │   └── SKILL.md
│   │
│   ├── opportunity-scan/
│   │   └── SKILL.md
│   │
│   ├── deep-research/
│   │   └── SKILL.md
│   │
│   └── ...
│
├── rules/
│   ├── R001-fear-greed.yaml
│   ├── R002-capital-preservation.yaml
│   ├── R003-profit-management.yaml
│   ├── R004-cheap-quality.yaml
│   ├── ...
│   └── R015-liquidity.yaml
│
├── schemas/
│   ├── market-scan.yaml
│   ├── investment-case.yaml
│   ├── decision.yaml
│   ├── trade.yaml
│   └── review.yaml
│
├── tools/
│   ├── market-data
│   ├── financial-data
│   ├── portfolio
│   └── calculator
│
└── storage/
    └── investment.db
```

这样才形成一个**真正可以运行的个人投资 Agent**。

---

# 3. 为什么要把 Rule 从 Skill 中拆出来？

这是我特别建议你这样做的地方。

你的：

> “别人贪婪我恐惧”

不是一个 Skill。

它其实是：

> **Investment Rule。**

而：

> “分析当前市场”

才是 Skill。

所以：

```text
Rule
=
你认为世界应该如何判断

Skill
=
AI应该如何执行一个任务
```

例如：

```text
R001
别人贪婪我恐惧
```

可以被：

```text
market-scan
opportunity-scan
thesis-challenge
exit-decision
```

四个 Skill 使用。

这样以后你发现：

> “别人恐惧我贪婪这个原则，在基本面持续恶化的公司上经常失败。”

你只需要修改：

```text
R001
```

而不用修改四个 Skill。

---

# 4. Rule 也可以是真正可以直接使用的文件

比如：

```text
rules/R001-fear-greed.yaml
```

直接写：

```yaml
id: R001

name: fear-and-greed

statement: >
  别人贪婪我恐惧，别人恐惧我贪婪。

intent:
  - identify excessive market optimism
  - identify excessive market pessimism
  - search for sentiment/fundamental divergence

applicable_skills:
  - market-scan
  - opportunity-scan
  - thesis-challenge
  - exit-decision

requirements:
  - sentiment must be evaluated
  - fundamentals must be evaluated
  - valuation must be evaluated
  - liquidity should be considered

constraints:
  - fear alone is not a buy signal
  - greed alone is not a sell signal
  - do not override fundamental deterioration
  - do not infer institutional intent without evidence

required_output:
  - sentiment
  - evidence
  - divergence
  - risk
  - confidence
```

这已经不是“描述”。

它就是：

> **机器可以读取的投资规则。**

---

# 5. 最关键的是：你和 AI 的交互可以非常自然

你不需要自己每天选择：

> Skill 01  
> Skill 02  
> Skill 03

你可以直接说：

> **“帮我看看今天美股市场。”**

Agent 根据 Skill description 判断：

```text
market-scan
```

然后运行。

---

你说：

> **“最近 NVIDIA 怎么样？我感觉跌下来以后挺便宜。”**

Agent 应该判断：

```text
opportunity-scan
        ↓
deep-research
        ↓
thesis-challenge
```

---

你说：

> **“我准备买 NVIDIA，准备投入 10%。”**

Agent 应该进入：

```text
thesis-challenge
        ↓
position-decision
```

---

你说：

> **“我刚刚买了 NVIDIA，记录一下。”**

进入：

```text
decision-record
```

然后自动写数据库。

---

你说：

> **“看看我的 NVIDIA 还要不要继续拿。”**

进入：

```text
position-monitor
```

---

你说：

> **“我准备卖掉 NVIDIA。”**

进入：

```text
exit-decision
```

---

你说：

> **“把我最近卖掉的股票复盘一下。”**

进入：

```text
trade-review
```

---

你说：

> **“看看我的‘别人恐惧我贪婪’到底有没有用。”**

进入：

```text
rule-review
```

---

# 6. 这才是 Agent 在这里真正的作用

Agent 并不是：

> “一个更高级的 Prompt。”

它负责：

```text
理解用户意图
      ↓
识别当前处于哪个投资阶段
      ↓
选择 Skill
      ↓
读取相关 Rules
      ↓
判断需要什么 Tools
      ↓
获取数据
      ↓
调用 LLM 分析
      ↓
生成结构化结果
      ↓
保存 Investment Record
      ↓
决定下一步
```

所以它才是：

> **Orchestrator。**

---

# 7. 而历史记录也不应该靠 Skill 自己保存

这一点我也想纠正一下之前的说法。

不要在每个 Skill 里面写：

> “请把结果保存到数据库。”

更好的架构是：

```text
Skill
  ↓
Structured Output
  ↓
Agent Runtime
  ↓
Record Manager
  ↓
Database
```

也就是说：

### Skill

只负责：

> **产生标准化结果。**

### Record Manager

负责：

> **把结果持久化。**

这样十个 Skill 都不用关心数据库。

---

# 8. 例如今天的整个过程

你：

> “帮我看看今天市场。”

Agent：

```text
调用 market-scan
```

得到：

```yaml
market_scan:
  market_regime: risk_on
  sentiment: greedy
  ...
```

系统自动创建：

```text
CASE-2026-0821-001
```

---

然后你：

> “那帮我看看有没有被低估的公司。”

Agent：

```text
opportunity-scan
```

生成：

```yaml
candidates:
  - NVDA
  - XXX
  - XXX
```

这些结果**自动追加到 Case**。

---

然后你：

> “深入看看 NVDA。”

Agent：

```text
deep-research
```

然后：

```text
thesis-challenge
```

然后你说：

> “我想买。”

Agent：

```text
position-decision
```

最后：

```text
decision-record
```

数据库里面最终是：

```text
CASE-2026-0821-001
│
├── Market Scan
│
├── Opportunity Scan
│
├── NVDA Research
│
├── Thesis Challenge
│
├── Position Decision
│
└── Decision Record
```

---

# 9. 几个月以后

你说：

> **“复盘我过去三个月的投资。”**

系统不是去搜索聊天记录。

而是：

```text
Database Query
       ↓
所有 Investment Cases
       ↓
所有 Decisions
       ↓
所有 Trades
       ↓
所有 Outcomes
       ↓
Trade Review
       ↓
Rule Review
       ↓
LLM
```

最后告诉你：

> “过去三个月你执行了 R004（好的便宜筹码）17 次，其中 12 次有效，但其中 4 次发生在基本面恶化的公司。”

然后进一步：

> **“建议把 R004 修改为：只有在基本面没有发生结构性恶化时，‘便宜’才构成低吸候选。”**

这就是你这个系统真正有价值的地方。

---

# 10. 所以你的下一步不应该再讨论“Skill是什么”

而应该真正开始**把它做出来**。

我建议第一版直接建立一个：

```text
personal-investment-agent/
```

然后我可以直接帮你生成完整的第一版，包括：

```text
personal-investment-agent/
│
├── README.md
│
├── skills/
│   ├── 01-market-scan/
│   │   └── SKILL.md
│   ├── 02-opportunity-scan/
│   │   └── SKILL.md
│   ├── 03-deep-research/
│   │   └── SKILL.md
│   ├── 04-thesis-challenge/
│   │   └── SKILL.md
│   ├── 05-position-decision/
│   │   └── SKILL.md
│   ├── 06-decision-record/
│   │   └── SKILL.md
│   ├── 07-position-monitor/
│   │   └── SKILL.md
│   ├── 08-exit-decision/
│   │   └── SKILL.md
│   ├── 09-trade-review/
│   │   └── SKILL.md
│   └── 10-rule-review/
│       └── SKILL.md
│
├── rules/
│   ├── R001.yaml
│   ├── R002.yaml
│   └── ... R015.yaml
│
├── schemas/
│   ├── investment-case.yaml
│   ├── decision.yaml
│   ├── trade.yaml
│   └── review.yaml
│
└── examples/
    └── example-investment-case.yaml
```

**每一个 `SKILL.md` 我都会写成可以直接交给 Agent Runtime 使用的正式 Skill，而不是再给你一个 user guide。** 同时把你最开始给我的 **15 条投资经验逐条转成真正的 Rule 文件**，做到每条经验都有 `id → 使用场景 → 触发条件 → 推理要求 → 限制条件 → 所需证据 → 输出要求 → 后续复盘指标`。

这样下一步就可以直接拿这个目录去适配 **Goose / OpenCode / Claude Code / DojoAgents** 等支持 Skill 的 Agent Runtime，而不是停留在架构设计层面。
把之前的方案**正式收敛成下面这一版**。这一版的核心目标就是：

> **以后无论你增加多少新的炒股经验，都不需要重新设计 Agent Workflow；只需要把新经验转换成 Knowledge Object，进入知识库，并通过验证逐渐演进。**

同时，它也能直接落到你前面一直讨论的 **DojoAgents / Goose + Skill + Tool + Rule + History** 体系中。

# 个人投资决策 Agent —— 最终架构方案

## 1. 总体架构

最终采用：

> **4 层架构 + 1 个横向编排层 + 1 个知识演进闭环**

```text
┌──────────────────────────────────────────────────────────┐
│              Generic Agent Decision Workflow             │
│                                                          │
│  01 Understand                                           │
│  02 Contextualize                                        │
│  03 Retrieve Knowledge                                   │
│  04 Gather Evidence                                      │
│  05 Analyze                                              │
│  06 Challenge                                            │
│  07 Decide                                               │
│  08 Act                                                  │
│  09 Monitor                                              │
│  10 Learn                                                │
└──────────────────────────┬───────────────────────────────┘
                           │
                           ↓
┌──────────────────────────────────────────────────────────┐
│           Context & Knowledge Orchestration              │
│                                                          │
│  Knowledge Resolver                                      │
│  Evidence Planner                                        │
│  Context Builder                                         │
│  Conflict Resolver                                       │
└───────────────┬───────────────────────┬──────────────────┘
                │                       │
                ↓                       ↓
┌────────────────────────┐    ┌────────────────────────────┐
│    Knowledge Layer     │    │        Tool Layer          │
│                        │    │                            │
│ Principles             │    │ Market Data                │
│ Rules                  │    │ Financial Data             │
│ Patterns               │    │ News / Sentiment           │
│ Constraints            │    │ Portfolio                  │
│ Heuristics             │    │ Calculation                │
│ Strategies             │    │ Execution                  │
│ Experiences            │    │                            │
│ Lessons                │    │                            │
└────────────┬───────────┘    └──────────────┬─────────────┘
             │                               │
             └───────────────┬───────────────┘
                             ↓
                    ┌─────────────────┐
                    │       LLM       │
                    │ Reasoning Core  │
                    └────────┬────────┘
                             ↓
┌──────────────────────────────────────────────────────────┐
│                  Persistence Layer                       │
│                                                          │
│ Decisions / Trades / Evidence / Outcomes / Reviews       │
│ Knowledge Versions / Rule Performance / Learning History │
└──────────────────────────┬───────────────────────────────┘
                           │
                           ↓
                  Knowledge Evolution
                           │
                  Human Approval
                           │
                           └────→ Knowledge Layer
```

---

# 2. 最重要的架构原则

整个系统遵守 6 条原则。

### 原则一：Workflow 稳定，Knowledge 动态

Workflow：

```text
Understand
→ Contextualize
→ Retrieve
→ Evidence
→ Analyze
→ Challenge
→ Decide
→ Act
→ Monitor
→ Learn
```

**基本不变。**

而：

```text
Rules
Patterns
Experiences
Strategies
```

可以无限增加。

---

### 原则二：Skill 不等于 Knowledge

这是前面讨论中最重要的结论之一。

**Skill：**

> AI 如何完成一类工作。

**Knowledge：**

> 你认为应该依据什么进行判断。

例如：

```text
Skill:
Analyze Opportunity

Knowledge:
别人恐惧我贪婪

Knowledge:
买阴不买阳

Knowledge:
低位缩量新低

Knowledge:
放量滞涨
```

因此以后新增经验**不需要新增 Skill**。

---

### 原则三：Tool 不负责解释投资经验

Tool 只回答：

> **现实世界发生了什么？**

例如：

```text
get_price()
get_volume()
get_ma250()
get_financials()
get_news()
get_portfolio()
```

返回事实。

至于：

> “这个事实意味着什么？”

由 Knowledge + LLM 判断。

---

### 原则四：Knowledge 不等于 Truth

你的个人经验进入系统后，默认应该被认为：

> **Hypothesis / Personal Heuristic**

而不是事实。

例如：

```text
R004:
缩量新低 → 可能是底部
```

系统不能直接变成：

```text
缩量新低 → BUY
```

而应该：

```text
Rule
+
Current Evidence
+
Market Regime
+
Historical Performance
+
Challenge
↓
Decision
```

---

### 原则五：Decision 必须包含 Risk

不是：

```yaml
action: BUY
```

而是：

```yaml
action: BUY

position:
  initial_allocation: 0.05

risk:
  max_account_loss: 0.02

entry:
  ...

exit:
  ...

invalidation:
  ...
```

**买不买只是第一层问题。**

真正完整的交易决策是：

> 买什么、为什么买、买多少、什么时候买、错了怎么办、什么时候卖。

---

### 原则六：AI 可以修改知识，但不能无条件自动修改

最终形成：

```text
Experience
↓
Knowledge
↓
Validation
↓
Usage
↓
Outcome
↓
Review
↓
Proposed Update
↓
Human Approval
↓
New Knowledge Version
```

所以这是一个：

> **Knowledge Evolution System**

而不是一个简单的 RAG。

---

# 3. Generic Agent Workflow

这 10 步以后固定下来。

---

## 01 Understand

理解用户任务。

输入：

```yaml
request:
  user_message: "NVDA 跌了 8%，现在是不是买阴？"
```

输出：

```yaml
task:
  type: investment_decision
  subject: NVDA
  objective: evaluate_buy_opportunity
  horizon: short_term
```

---

# 4. 02 Contextualize

建立当前上下文。

包括：

```text
Market
Sector
Stock
Portfolio
Position
Time Horizon
Risk State
Market Regime
```

可能调用：

```text
get_market_context
get_sector_context
get_stock_context
get_portfolio_context
```

输出：

```yaml
context:
  market_regime: bear_market
  sector_regime: weak
  stock_trend: down
  existing_position: 0
```

---

# 5. 03 Retrieve Knowledge

由：

## Knowledge Resolver

根据：

```text
Task
Context
Initial Evidence
```

寻找相关 Knowledge。

例如：

```text
P001 Fear & Greed
P002 Capital Preservation

R003 Volume Down
R004 Shrinking New Low
R010 Downtrend Elasticity

C001 Max Risk
C002 Equal Position
```

注意：

**Skill 不硬编码这些 Rule。**

Resolver 动态寻找。

---

# 6. 04 Gather Evidence

调用 Tool 获取事实。

例如：

```text
Market Data
Price
Volume
MA250
Support
Financials
News
Sentiment
Portfolio
Historical Cases
```

这里与 03 不是线性关系。

实际运行：

```text
Base Evidence
      ↓
Knowledge Retrieval
      ↓
Evidence
      ↓
More Knowledge?
      ↓
More Evidence?
      ↓
...
      ↓
Sufficient Evidence
```

这就是：

> **Evidence–Knowledge Discovery Loop**

---

# 7. 05 Analyze

LLM 接收到：

```text
Task
+
Context
+
Relevant Knowledge
+
Evidence
+
Historical Cases
```

然后判断：

```text
哪些 Rule 被触发？
哪些 Rule 不适用？
哪些 Evidence 支持？
哪些 Evidence 反驳？
当前属于什么市场环境？
历史上类似情况如何？
```

---

# 8. 06 Challenge

这是必须存在的“反方”。

例如：

```text
Rule:
缩量新低 → 左侧机会

Challenge:
但是：

MA250 向下
+
大盘处于熊市
+
基本面恶化

那么这个 Rule 是否仍然有效？
```

输出：

```yaml
challenge:
  supporting_factors:
    - low_volume
    - oversold

  conflicting_factors:
    - bearish_long_term_trend
    - weak_sector

  unresolved:
    - historical_rebound_probability
```

如果证据不足：

> **不要强行 Decision。**

可以返回：

```text
INSUFFICIENT_EVIDENCE
```

---

# 9. 07 Decide

标准输出必须结构化。

```yaml
decision:
  action: WAIT

  confidence:
    overall: 0.68

  thesis:
    summary: "..."

  position:
    initial_allocation: 0.00
    target_allocation: 0.05

  entry:
    strategy: scale_in
    conditions:
      - ...

  risk:
    max_account_loss: 0.02
    stop_condition:
      - ...

  exit:
    conditions:
      - ...

  invalidation:
    - ...

  monitoring:
    - volume
    - MA250
    - sector_strength
```

---

# 10. 08 Act

将 Decision 转换成 Action。

第一阶段：

```text
AI Decision
     ↓
Human Approval
     ↓
Execution Tool
```

以后可以接：

```text
Broker API
Trading API
```

但 Agent 不应该直接拥有无限制交易权限。

---

# 11. 09 Monitor

监控 Decision 中定义的：

```text
Entry
Position
Stop
Target
Invalidation
Market Regime
Rule Conditions
```

如果条件变化：

```text
Monitoring
   ↓
New Evidence
   ↓
Retrieve Knowledge
   ↓
Re-analyze
   ↓
Re-decide
```

所以 09 实际上又可以进入：

```text
03 → 04 → 05 → 06 → 07
```

而不是单向结束。

---

# 12. 10 Learn

交易结束：

```text
Decision
+
Evidence
+
Execution
+
Outcome
```

进行 Review。

例如：

```yaml
review:
  predicted_action: BUY
  actual_outcome: LOSS

  prediction_quality:
    thesis_correct: false

  contributing_factors:
    - market_regime
    - false_breakout

  rule_evaluation:
    - rule_id: R004
      result: failed
```

然后生成：

```yaml
proposed_knowledge_update:
  target_id: R004

  action: restrict_applicability

  proposal:
    bear_market: weak

  reason: "..."

  requires_human_approval: true
```

---

# 13. Knowledge Layer

这是整个系统最有价值的资产。

统一使用：

## Knowledge Object

而不是把所有东西都叫 Rule。

支持：

```text
Principle
Rule
Pattern
Constraint
Strategy
Heuristic
Observation
Experience
Lesson
```

---

# 14. Knowledge Object 推荐结构

例如：

```yaml
id: KO-000123

type: rule

name: shrinking_volume_new_low

domain:
  - technical
  - short_term

statement: >
  低位缩量创新低可能意味着
  杀跌动能衰竭。

conditions:
  - price_near_support
  - volume_declining

signals:
  - new_low
  - declining_volume

actions:
  preferred:
    - observe
    - consider_small_entry

applicable_regimes:
  bull_market: conditional
  sideways_market: strong
  bear_market: weak

authority:
  level: rule

reliability:
  score: 0.62

evidence_strength:
  score: 0.71

status:
  active

source:
  type: personal_experience

validation:
  sample_size: 0

version:
  number: 1

created_at: ...
updated_at: ...
```

---

# 15. 为什么一定要有 `applicable_regimes`

因为你的经验里面已经明确存在：

> “这些方法适合震荡市和弱势环境，但单边大牛市需要修正。”

因此知识本身就应该知道：

```text
Bull
Bear
Sideways
High Volatility
Low Liquidity
```

否则 AI 很容易把：

> 熊市经验

错误应用到：

> 牛市。

---

# 16. Knowledge Resolver

这是系统最核心的基础设施之一。

接口可以抽象成：

```python
resolve(
    task,
    context,
    evidence,
    constraints
)
```

输出：

```yaml
knowledge_context:

  relevant:
    - id: R004
      relevance: 0.91

    - id: R010
      relevance: 0.84

  constraints:
    - id: C001

  conflicts:
    - R004
    - R003

  missing_evidence:
    - volume_profile
    - MA250
```

底层以后可以是：

```text
YAML
SQLite
PostgreSQL
Vector DB
Knowledge Graph
```

Workflow 不关心。

---

# 17. 第一阶段不需要急着上 Knowledge Graph

我建议：

### Phase 1

```text
YAML / Markdown
+
Metadata
+
SQLite/PostgreSQL
+
Semantic Retrieval
```

### Phase 2

知识规模增加后：

```text
Vector Search
+
Metadata Filtering
+
LLM Re-ranking
```

### Phase 3

真正出现大量关系：

```text
Knowledge Graph
```

这样不会过度工程化。

---

# 18. Tool Layer

Tool 只负责现实世界。

可以分成：

```text
market/
    get_price
    get_volume
    get_market_index
    get_market_regime

financial/
    get_financials
    get_valuation

research/
    get_news
    get_sentiment
    get_institutional_flow

portfolio/
    get_positions
    get_cash
    get_trade_history

calculation/
    calculate_ma
    calculate_volatility
    calculate_position_size

execution/
    create_order
    cancel_order
```

---

# 19. Persistence Layer

必须从第一天就设计。

至少保存：

```text
Case
Decision
Evidence
Tool Results
Trade
Outcome
Review
Knowledge Version
Rule Performance
```

---

# 20. 一次完整交易应该成为一个 Case

例如：

```yaml
case_id: CASE-2026-000123

request:
  ...

context:
  ...

knowledge_used:
  - P001
  - R004
  - R010
  - C001

evidence:
  ...

analysis:
  ...

challenge:
  ...

decision:
  ...

execution:
  ...

outcome:
  ...

review:
  ...

knowledge_updates:
  ...
```

这非常重要。

因为未来你复盘的不是：

> “我当时买了 NVDA。”

而是：

> **“当时 AI 为什么认为应该买？用了哪些个人经验？当时有什么证据？哪些 Rule 最终被证明有效/无效？”**

---

# 21. Knowledge Evolution

最终形成：

```text
Draft
 ↓
Active
 ↓
Validated
 ↓
Degraded
 ↓
Retired
```

例如：

```text
R004
↓
使用 50 次
↓
胜率 72%
↓
牛市 81%
震荡 74%
熊市 42%
↓
AI 提议：
“限制熊市适用性”
↓
Human Approval
↓
Version 2
```

这样你的投资经验就不是静态 Markdown。

它变成：

> **可验证、可演进的个人知识资产。**

---

# 22. 你的两批经验最终怎么进入系统？

### 第一批

例如：

```text
别人贪婪我恐惧
保护本金
不要赚了钱就消费
低吸便宜筹码
稳住心态
人性博弈
指数/K线不能盲信
好公司三要素
高位不讲故事
低位不看业绩
```

转换成：

```text
Principles
Rules
Heuristics
Constraints
```

---

### 第二批

例如：

```text
买阴卖阳
年线
放量下跌
缩量新低
增量回升
三连阴
三颗星
下跌弹性
冷洗热卖
放量滞涨
热门题材轮动
等仓
2%风险
连续止损
```

转换成：

```text
Rules
Patterns
Constraints
Strategies
```

**不会改变 Workflow。**

---

# 23. 第三批、第四批经验怎么办？

只需要：

```text
New Experience
       ↓
Knowledge Extraction
       ↓
Knowledge Object
       ↓
Validation
       ↓
Index
       ↓
Available to Agent
```

**不用修改 10 个步骤。**

这就是这个架构最大的价值。

---

# 24. Skill 到底放在哪里？

这里也最终定下来。

**Skill 是 Workflow 的能力实现，不是经验存储。**

例如：

```text
skills/
├── understand_task
├── contextualize
├── retrieve_knowledge
├── gather_evidence
├── analyze
├── challenge
├── decide
├── execute
├── monitor
└── review
```

Skill 里面写：

> 如何完成这个任务。

而不是：

> 把你的 100 条投资口诀全部塞进来。

Skill 通过：

```text
Knowledge Resolver
```

动态取得相关 Knowledge。

---

# 25. 所以 DojoAgents / Goose 在这里的位置

最终：

```text
Your Investment System
│
├── Generic Decision Workflow
├── Knowledge Layer
├── Knowledge Resolver
├── Tool Layer
├── Persistence Layer
└── Investment Domain Logic
             │
             ↓
       Agent Runtime
       ┌─────┴─────┐
       │           │
   DojoAgents    Goose
```

也就是说：

**不要把整个系统建立在 Goose 或 DojoAgents 的 Skill 机制之上。**

应该反过来：

> **你的系统拥有自己的 Knowledge / Workflow / Persistence；DojoAgents 或 Goose 是 Runtime。**

这样以后换 Agent Runtime 不会把你的核心资产带走。

---

# 26. 第一版实际落地，我建议不要做得太复杂

你现在完全不需要马上：

- Knowledge Graph
    
- 大型 Vector DB
    
- 自动交易
    
- 多 Agent
    
- 复杂机器学习
    
- 自动修改 Rule
    

第一版可以非常简单：

```text
                    DojoAgents
                        │
                     Agent
                        │
                   10-step Loop
                        │
          ┌─────────────┼─────────────┐
          ↓             ↓             ↓
       Skills       Knowledge       Tools
          │             │             │
          │          YAML/MD       APIs
          │             │             │
          └─────────────┼─────────────┘
                        ↓
                   Context Builder
                        ↓
                       LLM
                        ↓
                   Decision YAML
                        ↓
                  SQLite/Postgres
```

**这已经可以做出真正可用的 POC。**

---

# 27. 最终的技术栈建议

如果让我现在帮你落地，我会选：

|层|第一版|
|---|---|
|Agent Runtime|**DojoAgents**|
|Workflow|Python|
|Skill|Markdown/YAML + 少量 Python|
|Knowledge|YAML/Markdown|
|Retrieval|SQLite/Postgres + metadata/semantic retrieval|
|Tools|Python tools / MCP|
|History|PostgreSQL 或 SQLite|
|Decision Schema|YAML / JSON Schema|
|LLM|你选择的 Model Provider|
|Execution|暂时 Human-in-the-loop|
|Vector DB|后期再加|
|Knowledge Graph|后期再加|

---

# 28. 最终架构原则，可以正式作为项目 Architecture Statement

> **本系统采用 Generic Decision Agent Architecture，将 Agent Workflow、Knowledge、Tools 和 Persistence 四个核心层彻底解耦。**
> 
> **Agent Workflow** 是稳定的通用决策生命周期，由 Understand、Contextualize、Retrieve Knowledge、Gather Evidence、Analyze、Challenge、Decide、Act、Monitor 和 Learn 十个阶段组成。Workflow 不包含具体投资经验，因此不会因为新增个人经验而发生结构性变化。
> 
> **Knowledge Layer** 是系统的动态知识资产，采用统一的 Knowledge Object 表示 Principle、Rule、Pattern、Constraint、Strategy、Heuristic、Experience 和 Lesson 等不同类型的知识。Knowledge Object 具有适用环境、可靠性、证据强度、状态和版本等属性，并通过 Knowledge Resolver 动态参与 Agent 决策。
> 
> **Tool Layer** 负责获取和操作现实世界数据，包括市场数据、财务数据、新闻、投资组合、计算以及交易执行。Tool 不负责解释个人投资经验，从而避免领域知识与工具实现耦合。
> 
> **Persistence Layer** 保存每一次 Decision Case 的上下文、Knowledge、Evidence、Decision、Execution、Outcome 和 Review，使每一次交易都成为可复盘、可验证的历史记录。
> 
> **Context & Knowledge Orchestration** 负责在 Workflow 运行过程中动态协调 Knowledge、Evidence、Tool Results 和 Historical Records。Knowledge Retrieval 与 Evidence Gathering 可以进行迭代循环，而不是简单的线性流程。
> 
> **Knowledge Evolution** 将历史交易结果反馈给 Knowledge Layer。AI 可以根据历史表现提出 Knowledge 更新建议，但 Knowledge 的关键修改需要经过人工确认，从而避免知识库发生不可控漂移。
> 
> **该架构将个人投资经验从固定 Prompt 转变为可检索、可验证、可版本化、可演进的知识资产，使 Agent Runtime、Workflow、Tools 和 Knowledge 可以独立演进。未来新增投资经验不需要重新设计 Workflow，只需新增或更新 Knowledge Object。**

---

## 最终你真正要构建的，不是“一个 AI 炒股 App”

而是下面这个东西：

```text
                 Personal Investment OS
                         │
          ┌──────────────┴──────────────┐
          │                             │
   Decision Engine              Personal Knowledge
          │                             │
   Generic Workflow             Your Experience
          │                             │
          └──────────────┬──────────────┘
                         ↓
                   Evidence / Tools
                         ↓
                      Decision
                         ↓
                      Outcome
                         ↓
                      Review
                         ↓
                 Knowledge Evolution
```

**你的第一批经验、第二批经验，以及未来所有新增经验，最终都会沉淀到右边的 Personal Knowledge；左边的 Decision Engine 不需要跟着你的经验不断重构。**

这就是这套方案真正的“generic”和可扩展性。
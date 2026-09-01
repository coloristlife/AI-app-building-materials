

> **一个 Rule 本身就是一个小型决策程序。**

它必须告诉 AI：

- 什么时候适用？
    
- 什么时候不适用？
    
- 需要什么输入？
    
- 哪些输入是市场数据？
    
- 哪些输入可以从工具获取？
    
- 哪些必须问用户？
    
- 如果输入缺失怎么办？
    
- 满足什么条件才触发？
    
- 触发以后产生什么判断？
    
- 输出什么？
    
- 输出的结果能不能直接成为交易动作？
    
- 和其他 Rule 冲突怎么办？
    

所以我建议你这次不要再把它叫成简单的“Rule 文件”。

---

# 我建议最终采用这个模型

不是：

```text
Skill
  ↓
Knowledge
  ↓
Rules
```

而是：

```text
                    Investment Skill
                           │
                    Rule Orchestrator
                           │
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
       Rule 001          Rule 002         Rule 003
          │                │                │
     Applicability     Applicability    Applicability
     Input            Input             Input
     Evidence         Evidence          Evidence
     Evaluation       Evaluation        Evaluation
     Output           Output            Output
          └────────────────┼────────────────┘
                           ↓
                    Decision Synthesis
                           ↓
                     Risk Control
                           ↓
                      Final Output
```

这里真正重要的是：

> **Rule 不只是 Knowledge，而是“带有执行契约的 Knowledge”。**

---

# 一、每个 Rule 应该有一个统一的“契约”

但是注意，我不是建议你搞一个复杂的软件 Schema。

你只需要规定：

> **每一个 Rule 都必须回答 7 个问题。**

这是整个系统最重要的设计。

## Rule Contract

每个 Rule 必须包含：

### 1. Purpose

这个 Rule 是干什么的？

### 2. Applicability

什么情况下使用？

什么情况下不要使用？

### 3. Required Inputs

这个 Rule 需要什么信息？

### 4. Evidence Source

这些信息从哪里来？

- 用户已经提供
    
- 市场数据工具
    
- 新闻工具
    
- 计算得到
    
- 用户必须确认
    

### 5. Evaluation

拿到输入以后，怎么判断？

### 6. Output

这个 Rule 最终产生什么结果？

### 7. Limitations

这个 Rule **不能证明什么**。

---

# 二、这样你刚才问的“缺输入怎么办”就解决了

比如你的：

> 低位缩量新低 → 左侧试仓

如果 AI 要使用它，它首先发现需要：

```text
Required Inputs:

1. 当前价格
2. 最近一段时间价格
3. 历史低点
4. 成交量
5. 最近成交量趋势
6. 股票当前趋势
```

然后 AI 不应该直接分析。

它应该进入：

# Input Resolution

逐个检查：

```text
当前价格       → 已有
历史价格       → 需要市场数据
成交量         → 需要市场数据
250MA          → 需要计算/市场数据
板块状态       → 需要外部数据
```

然后才决定：

> **哪些自己获取，哪些问用户。**

---

# 三、这里应该有一个非常明确的 Input Acquisition Policy

这是你刚才指出的一个非常关键的问题。

我建议固定成下面这个优先级：

```text
Rule Required Input
        ↓
用户已经提供？
   ↓ Yes
直接使用
   ↓ No
能通过工具获得？
   ↓ Yes
自动获取
   ↓ No
能从已有数据计算？
   ↓ Yes
计算
   ↓ No
是否必须由用户决定？
   ↓ Yes
询问用户
   ↓ No
标记 Unknown
```

这比“缺数据就问用户”专业很多。

---

# 四、什么时候 AI 自己查，什么时候问用户？

这个也应该成为 Skill 的固定规则。

## AI 应该自己获取的

例如：

- 当前股价
    
- 历史价格
    
- 成交量
    
- 250MA
    
- RSI
    
- MACD
    
- 财报
    
- 新闻
    
- 板块表现
    
- 市场指数
    

这些属于：

> **External Evidence**

如果 Agent 有相应工具，就应该自己获取。

用户没必要告诉 AI：

> “今天成交量是多少？”

---

## AI 应该问用户的

例如：

- 你这笔交易原来的买入逻辑是什么？
    
- 你现在有没有持仓？
    
- 买入价格是多少？
    
- 这是短线交易还是中线交易？
    
- 你愿意承担多少风险？
    
- 你最近是不是已经连续止损两笔？
    

这些属于：

> **User-Specific Context**

AI 通常无法可靠地从市场数据推断。

所以应该问用户。

---

# 五、还有第三类：AI 自己计算

例如 Rule 002：

> 250MA 向上还是向下？

用户没有提供。

市场数据也可能只给你价格。

那么 AI：

```text
获取过去250个交易日价格
        ↓
计算250MA
        ↓
计算250MA slope
        ↓
判断：
Up / Flat / Down
```

这不是“外部知识”，也不是“用户输入”。

而是：

> **Derived Evidence**

这个概念非常重要。

---

# 六、所以一个 Rule 实际上应该长这样

比如你的 Rule 003：

```text
# Rule 003 — 量价异动风控法则

## Purpose

通过价格与成交量的组合判断：
- 高位放量下跌
- 低位缩量新低
- 增量回升后的回踩确认

---

## Applicable When

当股票出现以下任一情况时考虑使用：

- 明显价格下跌并伴随成交量变化
- 创阶段新高/新低
- 突然出现异常成交量
- 从低位开始反弹

---

## Not Applicable When

如果缺少可靠的价格或成交量数据，不使用本 Rule 做结论。

---

## Required Inputs

### Market Data

- current_price
- historical_price
- trading_volume
- historical_volume

### Derived Data

- price_position
- recent_high
- recent_low
- volume_trend

---

## Evidence Sources

| Input | Source |
|---|---|
| current_price | Market Data Tool |
| historical_price | Market Data Tool |
| trading_volume | Market Data Tool |
| price_position | Derived |
| volume_trend | Derived |

---

## Evaluation

### Case A — High Position + High Volume + Falling Price

Interpretation:

Potential distribution / exit risk.

Suggested action:

REDUCE or EXIT depending on context.

---

### Case B — Low Position + New Low + Declining Volume

Interpretation:

Selling pressure may be weakening.

Suggested action:

Potential SCALE IN.

This is not confirmation of reversal.

---

### Case C — Increasing Volume During Recovery + Pullback Holds

Interpretation:

Potential right-side confirmation.

Suggested action:

Potentially increase exposure, subject to position-management rules.

---

## Output

Return:

- matched_pattern
- evidence
- interpretation
- confidence
- suggested_action

---

## Limitations

This Rule alone cannot establish:

- confirmed bottom
- confirmed trend reversal
- long-term investment value

It must be evaluated together with trend and risk-management rules.
```

你看，这时候它已经不是简单的“Knowledge”。

它实际上已经变成：

> **一个可以被 Agent 调用的 Decision Rule。**

---

# 七、那么 Skill 真正的职责是什么？

现在就清楚了。

**Skill 不负责知道每条 Rule 的具体内容。**

Skill 负责管理整个生命周期：

```text
1. Understand Request
        ↓
2. Identify Candidate Rules
        ↓
3. Load Rules
        ↓
4. Resolve Required Inputs
        ↓
5. Acquire Missing Evidence
        ↓
6. Evaluate Rules
        ↓
7. Combine Rule Results
        ↓
8. Resolve Conflicts
        ↓
9. Apply Risk Controls
        ↓
10. Produce Decision
```

这才是一个真正的 **Skill**。

---

# 八、所以我会把你的 Skill 改成这种定位

一句话：

> **Skill = Rule Orchestrator + Evidence Orchestrator + Decision Synthesizer**

而：

> **Rule = 一个具有输入、适用条件、判断逻辑和输出的个人投资知识单元。**

这就非常清楚了。

---

# 九、整个系统最终其实只有三个东西

我不想再给你增加第四个、第五个东西。

就三个：

```text
① SKILL
   ↓
   怎么协调整个分析过程

② RULES
   ↓
   你的个人投资经验如何执行

③ TOOLS / DATA
   ↓
   给 Rules 提供外部证据
```

然后运行：

```text
User Question
      ↓
   SKILL
      ↓
找哪些 RULE？
      ↓
RULE 告诉我需要什么 INPUT？
      ↓
SKILL 检查 INPUT
      ↓
已有 → 使用
缺失但工具能拿 → 自动获取
缺失但能计算 → 计算
必须用户提供 → 问用户
      ↓
RULE Evaluation
      ↓
多个 Rule Results
      ↓
SKILL 综合
      ↓
Risk Rule
      ↓
Final Decision
```

---

# 十、这也回答了你最后一个问题：Skill 能不能实现？

**能，但前提是 Skill 不能只是我前面写的那种“使用说明书”。**

它必须是一个**执行型 Skill**。

而且你现在的直觉非常正确：

> 如果 Rule 本身没有定义自己的 Input / Applicability / Evidence / Evaluation / Output，那么 Skill 再怎么写，也只能靠 LLM 猜。

而你真正想要的是：

> **减少 LLM 猜测。**

所以应该把**变化的东西放到 Rule 里面**：

```text
每个 Rule 自己定义：
    我什么时候用
    我需要什么
    我的数据从哪里来
    怎么判断
    我能产生什么结论
    我不能产生什么结论
```

把**不变的东西放到 Skill 里面**：

```text
所有 Rule 都按照：
    Discover
    Load
    Resolve Inputs
    Acquire Evidence
    Evaluate
    Combine
    Resolve Conflict
    Apply Risk
    Output
```

这就是我认为你现在这个投资 AI 架构应该最终固定下来的设计。

而且它和你之前一直在考虑的 **Personal Experience → Knowledge → Skill → Evidence → Decision** 思路是一致的，只是现在把中间最容易出问题的 **Rule 的“执行契约”** 补上了。
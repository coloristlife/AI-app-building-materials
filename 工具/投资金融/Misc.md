https://github.com/ZhuLinsen/daily_stock_analysis
LLM 驱动的多市场股票智能分析系统：多源行情、实时新闻、决策看板与自动推送，支持零成本定时运行。 LLM-powered multi-market stock analysis system with multi-source market data, real-time news, decision dashboard, automated notifications, and cost-free scheduled runs.


dexter

https://github.com/virattt/dexter
An autonomous agent for deep financial research

===




|项目|和你的方向的相关度|最值得借鉴的地方|
|---|--:|---|
|**openInvest**|⭐⭐⭐⭐⭐|Personal knowledge、Markdown/YAML、decision engine、audit trail、Agent Skill|
|**DojoAgents**|⭐⭐⭐⭐|Personal investment Agent、Agent Loop、Skill/Plugin|
|**stock-analysis**|⭐⭐⭐⭐|Evidence-driven analysis、framework、thesis|
|**InvestAgent**|⭐⭐⭐|Skill orchestration、references、workflow|
|**FinRobot**|⭐⭐⭐|金融 Agent 的完整架构|
|LangAlpha / Agentic Analyst|⭐⭐|多 Agent / 自动金融研究|

---

## 1.  `openInvest`

[openInvest GitHub repository](https://github.com/longsizhuo/openInvest?utm_source=chatgpt.com)

这个项目让我觉得**和我们刚才讨论的架构有非常强的重合**。

它自己定义的是：

> self-hosted investment decision engine for AI agents

它有几个设计和你现在的想法特别接近：

### ① Markdown + YAML Frontmatter

它直接把：

> **Markdown-as-a-Database**

作为设计理念。

也就是：

```text
YAML Frontmatter
+
Markdown Body
```

作为知识和决策记录的 source of truth。([GitHub](https://github.com/longsizhuo/openInvest?utm_source=chatgpt.com "GitHub - longsizhuo/openInvest: Research-grade investment decision engine for AI agents: isolated multi-agent committee, auditable verdicts, backtests with lookahead protection, published negative results · GitHub"))


---

### ② 它把 Agent 和 Investment Engine 分开

它的设计理念是：

```text
Your Agent
    │
    │ user understanding
    ▼
OpenInvest
    │
    │ investment reasoning
    ▼
Decision
```

也就是说：

> Agent 负责理解用户、记忆、对话；Investment Engine 负责投资分析和可审计决策。

这和我们刚才讨论的：

```text
Goose
  ↓
Skill
  ↓
Personal Knowledge
  ↓
Decision
```

非常类似。([GitHub](https://github.com/longsizhuo/openInvest?utm_source=chatgpt.com "GitHub - longsizhuo/openInvest: Research-grade investment decision engine for AI agents: isolated multi-agent committee, auditable verdicts, backtests with lookahead protection, published negative results · GitHub"))

---

### ③ 它甚至有 Agent Skill

它提供给 Claude Code、Codex、Hermes、OpenClaw 等 Agent 使用的 skill/plugin。([GitHub](https://github.com/longsizhuo/openInvest?utm_source=chatgpt.com "GitHub - longsizhuo/openInvest: Research-grade investment decision engine for AI agents: isolated multi-agent committee, auditable verdicts, backtests with lookahead protection, published negative results · GitHub"))

所以如果你的目标是：

> **“用 Goose Skill 构建个人投资 Agent”**

这个项目非常值得直接研究。

---

### ④ 它特别强调 Audit Trail

它不是只输出：

> Buy / Sell

而是保留：

> 为什么得出这个结论？

以及完整的 decision trail。

这个其实非常适合你的设计。

因为你想要：

```text
Consideration 1
Consideration 2
Consideration 3
...
Overall assessment
```

而不是黑盒：

> Buy: 73%

---

## 2.  openInvest 

openInvest 更偏：

> **Investment Decision Engine**



openInvest 更强调：

```text
Agent
 ↓
Investment Engine
 ↓
Market data / analysis
 ↓
Decision
```



---

# 3.  DojoAgents

[DojoAgents GitHub repository](https://github.com/Alpha-Dojo/DojoAgents?utm_source=chatgpt.com)

它定位就是：

> Full-Market AI Copilot for Personal Investment

而且它明确采用 **Agent Loop**，并且有：

- CLI
    
- Web Dashboard
    
- Chat Gateway
    
- Agent Loop
    
- Tools
    
- Data
    
- Infrastructure
    

这样的分层。([GitHub](https://github.com/Alpha-Dojo/DojoAgents?utm_source=chatgpt.com "GitHub - Alpha-Dojo/DojoAgents: DojoAgents: Full-Market AI Copilot for Personal Investment · GitHub"))

它还支持：

> Writing Custom Plugins & Claude Skills

所以如果你想研究：

> **“一个 Personal Investment Agent 应该怎么和 Skill / Plugin / Tools 组合”**

它非常值得看。

不过它比你的 V1 **大很多**。

---

# 4.  stock-analysis

[stock-analysis GitHub repository](https://github.com/AdvancingTitans/stock-analysis?utm_source=chatgpt.com)

这个项目的一个核心理念和你特别接近：

> **Evidence-driven stock market analysis**

它不是简单让 LLM “发表意见”，而是：

```text
Question
 ↓
Research Scene
 ↓
Evidence
 ↓
Financial Framework
 ↓
Analysis
 ↓
Report
```

它甚至明确说：

> identify the research scene → obtain public evidence → validate evidence → apply appropriate framework → deliver view / risks / action conditions. ([GitHub](https://github.com/AdvancingTitans/stock-analysis?utm_source=chatgpt.com "GitHub - AdvancingTitans/stock-analysis: Evidence-driven stock market analysis CLI for A/HK/US/JP/KR stocks, funds, and portfolios. · GitHub"))



它是：

> **Evidence → Financial Framework**


这个区别其实非常大。

例如 stock-analysis 可能使用：

```text
Buffett framework
DCF
Peer comparison
Financial metrics
```



---

# 6. InvestAgent 
[InvestAgent GitHub repository](https://github.com/tohnee/investagent?utm_source=chatgpt.com)

它特别有意思的一点是，它本身就用了：

```text
SKILL.md
skills/
references/
scripts/
```

这样的结构。([GitHub](https://github.com/tohnee/investagent?utm_source=chatgpt.com "GitHub - tohnee/investagent: 全栈AI投研Agent · Your AI research co-pilot for smarter investment decisions. Five integrated research frameworks: Serenity industry-chain analysis, Buffett value-investing filter, UZI-Skill 22-dim deep analysis, TradingAgents multi-agent decision, QuantDinger quant backtest. · GitHub"))

所以从你现在正在设计的 Goose Skill 文件结构来说，它是一个很好的**工程结构参考**。

不过它主要是：

```text
多个投资框架
        ↓
多个 Agent / Skill
        ↓
自动研究
```

而不是你的：

```text
我的个人经验
        ↓
Knowledge Engineering
        ↓
Personal Knowledge
        ↓
一个 Personal Investment Skill
```

---

# 7. FinRobot 

[FinRobot GitHub repository](https://github.com/AI4Finance-Foundation/FinRobot?utm_source=chatgpt.com)

FinRobot 是一个比较成熟的开源 Financial AI Agent 平台，涉及：

- Financial AI Agents
    
- Market Forecasting
    
- Document Analysis
    
- Trading Strategies
    
- Quantitative Analytics
    
- Risk Assessment
    

等等。([GitHub](https://github.com/ai4finance-foundation/finrobot?utm_source=chatgpt.com "GitHub - AI4Finance-Foundation/FinRobot: FinRobot: An Open-Source AI Agent Platform for Financial Analysis using LLMs 🚀 🚀 🚀 · GitHub"))



它更适合以后你想研究：

> “如果把我的个人 Skill 最终发展成一个完整金融 AI platform，会是什么架构？”



---

# 8. 其实还有一个项目值得你特别注意

`stock-analysis-agent`：

[Stock Analysis Agent GitHub repository](https://github.com/lowtidebuild/stock-analysis-agent?utm_source=chatgpt.com)

它有一个我非常喜欢的设计：

> **Blank beats wrong.**

也就是：

> 如果数据无法验证，就不要编造。

而且它给每个数字附带 source / confidence grade，并强调：

```text
No Source → No Number
```

以及：

```text
event
 ↓
P&L impact
 ↓
stock price impact
```

的 causal risk chain。([GitHub](https://github.com/lowtidebuild/stock-analysis-agent?utm_source=chatgpt.com "GitHub - lowtidebuild/stock-analysis-agent: Institutional-grade stock research for US and Korean equities — delivered in minutes. · GitHub"))

这个思想以后你可以直接吸收到你的 Skill 里。

---


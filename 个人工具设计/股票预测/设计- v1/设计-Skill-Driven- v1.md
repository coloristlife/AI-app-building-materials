

> **第一版可以不引入“RAG Framework”，但不能没有 Retrieval。**

第一版完全可以用 **Skill + 文件系统/YAML + 简单的搜索/过滤** 来实现。等你的 Intelligence、Personal Context、Historical Analysis 累积到一定规模，再把 Retrieval 升级成 Embedding / Hybrid Search / RAG。

这样做反而更符合你现在这个项目的实际需求，因为第一版真正需要验证的不是“RAG 能不能搜得准”，而是：

> **Personal Investment Context 能不能真正驱动 AI 去观察正确的信息，并最终改善投资分析。**

下面我基于我们今天讨论的全部内容，重新整理成一个比较完整的 **Design v1.0**。这次我不采用那种“1、2、3、4”的提纲式写法，而是按照真正产品设计文档的方式来写。

---

# Personal Investment Intelligence System

## Design v1.0

### —— A Skill-Driven Personal Investment Reasoning System

---

## 一、设计目标

这个系统并不是一个传统意义上的股票预测模型，也不是简单地把大量金融数据交给大语言模型，让模型自行预测股票涨跌。

它的核心思想是：

> **把一个人的投资经验、投资思维和长期积累的判断方式，转化为 AI 可以理解和调用的 Personal Investment Context，让 AI 在面对新的市场环境时，能够按照这个人的思维方式主动寻找和理解相关信息，再进行投资分析。**

因此，这个系统最重要的不是让 AI “知道更多金融知识”，而是让 AI：

> **知道在什么情况下应该观察什么，以及应该用什么样的思维去理解这些信息。**

例如，一个人的投资经验是：

> “高位不讲故事，低位不看业绩。”

这个经验本身并不是一个传统的量化交易 Rule。

它真正表达的是一种观察市场的方法：

当股票处于高位时，需要警惕市场叙事、过度乐观和预期透支；当股票处于低位时，不能仅仅因为当前业绩不好就否定未来机会。

因此，AI 在分析一只股票之前，不应该简单地检索这句话，而应该首先理解：

> **为了判断这条经验是否适用于当前市场环境，我需要观察哪些信息？**

这就是整个系统设计的核心。

---

# 二、系统的核心思想：Skill First，而不是 RAG First

第一版系统不需要以 RAG 为核心。

系统首先采用 **Skill-Driven Architecture**。

Skill 代表：

> **AI 完成某类任务时应该采用什么工作流程、使用什么信息、产生什么结果。**

例如：

- Intelligence Requirement Skill
    
- Intelligence Extraction Skill
    
- Personal Context Skill
    
- Investment Analysis Skill
    
- Prediction Skill
    
- Prediction Evaluation Skill
    

这些 Skill 共同构成 AI 的投资分析方法。

而长期保存的数据，则使用：

> **Obsidian + Markdown + YAML**

作为主要知识和历史数据载体。

因此第一版的基本关系是：

```text
Skill = AI 应该怎么工作

YAML / Markdown = AI 可以记住什么

Simple Retrieval = AI 当前需要读取什么

LLM = AI 的推理能力
```

第一版不需要马上引入 Vector Database、Embedding、RAG Pipeline 等复杂基础设施。

当数据量逐渐增长以后，再将 Simple Retrieval 升级成 Hybrid Retrieval / Semantic Search / RAG。

---

# 三、系统真正要解决的问题

这个系统需要解决的并不是：

> “如何让 AI 获取尽可能多的市场信息？”

而是：

> **“如何让 AI 获取与当前个人投资思维真正相关的信息，同时又避免个人经验限制 AI 对未知信息的观察？”**

因此系统采用两条 Intelligence Pipeline。

一条是 **Targeted Intelligence**，由 Personal Context 反向驱动。

另一条是 **Open Intelligence**，用于发现个人投资框架之外的重要变化。

最终形成：

```text
                  Personal Context
                         │
                         ▼
              Information Requirements
                         │
                         ▼
                 Targeted Intelligence
                         │
                         │
External World ──────────┤
                         │
                         ▼
                   Intelligence
                         │
                         ▼
                    Signals
                         │
                         ▼
              Personal Context Matching
                         │
                         ▼
                     Analysis
```

与此同时：

```text
External World
      │
      ▼
Open Intelligence
      │
      ▼
Unexpected / New Signals
      │
      ▼
Investment Analysis
```

两条路径最后汇合。

---

# 四、Personal Context 不再只是 Rule

第一版虽然可以继续使用 `Personal Rule` 这个 Data Object，但在产品概念上，我建议把它放在一个更大的概念下面：

> **Personal Investment Context**

因为一个人的投资方法并不一定全部都是 Rule。

它可能包括：

- 投资原则
    
- 投资经验
    
- 投资口诀
    
- 市场观察
    
- 心理偏好
    
- 历史教训
    
- 反复验证形成的判断方式
    

例如：

> “恐慌时拿先手，贪婪时给筹码。”

更像投资经验。

而：

> “高位不讲故事，低位不看业绩。”

更像一种市场观察框架。

所以 Personal Context 是总概念，`Personal Rule` 只是其中一种数据类型。

---

# 五、Personal Context 的真正价值是反向定义 Information Requirements

这是整个 v1.0 最大的设计变化。

以前的思路是：

```text
External Intelligence
        ↓
Extract everything
        ↓
Search Personal Rules
```

现在改成：

```text
Personal Context
        ↓
Information Requirements
        ↓
告诉 AI 应该观察什么
        ↓
External Intelligence
        ↓
Signals
        ↓
判断哪些 Personal Context 被激活
```

例如：

```text
Personal Context

高位不讲故事，低位不看业绩
```

AI 可以推导出：

```text
Information Requirements

Price Position
Market Sentiment
Market Expectation
Market Narrative
Valuation
Recent Performance
```

于是系统才会主动寻找：

- 当前股价处于什么历史位置
    
- 市场情绪如何
    
- 市场一致预期如何
    
- 当前市场正在讲什么故事
    
- 当前估值处于什么水平
    
- 最近价格表现如何
    

这比单纯搜索“高位不讲故事”有效得多。

---

# 六、Information Requirement 是连接个人经验和外部世界的桥梁

因此在第一版 Data Model 中，我建议正式增加：

```text
Information Requirement
```

它回答的问题是：

> **为了使用某一条 Personal Context，AI 需要知道什么？**

例如：

```yaml
---
type: information_requirement
id: IR-001

name: Price Position

purpose: >
  判断当前股票是否处于明显的高位或低位。

related_context:
  - PR-001

information_type:
  - market_data
  - historical_price

priority: high

tags:
  - price
  - position
---
```

它不应该是复杂的金融指标定义。

第一版只需要自然语言描述。

---

# 七、Personal Context 应该同时拥有 Targeted Requirements 和 Open Requirements

这里就是我们刚才讨论的第二个非常重要的概念。

如果完全根据 Personal Context 决定收集信息，会出现确认偏误。

例如：

> “高位不讲故事。”

如果系统只寻找：

> 泡沫、过度乐观、市场情绪高涨……

那么它可能忽略：

> 公司技术发生根本性突破。

因此 Personal Context 应该同时定义两类信息需求。

### Targeted Requirements

这些是：

> **为了验证和应用我的个人投资经验，我明确需要观察的信息。**

例如：

```text
Price Position
Market Sentiment
Market Expectations
Valuation
Narrative
```

### Open Requirements

这些是：

> **即使与当前 Personal Context 没有明显关系，也可能改变最终判断的重要信息。**

例如：

```text
Unexpected Company Event
Regulatory Change
Major Technology Breakthrough
Competitive Disruption
Management Change
Macroeconomic Shock
Black Swan Event
```

所以最终的信息采集应该是：

```text
Targeted Intelligence
        +
Open Intelligence
```

而不是只收集 Personal Context 需要的信息。

---

# 八、External Intelligence 不再是一个“大杂烩”

第一版 External Intelligence 可以来自：

- 新闻
    
- 公司公告
    
- 财报
    
- 政策
    
- 技术进展
    
- 行业报告
    
- 市场数据
    
- 分析师观点
    
- 用户主动提供的信息
    

这些信息首先进入：

> **Source**

Source 是原始证据。

然后通过：

> **Intelligence Extraction Skill**

生成结构化 Intelligence。

---

# 九、Intelligence Extraction Skill

这个 Skill 的职责不是预测股票。

它只负责：

> **把原始信息转换成 AI 后续分析需要的结构化 Intelligence。**

第一版可以提取：

```text
Facts
Events
Signals
Sentiment
Expectations
```

例如：

```yaml
---
type: intelligence
id: INT-20260813-001

sources:
  - SRC-20260813-001

entities:
  - ENT-NVDA

facts:
  - NVIDIA发布新的AI GPU

events:
  - 新产品发布

sentiment:
  - 市场情绪偏乐观

expectations:
  - 市场对未来增长预期较高

signals:
  - AI基础设施需求持续
  - AI芯片竞争加剧

status: active
---
```

这里特别强调：

> **Intelligence Extraction Skill 不负责回答“股票应该涨还是跌”。**

它只负责理解外部世界。

---

# 十、Market Signal 是 Intelligence 和 Personal Context 之间的接口

Market Signal 是：

> **当前市场环境中值得进一步关注的状态。**

例如：

```text
AI infrastructure demand remains strong
Market expectations are elevated
Investor sentiment is highly optimistic
Stock price is near historical high
```

它不是个人经验。

也不是最终投资结论。

它只是：

> **当前世界正在发生什么。**

然后系统利用这些 Signal 去寻找：

> 哪些 Personal Context 现在相关？

---

# 十一、Personal Context Retrieval 第一版不需要 RAG

这是我们现在需要明确的一点。

第一版可以直接：

```text
Market Signals
       ↓
Keyword / Metadata / Simple Semantic Matching
       ↓
Personal Context
```

例如：

```text
Signal:
Market sentiment is highly optimistic

↓

Personal Context:
高位不讲故事

Personal Context:
贪婪时给筹码
```

第一版甚至可以直接使用：

- YAML metadata
    
- tags
    
- topics
    
- relevant_signals
    
- information_requirements
    
- 简单文本搜索
    

不需要：

- Vector DB
    
- Embedding pipeline
    
- RAG framework
    

---

# 十二、什么时候才需要 RAG？

当你的 Personal Context 开始积累到：

```text
100+
500+
1000+
```

甚至：

```text
Historical Intelligence
10,000+
Analysis
5,000+
```

以后，仅靠文本搜索就开始变得困难。

这时候再加入：

```text
Embedding
+
Semantic Search
+
Keyword Search
+
Reranking
```

最终形成：

> Hybrid Retrieval / RAG

所以 RAG 在这个系统里应该是：

> **随着知识规模增长而引入的基础设施升级，而不是第一版的核心设计。**

---

# 十三、Entity 是整个数据模型的基础锚点

系统需要一个统一的 Entity。

例如：

```text
NVIDIA
NVDA
NVIDIA Corporation
英伟达
```

都对应：

```yaml
---
type: entity
id: ENT-NVDA

name: NVIDIA

entity_type: company

symbol: NVDA

aliases:
  - NVIDIA Corporation
  - 英伟达
---
```

Entity 可以代表：

- 公司
    
- 股票
    
- 行业
    
- 技术
    
- 政策
    
- 宏观因素
    
- 市场
    

其他对象通过 Entity 建立关系。

---

# 十四、第一版核心 Data Objects

经过今天的讨论，我建议最终暂时固定为：

```text
Entity
Source
Intelligence
Market Signal
Personal Context
Information Requirement
Analysis
Prediction
Outcome
```

其中：

**Entity** 是世界对象。

**Source** 是原始证据。

**Intelligence** 是 AI 对证据的理解。

**Market Signal** 是当前市场状态。

**Personal Context** 是个人投资思维。

**Information Requirement** 是个人经验告诉 AI“应该观察什么”。

**Analysis** 是一次完整的投资推理。

**Prediction** 是具体预测。

**Outcome** 是最终现实结果。

---

# 十五、完整的分析流程

用户提出：

> “分析 NVIDIA 未来一个月的走势。”

系统首先识别：

```text
Target Entity
      ↓
ENT-NVDA
```

然后加载与当前任务相关的 Personal Context。

不是把所有 Personal Context 都塞进去。

系统根据 Personal Context 得到：

```text
Information Requirements
```

例如：

```text
Price Position
Market Sentiment
Market Expectations
Valuation
AI Demand
Competition
```

然后通过 Targeted Intelligence Pipeline 获取这些信息。

与此同时，Open Intelligence Pipeline 搜索：

```text
Unexpected Events
Regulation
Technology Changes
Competitive Disruption
Macro Events
```

然后生成：

```text
Intelligence
      ↓
Market Signals
```

再根据 Market Signals 找到真正相关的 Personal Context。

例如：

```text
Market Signal:
股价处于历史高位
市场情绪高度乐观
AI叙事极强

↓

Relevant Personal Context:

高位不讲故事

贪婪时给筹码
```

最后才进入：

```text
Investment Analysis Skill
```

---

# 十六、Investment Analysis Skill

这个 Skill 才负责最终推理。

它接收：

```text
Target Entity

Relevant Intelligence

Market Signals

Relevant Personal Context

Historical Intelligence

Historical Analysis

Open Intelligence
```

然后要求 AI：

> **不要简单地机械执行 Personal Rule，而是把它作为投资判断框架的一部分。**

最终输出：

```text
Current Situation

Important Signals

Relevant Personal Context

Analysis

Counter Evidence

Risk Factors

Prediction

What Would Change This View
```

特别需要保留：

> **Counter Evidence**

这是防止系统变成“个人投资经验回音室”的重要机制。

---

# 十七、Prediction 不应该只是“涨/跌”

第一版可以简单：

```text
Bullish
Neutral
Bearish
```

同时保存：

```text
Prediction Horizon
Prediction Date
Key Reasons
Key Signals
Personal Context Used
Risk Factors
```

这样以后才能验证。

---

# 十八、Outcome 是这个系统真正形成闭环的地方

Prediction 不能停在：

> “AI 预测上涨。”

系统必须在未来自动或人工记录：

```text
Actual Outcome
```

然后比较：

```text
Prediction
vs.
Reality
```

最终可以回答：

> 哪些 Personal Context 经常有效？

> 哪些只在某些 Market Conditions 下有效？

> 哪些经验长期没有得到验证？

> 哪些新的经验正在形成？

这才是 Personal Investment Intelligence System 与普通股票 Chatbot 最大的区别。

---

# 十九、Personal Context 会不断进化

长期运行以后：

```text
Personal Context
       ↓
Information Requirements
       ↓
Intelligence
       ↓
Signals
       ↓
Analysis
       ↓
Prediction
       ↓
Outcome
       ↓
Validation
       ↓
Personal Context Evolution
```

例如：

原来的经验：

> 高位不讲故事。

经过 50 次历史验证以后，可能发现：

> 只有当市场情绪极度乐观 + 估值明显偏高 + 盈利预期已经充分 Price-in 时，这条经验才比较有效。

那么 AI 可以提出：

> “是否需要更新 Personal Context？”

**注意这里第一版仍然不应该让 AI 自动修改用户的投资原则。**

应该：

```text
AI proposes
      ↓
User reviews
      ↓
User approves
      ↓
Personal Context updated
```

这样才能真正保持“个人投资方法”的主人是用户，而不是 AI。

---

# 二十、Skill Architecture

最终 Skill 可以设计成：

```text
skills/

intelligence-requirement/
    SKILL.md

intelligence-acquisition/
    SKILL.md

intelligence-extraction/
    SKILL.md

signal-analysis/
    SKILL.md

personal-context/
    SKILL.md

investment-analysis/
    SKILL.md

prediction/
    SKILL.md

prediction-evaluation/
    SKILL.md

personal-context-evolution/
    SKILL.md
```

其中最关键的新 Skill 是：

> **Intelligence Requirement Skill**

它负责：

```text
Personal Context
       ↓
What should we observe?
       ↓
Information Requirements
```

这就是你刚才提出的核心思想。

---

# 二十一、第一版 Runtime 不需要非常复杂

第一版甚至不需要完整 Agent Framework。

基本流程：

```text
User Query
     ↓
Load Investment Analysis Skill
     ↓
Identify Entity
     ↓
Load Personal Context
     ↓
Generate Information Requirements
     ↓
Collect Intelligence
     ↓
Extract Signals
     ↓
Skill-directed Retrieve Relevant Context
     ↓
Analyze
     ↓
Predict
     ↓
Save YAML/Markdown
```

因此第一版完全可以使用：

```text
Python
+
LLM API
+
Skill Markdown
+
YAML Parser
+
Obsidian Vault
+
Simple Search
```

等以后规模扩大：

```text
Simple Search
      ↓
Hybrid Search
      ↓
Vector Search
      ↓
RAG
```

这是渐进式架构，而不是一开始就把所有技术堆进去。


因为 Skill **决定检索策略和目标**，但真正执行检索的仍然可以是一个独立的 Retrieval Layer。

例如：

```
              Investment Analysis Skill
                         │
                         │
                "我需要什么？"
                         ↓
                  Retrieval Plan
                         │
                         ↓
                Simple Retrieval
                         │
              ┌──────────┼──────────┐
              ↓          ↓          ↓
            Entity     YAML       Files
              ↓          ↓          ↓
            NVDA      Signals    Analysis
```

这样以后你升级 RAG 时，不需要修改 Skill。

**第一版先不要为了“Semantic Search”而引入 Vector 技术。**

让 Skill 根据 `Information Requirement → Entity → Type → Tag → Date → Status` 去做**确定性的结构化检索**。

等真实运行以后，我们再观察一个非常具体的指标：

> **“有多少次 Skill 明确知道需要某类 Personal Context，但 Structured Retrieval 找不到真正相关的 Context？”**

如果这个问题开始频繁出现，那就是引入 Semantic Search 的真正理由，而不是因为“AI 系统就应该有 RAG”。

---

# 二十二、最终的系统形态

我认为经过今天的讨论，你这个项目最准确的定义已经不是：

> **AI Stock Prediction Platform**

而应该更接近：

> **Personal Investment Intelligence & Reasoning System**

它不是单纯预测股票。

它建立的是：

```text
                 Personal Experience
                         │
                         ▼
                 Personal Context
                         │
                         ▼
              Information Requirements
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
      Targeted Intelligence    Open Intelligence
             │                       │
             └───────────┬───────────┘
                         ▼
                  Intelligence
                         │
                         ▼
                    Market Signal
                         │
                         ▼
             Relevant Personal Context
                         │
                         ▼
                  AI Reasoning
                         │
                         ▼
                    Prediction
                         │
                         ▼
                     Outcome
                         │
                         ▼
                  Experience Validation
                         │
                         ▼
                Personal Context Evolution
```

这条链，我认为现在已经比我们最开始讨论的 **“RAG + Rule + Memory + LLM”** 清晰很多。

**第一版的核心不是 RAG，也不是 Rule Engine。**

而是：

> **Skill 驱动的个人投资推理流程 + Obsidian/YAML 长期知识与历史记录 + Personal Context 驱动的信息需求 + Open Intelligence 防止认知盲区。**

等这个闭环真正跑起来以后，再根据数据规模决定什么时候引入 RAG、Vector Database、Graph、更加复杂的 Agent Runtime 等技术。

这也给下一阶段留下了一个非常明确的工作：**先把 Personal Context → Information Requirement → Intelligence Extraction 这一条链定义好。** 因为它决定了你的 AI 到底“看什么”，而“看什么”很可能比后面的“怎么分析”更加重要。
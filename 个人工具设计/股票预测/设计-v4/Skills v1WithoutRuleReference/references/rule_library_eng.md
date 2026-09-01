# Investment Rule Library — Reference Data

This file is the source of truth for the investment-rule-router skill. It contains:

1. Situation Tag Vocabulary
2. Rule Index (trigger tags per rule, for matching)
3. Canonical Input Schema (deduplicated required-input fields)
4. Conflict Matrix (known pairs of rules whose actions can contradict)
5. Per-Rule Evaluation Logic (compact IF/THEN, status, action, limitations)
6. Source Instructions for Rule Extraction (for adding new rules to this library)

Rule numbering matches the order the rules were originally authored in. Sub-letters (A/B/C)
mark rules that were split out of one user-provided experience because they had independent
trigger conditions and/or opposite actions.

---

## 1. Situation Tag Vocabulary

| Dimension | Values |
|---|---|
| price_position | 高位 / 低位 / 中位 / 未知 |
| volume | 放量 / 缩量 / 平量 |
| price_speed | 急跌 / 缓跌 / 急涨 / 平稳 |
| pattern | 横盘(前) / 三连阴 / 十字星×3 / 新低 / 新高 / 破位 / 回踩不破 / 冲高 / 滞涨 |
| timing | 早盘 / 尾盘 / 盘中 |
| trend_stage | 下跌初期 / 下跌途中 / 上涨途中 / 未知 |
| sentiment | 恐慌 / 贪婪 / 人声鼎沸 / 中性 |
| news | 利好公告 / 利空 / 无消息 |
| ma250 | 走平 / 向下 / 拐头向上 / 未知 |
| stock_type | 热门题材股 / 非题材股 / 未知 |
| account_state | 已止损 / 连续两笔止损 / 有浮盈 / 浮盈回吐 / 已解套 / 已止盈 / 新建仓 / 无仓位 |

Tag extraction should be liberal — a single user sentence commonly hits 3–5 dimensions.
Missing dimensions stay 未知/blank; do not force a tag that isn't actually implied.

---

## 2. Rule Index (matching table)

| ID   | Rule Name (中文)  | Trigger Tags (AND unless noted OR)                          |
| ---- | --------------- | ----------------------------------------------------------- |
| R1   | 逆向乖离法则（买阴卖阳）    | timing∈{早盘,尾盘} + price_speed∈{急跌,急涨}                        |
| R2   | 趋势锚定法则（年线定生死）   | ma250∈{走平,向下,拐头向上} [+ pattern=回踩不破 optional for buy branch] |
| R3-A | 高位放量下跌减仓        | price_position=高位 + volume=放量 + price_speed=下跌方向            |
| R3-B | 低位缩量新低试仓        | price_position=低位 + volume=缩量 + pattern=新低                  |
| R3-C | 增量回升右侧确认重仓      | pattern=放量上涨(前) + pattern=回踩不破(次日)                          |
| R4-A | 高位横盘冲高止盈（多头陷阱）  | price_position=高位 + pattern=横盘(前) + pattern=冲高              |
| R4-B | 低位横盘破低低吸（空头陷阱）  | price_position=低位 + pattern=横盘(前) + pattern=新低              |
| R5-A | 下跌初期三连阴禁止抄底     | trend_stage=下跌初期 + pattern=三连阴                              |
| R5-B | 下跌途中三颗星中继观望     | trend_stage=下跌途中 + pattern=十字星×3                            |
| R6-A | 缩量缓跌弱弹性做T       | price_speed=缓跌 + volume=缩量                                  |
| R6-B | 放量急跌强弹性低吸       | price_speed=急跌/加速 + volume=放量                               |
| R7-A | 利好兑现放量滞涨清仓      | (news=利好公告 OR sentiment=人声鼎沸) + volume=放量 + pattern=滞涨      |
| R7-B | 热门题材股短线情绪套利     | stock_type=热门题材股                                            |
| R8-A | 等仓出击（仓位恒定纪律）    | account_state=新建仓 (evaluate on every new position sizing)   |
| R8-B | 连续止损熔断暂停        | account_state=连续两笔止损                                        |
| R8-C | 止损铁律（逻辑失效/2%上限） | pattern=破位 OR sector_state=退潮 OR account_state亏损达2%         |
| R9   | 贪婪恐惧法则（逆向情绪）    | sentiment∈{贪婪,恐惧}（市场整体，非仅个股）                                |
| R10  | 本金优先保护法则        | account_state∈{有浮盈,浮盈回吐} + 价格逼近本金线                          |
| R11  | 卖出后情绪稳定法则（卖飞后悔） | account_state∈{已解套,已止盈} + price_speed=急涨(卖出后)               |
| R12  | 位置反向评判法则（故事/业绩） | (price_position=高位 + 存在故事叙事) OR (price_position=低位 + 业绩不佳)  |
| R13  | 显而易见法则（元原则）     | 无可操作标签 — 从不自动匹配，仅在用户明确要求复盘/元认知检查时手动调用                       |

Note: multiple rules regularly co-fire from one sentence. Always return the full candidate
list, not a single top match — see SKILL.md Step 2.

---

## 3. Canonical Input Schema (deduplicated fields)

Resolve each field once per conversation turn, then reuse across all matched rules.

| Field ID | Description | Evidence Source | Used by |
|---|---|---|---|
| `price_position` | 当前价格所处位置(高位/低位/中位) | DERIVED | R2,R3-A,R3-B,R4-A,R4-B,R12 |
| `volume_state` | 成交量相对均量(放量/缩量/平量) | MARKET_DATA→DERIVED | R3-A,R3-B,R3-C,R6-A,R6-B,R7-A |
| `price_speed` | 价格变动速度(急跌/缓跌/急涨) | DERIVED | R1,R6-A,R6-B |
| `consolidation` | 此前是否横盘及区间/时长 | DERIVED | R4-A,R4-B |
| `candle_pattern` | 近期K线形态(三连阴/十字星/阴阳线) | MARKET_DATA | R1,R5-A,R5-B |
| `trend_stage` | 下跌初期/途中判断 | USER_CONFIRMATION | R5-A,R5-B |
| `ma250_trend` | 年线形态及斜率 | DERIVED | R2 |
| `retest_result` | 次日回踩是否破位 | MARKET_DATA | R3-C |
| `has_good_news` | 是否存在利好公告 | NEWS_DATA | R7-A |
| `market_sentiment` | 情绪状态(贪婪/恐惧/人声鼎沸) | USER_CONFIRMATION/NEWS_DATA | R1,R7-A,R9 |
| `is_hot_theme_stock` | 是否为热门题材股 | USER_CONFIRMATION/NEWS_DATA | R7-B |
| `narrative_present` | 是否存在故事/题材叙事支撑 | NEWS_DATA/USER_CONFIRMATION | R12 |
| `earnings_state` | 当前业绩表现好坏 | NEWS_DATA | R12 |
| `sector_state` | 板块/题材是否退潮 | NEWS_DATA/USER_CONFIRMATION | R7-B,R8-C |
| `current_position` | 是否持仓/持仓比例 | USER_PROVIDED/USER_CONFIRMATION | R3-A,R3-C,R8-A,R8-C,R10,多数动作类 |
| `entry_cost` | 买入成本/本金 | USER_PROVIDED | R8-C,R10 |
| `original_thesis` | 原始买入逻辑 | USER_PROVIDED | R8-C |
| `max_floating_profit` | 曾达到的最高浮盈 | USER_PROVIDED/USER_CONFIRMATION | R10 |
| `recent_trade_results` | 最近交易结果序列(止损/止盈) | USER_PROVIDED/USER_CONFIRMATION | R8-B |
| `total_capital` | 总资金规模 | USER_PROVIDED | R8-A,R8-C |
| `standard_position_size` | 用户设定的标准单笔仓位 | USER_PROVIDED | R8-A |
| `intended_position_size` | 本次拟建仓仓位 | USER_PROVIDED | R8-A |
| `sell_reason` | 该笔卖出原因(解套/止盈/止损) | USER_PROVIDED | R11 |
| `post_sell_price_move` | 卖出后价格走势 | MARKET_DATA | R11 |

Resolution priority (always in this order): user already stated it → tool-retrievable
(MARKET_DATA/NEWS_DATA/DERIVED) → USER_CONTEXT/USER_CONFIRMATION batched question → mark
UNKNOWN if non-essential.

---

## 4. Conflict Matrix

| Rule A | Rule B | Nature of conflict | Default resolution |
|---|---|---|---|
| R3-B (低位缩量试仓) | R6-B (放量急跌低吸) | 同为低位/下跌场景，但一个要求缩量、一个要求放量，互斥，需先确认量能方向 | 以实际 volume_state 为准，二者不会同时 TRIGGERED；若用户描述模糊，先追问 |
| R5-A (三连阴禁止抄底) | R3-B / R6-B (试仓/低吸) | 阶段判断不同（下跌初期 vs 低位/恐慌尾声），动作相反 | 需 trend_stage 澄清；未澄清时不给出行动指令，仅并列展示两种可能 |
| R2 (熊市只做超跌反弹) | R4-B (低位破位低吸/黄金坑) | 熊市格局下的破位到底是继续探底还是黄金坑，仓位重量建议不同 | 结合 ma250_trend：若走平/向下，R2 的"仅超跌反弹、不做格局"限制 R4-B 的仓位规模上限 |
| R3-A (高位放量下跌减仓) | R6-B (放量急跌低吸) | 高位放量急跌同时满足两者表面条件，性质不同（派发 vs 恐慌） | 以 price_position 为主要区分依据：高位→倾向 R3-A；非高位的急跌→倾向 R6-B |
| 任意信号类规则 (R1,R2,R3,R4,R5,R6,R7,R9,R12) | R8-B / R8-C (账户纪律类) | 纪律类规则的性质是"一票否决" | **默认纪律类规则优先**：先提示暂停/离场/控制仓位，再把信号类结论作为背景信息呈现 |

---

## 5. Per-Rule Evaluation Logic (compact)

Format per rule: Trigger → Status/Action → key Limitation to always carry into output.

**R1 逆向乖离法则**
IF 早盘+急跌 → 解读:恐慌 → 动作: HOLD(不割肉)
IF 尾盘+急拉 → 解读:贪婪 → 动作: AVOID(不追高)
Limitation: 不判断趋势方向，仅识别情绪化定价窗口；重大基本面消息驱动时可能失效。

**R2 趋势锚定法则**
IF ma250=走平/向下 → 动作: 仅超跌反弹，不做格局
IF ma250=拐头向上 AND retest_result=回踩不破 → 动作: BUY/SCALE IN(中线)
IF ma250=拐头向上 AND 未回踩 → 动作: WAIT
Limitation: 不保证回踩后必然反弹；数据不足250日无法计算。

**R3-A 高位放量下跌减仓**
IF 高位+放量+下跌+持仓 → 动作: REDUCE
Limitation: 不预测跌幅；可能是情绪性抛售而非机构出逃。

**R3-B 低位缩量新低试仓**
IF 低位+缩量+新低 → 动作: SCALE IN(小仓位，左侧)
Limitation: 不确认底部；流动性枯竭型缩量需排除。

**R3-C 增量回升右侧确认重仓**
IF 放量上涨(前)+次日回踩不破 → 动作: BUY/SCALE IN(较大仓位)
IF 回踩破位 → 动作: WAIT
Limitation: 不保证趋势延续；与R3-A在特定阶段可能冲突。

**R4-A 高位横盘冲高止盈（多头陷阱）**
IF 高位+横盘(前)+冲高 → 动作: EXIT(止盈)
Limitation: 未结合成交量无法完全区分真突破/假突破。

**R4-B 低位横盘破低低吸（空头陷阱）**
IF 低位+横盘(前)+新低 → 动作: SCALE IN(分批)
Limitation: 不保证反弹；与R2熊市判断可能冲突。

**R5-A 下跌初期三连阴禁止抄底**
IF trend_stage=下跌初期 + 三连阴 → 动作: AVOID(严禁抄底)
Limitation: "下跌初期"判定标准依赖用户主观确认。

**R5-B 下跌途中三颗星中继观望**
IF trend_stage=下跌途中 + 十字星×3 → 动作: WAIT(空仓)
Limitation: 不确认何时终结；可能与右侧确认类规则冲突。

**R6-A 缩量缓跌弱弹性做T**
IF 缓跌+缩量 → 动作: 仅做T
Limitation: 不预测下跌何时结束；牛熊背景下含义可能不同。

**R6-B 放量急跌强弹性低吸**
IF 急跌/加速+放量(恐慌盘) → 动作: BUY/SCALE IN(敢于低吸)
Limitation: 重大基本面利空驱动时弹性逻辑可能不适用；与R5-A可能冲突。

**R7-A 利好兑现放量滞涨清仓**
IF (利好公告 OR 人声鼎沸)+放量+滞涨+持仓 → 动作: EXIT(清仓)
Limitation: "人声鼎沸"难以独立量化判断。

**R7-B 热门题材股短线情绪套利**
IF stock_type=热门题材股 → 动作: AVOID(长期持有)，仅短线
Limitation: 不评估基本面价值；分类标准依赖用户/舆情判断。

**R8-A 等仓出击**
IF intended_position_size ≠ standard_position_size (尤其亏后加仓/赚后减仓) → 动作: PAUSE，纠正仓位
Limitation: 仅能提示，不能强制执行。

**R8-B 连续止损熔断**
IF recent_trade_results=最近两笔均止损 → 动作: PAUSE(暂停交易)
Limitation: "连续"口径及暂停时长用户未定义。

**R8-C 止损铁律**
IF 逻辑失效(破位/退潮) OR 亏损≥总资金2% → 动作: EXIT(无条件离场)
Limitation: 高度依赖用户对原始买入逻辑的如实反馈。

**R9 贪婪恐惧法则**
IF market_sentiment=明显贪婪 → 动作: AVOID/REDUCE
IF market_sentiment=明显恐惧 → 动作: BUY/SCALE IN
Limitation: 情绪判断难以独立量化，依赖用户/舆情。

**R10 本金优先保护法则**
IF 曾有浮盈+浮盈回吐+价格逼近本金线 → 动作: EXIT/REDUCE(保本金)
Limitation: "逼近本金"阈值未定义；不涉及从未有浮盈的情形(该情形走R8-C)。

**R11 卖出后情绪稳定法则**
IF sell_reason∈{解套,止盈}+卖出后价格继续涨+用户表现后悔/冲动 → 动作: PAUSE(稳心态，暂缓追高)
Limitation: 无法独立识别用户情绪，需用户主动表达。

**R12 位置反向评判法则**
IF 高位+存在故事 → 动作: AVOID(警惕故事，弱化权重)
IF 低位+业绩不佳 → 动作: INFORMATIONAL(弱化业绩权重，综合判断)
Limitation: 不代表完全否定故事/业绩，仅权重调整。

**R13 显而易见法则**（不参与自动路由，仅按需手动调用）
无 IF/THEN 结构；仅作为复盘提示："这个机会是否因为太简单/太常见而被低估？"

---

## 6. Source Instructions for Rule Extraction (for adding new rules)

When the user provides a brand-new personal experience and wants it added to this library,
follow the original 7-part Rule Contract (Purpose / Applicability / Required Inputs / Evidence
Source / Evaluation / Output / Limitations), preserving the user's original meaning, labeling
any AI Interpretation explicitly, and splitting into multiple sub-rules whenever the source
experience contains independent trigger conditions and/or opposite actions (as was done for
rules 3, 4, 5, 6, 7, 8 above). After drafting the full rule, add a compact entry to:

- Section 2 (Rule Index) — trigger tags
- Section 3 (Canonical Input Schema) — any new field IDs, merging with existing fields where
  the concept already exists (e.g. don't create a second "价格位置" field under a different
  name)
- Section 5 (Evaluation Logic) — the compact IF/THEN form
- Section 4 (Conflict Matrix) — check whether the new rule's action contradicts any existing
  TRIGGERED-rule action under overlapping tags, and record it if so

Confirm the new entry with the user before treating it as part of the routable library.
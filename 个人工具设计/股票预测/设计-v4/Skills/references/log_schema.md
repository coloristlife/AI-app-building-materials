# 决策日志结构说明（用于人工审核与法则改进）

本文件定义每次使用 investment-rule-router 技能后，需要生成并追加保存的一条日志记录的完整结构。目的是让用户/审核者事后能够：① 复核当时的标签判断是否正确；② 复核法则匹配和评估逻辑是否合理；③ 积累足够样本用于后续修改法则库 `rule_library.md` 或各条法则原文。

## 一、文件与存储方式

- 日志文件名固定为 `decision_log.jsonl`，一行一条 JSON 记录（JSON Lines 格式），方便追加和后续用脚本/表格工具批量分析。
- 每次会话开始使用本技能时，先检查 `/mnt/user-data/uploads/` 下是否存在用户重新上传的  `decision_log.jsonl`（说明用户在延续此前的记录）。若存在，读取并在其基础上追加新记录；
  若不存在，从空文件开始。
- 每次给出最终结论后，把追加了新记录的完整 `decision_log.jsonl` 写入
  `/mnt/user-data/outputs/`，并通过 present_files 呈现给用户，同时提醒用户："请保留这个文件，下次需要延续记录时重新上传它"。
- 另外同步生成一份人类可读的摘要 `decision_log_summary.md`（每条记录一个小节，用于人工快速浏览，不需要逐行解析 JSON），同样输出并呈现。

## 二、单条日志记录的 JSON 结构

```json
{
  "log_id": "自增或时间戳生成的唯一ID，如 20260825-153000",
  "record_time": "记录写入时的完整时间戳，含时区",
  "user_query_raw": "用户原始输入的完整文字",
  "identified_ticker": "识别出的标的名称/代码，若未指明标的则为 null",

  "situation_tags": {
    "<字段ID，如 price_position>": {
      "value": "已核实的取值，如 低位 / 放量 / 走平，若未知则为 null",
      "status": "已核实 | 未知",
      "evidence": "支持该取值的具体依据摘要（如搜索到的哪条数据/新闻，或用户的哪句话）；
                    status=未知时此字段为 null",
      "evidence_source_type": "MARKET_DATA | NEWS_DATA | DERIVED | USER_PROVIDED |
                                USER_CONFIRMATION",
      "evidence_date": "该依据对应的日期（如行情数据的交易日、新闻发布日期）；
                         status=未知时为 null"
    }
    // ... 情境标签词表中的每一个维度都必须在此列出一条记录，即使 status=未知
  },

  "ma250_detail": {
    "note": "仅当本次涉及法则二(趋势锚定法则)或用户询问涉及年线时填写此块，否则为 null",
    "chart_period_start_date": "用于判断的K线图所覆盖区间的起始日期（约一年前）",
    "chart_period_end_date": "用于判断的K线图所覆盖区间的结束日期（通常为当前/最新交易日）",
    "chart_source": "用于判断的K线图截图来源：用户上传 | 工具检索到的行情图表（注明检索
                      方式，如搜索到的哪个网站/工具）",
    "chart_reference": "若图片可保留引用（如用户上传的文件名，或检索到的图片URL），
                         记录在此，便于日后复核时能找到同一张图",
    "recent_ma250_series": [
      {"date": "交易日", "ma250": "当日MA250数值"}
      // 尽量保存最近30个交易日的MA250数值序列，用于比对图片目视判断与实际数值走势是否一致；
      // 若无法获取具体数值（例如只能看图，没有可读取的原始数据源），此数组可以为空 []，
      // 不强制要求，但只要能拿到就应该填
    ],
    "slope_judgment": "本次基于该图目视得出的定性判断：走平 / 向下 / 拐头向上 / 未知
                        （图上未画出该均线，或图片本身无法获取时填未知）",
    "slope_judgment_basis": "对该定性判断的简要说明，仅需一句话描述图上均线的视觉形态，
                              例如'图中年线在近三个月持续小角度上行，此前半年基本走平'"
  },

  "rule_matching": {
    "matched_rules": [
      {
        "rule_id": "如 R3-B",
        "rule_name": "低位缩量新低试仓",
        "match_type": "完全匹配 | 部分匹配",
        "matched_tags": ["price_position=低位", "volume_state=缩量", "pattern=新低"],
        "unresolved_tags": ["列出仍未知、但不影响本次判定为候选的标签，若无则为空数组"]
      }
    ],
    "unmatched_rules": [
      {
        "rule_id": "如 R3-A",
        "rule_name": "高位放量下跌减仓",
        "reason_type": "标签明确不符 | 相关维度未知",
        "reason": "具体原因说明"
      }
      // 必须覆盖全部19条法则：出现在 matched_rules 中的，不再重复出现在这里
    ]
  },

  "missing_inputs_requested": [
    {"field_id": "如 current_position", "question_asked": "实际问用户的问题原文"}
  ],
  "user_answers": {
    "<field_id>": "用户给出的回答原文或结构化值"
  },

  "rule_evaluations": [
    {
      "rule_id": "如 R3-B",
      "status": "TRIGGERED | NOT_TRIGGERED | INCONCLUSIVE | INSUFFICIENT_DATA",
      "interpretation": "解读文字",
      "suggested_action": "建议动作，如 SCALE IN",
      "evidence_used": ["本次评估实际使用的字段及取值列表"],
      "missing_inputs": ["评估时仍缺失、已标记UNKNOWN的字段"]
    }
  ],

  "conflicts_detected": [
    {
      "rule_a": "如 R3-B",
      "rule_b": "如 R8-B",
      "conflict_note": "冲突说明",
      "priority_given_to": "本次实际给出优先建议的法则编号及理由"
    }
  ],

  "final_recommendation_summary": "最终呈现给用户的一句话结论",

  "flags_for_human_review": [
    "本条记录中，任何依赖'未知'字段却仍被判定为TRIGGERED/NOT_TRIGGERED的情况，
     或AI在标签核实/法则匹配环节做出的、值得人工复核的边界性判断，都应在此列出，
     便于后续修改 rule_library.md 或具体法则文件时优先查看"
  ]
}
```

## 三、字段填写的强制要求

- `situation_tags` 必须覆盖情境标签词表中的**全部维度**，逐一列出，不能只列已核实的、  漏掉未知的——未知也是一条有价值的记录，说明当时这个信息缺失。
- 任何 `status: 已核实` 的字段，`evidence` 和 `evidence_date` 不能为空——写不出具体依据的， 一律改成 `status: 未知`，这与 SKILL.md 中"宁可说未知，绝不编造"的原则一致，日志本身也不能例外。
- `unmatched_rules` 必须覆盖第二步中判定为不匹配的**全部**法则，不能只挑几个代表性的。
- 如果本次会话中用户对某个字段给出的回答，与第一步联网核实的结果**相互矛盾**（例如联网查到是"放量"，但用户说"我看着是缩量"），必须在 `flags_for_human_review` 中记录这一矛盾，不要自行覆盖掉其中一方，交给人工判断谁对。
- `ma250_detail.recent_ma250_series` **允许为空数组**（例如只能拿到一张K线图截图、没有可读取的原始行情数据源时），但只要能通过工具获取到近30个交易日的实际MA250数值，就应该填入，不要因为已经有了图片判断就省略这一步——数值序列和图片判断是互相校验的两份证据，两者不一致时同样要记入 `flags_for_human_review`。

## 四、人类可读摘要 `decision_log_summary.md` 的格式

每条记录对应一个二级标题小节，格式示例：

```markdown
## [2026-08-25 15:30] 记录ID: 20260825-153000

**用户输入**：低位横盘两周后放量创新低，还有仓位，最近第二笔可能止损

**标的**：未指明

**已核实标签**：价格位置=低位(依据:...) | 成交量=放量(依据:...)
**未知标签**：is_hot_theme_stock、sector_state、market_sentiment...

**匹配法则**：R4-B(部分匹配)、R8-B(部分匹配)
**不匹配法则**：R3-A(标签不符)、R3-B(与已核实的"放量"矛盾)...（此处仅摘要，完整19条见JSON）

**最终建议**：优先执行 R8-B 暂停交易的纪律，R4-B 的低吸建议降级为背景信息

**⚠️ 待人工复核**：本次"是否横盘"完全依赖用户描述，未做联网核实
```

## 五、用于后续改进法则库的使用方式（人工侧）

积累一定数量的 `decision_log.jsonl` 记录后，人工审核时可以重点筛查：
- `flags_for_human_review` 非空的记录 —— 优先看
- 同一条法则反复出现在 `unmatched_rules` 且 `reason_type=相关维度未知` —— 说明这条法则依赖的某个输入长期拿不到，可能需要考虑该字段是否真的必要，或改成有更易获取的替代判断依据
- `conflicts_detected` 中反复出现的法则对 —— 说明冲突矩阵里这一对的优先级设定是否需要重新考虑，或该场景本身需要拆分出更细的判断条件
- 某条法则的 `status` 长期是 `INCONCLUSIVE`/`INSUFFICIENT_DATA` —— 说明该法则的必需输入在实际使用中很难满足，可能需要简化其触发条件
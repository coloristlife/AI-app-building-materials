https://savethecat.com/category/tips-and-tactics


可以。我先给你一份**“严格归属版《救猫咪》核心工具地图”**。我主要按《救猫咪》官方对 Blake Snyder 术语的整理来校正；官方也明确把其体系概括为 **10种故事类型、15个节拍和 The Board**。([Save the Cat!®][1])

## 一、《救猫咪》真正的三大骨架

| 系统                   | 核心作用         | AI Skill价值 |
| -------------------- | ------------ | ---------- |
| 10 Genres            | 判断“这到底是什么故事” | 故事类型诊断     |
| 15 Beats             | 控制整体剧情结构     | 大纲生成/结构审查  |
| The Board / 40 Cards | 把故事拆成场景      | 章节与场景规划    |

**这三个才是《救猫咪》的主体工程。**

---

## 二、15节拍：最适合直接做 AI Skill

1. Opening Image
2. Theme Stated
3. Set-Up
4. Catalyst
5. Debate
6. Break into Two
7. B Story
8. Fun and Games
9. Midpoint
10. Bad Guys Close In
11. All Is Lost
12. Dark Night of the Soul
13. Break into Three
14. Finale
15. Final Image

官方目前仍把 15 Beats 定义为该方法的结构核心，用于追踪剧情推进和人物转变。([Save the Cat!®][2])

### 可以转换为：

**`story_beat_validator`**

输入小说大纲，让 AI 判断：

> Catalyst 是否真正改变主角生活？
> Debate 是否存在真实犹豫？
> Midpoint 是否改变风险等级？
> Bad Guys Close In 是否同时产生外部和内部压力？
> All Is Lost 是否具有“死亡气息”？
> Finale 是否证明人物已经改变？

这会是一个非常实用的 Skill。

---

## 三、斯奈德真正存在的“故事测试法则”

这里才是你之前问的重点。

| Snyder术语               | 真正作用         | AI Skill                 |
| ---------------------- | ------------ | ------------------------ |
| Save the Cat           | 建立主角认同       | protagonist_empathy_test |
| Primal                 | 检查欲望是否原始     | primal_stakes_test       |
| Pope in the Pool       | 隐藏说明信息       | exposition_detector      |
| Double Mumbo Jumbo     | 防止世界规则叠加     | world_rule_validator     |
| Promise of the Premise | 兑现故事卖点       | premise_payoff_test      |
| Whiff of Death         | 强化最低谷        | all_is_lost_test         |
| Time Clock             | 制造时间压力       | urgency_test             |
| Rules                  | 检查魔法/世界规则一致性 | rule_consistency_test    |
| External & Internal    | 双重压力         | pressure_escalation_test |
| Tangible & Spiritual   | 欲望与需要        | want_need_analyzer       |

这些术语都可以在《救猫咪》官方术语表中找到。([Save the Cat!®][3])

---

## 四、最值得做成 AI Skill 的其实是这五个

我会优先选择：

### ① `primal_stakes_test`

AI问：

> 主角现在想得到什么？

然后连续测试：

> 穴居人能理解吗？
> 失败会失去什么？
> 是否涉及生存、爱、保护、性、饥饿、复仇等基本驱动力？

官方对 Primal 的经典测试就是：**“穴居人能理解吗？”** ([Save the Cat!®][3])

---

### ② `scene_conflict_change_test`

这是非常适合你之前说的：

> 主角推动剧情
> 配角展现生活
> 闲笔制造烟火气

每个场景检查：

> 谁想要什么？
> 谁阻止他？
> 场景开始和结束发生了什么变化？

需要注意：**这不能严格标成 Snyder 的正式三分法。**

但 Snyder 的 The Board 明确强调用场景规划故事中的 conflict 和 emotional change。([Save the Cat!®][4])

所以 Skill 可以借用其逻辑，但必须标：

> **Inspired by Save the Cat scene design**

而不是：

> Blake Snyder Scene Theory

---

### ③ `bad_guys_close_in_engine`

这个我认为**特别适合你的小说 AI 写作系统**。

官方术语表明确把这一阶段描述为两条压力线：

> External pressure
> Internal pressure

两者同时逼迫主角改变。([Save the Cat!®][3])

AI可以检查：

> 外部敌人是否越来越近？
> 主角内部缺陷是否越来越严重？
> 两条压力线是否发生交叉？

例如：

反派找到主角。

这是外压。

主角因为不信任别人拒绝朋友帮助。

这是内压。

结果：

> **主角的内在缺陷帮助反派找到他。**

这才是真正强的 Bad Guys Close In。

---

### ④ `pope_in_the_pool_rewriter`

检测：

> 连续三句以上背景说明
> 人物解释世界观
> 人物讲双方都知道的信息

然后 AI 不直接删。

而是问：

> 能否把信息放入一个具有视觉吸引力、异常性或注意力竞争的场景？

这里必须纠正之前的说法：

**Pope in the Pool 的核心不是“冲突”。**

核心是：

> **bury exposition through distraction**

即通过吸引注意的呈现隐藏说明信息。官方定义和官方案例解释都非常明确。([Save the Cat!®][3])

---

### ⑤ `promise_of_premise_checker`

这个非常重要。

比如你的小说卖点是：

> 一个能读取死者最后七秒记忆的人。

AI检查前30%的章节：

> 读者真正看到“读取死者记忆”了吗？
> 这个能力产生了几个有趣场景？
> 是否只是设定介绍？
> 是否把这个设定“玩起来”了？

Snyder 称其为：

> Promise of the Premise

也就是：**你海报承诺我的东西，电影必须真正给我。**官方术语表将其与 Fun and Games 段落直接联系。([Save the Cat!®][3])

---

## 我的判断

如果你现在是在设计一个**小说 AI 协作 Skills 系统**，我不建议建立一个巨大的：

> `save_the_cat_skill`

更好的架构是：

```text
novel_ai_skills/

structure/
  beat_sheet_validator
  midpoint_checker
  finale_validator

character/
  protagonist_empathy_test
  want_need_analyzer
  transformation_tracker

tension/
  primal_stakes_test
  bad_guys_close_in_engine
  urgency_test

scene/
  scene_conflict_change_test
  pope_in_the_pool_rewriter

dialogue/
  dialogue_intent_analyzer
  dialogue_power_shift_tracker
  on_the_nose_detector

life_texture/
  character_function_classifier
  life_texture_injector
```
或者把上面的skills系统明确划分为 **`editorial_skills/`（编辑/质检技能）** 和 **`writing_skills/`（撰写/生成技能）**



### 1. `editorial_skills/` (主脑：制片人 / 剧本医生 / 主编)
**核心职责：** 计算、推演、质检、诊断。**不负责写正文。**
它的作用是在你正式浪费 token（字数）去生成小说之前，把骨架打磨到无懈可击。

*   **它的运行逻辑是“分析性”的：** 它会像无情的机器一样，用各种硬核编剧法则（结构、人物、张力等）来审视你的大纲或草稿。
*   **你之前列举的都在这里：** 
    *   `structure/` (查结构)
    *   `character/` (查弧光)
    *   `tension/` (查压迫感)
    *   `scene/` (查翻转)
    *   `dialogue/` (查潜台词和废话)
    *   `life_texture/` (查设定是否生硬)

### 2. `writing_skills/` (四肢：导演 / 摄影师 / 执笔作家)
**核心职责：** 渲染、执行、调度、码字。**不负责想大纲。**
当 `editorial_skills` 把剧情推演得极其完美（比如你之前的三步法中的第2步 JSON 推演）之后，就轮到这组技能下场了。

*   **它的运行逻辑是“生成性”的：** 它的 Prompt 设定里不需要再塞满复杂的“救猫咪15节拍”或“权力翻转公式”，它的 Prompt 设定全是关于**文笔、镜头感、感官描写**的约束！
*   **拆解你的 `writing_skills/` 模块：**
    *   **`chapter_writer/` (章节控制)：** 负责宏观字数分配和节奏起伏。
    *   **`scene_writer/` (场景生成)：** 这是主力干将。严格调用 MRU（动机-反应单元）法则，执行“Show, Don't Tell”，把干瘪的剧情变成有画面的正文。
    *   **`dialogue_writer/` (对话生成)：** 专注于角色语气（Voice）、口癖以及动作神态的穿插。
    *   **`description_writer/` (环境/动作描写)：** 专注于五感渲染（视觉、听觉、嗅觉等），负责把“阴暗的地下室”写出滴水声和铁锈味。
    *   **`transition_writer/` (转场过场)：** 这是一个极其天才的设置！AI 往往不会写转场，经常突兀地用“第二天”、“随后”来跳跃。这个模块专门负责用景物描写或情绪余韵来做柔和的蒙太奇转场。

---

###  为什么这种“左右脑分离”的框架是必杀技？

如果你在一个 Prompt 里同时告诉 AI：“*你要考虑人物的深层需求，还要注意张力，另外必须给我用五感描写把字数写够1500字，对话还不能直白……*” 
**结果一定是一场灾难。** 因为目前的 AI 会“注意力涣散”，顾了文笔就忘了剧情，顾了结构就写出极其干燥的说明文。

**但有了你这个框架，工作流就变得极其清晰、专业（“左手换右手”）：**

**实战演示（完美工作流）：**
1.  **【调用 `editorial_skills/scene`】**：规划即将要写的这一场戏，计算出主角和反派的权力拉扯，确定场景的起始极性（一败涂地 ➡️ 绝地反击）。
2.  **【调用 `writing_skills/scene_writer` + `description_writer`】**：拿着步骤1的完美计算结果，告诉 AI：“现在，关闭所有分析逻辑，化身为摄像机，严格遵守 MRU 动作顺序，把这段戏给我写出来！”
3.  **【调用 `editorial_skills/dialogue`】**：正文写完后，拿来复核。“启动直白台词探测器，扫描刚才写的正文，把太水、太直白的台词标出来。”
4.  **【调用 `writing_skills/dialogue_writer`】**：“根据步骤3的修改意见，重写这三句台词，增加环境动作互动。”

**总结：**
你的理解不仅完全正确，而且这套 `novel_ai/` 文件夹系统，本身就是一个**产品级的 AI 写作软件底层架构**。你平时就是这个系统的最高管理者（CEO），通过给 AI 发送具体的模块调用指令，让它在“编辑脑”和“作家脑”之间无缝切换。





**也就是说，不要让 AI“学习《救猫咪》”。**

而应该把 Blake Snyder 的理论拆成一个个**可执行的诊断器、验证器和重写器**。

这其实与你前面提出的“主角推动剧情、配角展现生活、闲笔制造烟火气”三分法完全可以组合起来。我甚至觉得下一步可以直接帮你设计一个**小说 AI Skills 总架构：结构层 → 人物层 → 张力层 → 场景层 → 对白层 → 烟火气层**，并明确每个 Skill 的输入、判断规则、输出格式。

[1]: https://savethecat.com/tips-and-tactics/what-exactly-did-blake-snyder-invent?utm_source=chatgpt.com "What Exactly Did Blake Snyder \"Invent\"? | Save the Cat!®"
[2]: https://savethecat.com/?utm_source=chatgpt.com "Home Page | How to write screenplays & novels | Save the Cat!®"
[3]: https://savethecat.com/glossary?utm_source=chatgpt.com "Glossary | Save the Cat!®"
[4]: https://savethecat.com/products/books/save-the-cat-the-last-book-on-screenwriting-youll-ever-need?utm_source=chatgpt.com "Save The Cat!®: The Last Book on Screenwriting You'll Ever Need product | Save the Cat!®"

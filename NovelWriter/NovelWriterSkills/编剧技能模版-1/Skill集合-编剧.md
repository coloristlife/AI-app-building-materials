1. 首先需要明确，写小说和写剧本是不一样的
2. 在生成具体的prompt时，需要提供哪些信息，比如参考的小说名称，作者名称，还是某些理论，比如救猫咪。还是需要把上述的信息自己整合成一个直接可以给AI的指令，去指导它生成最终对应skill的prompt？
3. 在生成editorial skill下面的具体的每个prompt时，需要两套分别对应大纲期和正文期
（还需要AI核实下面的skills是否全部都是适合剧本的）

# genesis_skills (创世纪与前置开发模块)
### Skill 1: `high_concept_logline_generator` (高概念与商业钩子提炼机)
### Skill 2: `truby_four_point_opposition_mapper` (特鲁比四点对立阵营网格仪)
### Skill 3: `ghost_wound_and_lie_excavator` (幽灵、创伤与谎言挖掘机)
### Skill 4: `magic_system_and_cost_architect` (硬核设定与代价法则建筑师)
### Skill 5: `aesthetic_and_taboo_rulemaker` (美学基调与禁忌词典生成器)


# editorial skills （需要大纲期和正文期两套）
## /character/ (人物弧光与内核质检)
在你的工作流中，当你或者 AI 构思出了一份初步的《人物设定表》与《故事大纲》时，**不要急着让 AI 去写正文**。

先调用这 5 个 `editorial_skills/character` 技能，让大模型以 JSON 格式对大纲进行“交叉审讯”。
*   如果 `want_vs_need_diagnostician` 亮红灯，说明你的主角是个纸片人。
*   如果 `pressure_choice_evaluator` 报错，说明你的高潮剧情太水。
*   
### Skill 1: `want_vs_need_diagnostician` (欲求与需求体检仪)
### Skill 2: `empathy_and_flaw_scanner` (共情点与“六个缺陷”扫描器)
### Skill 3: `pressure_choice_evaluator` (极限施压与真实品格测试仪)
### Skill 4: `arc_transformation_calculator` (人物弧光三段论推演机)
### Skill 5: `foil_network_checker` (对照组与B故事关系网核查仪)


## /dialogue/ (台词与对白质检)
### Skill 1: `voice_fingerprint_and_uniformity_analyzer` (声纹鉴定与同质化查杀仪)
### Skill 2: `dialogue_as_weapon_validator` (台词武器化校验器)
### Skill 3: `subtext_density_calculator` (潜台词密度计算器)
### Skill 4: `ping_pong_and_filler_trimmer` (乒乓式废话与应答裁剪刀)
### Skill 5: `talking_heads_anchoring_checker` (悬浮对话与肢体节拍锚定仪)

## /life_texture/ (生活质感与设定质检)
### Skill 1: `lived_in_wear_and_tear_scanner` (二手宇宙/磨损感扫描仪)
### Skill 2: `socio_economic_gravity_checker` (社会经济引力/生存底色测算仪)
### Skill 3: `lore_mundane_integration_tester` (宏大设定与凡俗生活融合度测试器)
### Skill 4: `sensory_noun_specificity_auditor` (感官特指与专有名词审核员)
### Skill 5: `system_cost_and_backlash_calculator` (系统代价与反噬审计员)

## /scene/ (微观场景与节拍质检)
### Skill 1: `micro_goal_and_opposition_scanner` (微观目标与直接阻力扫描仪)
### Skill 2: `scene_sequel_rhythm_analyzer` (场景与续场节拍器 / GCD-RDD校验)
### Skill 3: `in_late_out_early_trimmer` (晚进早出裁剪刀)
### Skill 4: `exposition_infodump_detector` (说明性文字与信息倾倒排雷针)
### Skill 5: `subtext_and_beat_extractor` (潜台词与微观节拍透视镜)

## /structure/ (结构质检与逻辑推演)
### Skill 1: `beat_sheet_validator` (15 节拍里程碑审计)
### Skill 2: `midpoint_pendulum_analyzer` (中点钟摆效应分析)
### Skill 3: `setup_payoff_matrix` (铺垫与收回矩阵)
### Skill 4: `value_shift_quantizer` (价值翻转量化仪)
### Skill 5: `b_story_integration_checker` (B故事融合度核查)

## /tension/ (张力与压迫感质检模块)
### Skill 1: `expectation_vs_reality_gap_calculator` (期望与现实鸿沟测算仪)
### Skill 2: `escalation_and_antagonism_scanner` (敌对力量与冲突升级扫描器)
### Skill 3: `stakes_and_clock_validator` (核心赌注与倒计时质检仪)
### Skill 4: `dramatic_irony_radar` (戏剧反讽/信息差雷达)
### Skill 5: `value_charge_shifter` (正负极价值翻转校验器)

# writing_skills（撰写/生成技能模块）
## chapter_writer/ (章节宏观调度与生成)
### 🎥 Skill 1: `pacing_and_word_allocator` (节奏与字数调度师 / 呼吸控制)
### 🎥 Skill 2: `cold_open_igniter` (冷开场抓手/入戏引爆器)
### 🎥 Skill 3: `psychic_distance_controller` (心理距离与焦距推拉手)
### 🎥 Skill 4: `thematic_palette_renderer` (基调色板渲染器)
### 🎥 Skill 5: `cliffhanger_and_hook_engineer` (断章大师 / 悬念抛钩手)

## description_writer/` (环境与五感渲染)
在这套 `writing_skills` 的生态里，`description_writer`（环境渲染）通常不单独成章，它是**“调味料”**和**“气氛组”**。
### 🖌️ Skill 1: `synesthesia_and_five_senses_engager` (通感与非视觉强制触发器)
### 🖌️ Skill 2: `environment_as_actor_animator` (环境拟人与主动攻击引擎)
### 🖌️ Skill 3: `objective_correlative_filter` (情绪滤镜/客观对应物渲染)
### 🖌️ Skill 4: `micro_macro_panning_crane` (微观宏观景深摇臂)
### 🖌️ Skill 5: `patina_and_decay_painter` (材质与做旧包浆师)

## dialogue_writer/` (台词与对白渲染)
在你的 AI 写作平台架构中，`dialogue_writer` 千万不能独立运行。它必须和前面拆解过的 `scene_writer`（场景与动作引擎）**交织在一起工作**。

如果你只跑 `dialogue_writer`，你得到的会是一份非常精彩的“话剧剧本”（全是台词）。
但小说不是话剧，小说需要画面。

### 🎭 Skill 1: `voice_and_lexicon_simulator` (声纹滤镜与阶级词汇渲染器)
### 🎭 Skill 2: `oblique_response_generator` (非对称交锋与闪避式对答)
### 🎭 Skill 3: `subtext_chatter_encoder` (昆汀式表面闲聊与潜台词伪装机)
### 🎭 Skill 4: `sorkin_overlap_and_interruption_director` (索金式火力交叉与打断调度)
### 🎭 Skill 5: `verbal_imperfection_injector` (生理瑕疵与呼吸感植入器)

## scene_writer/ (场景与微观动作渲染)
### 🎥 Skill 1: `mru_sequence_enforcer` (MRU 动机-反应链条锻造师)
### 🎥 Skill 2: `show_dont_tell_translator` (情感具象化/动态展示翻译机)
### 🎥 Skill 3: `spatial_and_prop_choreographer` (空间走位与道具调度员)
### 🎥 Skill 4: `action_physics_renderer` (动作物理引擎与受击反馈)
### 🎥 Skill 5: `subtextual_beat_contraster` (动作节拍与潜台词反差机)

## transition_writer (电影级蒙太奇转场)
### ✂️ Skill 1: `match_cut_animator` (视觉/听觉匹配剪辑师)
### ✂️ Skill 2: `j_cut_audio_pre_cog` (J-Cut 先声夺人桥接器)
### ✂️ Skill 3: `l_cut_emotional_echo` (L-Cut 情绪余韵尾音拖拽）
### ✂️ Skill 4: `sensory_montage_accelerator` (感官蒙太奇/岁月流逝压缩机)
### ✂️ Skill 5: `whiplash_hard_cut_director` (极性反差硬切刀 / 冰火两重天)

# `continuity skills/` (连贯性与品控场记模块)
**运行逻辑**：它不参与创作，它是无情的**后台审计程序（Daemon Process）**。每次生成完一章，它就自动运行一次，比对 JSON 数据库，查杀幻觉。

### Skill 1: `chekhovs_gun_and_open_loop_tracker` (契诃夫之枪与悬念开口追踪器)
### Skill 2: `inventory_and_lore_auditor` (物理道具与设定状态审计员)
### Skill 3: `emotional_inertia_and_polarity_manager` (情绪惯性与极性连贯器)
### Skill 4: `spatiotemporal_logistics_engine` (时空后勤引擎与坐标同步器)
### Skill 5: `narrative_voice_and_style_drift_watchdog` (叙事视角与文风漂移看门狗)


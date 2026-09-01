# AI生成

### Skills

- Brainstorming: npx skills add https://github.com/obra/superpowers
--skill brainstorming 
- Writing-Plans: npx skills add
https://github.com/obra/superpowers --skill writing-plans 
- Copywriting: npx
skills add https://github.com/coreyhaines31/marketingskills

- Humanizer: npx skills add
https://github.com/op7418/humanizer-zh --skill humanizer-zh

- more
  - https://mp.weixin.qq.com/s/0atUuqGHYR6XU48ioR4zUg


这四个安装命令来自于目前在 AI Agent（如 Claude Code, Cursor 等 CLI 工具）生态中非常流行的 **“AI 技能库 (AI Skills/Prompt Frameworks)”**。本质上，它们是经过顶级调优的 **System Prompts（系统提示词）和结构化工作流（通常以 `SKILL.md` 文件的形式存在）**。

**重要提示：** `npx skills add` 是供终端或代码编辑器使用的命令行工具。**NovelCrafter 作为一款带 UI 的专业小说创作软件，并不直接在终端运行这些代码**。但这完全没关系！你可以提取这 4 个开源 Repo 中的核心 `SKILL.md` 提示词文本，将其**直接粘贴并配置到 NovelCrafter 的「Custom Prompts（自定义提示词）」库中**，从而为你的小说创作插上翅膀。

下面为你详细介绍这 4 个库的核心功能，以及如何将它们与 NovelCrafter 完美结合：

### 1. `obra/superpowers` (Brainstorming)
* **介绍**：Superpowers 是一套强调“逻辑和结构”的 AI 工作流框架。其中的 `brainstorming`（头脑风暴）技能，核心是强制 AI 在执行任何具体生成任务**之前**，先进行发散性思考、探讨意图、用户需求和设计可能性。
* **配合 NovelCrafter 使用场景**：**小说前期的灵感探索与世界观构建。**
* **如何配置**：
  1. 在 NovelCrafter 左侧菜单打开 **Prompts（提示词）** -> 创建一个新的 **Chat Prompt（聊天提示词）**。
  2. 去该 GitHub 仓库找到 `brainstorming` 的提示词逻辑。
  3. 将其逻辑转化为小说向：“在开始写正文之前，你必须通过提问来与我探讨核心冲突、人物动机和可能的情节走向。不要直接写正文，而是给我 3-4 个发散性的创意选项……”
  4. **使用方法**：在 NovelCrafter 的 Chat 界面召唤这个 Prompt，与 AI 探讨剧情，打破卡壳。

### 2. `obra/superpowers` (Writing-Plans)
* **介绍**：同样来自 Superpowers 框架，`writing-plans` 的核心作用是将复杂的任务拆解为**可执行的结构化计划**（执行大纲）。它要求 AI 把想法具象化为一步步的执行步骤。
* **配合 NovelCrafter 使用场景**：**大纲拆解与分场（Beat Sheet）规划。**
* **如何配置**：
  1. 可以在 NovelCrafter 中建立一个名为“大纲生成器”的 **Chat Prompt**。
  2. 提取 `writing-plans` 强调逻辑链和逐步递进的 Prompt 逻辑。
  3. **使用方法**：当你在上一步（Brainstorming）定下剧情走向后，调用这个 Prompt：“请根据我们的讨论，为第 X 章输出一个包含 5 个关键节拍（Beats）的详细计划，明确每个场景的 POV（视点人物）、场景目标和场景冲突。” 这个生成的计划可以直接放入 NovelCrafter 的 Scene 笔记中作为参考。

### 3. `coreyhaines31/marketing` (Copywriting)
* **介绍**：这是一个非常全面的 SaaS 与营销技能库（Marketing Skills Bundle）。它包含了转化率优化、文案撰写（Copywriting）、SEO 策略等专业营销逻辑，深谙受众心理学。
* **配合 NovelCrafter 使用场景**：**小说包装、宣发文案与“推书”语料生成。**
* **如何配置**：
  1. 在 NovelCrafter 创建一个新的独立 Prompt。
  2. 从该仓库的 `SKILL.md` 中提取 Copywriting（尤其是文案心理学、AIDA 模型等框架）的系统指令。
  3. **使用方法**：书写完毕后，利用 NovelCrafter 的全书上下文（Context），使用该 Prompt 生成：
     * 引人入胜的小说简介（Blurb）或亚马逊/网文平台的书籍详情页介绍。
     * 用于社交媒体（Twitter, 小红书等）推广你小说的短推文，制造悬念吸引读者。
     * 给不同平台读者的精准广告投放文案。

### 4. `op7418/humanizer-zh` (Humanizer-zh 中文去 AI 味)
* **介绍**：这是针对中文内容创作者的神器。它总结了 24 种常见的“AI 写作痕迹”（如过度使用排比、夸张的象征、诸如“不仅……而是”、“至关重要”、“深入探讨”等套话），并能自动将文本重写为自然、地道、有人味的中文。
* **配合 NovelCrafter 使用场景**：**正文润色与重写（Text Replacement Prompt）。**
* **如何配置**：
  1. 在 NovelCrafter 中找到 **Prompts**，选择创建一个 **Text Replacement Prompt（文本替换/修改提示词）** 或 **Rephrase Prompt**。
  2. 去该 GitHub 仓库复制 `humanizer-zh` 的核心规则（即要求 AI 避开哪些具体句式，如何增加长短句结合，如何减少成语堆砌等）。
  3. 将这些规则写进 NovelCrafter 的 Instructions 栏中。
  4. **使用方法**：在 NovelCrafter 的正文编辑器中，当你用 AI 扩写（Expand）了一段剧情觉得“机器味”太重时，直接框选这段文字，点击你的 `Humanizer-zh` 修改指令。AI 会当场把生硬的网文套话，改写成富有呼吸感、像人类作家写出的生动文学语言。

### 总结：NovelCrafter 的终极协作流
你可以将这 4 个 Repo 的核心逻辑提取后，在 NovelCrafter 中串联起一个完整的闭环：
1. 用 **Brainstorming** (在 Chat 中) 和 AI 聊出小说的点子。
2. 用 **Writing-Plans** 把点子变成具体到章节的网文大纲/大纲树。
3. 用 NovelCrafter 依据大纲写出正文后，用选中文本，使用配置了 **Humanizer-zh** 的重写按钮，把正文洗出“人情味”。
4. 完稿后，丢进配置了 **Copywriting** 逻辑的提示词中，自动生成爆款小说简介和推广文案。






## 第一部分：到底什么是“Skill（技能）”？

在 AI 的语境下（特别是你提到的 `npx skills add` 这种代码命令），**Skill 本质上就是一个“大师级的高级提示词（Advanced Prompt）”或“标准作业程序（SOP）”。**

你可以这样理解：
如果基础的人工智能是一个“绝顶聪明但完全没有工作经验的实习生”，那么：
*   **普通 Prompt（提示词）：** 就像你随口吩咐一句“帮我写个大纲”。实习生会按自己的理解瞎写一通。
*   **Skill（技能）：** 就像你扔给实习生一本**《好莱坞金牌编剧工作手册》**。这本手册里详细规定了：“第一步，你必须先问我三个关于主角动机的问题；第二步，分析反派的弱点；第三步，使用三幕剧结构输出大纲；第四步，绝对不允许使用陈词滥调”。

**一个标准的 Skill 仓库（Repo）里通常包含：**
1.  **Role（角色设定）：** 让 AI 扮演极其专业的特定角色（如顶级营销专家、资深网文编辑）。
2.  **Rules / Constraints（规则与禁忌）：** 明确告诉 AI “禁止做什么”（例如 Humanizer 技能里会禁止 AI 使用“至关重要”、“不仅……而且”等机器味很重的词）。
3.  **Workflow（结构化工作流）：** 强迫 AI 按照 1、2、3 的步骤思考，而不是一口气把废话全吐出来。

**总结：** `npx skills add...` 是给程序员在终端（Terminal）里用的安装命令，用来把这些优秀的“工作手册”下载到他们的写代码软件里。

---

## 第二部分：如何在 NovelCrafter 中使用这些 Skills？ (跟前面的部分内容重复)

**核心观念：NovelCrafter 并没有终端可以输入 `npx` 命令。** 所以，你不能“一键安装”它们。
你需要做的是 **“知识搬运”** —— 把这些 GitHub 仓库里的核心“工作手册（Prompt 文本）”复制出来，粘贴到 NovelCrafter 的**自定义提示词库（Custom Prompts）**里。

具体操作步骤如下：

#### 第一步：提取 Skill 的核心文本（搬运）
1.  复制你提到的那些 GitHub 链接，在浏览器里打开（例如打开 `https://github.com/op7418/humanizer-zh`）。
2.  在仓库的文件列表里，寻找以 `.md`（Markdown格式）或 `.txt`、`.json` 结尾的文件（通常叫 `SKILL.md`、`prompt.md` 或 `README.md` 中的系统提示词部分）。
3.  打开这个文件，**把你看到的一长串规则、指令、Prompt 文本全部复制下来**。

#### 第二步：在 NovelCrafter 中创建对应的 Prompt
打开你的 NovelCrafter，点击侧边栏的 **Settings（设置）** -> 选择 **Prompts** 选项卡。

由于这 4 个技能的作用不同，你需要将它们配置成 NovelCrafter 中不同**类型**的 Prompt：

#### 1. Brainstorming & Writing-Plans（头脑风暴与大纲计划）
这两个技能的作用是和你对话、探讨剧情。
*   **如何配置：**
    *   在 NovelCrafter 的 Prompts 设置中，点击 **Add Prompt**。
    *   将 **Type（类型）** 设置为 **Chat Prompt（聊天提示词）**。
    *   给它起个名字，比如 `Skill: 顶级头脑风暴`。
    *   在 **System Message / Instructions** 框里，粘贴你从 GitHub 复制过来的 Brainstorming 代码/提示词。
*   **如何使用：**
    *   在写作界面的右侧边栏打开 **Chat（聊天）** 面板。
    *   在输入框上方选择你刚才创建的 `Skill: 顶级头脑风暴` 提示词。
    *   跟 AI 说：“我想写一个关于赛博朋克刺客的故事”，AI 就会严格按照 Skill 的专业逻辑，一步步引导你完善设定，而不是直接乱写。

#### 2. Humanizer-zh（去 AI 味润色大师）
这个技能的作用是修改已经写好的、比较生硬的中文文本。
*   **如何配置：**
    *   在 Prompts 设置中，点击 **Add Prompt**。
    *   将 **Type（类型）** 设置为 **Selection Prompt（选中文字提示词）** 或者 **Rewrite（重写）**。
    *   名字叫 `Skill: 去除AI味重写`。
    *   在内容框里粘贴 Humanizer-zh 仓库里关于“避开AI常用词、使用自然长短句”的中文规则。
*   **如何使用：**
    *   在正文编辑器里，**用鼠标高亮选中**一段你觉得太像 AI 写的段落。
    *   会弹出一个快捷菜单，点击 **Rewrite（重写）** 或找到你设置的 `Skill: 去除AI味重写`。
    *   AI 会在原地把这段文字“洗”得充满人情味。

#### 3. Copywriting (营销文案)
这个技能用于给小说写简介、推文、广告词。
*   **如何配置：**
    *   将其配置为 **Chat Prompt**（用于对话生成）或 **Command Prompt**（命令提示词）。
    *   粘贴 Copywriting 仓库里的营销心理学框架指令。
*   **如何使用：**
    *   打开侧边栏 Chat，选中这个 Prompt。
    *   你可以利用 NovelCrafter 的上下文功能（比如引入整个系列的故事大纲），对 AI 说：“请根据我小说的全局大纲，用 AIDA（吸引-兴趣-欲望-行动）营销模型，帮我写一段 200 字的小红书推书文案。”

### 💡 进阶技巧：结合 NovelCrafter 的 Snippets（代码片段）
在 NovelCrafter 里粘贴这些 Skill 文本时，你可以加入 NovelCrafter 特有的**变量标签**，让 Skill 威力倍增。
例如，在你的 Prompt 文本末尾加上：
> “请基于以下当前场景的信息进行分析： `{scene_summary}`，并参考以下角色设定：`{characters}`”

这样，你从外面“偷师”来的高级 AI 技能，就完美融入了你小说当前的情境中，真正变成你专属的 AI 写作助理。
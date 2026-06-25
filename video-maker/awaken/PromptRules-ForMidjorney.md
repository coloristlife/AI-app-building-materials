
如果你的目标是制作一部**一分钟的软科幻电影短片**（通常需要分镜策划，并结合 Midjourney 生成画面，再用 Runway/Sora/Pika 等工具转化为动态视频），我强烈建议你**以【4S框架（叙事思维）】为主，将【Atomic（原子框架）】作为辅助工具套入其中**。

为什么这么建议？以下是具体的实战分析：

### 1. 为什么【4S框架】更适合做电影短片？

*   **电影是“动”的，需要叙事：** 一分钟的短片大约需要 15-20 个镜头。你需要描述角色的动作、情绪的变化、环境的流转。**4S框架的自然语言描述（讲故事）**非常适合用来写分镜脚本（Storyboard）。
*   **AI 视频工具的偏好：** 现在的 AI 视频生成工具（如 Runway Gen-2, Pika, Sora）更倾向于理解**“符合人类自然语言逻辑”**的提示词。你直接塞一堆由逗号分隔的单词（原子法），生成的视频往往会缺乏核心焦点和连贯动作；而用自然语言描述（4S法），视频的动作和物理规律会更合理。
*   **软科幻的特质：** 软科幻（Soft Sci-Fi）重在**氛围、心理、社会学和人物情绪**（比如电影《Her》或《银翼杀手2049》的文戏），而不是硬核的机械结构。4S框架能更好地描绘“孤独的人工智能看着窗外的霓虹灯”这种带有情绪的画面。

---

### 2. 实战工作流：如何结合两套框架制作这部短片？

最聪明的做法是：**用【原子法】定基调，用【4S法】跑镜头。**

#### 第一步：用【原子法】制作短片的“视觉概念设计”（Lookbook）
在开机前，导演需要确定整部片子的美术风格。你可以把图片里“分子级”和“原子级”的参数固定下来，作为你这部软科幻短片的**“祖传滤镜”**。

*   **提取你的软科幻“原子公式”：**
    `35mm film, directed by Denis Villeneuve, cinematic lighting, cool blue and neon pink color palette, melancholy emotion, highly detailed, --ar 16:9 --style raw`
    *(这个公式你先存好，后面每一个镜头都要加上它，以保证一分钟短片的画风统一)*

#### 第二步：用【4S法】逐个生成镜头的分镜
现在开始按镜头写提示词。你只需要改变 4S 中的前三项（Scene/Subject/Setting），最后一项（Style）直接贴上你刚才确定的“原子公式”。

**镜头 1：开场远景（交代世界观）**
*   **Scene:** 赛博朋克城市的黄昏 (A dusk view of a cyberpunk city)
*   **Subject:** 全息广告牌在闪烁 (holographic billboards flickering)
*   **Setting:** 空气中弥漫着雾气和微雨 (fog and light rain in the air)
*   **Style (套用原子公式):** `35mm film, directed by Denis Villeneuve, cinematic lighting, cool blue and neon pink color palette, melancholy emotion --ar 16:9 --style raw`

**镜头 2：主角特写（软科幻的情感切入）**
*   **Scene:** 一个安静的公寓房间内 (Inside a quiet apartment room)
*   **Subject:** 一个仿生人女孩坐在窗边，眼神忧郁，看着窗外 (an android girl sitting by the window, melancholy eyes, looking outside)
*   **Setting:** 霓虹灯光映在她的机械义体皮肤上 (neon lights reflecting on her cybernetic synthetic skin)
*   **Style (套用原子公式):** `35mm film, directed by Denis Villeneuve... (同上)`

**镜头 3：细节特写（推动剧情）**
*   **Scene:** 桌子上的特写镜头 (Close up shot on a desk)
*   **Subject:** 她的手正握着一株发光的机械植物 (her hand is holding a glowing mechanical plant)
*   **Setting:** 背景是模糊的城市夜景，景深很浅 (shallow depth of field, blurred city night in the background)
*   **Style (套用原子公式):** `35mm film, directed by Denis Villeneuve... (同上)`

### 总结建议：

*   如果你是在**找灵感、调风格、测试哪种灯光或胶片效果最好看**，用图片里的**【Atomic（原子级）】**模板不断替换词汇，效率极高。
*   一旦风格确定，进入**实际的镜头生产环节**，请切换到表格里的**【4S框架】**，像导演讲戏一样去描述你的软科幻故事，把你的风格词缀放在最后。这样产出的连贯性和故事感是最强的。


# 需要考虑的因素
- 全门类摄影类型
- 光影
- 时装
- 情绪、面部表情与手部姿态
- 相机
- 胶片型号
- 时代
- 镜头语言、景别与构图
- 动态与动作捕捉


# 构建软科幻提示词

## 要求
### 有 sref 的情况：

考虑midjourney 4S 框架和 按照需要选择这些下面的元素，如何为软科幻短片（《醒来》AIGC/60秒）构建midjorney提示词，有 sref 人物 refer,需要考虑生成图片作为runway视频材料时，需要考虑的一致性问题：
- 全门类摄影类型
- 光影
- 时装
- 情绪、面部表情与手部姿态
- 相机
- 胶片型号
- 时代
- 镜头语言、景别与构图
- 动态与动作捕捉

| 4S 框架维度 | 对应九大元素 | 核心作用 |
| :--- | :--- | :--- |
| **1. Scene (场景起手)** | 镜头语言、景别与构图 + 动态与动作捕捉 | 决定本镜头的**拍摄视角**、主体正在进行的**核心动作与运动幅度**。 |
| **2. Subject (主体承接)**| 情绪、面部表情与手部姿态 + 时装 | 决定角色的**情感状态、微表情、手势**以及**服装材质与风格**。 |
| **3. Setting (环境转换)**| 全门类摄影类型 + 时代环境 | 决定画面的**媒介属性**（如纪录片、水下摄影）和**世界观背景**。 |
| **4. Style (风格定调)** | 光影 + 相机 + 胶片型号 + 时代感 | 决定画面的**色彩科学、物理质感（如颗粒）与曝光调性**。 |

相应的分镜场景为：




### 无 sref 的情况：
考虑4S 框架和 按照需要选择这些下面的元素，如何为软科幻短片（《醒来》AIGC/60秒）构建midjorney提示词，需要考虑生成图片作为runway视频材料时，需要考虑的一致性问题：：
- 全门类摄影类型
- 光影
- 时装
- 情绪、面部表情与手部姿态
- 相机
- 胶片型号
- 时代
- 镜头语言、景别与构图
- 动态与动作捕捉

| 4S 框架维度 | 对应九大元素 | 核心作用 |
| :--- | :--- | :--- |
| **1. Scene (场景起手)** | 镜头语言、景别与构图 + 动态与动作捕捉 | 决定本镜头的**拍摄视角**、主体正在进行的**核心动作与运动幅度**。 |
| **2. Subject (主体承接)**| 情绪、面部表情与手部姿态 + 时装 | 决定角色的**情感状态、微表情、手势**以及**服装材质与风格**。 |
| **3. Setting (环境转换)**| 全门类摄影类型 + 时代环境 | 决定画面的**媒介属性**（如纪录片、水下摄影）和**世界观背景**。 |
| **4. Style (风格定调)** | 光影 + 相机 + 胶片型号 + 时代感 | 决定画面的**色彩科学、物理质感（如颗粒）与曝光调性**。 |


## 参考答案


在制作一分钟软科幻短片时，结合 **4S 框架**与前述的**九大原子级元素**，能帮你建立一套标准的电影级工作流。

以下是针对“**无参考图（纯文本跑图）**”与“**有参考图（`--cref` / `--sref` 双轨跑图）**”两种不同创作场景下的策略、公式与实战演示。

---

## 🧭 第一部分：九大元素在 4S 框架中的映射表

为了保持结构清晰，我们需要将九大元素精准归类到 4S 框架的四个维度中：

| 4S 框架维度 | 对应九大元素 | 核心作用 |
| :--- | :--- | :--- |
| **1. Scene (场景起手)** | 镜头语言、景别与构图 + 动态与动作捕捉 | 决定本镜头的**拍摄视角**、主体正在进行的**核心动作与运动幅度**。 |
| **2. Subject (主体承接)**| 情绪、面部表情与手部姿态 + 时装 | 决定角色的**情感状态、微表情、手势**以及**服装材质与风格**。 |
| **3. Setting (环境转换)**| 全门类摄影类型 + 时代环境 | 决定画面的**媒介属性**（如纪录片、水下摄影）和**世界观背景**。 |
| **4. Style (风格定调)** | 光影 + 相机 + 胶片型号 + 时代感 | 决定画面的**色彩科学、物理质感（如颗粒）与曝光调性**。 |

---

## 场景一：无参考图（纯文本跑图）
*适用于短片前期，用来进行视觉探索、建立故事板（Storyboard）和设计视觉基调（Lookbook）。*

### 1. 纯文本黄金提示词公式
> **`[摄影类型], [景别/镜头角度], [动态/动作描写], [主体特征 + 时装材质 + 表情/手势], [时代背景环境], shot on [相机型号], using [胶片型号], [光影/构图风格] --ar 16:9 --style raw`**

### 2. 软科幻实战演示
*   **分镜脚本构思：** 女主（仿生人）在雨夜的霓虹街头奔跑逃亡，神色惊恐，手向后伸。
*   **拼装后的提示词 (Prompt)：**
    > `Documentary photography, Dutch angle and motion blur of a woman running down a rain-slicked futuristic neon street, she is wearing a translucent techwear raincoat over a spandex jumpsuit, desperate and vulnerable expression on her face as her synthetic hand reaches back towards the dark alley, the 1980s retro sci-fi background, shot on Arriflex, using CineStill 800T, dramatic low-key lighting, rule of thirds --ar 16:9 --style raw`
*   **公式拆解说明：**
    *   `Scene`: 荷式倾斜、动感模糊、在雨夜街头奔跑 (`Dutch angle and motion blur... running down...`)
    *   `Subject`: 女人、穿着半透明机能风雨衣、紧身连体衣、神色惊恐脆弱、合成手向后伸 (`woman... translucent techwear... desperate expression... synthetic hand reaches back`)
    *   `Setting`: 纪实摄影、80年代复古科幻背景 (`Documentary photography`, `1980s retro sci-fi`)
    *   `Style`: 阿莱胶片机拍摄、CineStill 800T（获得标志性红晕与冷调）、低调光、三分法构图 (`shot on Arriflex, using CineStill 800T, low-key lighting, rule of thirds`)

---

## 场景二：有参考图（`--cref` + `--sref` 双轨跑图）
*适用于短片的中后期制作。当你已经确定了主角长相（`--cref`）和全片的视觉色调（`--sref`），需要批量产出不同分镜画面。*

### 1. 双轨跑图的“风格冲突”避坑规则：
*   **不要在文本中写具体的相机和胶片：** `--sref` 已经锁定了画面的色彩底色和噪点质感。如果在提示词里继续写 `CineStill 800T` 或 `Arri Alexa`，会导致文本与参考图拉扯，画面色彩可能会过度饱和或出现噪点混乱。
*   **不要在文本中过度描述角色长相：** `--cref` 已经锁定了角色的面部、发型和基础体型。文本中只需保留情绪、表情、手势以及可能需要更换的“新服装”。
*   **利用权重控制服装更换：** 
    *   如果要保持参考图中的衣服不变，使用 `--cw 100`。
    *   如果要为角色更换新衣服，使用 `--cw 0`（此时仅保留面部），并在提示词中详细写出新时装（如 `wearing a translucent techwear coat`）。

### 2. 有参考图的简化版提示词公式
> **`[摄影类型], [景别/镜头角度] of [动态/动作描写], [主体新服装描写], [表情/手势描写], [时代背景环境] --cref [角色图URL] --sref [风格图URL] --cw [0或100] --sw [风格权重] --ar 16:9 --style raw`**

### 3. 软科幻实战演示（换装 + 动作分镜）
*   **分镜脚本构思：** 继承前期的风格和角色。在这一镜中，角色换上了机能风外套，在水下实验室里，手指轻轻触摸发光的机械植物，神色专注、出神。
*   **拼装后的提示词 (Prompt)：**
    > `Underwater photography, closeup shot of a woman looking mesmerized, her fingers gently touching a glowing bioluminescent mechanical plant, wearing a dark neoprene techwear outfit, deep water laboratory environment, off-center composition --cref [角色图URL] --sref [风格图URL] --cw 0 --sw 800 --ar 16:9 --style raw`
*   **公式拆解说明：**
    *   `Scene`: 水下摄影、特写镜头、手指轻轻触摸 (`Underwater photography, closeup shot... fingers gently touching`)
    *   `Subject`: 换上黑色潜水服面料机能服（因为写了 `--cw 0`）、神色出神/被迷住 (`wearing a dark neoprene techwear outfit`, `looking mesmerized`)
    *   `Setting`: 深水实验室环境 (`deep water laboratory environment`)
    *   `Style` (极简处理，避免与 `--sref` 冲突)：仅保留了 `off-center composition`（偏离中心构图）来引导排版，没有任何关于色彩、相机、胶片和曝光的描述。这些全部交给底层的 `--sref` 去控制和释放。
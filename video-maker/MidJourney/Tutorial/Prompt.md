
# Cinematic AI Photography Prompt Structure 


**ATOMIC PROMPTING - Cinematic** (原子级提示词 - 电影感)

**【Organism Level / 生物级】**(对应图片绿色文字)
Cinematic, [PHOTOGRAPHY TYPE] [SUBJECT/ACTION]

**【Molecular Level / 分子级】**(对应图片黄色文字)
[SHOT TYPE] [LOCATION] [FASHION] [YEAR] [FILM STOCK] [CAMERA] [DIRECTOR] [EMOTION] [LIGHTING] [COLOR]

**【Atomic Level / 原子级】**(对应图片红色文字)
[costume description] [fashion color palette] [fashion brand] [fashion material]

**【Parameters / 参数】**
*   `--ar 16:9` [your choice of aspect ratio]
*   `--s value` [if you want to use default Midjourney Aesthetics, value range= 0 - 1000]
*   `--style raw` [if you don't want to use default Midjourney Aesthetics, for a deeper focus on your style keywords]
*   `--w value` [short for: --weird, brings unconventional results, value range= 0 - 3000]
*   `--w value --s value` [default Midjourney Aesthetics with an unconventional touch]





# **4S 提示词构建法**

Midjourney 提示词创作中至关重要的 **“结构化思维”** 与 **“渐进式迭代”** 。

正如文中开头所说，“世上没有完美的提示词，出图永远需要实验、引导和偶发的灵感（Serendipity）”。但是，拥有一套清晰的结构能帮你将脑海中的画面精准、有逻辑地翻译给 AI。

以下为您将这段视频的核心教学梳理为一套可以直接套用的 **“4S 提示词构建法”** 与 **高级进阶技巧**：

---

### 一、 4S 提示词构建法（The Four S's）

写长提示词时最忌讳胡乱堆砌词汇。作者推荐将提示词拆分为四个层次，一层层递进构建：

| 层次 | 英文名称 | 核心作用 | 本例中的演变 |
| :--- | :--- | :--- | :--- |
| **1. Scene** | **场景总览** | 用最基础、通用的原型词汇（Archetypes）定下故事大纲。 | `an anthropomorphic barn owl exploring an abandoned temple --ar 16:9 --style raw` *(一只拟人化的仓鸮探索废弃的寺庙)* |
| **2. Subject** | **主体细节** | 为主角添加衣着、动作、携带道具等细节。 | `the owl is wearing cult robes and a hood, holding a burning torch...` *(猫头鹰穿着邪教长袍，戴着兜帽，手持燃烧的火炬)* |
| **3. Setting** | **环境细节** | 描绘背景墙面、空气氛围、光影质感。 | `the temple has dusty relics and faded murals on the walls, dark and mystical atmosphere...` *(寺庙墙上有尘土飞扬的文物和褪色的壁画，黑暗神秘的氛围)* |
| **4. Style** | **美学风格** | 引入特定导演风格、摄影手法、胶片型号。 | `in the style of Guillermo del Toro, 35mm Kodak Vision2 500T 5218, low-key lighting, deep shadows...` *(吉尔莫·德尔·托罗风格，35mm柯达胶片，低调光与深邃阴影)* |

---

### 二、 核心进阶技巧

在这个案例中，有三个非常高级且实用的写实/电影感调优技巧：

#### 1. “指代呼应”法（Calling Back）
这是解决 Midjourney “长提示词混乱、多画角色”最有效的技巧：
*   **问题**：如果你在 Scene 写了 `a barn owl`（一只仓鸮），在 Subject 写细节时又用 `an owl`（一只猫头鹰）或者 `the animal`（这只动物），AI 很容易产生混乱，误以为画幅里要出现两只动物（一只仓鸮，一只穿长袍的猫头鹰）。
*   **解决方法**：使用**定冠词和完全一致的词汇进行指代呼应**。比如后文一直使用 **`the owl`**、**`the temple`**，明确地告诉 AI：“我接下来说的所有细节，都是在描述刚刚那同一个主体、同一个环境”，从而让画面元素高度聚合。

#### 2. “胶片型号”优于“相机型号”（Film Stock > Camera Name）
很多新手喜欢在提示词里堆砌 `Sony A7R5, 8k, Canon EOS` 等相机型号，但实际效果往往不尽人意。
*   **为什么**：Midjourney 对相机机身名字的理解通常较为宽泛，而**胶片型号（Film Stock）**则自带极其独特的**色调曲线、色彩偏好和颗粒感（Film Grain）**。
*   **本例实践**：使用特定的电影胶片 **`35mm Kodak Vision2 500T 5218`**，能瞬间为画面渲染出一种好莱坞式的、厚重且有故事感的冷暖对比影调（正如《潘神的迷宫》那种暗黑童话感）。

#### 3. 光影术语的精准升级
*   起初，作者使用 `soft Eerie lighting`（柔和怪异的光影），AI 给出的效果可能比较随机。
*   为了更精准地贴近《潘神的迷宫》那种高对比、暗黑的氛围，作者将其升级为了更专业的电影照明术语：**`low-key lighting and deep shadows`（低调光与深邃阴影）**。这种精准的术语能够强迫 AI 大幅压暗环境，只留局部高光，制造戏剧张力。

---

### 三、 科学的迭代工作流（Workflow）

文本最后展示了专业创作者是如何“调图”的：

1.  **搭骨架**：先用极简的句子生成基础画面（Scene + 比例 + `--style raw`）。
2.  **填血肉**：观察首轮出图，不满意的地方通过“指代呼应”逐步添加 Subject、Setting 和 Style。
3.  **调画质（参数介入）**：当**文字提示词基本确定**、画面构图满意后，开始调整参数。
    *   尝试不同的 `--stylize` 数值（如 `--s 50` 测试写实，`--s 300` 测试艺术化）。
    *   在 `Standard` 模式与 `Raw` 模式之间切换，对比哪种模式色彩和细节更符合直觉。
4.  **完成**：选出最完美的图像。

这是一个由浅入深、逐步收敛逻辑的过程。按照这套方法，您可以非常高效地控制 Midjourney 输出任何复杂、有深度故事感的视觉作品。


-----
# **AI 分词原理（Tokenization）**、**逆向工程学习（Midlibrary 与 `/describe`）**

我们开始进入 Midjourney 提示词的“深水区”，涉及到了 **AI 分词原理（Tokenization）**、**逆向工程学习（Midlibrary 与 `/describe`）**，以及 **Logo 设计与矢量艺术（Vector Art）** 的专业工作流。

以下为您将这三个章节的知识系统地整理成中文解析，帮助您更好地掌握这些高级技巧：

---

### 一、 机制篇：分词原理（Tokenization）与强力词（Power Tokens）

#### 1. 什么是 Token？
Midjourney 并不会像人类一样去理解整句英文的语法，而是将你的提示词拆分成更小的语义片段，这些片段被称为 **Tokens（词元）**。
*   例如，它不会去分析动词、副词、介词的语法关系，而是将这些 Tokens 与其训练数据库中的图像特征进行关联匹配。

#### 2. 强力词（Power Tokens）
在成千上万个 Tokens 中，有一些词对画面的影响力和控制力远超其他词，它们被称为**强力词（Power Tokens）**。
*   **跨媒介应用**：虽然很多强力词源于摄影术语（如 `35mm`、`low-key lighting`），但它们并不局限于摄影。如果你在写实风格之外（如油画、3D 渲染或动漫风格中）使用这些摄影强力词，同样会极大地改变画面的构图、光影和质感。
*   **建立专业词汇库**：想成为 Midjourney 高手，核心不是去背模板，而是去积累各个领域（如时装、建筑、平面设计、电影）的专业词汇。

---

### 二、 逆向学习篇：Midlibrary 与 `/describe`

如果你感到词穷，或者不知道如何用言语描述某种风格，以下两个工具是你的“作弊器”：

#### 1. Midlibrary（midlibrary.io）—— 最强大的风格图书馆

https://midlibrary.io/


这是一个专门研究 Midjourney 如何解释各种艺术风格的第三方数据库。
*   **作用**：它系统化地整理了数千位艺术家、插画家、摄影师、建筑师、时尚设计师以及各种艺术流派和技术在 Midjourney 中的出图效果。
*   **Style Reference（风格参考）**：Midlibrary 还整理了大量的 **SREF 编码（Style Reference Codes，如 `--sref 1234567`）**。在提示词末尾加上这些代码，AI 就能直接套用其对应的视觉风格，实现高度一致的艺术调性。

#### 2. `/describe`（图像逆向描述）
当你看到一张喜欢的图，却不知道它是怎么画出来的时候：
*   **操作**：在 Midjourney 中使用 `/describe` 命令并上传这张图片，或者在网页端上传图片并点击“小眼睛”图标。
*   **效果**：AI 会自动为你生成 4 组描述该图的提示词，其中会包含它识别出来的相似艺术家、风格流派和专业强力词。你可以从中挑选最有趣的词汇融入到自己的创作中。



----
## style reference 和4s提示词的混搭


**1. 找到 Style Reference (`--sref`) 后，还需要使用 4S 框架吗？**

**仍需要，但可以精简。**
*   **前 3 个 S（场景 Scene、主体 Subject、环境 Setting）：** 必须保留。它们决定画面“画什么”（内容构图）。参考图无法完美替代具体的动作、道具或环境描述。
*   **第 4 个 S（风格 Style）：** 可以**大幅省略**。既然 `--sref` 已经规定了色彩、笔触或光影质感，文本中的导演、胶片、画风等词汇可以删减，将视觉美学交给参考图接管。

---

**2. 文本描述与 `--sref` 冲突时，Midjourney 如何处理？**

**Midjourney 会将两者进行“强行混合”。** 

通常，文本主导“内容主体”，`--sref` 主导“视觉美学”。如果文本和参考图在**纯风格层面**发生直接矛盾（例如：文本写“黑白极简素描”，`--sref` 给了一张“色彩浓烈的赛博朋克 3D 渲染图”），MJ 的处理逻辑如下：

*   **结果体现为“融合体”：** MJ 不会完全忽略某一方，而是产出一种混合画风。比如，可能会生成带有赛博朋克光影结构的黑白线条画，或者带有素描纹理的彩色 3D 图。
*   **如何控制谁赢谁输？**
    使用 **风格权重参数 `--sw`**（默认 100，范围 0-1000）来裁决冲突：
    *   **偏向参考图：** 调高权重（如 `--sw 800`）。MJ 会压制你的文本风格词，强制服从 `--sref` 的画风。
    *   **偏向文本提示词：** 调低权重（如 `--sw 50`）。MJ 仅借鉴参考图的极少元素（如微小的色调倾向），主要服从文本描述。
---

### 三、 实战篇之 Logo 设计

在 Midjourney 中设计 Logo 与普通生成插画截然不同，它需要克制和极简。

#### 1. 基础配置
*   **画幅比例**：通常建议设为正方形 `--ar 1:1`，这是大多数应用、头像和标志的通用比例。

#### 2. Logo 的强力词配方
*   **基础概念词**：`minimalist`（极简主义）、`abstract`（抽象）、`brandmark`（品牌符号）、`geometric`（几何形状）。
*   **垂类调性词**：`Boutique`（精品店风）、`psychedelic`（迷幻风）、`retro`（复古风）。
*   **大师流派（借鉴平面设计巨匠）**：
    *   `Milton Glaser`（米尔顿·格拉瑟，I ♥ NY 设计者）
    *   `Paul Rand`（保罗·兰德，IBM、Steve Jobs 的 NeXT 标志设计者）
    *   `Carolyn Davidson`（卡洛琳·戴维森，Nike 标志设计者）

#### 3. 美化度（Stylize）的调优技巧
*   对于**极简或品牌符号类（Minimalist/Brandmark）** Logo，中高美化度（如 `--s 100` 到 `--s 250`）可以产出很具现代设计感的结果。
*   但对于**迷幻（Psychedelic）**等复杂风格，一旦 `--stylize` 超过 `200`，画面就会变得过于繁复，从而失去 Logo 应有的高识别度与纯粹性。

#### 4. 文字注入（Text Generation）
在 Midjourney 中加入精准文字，需要在提示词中使用双引号包裹：
*   **示例**：`coffee shop logo, "Kevin's coffee", minimalist, geometric --ar 1:1`

---

### 四、 实战篇之矢量与文创艺术（Vector Art）及后期转换

如果你想设计用于 T 恤印花、马克杯、乙烯基贴纸（vinyl sticker）或徽章的图案：

#### 1. 矢量风格的强力词配方
*   `Vector art`（矢量艺术）、`Vector graphic`（矢量图形）、`graphic design`（平面设计）。
*   `icon`（图标）、`emblem`（徽章）、`shirt design`（T恤设计）、`vinyl sticker`（乙烯基贴纸）、`clip art`（剪贴画）。
*   `silhouette`（剪影）、`outline`（轮廓线）。

#### 2. 栅格图转矢量图的后期工作流
Midjourney 输出的图像是**栅格图（Raster Image，如 PNG）**，由像素组成，放大后会模糊。要进行印刷、商业排版或刺绣，必须将其转换为能够无限放大且可编辑的**矢量图（Vector Image，如 SVG）**。

可以使用以下转换工具：
*   **Adobe Express (免费)**：内置了免费的 PNG 转 SVG 工具，可以快速将干净的 Logo 或图标转为矢量图，适合日常和轻量使用。
*   **Vectorizer.ai (专业 / 收费)**：这是一个极其强大的 AI 矢量化工具。它对渐变色、复杂曲线和细节的处理比传统的描摹引擎更精细，非常适合经常从事文创、印花设计的专业人士。
*   **Adobe Illustrator**：最后导入 AI 软件中，使用“图像描摹（Image Trace）”或手动钢笔工具进行细节调整、改色和最终输出。
*   


------
# **如何在 Midjourney 中精准控制文本生成**，以及 **10 个来自官方文档与资深创作者实战总结的提示词黄金法则**。

以下为您将这些极具实操价值的技巧整理为系统化的中文解析：

---

### 一、 文字生成（Generating Text）的进阶指南

在 Midjourney v6、v7 及后续版本中，文字生成功能得到了极大的提升，但要做到 100% 准确，仍需配合特定方法：

#### 1. 基础语法规则
*   **使用双引号**：必须用英文双引号将目标文字括起来，例如 `"Kevin's coffee"`。
*   **大小写敏感**：双引号内的字母大小写及特殊字符会被严格遵循。
*   **易成功场景（文字载体）**：如果文字附着在现实中本就经常印有文字的载体上，AI 的生成成功率会成倍增加。
    *   *推荐载体*：纸张、车牌（license plates）、影院灯箱招牌（theater signs）、路边广告牌（Billboards）等。

#### 2. “局部重绘（Vary Region / Inpainting）”的文字后期修正大法
如果首次生成的图像构图非常完美，但文字出现了拼写错误（这是 AI 生成文字的常见现象），不需要去 Photoshop 修改，可以直接利用 Midjourney 的后期能力：
1.  **框选区域**：在图片下方点击 **Vary Region**（局部重绘 / 局部变形），用套索工具选中文字写错或缺失的区域（如果是 Logo，可以直接选中需要放品牌名字的空白位置）。
2.  **重写提示词**：在下方的输入框中，仅输入双引号包裹的目标词汇，例如 `"coffee"`。
3.  **生成并匹配风格**：Midjourney 会在保留原图其他部分的前提下，专门在框选区域内重新绘制文字。最神奇的是，**它会自动匹配原图的配色、渐变效果、材质和现有的字体风格**，让新文字自然融入原图。

---

### 二、 10 个快速提效的提示词技巧（10 Prompting Tips）

这些技巧能帮助你告别低效、冗长的“废话提示词”，用更精准的“词元（Tokens）”去跟 AI 交流：

#### 1. 极简叙述，直奔主题（Simplify Phrasing）
*   **避免废话**：不要像跟人类聊天一样写：“请给我画一幅有很多盛开的加州罂粟花的画，让它们呈现明亮、充满活力的橙色，并用彩色铅笔画出插画风格……”
*   **高效改写**：`bright orange California poppies drawn with colored pencils`
*   **原理**：Midjourney 会将句子拆分成“Tokens”（词元）。“Show picture”（画一幅画）或“lots of”（很多的）这些词会生成无意义的无用词元，反而会干扰 AI 对核心词汇的注意力。

#### 2. 词汇具体化（Specificity）
*   避免使用像 `big`（大）这样过于宽泛、平淡的词。
*   改用语义更具体、冲击力更强的近义词，如：`High`（高耸的）、`gigantic`（巨大的）、`enormous`（庞大的）。

#### 3. 避免使用模糊的复数（Specify Quantities）
*   如果你写 `cats`（猫），AI 可能会随机画出 3 只、10 只甚至 100 只。
*   **正确做法**：明确给出一个具体的数量，例如 `three cats`（三只猫）。

#### 4. 用“正向引导”而非“负向否定”
*   AI 无法很好地理解自然语言中的否定句。如果你写 `a birthday party with no cake`（没有蛋糕的生日派对），由于提示词中包含了“cake”这个 Token，AI 有极大概率依然会画出一个蛋糕。
*   **正确做法**：直接在提示词末尾添加排除参数 **`--no cake`**。

#### 5. 明确你关心的所有核心元素
*   如果你不指定背景、光影或构图，AI 就会用它的默认美学随机帮你填满。
*   凡是你认为重要的元素（主体、介质、光影、色彩、情绪、构图），务必都在提示词中交代清楚。

#### 6. 全身照黄金秘诀：描述鞋子（The Shoes Hack）
*   Midjourney 在默认生成人像时，经常会自动裁剪掉下半身，只保留半身像。
*   **绝招**：在提示词中**明确描述人物穿的鞋子**（例如 `wearing leather boots` 或 `wearing white sneakers`）。为了把鞋子画出来，AI 会强制退远镜头，从而 100% 保证生成全身照。

#### 7. 一键电影感（Cinematic Hack）
*   想要快速获得电影大片级的剧照质感，最简单、最高效的两个短语是：**`cinematic still`**（电影剧照）或 **`35mm cinematic`**（35毫米电影感）。

#### 8. 善用官网 Explore（探索）页
*   当遇到创作瓶颈时，去 Midjourney 官网的 Explore（探索）页面，搜索相似的关键词，看看别人成功作品的提示词是如何构建的，这是最高效的学习方式。

#### 9. 灵活切换 Standard 与 Raw 模式
*   对于同一个提示词，在 `--style raw`（还原度高、更写实）和默认的标准模式（美化度高、更具艺术感）之间反复切换对比，往往能带给你截然不同的创意启发。

#### 10. 使用 Emoji（表情符号）和打破规则
*   不要被规则限制。如果你想寻找纯粹的随机灵感，忘掉所有单词，尝试直接在提示框里输入几个 Emoji 表情符号（例如 🐉🔥🌲），看看 AI 能够根据这些图形符号发散出怎样令人惊叹的画面。
*   



# reference:

https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics

**提示与技巧（Prompting Tips & Tricks）**
在 Midjourney 中，简短而直接的提示词通常能生成最好的图像。使用能够清晰描述你想看到内容的短语，把它当作是在快速“截图”你的想法。避免使用冗长的列表或过于详细的说明，因为这些可能会让生成过程变得混乱。

👎 显示一张包含大量盛开的加州罂粟花的图片，让它们呈现明亮、鲜艳的橙色，并以彩色铅笔插画风格绘制
👍 彩色铅笔插画风格的明亮橙色加州罂粟花

---

### 选择合适的词语

你选择的词很重要！尽量使用更具体的同义词。例如，不要只用“big（大）”，可以考虑“huge（巨大的）”“gigantic（庞大的）”或“enormous（极其巨大的）”。越精确，结果往往越好。

---

### 使用具体数字

像“cats（猫）”这样的复数词可能比较模糊。可以改用具体数字，例如“three cats（三只猫）”。或者使用集合名词，比如“flock of birds（一群鸟）”，而不是简单的“birds（鸟）”。

---

### 聚焦你想要的内容

描述你想要的东西，而不是你不想要的。如果你说“没有蛋糕的派对”，系统仍然可能生成蛋糕。若要排除某些元素，请参考 no 参数的使用方式。

---

### 提示词长度与细节

你的提示词可以非常简单——甚至一个词或一个表情符号也可以。短提示词会让 Midjourney 默认风格自动填补细节。但如果你有明确的重要元素，一定要写清楚。细节越少，变化越多，但对结果的控制也越弱。

如果某些细节对你很重要，可以参考以下方面：

* **主体**：是谁或什么？（人物、动物、角色、地点、物体）
* **媒介**：以什么形式呈现？（照片、绘画、插画、雕塑、涂鸦、挂毯）
* **环境**：在哪里？（室内、室外、月球、水下、城市中）
* **光照**：什么样的光？（柔和、环境光、阴天、霓虹灯、摄影棚灯光）
* **颜色**：什么色调？（鲜艳、柔和、明亮、单色、多彩、黑白、粉彩）
* **情绪**：想表达什么感觉？（俏皮、平静、阴郁、充满活力）
* **构图**：如何构图？（肖像、头像、特写、鸟瞰图）

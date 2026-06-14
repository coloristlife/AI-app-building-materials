### 一、 什么是 SREF？

**SREF** 是 **Style Reference（风格参考）** 的缩写，是 Midjourney 专门用于**复制、锁定和延续特定画面视觉风格（包括色彩、调色、光影、笔触、材质和氛围）**的核心参数。

它的引入极大解决了 AI 绘图“画风不稳定、无法复现”的痛点。在 Midjourney 中，SREF 主要有以下三种应用方式：

1.  **图片链接引用（`--sref <图片网址>`）**：
    告诉 AI：“请参考这张图的画风和配色，来画我新输入的提示词。”（例如：`a cat --sref https://example.com/style.jpg`）。
2.  **随机探索（`--sref random`）**：
    让 Midjourney 随机摇号产生一种独特、小众的艺术风格。如果摇出来的画面效果很好，你可以查看这张图的信息，它会附带一串纯数字的 SREF 编码。
3.  **数字代码引用（`--sref <纯数字编号>`）**：
    这是最强大、也是 Midlibrary 收集的核心内容。这些数字编号（如 `--sref 2106517499`）代表了 Midjourney 神经网络中固化好的某种美学“数字指纹”。只要加上这串数字，就能精准重现特定的色调和艺术笔触。

> **💡 配合参数 `--sw`（Style Weight，风格权重）**：
> 默认权重为 100，取值范围为 0-1000。数值越高，AI 对该 SREF 风格的模仿就越死板、越极致；数值越低，AI 则更自由。

---

### 二、 如何在 Midlibrary 找到 SREF？

Midlibrary（`midlibrary.io`）不仅是常规的艺术家风格库，它还维护着一个非常强大的 **SREF 专属目录（SREF codes catalog）**。

以下是在 Midlibrary 查找并使用 SREF 编码的步骤：

#### 1. 访问专属目录
打开浏览器，直接访问 Midlibrary 的 SREF 专区：
👉 **`https://midlibrary.io/sref-codes`**
（也可以在 Midlibrary 首页的顶部导航栏，直接找到 **SREF** 或 **Style Codes** 专区）。

#### 2. 利用其核心功能进行筛选
Midlibrary 相比于其他平台，最实用的地方在于它提供了极其科学的**横向对比和基准测试**：
*   **多版本兼容性**：Midlibrary 收录了适用于不同模型版本（如 V6.1、Niji、V7、V8 等）的数千个精选 SREF 代码。您可以根据当前在 Midjourney 中使用的版本进行筛选。
*   **17 种基准测试（Benchmark Prompts）**：这是 Midlibrary 的王牌功能。对于收录的每一个 SREF 编码（例如 `--sref 2106517499`），他们的团队都会使用 **17 个完全相同的基准提示词**去生成图片。
    *   这意味着你可以看到同一个 SREF 代码在：*摄影、插画、3D 渲染、建筑、角色设计、时尚、自然风景*等完全不同题材下的视觉表现。这能帮你提前避坑，确认该代码是否能完美适配你的出图主题。
*   **分类与过滤器**：可以通过高级过滤器按色彩冷暖、艺术媒介、氛围（如暗黑、复古、明亮）等标签来检索符合预期的风格。

#### 3. 复制与使用
当你在 Midlibrary 找到喜欢的画风时：
1.  直接点击该风格卡片，复制其提供的纯数字编号（如 `2106517499`）。
2.  在 Midjourney 中，将这串代码加在你的提示词末尾即可：
    > `a futuristic robot --sref 2106517499 --ar 16:9`

---

### 三、 其他寻找 SREF 编码的免费/辅助渠道

除了 Midlibrary 之外，如果想探索更多风格，还可以通过以下渠道互补：

1.  **Midjourney 官方网站的 Explore（探索）页**：
    登录 Midjourney 官网，进入 Explore 页面。如果看到别人生成的画风非常好看，把鼠标悬停在图片上，很多时候能直接看到创作者使用的 `--sref <数字>` 码，点击即可直接复制。
2.  **SrefHunt（srefhunt.com）等第三方免费库**：
    专门用于收集和分享 SREF 的社区型网站。不仅有丰富的分类（如单色、微距、赛博朋克等），还支持用户上传自己摇出的优秀 SREF 码，是一个很好的灵感来源。

    https://srefhunt.com/

    https://creatorimpact.com/project/midjourney-v6-style-codes-for-sref/

    https://sites.google.com/charlottequinndesigns.com/cqs-sref-library/mj-6-codes

    https://midlibrary.io/sref-codes

    
https://github.com/VoltAgent/awesome-design-md/tree/main

DESIGN.md is a new concept introduced by Google Stitch. A plain-text design system document that AI agents read to generate consistent UI.

It's just a markdown file. No Figma exports, no JSON schemas, no special tooling. Drop it into your project root and any AI coding agent or Google Stitch instantly understands how your UI should look. Markdown is the format LLMs read best, so there's nothing to parse or configure.


# tutorial

AwesomeDesign-md + OpenCode,Claude: This OPENSOURCE Design System is SO EASY & SO GOOD!
https://www.youtube.com/watch?v=cSF-bxotrz4

这是一篇基于您提供的内容归纳整理的结构化中文博客片段：

标题：使用 Awesome Design MD 与 AI 代理构建高质量前端 UI
1. 核心痛点：AI 生成前端的“视觉混乱”

大多数 AI 代理现在都能编写出结构良好的代码，这已经不足为奇。但真正的问题在于，它们生成的前端在视觉上往往杂乱无章：你可能会得到一个还不错的首屏（Hero section），紧接着是随意的间距、奇怪的卡片，以及看起来像从其他网站生搬硬套过来的按钮。拉到页面底部时，整个页面感觉就像是用五个不同的提示词（Prompt）东拼西凑出来的。而 Volta Agent 开源的 Github 仓库 awesome design MD 正是为了解决这个真实存在的痛点。

2. 什么是 Awesome Design MD？

乍一看这只是另一个 Awesome 列表，但它实际上是一个精心策划的 design.md 文件集合，灵感来自于真实的、特别是面向开发者的网站设计。

丰富的资源：包含超过 50 个不同的设计文件夹，涵盖了 Vercel、Linear、Stripe、Raycast、Supabase、Notion、Volta Agent 等知名设计风格。

文件结构：每个条目不仅是随机的文本笔记，都配有规范的 design.md 文件，以及 preview.html 和 preview-dark.html 预览文件，方便你在使用前检查视觉方向。

AI 可读的设计系统：design.md 是一个纯 Markdown 文件，以 AI 代理能很好理解的方式描述了设计系统。它涵盖了视觉情绪、调色板、排版规则、组件样式、间距、布局原则、深度、响应式行为以及设计护栏。这让你不再依赖“让它看起来干净现代”这种模糊的一句话提示，而是直接给模型提供可用的具体设计参考。

核心概念区分：

agents.md：负责项目应该如何构建（架构、行为、实现规则）。

design.md：负责项目应该呈现怎样的外观和感觉（视觉行为）。
这种分离非常重要，因为许多“AI UI 风格偏移”正是源于试图将架构、行为、样式和文案方向全部塞进同一个提示词中。

3. 结合 Verdant 的实战工作流

(注：Awesome Design MD 仓库是免费且采用 MIT 协议的，但 Verdant 是一款消耗积分的付费产品，在生成大型 UI 时需留意成本。)

Awesome Design MD 可以非常自然地融入到 Verdant 的项目工作流中：

准备项目：在 Verdant 中创建或打开一个前端项目（无论是 Next、Vite 还是 Astro 应用都可以，只需打开工作区）。

放置文件：克隆 awesome design MD 仓库，将你选择的 design.md （例如 Vercel 风格）复制到项目的根目录中。（理清这三个文件：verdant.md 是全局规则，agents.md 是特定项目实现规则，design.md 是视觉参考）。

打开 Verdant：通过桌面端登录打开文件夹，或在 VS Code 安装 Verdant 扩展并打开面板。

明确的提示词（Prompt）：即使 Verdant 会自动读取文件，依然建议在提示词中明确指出。如果是大型项目建议先用“计划模式（Plan mode）”，小型落地页直接用“代理模式（Agent mode）”即可。

验证过的初始 Prompt 示例：

“为一个名为 Shipstack 的开发者工具构建一个响应式落地页。使用项目根目录中的 design.md 文件作为视觉的真实基准（visual source of truth）。创建一个首屏区块、一个功能网格、一个代码示例区块、一个定价区块、客户 Logo 展示以及最后的行动呼唤（CTA）。保持文案简洁，并与设计文件中的间距、排版和表面处理保持一致。”

生成与审查：发送提示后，Verdant 会检查工作区并读取包含 design.md 在内的文件。在第一遍生成时，你就能看出效果：首屏会更有设计感，间距更严谨，按钮和卡片不再显得随意。它解决了页面“泛泛而谈”的感觉。

第二轮优化（Refinement）：第一遍通常不完美，需要进行修正。

验证过的优化 Prompt 示例：

“精简首屏文案，减少不必要的装饰元素，让功能卡片更扁平化，并使最后的行动呼唤（CTA）更贴近 design.md 中定义的视觉语言。同时，检查移动端布局。”

这种工作流之所以可靠，是因为设计文件一直留在项目根目录，Verdant 会不断回归同一个视觉基准，而不是随着后续的提示词发生风格偏移。

4. 优缺点评估

优点：

提供了开发者熟知网站（如 Vercel, Linear 等）的风格，让你心里有明确的目标预期，既简化了提示过程，也更容易评判输出质量。

与 agents.md 搭配使用效果极佳，能让提示词更简短、更具可重复性。

缺点与注意事项：

并非魔法：仅有详细的文件不能保证结果一定惊艳，质量依然取决于 AI 代理的能力、你的提示词以及项目结构。

可能过于衍生（同质化）：某些设计风格特征太强，如果不加注意，页面可能会显得像是在抄袭。因此一定要修改内容结构、产品定位和品牌细节，将其作为设计规范的借鉴而不是进行懒惰的克隆。

适用场景：对于极其简单的内部工具，这套设置可能有点大材小用。但对于落地页、精美的仪表盘、文档网站、演示 Demo 以及面向客户的 UI 来说，这是一个非常扎实的工作流。

5. 总结

Awesome Design MD 是那种能默默解决 AI 辅助前端开发实际问题的仓库。它将通常只存在于人们脑海中、截图里或模糊提示词中的设计语言，转化成了 AI 代理可以切实遵循、可复用的文本格式。

只需“打开项目 -> 放入 design.md -> 提示 Verdant 将其作为视觉基准 -> 生成并优化”这套简单、实用且易于重复的工作流，就能让你告别那些“顶部看起来还行，往下一滑就惨不忍睹”的 AI 生成页面。如果你也在用 AI 构建前端，这个仓库绝对值得一试。

(如果您喜欢这些内容，可以考虑通过 Super Thanks 选项打赏，或点击 Join 按钮成为会员。)
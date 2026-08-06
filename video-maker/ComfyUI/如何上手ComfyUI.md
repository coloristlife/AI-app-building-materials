

# 如何上手 ComfyUI？（全套实操指南） - v1

如果你理解了上面的原理，你就会发现，**ComfyUI 是目前学习扩散模型（Diffusion Models）工作原理最好的工具之一。**

相比 Automatic1111 等 WebUI，它们已经把大部分底层流程封装好了，更适合快速出图；而 ComfyUI 采用节点式（Node-Based）设计，把模型推理过程完整地拆解出来，让你亲手搭建整个生成流程，因此更容易真正理解 AI 是如何一步步生成图片的。([ComfyUI][2])

下面按照实际学习路线，一步一步掌握 ComfyUI。

---

# 阶段一：前期准备与安装

## 硬件要求

建议使用 **NVIDIA（英伟达）显卡**，因为目前 CUDA 生态仍然最成熟。

常见模型的大致配置建议：

* **SD 1.5：**4GB 显存即可运行，6GB 以上体验更好。
* **SDXL：**建议 8GB 显存以上，12GB 体验更流畅。
* **Flux、SD3 等新模型：**建议至少 12GB 显存，16GB 或以上效果更佳。

当然，如果显存不足，也可以通过低显存模式、模型量化（GGUF）等方式运行，只是速度会慢一些。

---

## 软件安装

去 GitHub 下载 **ComfyUI 官方版本**。

Windows 用户推荐下载官方提供的 **Standalone（独立版）**。

解压后，直接运行：

```
run_nvidia_gpu.bat
```

浏览器会自动打开 ComfyUI 的操作界面。

---

## 下载模型（Model）

ComfyUI 本身只是一个工作流平台，它并不自带绘画模型，因此第一次使用需要下载模型。

目前最常见的模型来源包括：

* Civitai（C站）
* Hugging Face

下载后的模型文件（通常是 `.safetensors`）放到：

```
ComfyUI/models/checkpoints
```

以后随着学习深入，你还会接触：

* LoRA
* VAE
* ControlNet
* Upscale Model
* Embedding
* Text Encoder

它们分别放在 models 目录下对应的子文件夹中。([ComfyUI][3])

---

# 阶段二：必须掌握的核心节点（对应刚才讲的原理）

第一次打开 ComfyUI，你会看到默认的 Workflow（工作流）。

不要害怕，这些节点其实就是把我们刚刚介绍的 AI 画图流程拆解成一个个独立模块，然后用连线把它们连接起来。

理解了这几个节点，你就理解了整个 AI 图片生成流程。

---

## Load Checkpoint（加载模型）

这是整个工作流的起点。

它负责加载 AI 绘画模型。

右侧通常会输出三个重要组件：

**MODEL**

负责执行扩散过程中的去噪计算。

在传统 Stable Diffusion 中，它主要就是 UNet；而在新一代模型中，内部结构可能有所不同，但作用依然是完成图像生成。

**CLIP**

负责理解文字，把提示词转换成 AI 能理解的语义向量。

**VAE**

负责在潜空间（Latent）和真正图片（Pixel）之间进行转换。

可以把它理解成图片的"压缩器"和"解压器"。

---

## CLIP Text Encode（文字编码节点）

连接到 Load Checkpoint 输出的 CLIP。

通常需要两个：

一个输入：

**Positive Prompt（正向提示词）**

告诉 AI：

> 我要画什么。

另一个输入：

**Negative Prompt（反向提示词）**

告诉 AI：

> 不要画什么。

最终输出的是：

**Conditioning（条件）**

它就是 AI 绘画时参考的"设计说明书"。

---

## Empty Latent Image（创建潜空间画布）

很多新人误以为这里创建的是一张空白图片。

实际上，它创建的是：

**一块随机噪声组成的潜空间（Latent）画布。**

同时也决定：

* 图片宽度
* 图片高度

可以理解成：

给 AI 准备了一块还没有绘制的画布，并规定好了最终图片尺寸。([ComfyUI][2])

---

## KSampler（采样器）

这是整个工作流的核心，也是 AI 真正开始"画画"的地方。

它负责把随机噪声一步一步去掉，最终生成符合提示词要求的图像。

它需要接收：

* MODEL（负责去噪）
* Positive Conditioning（正向提示）
* Negative Conditioning（反向提示）
* Latent Image（潜空间画布）

几个最重要的参数包括：

**Steps（步数）**

表示去噪多少次。

通常步数越多，细节越丰富，但速度越慢。

**CFG Scale（提示词引导强度）**

决定 AI 有多"听你的话"。

数值太低容易自由发挥；

数值太高可能导致画面不自然。

**Sampler / Scheduler（采样算法）**

决定 AI 去噪采用哪一种数学方法。

不同算法速度、风格、稳定性都会有所不同。

KSampler 输出的仍然不是图片，而是：

**Latent（潜空间图像）**

---

## VAE Decode（VAE 解码）

这里负责把 KSampler 输出的 Latent 转换成真正的图片。

简单来说：

它就是把"压缩版图片"解压成我们肉眼能够看到的 PNG 图像。

---

## Save Image（保存图片）

最后一步。

把解码后的图片显示出来，并保存为 PNG。

值得一提的是：

ComfyUI 会把当前 Workflow 自动保存到图片元数据（Metadata）中。

以后只要把这张图片重新拖回 ComfyUI，就能自动恢复生成它的整个工作流，非常方便分享和复现。([ComfyUI][4])

---

# 阶段三：学会 Workflow（工作流）思维

很多人刚开始学习 ComfyUI，总是在记各种节点。

其实真正需要学习的，不是节点，而是：

**Workflow（工作流）思维。**

一个 Workflow，就是一张完整的 AI 生成流程图。

节点代表不同功能；

连线代表数据流向。

以后无论生成：

* 图片
* 视频
* 音频
* 3D
* AI Agent

本质上都是不同节点组合形成的 Workflow。

所以，学会阅读别人分享的 Workflow，比死记节点更重要。([ComfyUI][4])

---

# 阶段四：需要进阶学习的核心技术

当你能够跑通默认工作流之后，就可以逐步学习下面这些能力。

---

## ComfyUI Manager（插件管理器）

建议第一个安装。

它可以帮助你：

* 安装 Custom Nodes（自定义节点）
* 下载缺失模型
* 更新插件

以后几乎所有第三方功能，都离不开它。

---

## LoRA（低秩微调模型）

作用：

让 AI 学会某一种固定能力。

例如：

* 固定画风
* 固定人物
* 固定服装
* 固定角色脸型

通常会在模型之后加载一个 LoRA 节点，再送入后续流程。

---

## Img2Img（图生图）

除了文生图（Text to Image），图生图也是最常用的能力之一。

它允许 AI 在参考原图的基础上重新绘制。

最重要的参数就是：

**Denoise（重绘强度）**

数值越小，越接近原图；

数值越大，AI 改动越明显。([ComfyUI][5])

---

## Inpainting（局部重绘）

如果：

整体都很好，

只有手画崩了，

或者脸不满意，

就可以使用遮罩（Mask）把需要修改的区域盖住。

AI 只会重新生成这一小块区域，而不会影响其它部分。

---

## ControlNet（控制网）

作用：

精准控制构图。

例如：

给 AI 一个：

* OpenPose（人体骨架）
* Canny（边缘图）
* Depth（深度图）
* LineArt（线稿）

AI 就会严格按照这些结构进行绘制。

它更像是在提示词之外，再增加一份"结构说明书"。

---

## Upscale（高清放大）

AI 直接生成超高分辨率图片，容易出现：

* 多手
* 多腿
* 结构崩坏

因此，更推荐的流程是：

先生成中等分辨率图片（例如 SD1.5 的 512×512，或 SDXL 的 1024×1024），

再利用 Latent Upscale 或 AI 放大模型放大图片，

最后进行一次轻微重绘，提高整体细节和清晰度。

---

# 阶段五：不断积累自己的 Workflow

当你掌握以上内容后，你会发现：

真正决定 ComfyUI 水平的，不是会多少节点，而是拥有多少高质量 Workflow。

优秀的 Workflow 往往融合了：

* 多种模型
* 多个 LoRA
* 多种控制方式
* 放大流程
* 局部修复
* 自动化处理

随着经验不断积累，你会逐渐建立属于自己的 Workflow 库。

而这，也正是 ComfyUI 最大的魅力——它不仅仅是一个 AI 绘图软件，更是一个可以自由组合、自由扩展的生成式 AI 工作流平台。([ComfyUI][4])

[1]: https://docs.comfy.org/?utm_source=chatgpt.com "ComfyUI Official Documentation - ComfyUI"
[2]: https://docs.comfy.org/tutorials/basic/text-to-image?utm_source=chatgpt.com "ComfyUI Text to Image Workflow - ComfyUI"
[3]: https://docs.comfy.org/get_started/first_generation?utm_source=chatgpt.com "Getting Started with AI Image Generation - ComfyUI"
[4]: https://docs.comfy.org/development/core-concepts/workflow?utm_source=chatgpt.com "Workflow - ComfyUI"
[5]: https://docs.comfy.org/tutorials/basic/image-to-image?utm_source=chatgpt.com "ComfyUI Image to Image Workflow - ComfyUI"



# 如何上手 ComfyUI？（全套实操指南） - v2




基于最新的行业发展（特别是进入 2026 年的 AI 生态），ComfyUI 已经不再仅仅是“用来跑 Stable Diffusion 的工具”，而是进化成了一个**通用的生成式 AI 工作流平台（AI Workflow Platform）**。无论是跑最火的 Flux、SD3，还是 CogVideoX、Hunyuan 等视频模型，甚至音频与 3D 生成，ComfyUI 都是目前的最优解。

以下是为你量身定制的、符合当前最新生态的 ComfyUI 学习路线与操作指南：

---

# 🚀 ComfyUI 零基础到进阶全案指南

**为什么选择 ComfyUI？**
相比 Automatic1111 等 WebUI 更偏向于“封装好的图形界面”（容易上手但限制较多），ComfyUI 将整个推理流程**节点化（Node-based）**。它是目前学习扩散模型（Diffusion Models）工作原理最好的工具，适合深入理解模型机制并搭建极其复杂的工业级自动化工作流。

---

## 阶段一：前期准备与基础认知

**1. 硬件要求（显存 VRAM 是核心）**
生成式 AI 对显存的要求差异很大，强烈建议使用 NVIDIA（英伟达）显卡：
*   **入门级 (4GB - 6GB)**：可以流畅跑传统的 SD 1.5 模型。
*   **进阶级 (8GB - 12GB)**：能够较好地体验 SDXL 模型，勉强运行量化版的 Flux。
*   **发烧级 (16GB - 24GB及以上)**：跑当前主流的 Flux 模型、复杂的视频生成模型（Video Generation）的最佳配置。

**2. 软件安装**
*   前往 GitHub 搜索 `ComfyUI`，下载官方提供的 **Windows Standalone（独立免安装压缩包）**。
*   解压后，双击 `run_nvidia_gpu.bat` 即可启动，浏览器会自动打开操作界面。

**3. 下载与理解模型生态**
现在的模型已经不再是单一的 `.safetensors` 文件。你需要将下载的模型放入 `ComfyUI/models/` 下的对应文件夹。常见模型生态包括：
*   **Checkpoint / Diffusion Model**：核心大模型（如 Flux, SDXL）。*注：现在的模型格式越来越多样，ComfyUI 已经全面支持 Checkpoint、单独的 UNet/Diffusion Model 甚至 GGUF 格式。*
*   **LoRA**：微调模型，用于固定特定人物脸型、画风或服装。
*   **Text Encoder (如 CLIP, T5)**：文字编码器，负责把你的提示词翻译给 AI。
*   **VAE**：潜空间与像素空间的“智能压缩/解压器”。
*   **ControlNet / IPAdapter**：用于精准控制画面结构或参考图风格的模型。

---

## 阶段二：必须掌握的 7 个核心节点

第一次打开 ComfyUI，你会看到默认的文生图工作流。不要怕，理解以下 7 个核心节点，你就掌握了扩散模型的命脉：

1.  **Load Checkpoint（加载大模型）**：
    它的右侧有三个输出口：**MODEL**（扩散模型核心，负责去噪预测，早期是UNet，现在可能是Transformer）、**CLIP**（文字编码器）和 **VAE**（解压器）。
2.  **CLIP Text Encode（文字编码）**：
    连接大模型的 CLIP 出口。你需要两个：一个写**正向提示词（你要什么）**，一个写**反向提示词（你不要什么）**。它输出的是 `Conditioning（条件）`，也就是给 AI 的指导书。
3.  **Empty Latent Image（空潜空间图像）**：
    它的作用是**创建一个纯随机噪声的潜空间（Random Latent）**，同时由你在这里定义最终生成图片的尺寸（宽x高）。
4.  **KSampler（采样器 - 心脏节点）**：
    负责执行核心的“去噪”工作。它接入 MODEL（工人）、Conditioning（图纸）和 Latent（噪声画布）。
    *注意：KSampler 真正输出的是 **Latent Image（潜空间微缩图）**，肉眼还看不懂，它不是 PNG 图片！*
5.  **VAE Decode（VAE 解码）**：
    接入 KSampler 吐出来的 Latent，以及大模型里的 VAE。把它 **“解压”** 成肉眼可见的真实像素图片（Pixel）。
6.  **Save Image（保存图像 - 魔法节点）**：
    显示并保存 PNG 图片。**更核心的是：它会把当前整个 Workflow（连线逻辑）以 JSON 格式静默写入这张 PNG 的元数据（Metadata）中。** 以后你只要把这张图片拖回 ComfyUI 界面，整个工作流就会瞬间完美复原！

---

## 阶段三：真正的新手进阶路线图

不要一开始就去学最难的控制网，按照以下顺序循序渐进，最符合当前的 AI 创作流：

1.  **ComfyUI Manager（必备插件）**：第一步必须安装！它是 ComfyUI 的“应用商店”，一键帮你安装缺失节点、更新软件、下载模型。
2.  **LoRA（风格微调）**：在 Load Checkpoint 和 KSampler 之间串联 `Load LoRA` 节点，学会如何改变画风。
3.  **Img2Img（图生图）**：舍弃 Empty Latent，使用 `Load Image` + `VAE Encode` 把你准备好的参考图压缩成 Latent，送给 KSampler 去噪重绘。
4.  **Inpainting（局部重绘）**：结合遮罩（Mask），让 AI 只修改画错的手指或给人物换衣服。
5.  **ControlNet（控制网）**：提取图片的线稿、深度图或人体骨架（OpenPose），强行规定 AI 的构图和人物姿势。
6.  **Upscale（高清放大）**：学习 Latent 潜空间放大或 Ultimate SD Upscale 插件，突破显存限制生成 4K 高清大图。
7.  **IPAdapter（垫图神器）**：不需要提示词，直接喂给 AI 一张图，让 AI 完美复刻原图的风格、色彩或人物特征。
8.  **Video / AnimateDiff（视频生成）**：进军动态领域，结合 Video Helper Suite 插件跑通视频模型。

---

## 阶段四：跨越新手墙 —— 建立“Workflow (工作流) 思维”

真正掌握 ComfyUI，**不是死记硬背每个节点，而是学会阅读和设计 Workflow**。这是 ComfyUI 最大的优势：

1.  **学会“抄作业”**：去开源社区（如 Civitai, ComfyWorkflows）下载别人做好的高质量图片，直接拖进你的 ComfyUI。如果飘红报错，就点开 Manager 选 `Install Missing Custom Nodes` 一键补齐缺失插件。
2.  **看懂“数据流”颜色**：
    *   🟣 **紫色线**：传 Latent（潜空间数据）。
    *   🟡 **黄色线**：传 Conditioning（提示词控制条件）。
    *   🔵 **蓝色线**：传 Image/Pixel（真实的像素图像）。
    顺着颜色的流动，你就能读懂数据是怎么被加工的。
3.  **模块化与排版整理**：
    *   使用 **Group（群组）** 把复杂的节点框起来分类（如：提示词区、采样区、放大区）。
    *   使用 **Reroute（路由节点）** 让满屏乱飞的线缆变得像电路板一样整洁。
    *   使用 **Primitive Node（基础节点）** 把 Seed 或步数参数单独拎出来做成控制面板。

---

## 阶段五：拥抱强大的插件生态（Custom Nodes）

目前真正决定 ComfyUI 水平的是社区开发者贡献的第三方插件。当你度过新手期，你一定会用到以下几个“装机必备”插件包：

*   **ComfyUI Impact Pack**：提供了极其强大的自动化修脸（Face Detailer）、遮罩增强功能。
*   **Efficiency Nodes**：把 Load 模型、KSampler 等多个基础节点缝合成一个超级节点，极大精简连线。
*   **rgthree-comfy**：提供了高级的节点开关（Bypass）、路由整理工具，中大型工作流必备。
*   **Comfyroll Studio**：提供极其丰富的排版、基础数学运算、文本处理节点。
*   **Video Helper Suite (VHS)**：加载和保存视频、GIF，做 AI 视频的核心基础插件。

**总结：**
不要被 ComfyUI 满屏的“蜘蛛网”吓倒。把它当成一套**可视化的编程乐高**。从最基础的文生图（6个节点）开始，慢慢往里面加 LoRA 积木、加 ControlNet 积木。当你熟练掌握了这些积木的数据流向，你就能搭建出全世界最顶尖的、完全属于你自己的自动化 AI 创作流水线。

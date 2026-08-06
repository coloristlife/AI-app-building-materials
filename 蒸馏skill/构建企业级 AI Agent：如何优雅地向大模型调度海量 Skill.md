# AI 生成



# 构建企业级 AI Agent：如何优雅地向大模型调度海量 Skill？

在现代 AI Agent（智能体）开发中，我们常常面临一个关键的工程挑战：当你拥有几十个、甚至上百个结构化技能（Skill）时，如何让 AI 在极短的时间内，精准地选出最合适的那个技能来执行任务？

如果你只是简单粗暴地把所有 Skill 的全文塞进大模型的提示词（Prompt）里，或者直接把全文丢进向量数据库（Vector DB）做 RAG 检索，你很快就会撞上两堵墙：**Token 上下文溢出**，以及致命的**语义污染（Semantic Pollution）**。

本文将深入探讨 AI Agent 技能调度的核心架构，并解析四种主流的“海量 Skill 投喂”方案。

---

## 一、 核心痛点：为什么不能“全文检索”？（语义污染现象）

在很多初级 RAG 系统中，开发者习惯将整个技能文档（包含标题、描述、执行步骤、案例等）直接进行 Embedding（向量化）。这会导致严重的误唤醒。

举个例子，假设你的技能库里有两个 Skill：
*   **Skill A【时间管理】**：其中在“案例”部分提到了 *“例如：如何安排写销售文案的时间表、如何拜访客户...”*
*   **Skill B【销售文案公式】**：专门教 AI 怎么写销售文案。

当用户输入：*“帮我写一篇销售文案”* 时，如果系统做的是全文 Embedding，向量模型并不知道“案例”只是案例。它只提取到了 `销售`、`文案` 等特征词，最终极有可能错误地把 **Skill A【时间管理】** 给召回并喂给了大模型。

这就是“语义污染”。要解决这个问题，现代 Agent 架构必须遵循一个根本原则：

> **索引与内容解耦（Index-Payload Decoupling）**：
> 真正应该被 Embedding 和比对的，是描述技能用途的“意图（Intent）”，而不是技能的“正文（Payload）”。

像 `cangjie-skill` 等先进的技能框架中，专门设计了 **A2 — 触发场景（Future Trigger）** 模块，其核心目的就是为了提供一个纯净的、低噪声的**意图描述**，专门用于检索比对。

---

## 二、 破解之道：海量 Skill 调度的四种核心架构

围绕着“解耦”思想，在真实的 AI 工程中，通常采用以下 4 种架构来实现精准调度：

### 方案一：意图索引与文档库映射（Keyed Retrieval / Intent Index）
这是在使用向量数据库时最稳妥的做法。我们将技能拆分为索引键（Key）和实际内容（Value），在业界也常被称为 `Metadata Lookup` 或 `Intent Index + Document Store`。

*   **构建索引（Key）**：我们只提取技能的“触发场景（如 A2 模块）”和“标签”，将这些纯粹的意图描述转化为向量存入数据库。
*   **内容存储（Value）**：完整的技能文本（包含执行步骤 E、边界 B 等）作为 Payload，存在常规数据库或对象存储中，不参与相似度计算。
*   **运行逻辑**：当用户输入需求时，系统只拿用户的输入去和 Key（触发场景）做比对。一旦命中，直接根据引用 ID 提取出对应的完整 Skill 文本，动态注入到 LLM 的上下文中。

### 方案二：大模型原生工具调用（Function Calling / Tool Schema）
如果你使用的是 OpenAI (GPT-4) 或 Claude 的原生 API，可以利用其强大的 Tool Calling 机制实现隔离。

*   **运行机制**：在 API 请求中，我们不给 AI 传技能全文，而是传一个结构化的 `Tool Schema`。这个 Schema 包含了：
    *   `Tool Name`（工具名称）
    *   `Description`（描述：这里直接填入 A2 触发场景）
    *   `Parameters`（参数结构）
*   **精准触发**：AI 脑子里只有这些高度概括的 Schema。真正参与工具选择的是整个 Schema（其中 Description 起决定性作用）。
*   **按需加载**：当用户的输入命中了 Description，LLM 会决定 `call tool`。此时，具体的 Tool 设计将接管流程：你可以让 Tool 返回一段 SQL 结果，也可以让 Tool 读取本地的完整 Skill 文档（Payload）并将其作为结果返回给 LLM，让 LLM 继续进行下一步的推理和执行。

### 方案三：两阶段路由映射（Router-Planner-Executor 模式）
这是一种轻量级、无需复杂向量库、仅靠 Prompt 就能实现的经典多智能体（Multi-Agent）协作模式。

*   **Routing Index（路由目录）**：只给大模型提供一份极简的 `INDEX.md` 目录（仅包含每个技能的名称和一句意图描述）。
*   **运行逻辑**：
    1.  **意图检测（Router Agent）**：前台 AI 阅读 `INDEX.md`，分析用户意图，只输出一个决定：“应该使用 `sales_skill.md`”。
    2.  **技能执行（Executor Agent）**：系统通过脚本拿到这个文件名，去本地读取完整文本，然后新开一个干净的对话窗口，把用户问题和完整的技能文本一起交给执行 Agent，完成最终任务。

### 方案四：结构化技能注册与延迟加载（Skill Registry & Lazy Load）
这是目前最前沿的企业级 Agent 平台（如 OpenAI Agents SDK、Anthropic 智能体实践）中最常见的成熟模式。它淡化了纯粹的向量检索，走向了更确定性的系统工程。

*   **注册表（Registry）**：所有的 Skill在系统启动时，都会向系统注册自己的元数据：
    ```json
    {
        "id": "sales_5_steps",
        "name": "五阶段销售公式",
        "description": "用于编写产品介绍、销售信...",
        "tags": ["copywriting", "sales"],
        "input_schema": {...},
    }
    ```
*   **运行逻辑**：系统的核心大脑（Planner Agent）掌握着这个注册表。当复杂任务到来时，Planner 会统筹规划，决定调用哪个/哪几个 Skill。
*   **延迟加载（Lazy Load）**：只有在 Planner 明确下达了调用指令后，系统才会把该 Skill 庞大的具体执行步骤（Execution 模块）加载进内存。这极大地优化了系统的响应速度和 Token 开销。

---

## 三、 总结：重新认识“结构化技能”

在了解了上述架构后，我们就能明白为什么像 `cangjie-skill` 这样的项目，要煞费苦心地把一篇读书笔记拆解成 `A2 (触发场景)`、`E (执行步骤)`、`B (边界)` 等模块。

这种设计的终极目标，就是提供一个**高质量、低噪声的意图描述（Intent Description）**。这个描述既可以作为 RAG 的意图索引，也可以作为 API 的 Tool Description，还可以作为 Router Agent 的路由依据，甚至是 Planner 的记忆图谱。

**现代 AI Agent 的核心原则不是“全文检索”，而是“索引与内容解耦”。**

系统应尽量使用简洁、低噪声的元数据进行检索或路由调度；在命中之后，再“按需加载（Lazy Load）”完整的执行逻辑。只有这样的工程架构，才能彻底告别语义污染，让你的 AI 助手即使挂载了上千个技能，依然能保持敏锐、精准和高效。


===
**必须使用具备“Agent（智能体）工作流”或“工具调用（Tool Calling）”能力的平台或工具链。**

普通的对话框（比如早期的网页版 ChatGPT 或最基础的网页版 Claude 对话框）是**无法自动处理**这种复杂依赖关系的。

如果一个 Skill（比如 A）依赖另一个 Skill（比如 B），AI 必须具备一种**“停下来 -> 去找 B -> 把 B 读进脑子 -> 继续干活”**的自动化能力。这种能力被称为 **Agentic 循环（如 ReAct 模式）**。

为了让这种带有复杂依赖（`depends-on`、`composes-with`）的 Skill 真正跑起来，目前业界通常使用以下三类“专门的平台或环境”：

### 1. AI 编程 IDE 或 CLI 工具（最无缝的体验）
你在第一条问题中提到了 `cangjie-skill` 是安装到 **Cursor** 或 **Claude Code** 目录下的，这正是因为它们在底层做了极其强大的依赖图谱解析：
*   **Cursor / Windsurf**：当你把这些 Skill 放在 `.cursor/rules` 文件夹下时，Cursor 的后台搜索引擎会自动建立依赖索引。当 AI 执行 Skill A 发现缺少 Skill B 时，Cursor 的原生 RAG 引擎会自动把 B 的文件也“挂载”到上下文中，完全不需要你手动干预。
*   **Claude Code**：这是 Anthropic 官方出的命令行 Agent，它天生就是为了读取本地目录、执行复杂多步任务而设计的，能完美处理这种文件间的关联。

### 2. 无代码 Agent 编排平台（适合非程序员构建企业级应用）
如果你不是写代码，而是想做一个“营销内容自动生成系统”，你需要使用类似下面这些平台：
*   **国内：Dify、Coze（扣子）、FastGPT**
*   **国外：LangFlow、Flowise**
*   **怎么用**：在这些平台上，你可以把所有的 Skill 做成一个个独立的“工具（Tools）”或“节点（Nodes）”。你可以配置一个**路由节点（Router）**，当它发现某个任务需要 A 和 B 组合（`composes-with`）时，它会自动并行调用 A 节点和 B 节点，然后把结果汇总给最后一个节点来生成最终答案。

### 3. 代码级 Agent 框架（适合高级开发者）
如果你在开发底层的 AI 软件，你会用代码来管理这些依赖：
*   **框架**：LangChain、LlamaIndex、CrewAI、OpenAI Swarm 等。
*   **怎么用**：你会写一段代码（也就是我们上一篇博文提到的 Planner / Registry）。当 LLM 决定使用 Skill A 时，你的代码逻辑会去解析 Skill A 的 JSON 配置文件，读取到 `depends-on: ["Skill_B"]`，然后**你的代码会自动把 Skill B 也加载进来**，打包发给大模型。

---

### 如果我只有网页版的 Claude（Claude.ai）或 ChatGPT 怎么办？

如果你手头只有网页版，可以通过它们的**高级功能**勉强实现，但会有局限：

*   **Claude 的 Projects（项目）功能**：你可以建一个 Project，把 `INDEX.md` 和所有具体的 Skill Markdown 文件上传到 Knowledge（知识库）里。并在 Custom Instructions（系统提示词）里写明：*“执行任务时，请先查阅 INDEX.md 寻找需要的技能文件。如果技能文件中标明了 depends-on 依赖，请务必使用搜索工具去读取对应的依赖文件后再输出。”* Claude 3.5 Sonnet 的逻辑非常强，它通常能按照这个指令自己去翻找文件。
*   **ChatGPT 的 GPTs**：同理，把技能文件上传到 Knowledge，要求它在回复前先用文件搜索工具（File Search）读取相关依赖。

### 总结

单纯的大语言模型（LLM）只是一个**“最强大脑”**，它没有手脚，也没有翻找文件夹的动作。

遇到带有复杂依赖关系的 Skill 网络：
*   **LLM 负责“看懂”**：“哦，这里写了 `depends-on: feature-to-benefit`，所以我现在需要去用那个技能。”
*   **平台（Cursor / Dify / 代码框架）负责“跑腿”**：“好的老大，我去把 `feature-to-benefit` 这个文件拿过来给你看。”

所以，**是的，要让这套高度工程化的技能库发挥 100% 的威力，你必须脱离简单的聊天框，走向 Agent 平台（如 Coze/Dify）或 AI 增强型工作区（如 Cursor / Claude Projects）。**
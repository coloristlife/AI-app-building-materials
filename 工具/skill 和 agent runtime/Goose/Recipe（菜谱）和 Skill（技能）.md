在 Goose 中，**Recipe（菜谱）**和 **Skill（技能）**并不是“谁比谁更好用”的关系，而是**设计理念和使用场景完全不同**的两个核心维度。

Goose 的开发团队曾在 GitHub 上的讨论中明确表示：“刻意保留两者的区别是有意为之的”。简单来说，**Recipe 是“你强制 Agent 去做的事情”，而 Skill 是“Agent 自己决定何时使用的工具箱”。**

以下是针对你问题的详细解答：

### 1. 两个文件的使用场景是什么？为什么要保留两个？

*   **Recipe（菜谱）—— 核心场景：确定性的、强制的自动化工作流**
    *   **定义**：Recipe 是一个包含明确指令、输入参数和所需扩展（Extensions）的 YAML 文件。
    *   **用法**：你通常会在命令行或 CI/CD 环境中“无头”（Headless）或一键执行它（例如 `goose run --recipe code-review.yaml`）。
    *   **场景**：当你需要 Goose **每次都按照一模一样的标准流程**完成某个特定任务时使用。比如：自动总结项目里的每日日志、运行固定的预发布检查脚本、批量转换某种格式的数据等。它就像是写给 AI 的“自动化脚本”。
*   **Skill（技能）—— 核心场景：跨会话的背景知识和动态能力**
    *   **定义**：Skill 遵循开放的 Agent Skills 标准，通常是一个包含 YAML 元数据和 Markdown 文本的 `SKILL.md` 文件。
    *   **用法**：你不需要显式地去“运行”它，它潜伏在你的自然语言对话中。
    *   **场景**：当你希望给 Goose **注入特定领域知识或团队规范**时使用。比如：你们公司内部私有 API 的调用文档、你们团队独特的 TypeScript 报错处理指南、或者特定的部署 checklist。在使用普通对话模式时，如果遇到相关问题，Goose 会自己去调取这些知识。

**为什么要保留两个？**
因为 AI 既需要**自主性**（通过 Skill 动态解决你随口问的问题），也需要**可重复性**（通过 Recipe 成为流水线上稳定、不偏离轨道的打工人）。强行用对话来触发固定流程既慢又容易出错，而强行把所有知识塞进一次性脚本里又失去了 AI 的灵活性。

### 2. Goose 里可以有多个 Skill 文件吗？

**完全可以，而且非常鼓励配置多个。**

Goose 支持开放的 Agent Skills 标准。它会自动扫描并加载多个目录下的技能（例如项目级目录 `.goose/skills/`、`.claude/skills/` 或是全局目录 `~/.claude/skills/`、`~/.cursor/skills/`）。

通常，目录结构会按照功能分类，每个技能独占一个文件夹，例如：
```text
.goose/skills/
  ├── internal-api-docs/
  │   └── SKILL.md
  ├── deploy-checklist/
  │   └── SKILL.md
  └── db-migration/
      ├── SKILL.md
      └── check_db.sh
```

### 3. Goose 会自动匹配最合适的 Skill 吗？如何匹配的？

是的，Skill 最大的特点就是 **“Agent-discoverable”（对智能体自发现）**。

*   **按需动态加载**：Goose 并不会一开始就把你所有的 Skill 几万字的内容全塞进对话上下文（这样既浪费 Token 成本，又会稀释 LLM 的注意力）。
*   **大模型充当“路由”**：启动时，Goose 的插件引擎只会提取所有 `SKILL.md` 的 YAML 头部信息（Frontmatter，非常轻量）。当用户输入 prompt 时，大语言模型（LLM）会评估当前任务，自动决定：“为了回答这个问题，我需要加载 `internal-api-docs` 这个技能的完整内容来看看”。
*   **信心指数（Confidence/Context Similarity）**：模型判断相关性后，才会在后台自动读取所需的 `SKILL.md` 展开阅读。

### 4. 命名规则有规定吗？主要以 Description 为准吗？

有非常明确的规定和匹配逻辑：

1.  **文件名的强制硬性规定**：技能的入口文件**必须**命名为 **`SKILL.md`**（因为 Goose 支持跨生态的通用 Agent Skills 规范，只有识别到 `SKILL.md` 才会当做技能解析）。至于外层的文件夹名字，你可以自由命名（如 `my-react-skill`）。
2.  **匹配主要以 `description` 为准**：在 `SKILL.md` 文件的最顶端，必须有一段 YAML 格式的元数据（Frontmatter），如下所示：
    ```markdown
    ---
    name: square-integration
    description: How to integrate with our Square account. Use this whenever the user asks to create customers, handle payments, or parse Square webhooks.
    ---
    # Square Integration
    (下方是具体的 Markdown 知识内容...)
    ```
    *   **name**：提供给系统和用户看的简短标识。
    *   **description**：**这是 LLM 能否准确匹配到这个 Skill 的绝对核心**。你在这里写的内容，就是大模型用来决定“要不要调取这个技能”的判断依据。

**最佳实践**：在写 `description` 时，不要只写一句“数据库文档”，而是要写得像给 AI 的“触发说明书”（Trigger prompts），比如：*“当用户要求修改数据库 Schema、或者遇到与 PostgreSQL 迁移相关的报错时，请加载此技能。”* 这样 Goose 在对话中匹配得会非常精准。
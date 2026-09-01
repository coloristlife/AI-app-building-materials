
https://www.novelcrafter.com/help/docs/codex/codex-tracking


> **控制 Codex 条目在你的项目（Project）中如何被追踪、识别以及高亮显示。**

在 Novelcrafter 中，“追踪（Tracking）”标签页赋予你完全的控制权，决定应用如何检测和高亮显示各个 Codex 条目。同时，这也是你配置该条目**如何与 AI 进行交互**（即：是否以及在何时将该条目作为上下文喂给 AI）的核心区域。
![[Pasted image 20260813192257.png]]

---

## 一、 核心功能模块详解

### 1. 追踪与匹配开关（Tracking / Matching）
“通过名称/别名追踪此条目（Track this entry by name/alias）”勾选框决定了 Novelcrafter 是否会在你的正文中主动查找该条目的名称及任何别名。

* **当追踪开启时（默认状态）：**
  * 条目名称及其别名在你的**手稿（Manuscript）**、**大纲/计划（Plan）**
  * 和**片段（Snippets）** 中会被**下划线高亮**。
  * 系统会统计提及次数，并显示在 Codex 标题栏的“提及追踪器（Mentions Tracker）”中。
  * 该条目会出现在出场热力图（Appearance Heatmap）中。
* **当追踪关闭时：**
  * 下划线高亮消失。
  * 该条目将被排除在提及热力图之外。

> 💡 **实用小贴士（Extra Tip）：**
> 你可以在写作过程中随时切换追踪状态。例如：在**初稿创作时**开启追踪，以便随时发现遗漏的 Codex 设定；而在**精修或校对时**将某些条目的追踪关闭，避免过多的下划线分散你的注意力。

---

### 2. 自动复数形式识别（Auto-Pluralisation）
对于设置为**英语变体**的小说项目，Novelcrafter 会自动匹配条目名称及别名的常见复数形式。
* 例如：名为“Goblin（哥布林）”的条目，即使你没有将其复数形式单独添加为别名，手稿中出现的“Goblins”也会被自动识别。
* **例外情况**：更复杂的复数变形（例如 `Wolf` $\rightarrow$ `Wolves`）无法被自动匹配，但你可以根据需要手动将其添加为别名。

---

### 3. 大小写敏感匹配（Case-Sensitive Matching）
默认情况下，Novelcrafter 采用**大小写不敏感**的方式匹配条目名称和别名——例如名为“Charm（查姆/魅力）”的条目，也会匹配手稿中的小写“charm”。
如果你的条目名称恰好是一个普通的日常单词（容易发生误判），你可以开启大小写敏感匹配：
1. 打开该 Codex 条目。
2. 切换到 **Tracking（追踪）** 标签页。
3. 勾选 **Case-sensitive matching（大小写敏感匹配）**。
* **效果**：只有当正文中的词汇大小写与名称（或别名）完全一致时，才会被高亮和计数。

> 💡 **实用小贴士：**
> 这对于名称是普通名词的条目非常有用——例如名字叫“Red（红色/雷德）”的角色，或者名字叫“Storm（风暴）”的地点。

---

### 4. 排除名单（Exclusion List）
排除名单允许你指定某些**不应被计入**该条目提及次数的词汇或短语，哪怕它们在字面上与条目名称或别名完全一致。
* **典型场景**：如果你的角色名字叫“Will（威爾）”，但你并不希望文章中每一次出现助动词“will（将要/会）”都被统计为对该角色的提及，你可以选择开启大小写敏感，或者将常见的“误杀”短语加入排除名单。
* **添加方式**：
  1. 打开 Codex 条目，进入 **Tracking** 标签页。
  2. 在 **Exclusions（排除项）** 输入框中，输入你想排除的词汇或短语，并用逗号隔开。
  3. 排除项的匹配规则与条目名称相同（默认大小写不敏感，若开启了大小写敏感则严格区分）。

---

### 5. AI 上下文集成（AI Context）
AI 上下文设置用于控制：**该 Codex 条目的信息是否、以及在何时作为 Prompt（提示词）上下文的一部分发送给 AI。**

| 选项 (Option) | 行为逻辑 (Behaviour) |
| :--- | :--- |
| **Always include（总是包含）** | 无论当前文本中是否检测到该条目，它都会被强制加入 AI 上下文。（注：该选项在旧版本中被称为 Global entry / 全局条目） |
| **Include when detected（检测到时包含）** | **（默认）** 当在选定文本、场景节拍（Scene Beats）或聊天消息中检测到该条目的名称或别名时，它会被包含进 AI 上下文。 |
| **Don’t include when detected（检测到时不包含）** | 即使在文本中检测到了该条目，它也会被从 AI 上下文中排除。不过，当它被**手动添加**为场景上下文，或通过**关联关系（Relation）**被引述时，依然可以被拉取进来。 |
| **Never include（从不包含）** | 绝对不会发送给 AI。非常适用于私人笔记、剧透内容或仅供人类参考的条目。 |

> ℹ️ **重要提示：**
> 关闭“追踪功能（Tracking）”也会同时阻止系统在“检测到时包含（Include when detected）”选项中对该条目的识别。如果你希望 AI 能够读取该条目，但又不想手稿里到处都是下划线高亮，建议使用 **Always include（总是包含）** 并配合关闭追踪，或者灵活运用各项配置。

---

## 二、 关键技术与底层概念解释

为了更好地理解上述文档，我们需要剖析 Novelcrafter 在架构上采用的几个核心技术概念：

1. **实体识别与正则匹配引擎（Entity Recognition & Regex-based Matching）**
   * **技术本质**：Novelcrafter 的 Tracking 功能并不是简单的全文本暴力检索，而是一个基于配置规则的**前端/文本解析过滤器**。它在后台维护了一个动态的词表（包含主名与 Aliases 别名），并利用自动复数转换、大小写控制和 Exclusion List 过滤机制，在作者键入或导入文本时进行实时的语法标记（Span Highlighting）。
2. **上下文检索增强（RAG - Retrieval-Augmented Generation）的裁剪与注入**
   * **技术本质**：在“AI Context”中，系统扮演了极简版的 RAG 角色。大语言模型（LLM）的 Token 窗口有限，不可能把整个世界观（Codex）全部无脑塞给 AI。Novelcrafter 通过 **“检测-触发-动态拼装（Detect-Trigger-Assemble Pipeline）”** 技术：
     * **Always include** 属于静态全局注入（Static Global Injection）。
     * **Include when detected** 属于动态事件驱动注入（Dynamic Event-Driven Retrieval）。
     * 这种分级控制有效避免了 Token 的浪费，并精准保证了 AI 在生成对应情节时，只拥有“当前视野内应该知道”的信息，防止发生因剧透或信息过载导致的逻辑混乱。
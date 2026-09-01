
> **在整部小说中使用别名和昵称来追踪你的 Codex 条目。**

https://www.novelcrafter.com/help/docs/codex/aliases

无论你是否使用 AI，别名对于保持 Codex 条目的条理清晰都至关重要。无论你是用它们来存储昵称、分身（Alter-egos），还是与该 Codex 条目相关的头衔/称号，这些词汇都会在 Novelcrafter 的手稿（Manuscript）、大纲（Plan）以及所有的片段/聊天（Snippets/chats）中被高亮显示，从而让你能够追踪它们的提及情况。

**如何查看你的 Codex 条目或其任何别名的提及记录：**
1. 打开 Codex 条目。
2. 切换到 **Mentions（提及）** 标签页。
3. 点击下方的各个标签页，查看你的 Codex 条目在哪里被提及。

你可以在我们的 *Codex Recipes（Codex 食谱/技巧指南）* 中了解关于使用别名的其他方法。

**如何让别名不在手稿中显示（例如：如果你不想一直看到这些词被高亮）：**
1. 打开 Codex 条目。
2. 切换到 **Tracking（追踪）** 标签页。
3. 取消勾选 **“Track this entry by name/alias（通过名称/别名追踪此条目）”**。

### 大小写敏感匹配（Case-Sensitive Matching）
默认情况下，Novelcrafter 以**大小写不敏感**的方式匹配 Codex 条目的名称和别名。如果你的条目名称是一个常用词，导致普通的日常用法也被高亮了（例如 “Will”、“May” 或 “River”），请在 **Tracking（追踪）** 标签页中启用**大小写敏感匹配（Case-sensitive matching）**。启用后，只有大小写完全一致的出现频次才会被统计。

> 有关所有追踪选项的更多详情（包括大小写敏感匹配、自动复数形式、排除名单以及 AI 上下文设置），请参阅 **Codex Tracking（Codex 追踪）** 文档。

---

## 核心概念与技术解释

1. **别名机制（Aliases System）的多重作用**
   * **实体消歧（Entity Disambiguation）**：在文学创作中，同一个角色可能会被称为名字（如“John”）、姓氏（如“Smith”）、昵称（如“Johnny”）或称号（如“The Butcher”）。别名机制允许把这些散落在各处的称呼**归一化（Normalize）**指向同一个 Codex 实体，防止 AI 产生“这是不同角色”的幻觉。
2. **全局高亮与视觉追踪（Visual Tracking & Cross-Document Binding）**
   * 该功能通过双向绑定技术，将 Codex 数据库的元数据与具体文本（Manuscript / Plan / Snippets）打通。当作者在正文输入别名时，前端解析器会实时捕获并建立索引，使得 Mention 统计和热力图能够动态生成。


### Product & Technical Design Document v0.1

---

## 1. 项目概述

### 1.1 项目目标

LLM Wiki 的目标不是简单建立一个“可以聊天的 RAG”。

它希望建立一个：

> **以 Markdown 为长期知识源、以结构化元数据和知识链接组织内容、以全文搜索和语义搜索提供检索能力、最终由 AI Agent 使用的个人知识系统。**

核心思想：

```text
                 LLM Wiki
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
   Knowledge Layer         Search Layer
          │                     │
 Markdown / YAML           BM25 / FTS
 Wiki Links                Semantic Index
 Headings                  Metadata Filter
 Properties                Reranker
          │                     │
          └──────────┬──────────┘
                     ↓
                   Agent
                     ↓
          Answer + Provenance
```

其中：

**Markdown 是 Source of Truth。**

搜索索引、Embedding、Vector Index、BM25 Index 等全部属于派生数据，可以删除、重建、替换，而不应该成为知识本身。

---

# 2. 为什么不直接把项目定义成 RAG？

传统 RAG 通常可以抽象为：

```text
Documents
    ↓
Chunking
    ↓
Embedding
    ↓
Vector Database
    ↓
Retrieval
    ↓
LLM
```

这种架构适合：

- 大量相对稳定的文档
    
- FAQ
    
- 企业文档
    
- 产品文档
    
- PDF 知识库
    

但它并不完全适合个人 Wiki。

个人 Wiki 有几个特殊特征：

1. 内容持续变化
    
2. 同时修改大量文件很常见
    
3. 文件本身具有很强的结构
    
4. Markdown Heading 本身具有语义
    
5. YAML Properties 包含重要元数据
    
6. Wiki Links 表达知识之间的关系
    
7. 用户需要知道答案来自哪里
    
8. 用户可能需要按照 metadata 筛选知识
    
9. 很多问题适合关键词搜索，而不是语义搜索
    
10. AI 不应该只得到一段孤立的 Vector Chunk，而应该知道这个 Chunk 所属的 Note、Section、Source 和状态
    

因此：

> **RAG 应该是 LLM Wiki 的一个“搜索能力”，而不是 LLM Wiki 本身。**

---

# 3. 核心设计原则

## Principle 1：Markdown First

Markdown 是唯一的知识源。

```text
Obsidian Markdown
        ↓
   Source of Truth
```

Vector DB、SQLite Index、Embedding 等全部属于缓存/派生层。

因此未来即使：

```text
QMD
→ LlamaIndex
→ Qdrant
→ Elasticsearch
→ 其他 Search Engine
```

发生替换，也不应该影响原始知识。

---

## Principle 2：Structure First, Embedding Second

不要首先问：

> “如何把所有 Markdown 转成 Vector？”

而应该首先问：

> “如何把 Markdown 中已经存在的结构保存下来？”

因此优先保留：

```text
Filename
Properties
Aliases
Tags
Headings
Wiki Links
Source
Content
```

Embedding 只是其中一种搜索表示。

---

## Principle 3：不要让 Vector 成为唯一检索方式

系统应该同时支持：

```text
Exact Search
    +
Semantic Search
    +
Metadata Filter
    +
Knowledge Links
```

即：

```text
BM25 / FTS
       +
Vector Search
       +
Metadata
       +
Wiki Graph
```

而不是：

```text
Vector Search Only
```

---

## Principle 4：Block-level Incremental Indexing

用户的实际使用方式是：

> 经常对很多 Markdown 文件进行小幅修改。

因此不应该采用：

```text
File
 ↓
One Embedding
```

而应该：

```text
Markdown
   ↓
Sections / Chunks
   ↓
Individual Embeddings
```

例如：

```text
MCP Security.md

├── ## Overview
│      └── Chunk A
│
├── ## Tool Poisoning
│      └── Chunk B
│
├── ## Prompt Injection
│      └── Chunk C
│
└── ## Defense
       └── Chunk D
```

如果只修改 `Defense`：

```text
A unchanged
B unchanged
C unchanged
D changed
```

则：

```text
只重新生成 D 的 Embedding
```

而不是整个文件重新 Embedding。

---

## Principle 5：Provenance First

任何 AI 搜索结果都应该能够回答：

> “这条信息到底来自哪里？”

至少应该知道：

```text
Source File
Path
Heading
Chunk
Position
Source
Status
Confidence
```

例如：

```text
MCP Security.md
└── Tool Poisoning
    └── Chunk #03

Source:
MCP Specification

Status:
verified

Confidence:
high
```

因此系统不是：

> Vector → Answer

而是：

> Vector → Knowledge Block → Source Context → Answer

---

# 4. LLM Wiki 的产品定位

## 4.1 用户看到的是什么？

用户主要使用 Obsidian。

例如：

```text
My LLM Wiki/
│
├── Concepts/
├── Technologies/
├── Projects/
├── References/
├── Sources/
├── Decisions/
└── Procedures/
```

每个知识都是 Markdown。

例如：

```text
MCP Tool Poisoning.md
```

---

# 5. Markdown 知识模型

一个 Note 至少包含：

```text
Frontmatter
+
Title
+
Sections
+
Content
+
Wiki Links
```

示例：

```yaml
---
type: concept

status: verified

tags:
  - ai-security
  - mcp
  - prompt-security

aliases:
  - Tool Poisoning Attack
  - TPA
  - 工具投毒

summary: "MCP Tool Poisoning 是通过恶意工具描述影响模型行为的一类攻击。"

source: "[[MCP Specification]]"

source_type: official

knowledge_type: fact

confidence: high

verified_at: 2026-08-11
---

# MCP Tool Poisoning

## Definition

MCP Tool Poisoning 是……

## Attack Mechanism

攻击者……

## Example

……

## Defense

……
```

Obsidian 原生 Properties 支持结构化数据，包括文本、链接、日期、数字、checkbox 和 tags；`tags`、`aliases` 等也是 Obsidian 的默认 Properties。

---

# 6. Properties 设计

不要一开始建立几十个 Property。

第一版建议只定义下面这些核心字段。

## 6.1 type

回答：

> “这是什么？”

建议：

```text
concept
technology
project
reference
source
decision
procedure
```

例如：

```yaml
type: concept
```

---

## 6.2 status

回答：

> “这条知识现在处于什么状态？”

建议：

```text
draft
reviewed
verified
obsolete
```

例如：

```yaml
status: verified
```

意义：

- draft：正在整理
    
- reviewed：已经检查
    
- verified：可以作为可靠依据
    
- obsolete：已经过时
    

---

## 6.3 tags

回答：

> “它涉及什么主题？”

例如：

```yaml
tags:
  - ai-security
  - mcp
  - prompt-injection
```

不要用 tags 表示：

```text
concept
verified
draft
important
article
```

这些应该进入 Properties。

原则：

> **Type 是“它是什么”；Tag 是“它涉及什么”。**

---

## 6.4 aliases

回答：

> “它还有什么名字？”

例如：

```yaml
aliases:
  - Tool Poisoning Attack
  - TPA
  - 工具投毒
```

Aliases 特别适合：

- 缩写
    
- 中英文名称
    
- 同义词
    
- 常见叫法
    
- 历史名称
    

---

## 6.5 summary

回答：

> “这篇 Note 最核心的内容是什么？”

例如：

```yaml
summary: "MCP Tool Poisoning 是通过恶意工具描述影响模型行为的一类攻击。"
```

这个字段对 AI 很有价值。

Agent 可以先读取：

```text
Title
Type
Summary
Tags
Status
```

判断是否需要进一步读取完整 Note。

因此 Summary 可以理解为：

> **机器友好的知识目录。**

---

## 6.6 source

回答：

> “这条知识来自哪里？”

例如：

```yaml
source: "[[MCP Specification]]"
```

或者：

```yaml
source:
  - "[[MCP Specification]]"
  - "[[OWASP MCP Security]]"
```

如果一个知识是个人总结：

```yaml
source: "[[My MCP Security Analysis]]"
```

---

## 6.7 source_type

回答：

> “这个来源属于什么类型？”

建议：

```text
official
paper
book
article
conversation
personal
inference
```

例如：

```yaml
source_type: official
```

这样 Agent 可以区分：

```text
官方规范
```

和：

```text
个人推论
```

---

## 6.8 knowledge_type

回答：

> “这条内容本质上是什么？”

建议：

```text
fact
inference
opinion
hypothesis
```

例如：

```yaml
knowledge_type: fact
```

这对 AI 防止“把个人推测当成事实”非常重要。

---

## 6.9 confidence

回答：

> “我对这条知识有多大把握？”

例如：

```yaml
confidence: high
```

建议：

```text
high
medium
low
```

注意：

```text
status
```

和：

```text
confidence
```

不是一回事。

例如：

```yaml
status: reviewed
confidence: medium
```

意思是：

> 我审核过，但我仍然认为这个结论只有中等可信度。

---

## 6.10 verified_at

不要自己维护：

```text
created
updated
```

来重复记录文件时间。

Obsidian 本身可以提供文件级的：

```text
file.ctime
file.mtime
file.path
file.name
file.links
```

这些可以由文件系统/Obsidian 提供。

真正值得记录的是：

```yaml
verified_at: 2026-08-11
```

它表达的是：

> 这条知识什么时候被人工确认。

---

# 7. Tags / Properties / Links 的职责边界

这是整个 Wiki Schema 最重要的设计之一。

|元素|作用|示例|
|---|---|---|
|Filename|知识名称|`MCP Tool Poisoning.md`|
|Alias|其他名称|`TPA`|
|Heading|知识内部结构|`## Defense`|
|Tag|主题|`mcp`|
|Type|对象类型|`concept`|
|Status|知识状态|`verified`|
|Property|结构化信息|`confidence: high`|
|Wiki Link|知识关系|`[[Prompt Injection]]`|
|Source|知识来源|`[[MCP Specification]]`|
|Content|实际知识|Markdown 正文|
|Embedding|语义表示|Vector|

核心原则：

> **不要用一种机制解决所有问题。**

---

# 8. Markdown Heading 是重要的知识边界

Markdown 应尽量保持清晰的层级。

例如：

```markdown
# MCP Security

## Tool Poisoning

...

## Prompt Injection

...

## Authorization

...

## Defense

...
```

Heading 同时承担三个作用：

```text
Human Navigation
       +
Knowledge Structure
       +
AI Chunk Boundary
```

因此 Markdown 的结构质量会直接影响未来 Semantic Search 的质量。

---

# 9. Index 的基本数据模型

Semantic Index 不应该只保存：

```text
Vector
```

而应该保存一个完整的 Search Record。

例如：

```text
chunk_id:
MCP-Security::Tool-Poisoning::003

note_id:
MCP Security

path:
Security/MCP Security.md

heading:
Tool Poisoning

text:
工具投毒……

tags:
mcp
ai-security

type:
concept

status:
verified

source:
MCP Specification

confidence:
high

position:
...
hash:
...

embedding:
[...]
```

因此一个搜索结果实际上是：

```text
Knowledge Block
+
Metadata
+
Provenance
+
Embedding
```

---

# 10. Incremental Indexing

这是整个系统的核心技术要求之一。

## 10.1 第一次建立 Index

假设：

```text
10,000 Markdown
```

第一次：

```text
Markdown
   ↓
Parse
   ↓
Chunk
   ↓
Embedding
   ↓
Index
```

这是一次性的成本。

---

## 10.2 日常修改

如果：

```text
MCP Security.md
```

只有一个 Section 被修改：

```text
Section A unchanged
Section B unchanged
Section C changed
Section D unchanged
```PMG

则：

```text
A → skip
B → skip
C → re-embed
D → skip
```

---

## 10.3 Hash

每个 Document / Chunk 可以保存内容 Hash：

```text
Chunk A → hash 123
Chunk B → hash 456
Chunk C → hash 789
```

修改后：

```text
A → 123 → unchanged
B → 456 → unchanged
C → 999 → changed
```

系统只更新 C。

QMD 当前的本地索引结构已经采用 document/chunk hash、sequence、position 等字段管理 Markdown 内容和 embedding chunks；其 `content_vectors` 表保存 embedding chunks，并使用 SQLite FTS5 和 sqlite-vec 作为全文/向量索引。

---

# 11. Debounce

用户可能连续编辑：

```text
Save
Save
Save
Save
Save
```

不能每次保存都立即 Embedding。

应该：

```text
修改
 ↓
等待
 ↓
继续修改？
 ├── Yes → 重新等待
 └── No
       ↓
    Embedding
```

这个机制叫：

> Debounce

它可以显著减少频繁编辑产生的重复计算。

因此 Indexer 应该具备：

```text
File Watcher
+
Debounce
+
Hash Detection
+
Incremental Update
```

---

# 12. 为什么采用 Block/Chunk，而不是 File-level Index？

File-level：

```text
Note
 ↓
Vector
```

如果一个 Note 有 20,000 字，修改其中 100 字：

```text
20,000 字
 ↓
重新 Embedding
```

效率低。

Block-level：

```text
Note
├── Block A
├── Block B
├── Block C
└── Block D
```

只修改 C：

```text
C → re-embed
```

因此：

> **对于频繁微调多个 Markdown 文件的个人 Wiki，Block/Chunk-level Index 是优先设计，而不是 File-level Embedding。**

---

# 13. Semantic Index 到底是什么？

Semantic Index 不是一个特殊的数据库名称。

它本质上是：

```text
Content
 ↓
Embedding Model
 ↓
Vectors
 ↓
Vector Search Structure
```

例如：

```text
“MCP 工具投毒”

        ↓

Embedding Model

        ↓

[0.12, -0.31, 0.87, ...]
```

用户搜索：

```text
“恶意工具描述如何影响 AI？”
```

也转换成 Vector：

```text
Query
 ↓
Embedding
 ↓
Query Vector
```

然后计算：

```text
Query Vector
      ↓
Vector Similarity
      ↓
最相似的 Blocks
```

因此 Semantic Search 能够找到：

> “恶意工具描述影响模型”

即使原文没有出现完全相同的关键词：

> “工具投毒”。

---

# 14. Embedding Model

Embedding Model 与 LLM 不一样。

LLM：

```text
Qwen / GPT / Claude
```

负责：

> 生成答案。

Embedding Model：

```text
Qwen3-Embedding
```

负责：

> 把文本转换成用于检索的向量。

对于中文、多语言个人 Wiki，当前值得优先测试：

> **Qwen3-Embedding-0.6B**

官方模型卡显示它是专门用于文本 embedding 和 ranking 的模型，支持 100+ 语言、32K context，并支持最高 1024 维 embedding；同时提供 Qwen3-Reranker 系列。

因此第一版建议：

```text
Qwen3-Embedding-0.6B
```

而不是把 Embedding Model 和生成模型混为一谈。

---

# 15. Embedding Model 不应该频繁更换

同一个 Semantic Index 中：

```text
旧 Vector
+
新 Vector
```

最好来自同一个 Embedding Model。

如果从：

```text
Embedding Model A
```

换成：

```text
Embedding Model B
```

通常需要重新生成整个 Semantic Index。

因此：

> **Embedding Model 是基础设施级选择，不应该频繁更换。**

这也是为什么第一版应该先做小规模 Benchmark，再确定最终模型。

---

# 16. BM25 与 Semantic Search

两种搜索解决不同问题。

## BM25

适合：

```text
MCP
Qwen
Javelin
CVE-2025-xxxx
Tool Poisoning
```

也就是：

> **关键词非常重要的问题。**

---

## Semantic Search

适合：

```text
有没有关于“恶意工具描述影响 AI 行为”的知识？
```

即：

> **语义相似但关键词可能不同的问题。**

---

## 最佳方案

不要二选一。

采用：

```text
BM25
 +
Semantic Search
```

即：

> Hybrid Search

---

# 17. Hybrid Search

推荐架构：

```text
                    Query
                      │
             ┌────────┴────────┐
             ↓                 ↓
           BM25             Vector
             │                 │
             ↓                 ↓
        Keyword Results   Semantic Results
             │                 │
             └────────┬────────┘
                      ↓
                    Fusion
                      ↓
                  Top N
```

这样可以兼顾：

```text
精确关键词
+
语义理解
```

---

# 18. Metadata Filtering

Vector Search 之前/过程中还应该支持：

```text
type
status
tags
source_type
knowledge_type
confidence
```

例如用户问：

> “只告诉我已经验证过的 MCP 安全知识。”

搜索条件可以是：

```text
tags contains mcp
AND
status = verified
```

然后再：

```text
BM25
+
Semantic Search
```

因此：

> **Metadata 是 Search Layer 的一等公民。**

不能只把 metadata 当作 Vector DB 的附属字段。

---

# 19. Reranker

当搜索产生：

```text
50 candidates
```

可以进一步：

```text
50
 ↓
Reranker
 ↓
Top 5
```

Reranker 的作用不是建立 Index，而是：

> 判断候选内容与用户问题的相关程度。

Qwen3 Embedding 系列同时提供 Reranker 模型，例如 `Qwen3-Reranker-0.6B`。

因此未来可以：

```text
BM25
 +
Vector
 ↓
Top 30
 ↓
Qwen3-Reranker-0.6B
 ↓
Top 5
```

但：

> **第一版不一定需要 Reranker。**

先测：

```text
BM25 + Vector
```

如果效果不够，再加入。

---

# 20. Provenance / 溯源设计

这是 LLM Wiki 与普通 RAG 的一个重要区别。

每个 Search Result 应该能够追溯：

```text
Note
 ↓
Path
 ↓
Heading
 ↓
Block
 ↓
Original Markdown
```

例如：

```text
Result

File:
Security/MCP Security.md

Heading:
## Tool Poisoning

Chunk:
003

Source:
[[MCP Specification]]

Status:
verified

Confidence:
high
```

因此最终 Agent 可以生成：

> 根据 `MCP Security.md` 中的 `Tool Poisoning` 章节……

而不是：

> 根据知识库检索结果……

---

# 21. Source of Truth 与 Search Index 分离

系统应该明确分为两层。

## Knowledge Layer

```text
Obsidian
│
├── Markdown
├── YAML
├── Tags
├── Aliases
├── Wiki Links
└── Headings
```

这是：

> **永久数据。**

---

## Search Layer

```text
BM25 Index
Vector Index
Embedding
Reranker Cache
Search Cache
```

这是：

> **派生数据。**

可以：

```text
Delete
Rebuild
Replace
Migrate
```

而不会影响知识本身。

---

# 22. 为什么第一版不推荐直接使用 LlamaIndex？

LlamaIndex 非常强大，也非常适合构建复杂 RAG。

它的优势是：

```text
Data Ingestion
Node Parsing
Index
Retriever
Postprocessor
Query Engine
LLM
```

高度模块化。

但对于这个项目：

> LlamaIndex 应该被看作“未来可以使用的开发框架”，而不是第一层产品架构。

原因是：

如果一开始直接：

```text
Obsidian
 ↓
LlamaIndex
 ↓
Vector DB
```

很容易把：

```text
Wiki
```

误设计成：

```text
RAG Database
```

而我们的目标其实是：

```text
Wiki
 ↓
Search Engine
 ↓
Agent
```

因此：

> **先定义 Wiki Schema，再决定是否用 LlamaIndex。**

---

# 23. 为什么不建议第一版直接部署 Qdrant / Chroma？

个人 Wiki 的规模通常没有必要一开始就引入独立 Vector Database。

QMD 当前采用：

```text
SQLite
+
FTS5
+
sqlite-vec
```

并将 Index 存储在本地 SQLite 文件中。其当前 schema 包含 collections、documents、documents_fts、content_vectors、vectors_vec 等结构。

因此对于个人 Wiki，第一阶段更适合：

```text
SQLite
```

而不是：

```text
Qdrant Server
```

除非未来出现：

- 多用户
    
- 云端服务
    
- 大规模数据
    
- 高并发
    
- 独立 Search Service
    

才考虑升级。

---

# 24. QMD 在整个系统中的定位

QMD 不应该被定义为：

> “我的知识库”。

更准确的定位是：

> **Local Search Engine / Indexing Engine**

它可以负责：

```text
Markdown
 ↓
Chunk
 ↓
BM25
 ↓
Embedding
 ↓
Vector Search
 ↓
Reranking
```

而：

```text
Obsidian
```

仍然是：

> Knowledge System。

QMD 当前的索引结构已经包含 Markdown 文档、FTS5 全文索引、embedding chunks、sqlite-vec 向量索引以及 LLM cache 等组件。

因此它非常接近本项目需要的 Search Layer。

---

# 25. 推荐的整体技术架构

第一阶段推荐：

```text
                    ┌─────────────────┐
                    │     Obsidian    │
                    │     Markdown    │
                    └────────┬────────┘
                             │
                    Source of Truth
                             │
             ┌───────────────┼────────────────┐
             ↓               ↓                ↓
         Properties       Headings         Wiki Links
             │               │                │
             └───────────────┼────────────────┘
                             ↓
                       Index Pipeline
                             │
                   ┌─────────┴─────────┐
                   ↓                   ↓
                 BM25              Semantic
                   │                   │
                   │             Qwen3-Embedding
                   │                   │
                   │              Vector Index
                   │                   │
                   └─────────┬─────────┘
                             ↓
                       Hybrid Search
                             ↓
                     Metadata Filter
                             ↓
                          Reranker
                             ↓
                           Agent
                             ↓
                  Answer + Provenance
```

---

# 26. 推荐的技术栈 v0.1

| 层                  | 推荐                          |
| ------------------ | --------------------------- |
| Knowledge Editor   | Obsidian                    |
| Source Format      | Markdown                    |
| Metadata           | YAML Properties             |
| Relationships      | Wiki Links                  |
| Structure          | Markdown Headings           |
| Full-text Search   | BM25 / SQLite FTS5          |
| Semantic Search    | Vector Search               |
| Embedding          | Qwen3-Embedding-0.6B        |
| Local Storage      | SQLite                      |
| Vector Extension   | sqlite-vec 或等价本地实现          |
| Chunking           | Markdown-aware Block/Chunk  |
| Incremental Update | Hash                        |
| Edit Optimization  | Debounce                    |
| Reranker           | Qwen3-Reranker-0.6B，第二阶段    |
| Search Engine      | QMD 或自建轻量 Indexer           |
| RAG Framework      | 暂不强制                        |
| Agent Interface    | MCP / API                   |
| LLM                | 后续根据 Agent 场景选择             |

---

# 27. 为什么 Qwen3-Embedding-0.6B 是当前候选，而不是最终锁定？

它目前非常符合这个项目：

```text
中文
+
英文
+
代码
+
多语言
+
本地运行
+
0.6B
+
32K context
```

官方资料显示其支持 100+ 语言、32K context，并允许 32～1024 范围内的输出维度选择。

但是：

> **最终模型不能只靠“排行榜”决定。**

应该建立一个自己的 Retrieval Benchmark。

例如准备：

```text
50 个真实问题
```

每个问题标记：

```text
Expected Notes
Expected Sections
Expected Blocks
```

然后比较：

```text
BGE-M3
Qwen3-Embedding-0.6B
EmbeddingGemma
其他候选
```

最终根据：

```text
Recall@5
Recall@10
MRR
实际回答质量
速度
内存
```

决定。

---

# 28. Index Pipeline

推荐实现：

```text
File Watcher
      ↓
Detect Markdown Change
      ↓
Debounce
      ↓
Parse Frontmatter
      ↓
Parse Markdown Structure
      ↓
Identify Sections / Blocks
      ↓
Calculate Hash
      ↓
Compare Existing Index
      ↓
┌───────────────┬───────────────┐
│ unchanged     │ changed       │
│               │               │
│ skip          │ re-index      │
└───────────────┴───────────────┘
                       ↓
                   Chunking
                       ↓
                Embedding Model
                       ↓
                 Update Index
```

---

# 29. 删除文件

Indexing 不仅要处理：

```text
Create
Update
```

还必须处理：

```text
Delete
Rename
Move
```

例如：

```text
MCP.md
```

删除以后：

```text
Vector Index
BM25 Index
Metadata Index
```

中对应记录也必须删除。

Rename / Move 则必须更新：

```text
path
note_id
provenance
links
```

---

# 30. Metadata 更新

例如用户没有修改正文，只修改：

```yaml
status: draft
```

变成：

```yaml
status: verified
```

这种情况：

> **不应该重新 Embedding 正文。**

因为：

```text
Content Hash
```

没有变化。

只需要：

```text
Update Metadata Index
```

这是另一个重要的性能优化。

因此 Index Pipeline 应区分：

```text
Content Change
```

和：

```text
Metadata Change
```

---

# 31. Wiki Link 更新

例如：

```markdown
[[Prompt Injection]]
```

改成：

```markdown
[[MCP Prompt Injection]]
```

这种变化可能不需要重新 Embedding 正文，但需要更新：

```text
Graph
Backlinks
Relation Index
```

因此未来最好把：

```text
Content Index
Metadata Index
Relation Index
```

分开管理。

---

# 32. 三类 Index

最终可以形成：

```text
                 LLM Wiki
                    │
       ┌────────────┼────────────┐
       ↓            ↓            ↓
 Content Index  Metadata Index  Graph Index
       │            │            │
       ↓            ↓            ↓
   BM25/Vector    Properties   Wiki Links
```

分别回答：

### Content Index

> “哪段内容和问题最相关？”

### Metadata Index

> “哪些知识符合条件？”

### Graph Index

> “这个知识和哪些知识有关？”

---

# 33. Agent 不应该直接访问 Vector DB

Agent 应该调用一个统一的 Search Interface：

```text
search(query, filters, options)
```

例如：

```json
{
  "query": "MCP 工具投毒如何攻击模型？",
  "filters": {
    "status": "verified",
    "tags": ["mcp"]
  },
  "top_k": 5
}
```

返回：

```text
{
  "content": "...",
  "note": "MCP Security.md",
  "heading": "Tool Poisoning",
  "path": "Security/MCP Security.md",
  "status": "verified",
  "source": "MCP Specification",
  "confidence": "high"
}
```

这样 Agent 不需要知道：

```text
SQLite
sqlite-vec
QMD
Qdrant
LlamaIndex
```

Agent 只知道：

> **Search my Wiki.**

---

# 34. Agent 最终获得的不是“向量”

这是非常重要的设计思想。

Agent 得到：

```text
Knowledge Block
```

而不是：

```text
Vector
```

例如：

```text
Knowledge Block
────────────────────
Title:
MCP Tool Poisoning

Section:
Tool Poisoning

Content:
……

Source:
MCP Specification

Status:
verified

Confidence:
high

Path:
Security/MCP Security.md

Links:
[[Prompt Injection]]
[[MCP Security]]
```

Vector 只是 Search Engine 内部的实现细节。

---

# 35. RAG 的最终角色

在这个架构中：

```text
RAG
```

不是整个系统。

它只是：

```text
Search
 ↓
Relevant Knowledge
 ↓
Context Construction
 ↓
LLM
```

所以最终系统可以理解为：

```text
LLM Wiki
   │
   ├── Knowledge Management
   ├── Search
   ├── Provenance
   ├── Relations
   └── Agent Interface
           │
           ↓
          RAG
           │
           ↓
          LLM
```

---

# 36. 产品设计：用户应该感知什么？

第一版用户甚至不需要知道：

```text
Embedding
Vector DB
BM25
Reranker
Chunk
```

用户只需要：

### 写

在 Obsidian 写 Markdown。

### 整理

使用：

```text
Properties
Tags
Aliases
Wiki Links
Headings
```

### 搜索

输入自然语言。

### 追溯

点击：

```text
Source
Note
Heading
```

### 询问 AI

让 Agent 使用 Wiki。

因此：

> **复杂性应该留在系统内部，而不是让用户维护 RAG。**

---

# 37. 第一版产品功能

建议 MVP 只有：

### P0

1. Obsidian Markdown
    
2. YAML Properties
    
3. Wiki Links
    
4. Markdown-aware Chunking
    
5. Incremental Index
    
6. Hash Detection
    
7. BM25
    
8. Semantic Search
    
9. Provenance
    
10. Metadata Filter
    
11. Search API
    
12. Agent Interface
    

---

### P1

增加：

```text
Reranker
Query Expansion
Related Notes
Backlinks
Knowledge Graph
Search Explanation
```

---

### P2

再考虑：

```text
Automatic Knowledge Extraction
AI Note Creation
AI Metadata Generation
Conflict Detection
Knowledge Deduplication
Knowledge Freshness Detection
Source Verification
Personal Memory
Agentic Research
```

---

# 38. 不应该第一阶段做的东西

不要一开始就做：

```text
GraphRAG
Knowledge Graph Database
Qdrant Cluster
复杂 Agent
多 Agent
自动知识重写
自动修改 Wiki
复杂 Ontology
```

这些都可以以后增加。

第一阶段最重要的是：

> **把 Markdown → Structure → Search → Provenance 这条链打通。**

---

# 39. 知识质量比模型大小重要

这个项目最终效果很可能不是：

```text
更大的 LLM
```

决定的。

而是：

```text
好的 Markdown Structure
+
好的 Metadata
+
好的 Chunking
+
好的 Retrieval
+
好的 Provenance
```

决定的。

尤其是：

> **一个结构清晰的 5,000 篇 Markdown Wiki，可能比一个混乱的 50,000 篇 Vector Database 更有价值。**

---

# 40. 与传统 RAG 的区别

传统 RAG：

```text
PDF
 ↓
Chunks
 ↓
Vector DB
 ↓
LLM
```

LLM Wiki：

```text
Markdown
 ├── Properties
 ├── Tags
 ├── Aliases
 ├── Wiki Links
 ├── Headings
 └── Content
        ↓
 ┌──────┼─────────┐
 ↓      ↓         ↓
BM25  Vector    Graph
 ↓      ↓         ↓
 └──────┼─────────┘
        ↓
     Reranker
        ↓
      Agent
        ↓
 Answer + Provenance
```

因此：

> **LLM Wiki 是 Knowledge System，RAG 是其中的 Retrieval/Generation mechanism。**

---

# 41. 一个关键的长期设计决策

## 不要让 Search Index 成为数据库事实源

例如：

```text
QMD index.sqlite
```

丢了：

> 没关系。

重新建立。

```text
Vector DB
```

坏了：

> 没关系。

重新建立。

```text
Embedding Model
```

换了：

> 重新 Embedding。

但：

```text
Markdown
```

丢了：

> 这是灾难。

所以：

```text
Markdown = Permanent
Index = Disposable
```

这是本项目最重要的架构原则之一。

---

# 42. 推荐的目录结构

第一版可以：

```text
LLM Wiki/
│
├── 00 Inbox/
│
├── 01 Concepts/
│
├── 02 Technologies/
│
├── 03 Projects/
│
├── 04 References/
│
├── 05 Sources/
│
├── 06 Decisions/
│
├── 07 Procedures/
│
├── 08 People/
│
└── 99 Archive/
```

但目录不应该成为唯一分类方式。

真正的机器分类应该依靠：

```text
type
tags
properties
links
```

目录主要服务于：

> 人类浏览。

---

# 43. 推荐的 Note 生命周期

一篇新知识：

```text
Inbox
 ↓
Draft
 ↓
Reviewed
 ↓
Verified
 ↓
Maintained
 ↓
Obsolete
```

例如：

```yaml
status: draft
```

AI 可以知道：

> 这是尚未确认的信息。

最终：

```yaml
status: verified
```

AI 才可以更放心地作为依据。

---

# 44. 知识的新鲜度

未来可以增加：

```text
last_verified
```

例如：

```yaml
verified_at: 2026-08-11
```

然后 Agent 可以知道：

```text
知识已经 3 年没有确认
```

对于：

```text
AI
Cloud
Security
Software
API
```

这些变化很快的领域尤其重要。

未来甚至可以设计：

```text
Freshness Score
```

例如：

```text
Freshness:
High
Medium
Low
```

---

# 45. 知识冲突

未来两个 Note 可能出现：

```text
Note A:
MCP supports X.

Note B:
MCP no longer supports X.
```

此时系统不应该简单地：

```text
Vector similarity
```

然后选一个。

应该利用：

```text
source_type
verified_at
status
confidence
source
```

判断。

最终甚至可以让 Agent 告诉用户：

> 我的知识库中存在两个相互冲突的结论，较新的官方来源是……

这是未来非常有价值的能力。

---

# 46. 最终技术路线

## Phase 0：Schema

先定义：

```text
Properties
Tags
Aliases
Types
Status
Sources
Knowledge Types
```

**暂时不做 RAG。**

---

## Phase 1：Obsidian Wiki

建立：

```text
Markdown
+
Properties
+
Wiki Links
+
Headings
```

目标：

> 建立高质量 Knowledge Base。

---

## Phase 2：全文搜索

加入：

```text
BM25 / FTS5
```

目标：

> 精确搜索。

---

## Phase 3：Semantic Search

加入：

```text
Qwen3-Embedding-0.6B
+
Block-level Index
```

目标：

> 语义搜索。

---

## Phase 4：Hybrid Search

```text
BM25
+
Vector
```

目标：

> 提升 Recall。

---

## Phase 5：Provenance

Search Result 增加：

```text
Note
Path
Heading
Source
Status
Confidence
```

目标：

> 可解释、可追溯。

---

## Phase 6：Reranker

加入：

```text
Qwen3-Reranker-0.6B
```

目标：

> 提升 Precision。

---

## Phase 7：Agent

提供：

```text
Search API
Read Note
Read Section
Find Related Notes
Get Source
```

然后接入：

```text
MCP
```

目标：

> 让 Agent 使用整个 Wiki。

---

## Phase 8：Knowledge Graph

只有当实际使用中发现：

> “单纯 Search 不够，需要理解大量实体之间的关系。”

再增加：

```text
Graph Index
```

而不是一开始就上 Neo4j。

---

# 47. 最终系统架构图

```text
                              ┌──────────────────┐
                              │     AI Agent     │
                              └────────┬─────────┘
                                       │
                              Search / Read / Link
                                       │
                              ┌────────▼─────────┐
                              │   Wiki API/MCP   │
                              └────────┬─────────┘
                                       │
                       ┌───────────────┼────────────────┐
                       ↓               ↓                ↓
                    BM25           Semantic          Metadata
                  / FTS5            Search            Filter
                       │               │                │
                       │          Embedding             │
                       │               │                │
                       │       Vector Index             │
                       │               │                │
                       └───────────────┼────────────────┘
                                       ↓
                                   Fusion
                                       ↓
                                   Reranker
                                       ↓
                              Knowledge Blocks
                                       │
                    ┌──────────────────┼──────────────────┐
                    ↓                  ↓                  ↓
                  Note              Heading            Source
                    │                  │                  │
                    └──────────────────┼──────────────────┘
                                       ↓
                                Obsidian Markdown
                                       │
                    ┌──────────────────┼──────────────────┐
                    ↓                  ↓                  ↓
                Properties          Wiki Links         Content
                    │                  │                  │
                    └──────────────────┼──────────────────┘
                                       ↓
                              SOURCE OF TRUTH
```

---

# 48. 最终结论

经过前面的讨论，本项目目前最重要的结论不是：

> “选 LlamaIndex 还是 QMD？”

而是下面这几个架构决策。

### 结论 1

**LLM Wiki 不是一个 RAG 项目。**

它是一个：

> **Personal Knowledge System。**

RAG 只是其中的搜索/生成能力。

---

### 结论 2

**Obsidian Markdown 是 Source of Truth。**

所有 Index 都是派生数据。

---

### 结论 3

**Properties、Tags、Aliases、Wiki Links、Headings 必须从一开始设计好。**

因为它们决定未来 AI 能否理解知识的：

```text
身份
类型
主题
关系
来源
状态
可信度
时间
结构
```

---

### 结论 4

**Semantic Index 不应该以整个 Markdown 文件为最小单位。**

对于本项目：

> **Block/Chunk-level Index 是更合适的设计。**

---

### 结论 5

**必须采用增量 Index。**

依靠：

```text
File Watcher
+
Debounce
+
Hash
+
Incremental Update
```

减少频繁修改造成的重复 Embedding。

---

### 结论 6

**BM25 和 Semantic Search 应该并存。**

因为：

```text
BM25 → 精确关键词
Vector → 语义理解
```

两者互补。

---

### 结论 7

**Metadata 必须参与检索。**

不能只做：

```text
Vector Search
```

而应该支持：

```text
Metadata Filter
+
BM25
+
Vector
```

---

### 结论 8

**Provenance 是一等公民。**

AI 找到一段知识以后，必须能够知道：

```text
来自哪个 Markdown
哪个目录
哪个 Heading
哪个 Block
什么 Source
什么 Status
什么 Confidence
```

---

### 结论 9

**第一阶段不需要 Qdrant / Chroma / Neo4j。**

个人 Wiki 优先考虑：

```text
SQLite
+
FTS5
+
sqlite-vec
```

这种本地方案。

QMD 已经采用类似的本地索引架构。

---

### 结论 10

**第一阶段也不需要 LlamaIndex。**

先把：

```text
Wiki Schema
+
Incremental Index
+
Hybrid Search
+
Provenance
```

设计清楚。

以后如果需要复杂 RAG Pipeline，再把 LlamaIndex 引入。

---

### 结论 11

**Embedding Model 应该作为基础设施组件单独设计。**

当前候选：

> Qwen3-Embedding-0.6B

它支持 100+ 语言、32K context，并提供可调整的 embedding 维度。

但最终应该用自己的 Retrieval Benchmark 决定，而不是仅凭模型排行榜。

---

### 结论 12

最终目标不是：

```text
“让 AI 能搜索我的 Markdown”
```

而是：

> **让 AI 能够理解、检索、引用、判断可信度，并沿着知识之间的关系使用我的个人知识。**

这才是这个项目真正的长期价值。

---

# 49. 一句话定义项目

如果以后要向别人介绍这个项目，可以这样描述：

> **LLM Wiki 是一个以 Obsidian/Markdown 为知识源、以结构化 Metadata 和 Wiki Links 构建知识结构、以增量式 Hybrid Search 提供全文与语义检索、以 Provenance 保证知识可追溯，并通过 Agent/MCP 为 AI 提供个人长期知识上下文的开放式 Personal Knowledge System。**

---

# 50. 当前推荐的 MVP

最终不要一次做完所有东西。

第一版只需要：

```text
Obsidian
   ↓
Markdown + YAML Properties
   ↓
Markdown-aware Chunking
   ↓
Hash + Incremental Index
   ↓
SQLite FTS5
   +
Qwen3-Embedding-0.6B
   ↓
Hybrid Search
   ↓
Provenance
   ↓
Search API
   ↓
Agent
```

然后根据真实使用效果逐步增加：

```text
Reranker
    ↓
Query Expansion
    ↓
Related Notes
    ↓
Graph
    ↓
AI Knowledge Extraction
    ↓
AI Knowledge Maintenance
```

**这应该是 LLM Wiki 的 v0.1 技术路线。**
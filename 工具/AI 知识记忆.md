https://github.com/topoteretes/cognee

> **Cognee 是一个把“文档 + 向量检索 + Knowledge Graph + Long-term Memory”组合起来的 AI 知识/记忆基础设施。**

它不是单纯的 Knowledge Graph，也不是单纯的 Memory，更不是传统 RAG。官方目前强调的是把原始数据转化成可持续更新的知识图谱，并结合向量搜索和图关系进行检索。

Cognee 的思路更接近：

```
                 Documents
                     ↓
              Extract / Cognify
                     ↓
        ┌────────────┴────────────┐
        ↓                         ↓
   Vector Knowledge          Knowledge Graph
        ↓                         ↓
        └────────────┬────────────┘
                     ↓
                AI Memory
                     ↓
                   Recall
```

也就是说，它不只是问：

> “哪几个文本和我的问题最相似？”

而是还希望理解：

> **“这些东西之间是什么关系？”**
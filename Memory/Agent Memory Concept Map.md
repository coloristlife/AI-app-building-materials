![[Pasted image 20260810205541.png]]

![[Pasted image 20260810205632.png]]

| 项目                 | 技术路线                                  | 官方 GitHub                                                                                               |
| ------------------ | ------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Hindsight**      | Cognitive / Learning Memory           | [github.com/vectorize-io/hindsight](https://github.com/vectorize-io/hindsight?utm_source=chatgpt.com)   |
| **Mem0**           | 通用 Agent Memory Layer                 | [github.com/mem0ai/mem0](https://github.com/mem0ai/mem0?utm_source=chatgpt.com)                         |
| **Letta (MemGPT)** | Stateful Agent + Memory               | [github.com/letta-ai/letta](https://github.com/letta-ai/letta?utm_source=chatgpt.com)                   |
| **Zep / Graphiti** | Temporal Knowledge Graph              | [github.com/getzep/graphiti](https://github.com/getzep/graphiti?utm_source=chatgpt.com)                 |
| **Honcho**         | User / Agent Modeling                 | [github.com/plastic-labs/honcho](https://github.com/plastic-labs/honcho?utm_source=chatgpt.com)         |
| **Mnemosyne**      | Local / Lightweight Persistent Memory | [github.com/mnemosyne-oss/mnemosyne](https://github.com/mnemosyne-oss/mnemosyne?utm_source=chatgpt.com) |
| **MemMachine**     | Ground-truth / Episodic Memory        | [github.com/MemMachine/MemMachine](https://github.com/MemMachine/MemMachine?utm_source=chatgpt.com)     |


| 排名  | 项目                 | 我认为最强的方向                                 | 综合评价  |
| --- | ------------------ | ---------------------------------------- | ----- |
| 🥇  | **Hindsight**      | Cognitive Memory / Reflection / Learning | ⭐⭐⭐⭐⭐ |
| 🥈  | **Letta**          | Stateful Agent / Long-term Learning      | ⭐⭐⭐⭐⭐ |
| 🥉  | **Graphiti / Zep** | Temporal Graph / Retrieval               | ⭐⭐⭐⭐½ |
| 4   | **MemMachine**     | Episodic / Ground-truth Memory           | ⭐⭐⭐⭐½ |
| 5   | **Mem0**           | 通用 Memory Layer / 生态                     | ⭐⭐⭐⭐  |
| 6   | **Honcho**         | User Modeling / Personalization          | ⭐⭐⭐⭐  |
| 7   | **Mnemosyne**      | Local / Lightweight Memory               | ⭐⭐⭐½  |

因为你前面列的这些项目解决的是不同层次的问题。真正复杂的 Agent Memory 系统，很可能不是：

> **Hindsight vs Mem0 vs Graphiti**

而是：

> **Hindsight + Graphiti + Letta + 一个底层存储**

不过有一个关键点：**不要让多个 Memory 系统同时“随便记忆”，否则很容易出现重复、冲突和互相污染。** 最好采用“分工协作”的架构。

### 一个比较理想的组合

![[Pasted image 20260810220927.png]]

然后再根据实际需求加入：

![[Pasted image 20260810220943.png]]
甚至：

```
Honcho
   ↓
User Modeling
   ↓
“这个用户到底是什么样的人？”
```

这样就不是几个 Memory 工具互相竞争，而是：

> **每个 Memory Engine 负责自己最擅长的记忆类型。**
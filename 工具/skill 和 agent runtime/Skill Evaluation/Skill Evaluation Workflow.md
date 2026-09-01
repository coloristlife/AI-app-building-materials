---
内容生成: AI
---


> **Skill 本身是一个相对标准化的 Artifact，但 Skill 的实际效果并不只由 Skill 决定，而是由承载它的 Agent Runtime 决定。**

Agent Skills Specification 主要解决的是“Skill 长什么样、怎么描述、怎么组织资源”这个问题。比如 `SKILL.md`、`references/`、`scripts/` 这些属于相对标准化的部分。但是，当一个 Skill 真正被 Agent 使用时，它并不是直接“执行” `SKILL.md`，而是要经过 Agent Runtime 的一整套 orchestration 机制。

首先是 **Discovery**。Agent Runtime 需要判断当前有哪些 Skill，以及当前用户的任务是否和某个 Skill 相关。不同平台可能采用不同的机制来做这件事情。有的平台可能主要依赖 Skill 的 `name` 和 `description`，有的平台可能会进一步使用模型来判断相关性。因此，即使是完全相同的 Skill，在不同 Runtime 中被发现和激活的概率也可能不同。

然后是 **Activation 和 Context Loading**。Runtime 判断某个 Skill 相关以后，需要决定什么时候加载 Skill，以及加载多少内容。最基本的是把 `SKILL.md` 加进 Context，但对于 `references/`、`scripts/`、`assets/` 这些资源，不同 Agent 可能有不同的加载和调用机制。有的 Runtime 更强调 progressive disclosure，只在需要的时候读取 reference；有的可能一次加载更多内容。这个过程直接决定了模型实际“看到”的 Context，因此即使底层使用的是同一个模型，模型收到的信息也可能不完全一样。

接下来是 **Instruction Following 和 Agent Loop**。Skill 中写的是 instructions，但 Agent 并不是读完 instructions 就一次性生成答案。它可能需要经过多轮：

```text
User Request
    ↓
Model
    ↓
决定下一步行动
    ↓
Tool / Script / MCP
    ↓
获得结果
    ↓
Runtime 处理结果
    ↓
重新进入 Model
    ↓
继续执行
    ↓
Final Response
```

这里 Runtime 的差异就非常明显了。不同平台可能对 system prompt、Skill instructions、tool results、历史消息以及中间状态采用不同的组织方式。甚至模型调用之间的 context reconstruction、compression、state management 都可能不同。

然后就是 **Tool / MCP 调用**。如果 Skill 只是提供 instructions 和 reference，那么 Runtime 的差异可能还没有那么明显；但如果 Skill 需要调用工具，差异就会进一步放大。因为 Agent 不只是需要知道“有一个 Tool”，还需要决定什么时候调用、传什么参数、如何处理 Tool 返回的数据、Tool 出错以后是否 retry，以及 Tool 返回的结果应该以什么形式重新放入 Context。不同 Agent Runtime 对这些过程的实现都可能不同。

所以你刚才说的“**模型可能是一样的，但是处理模型反馈结果的机制不一样**”，这个理解非常关键。更准确地说，模型只是整个 Agent System 中的一个组件：

```text
Agent Behavior =
Model
+ System Instructions
+ Skill
+ Context Management
+ State Management
+ Tool/MCP Handling
+ Execution Loop
+ Runtime Policies
```

因此，即使：

```text
Model = Claude
Skill = 同一个 SKILL.md
User Prompt = 同一个
```

如果：

```text
Anthropic Runtime ≠ Goose Runtime
```

最终的行为也不一定相同。

这也就是为什么不同的 Agent 平台需要自己的 **Skill Evaluation**。它们并不是在重新验证“这个 SKILL.md 是否符合 Agent Skills Specification”。这一部分可以由类似 `skills-ref validate` 的规范验证工具完成。平台真正需要验证的是：

> **这个 Skill 在我的 Runtime 里面，是否能够按照预期被发现、激活、加载、执行，并且最终产生正确的结果。**

所以 Anthropic 的 evaluation 和 Goose 的 evaluation 本质上是在回答不同的问题。

Anthropic 的 evaluation 更关心：

> 这个 Skill 在 Anthropic 的 Agent execution environment 中是否改善了任务表现？

Goose-based evaluation 则应该问：

> 这个 Skill 在 Goose 的 discovery、activation、context management、tool execution 和 agent loop 中是否能够稳定完成预期任务？

因此，它们可以使用完全相同的 **test cases**，甚至可以使用类似的 **grader、comparator、benchmark**，但最底层的 **executor** 不一定一样。

你可以把整个关系理解成：

```text
                 Agent Skills Specification
                         │
                         │
                    定义 Skill
                         │
                         ↓
                    SKILL.md
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
        Anthropic Runtime       Goose Runtime
              │                     │
        Discovery               Discovery
              ↓                     ↓
        Activation              Activation
              ↓                     ↓
        Context Loading         Context Loading
              ↓                     ↓
        Agent Loop              Agent Loop
              ↓                     ↓
        Tool / MCP              Tool / MCP
              ↓                     ↓
        State Management        State Management
              ↓                     ↓
        Final Output            Final Output
              │                     │
              ↓                     ↓
       Anthropic Eval          Goose Eval
```

所以这里有一个很重要的区分：

**Agent Skills Specification 是跨平台的标准；Skill Evaluation 是 Runtime-specific 的。**

这并不意味着每个平台都必须重新发明一套 evaluation framework。实际上，很多 evaluation 的上层方法完全可以复用，例如同一个 test prompt、同一个 expected behavior、同一个 grader，甚至同一个 A/B comparison 方法都可以复用。真正需要针对平台变化的，主要是 **execution layer**——也就是“到底让哪个 Agent Runtime 去运行这个 Skill”。

这也是为什么我们前面讨论的 Anthropic Skill Creator 仍然可以拿来生成 Skill，然后再放到 Goose 上评估。你可以复用 Anthropic 的 **Skill creation methodology 和 evaluation methodology**，但把它原本面向 Claude 的执行部分替换成 Goose。

最终你真正需要验证的其实不是：

> “Anthropic 创建的 Skill 是否兼容 Goose？”

而是：

> **“这个 Skill 是否符合 Agent Skills Specification，以及它在 Goose Runtime 中是否能够按照预期完成任务。”**

前者是 **specification validation**，后者才是 **Goose-based runtime evaluation**。这两个概念分开以后，为什么不同 Agent 平台会有不同的 Skill evaluation mechanism，就很好理解了。
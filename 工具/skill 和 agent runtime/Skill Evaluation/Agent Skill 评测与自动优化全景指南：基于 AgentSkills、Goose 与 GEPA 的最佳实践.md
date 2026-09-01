---
内容生成: AI
---

**导读**：本文旨在系统性梳理基于大型语言模型（LLM）Agent（如 Goose）的技能（Skill）评测与自动优化技术架构。我们将深入探讨评测（Evaluation）、自动优化（Optimization）、知识库（Knowledge Base）以及底层基础设施（Harbor、Inspect AI 与 GEPA 框架）之间的协同关系，并给出一个具备高扩展性的四层解耦架构方案。

---

## 1. 背景：我们到底想解决什么问题？

在当前的语境下，我们讨论的并非传统的 Coding Agent 评测，而是针对 **Knowledge-based Task（基于知识库的任务）** 的特定场景。

整个交互链路如下：

```text
User
  │
  │ Security / Knowledge Question
  ▼
Goose Agent
  │
  │ loads
  ▼
Agent Skill (SKILL.md)
  │
  │ retrieves / reasons over
  ▼
Knowledge Base
  │
  ▼
Answer
```

以一个“安全架构评估技能（Security Architecture Skill）”为例：该 Skill 的目标是根据系统架构描述识别安全隐患，并从安全知识库（Security Knowledge Base）中匹配对应的安全需求，最终生成结构化结果。

这里核心需要回答的问题不是 *“Goose 能不能执行这个 Skill？”*，而是：
> **“这个 Skill 是否真的改善了 Agent 检索、理解和使用知识库的能力？”**

因此，我们的评测（Evaluation）指标必须涵盖：
*   **Retrieval Relevance**（检索相关性）
*   **Retrieval Completeness**（检索完整性）
*   **Groundedness**（内容溯源性/有据可查）
*   **Correctness**（正确性）
*   **Hallucination**（幻觉率）

更重要的是，我们最终希望形成一个持续迭代的**自动化闭环（Skill Optimization）**：

```text
Skill → Evaluation → Failure Analysis → Improvement → New Skill → Evaluation...
```

---

## 2. 核心认知：Evaluation（评测）与 Optimization（优化）是两码事

这是在构建 Agent 评测系统时最容易混淆的概念。

*   **Evaluation（评测）** 回答的是：*“当前这个 Skill 表现有多好？”*
*   **Optimization（优化）** 回答的是：*“怎样修改这个 Skill，能让它变得更好？”*

两者的协同关系如下：

```text
              Evaluation
                  │
                  ▼
             Score / Feedback
                  │
                  ▼
             Optimization
                  │
                  ▼
             New Candidate
                  │
                  ▼
              Evaluation
```

如果只有 Evaluation，你只能得到一个静态的干瘪数字（例如 `Skill → 82/100`）。
只有引入 Optimization，系统才能分析出失败原因，生成新的 Skill 版本（如 `v2 → 91/100`），从而真正产生工程上的自动化价值。

---

## 3. GEPA 框架：Evaluation-driven Optimization Engine

**GEPA (Genetic-Pareto)** 是一个用于自动优化文本型系统组件的开源优化框架。官方实现明确支持优化 Prompts、Code、Agent Architectures 及 Configurations 等文本参数。

其背后的核心理念源自相关学术研究：**不要仅仅将 Agent 的表现压缩成一个标量分数（Scalar Reward），而是让 LLM 读取完整的执行与评测追踪记录（Execution/Evaluation Traces），通过自然语言的反思（Reflection）找出失败根因，并生成针对性的修改方案。**

因此，GEPA 并非传统意义上的评测框架，它更准确的定位是：**基于评测驱动的优化引擎（Evaluation-driven Optimization Engine）**。

---

## 4. GEPA 与传统强化学习 (RL) 的本质区别

传统 RL 的优化思路更关注结果的反馈：

```text
Candidate → Run → Reward = 0.72 → Optimization
```
问题在于：`0.72` 只告诉你“失败了多少”，却无法告诉你“为什么失败”。

而 GEPA 保留了极度丰富的上下文信息：

```text
Candidate
   ↓
Run
   ↓
Execution Trace + Evaluation Result + Error/Feedback
   ↓
LLM Reflection ("Why did this candidate fail?")
   ↓
Proposed Improvement
```
GEPA 利用执行轨迹和自然语言反馈来诊断问题，这使得它的寻优路径更加高效且具备可解释性。

---

## 5. GEPA 的核心机制：自然语言反思 (Reflection)

假设你的初始技能 `Skill v1` 描述为：
> *Identify the security concerns and find the relevant security requirements from the knowledge base.*

评测结果发现：
*   检索相关性 (Relevance): 92%
*   检索完整性 (Completeness): **67%** (偏低)
*   正确性 (Correctness): 89%

普通优化器只能看到总体得分 `85.5`。而 GEPA 通过读取 Trace 可以发现具体案例的失败原因：
> **Case #17 分析**：Agent 在找到两个相关需求后，没有验证结果集是否完整，便过早停止了检索。

基于此，GEPA 的 Reflection Model 会生成针对性的 `Candidate v2`：
> *After identifying relevant requirements, perform a completeness check and determine whether additional related requirements should be retrieved.*

通过这种方式，Skill 的改进直击痛点。

---

## 6. 为什么叫 Genetic-Pareto (遗传-帕累托)？

GEPA 的进化路线并非线性的 `v1 → v2 → v3`，而是维护着一棵变异树，保留多个互补的高质量候选版本：

```text
                Skill v1
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
      v2-A       v2-B       v2-C
```

由于没有一个候选能在所有维度上做到绝对第一（例如 A 胜在检索，B 胜在溯源），GEPA 采用 **Pareto-efficient selection（帕累托最优选择）** 机制，保留这些在不同维度上表现优异的候选，防止陷入局部最优。

---

## 7. 将 GEPA 融入 Skill Evaluation 架构

理清上述概念后，整个架构的工作流变得非常清晰：

```text
                 SKILL.md v1
                      │
                      ▼
                    Goose (Runtime)
                      │
                      ▼
                Knowledge Base
                      │
                      ▼
                    Answer
                      │
                      ▼
                 Evaluation
                      │
          ┌───────────┼───────────┐
          ↓           ↓           ↓
      Retrieval   Grounding   Correctness
          │           │           │
          └───────────┼───────────┘
                      ↓
                  Feedback
                      │
                      ▼
                    GEPA (Optimizer)
                      │
             ┌────────┴────────┐
             ↓                 ↓
          Skill v2-A        Skill v2-B
             │                 │
             └────────┬────────┘
                      ↓
                  Evaluation
                      │
                      ▼
                Best Candidate
```
**结论**：Evaluation 是 GEPA 的“眼睛”，而 GEPA 是 Evaluation 背后的“大脑与优化器”。

---

## 8. Evaluation Framework 的核心职责

在第一版实现中，评测框架不需要过度复杂，核心只需实现一个 `KnowledgeSkillScorer`。

**输入侧 (Inputs)**：
*   Question (问题)
*   Expected Knowledge / Expected Evidence (预期知识与证据)
*   Agent Output (Agent 实际回答)
*   Agent Trace (执行轨迹)

**输出侧 (Outputs)**：
输出结构化的评估数据供 GEPA 使用，例如：
```json
{
  "retrieval_relevance": 0.92,
  "retrieval_completeness": 0.67,
  "groundedness": 0.94,
  "correctness": 0.89,
  "hallucination": 0.03,
  "overall_score": 0.85,
  "feedback": [
    "Agent stopped retrieval too early",
    "Two relevant requirements were omitted"
  ]
}
```

---

## 9. 完整的 8 步 Evaluation 工作流

为了确保科学衡量技能的增益，建议固定以下八步标准化流程：

1.  **定义数据集 (Evaluation Dataset)**：建立基于 YAML/JSON 的测试用例（Question, Expected Knowledge 等）。
2.  **设定基线 (Baseline)**：在**不加载 Skill** 的情况下运行 Agent，得出 Baseline 分数（如 71 分）。
3.  **技能评测 (Skill Evaluation)**：加载 `SKILL.md` 运行，得出带技能的分数（如 83 分），由此得出最核心的指标：**Skill Lift (+12 分)**。这是证明 Skill 价值的唯一依据。
4.  **失败诊断 (Failure Analysis)**：剖析 17 分的扣分项在哪里（例如：检索相关性达标，但完整性不足）。
5.  **GEPA 反思 (Reflection)**：将 Trace、Feedback 交给 GEPA 生成下一代 Candidate。
6.  **回归测试 (Re-Evaluation)**：重新评测新版本，确保提升检索能力的同时，正确性没有发生 Regression（退化）。
7.  **帕累托选择 (Pareto Selection)**：保留在不同指标维度上占据帕累托前沿的多个优质版本。
8.  **人工审批 (Human Approval)**：最终胜出的 Candidate 必须经过人工复核方可发布。

---

## 10. 为什么必须保留“人工审批 (Human Approval)”环节？

尽管 GEPA 支持全自动更新，但面对 **安全知识 / 安全架构 (Security Architecture)** 场景，自动优化器可能会为了“刷高” Benchmark 分数，生成针对测试集过拟合、但在实际安全逻辑上并不严谨的诡异规则。

因此，`自动化生成候选 → 自动化回归测试 → 人工审批 → 生产发布`，比全自动覆盖安全得多，是一条必须坚守的底线。

---

## 11. Harbor 在此架构中的定位

Harbor 是一个优秀的工具，但它不应与 GEPA 或 Inspect AI 混为一谈。

Harbor 本质上是：**重型的 Agent 执行与评测基础设施 (Agent Evaluation / Execution Infrastructure)**。它擅长处理复杂的沙盒环境（Sandbox）、容器化、文件系统还原、多步执行以及大规模并行 Trial。

由于早期的 Knowledge-based 任务不需要 Docker 级别的隔离，Harbor 适合作为**未来第二或第三阶段**的底座：

```text
       GEPA (Optimizer) ↔ Evaluator
              │               ↑
              ↓               │
           Harbor (Infrastructure)
              │
              ↓
            Goose
              │
    ┌─────────┴─────────┐
    ↓                   ↓
Knowledge Base        Tools/MCP
```

---

## 12. Inspect AI 的定位

对比 Harbor，由英国 AI 安全研究所开源的 **Inspect AI** 更加轻量，完美契合早期的问答类与知识类评测。

*   **Inspect AI**：轻量级评测层，聚焦于 `Dataset → Agent/Solver → Scorer → Evaluation` 链路。非常适合当前的纯文本知识问答评测。
*   **Harbor**：重量级执行层，聚焦于 `MCP + Tools + Sandbox + Parallel Trials` 复杂环境。

结论：**第一阶段使用 Inspect AI 作为评测框架；未来出现复杂环境需求时，再将底层执行交给 Harbor。**

---

## 13. 最终推荐的系统架构蓝图

基于以上分析，彻底摒弃“Fork Anthropic Skill Creator 以求大而全”的诱惑，我们确立以下**四层解耦**的架构体系：

```text
                         AgentSkills (Skill 规范层)
                             │
                          SKILL.md
                             │
                             ▼
                           Goose (Runtime 运行时层)
                             │
                  ┌──────────┴──────────┐
                  ↓                     ↓
            Knowledge Base          Tools/MCP
                  │                     │
                  └──────────┬──────────┘
                             ↓
                          Output
                             │
                             ▼
                   Evaluation Layer (评测层)
                             │
                 ┌───────────┴───────────┐
                 ↓                       ↓
            Inspect AI               Harbor
           (Phase 1 主力)          (Phase 2+ 扩展)
                 │                       │
                 └───────────┬───────────┘
                             ↓
                    Knowledge Scorer
                             │
                             ▼
                    GEPA (Optimization 优化层)
                             │
                   Reflect / Mutate / Select
                             │
                             ▼
                       Human Approval
                             │
                             ▼
                       Production Skill
```

---

## 14. 为什么该方案优于 Anthropic Skill Creator？

Anthropic Skill Creator 捆绑了 *技能创作、执行环境和评测机制*。如果直接 Fork 并基于此开发，会陷入深深的平台绑定。

上述四层解耦架构确保了系统极度灵活：
未来，即使 Agent 运行时从 Goose 换成 OpenHands，评测框架从 Inspect 换成 Harbor，只需替换对应的接口层，**评测方法论和 GEPA 优化引擎资产完全不用重写。**

---

## 15. 最小可行性产品 (MVP) 需要写多少代码？

这种架构将业务开发量压缩到了极致。在第一阶段，开发者只需专注开发最核心的业务逻辑：

1.  **Evaluation Dataset**：构建知识评测的数据集。
2.  **Goose Adapter**：用 Python 编写，使得 Inspect AI 能唤起 Goose CLI 并捕获输出。
3.  **Knowledge Scorer**：实现判定“检索、溯源、正确性”四大指标的具体评测逻辑。

你**完全不需要**重新造轮子去写并发调度、实验管理、进化算法或底层沙盒环境。

---

## 16. 项目落地技术路线图 (Roadmap)

建议分三个阶段稳步推进：

### Phase 1：最小可运行系统 (MVP)
*   **技术栈**：`AgentSkills` + `Goose` + `Knowledge Base` + `Inspect AI`
*   **目标**：跑通 `Baseline vs Skill` 的对比，量化证明 **Skill Lift**。建立四大核心评测指标。

### Phase 2：自动化 Skill 优化
*   **引入**：`GEPA`
*   **目标**：将评测反馈（Feedback）输入 GEPA，利用其自然语言反思和帕累托选择能力，自动生成并筛选迭代更优的候选 Skill，大幅降低人工调优成本。

### Phase 3：复杂 Agent 评测
*   **引入**：`Harbor`
*   **目标**：当 Goose 的技能扩展到需要 MCP、代码执行（Code Execution）、多步工具调用（Tools/Files）时，将底层执行框架迁移至 Harbor，以支撑重度并行和安全沙盒隔离。

---

## 17. 总结：四层架构的核心心法

整个系统最重要的护城河不是某个单一工具，而是**四层严格解耦的设计原则**。它们分别回答了四个根本问题：

1.  **Skill 应该长什么样？** → **AgentSkills (SKILL.md)** 负责规范定义。
2.  **Skill 在哪里执行？** → **Goose (Runtime)** 负责调度与运行。
3.  **Agent 执行得好不好？** → **Inspect AI / Harbor** 负责公正评测。
4.  **如何变得更好？** → **GEPA** 负责基于反馈的持续优化进化。

聚焦于具有业务价值的 `Scorer` 和 `Dataset` 建设，充分利用现有的顶级开源基础设施，这将是当前落地 Knowledge-based Agent Skill 评测系统**最高效、最稳健、最具扩展性**的最佳实践。
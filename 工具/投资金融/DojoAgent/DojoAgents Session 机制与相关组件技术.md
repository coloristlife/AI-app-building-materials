

---

# DojoAgents Session 机制与相关组件技术白皮书

## 1. 文档目的
本文用尽可能通俗的语言解释 DojoAgents 中的 **Session 机制**，以及与 Session 密切相关的 Runtime、Agent、Harness、SessionStore、BlobStore、Checkpoint、Principal、Run、Turn、Event、Lease 等概念。

重点回答几个问题：
1. Session 到底是什么？
2. 为什么需要 Session？
3. Session 和 Runtime、Agent、Harness 分别是什么关系？
4. Session 中保存什么？
5. Session 如何保证不同用户之间的数据隔离？
6. Checkpoint 如何实现 Agent 工作流恢复？
7. SessionStore 和 BlobStore 为什么要分开？
8. 多实例并发时 Lease、Fencing Token、Idempotency 如何工作？
9. 第三方项目如何使用或替换 Session 后端？
10. 为什么 DojoAgents 不让 Harness 自己管理 Session？

---

## 2. 先理解整个 DojoAgents 架构
理解 Session 之前，首先需要知道 DojoAgents 中几个核心角色。可以把整个系统想象成一个“Agent 工作平台”：

```text
                    Host Application
               API / Gateway / CLI / Worker
                           │
                           ↓
                    Runtime Assembler
                           │
             ┌─────────────┴─────────────┐
             │                           │
          Agent Core                  Harness
             │                           │
       AgentLoop                  Prompt / Skills
       ToolExecutor               Tools / Policy
       Sandbox                    Memory / Task
             │                           │
             └─────────────┬─────────────┘
                           ↓
                    SessionService
                     /           \
                    ↓             ↓
              SessionStore     BlobStore
                    │             │
              metadata/state   files/artifacts
```

其中最重要的分工是：

| 组件                   | 通俗理解                   | 主要职责                                   |
| :------------------- | :--------------------- | :------------------------------------- |
| **Host Application** | 外面的应用                  | 接收 HTTP/API/CLI 请求、认证用户                |
| **Runtime**          | Agent 的运行环境            | 把 Agent、Harness、Session 等组装起来          |
| **Agent Core**       | Agent 的通用发动机           | LLM 循环、Tool 执行、Sandbox、事件              |
| **Harness**          | 某个具体场景的“大脑配置”          | Prompt、Tools、Skills、Policy、Memory、业务流程 |
| **Session**          | **Agent的大脑记忆库** / 工作空间 | 保存对话、执行记录、状态、Checkpoint                |
| **SessionStore**     | Session 数据库            | 保存 Session 的结构化数据                      |
| **BlobStore**        | 文件仓库                   | 保存 PDF、图片、artifact 等大对象                |
| **Checkpoint**       | 工作进度“存档点”              | 让 Agent 可以从中断位置恢复                      |

---

## 3. 什么是 Session？

最简单的理解：**Session 就是一个 Agent 持续工作的“工作空间”或“记忆库”。**

它不只是聊天记录。普通 Chat Session 可能只有 `User message -> Assistant response`。而 DojoAgents Session 保存的信息更多：

```text
Session
│
├── Message (消息)
├── Run (运行记录)
├── Turn (交互轮次)
├── Event (事件)
├── Usage (Token消耗)
├── Checkpoint (状态快照)
├── Object metadata (对象元数据)
└── Session state (业务状态)
```

例如用户说：“帮我分析这个 AI Architecture 的安全风险。”Agent 会产生一连串的 Run、Turn 和 Checkpoint。因此 Session 可以理解为：**Agent 在某个用户、某个场景下持续工作的完整上下文和历史。**

**💡 用途拓展：Session 能干什么？**
*   **多租户 SaaS 服务：** 极高安全性的数据隔离，同一个 Agent 同时服务数百企业，数据绝不串门。
*   **超长复杂工作流：** 跑几天的 AI 任务，服务器重启后可从断点精准恢复。
*   **多媒体 AI 交互：** 完美支持用户发语音/图片，AI 自动生成 PDF 或图表的场景。

---

## 4. Session 和 Runtime 是什么关系？
这是最容易混淆的地方。

**Runtime 是“运行机器”**，它负责运行 Agent 并包含 Harness、Tools、SessionService 等。
一个 Runtime 可以同时服务很多用户：

```text
             One Runtime (共享的)
                  │
       ┌──────────┼──────────┐
       ↓          ↓          ↓
   Session A  Session B  Session C (隔离的)
```

所以：**Runtime 是共享的，Session 是隔离的。** 不能理解成 `User A → Runtime A`。

正确的方式是让 Runtime 长时间运行，处理大量请求，而不是每一个 HTTP request 都 `Runtime.create(...)`。

---

## 5. Session、Run、Turn、Event 的关系
这几个词可以用“工作过程”来理解：

*   **Session (工作空间):** 整个持续工作的空间，如 `conversation-001`。
*   **Run (一次任务):** 一次完整的 Agent 执行。用户问一句话，产生一个 `Run #123`。
*   **Turn (执行轮次):** Run 中的一次交互过程（如 `用户提问 -> LLM -> 调用工具 -> LLM -> 回答`）。
*   **Event (具体事件):** 执行中发生的事件，如 `tool_called`, `llm_completed`。

---

## 6. 为什么 Session 必须按 Tenant + User 隔离？
这是非常重要的安全原则。Session 的身份（Identity）是：`(tenant_id, user_id, session_id, harness_id)`。虽然两个不同用户都可以有一个叫 `conversation-001` 的 session_id，但它们不是同一个 Session。真正的身份是三者的结合。

## 7. 为什么不能只使用 session_id？
如果数据库只查询 `WHERE session_id = 'session-001'`，User B 可能会越权拿到 User A 的数据。
所以 DojoAgents 要求查询直接携带 `SessionPrincipal`（门禁卡）。数据库逻辑是 `WHERE tenant_id = ? AND user_id = ? AND session_id = ?`。
**“身份是存储边界”是 DojoAgents Session 安全设计的核心原则。**

## 8. SessionPrincipal 是什么？
`SessionPrincipal` 是**经过认证之后，系统确认“你是谁、属于哪个租户、拥有什么角色”的可信身份对象（门禁卡）。**
它必须由 Authentication 模块生成，**绝不能信任 HTTP 请求里的 user_id**，防止越权访问。

---

## 9. Session 中到底保存什么？
*   **Message:** 用户和 Agent 的消息。
*   **Run & Turn:** Agent 的完整执行记录和轮次。
*   **Event:** 执行过程中的事件，非常重要，用于**支持执行过程恢复和实时事件推送(SSE)**。
*   **Usage:** 记录 input/output tokens、时长等，用于成本计费。
*   **Checkpoint:** 保存 Agent 当前可恢复的状态。
*   **Object:** 文件或 artifact（Session 只存 `BlobRef`，不存实体）。

## 10. 为什么 SessionStore 和 BlobStore 要分开？
数据库适合保存结构化数据（metadata），但不适合保存大量二进制文件（PDF/PNG/Excel）。分开设计可以让 `MySQL/PostgreSQL` 结合 `S3/阿里云OSS` 组合使用，这是极其合理的工程设计。

---

## 11. Harness 是什么？
Harness 是**把通用 Agent 变成一个“特定用途 Agent”的配置和控制层**。Agent Core 是通用的发动机，而 Harness 告诉它“你是客服 Agent，你只能用这几个工具，遵守这些 Policy”。

## 12. 为什么 Harness 不应该自己创建 Session？
如果每个 Harness（客服、安全、投资）都自己建 `.db` 文件，系统会产生无数个存储方式、权限模型和并发模型。
**Session 是 Runtime 基础设施，而不是某个具体业务 Harness 的私有能力。**

## 13. HarnessSessionStateFacade 是什么？
它是给 Harness 使用的一个**受限制的 Session 操作接口**。Harness 不需要知道 PostgreSQL 怎么连，只需要通过 Facade 调用 `save state` 或 `create checkpoint`。

## 14. `harness:<harness_id>` 是什么？
这是 Harness 的 Session State 命名空间。例如 `harness:customer-support`。它避免了同一个 Session 下，不同 Harness 的内部状态互相污染。

---

## 15. 三种 State Scope (状态生命周期)
系统明确区分三种状态，开发者必须存在正确的地方：

| 状态类型 | 生命周期/存活时间 | 典型用途 | 是否持久化？ |
| :--- | :--- | :--- | :--- |
| **Runtime State** | Runtime/Harness 实例存在期间 | 连接池、缓存。程序一关就没。 | ❌ 不持久化 |
| **Session State** | Session 生命周期 (长期存在) | 工作流、偏好、业务上下文。 | ✅ Checkpoint |
| **Turn State** | 一次 Agent turn (阅后即焚) | 临时变量、决策日志。 | ❌ 不长期保存 |

## 16-18. 状态的深入理解
*   **Runtime State:** 实例关闭就释放，无需存 Session。
*   **Session State:** 如果 Runtime 崩溃，重启后加载 Checkpoint 恢复工作进度。
*   **Turn State:** Turn 结束即释放，属于典型的 State Scoping 设计。

---

## 19. Checkpoint 是怎么工作的？
就像游戏的“存档点”。如果 Agent 执行到 Tool B 时崩溃，有了 Checkpoint，重启后可以直接恢复到 Tool B 之后继续执行 Tool C，避免从头开始浪费大量算力。

## 20. 为什么需要 HarnessStateCodec？
不同 Harness 的业务状态结构完全不同（客服存工单号，安全存风险分）。DojoAgents 使用 Codec（编解码器）负责将 Python State 和 Checkpoint data 互相转换，以及版本升级。

## 21. 为什么 checkpoint 还要保存 Harness version？
软件升级后，旧存档可能读不了。保存 `State Schema Version` 可以让系统在恢复时判断是否需要调用 `HarnessStateCodec.migrate()` 进行数据迁移。

---

## 22. 为什么需要 Lease（租约）？
当多台服务器（多个 Runtime）同时服务时，如果同时修改同一个 `Session-001` 会互相覆盖。Lease 就是当前 Session 的“临时编辑权”，拿到租约的实例才能写入。

## 23. Fencing Token (防护牌) 是什么？
如果 Runtime A 拿到 Lease（Token=10）后卡死了，Runtime B 拿到了新 Lease（Token=11）。如果 A 恢复了继续写，会覆盖 B。
Fencing Token 要求存储层“**只有更高或当前的 Token 才能写**”，从而防止失效实例覆盖数据。

## 24. Run Idempotency (幂等性) 是什么？
用户网络卡顿狂点发送，或者网络重试，如果没有幂等控制会产生多个重复的 Run。通过 `Idempotency Key` (幂等键)，相同的请求只会执行一次，防止重复计算。

## 25. Event 为什么需要持久化？
支持 Server-Sent Events (SSE) 断线恢复。如果用户手机断网，重连后可以根据 `last_event_id` 从 SessionStore 读取丢失的事件无缝恢复。消息总线只用于降低通知延迟，Store 才是可靠来源。

---

## 26. 为什么 Runtime 还需要 SessionService？
它是一个中间协调层（协调生命周期、事件、并发控制等）。Agent Core 和 Harness 通过它操作存储，从而实现和底层数据库的彻底解耦。

## 27-29. 为什么可以替换 SessionStore？如何替换？
DojoAgents 定义的是统一接口（Port/Adapter 思想）。
*   **开发环境：** 用 File 后端，简单免安装。
*   **生产环境：** 用 MySQL/PostgreSQL，支持多实例并发、事务、高可用。

**自定义 Store 必须全量实现接口：** 不能“碰巧用到哪个写哪个”，必须完整实现 lease, fencing, usage, checkpoint, cursor 等所有基础设施能力。

**💻 替换 Session 后端的实战配置示例 (`agents.yaml`)：**
```yaml
sessions:
  enabled: true
  store:
    provider: mysql
    factory: my_project.session_backends.mysql:create_session_store
    options:
      dsn_env: DOJO_SESSION_DSN  # 密码走环境变量，极其重要！
      pool_size: 20
```

---

## 30-31. Host Application 与 ExternalServiceBinding
FastAPI/CLI 属于 Host Application，负责认证和 HTTP。Harness 不能直接导入 FastAPI 路由，也不能写死 CRM 实现。
通过 `ExternalServiceBinding`，Harness 声明它需要

https://www.anthropic.com/engineering/advanced-tool-use

AI 代理（AI Agents）的未来，是一个模型能够在成百上千个工具之间无缝协作的世界。想象一下：一个集成了 Git 操作、文件处理、包管理器、测试框架以及部署流水线的 IDE 助手；或者一个能同时连接 Slack、GitHub、Google Drive、Jira、公司数据库以及数十个 MCP（模型上下文协议）服务器的运营协调员。

为了构建高效的代理，它们必须能够使用无限大的工具库，而不是一开始就把每一个工具的定义都塞进上下文里。在我们之前关于“如何结合 MCP 使用代码执行”的博客文章中曾讨论过，有时候在代理读取用户的请求之前，工具的返回结果和定义就能消耗掉超过 50,000 个 Token。代理应该具备**按需发现和加载工具**的能力，只保留对当前任务有用的内容。

此外，代理还需要能够**通过代码来调用工具**。在使用自然语言调用工具时，每一次调用都需要进行一次完整的推理（Inference pass），而且无论中间结果是否有用，它们都会堆积在上下文中。相比之下，代码天生就适合处理编排逻辑，比如循环、条件判断和数据转换。代理需要这种灵活性，以便根据手头的任务在代码执行和自然语言推理之间做出选择。

最后，代理还需要能够**从示例中学习工具的正确使用方法**，而不仅仅依赖于 Schema（模式）定义。JSON Schema 可以定义结构上什么是有效的，但无法表达使用习惯：比如什么时候该包含可选参数，哪些参数组合是有意义的，或者你的 API 期望怎样的命名约定。

今天，我们正式发布三大全新功能，让这一切成为可能：

*   **工具搜索工具（Tool Search Tool）**：允许 Claude 使用搜索工具来访问数千个工具，而不会耗尽其上下文窗口。
*   **编程式工具调用（Programmatic Tool Calling）**：允许 Claude 在代码执行环境中调用工具，大幅降低对模型上下文窗口的影响。
*   **工具使用示例（Tool Use Examples）**：提供了一个通用标准，用于向模型演示如何高效地使用特定工具。

在内部测试中，我们发现这些功能帮助我们构建出了传统工具调用模式下根本无法实现的应用。例如，“Claude for Excel”就使用了编程式工具调用来读取和修改包含数千行数据的电子表格，而不会让模型的上下文窗口超载。

基于我们的经验，我们相信这些功能将为您使用 Claude 进行构建打开全新的可能性。

---

## 1. 工具搜索工具 (Tool Search Tool)

### 挑战
MCP 工具定义提供了重要的上下文，但随着连接的服务器越来越多，这些 Token 的消耗会迅速累加。考虑以下这个连接了 5 个服务器的配置场景：

*   **GitHub**: 35 个工具（约 26,000 Tokens）
*   **Slack**: 11 个工具（约 21,000 Tokens）
*   **Sentry**: 5 个工具（约 3,000 Tokens）
*   **Grafana**: 5 个工具（约 3,000 Tokens）
*   **Splunk**: 2 个工具（约 2,000 Tokens）

在对话甚至还没开始之前，这 58 个工具就已经消耗了大约 55,000 个 Token。如果再添加像 Jira 这样的服务器（仅它自己就要占用约 17,000 个 Token），你将很快面临 100,000+ 的 Token 开销。在 Anthropic 内部，我们甚至见过未经优化前，工具定义就消耗了 134,000 个 Token 的情况。

但 Token 成本并非唯一的问题。最常见的失败在于**错误的工具选择**和**错误的参数传递**，尤其是当工具名称非常相似时（例如 `notification-send-user` 与 `notification-send-channel`）。

### 我们的解决方案
“工具搜索工具”不再一开始就加载所有的工具定义，而是按需动态发现工具。Claude 只会看到它当前任务实际需要的工具。

通过工具搜索工具，与 Claude 传统方法（保留 122,800 个 Token 上下文）相比，现在可以保留 191,300 个 Token 的上下文。

**传统方法：**
*   一开始加载所有工具定义（50+ 个 MCP 工具约 72K Token）
*   对话历史和系统提示词（System Prompt）竞争剩余的上下文空间
*   **总上下文消耗：** 在开始任何工作前约为 **77K Tokens**

**使用工具搜索工具：**
*   一开始只加载“工具搜索工具”本身（约 500 Tokens）
*   按需动态发现工具（检索 3-5 个相关工具，约 3K Tokens）
*   **总上下文消耗：** 约 **8.7K Tokens**，保留了 95% 的上下文窗口

这不仅意味着 Token 使用量减少了 **85%**，同时依然保持了对整个工具库的访问权限。内部测试表明，在处理大型工具库时，启用工具搜索工具后，MCP 评估的准确率有了显著提升：Opus 4 的准确率从 49% 提升到了 **74%**，Opus 4.5 从 79.5% 提升到了 **88.1%**。

### 工具搜索工具是如何工作的
工具搜索工具让 Claude 动态发现工具，而不是预先加载所有定义。你可以向 API 提供所有的工具定义，但将它们标记为 `defer_loading: true`（延迟加载），使它们可以在需要时被检索到。被延迟加载的工具最初不会进入 Claude 的上下文。Claude 一开始只能看到“工具搜索工具”本身，以及任何标记为 `defer_loading: false` 的工具（即你最核心、最常用的工具）。

当 Claude 需要特定功能时，它会搜索相关工具。工具搜索工具会返回匹配工具的引用，然后这些引用才会在 Claude 的上下文中展开为完整的定义。

例如，如果 Claude 需要与 GitHub 交互，它会搜索“github”，那么只有 `github.createPullRequest` 和 `github.listIssues` 会被加载——而不是把 Slack、Jira 和 Google Drive 中剩下的 50 多个工具全加载进来。

这样一来，Claude 就能访问你的完整工具库，同时你只需为它实际使用的工具支付 Token 成本。

> **提示词缓存 (Prompt caching) 注意事项：** 工具搜索工具不会破坏提示词缓存机制，因为被延迟加载的工具从一开始就被完全排除在了初始提示词之外。它们只有在 Claude 搜索后才会被添加到上下文中，因此你的系统提示词和核心工具定义仍然是可以被缓存的。

**代码实现：**

```json
{
  "tools": [
    // 包含一个工具搜索工具（支持正则表达式、BM25 或自定义）
    {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},

    // 标记需要按需发现的工具
    {
      "name": "github.createPullRequest",
      "description": "Create a pull request",
      "input_schema": {...},
      "defer_loading": true
    }
    // ... 还有成百上千个带有 defer_loading: true 的延迟工具
  ]
}
```

对于 MCP 服务器，你可以选择延迟加载整个服务器，同时保持特定的高频工具始终处于加载状态：

```json
{
  "type": "mcp_toolset",
  "mcp_server_name": "google-drive",
  "default_config": {"defer_loading": true}, // 延迟加载整个服务器
  "configs": {
    "search_files": {
      "defer_loading": false // 保持最常用的工具处于加载状态
    }
  }
}
```

Claude 开发者平台提供了开箱即用的基于正则匹配（Regex）和基于 BM25 的搜索工具，但你也可以使用向量嵌入（Embeddings）或其他策略实现自定义的搜索工具。

### 何时使用工具搜索工具
像任何架构决策一样，启用工具搜索工具涉及权衡。该功能在调用工具之前增加了一个搜索步骤，因此当“节省的上下文成本和准确率的提升”大于“增加的延迟”时，它的投资回报率最高。

**最适合使用的场景：**
*   工具定义占用的 Token 超过 10,000
*   遇到工具选择准确率低下的问题
*   构建包含多个服务器的 MCP 驱动系统
*   拥有 10 个以上的可用工具

**不太适用的场景：**
*   工具库很小（<10 个工具）
*   所有工具在每次会话中都会被频繁使用
*   工具的定义本身非常简短紧凑

---

## 2. 编程式工具调用 (Programmatic Tool Calling)

### 挑战
随着工作流变得越来越复杂，传统的工具调用会产生两个根本性问题：

1.  **中间结果导致上下文污染：** 当 Claude 分析一个 10MB 的日志文件以寻找错误模式时，整个文件都会进入其上下文窗口，尽管 Claude 实际需要的仅仅是错误频率的摘要。当跨多个表获取客户数据时，每条记录都会堆积在上下文中，无论其是否相关。这些中间结果消耗了海量的 Token 预算，甚至可能把重要信息完全挤出上下文窗口。
2.  **推理开销和手动综合分析：** 每调用一次工具，就需要进行一次完整的模型推理。收到结果后，Claude 必须通过自然语言处理，用“肉眼”去提取相关信息、推理各部分之间的联系并决定下一步做什么。一个包含 5 个工具的工作流意味着 5 次推理阶段，加上 Claude 解析每个结果、比较数值并得出结论的开销。这既缓慢又容易出错。

### 我们的解决方案
编程式工具调用（Programmatic Tool Calling, PTC）使 Claude 能够通过代码（而非单独的 API 往返）来编排工具。Claude 不再需要一次请求一个工具并把每个结果都扔回上下文中，而是编写一段代码来调用多个工具，处理它们的输出，并**精确控制哪些信息最终进入其上下文窗口**。

Claude 非常擅长编写代码。让它在 Python 中表达编排逻辑，而不是通过自然语言的工具调用，可以为您带来更可靠、更精确的控制流。循环、条件判断、数据转换和错误处理都在代码中得到了明确表达，不再隐含在 Claude 的语言推理中。

### 示例：预算合规性检查
考虑一个常见的业务任务：“哪些团队成员超出了他们第三季度的差旅预算？”

你提供了 3 个可用工具：
*   `get_team_members(department)` - 返回带有 ID 和职级的团队成员列表
*   `get_expenses(user_id, quarter)` - 返回某个用户的报销明细行
*   `get_budget_by_level(level)` - 返回特定员工职级的预算上限

**传统方法：**
1.  获取团队成员 → 返回 20 个人
2.  针对每个人，获取他们 Q3 的报销明细 → **20 次工具调用**，每次返回 50-100 行明细（机票、酒店、餐饮、收据）
3.  按员工职级获取预算上限
4.  所有这些数据全部进入 Claude 的上下文：**2,000+ 条报销明细（超过 50 KB 的数据）**
5.  Claude 手动将每个人的费用相加，查找他们的预算，比较费用和预算限制
6.  **结果：**与模型产生大量的往返交互，导致巨大的上下文消耗。

**使用编程式工具调用：**
工具的结果不会直接返回给 Claude。相反，Claude 会编写一个 Python 脚本来编排整个工作流。该脚本在“代码执行工具（Code Execution tool）”（一个沙箱环境）中运行，当需要工具结果时脚本会暂停。当你通过 API 返回工具结果时，它们会**被脚本处理**，而不是被模型消耗。脚本继续执行，最终 Claude **只看到最终的输出结果**。

这使得 Claude 能够并行执行工具调用。以下是 Claude 为此预算合规任务生成的编排代码示例：

```python
team = await get_team_members("engineering")

# 为每一个不重复的职级获取预算
levels = list(set(m["level"] for m in team))
budget_results = await asyncio.gather(*[
    get_budget_by_level(level) for level in levels
])

# 创建查找字典: {"junior": budget1, "senior": budget2, ...}
budgets = {level: budget for level, budget in zip(levels, budget_results)}

# 并行获取所有的报销明细
expenses = await asyncio.gather(*[
    get_expenses(m["id"], "Q3") for m in team
])

# 找出超出差旅预算的员工
exceeded = []
for member, exp in zip(team, expenses):
    budget = budgets[member["level"]]
    total = sum(e["amount"] for e in exp)
    if total > budget["travel_limit"]:
        exceeded.append({
            "name": member["name"],
            "spent": total,
            "limit": budget["travel_limit"]
        })

print(json.dumps(exceeded))
```

Claude 的上下文仅仅接收到最终结果：两到三个超支的人。那 2,000 多行明细、中间的求和计算以及预算查找过程**完全不会影响 Claude 的上下文**。这将上下文消耗从 200KB 的原始报销数据骤降到了仅 1KB 的结果数据。

效率的提升是巨大的：
*   **节省 Token：** 通过将中间结果挡在 Claude 的上下文之外，PTC 大幅降低了 Token 消耗。在复杂的研究任务上，平均消耗从 43,588 Tokens 下降到 27,297 Tokens，降幅达 **37%**。
*   **降低延迟：** 每一次 API 往返都需要模型推理（耗时几百毫秒到几秒不等）。当 Claude 在一个代码块中编排 20 多个工具调用时，你**消除了 19 次以上的推理阶段**。API 直接处理工具执行，无需每次都返回给模型。
*   **提高准确率：** 通过编写显式的编排逻辑，Claude 犯的错误比在自然语言中处理多重工具结果时要少得多。内部知识检索准确率从 25.6% 提高到 **28.5%**；GIA 基准测试从 46.5% 提高到 **51.2%**。

生产环境中的工作流往往伴随着杂乱的数据、复杂的条件逻辑和需要扩展的操作。编程式工具调用让 Claude 以编程的方式应对这些复杂性，同时保持其注意力集中在“可操作的结果”上，而不是去生啃原始数据。

### 编程式工具调用是如何工作的

**1. 标记工具为“允许从代码中调用”**
在 `tools` 列表中添加 `code_execution` 工具，并使用 `allowed_callers` 让特定的工具选择加入（opt-in）编程式执行：

```json
{
  "tools": [
    {
      "type": "code_execution_20250825",
      "name": "code_execution"
    },
    {
      "name": "get_team_members",
      "description": "Get all members of a department...",
      "input_schema": {...},
      "allowed_callers": ["code_execution_20250825"] // 允许被编程式调用
    },
    {
      "name": "get_expenses",
      // ...
    },
    {
      "name": "get_budget_by_level",
      // ...
    }
  ]
}
```
API 会将这些工具定义转换为 Claude 可以调用的 Python 函数。

**2. Claude 编写编排代码**
不再是一个一个请求工具，Claude 会直接生成 Python 代码：

```json
{
  "type": "server_tool_use",
  "id": "srvtoolu_abc",
  "name": "code_execution",
  "input": {
    "code": "team = get_team_members('engineering')\n..." // 也就是上面的那段代码
  }
}
```

**3. 工具在不进入 Claude 上下文的情况下执行**
当代码中调用 `get_expenses()` 时，您将收到一个带有 `caller` 字段的工具请求：

```json
{
  "type": "tool_use",
  "id": "toolu_xyz",
  "name": "get_expenses",
  "input": {"user_id": "emp_123", "quarter": "Q3"},
  "caller": {
    "type": "code_execution_20250825",
    "tool_id": "srvtoolu_abc"
  }
}
```
您提供结果后，结果会在“代码执行（Code Execution）”环境中进行处理，而不是回到 Claude 的上下文中。这个请求-响应循环会针对代码中的每个工具调用重复进行。

**4. 只有最终输出才会进入上下文**
代码运行结束后，只有代码的执行结果被返回给 Claude：

```json
{
  "type": "code_execution_tool_result",
  "tool_use_id": "srvtoolu_abc",
  "content": {
    "stdout": "[{\"name\": \"Alice\", \"spent\": 12500, \"limit\": 10000}...]"
  }
}
```
这就是 Claude 看到的全部内容，而不是处理过程中那 2000 多条报销明细。

### 何时使用编程式工具调用
编程式工具调用在工作流中增加了一个代码执行步骤。当 Token 节省量、延迟改善和准确率提升显著时，这种额外的开销就是物超所值的。

**最适合使用的场景：**
*   处理大型数据集，且只需要汇总或摘要信息时
*   运行包含 3 个以上互相依赖工具调用的多步骤工作流
*   在 Claude 看到工具结果之前，需要对其进行过滤、排序或转换
*   处理“中间数据不应影响 Claude 推理过程”的任务
*   跨大量项目并行运行操作（例如，同时检查 50 个终端节点）

**不太适用的场景：**
*   简单的单次工具调用
*   任务要求 Claude 必须看到所有中间结果并对其进行推理
*   响应数据量非常小的快速查询任务

---

## 3. 工具使用示例 (Tool Use Examples)

### 挑战
JSON Schema 极其擅长定义数据结构——类型、必填字段、允许的枚举值等——但它无法表达使用模式：何时应该包含可选参数、哪些组合才有意义、或者您的 API 期望遵循什么内部约定。

来看一个技术支持工单 API 的例子：

```json
{
  "name": "create_ticket",
  "input_schema": {
    "properties": {
      "title": {"type": "string"},
      "priority": {"enum": ["low", "medium", "high", "critical"]},
      "labels": {"type": "array", "items": {"type": "string"}},
      "reporter": {
        "type": "object",
        "properties": {
          "id": {"type": "string"},
          "name": {"type": "string"},
          "contact": {
            "type": "object",
            "properties": {
              "email": {"type": "string"},
              "phone": {"type": "string"}
            }
          }
        }
      },
      "due_date": {"type": "string"},
      "escalation": {
        "type": "object",
        "properties": {
          "level": {"type": "integer"},
          "notify_manager": {"type": "boolean"},
          "sla_hours": {"type": "integer"}
        }
      }
    },
    "required": ["title"]
  }
}
```
这个 schema 定义了什么是合法的结构，但却留下了许多未解的关键疑问：
*   **格式歧义：** `due_date` 应该是 "2024-11-06"、"Nov 6, 2024" 还是 "2024-11-06T00:00:00Z"？
*   **ID 约定：** `reporter.id` 是个 UUID，是 "USR-12345"，还是仅仅为 "12345"？
*   **嵌套结构用法：** Claude 究竟在什么时候需要填充 `reporter.contact`？
*   **参数间的关联：** `escalation.level`、`escalation.sla_hours` 与 `priority`（优先级）之间是什么关系？

这些歧义极易导致结构异常的工具调用和不一致的参数传值。

### 我们的解决方案
“工具使用示例”允许您直接在工具定义中提供示例调用。不要仅仅依赖 Schema，您可以通过直接向 Claude 演示具体的使用模式来解决问题：

```json
{
    "name": "create_ticket",
    "input_schema": { /* 同上方的 schema */ },
    "input_examples": [
      {
        "title": "Login page returns 500 error",
        "priority": "critical",
        "labels": ["bug", "authentication", "production"],
        "reporter": {
          "id": "USR-12345",
          "name": "Jane Smith",
          "contact": {
            "email": "jane@acme.com",
            "phone": "+1-555-0123"
          }
        },
        "due_date": "2024-11-06",
        "escalation": {
          "level": 2,
          "notify_manager": true,
          "sla_hours": 4
        }
      },
      {
        "title": "Add dark mode support",
        "labels": ["feature-request", "ui"],
        "reporter": {
          "id": "USR-67890",
          "name": "Alex Chen"
        }
      },
      {
        "title": "Update API documentation"
      }
    ]
  }
```

通过这三个示例，Claude 能够学习到：
*   **格式约定：** 日期使用 `YYYY-MM-DD` 格式，用户 ID 遵循 `USR-XXXXX` 格式，标签（labels）使用 kebab-case（连字符命名法）。
*   **嵌套结构模式：** 包含其嵌套 `contact` 对象的 `reporter` 对象应该如何构建。
*   **可选参数的关联：** “Critical（严重）”级别的 bug 会携带完整的联系信息和有严格 SLA 限制的升级（escalation）配置；特性请求只带报告者（reporter）而不带联系方式或升级配置；内部任务只需填写标题。

在我们内部测试中，工具使用示例在处理复杂参数时的准确率从 72% 提升到了 **90%**。

### 何时使用工具使用示例
因为添加示例会增加工具定义消耗的 Token，所以只有在准确率提升的价值超过增加的成本时，它们才最有价值。

**最适合使用的场景：**
*   合法 JSON 结构并不能暗示出正确用法的复杂嵌套结构
*   拥有大量可选参数，且参数的包含规则（inclusion patterns）很重要的工具
*   Schema 无法捕获且具有强特定领域约定的 API
*   功能相似的工具（例如 `create_ticket` 和 `create_incident`），可以通过示例帮助区分该用哪一个

**不太适用的场景：**
*   用法非常显而易见的简单单参数工具
*   Claude 已经熟知的标准格式，如 URL 或电子邮件
*   那些使用 JSON Schema 约束就能很好处理的纯验证问题

---

## 最佳实践 (Best Practices)

要构建能在现实世界中执行操作的代理，意味着您必须同时处理规模、复杂性和精确度。这三大功能协同工作，能解决工具使用工作流中不同环节的瓶颈。以下是如何有效地组合它们：

### 战略性地分层使用功能
并不是每个代理都需要在所有任务中强行用上这三大功能。**从您最大的瓶颈开始入手：**
*   工具定义导致的上下文膨胀 → 使用**工具搜索工具**
*   海量中间结果污染了上下文 → 使用**编程式工具调用**
*   频繁出现参数错误和调用格式错误 → 使用**工具使用示例**

这种聚焦的方法让您可以精准解决限制代理性能的具体问题，而不是一开始就引入不必要的复杂性。

之后再按需叠加其他功能。它们是高度互补的：工具搜索工具确保**找到正确的工具**，编程式工具调用确保**高效地执行**，而工具使用示例确保**调用的正确性**。

### 配置工具搜索工具以获得更好的发现效果
工具搜索主要匹配名称和描述，因此清晰、描述性强的定义能够提升发现的准确率。

```json
// 正确做法 (Good)
{
    "name": "search_customer_orders",
    "description": "Search for customer orders by date range, status, or total amount. Returns order details including items, shipping, and payment info."
}

// 错误做法 (Bad)
{
    "name": "query_db_orders",
    "description": "Execute order query"
}
```

**添加系统提示词引导**，让 Claude 知道有哪些能力可用：
> "You have access to tools for Slack messaging, Google Drive file management, Jira ticket tracking, and GitHub repository operations. Use the tool search to find specific capabilities."

始终保持您最常用的 **3 到 5 个工具**处于加载状态，其余的则设置为延迟加载。这可以在“常见操作的即时访问”与“其他一切的按需发现”之间取得完美平衡。

### 配置编程式工具调用以确保正确执行
由于 Claude 会编写代码来解析工具的输出，因此请**清晰地说明返回数据的格式**。这能帮助 Claude 写出准确的解析逻辑：

```json
{
    "name": "get_orders",
    "description": "Retrieve orders for a customer.\nReturns:\n    List of order objects, each containing:\n    - id (str): Order identifier\n    - total (float): Order total in USD\n    - status (str): One of 'pending', 'shipped', 'delivered'\n    - items (list): Array of {sku, quantity, price}\n    - created_at (str): ISO 8601 timestamp"
}
```

强烈建议以下类型的工具加入（opt-in）编程式编排：
*   能够并行运行的工具（独立操作）
*   可以安全重试的工具（具有幂等性）

### 配置工具使用示例以提升参数准确性
为了清晰展示行为模式，请精心设计示例：
*   **使用真实数据**（使用真实的城市名称、合理的价格数字，不要填入无意义的 "string" 或 "value"）
*   **展示多样性**，提供参数最小化、部分填写和全部完整填写的调用模式
*   **保持简练**：每个工具提供 1-5 个示例即可
*   **聚焦于歧义痛点**（仅为那些无法单纯通过 schema 看出正确用法的场景添加示例）

---

## 快速上手指南

这些功能现已在 Beta 版中提供。想要启用它们，请添加 beta 请求头，并在请求中包含您所需要的工具：

```python
client.beta.messages.create(
    betas=["advanced-tool-use-2025-11-20"],
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    tools=[
        {"type": "tool_search_tool_regex_20251119", "name": "tool_search_tool_regex"},
        {"type": "code_execution_20250825", "name": "code_execution"},
        # 在此处放入您配置了 defer_loading、allowed_callers 以及 input_examples 的工具
    ]
)
```

如需获取详细的 API 文档和 SDK 示例，请参阅我们的：
*   工具搜索工具的文档与 Cookbook
*   编程式工具调用的文档与 Cookbook
*   工具使用示例的文档

这些功能的推出，标志着“工具使用”正在从简单的“函数调用（function calling）”迈向真正的“智能编排（intelligent orchestration）”。当 AI 代理开始应对横跨数十个工具和海量数据的复杂工作流时，动态的工具发现、高效的执行以及可靠的调用，必将成为最坚实的技术基石。
**Programmatic Tool Calling (PTC)**—often referred to as **Code Mode**—is a paradigm shift in how AI agents execute multi-step tasks. 

Instead of generating rigid JSON blocks for every tool call and waiting for the host system to send back raw API results, **Claude writes Python code to orchestrate, filter, loop over, and process tool calls programmatically inside an execution sandbox**.

---

### The Paradigm Shift: Traditional vs. Programmatic Tool Calling

#### Traditional Tool Calling (JSON Round-Trips)
```text
User Request ──> LLM ──> JSON Tool Call ──> Host App Executes Tool
                 ▲                                     │
                 └────── Return Raw API JSON Data ─────┘  (Repeats 10–20 times!)
```
* **Problems:** 
  * If an API tool returns 50,000 rows of JSON, that entire payload gets dumped directly into Claude's context window.
  * Running a loop across 20 database items requires 20 separate LLM API round-trips, causing high cost, high token bloat, and long latency.

#### Programmatic Tool Calling (Code Execution Sandbox)
```text
User Request ──> LLM ──> Writes Python Script
                             │ (Executed in isolated Sandbox)
                             ├── Loop over APIs
                             ├── Filter 50,000 rows -> 5 rows
                             └── Calculate totals
                                     │
                 LLM ◄── Return ONLY Final 5 Rows (Final Answer)
```
* **Benefits:**
  * **Up to 98% Token Reduction:** Bulk intermediate data remains inside the Python runtime environment, never polluting Claude's context.
  * **1-Turn Loops & Logic:** Claude uses standard `for` loops, `if/else` conditionals, and data manipulation libraries (like `pandas` or standard math) in Python rather than spending LLM turns.
  * **Higher Accuracy:** Code is deterministic—calculating averages, sums, and complex logic in code eliminates LLM arithmetic hallucinations.

---

### Key API Implementation Requirements

To enable Programmatic Tool Calling via the Anthropic API, three key configurations are required:

1. **Beta Header:** Include `advanced-tool-use-2025-11-20` in your request headers.
2. **Code Execution Tool:** Declare the code execution tool in your `tools` list (e.g. `code_execution_20250825`).
3. **`allowed_callers` Tag:** In your custom tool schemas, add `"allowed_callers": ["code_execution_20250825"]`. This tells Claude that this specific tool can be called directly from Python code inside the sandbox rather than via standard JSON tool blocks.

---

### Complete Python Implementation Example

Here is a working implementation using the Anthropic API SDK demonstrating how Claude programmatically queries database endpoints across multiple regions in Python:

```python
import os
import json
from anthropic import Anthropic

# Initialize Anthropic Client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# 1. Define custom tools that can be invoked via Python code
db_tool_schema = {
    "name": "query_regional_database",
    "description": "Queries sales records for a specific region. Returns JSON with fields: region, revenue, tax_rate.",
    "input_schema": {
        "type": "object",
        "properties": {
            "region": {
                "type": "string", 
                "description": "Region name (e.g. north_america, europe, asia_pacific, latam)"
            }
        },
        "required": ["region"]
    },
    # IMPORTANT: Allow this tool to be executed programmatically inside Python!
    "allowed_callers": ["code_execution_20250825"]
}

# 2. Add Code Execution capability alongside custom tools
tools = [
    {
        "type": "code_execution_20250825",
        "name": "code_execution"
    },
    db_tool_schema
]

# 3. User query requiring data from multiple sources and computation
prompt = (
    "Check sales for 'north_america', 'europe', 'asia_pacific', and 'latam'. "
    "Calculate the net revenue (revenue minus tax) for each, filter out regions "
    "with net revenue under $50,000, and return only the top performing region."
)

# 4. Make API call using the Advanced Tool Use beta header
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    betas=["advanced-tool-use-2025-11-20"],
    max_tokens=2048,
    tools=tools,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

print(response)
```

---

### What Claude Generates Behind the Scenes

When Claude receives this request, instead of making 4 separate sequential tool call steps via JSON, Claude generates and runs a Python script inside the container:

```python
# Code written autonomously by Claude inside the Python sandbox:
import query_regional_database

regions = ['north_america', 'europe', 'asia_pacific', 'latam']
results = []

for r in regions:
    # Programmatic tool call to host tools directly in code!
    data = query_regional_database(region=r)
    net_revenue = data['revenue'] * (1 - data['tax_rate'])
    
    if net_revenue >= 50000:
        results.append({'region': r, 'net_revenue': net_revenue})

# Sort and pick winner inside the sandbox
top_region = max(results, key=lambda x: x['net_revenue'])
print(f"Top Region: {top_region['region']} with Net Revenue: ${top_region['net_revenue']:,.2f}")
```

### Response Result Comparison

| Metric | Traditional JSON Tool Calling | Programmatic Tool Calling |
| :--- | :--- | :--- |
| **API Round Trips** | 5 round trips (4 calls + final answer) | **1 round trip** |
| **Tokens Consumed** | ~15,000–50,000 tokens (raw responses in context) | **~1,200 tokens** (only final summary returned) |
| **Latency** | 12–25 seconds | **2–4 seconds** |
| **Computation Accuracy** | Susceptible to arithmetic errors | **100% Deterministic (Python math)** |

---

### How to Build a Custom Programmatic Tool Calling Engine (Self-Managed Sandbox)

If you are using custom local models (like Qwen, Llama) or building your own custom runtime engine without using Anthropic's managed cloud execution environment, you use the **Tool Bridge Pattern**:

1. **Docker / E2B Sandbox Isolation:** Spin up an isolated Python runtime container (e.g. using `docker` or `llm-sandbox` / `e2b`).
2. **Tool Injection:** Inject Python wrapper functions inside the sandbox environment that map directly to your local APIs/databases via local RPC calls or HTTP endpoints.
3. **Execution Pipeline:**
   * Prompt model: *"Write Python code to accomplish task X. Use imported functions `[tool_a(), tool_b()]`."*
   * Capture model's code block -> execute code inside the sandboxed container -> capture `stdout`/`stderr`.
   * Feed back **only the `stdout` summary** to the model.


# E2B

---

### 一、 什么是 E2B Sandbox Isolation（E2B 沙箱隔离）？

#### 1. 什么是 E2B？
**E2B (Enterprise to Developer)** 是一种专门为 AI Agent（如 Claude、GPT-4 等）设计的**安全代码执行沙箱服务/开源框架**。它底层通常基于 Firecracker 微型虚拟机（MicroVM）或轻量级 Docker 隔离技术。

#### 2. 为什么要进行“沙箱隔离（Sandbox Isolation）”？
LLM 在生成并执行代码（比如 Python）时，存在极大的安全风险：
* **恶意/错误代码**：模型可能会生成 `import os; os.system("rm -rf /")` 这种破坏性指令，或者写出无限递归死循环。
* **数据泄露**：如果不隔离，生成的代码可能会读取你服务器上的 `.env` 环境变量、密钥或本地敏感文件。

**沙箱隔离的作用**：
* **彻底隔离（Isolation）**：在宿主服务器之外，瞬间（几毫秒内）弹出一个纯净、封闭的虚拟机/容器。LLM 生成的代码在这个封闭环境里运行。哪怕代码把这个沙箱“搞崩了”或执行了删除指令，也**完全影响不到你真实的宿主服务器**，运行完随手销毁即可。
* **资源限制**：限制 CPU、内存和运行时间上限（比如最多运行 10 秒）。

---

### 二、 什么是 Tool Injection（工具注入与映射机制）？

> 原文："Tool Injection: Inject Python wrapper functions inside the sandbox environment that map directly to your local APIs/databases via local RPC calls or HTTP endpoints"

这段话解决了一个核心矛盾：
👉 **沙箱是被彻底封禁隔离的，但 Python 代码又需要查询你真实的本地数据库或调用内部 API，怎么办？**

**答案就是：工具注入（Tool Injection）。**

#### 工作机制拆解：

![[Pasted image 20260826210951.png]]

#### 详细步骤说明：

1. **注入包装函数 (Inject Python wrapper functions)**：
   在 E2B 沙箱启动 Python 环境时，程序会在 Python 的全局作用域里**预先载入**一些简单的 Python 函数（即 Wrapper 函数）。
   * 对 Claude 来说，它在 Python 里看到的就是一个普通的函数：`query_db(sql)`。

2. **内部通过 RPC / HTTP 映射 (Map via RPC/HTTP)**：
   这个 `query_db(sql)` 函数内部并没有安装数据库驱动，也不直接存有数据库密码。**它的底层实现只是一段网络请求代码**（通过 RPC 或 HTTP）。
   * 当沙箱里的代码运行 `query_db("SELECT...")` 时，它会向沙箱外部（宿主机的 Bridge 代理服务）发起一个网络请求。

3. **宿主机安全代执行**：
   宿主机上的 Bridge 代理接收到请求后，用真实的数据库连接去查数据库，拿到 JSON 结果，再把结果返还给沙箱内部的 `query_db` 函数。

---

### 三、 通俗的比喻

* **E2B 沙箱隔离**：就像给一个外聘的实习生（AI 代码）准备了一间**绝对隔离的无尘无网玻璃密室**。他在里面怎么折腾、丢垃圾都不会破坏公司大楼（宿主服务器）。
* **Tool Injection（工具注入）**：因为密室是隔离的，实习生无法自己跑去公司财务室看账本（访问真实 DB）。于是你在密室墙上装了一部**专用对讲机（Python Wrapper 函数）**。
  * 实习生只需要对着对讲机喊：“帮我查一下 A 部门的账单”（调用函数）。
  * 墙外的正式员工（宿主机 RPC Bridge）收到指令后，去财务室查好结果，再通过对讲机把答案报给密室里的实习生。

---

### 四、 总结

将 **E2B 沙箱隔离** 与 **工具注入（Tool Injection）** 结合，是目前构建自主 AI Agent 系统最标准、最安全的做法：
1. **沙箱隔离** 保证了**安全性**（防止恶意代码破坏系统）。
2. **工具注入** 保证了**连通性**（让隔离的代码依然能够安全地调用外部 API / 数据库数据）。

# Language Intelligence Tools
在软件开发和开发工具（DevTools）领域，**语言智能工具（Language Intelligence Tools）** 指的是**能够“理解”编程语言的语法、结构、类型系统和语义，并为开发者提供实时代码辅助与分析的后端引擎或程序**。

简单来说，它们就是让代码编辑器（如 VS Code、Neovim、Cursor）变“聪明”的**幕后大脑**。

---

### 一、 语言智能工具核心解决什么问题？

文本编辑器本身只知道代码是“一堆字符/纯文本”。而语言智能工具的作用，是把这些纯文本解析成**计算机可以理解的代码结构（如抽象语法树 AST、符号表、类型图）**，从而实现对代码的“深度理解”。

如果没有语言智能工具：
* 编辑器无法知道某个变量是在哪里定义的。
* 输入 `user.` 时，编辑器无法弹出 `user` 对象下有哪些属性和方法。
* 写错语法或类型时，只有等到编译或运行那一步才会报错。

---

### 二、 语言智能工具的主要能力

语言智能工具通常提供以下 5 大核心功能：

#### 1. 智能补全与推断（Autocompletion & Type Inference）
* 当你输入 `person.` 时，工具会根据上下文和类型定义，智能弹出该对象包含的字段或方法（如 `person.getName()`），并给出参数提示。

#### 2. 实时诊断与错误检查（Diagnostics & Linting）
* 在你打字的同时，后台实时检查代码中的语法错误、类型不匹配、未使用的变量或潜在的安全漏洞，并在代码下方画红线/黄线波浪线提示。

#### 3. 符号导航与引用查找（Navigation & Definition）
* **Go to Definition（跳转到定义）**：按住 `Ctrl/Cmd + 单击`，瞬间跳转到函数或类声明的位置。
* **Find References（查找引用）**：找到整个项目中所有调用了该函数的地方。

#### 4. 安全的代码重构（Refactoring）
* **Symbol Rename（符号重命名）**：修改一个变量或方法的名字，工具会自动跨文件更新所有调用它的地方，而不会误伤同名的字符串或注释。

#### 5. 代码格式化（Formatting）
* 自动按照语言规范（如 PEP 8、Prettier）调整代码缩进、空格和排版。

---

### 三、 常见的语言智能工具代表

在日常开发中，你每天都在使用这些工具（通常以 **LSP 语言服务器（Language Server）** 或 **静态分析器** 的形式存在）：

| 编程语言 | 代表性的语言智能工具 / 语言服务器 |
| :--- | :--- |
| **Python** | `Pyright` / `Pylance`（微软）, `Ruff`, `pylsp` |
| **Rust** | `rust-analyzer` |
| **Go** | `gopls` |
| **TypeScript / JS** | `vtsls` / `tsserver`, `ESLint` |
| **C / C++** | `clangd` |
| **通用的语法解析器** | `Tree-sitter`（超高速增量语法解析引擎） |

---

### 四、 传统语言智能 vs. AI 语言智能

随着 AI 技术的爆发，“语言智能”的概念正在从**传统的静态分析**向**大模型 AI 智能**演进：

| 维度 | 传统语言智能工具 (如 LSP / Pyright) | AI 语言智能工具 (如 Copilot / Claude / Cursor) |
| :--- | :--- | :--- |
| **工作原理** | 基于确定性的编译器原理、抽象语法树 (AST)、类型系统。 | 基于概率分布的大语言模型 (LLM)、Transformer 架构。 |
| **准确性** | **100% 确定性**（精准，绝不会犯低级语法/类型推断错误）。 | **概率性**（可能产生幻觉，但具备创造力和自然语言推断能力）。 |
| **能力边界** | 擅长语法检查、类型推断、精确重构、精确跳转。 | 擅长根据上下文直接生成完整代码块、解释复杂逻辑、自动修复 Bug。 |

#### 当前的最佳实践（两者结合）：
现代顶尖的 AI 代码编辑器（如 Cursor、Claude Code）并不是单独依赖 AI，而是**将传统语言智能工具与 AI 结合**：
* 先用 **传统语言智能工具 (LSP)** 精确获取代码的类型定义和符号树。
* 再把这些精确数据作为 Prompt 上下文喂给 **AI 大模型**。
* 这样生成的代码既准确（不幻觉），又具备强大的逻辑生成能力。
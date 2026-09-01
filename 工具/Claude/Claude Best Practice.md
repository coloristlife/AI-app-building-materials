---
内容生成: AI
---

Claude Code 与传统的网页端 ChatGPT/Claude 不同，**它可以直接读取你的本地文件系统、执行终端命令、修改代码并自己运行测试。** 这种“自主性”决定了我们使用它的方式必须从“指令式编程”转变为“结对编程”或“项目经理+技术主管”的模式。

关于你的核心问题：**是给它具体的实现细节（Implementation Detail），还是用户需求（User Requirements）？**
**答案是：两者都需要，但要在不同的阶段给，且侧重点不同。最成功的模式是“给出明确的用户需求 + 严格的技术约束”，而把“具体代码怎么写”交给它。**

以下是使用 Claude Code 从零到一开发 App 的 **Best Practices (最佳实践) 和 Guidance (指南)**：

---

### 一、 核心法则：如何平衡“需求”与“细节”

#### 1. 前期：扮演产品经理（给需求） + 架构师（给约束）
不要一上来就让它写具体的函数。你应该给它一个高视角的 Context。
*   **给用户需求 (User Requirements)：** 告诉它你要做什么，目标用户是谁，核心功能是什么。
*   **给技术约束 (Technical Constraints)：** 这是极其重要的一步！你需要明确告诉它使用什么技术栈（例如：Next.js App Router, TailwindCSS, Supabase, TypeScript），以及你不希望它用什么（例如：不要用 Class Component）。
*   **❌ 错误示范：** “帮我写一个 React 登录组件，包含 email 和 password 的 input，点击后调用 fetch 发送 POST 请求到 /api/login。”（太细节，限制了它的发挥，且容易出错）
*   **✅ 正确示范：** “我要做一个 Todo App，现在需要实现用户登录功能。技术栈是 React + Firebase Auth。请帮我实现一个美观的登录页面，包含邮箱密码登录和 Google 登录。请先设计方案并告诉我你打算修改/创建哪些文件。”

#### 2. 中期：扮演代码审查员（Reviewer）
Claude Code 具备自己查看项目、阅读代码的能力。
*   当它给出计划后，如果你觉得没问题，再让它执行（`Proceed`）。
*   如果它写错了，**不要自己去改代码**，而是把终端的报错信息、或者 UI 的表现告诉它，让它自己去 Debug。

---

### 二、 Claude Code 高效开发工作流 (Best Practices)

#### 1. 使用 `PRD.md` 或 `SPEC.md` 作为“单点真相” (Single Source of Truth)
不要在对话框里长篇大论地输入所有需求。
*   **做法：** 在项目根目录创建一个 `spec.md` 或 `architecture.md` 文件。把你的 App 需求、数据库设计、UI 风格写在里面。
*   **Prompt：** “Please read `spec.md`. We are going to build this app step by step. Let's start with Step 1: Initialize the project and setup the database schema.”
*   **优势：** Claude Code 可以随时去读取这个文件，这样在漫长的开发过程中它永远不会偏离主线。

#### 2. “切香肠”策略：分解任务 (Step-by-Step)
这是最重要的法则。**绝对不要让 Claude Code “一次性帮我把这个 App 做出来”。**
*   把它当成你的初级/中级开发同事。每次只分配**一个逻辑闭环**的任务。
*   例如：
    *   第一轮：初始化项目，配置 ESLint, Tailwind, 和路由骨架。
    *   第二轮：开发通用的 UI 组件（Button, Input, Navbar）。
    *   第三轮：实现数据库 Schema 和 API 接口。
    *   第四轮：将前端页面与 API 对接。

#### 3. 善用 Claude Code 的“Agentic (代理)”能力
因为它在你的终端里，它可以做很多网页端做不到的事：
*   **让它自己运行命令：** “Please write the unit tests for the Auth module, and run `npm run test` to make sure they pass. Fix any errors you find.”（让它写测试 -> 运行测试 -> 自己修 Bug，全自动）
*   **让它自己找上下文：** 如果接手老项目，直接说：“我想在支付流程中加一个优惠券功能，但我不知道现在的支付逻辑在哪里。请搜索代码库并告诉我你打算怎么修改。”（它会自己使用 `grep` 或 `glob` 工具去找文件）

#### 4. 管理 Context Window（上下文窗口）
这是高阶技巧。长时间对话会导致 Context 变得极其庞大，既贵又容易让 Claude 产生幻觉（忘记前面的设定）。
*   **使用 `/compact` 命令：** 当一个功能开发完毕（比如登录模块做好了），在终端输入 `/compact`。这会让 Claude 总结之前的对话并开启新的上下文，同时保留核心记忆。
*   **使用 `/clear` 命令：** 当你开始一个完全独立的新任务时，清理历史记录。

---

### 三、 经典的 Prompt 模板推荐

**1. 启动新功能的 Prompt：**
> "I want to add a [Feature Name] to this app.
> **User Requirement:** Users should be able to [What the user does].
> **Tech constraints:** Use [Tech stack/Library]. Make sure it looks consistent with our existing UI components in `src/components`.
> **Action:** Please review the current codebase to understand how we handle similar features, then propose an implementation plan. Wait for my approval before modifying files."

**2. 遇到 Bug 时的 Prompt：**
> "When I run `npm run dev` and click the Submit button on the /login page, the terminal throws this error: [Paste error]. The browser console says [Paste console error].
> Please use your tools to check the relevant files, identify the root cause, and fix it. You can run `npm run lint` or `npm run type-check` to verify your fix."

**3. 代码重构的 Prompt：**
> "The component `src/components/Dashboard.tsx` is getting too large and complex.
> Please refactor it. Extract the business logic into a custom hook, and break the UI down into smaller sub-components. Maintain all existing functionality."

---

### 四、 避坑指南 (What NOT to do)

1.  **不要过早优化：** 让它先跑通核心逻辑（MVP），再去让它“优化性能”或“增加漂亮的动画”。
2.  **不要和它争夺键盘：** 当 Claude Code 在修改文件时，不要同时在你的 IDE 里修改同一个文件，会导致冲突。
3.  **不要盲目同意危险操作：** Claude Code 执行 `npm install`、`git commit` 甚至 `rm` 命令前通常会询问你（取决于权限设置）。一定要看一眼它打算跑什么命令。
4.  **避免模棱两可的词：** 比如“把这个页面变好看一点”，不如说“按照 Vercel 的设计风格重构这个页面，使用更多的留白（padding）、更淡的边框，并加上适当的 hover 动画”。

**总结来说：**
把你对 App 的愿景（User Needs）和技术红线（Constraints）清晰地交给 Claude Code，然后像带徒弟一样，**一步一步（Step-by-step）** 派发任务。遇到报错让它**自己去探测（Investigate）和解决**，适时使用 `/compact` 保持它的“头脑清醒”。这样你就能极快地构建出高质量的 App。

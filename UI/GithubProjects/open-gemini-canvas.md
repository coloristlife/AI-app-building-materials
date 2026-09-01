
https://github.com/CopilotKit/open-gemini-canvas
This project showcases how to build practical AI agents with **CopilotKit**, **Google DeepMind’s Gemini**, and **LangGraph**.  
It includes two agents, exposed through a **Next.js frontend** and a **FastAPI backend**.

### ✨ Features

[](https://github.com/CopilotKit/open-gemini-canvas#-features)

- **Post Generator Agent**  
    Generate LinkedIn and Twitter posts from the context you provide.  
    Useful for creating professional, context-aware social content.
    
- **Stack Analyzer Agent**  
    Provide a URL and get a detailed breakdown of the site’s technology stack.  
    Quickly identify frameworks, libraries, and infrastructure used.

### Tech Stack

- **Frontend**: Next.js
- **Backend**: FastAPI
- **Agents**: Google Gemini + LangGraph
- **UI Layer**: CopilotKit


## package file
这个 `package.json` 文件是一个标准的全栈 AI Web 项目依赖配置（主要使用了 Next.js + React 19 + Tailwind CSS + shadcn/ui 组件库 + CopilotKit AI Agent 框架）。

以下是包含的所有依赖包（库）及其具体功能的分类整理：

---

### 一、 核心框架与语言基础 (Core Framework & Language)

1. **`next`**: Next.js 框架，提供服务端渲染 (SSR)、静态生成 (SSG)、App Router 路由系统及全栈 Web 开发支持。
2. **`react`**: React 核心视图层库。
3. **`react-dom`**: React 用于 DOM 渲染的绑定库。
4. **`typescript`**: TypeScript 编译器与静态类型检查语言工具。
5. **`@types/node`**: Node.js API 的 TypeScript 类型声明。
6. **`@types/react`**: React 的 TypeScript 类型声明。
7. **`@types/react-dom`**: React DOM 的 TypeScript 类型声明。

---

### 二、 AI 与 AI Agent 框架 (AI & Copilot SDKs)

1. **`ai`**: Vercel AI SDK 核心库，用于处理 LLM 流式响应（Streaming）、Prompt 构造及模型调用。
2. **`@ai-sdk/openai`**: Vercel AI SDK 的 OpenAI 接口适配层。
3. **`@ai-sdk/react`**: Vercel AI SDK 提供的 React 专用 Hooks（如 `useChat`、`useCompletion` 等）。
4. **`copilotkit`**: CopilotKit 框架主包，用于在应用中构建嵌入式 AI 助手/Copilot。
5. **`@copilotkit/react-core`**: CopilotKit 的 React 核心状态管理与上下文 Hook 接口。
6. **`@copilotkit/react-ui`**: CopilotKit 提供的预制 AI 聊天界面、对话框及交互组件。
7. **`@copilotkit/runtime`**: CopilotKit 后端/运行时引擎，处理 Agent 状态与后端通信。
8. **`@copilotkit/runtime-client-gql`**: CopilotKit 运行时的 GraphQL 客户端通信 SDK。

---

### 三、 Radix UI 无样式 UI 基础件 (Radix UI Primitives)
*(无样式的可访问性 UI 基础件，通常为 shadcn/ui 底层依赖)*

1. **`@radix-ui/react-accordion`**: 手风琴折叠面板。
2. **`@radix-ui/react-alert-dialog`**: 警告/二次确认模态弹窗。
3. **`@radix-ui/react-aspect-ratio`**: 固定比例容器（如 16:9 比例锁定）。
4. **`@radix-ui/react-avatar`**: 用户头像及图片加载失败回退组件。
5. **`@radix-ui/react-checkbox`**: 复选框。
6. **`@radix-ui/react-collapsible`**: 可收起/展开的内容容器。
7. **`@radix-ui/react-context-menu`**: 右键上下文菜单。
8. **`@radix-ui/react-dialog`**: 标准模态对话框/弹窗。
9. **`@radix-ui/react-dropdown-menu`**: 下拉菜单。
10. **`@radix-ui/react-hover-card`**: 鼠标悬停预览卡片。
11. **`@radix-ui/react-label`**: 表单表头 label 关联组件。
12. **`@radix-ui/react-menubar`**: 顶部操作菜单栏。
13. **`@radix-ui/react-navigation-menu`**: 网站主导航菜单。
14. **`@radix-ui/react-popover`**: 浮层气泡框。
15. **`@radix-ui/react-progress`**: 进度条组件。
16. **`@radix-ui/react-radio-group`**: 单选框按钮组。
17. **`@radix-ui/react-scroll-area`**: 自定义滚动的区域容器。
18. **`@radix-ui/react-select`**: 下拉选择器。
19. **`@radix-ui/react-separator`**: 视觉分隔线。
20. **`@radix-ui/react-slider`**: 滑块输入控件。
21. **`@radix-ui/react-slot`**: 将属性穿透合并到直接子元素的抽象工具。
22. **`@radix-ui/react-switch`**: 开关 Toggle 开关。
23. **`@radix-ui/react-tabs`**: 选项卡切换组件。
24. **`@radix-ui/react-toast`**: Toast 原生通知弹窗底层。
25. **`@radix-ui/react-toggle`**: 状态切换按钮。
26. **`@radix-ui/react-toggle-group`**: 开关按钮组。
27. **`@radix-ui/react-tooltip`**: 鼠标悬停文字提示框。

---

### 四、 扩展 UI 与交互组件库 (Extended UI & Visualization)

1. **`lucide-react`**: 高质量 Icon 图标库。
2. **`recharts`**: 基于 React 的响应式数据图表库（折线图、柱状图、饼图等）。
3. **`cmdk`**: 命令面板组件（类似于 macOS 上的 Spotlight 或 `Cmd+K` 搜索弹窗）。
4. **`embla-carousel-react`**: 响应式走马灯/轮播图组件。
5. **`vaul`**: 移动端友好的抽屉组件（Bottom Sheet Drawer）。
6. **`input-otp`**: 用于输入手机/邮箱验证码（OTP）的分格输入框组件。
7. **`react-day-picker`**: 日历与日期选择组件。
8. **`react-resizable-panels`**: 可拉伸/调整大小的分屏面板布局组件。
9. **`sonner`**: 现代、美观且开箱即用的 Toast 消息提示库。

---

### 五、 样式与主题管理 (Styling & CSS Tooling)

1. **`tailwindcss`**: 原子化 CSS 样式框架。
2. **`@tailwindcss/postcss`**: Tailwind CSS v4 的 PostCSS 插件整合包。
3. **`postcss`**: 用于转换 CSS 代码的 JavaScript 工具引擎。
4. **`autoprefixer`**: 根据 Can I Use 自动增加 CSS 浏览器兼容前缀的 PostCSS 插件。
5. **`next-themes`**: Next.js 极简无闪烁深色/浅色主题切换工具。
6. **`clsx`**: 条件化组合 `className` 类名的轻量工具。
7. **`tailwind-merge`**: 智能合并 Tailwind 类名并自动解决冲突（例如消除重复的 `padding` 设置）。
8. **`class-variance-authority` (CVA)**: 轻松为组件构建基于变体（Variants）的样式映射工具。
9. **`tailwindcss-animate`**: Tailwind CSS 预设动画扩展插件。
10. **`tw-animate-css`**: 基于 CSS animation 的 Tailwind 简易动画效果扩展。
11. **`geist`**: Vercel 官方设计的精美字体库（包含 Geist Sans 和 Geist Mono）。

---

### 六、 表单与数据校验 (Form & Data Validation)

1. **`react-hook-form`**: 高性能、零重渲染开销的 React 表单状态管理库。
2. **`zod`**: TypeScript 优先的数据 Schema 建模与运行时类型校验库。
3. **`@hookform/resolvers`**: 将 Zod 校验规则桥接到 React Hook Form 的适配器。

---

### 七、 工具与构建脚本 (Utilities & Workflow)

1. **`date-fns`**: 轻量且功能强大的 JavaScript 日期处理与格式化工具库。
2. **`concurrently`**: 在终端中并行执行多条命令行脚本工具（在此项目中用于同时启动前端 Next.js 服务与 `agent` 目录下的 Python 后端程序）。
## open-gemini-canvas
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


## Open Generative UI
https://github.com/CopilotKit/OpenGenerativeUI
https://opengenerativeui.copilotkit.ai/

An open-source showcase for building rich, interactive AI-generated UI with [CopilotKit](https://copilotkit.ai/) and [LangChain Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview). Ask the agent to visualize algorithms, create 3D animations, render charts, or generate interactive diagrams — all rendered as live HTML/SVG inside a sandboxed iframe.

### Key CopilotKit Patterns


|Pattern|Hook / Option|Example|
|---|---|---|
|Open Generative UI|`openGenerativeUI` + `renderActivityMessages`|Streaming sandboxed widgets via `generateSandboxedUi`|
|Generative UI|`useComponent`|Pie charts, bar charts|
|Frontend tools|`useFrontendTool`|Theme toggle|
|Human-in-the-loop|`useHumanInTheLoop`|Meeting scheduler|
|Default tool render|`useDefaultRenderTool`|Tool execution status|
## Tech Stack

[](https://github.com/CopilotKit/OpenGenerativeUI?utm_source=chatgpt.com#tech-stack)

Next.js 16, React 19, Tailwind CSS 4, LangChain Deep Agents, LangGraph, CopilotKit v2, Turborepo, Recharts

## Open AG UI Demo
https://github.com/TheGreatBonnie/open-ag-ui-langgraph?utm_source=chatgpt.com
https://www.youtube.com/watch?v=8Kjx0TOqF-c&t=1s
A full-stack AI-powered stock analysis and portfolio management application that demonstrates the integration of CopilotKit with LangGraph for intelligent financial analysis. The project features a Next.js frontend with an interactive chat interface and a FastAPI backend powered by Google's Gemini AI for real-time stock analysis and investment recommendations.

## 🚀 Features

[](https://github.com/TheGreatBonnie/open-ag-ui-langgraph?utm_source=chatgpt.com#-features)

- **🤖 AI-Powered Stock Analysis**: Intelligent stock analysis using Google Gemini AI
- **📊 Interactive Charts**: Real-time portfolio performance visualization with Recharts
- **💬 Chat Interface**: Natural language conversation with AI investment advisor
- **📈 Portfolio Management**: Track investments, allocations, and performance metrics
- **🎯 Investment Insights**: Bull and bear market insights for informed decision-making
- **🔄 Real-time Updates**: Live portfolio tracking and state management
- **📱 Responsive Design**: Modern UI built with Next.js 15 and Tailwind CSS
- **🔧 Tool Integration**: Yahoo Finance API integration for real-time stock data
- **🌐 AG-UI Protocol**: Event-driven communication between frontend and LangGraph agent
- **📡 Real-time Streaming**: Server-sent events for live agent interactions

## 🛠 Tech Stack

[](https://github.com/TheGreatBonnie/open-ag-ui-langgraph?utm_source=chatgpt.com#-tech-stack)

### Frontend

[](https://github.com/TheGreatBonnie/open-ag-ui-langgraph?utm_source=chatgpt.com#frontend)

- **Framework**: Next.js 15 with React 19
- **Styling**: Tailwind CSS 4
- **Charts**: Recharts for data visualization
- **AI Integration**: CopilotKit React components
- **Icons**: Lucide React
- **Language**: TypeScript

### Backend

[](https://github.com/TheGreatBonnie/open-ag-ui-langgraph?utm_source=chatgpt.com#backend)

- **Framework**: FastAPI with Python 3.12
- **AI Engine**: LangChain with Google Gemini
- **Workflow**: LangGraph for agent orchestration
- **AG-UI Protocol**: Event-driven agent communication framework
- **Data**: Yahoo Finance (yfinance) for stock data
- **Search**: Tavily for web research
- **Data Processing**: Pandas for financial analysis
- **Environment**: Poetry for dependency management
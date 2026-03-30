- https://github.com/NirDiamant/prompt_engineering

This repository offers a comprehensive collection of tutorials and implementations for Prompt Engineering techniques, ranging from fundamental concepts to advanced strategies. It serves as an essential resource for mastering the art of effectively communicating with and leveraging large language models in AI applications





# Fabric
虽然 Fabric 不是一个带图形界面的“专属审查平台”，但它是目前全球安全圈最火的开源 AI 安全工作流框架。由知名安全专家 Daniel Miessler 开源。

如何用于架构审查：Fabric 内置了大量经过安全专家精心调优的 AI Prompts（在项目中称为 Patterns）。你可以直接在命令行中输入架构文档或代码，调用它的专属 Pattern：
create_threat_model：自动生成高水平的威胁模型。
analyze_tech_stack：分析技术栈的安全隐患。
review_architecture：进行深度的安全架构审查。

Fabric 的核心就是一套高质量的 System Prompts（系统提示词），但在项目中它们被称为 "Patterns"（模式）

https://github.com/danielmiessler/fabric/tree/main/patterns
安全相关的 Prompt 示例：
针对你关心的安全架构审查，你可以直接查看以下 Pattern 的 system.md 内容：
create_threat_model：让 AI 扮演安全专家，进行 STRIDE 威胁建模。
analyze_tech_stack：分析技术栈组件的安全风险。
analyze_logs：安全日志分析。[2]
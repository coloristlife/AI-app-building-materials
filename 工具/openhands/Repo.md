https://github.com/OpenHands/openhands

OpenHands 是"写代码"专用做到极致、顺带能通过MCP扩展做点别的的框架，不是一个真正意义上的通用agent平台.

**OpenHands 的核心设计初衷和优势场景确实是写代码**——它前身是OpenDevin，定位就是"自主软件工程师"：开PR、修bug、跑测试、代码迁移。它的benchmark主打指标也是SWE-bench Verified（真实GitHub issue解决率），配合Claude系列能到53%+，这是它被验证得最扎实的能力。

但从架构上说，它不是"只能写代码"，而是"为写代码这个场景做了深度优化"，具体表现在：

### 它偏"写代码"的地方

- **沙箱执行**（Docker/Remote Workspace）本质是为了安全地跑代码、跑测试
- **风险评估机制**主要针对"这条shell命令/文件修改安全吗"这类判断
- **官方工具集**（bash执行、文件编辑、VSCode集成）都是开发工具
- 它的CLI、GitHub App集成、Large Codebase SDK（理解大型代码库依赖关系）都是软件工程专用能力

### 它也能做非编程任务，但要靠你自己拼

- 因为底层是**通用的Agent-Tool-LLM框架**，Tool System支持MCP，所以理论上你可以接任何MCP工具（金融数据、写作辅助工具等），让它做代码之外的分析、研究类任务
- 但这需要你自己配置，官方生态和文档基本没有为非编程场景做过优化或背书
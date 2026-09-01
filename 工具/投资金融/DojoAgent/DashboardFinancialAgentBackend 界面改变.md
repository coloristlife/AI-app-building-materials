不只是聊天窗口里的文字——这是通过 `DashboardFinancialAgentBackend` 暴露给 LLM 的一批"写操作"财务工具实现的。

## 1. 哪些工具会真正改写 dashboard 的数据

在 [financial_portfolio_tools.py](https://claude.ai/epitaxy/dojoagents/dashboard/integrations/financial_portfolio_tools.py) 里，除了只读的市场数据工具外，明确存在一批带副作用的写操作，比如（对应 `resource_changes` 标记）：

|动作|代码位置|
|---|---|
|创建组合 (create portfolio)|[financial_portfolio_tools.py:150](https://claude.ai/epitaxy/dojoagents/dashboard/integrations/financial_portfolio_tools.py:150)|
|重命名组合 (rename)|[:165](https://claude.ai/epitaxy/dojoagents/dashboard/integrations/financial_portfolio_tools.py:165)|
|删除组合 (delete)|[:178](https://claude.ai/epitaxy/dojoagents/dashboard/integrations/financial_portfolio_tools.py:178)|
|添加候选股 (add_candidate)|[:199](https://claude.ai/epitaxy/dojoagents/dashboard/integrations/financial_portfolio_tools.py:199) / [:255](https://claude.ai/epitaxy/dojoagents/dashboard/integrations/financial_portfolio_tools.py:255)|
|创建交易/建仓 (create_order)|[:287](https://claude.ai/epitaxy/dojoagents/dashboard/integrations/financial_portfolio_tools.py:287) / [:388](https://claude.ai/epitaxy/dojoagents/dashboard/integrations/financial_portfolio_tools.py:388)|
|同步外部持仓 (sync_positions)|[:448](https://claude.ai/epitaxy/dojoagents/dashboard/integrations/financial_portfolio_tools.py:448)|
|移除持仓 (remove_holding)|[:463](https://claude.ai/epitaxy/dojoagents/dashboard/integrations/financial_portfolio_tools.py:463)|

这些工具在被 LLM 调用后，会通过 `registry.portfolio_service`（[financial_portfolio_tools.py:53-57](https://claude.ai/epitaxy/dojoagents/dashboard/integrations/financial_portfolio_tools.py:53)）真正落到 dashboard 后端的持久化存储上——也就是同一个 `app_services.registry`，跟你用鼠标点 dashboard 界面上"新建组合""下单"按钮时走的**是同一套后端服务**。

## 2. 改动如何反映到界面

每次写操作返回时都会带上 `resource_changes` 字段，例如：

```python
resource_changes=[{"resource": "portfolio", "action": "create", "portfolio_id": ...}]
```

这个字段一路透传：`ToolResult.resource_changes`（[models.py:70](https://claude.ai/epitaxy/dojoagents/agent/models.py:70)）→ `loop.py:160`/`1449` → 最终随聊天响应回到前端。前端 [agentFolioSync.ts](https://claude.ai/epitaxy/dojoagents/dashboard/web/src/utils/agentFolioSync.ts) 会读取这个字段，**据此触发相应组合视图的刷新**——所以用户跟 LLM 说"帮我建一个新组合，买入 500 股 AAPL"，如果 LLM 调用了对应的写工具，dashboard 的组合列表/持仓页面会自动刷新出这次变化，不需要用户手动刷新页面。

## 3. 边界在哪里

- LLM 能造成的改变，**严格限定在已注册进 `ToolRegistry` 的那些工具能做的事**——即 `DashboardFinancialAgentBackend.supported_tools` 里列出的名字。它不能跳出这个范围去改 dashboard 的其他任意状态（比如系统设置、用户权限、代码本身）。
- 每次写操作都要求 `principal`（已认证用户）和 `session_id`（[financial_agent_backend.py:59-62](https://claude.ai/epitaxy/dojoagents/dashboard/integrations/financial_agent_backend.py:59)），不是匿名可执行的。
- 只读类工具（市场行情、板块、财务数据查询）不会产生 `resource_changes`，只是把信息读出来给 LLM 看，不改 dashboard 状态。
- 代码执行工具、session 文件读写工具，作用范围是服务器端沙箱/会话文件系统，跟"改 dashboard 业务数据"是两件事，除非配合可视化技能（如 `canvas-chart`）生成图表 artifact 展示在对话里。

**一句话：能改，但只能通过被明确注册为"写操作"的财务组合工具（建组合/下单/同步持仓/删除等），改动会经同一套后端服务持久化，并通过 `resource_changes` 通知前端刷新对应界面；LLM 无法越过这批工具去改动 dashboard 之外的任意状态。**
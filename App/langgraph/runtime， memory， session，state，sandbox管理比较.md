---
内容生成: AI
---


直接说结论:**这五个维度不是一个"谁更好"的问题,而是天然分工不同的两层**——LangGraph 在"跨轮次、跨 agent 的状态编排"上更强,Goose/DojoAgent 这类 Agent Runtime 在"单次任务的执行沙箱"上更强。硬要放在同一层竞争,两边都会做得别扭。

## 逐维度对比

|维度|LangGraph|Goose/DojoAgent(Agent Runtime)|
|---|---|---|
|**Runtime**(执行模型)|图/状态机执行,适合"多步骤+条件分支+人工确认"的编排,但**不提供代码执行沙箱**|专门为"执行动作"设计——跑代码、调 shell、操作文件系统,有真正的隔离执行环境|
|**Memory**(长期记忆)|`checkpointer`(Postgres/Redis/SQLite)原生支持跨 session 持久化、可回放、可分支(time-travel)|通常只有"当前任务上下文",没有跨 session 的长期记忆抽象,重启就丢|
|**Session**|`thread_id` 是一等公民,天然支持多用户、多会话隔离|大多是"一次运行=一个进程/一个上下文",session 概念弱或需要自己拼|
|**State**|强类型 State schema + reducer,状态变更可追踪、可持久化、可在节点间显式传递|内部状态往往是隐式的(黑盒内部维护),对外只暴露输入输出,不暴露中间状态|
|**Sandbox 管理**|**没有**原生沙箱能力,顶多调用外部沙箱服务|这是它们的强项——Goose 有 workspace/权限隔离,DojoAgent 通常跑在专用仿真容器里,资源限制、超时、隔离都是内建的|

## 结论

- **记忆、session、state** → 应该完全交给 LangGraph 的 checkpointer,不要让 Goose/DojoAgent 自己维护这些(否则出现"双重记忆源",数据不一致时很难排查是哪边过期了)。
- **runtime 执行、sandbox** → 应该完全交给 Goose/DojoAgent,LangGraph 不要自己去起容器/管进程生命周期,它只需要知道"沙箱句柄"存在,不需要知道沙箱内部怎么隔离。

所以集成方式的关键,是在 LangGraph 的 State 里加一个**沙箱句柄字段**,让 LangGraph 能"记住"某个 session 对应哪个正在运行的沙箱,而不用每次都新建。




## 集成示例:沙箱生命周期跟 LangGraph session 绑定

### 1. State 里加沙箱句柄

```python
class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    thread_id: str
    goose_sandbox_id: str | None      # Goose workspace/session 的句柄,由 Goose 侧生成
    dojo_sandbox_id: str | None       # DojoAgent 仿真环境句柄
    tool_result: dict | None
```

因为这个 state 会被 checkpointer 持久化,所以**沙箱句柄本身会随 session 一起被 LangGraph 记住**——下次同一个 `thread_id` 进来,可以直接复用沙箱,而不用重新创建。

### 2. MCP 工具里加"沙箱生命周期"三个动作(创建/复用/销毁)

```python
# goose_mcp_server.py
from mcp.server.fastmcp import FastMCP
import subprocess, json

mcp = FastMCP("goose-tools")

@mcp.tool()
def goose_create_sandbox(user_id: str) -> dict:
    """创建一个新的 Goose 隔离 workspace,返回 sandbox_id。"""
    result = subprocess.run(
        ["goose", "sandbox", "create", "--user", user_id, "--output-format", "json"],
        capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)  # {"sandbox_id": "gs-xxxx"}

@mcp.tool()
def goose_run_in_sandbox(sandbox_id: str, instruction: str) -> dict:
    """在已存在的 sandbox 里执行任务,不新建环境。"""
    result = subprocess.run(
        ["goose", "run", "--sandbox", sandbox_id, "--text", instruction, "--output-format", "json"],
        capture_output=True, text=True, timeout=120, check=True,
    )
    return json.loads(result.stdout)

@mcp.tool()
def goose_destroy_sandbox(sandbox_id: str) -> dict:
    """任务结束/session 超时后回收资源。"""
    subprocess.run(["goose", "sandbox", "destroy", sandbox_id], check=True)
    return {"status": "destroyed"}
```

### 3. LangGraph 节点:按需创建、复用、清理

```python
async def ensure_goose_sandbox(state: GraphState) -> GraphState:
    if state.get("goose_sandbox_id") is None:
        result = await mcp_client.call_tool("goose", "goose_create_sandbox",
                                             {"user_id": state["user_id"]})
        state["goose_sandbox_id"] = result["sandbox_id"]
        # 这个字段进 checkpointer,下一轮同 thread_id 直接复用,不再创建
    return state

async def call_goose_node(state: GraphState) -> GraphState:
    result = await mcp_client.call_tool("goose", "goose_run_in_sandbox", {
        "sandbox_id": state["goose_sandbox_id"],
        "instruction": state["messages"][-1].content,
    })
    state["tool_result"] = result
    state["messages"].append({"role": "assistant", "content": result.get("summary", "")})
    return state

graph.add_node("ensure_sandbox", ensure_goose_sandbox)
graph.add_node("goose", call_goose_node)
graph.add_edge("ensure_sandbox", "goose")
```

### 4. 沙箱回收:用 LangGraph 之外的 TTL 机制,而不是让 Goose 自己猜

```python
# 独立的清理任务(cron / 定时 worker),扫 checkpointer 里久未活跃的 thread
async def reap_idle_sandboxes():
    for thread in checkpointer.list_idle_threads(idle_minutes=30):
        state = checkpointer.get(thread)
        if state.get("goose_sandbox_id"):
            await mcp_client.call_tool("goose", "goose_destroy_sandbox",
                                        {"sandbox_id": state["goose_sandbox_id"]})
```

这一步很重要:**沙箱什么时候销毁,应该由 LangGraph(知道 session 活跃度)决定,而不是 Goose 自己内部超时**——否则会出现"LangGraph 还以为沙箱存在、实际已经被 Goose 自己回收"的状态不一致问题。

## 一句话总结分工

> LangGraph 负责"记住有一个沙箱、它属于谁、什么时候该收回它";Goose/DojoAgent 负责"沙箱里具体发生了什么",这条线不能反过来,否则两边都会各自维护一份互相不同步的状态。



要不要我把这个"沙箱句柄 + 空闲回收"的模式,扩展成一个可以同时管理 Goose 和 DojoAgent 两种沙箱的统一 `SandboxManager` 抽象层,这样以后再接入第三个 runtime 也不用改 LangGraph 主图?
给你一个统一的 `SandboxManager` 抽象层设计,核心思路:**LangGraph 侧永远只跟 `SandboxManager` 打交道,不直接认识 Goose 或 DojoAgent**——新增第三个 runtime 只需要写一个新的 Provider 类,主图代码零改动。

## 1. 定义统一接口(Provider 协议)

```python
# sandbox/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SandboxHandle:
    provider: str          # "goose" / "dojo" / 未来的第三方
    sandbox_id: str
    created_at: datetime
    last_used_at: datetime

class SandboxProvider(ABC):
    name: str  # 子类必须定义,如 "goose"

    @abstractmethod
    async def create(self, user_id: str) -> str:
        """创建沙箱,返回 provider 内部的 sandbox_id"""

    @abstractmethod
    async def run(self, sandbox_id: str, instruction: str, **kwargs) -> dict:
        """在已有沙箱里执行任务"""

    @abstractmethod
    async def destroy(self, sandbox_id: str) -> None:
        """销毁沙箱、回收资源"""

    @abstractmethod
    async def health_check(self, sandbox_id: str) -> bool:
        """沙箱是否还存活(可能被 provider 自己超时回收了)"""
```

## 2. 两个具体 Provider(都只是薄薄一层 MCP 调用)

```python
# sandbox/goose_provider.py
from .base import SandboxProvider

class GooseSandboxProvider(SandboxProvider):
    name = "goose"

    def __init__(self, mcp_client):
        self.mcp = mcp_client

    async def create(self, user_id: str) -> str:
        result = await self.mcp.call_tool("goose", "goose_create_sandbox", {"user_id": user_id})
        return result["sandbox_id"]

    async def run(self, sandbox_id: str, instruction: str, **kwargs) -> dict:
        return await self.mcp.call_tool("goose", "goose_run_in_sandbox", {
            "sandbox_id": sandbox_id, "instruction": instruction,
        })

    async def destroy(self, sandbox_id: str) -> None:
        await self.mcp.call_tool("goose", "goose_destroy_sandbox", {"sandbox_id": sandbox_id})

    async def health_check(self, sandbox_id: str) -> bool:
        try:
            result = await self.mcp.call_tool("goose", "goose_ping_sandbox", {"sandbox_id": sandbox_id})
            return result.get("alive", False)
        except Exception:
            return False
```

```python
# sandbox/dojo_provider.py
from .base import SandboxProvider

class DojoAgentSandboxProvider(SandboxProvider):
    name = "dojo"

    def __init__(self, mcp_client):
        self.mcp = mcp_client

    async def create(self, user_id: str) -> str:
        result = await self.mcp.call_tool("dojo", "dojo_create_env", {"user_id": user_id})
        return result["env_id"]

    async def run(self, sandbox_id: str, instruction: str, **kwargs) -> dict:
        return await self.mcp.call_tool("dojo", "dojo_execute", {
            "env_id": sandbox_id, "task": instruction, **kwargs,
        })

    async def destroy(self, sandbox_id: str) -> None:
        await self.mcp.call_tool("dojo", "dojo_teardown_env", {"env_id": sandbox_id})

    async def health_check(self, sandbox_id: str) -> bool:
        result = await self.mcp.call_tool("dojo", "dojo_env_status", {"env_id": sandbox_id})
        return result.get("status") == "running"
```

注意两个 Provider 的字段名(`sandbox_id` vs `env_id`)、返回结构完全不同——这正是 Provider 层要吸收掉的差异,`SandboxManager` 之上看到的永远是统一的 `SandboxHandle`。

## 3. SandboxManager:注册表 + 生命周期策略

```python
# sandbox/manager.py
from datetime import datetime, timedelta
from .base import SandboxProvider, SandboxHandle

class SandboxManager:
    def __init__(self, idle_ttl_minutes: int = 30):
        self._providers: dict[str, SandboxProvider] = {}
        self._idle_ttl = timedelta(minutes=idle_ttl_minutes)

    def register(self, provider: SandboxProvider) -> None:
        self._providers[provider.name] = provider

    async def ensure(self, provider_name: str, user_id: str,
                      existing: SandboxHandle | None) -> SandboxHandle:
        provider = self._providers[provider_name]

        if existing and await provider.health_check(existing.sandbox_id):
            existing.last_used_at = datetime.utcnow()
            return existing

        sandbox_id = await provider.create(user_id)
        return SandboxHandle(provider=provider_name, sandbox_id=sandbox_id,
                              created_at=datetime.utcnow(), last_used_at=datetime.utcnow())

    async def run(self, handle: SandboxHandle, instruction: str, **kwargs) -> dict:
        provider = self._providers[handle.provider]
        handle.last_used_at = datetime.utcnow()
        return await provider.run(handle.sandbox_id, instruction, **kwargs)

    async def reap_idle(self, handles: dict[str, SandboxHandle]) -> list[str]:
        """扫描所有 handle,销毁空闲超时的,返回被销毁的 key 列表"""
        reaped = []
        now = datetime.utcnow()
        for key, handle in list(handles.items()):
            if now - handle.last_used_at > self._idle_ttl:
                provider = self._providers[handle.provider]
                await provider.destroy(handle.sandbox_id)
                reaped.append(key)
        return reaped
```

`ensure()` 里做了健康检查——即使 Goose/DojoAgent 自己内部有超时回收沙箱的逻辑,LangGraph 这边也不会因为"以为沙箱还活着"而调用失败,发现死了就自动重建。这解决了之前提到的"双方状态不同步"问题。

## 4. State 改成统一存 handle,不再分字段

```python
class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    thread_id: str
    sandboxes: dict[str, SandboxHandle]   # key 是 provider name: {"goose": handle, "dojo": handle}
    tool_result: dict | None
```

## 5. 通用节点工厂——新增第三个 runtime 时,主图不用改

```python
def make_sandbox_node(provider_name: str, sandbox_manager: SandboxManager):
    async def node(state: GraphState) -> GraphState:
        existing = state["sandboxes"].get(provider_name)
        handle = await sandbox_manager.ensure(provider_name, state["user_id"], existing)
        state["sandboxes"][provider_name] = handle

        result = await sandbox_manager.run(handle, state["messages"][-1].content)
        state["tool_result"] = result
        state["messages"].append({"role": "assistant", "content": result.get("summary") or result.get("result", "")})
        return state
    return node

sandbox_manager = SandboxManager(idle_ttl_minutes=30)
sandbox_manager.register(GooseSandboxProvider(mcp_client))
sandbox_manager.register(DojoAgentSandboxProvider(mcp_client))

graph.add_node("goose", make_sandbox_node("goose", sandbox_manager))
graph.add_node("dojo", make_sandbox_node("dojo", sandbox_manager))
# 未来接入第三方 runtime,只需要:
# sandbox_manager.register(NewRuntimeProvider(mcp_client))
# graph.add_node("new_runtime", make_sandbox_node("new_runtime", sandbox_manager))
```

## 6. 空闲回收也变成通用逻辑

```python
async def reap_all_idle_sessions():
    for thread_id in checkpointer.list_active_threads():
        state = checkpointer.get(thread_id)
        reaped_keys = await sandbox_manager.reap_idle(state["sandboxes"])
        for key in reaped_keys:
            del state["sandboxes"][key]
        if reaped_keys:
            checkpointer.put(thread_id, state)
```

## 分工总结

- **`SandboxProvider`**:知道怎么跟具体 runtime(Goose/DojoAgent)说话,吸收字段差异。
- **`SandboxManager`**:统一生命周期策略(创建/健康检查/复用/回收),对上层屏蔽 provider 差异。
- **LangGraph 主图**:只知道"有一个叫 goose 的沙箱节点、一个叫 dojo 的沙箱节点",不知道也不需要知道它们内部怎么实现。
- **State + checkpointer**:唯一的事实来源,记录"这个 session 目前挂着哪些沙箱、什么时候最后用过"。

这样以后要接入第三个 agent runtime,改动范围严格限制在"写一个新 Provider 类 + 注册 + 加一个节点",不会牵扯到鉴权、记忆、路由这些已经稳定的部分。




# other
**1. 别把 `thread_id` 当成你的 session_id**

这个是对的,而且成本很低——即使你永远只用 LangGraph,自己铸造一个 `session_id` 再映射到 `thread_id`,也只是多一行代码,却让你保留了以后不被 LangGraph 锁死的余地:

session_id = platform.sessions.create(user_id=user_id).id
config = {"configurable": {"thread_id": f"lg-{session_id}"}}

**2. 用 LangGraph 官方的 `Store`,而不是自己在 node 里裸调 mem0**

我之前直接在节点里 `memory.search()` / `memory.add()`,是把"记忆后端选型"硬编码进了业务节点。更好的做法是包一层 `BaseStore` 接口,mem0 只是其中一种实现——这样以后想换成 LangGraph 官方 `Store` + pgvector,或者换掉 mem0,业务节点不用改:

from langgraph.store.base import BaseStore

class Mem0Store(BaseStore):
    def __init__(self, memory_client): self.memory = memory_client
    def get(self, namespace, key): ...
    def search(self, namespace, query, limit=5):
        return self.memory.search(query=query, user_id=namespace[-1], limit=limit)["results"]
    def put(self, namespace, key, value): self.memory.add(...)

app = graph.compile(checkpointer=checkpointer, store=Mem0Store(memory))

节点里改成 `store.search(...)`,不再直接 import mem0——这一步无论走哪条架构都值得做。

**3. 用 `context_schema` 传 session/user 信息,别塞进 State**

这个之前我确实做得不够干净——`user_id`、`sandboxes` 这类"平台层信息"混进了业务 `GraphState`,导致 State 同时承担"对话数据"和"平台元数据"两种职责。用 `context_schema` 分开:
```
from dataclasses import dataclass

@dataclass
class RuntimeContext:
    user_id: str
    session_id: str
    tenant_id: str

graph = StateGraph(GraphState, context_schema=RuntimeContext)

def call_goose_node(state: GraphState, runtime: Runtime[RuntimeContext]) -> GraphState:
    handle = sandbox_manager.ensure("goose", runtime.context.user_id, ...)
    ...
```


这样 `GraphState` 只放"这次对话真正需要的数据",平台元数据走 context——即使你不搭 Runtime 层,这也是更干净的 LangGraph 用法。



**完整的 Adapter 契约(`start/resume/invoke/stream/interrupt/cancel/close`)统一抽象 LangGraph 和 Goose**——这是在假设"LangGraph 的图执行模型"和"Goose 的 agent loop"和"DojoAgent 的仿真环境"能被同一套生命周期接口覆盖。实际上:

- LangGraph 的 `interrupt`/`resume` 是基于 checkpoint 的细粒度断点恢复
- Goose 的"session"更像是一个持续运行的 workspace,概念上不是"暂停再恢复到某一步"
- DojoAgent 的仿真环境可能根本没有"interrupt"这个概念

强行统一成一个 Adapter 接口,大概率会变成"最小公分母"接口——每个 adapter 里一半方法是空实现或者语义打折扣。**在你只有一个真正在用的 Framework(LangGraph)之前,这层抽象没有第二个实现来验证它是否设计对,写出来大概率是错的,以后还要重构。**
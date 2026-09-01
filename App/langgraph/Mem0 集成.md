可以,而且这正好补上 LangGraph checkpointer 天生缺的一块——**跨 thread 的语义化长期记忆**。

## 先分清楚两者不是替代关系

|LangGraph checkpointer|mem0|
|---|---|---|
|作用范围|单个 `thread_id` 内的完整状态快照,可回放/可分支|跨 `thread_id`、跨 session,按 `user_id` 聚合的"关于这个人的事实"|
|存的是什么|原始对话历史 + 你 State 里的所有字段(全量)|抽取/摘要后的语义记忆片段(精炼后的事实),支持向量检索|
|典型问题|"上一轮说了什么"|"这个用户三个月前提到过他不喜欢用 Docker"|
|生命周期|一个会话线程|用户本人,理论上永久|

所以正确的接法是:**checkpointer 继续管当前会话的完整状态,mem0 单独管跨会话的用户长期记忆**,两者在 LangGraph 图里是并列的两个能力,不冲突。

## 1. 安装 & 初始化

```python
pip install mem0ai
```

```python
from mem0 import Memory

# 可以用云端 mem0 平台,也可以自托管(向量库+图数据库都能换成自己的)
memory = Memory.from_config({
    "vector_store": {"provider": "qdrant", "config": {"host": "localhost", "port": 6333}},
    "llm": {"provider": "anthropic", "config": {"model": "claude-sonnet-5"}},
})
```

## 2. State 里不需要额外存 mem0 的数据——它自己按 user_id 管理

```python
class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    thread_id: str
    retrieved_memories: list[dict]   # 本轮检索出来、注入 prompt 用的记忆
    sandboxes: dict[str, SandboxHandle]
```

## 3. 检索节点:对话开始前,把相关长期记忆捞出来

```python
def retrieve_memory_node(state: GraphState) -> GraphState:
    query = state["messages"][-1].content
    results = memory.search(query=query, user_id=state["user_id"], limit=5)
    state["retrieved_memories"] = results["results"]
    return state
```

## 4. 注入到 LLM 的 system prompt

```python
def build_prompt_node(state: GraphState) -> GraphState:
    memory_text = "\n".join(f"- {m['memory']}" for m in state["retrieved_memories"])
    system_msg = f"以下是关于这个用户的已知长期信息:\n{memory_text}\n\n请结合这些信息回应用户。"
    state["messages"] = [{"role": "system", "content": system_msg}] + state["messages"]
    return state
```

## 5. 写回节点:对话结束后,让 mem0 自动抽取新记忆

```python
def save_memory_node(state: GraphState) -> GraphState:
    # mem0 自己会用 LLM 判断这段对话里哪些信息值得记、哪些是噪音,不需要你手写抽取逻辑
    memory.add(
        messages=[{"role": m["role"], "content": m["content"]} for m in state["messages"][-2:]],
        user_id=state["user_id"],
    )
    return state
```

## 6. 组装进图里

```python
graph.add_node("retrieve_memory", retrieve_memory_node)
graph.add_node("build_prompt", build_prompt_node)
graph.add_node("worker", worker_node)          # 之前的 goose/dojo/router 逻辑
graph.add_node("save_memory", save_memory_node)

graph.add_edge("auth", "retrieve_memory")
graph.add_edge("retrieve_memory", "build_prompt")
graph.add_edge("build_prompt", "worker")
graph.add_edge("worker", "save_memory")
graph.add_edge("save_memory", END)
```

## 结合之前的 SandboxManager/多角色路由怎么摆位置

```
auth → retrieve_memory(mem0,跨session长期记忆) → build_prompt → router
                                                                  ├─► goose(沙箱短时执行)
                                                                  └─► dojo(沙箱短时执行)
                                                                  └─► save_memory(mem0写回) → END
```

分层非常清晰:

- **checkpointer**:这一次会话完整发生了什么(可回放)
- **mem0**:关于这个人,长期该记住什么(跨会话可检索)
- **SandboxManager**:执行任务时临时挂着的沙箱(和记忆完全无关,任务结束就该回收)

## 一个容易踩的坑

不要把 mem0 的 `add()` 放在每个节点里都调一次——它内部会调 LLM 去判断"这段内容值不值得记",高频调用会产生不必要的 LLM 开销和记忆噪音。比较好的做法是像上面这样,**只在一轮对话/一个任务真正结束时调一次**,而不是每个 tool 调用后都调。

# mem0 的检索结果也接入 Goose/DojoAgent 那条线吗?
 比如把"用户长期偏好"作为额外 context 传给 `goose_run_in_sandbox`,让沙箱执行时也能感知用户历史习惯

一个完整的端到端例子:mem0 检索出的用户偏好,通过 `SandboxManager.run()` 的 `**kwargs` 一路传到 `goose_run_in_sandbox`,让 Goose 在沙箱里执行时能感知这些偏好。

## 1. 改造 Goose MCP Server:工具签名加一个 `user_preferences` 参数

```python
# goose_mcp_server.py
from mcp.server.fastmcp import FastMCP
import subprocess, json

mcp = FastMCP("goose-tools")

@mcp.tool()
def goose_create_sandbox(user_id: str) -> dict:
    result = subprocess.run(
        ["goose", "sandbox", "create", "--user", user_id, "--output-format", "json"],
        capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)

@mcp.tool()
def goose_run_in_sandbox(sandbox_id: str, instruction: str,
                          user_preferences: list[str] | None = None) -> dict:
    """在已有 sandbox 里执行任务。user_preferences 是从长期记忆里检索出的、
    与本次任务相关的用户偏好(比如'不用 Docker,直接用 venv'),会作为
    额外约束条件注入 Goose 的 system context,而不是拼进 instruction 正文里,
    避免和用户当下的真实指令混在一起。"""
    payload = {
        "instruction": instruction,
        "constraints": user_preferences or [],
    }
    result = subprocess.run(
        ["goose", "run", "--sandbox", sandbox_id,
         "--input", json.dumps(payload),
         "--output-format", "json"],
        capture_output=True, text=True, timeout=120, check=True,
    )
    return json.loads(result.stdout)

@mcp.tool()
def goose_destroy_sandbox(sandbox_id: str) -> dict:
    subprocess.run(["goose", "sandbox", "destroy", sandbox_id], check=True)
    return {"status": "destroyed"}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

关键设计:`user_preferences` 是独立字段,不是拼接到 `instruction` 字符串里——这样 Goose 内部可以把它当"约束/背景信息"而不是"用户这句话要求的事",防止偏好信息污染或覆盖用户当次真实意图。

## 2. Provider 层:把 `user_preferences` 透传下去

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

    async def run(self, sandbox_id: str, instruction: str,
                   user_preferences: list[str] | None = None, **kwargs) -> dict:
        return await self.mcp.call_tool("goose", "goose_run_in_sandbox", {
            "sandbox_id": sandbox_id,
            "instruction": instruction,
            "user_preferences": user_preferences or [],
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

`SandboxManager.run()` 之前已经用 `**kwargs` 转发(见上一轮代码),所以这一层不用改。

## 3. State 加一个字段,存"筛选后适合给 Goose 的偏好"

```python
class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str
    thread_id: str
    retrieved_memories: list[dict]      # mem0 原始检索结果
    goose_preferences: list[str]        # 从 retrieved_memories 里筛出、跟"执行环境"相关的部分
    sandboxes: dict[str, SandboxHandle]
    tool_result: dict | None
```

## 4. 筛选节点:不是所有长期记忆都该给 Goose

```python
def extract_goose_preferences_node(state: GraphState) -> GraphState:
    """从 mem0 检索结果里,只挑与代码执行/环境相关的偏好传给 Goose,
    避免把跟任务无关的私人信息(比如'用户喜欢喝咖啡')也塞进沙箱上下文。"""
    relevant_categories = {"tooling", "environment", "coding_style"}
    state["goose_preferences"] = [
        m["memory"] for m in state["retrieved_memories"]
        if m.get("metadata", {}).get("category") in relevant_categories
    ]
    return state
```

这里假设写入 mem0 时打了 `category` 标签,便于后续按用途过滤。如果你的 mem0 记录没有分类,也可以退化成直接把全部 `retrieved_memories` 传过去,先跑起来再迭代。

## 5. 调用 Goose 的节点:把偏好传进去

```python
async def call_goose_node(state: GraphState) -> GraphState:
    existing = state["sandboxes"].get("goose")
    handle = await sandbox_manager.ensure("goose", state["user_id"], existing)
    state["sandboxes"]["goose"] = handle

    result = await sandbox_manager.run(
        handle,
        instruction=state["messages"][-1].content,
        user_preferences=state["goose_preferences"],
    )
    state["tool_result"] = result
    state["messages"].append({"role": "assistant", "content": result.get("summary", "")})
    return state
```

## 6. 完整图组装

```python
graph = StateGraph(GraphState)
graph.add_node("auth", auth_node)
graph.add_node("retrieve_memory", retrieve_memory_node)          # mem0.search()
graph.add_node("extract_goose_prefs", extract_goose_preferences_node)
graph.add_node("router", router_node)
graph.add_node("goose", call_goose_node)
graph.add_node("dojo_agent", call_dojo_agent_node)
graph.add_node("save_memory", save_memory_node)                  # mem0.add()

graph.set_entry_point("auth")
graph.add_edge("auth", "retrieve_memory")
graph.add_edge("retrieve_memory", "extract_goose_prefs")
graph.add_edge("extract_goose_prefs", "router")
graph.add_conditional_edges("router", route_condition, {
    "goose": "goose",
    "dojo_agent": "dojo_agent",
})
graph.add_edge("goose", "save_memory")
graph.add_edge("dojo_agent", "save_memory")
graph.add_edge("save_memory", END)

app = graph.compile(checkpointer=checkpointer)
```

## 端到端跑一遍会发生什么

1. 用户第一次说"帮我写个爬虫脚本,别用 Docker,我这台机器装不了"
2. `save_memory_node` 把这句话喂给 mem0,mem0 自动抽取出 `{"memory": "不希望用 Docker,偏好直接用 venv", "metadata": {"category": "environment"}}`,存到 `user_id` 下
3. 一周后,新的 session(不同 `thread_id`,但同一个 `user_id`)用户说"再帮我写个数据清洗脚本"
4. `retrieve_memory_node` 用这句话去 mem0 检索,命中上次那条 Docker 偏好
5. `extract_goose_preferences_node` 筛出这条(category 匹配),放进 `goose_preferences`
6. `call_goose_node` 把 `["不希望用 Docker,偏好直接用 venv"]` 作为 `user_preferences` 传给 `goose_run_in_sandbox`
7. Goose 在沙箱里执行时,会带着"别用 Docker"这个约束去写脚本——即使用户这次完全没提这件事

这就是长期记忆真正发挥价值的地方:**执行细节的一致性不需要用户每次重复提要求**,而且这个链路完全没有绕开之前建立的边界——用户身份鉴权仍在 LangGraph,沙箱仍是 Goose 的黑盒,mem0 只负责在两者之间递一张"备忘条"。
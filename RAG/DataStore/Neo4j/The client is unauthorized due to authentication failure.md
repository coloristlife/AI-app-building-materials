
# The client is unauthorized due to authentication failure


这个错误 `Neo.ClientError.Security.Unauthorized` 和 `authentication failure` 非常明确：**你的 Python 脚本由于密码（或用户名）不正确，被 Neo4j 数据库拒绝访问了。**

我们在 `import_to_neo4j.py` 脚本中设置了从环境变量读取密码：
`NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "your_neo4j_password")`

如果你没有在终端里设置这个环境变量，它就会使用默认的 `"your_neo4j_password"` 去尝试连接你的数据库，这必然会失败。

### 解决方法（选择一种即可）：

#### 方法 1：在终端中设置环境变量 (推荐，最安全)
在运行你的 Python 导入脚本之前，在同一个终端窗口中执行以下命令（将 `这里替换为你的真实密码` 替换为你在创建 Neo4j 数据库时设置的密码）：

**Mac/Linux:**
```bash
export NEO4J_PASSWORD="这里替换为你的真实密码"
python import_to_neo4j.py
```

**Windows (PowerShell):**
```powershell
$env:NEO4J_PASSWORD="这里替换为你的真实密码"
python import_to_neo4j.py
```

#### 方法 2：直接在代码中修改 (最直接)
如果你只是在本地测试，不想折腾环境变量，可以直接打开 `import_to_neo4j.py`，把密码硬编码进去。

找到这行代码：
```python
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "your_neo4j_password")
```
修改为（保留引号）：
```python
NEO4J_PASSWORD = "你的真实Neo4j密码" 
```

---

### 💡 如果你忘记了 Neo4j 的密码怎么办？

如果你不记得当初在 Neo4j Desktop 里给这个数据库设置的密码是什么了，你可以直接重置它：

1. 打开 **Neo4j Desktop**。
2. 找到正在运行的 `securityArcGraph` 实例。
3. 点击实例卡片右上角的 **三个点 (...)**。
4. 在弹出的菜单中选择 **"Reset password"** (重置密码)。
5. 输入一个新的密码。
6. 使用这个新密码更新你的环境变量或 Python 脚本，然后再次运行 `import_to_neo4j.py`。
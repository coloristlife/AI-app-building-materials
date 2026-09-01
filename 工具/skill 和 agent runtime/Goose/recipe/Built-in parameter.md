## recipe_dir

`recipe_dir` 的值是无法在代码或界面里手动修改的。**

在 Goose 中，`recipe_dir` 是一个**只读的系统内置变量**。

它的设计初衷，是为了让 Recipe **“知道自己被保存在哪里”**。
举个例子：如果你写了一个很复杂的 Recipe，除了 `.yaml` 文件，同目录下还跟着一个 `prompt.txt` 和一个 `style-guide.md`。无论你把这个文件夹移动到电脑的哪里，只要在代码里写 `{{ recipe_dir }}/prompt.txt`，Goose 就永远能精准地找到这个配套文件，而不会报错。

**总结：**
* **`recipe_dir`（内置位置）** = “我的配置文件放在哪”。（**不可改**，除非你把 `.yaml` 文件移走）
* **`target_dir`（自定义参数）** = “我想让 AI 去处理哪个文件夹”。（**随便改**，通过 UI 弹窗或命令行传参）

所以，只要你需要指定一个**目标工作目录**，永远应该自己定义一个新的参数（如 `target_dir`），而把 `recipe_dir` 留给系统去自动找它自己的配件就好啦！




当你把带有 `parameters` 块的 Recipe 文件放入默认目录（`~/.config/goose/recipes`）并在界面中打开时，**Goose 客户端会自动为你生成一个表单（UI 输入框）**，你完全不需要去记命令行参数。

以下是具体的实现步骤：

### 1. 修改并保存你的 Recipe 文件
确保你保存在 `~/.config/goose/recipes/security-review-debug.yaml` 的代码是下面这种带有 `parameters` 定义的形式：

```yaml
version: "1.0.0"
name: "security-review-debug"
description: "Debug target directory"

# 1. 在这里定义你需要的参数（界面会自动把这些变成输入框）
parameters:
  - name: target_dir
    type: string
    description: "Please enter the directory you want to review"
    required: true

# 2. 在指令中使用这个参数
instructions: |
  DEBUG TASK
  
  Please ONLY echo the literal text below. 
  DO NOT use any tools. DO NOT list the directory contents. 
  Just tell me this path:

  {{ target_dir }}
```

### 2. 在 Goose 桌面端中运行它
修改保存后，回到你的 Goose 桌面客户端，按照以下步骤操作：

1. **打开 Recipe 库**：在主界面左侧菜单（或左上角边栏）点击 **“Recipes”**。
2. **选择你的 Recipe**：在列表中找到你刚刚保存的 `security-review-debug`（如果没有，可以尝试刷新或重启客户端）。
3. **点击“Run Recipe”（运行配方）**。
4. **填写弹出的表单**：因为我们在文件里定义了 `target_dir`，此时**界面上会自动弹出一个名为 "Recipe Parameters" 的输入框/对话框**。
5. **输入目标路径**：在对话框的文本框中，输入你想要分析的目录绝对路径（例如 `/Users/yani_dong/my-project`），然后点击提交。

提交后，Goose 就会使用你刚才通过 UI 输入的路径去替换 `{{ target_dir }}`，并以此来初始化这一轮的新对话。

### 💡 进阶 UI 技巧：使用下拉菜单选择路径
如果你只有几个固定的路径想让 AI 处理，你甚至可以让 UI 渲染成一个**下拉菜单**，防止自己手动打错路径。只需要在 `parameters` 中使用 `select` 类型和 `options` 字段：

```yaml
parameters:
  - name: target_dir
    type: select  # 改变类型为选择器
    description: "Choose the target project directory"
    required: true
    options:      # 提供可选列表
      - "/Users/yani_dong/project-A"
      - "/Users/yani_dong/project-B"
      - "/Users/yani_dong/Downloads"
```
这样修改后，下次你在桌面端运行这个 Recipe 时，原本的文本输入框就会变成一个下拉菜单，供你直接点击选择！


## Goose 桌面客户端（GUI）在底层是如何管理 Recipe 文件的

当你通过 Goose 界面 **“Load（加载/导入）”** 一个 `.yaml` 文件时，发生了以下事情：

### 为什么会变成默认路径？
为了方便统一管理，当你把一个外部的 `.yaml` 文件加载到 Goose 界面中时，**Goose 客户端会在后台把这个文件“复制”或“安装”到它的系统统一目录**（也就是 `~/.config/goose/recipes`）。

既然这个文件已经被 Goose 收编、存放到了默认目录里，那么当它开始运行时，`recipe_dir`（永远指向文件当前真实物理位置）自然就会输出这个默认路径！

### 这说明了一个核心事实：
**不要试图用 `recipe_dir` 来作为“你想让 AI 去处理的业务目录”！**

无论你怎么折腾，只要文件交给了 Goose 界面去运行，`recipe_dir` 基本上都会指向 Goose 的安装或默认配置目录。它只是用来让 Recipe 找“自身附属文件”（比如配套的 txt 模板）的，**不是用来指定工作目录的**。

---

### 💡 彻底解决你需求的终极方案

如果你现在的真实需求是：**我想在 Goose 界面里运行这个 Recipe，并让 AI 去分析我电脑里其他的某个文件夹（比如桌面上的项目文件）。**

请**彻底放弃**在 prompt 里使用 `{{ recipe_dir }}`，改为以下步骤：

**第一步：修改你的 `.yaml` 文件，定义一个专门的参数（比如叫 `work_path`）**
```yaml
version: "1.0.0"
name: "security-review"
description: "Review a system"

# 1. 强行定义一个自定义变量，让界面弹出一个输入框
parameters:
  - name: work_path
    type: string
    description: "请输入你要分析的项目所在路径（例如 /Users/yani_dong/my-project）"
    required: true

# 2. 在指令里使用这个自定义变量，完全不要提 recipe_dir
instructions: |
  请对下面这个目录中的文件进行安全审查：
  
  {{ work_path }}
```

**第二步：在 Goose 界面重新 Load 并运行它**
1. 把修改后的 `.yaml` 加载进 Goose 界面。
2. 点击运行（Run Recipe）。
3. 此时，Goose 界面会弹出一个表单，提示你输入 `work_path`。
4. **在这个输入框里，手动填入你想让它去分析的那个路径**（比如填 `/Users/yani_dong/Downloads/test`）。
5. 点击确认。

这样，AI 就会准确无误地去读取你输入的 `/Users/yani_dong/Downloads/test` 目录，而不会再去管什么默认路径了！
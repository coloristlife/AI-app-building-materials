## Obsidian 引用方式速查表

|写法|类型|当前文章显示什么|Original 更新后|在当前文章中修改|是否会修改 Original|
|---|---|---|---|---|---|
|`[[Original]]`|普通 Link|❌ 不显示内容，只显示链接|—|❌ 不能直接修改引用内容|❌|
|`![[Original]]`|Embed|✅ 整篇文章|✅ 自动更新|✅ 可以编辑|**✅ 会修改 Original**|
|`[[Original#Section]]`|Section Link|❌ 不显示 Section 内容|—|❌|❌|
|`![[Original#Section]]`|Section Embed|✅ 显示整个 Section|✅ 自动更新|✅ 可以编辑|**✅ 会修改 Original**|
|`[[Original#^block-id]]`|Block Link|❌ 不显示 Block 内容|—|❌|❌|
|`![[Original#^block-id]]`|Block Embed|✅ 显示这个 Block|✅ 自动更新|✅ 可以编辑|**✅ 会修改 Original**|

### 最关键的一点

所以如果你的要求是：

> **“我想引用 Original 的内容，并且 Original 更新时自动同步，但我在引用文章里不能修改 Original。”**

那么上面这些 **Obsidian 原生引用方式都不能真正做到“只读引用”**。

可以把它简单记成：

```text
[[...]]
    = 只链接，不显示

![[...]]
    = 显示 + 保持同步 + 修改会回写 Original
```

而 `Section` 和 `Block` 的区别只是**引用范围不同**：

```text
![[Original]]
        → 整篇

![[Original#Section]]
        → 一个 Section

![[Original#^block-id]]
        → 一个 Block
```






### 1. 普通链接：只建立“跳转关系”

```markdown
[[Original]]
```

效果：

> 当前文章里出现一个链接，点击后跳到 `Original.md`。

它**不会把 Original 的内容显示在当前文章里**。

```text
Article A
   │
   └── [[Original]]
             ↓
        点击后打开 Original
```

**适合：**参考资料、关联文章。

---

## 2. 整篇文章 Embed

```markdown
![[Original]]
```

效果：

> 把 `Original.md` 的整个内容显示在当前文章里。

如果 Original 修改：

```text
Original
   ↓
自动更新
   ↓
Article A
```

**适合：**你希望完整复用另一篇文章的时候。

---

# 3. Section Reference：引用一个章节

例如 Original：

```markdown
# AI Security

## Prompt Injection

Prompt injection is an attack...

There are several attack patterns...

## Mitigation

Applications should implement...

Security controls should include...
```

可以：

```markdown
![[Original#Prompt Injection]]
```

或者：

```markdown
![[Original#Mitigation]]
```

这样引用的是对应 Heading 下的整个 Section。

### Section 的边界是什么？

最简单理解：

```text
## Prompt Injection
       ↓
       内容
       内容
       内容

## Mitigation
       ↑
       Prompt Injection Section 在这里结束
```

也就是说：

> **遇到同级或更高层级的 Heading，前一个 Section 就结束。**

所以：

```markdown
## A

内容 A

### A-1

内容 A-1

### A-2

内容 A-2

## B

内容 B
```

`## A` Section 包含：

```text
A
├── A-1
└── A-2
```

直到遇到：

```markdown
## B
```

才结束。

---

# 4. Block Reference：引用一个具体内容块

这是我认为**最适合你 Knowledge Base 的方式**。

例如：

```markdown
## Definition

Prompt injection is a technique where an attacker
manipulates the model through crafted instructions.
The goal is to cause unintended behavior. ^prompt-injection-definition
```

这里：

```text
^prompt-injection-definition
```

就是这个 Block 的 ID。

其他文章：

```markdown
![[Original#^prompt-injection-definition]]
```

就可以只引用这一块。

---

# 5. Block 到底有多大？

这是你刚才问的重点。

**Block ≠ 一行。**

例如：

```markdown
这是第一行，
这是第二行，
这是第三行。 ^my-block
```

可以是**一个 Block**。

真正需要注意的是：

### 普通换行 ≠ 一定产生新的 Block

```markdown
第一行
第二行
第三行
```

仍然可以属于同一个 Markdown paragraph/block。

### 空行通常会产生新的 Block

例如：

```markdown
第一段第一行。
第一段第二行。

第二段第一行。
第二段第二行。
```

这里通常是：

```text
Block 1
├── 第一段第一行
└── 第一段第二行

Block 2
├── 第二段第一行
└── 第二段第二行
```

所以你可以记住：

> **Block 的边界主要由 Markdown 的结构决定，而不是简单由“换行”决定。**

---

# 6. Block 不只有 Paragraph

Block 可以是很多 Markdown 元素。

例如一个引用块：

```markdown
> This is an important security principle.
> It should be applied consistently. ^security-principle
```

可以作为一个 Block。

列表：

```markdown
- Validate the token
- Check the audience
- Verify the issuer ^token-validation
```

也可以作为一个 Block。

Callout：

```markdown
> [!warning]
> This control is mandatory.
> Do not skip validation. ^mandatory-control
```

也可以作为一个 Block。

所以：

> **Block 更接近“一个 Markdown 结构单元”，而不是“一行文字”。**

---

# 7. Section 和 Block 的关系

这个可以用一个树形结构理解：

```text
Original.md
│
├── ## Prompt Injection       ← Section
│   │
│   ├── Definition            ← Block
│   ├── Attack Mechanism      ← Block
│   └── Mitigation            ← Block
│
├── ## Tool Poisoning         ← Section
│   │
│   ├── Definition            ← Block
│   └── Mitigation            ← Block
│
└── ## Monitoring             ← Section
    │
    ├── Detection             ← Block
    └── Logging               ← Block
```

所以：

**Section 是大的容器。**

**Block 是里面可以独立复用的小知识单元。**

---

# 8. 最后一个非常重要的区别：Link vs Embed

这几个符号很容易混：

|写法|意义|
|---|---|
|`[[Original]]`|链接到文章|
|`![[Original]]`|显示整篇文章|
|`[[Original#Section]]`|链接到 Section|
|`![[Original#Section]]`|显示 Section|
|`[[Original#^block-id]]`|链接到 Block|
|`![[Original#^block-id]]`|显示 Block|

这里的 `!` 可以理解成：

> **“不要只是链接，我要把它显示在这里。”**

---

# 9. 针对你的 Knowledge Base，我建议这样设计

你可以采用：

```text
Knowledge Object
│
├── Section
│   ├── Block
│   ├── Block
│   └── Block
│
├── Section
│   ├── Block
│   └── Block
│
└── Section
    └── Block
```

然后：

### 大范围复用 → Section

```markdown
![[AI Security#Prompt Injection]]
```

### 精确复用 → Block

```markdown
![[AI Security#^prompt-injection-definition]]
```

### 只是想建立关联 → 普通 Link

```markdown
[[AI Security]]
```

---

## 10. 最推荐的工作原则

你以后写 Knowledge Base，可以把它理解成：

> **Section = Topic**
> 
> **Block = Reusable Knowledge Unit**
> 
> **Article = Presentation / Application**
> 
> **Link = Relationship**
> 
> **Embed = Reuse**

例如：

```text
                    Knowledge Base
                          │
              ┌───────────┴───────────┐
              │                       │
       Prompt Injection          Tool Poisoning
              │
      ┌───────┼────────┐
      ↓       ↓        ↓
 Definition  Risk   Mitigation
    Block     Block     Block
      │                  │
      │                  │
      ↓                  ↓
 DP Article         Security Review
```

这样你以后修改 **Canonical Knowledge Object 里的 Block**，所有引用这个 Block 的文章都会跟着更新。

**一句话总结：**

> **Section 用来组织知识，Block 用来复用知识，Embed 用来显示知识，Link 用来关联知识。**

另外，关于你前面特别关心的**“引用后能不能防止误修改 Original”**：Obsidian 原生的 Embed/Block Reference **并不是权限意义上的只读**。如果你要把这个 Knowledge Base 做成真正的 **Canonical Source → Read-only Reference** 模式，需要额外解决“引用内容不可编辑”这个问题。
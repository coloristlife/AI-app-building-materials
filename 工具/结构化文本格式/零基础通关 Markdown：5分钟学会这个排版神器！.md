# 💡 什么是 Markdown？

简单来说，Markdown 是一种极其简单的“排版语法”。

平时我们在 Word 里写文章，要加粗字体、设置标题，得频繁用鼠标去点顶部的工具栏。而在 Markdown 里，你只需要在文字旁边加上几个简单的符号（比如 # 或者 \* **），你的写作软件就会自动把它们变成漂亮的标题、加粗文字或表格。

它就像是给纯文本施了魔法，让你手不离开键盘，就能完成所有排版。

# 🌟 为什么要学习 Markdown？

除了“排版好看”、“沉浸式写作”之外，在今天，我们有了一个不得不学 Markdown 的绝对理由：

👉这是 AI（人工智能）最喜欢的语言！

如果你经常使用 ChatGPT、Kimi 或 Claude 等 AI 工具，你会发现：

- AI 沟通零障碍：AI 生成的所有回答（包括表格、代码、加粗高亮），底层全是用 Markdown 写的。
    
- AI 更容易理解你：Word 文档或富文本网页里藏着大量 AI 看不懂的杂乱代码。而 Markdown 是最纯净的文本格式，不仅体积小，而且结构极其清晰（哪里是重点、哪里是列表一目了然）。当你用 Markdown 格式向 AI 提问或喂资料时，AI 的理解准确率会大幅提升。
    

可以说，掌握 Markdown，就是掌握了与 AI 高效对话的“普通话”。

# 🛠️ Markdown 核心语法（一看就会）

Markdown 的语法非常简单，就像是在文字旁边做小记号。我们只要记住最常用的几个就行了。

(💡新手必看秘籍：在 Markdown 里，符号和文字之间，通常都需要留一个空格哦！)

## 1. 标题：用 # 搞定

在文字前面加上 # 号就能变成标题。1 个 # 是一级标题，2 个 # 是二级标题，最多支持六级。

✍️ 你这样写：

# 这是一个一级标题

## 这是一个二级标题

### 这是一个三级标题

✨ 出来的效果就是：

![Image](https://mmbiz.qpic.cn/sz_mmbiz_png/Vibdnzy0jBL6iaYZm1MAhabVAdeokpaqtkyGERG0dNVN9tbamWcYp6wGvAicJqkCBW4fibWn9icz4msH1yFCpakN0TDt4wOaEjVFZib2X2eeunlHA/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

(注意：标题级别不要太多，一般用到三四级就足够啦。)

## 2. 列表：帮你有条理地表达

列表分为“无序列表”（只有圆点）和“有序列表”（有数字）。

✍️ 你这样写（注意符号后的空格）：

- 这是无序列表的第一点

- 这是无序列表的第二点

1. 这是有序列表的第一步

2. 这是有序列表的第二步

✨ 出来的效果就是：

![Image](https://mmbiz.qpic.cn/mmbiz_jpg/Vibdnzy0jBL7BFUb8C201VnwD8iabQcCYa639INF9o79C8sFpRx6ibs4uFfcO9Wk3hbyHQnHCEr1mZhEAyy2G51OxlfDMoyx2P3Wwl0T7icLibFc/640?wx_fmt=jpeg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

## 3. 强调文字：加粗与斜体

想让某个词变得醒目？用星号 * 把文字包起来就行！

✍️ 你这样写：

在这个句子里，我要**加粗**重点，还要使用*斜体*。

如果想又加粗又斜体，就用***三个星号***。

✨ 出来的效果就是：

![Image](https://mmbiz.qpic.cn/mmbiz_jpg/Vibdnzy0jBL5AIEkJ1CVpBR1gzgoaQZk0pAOMHicwyRZibDJFPvPUBubYX1qWt6kgL4EAaFiaI96N3QhwDXKpT5fMABcO0FcR5thCpY2eiaLaqdM/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2)

## 4. 插入链接和图片

这两个语法的长相非常像，就像一对双胞胎：

链接：
```
[显示的文字](网址)
```

图片：
```
![图片描述](图片地址)
```

 （比链接前面多了一个感叹号 !）

✍️ 你这样写：

```
欢迎使用 [百度搜索](https://www.baidu.com) 查找资料。
下面是一张可爱的网络图片：
![图片](https://picsum.photos/300/200)
```

✨ 出来的效果就是：

![Image](https://mmbiz.qpic.cn/sz_mmbiz_png/Vibdnzy0jBL5pPgZctw3Y8iavsQtzzxHicfD0mmfBQhPO2GIHXgscarNnv6lNks9O8ib4Y8OHGSEOmickGOjOicxPI7tBVyGYPpqyIiaZdCsqKmd68/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=3)

(小贴士：插入本地图片容易因为文件移动而丢失，初学者建议多使用网络图片链接，或者借助专门的写作软件自动处理。)

## 5. 待办事项（任务列表）

想做一个打卡清单吗？用这个语法最酷了！方括号里是空格表示未完成，写上 x 表示已完成。

✍️ 你这样写：
```
- [x] 早上喝一杯水

- [ ] 学习 Markdown

- [ ] 和 AI 对话一次
```

✨ 出来的效果就是：

![Image](https://mmbiz.qpic.cn/mmbiz_jpg/Vibdnzy0jBL7mPibwtfrPVhv4B3xY8IDsiaG0S2ythibWANIicvjmblT8uEhOEiaWpGlGjcxrFDpoiabavTjeapB0LZH2GsyfwzRXwsQRoanUEms7k/640?wx_fmt=jpeg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=4)

## 6. 表格
插入表格：

Markdown 的表格是画出来的，用竖线 | 分隔列，用短横线 - 分隔表头。

✍️ 比如这样：

```
|姓名 | 数学 | 语文 |

|--- | --- | --- |

| 张三 |100|90|

| 李四 |80|95|
```

✨ 出来的效果就是：

![Image](https://mmbiz.qpic.cn/mmbiz_png/Vibdnzy0jBL6rbOV261CbzIp6diaAk5ZvnD49AKianyfu1ew84TgXJBDLliawicvpqqS1jRsMVMyKbW1D7ZKBDK5xDdSeJEiaH3kMz6hN8INEuiah4/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=5)

【小贴士】：

纯手打表格有点枯燥，平时可以借助在线工具，比如 TableGenerator：https://www.tablesgenerator.com/markdown_tables 自动生成 Markdown 表格哦！

---

# 🎁 去哪里写 Markdown 呢？

很多初学者看完语法后，满怀激动地打开 Microsoft Word 敲下 # 标题，结果发现什么变化都没有，瞬间产生挫败感。

为了不踩坑，在开始动手前，你需要了解以下三个关键常识：

## ❌ 1. 避坑指南：不要在 Word 里直接写

Word、WPS 等属于“富文本编辑器”，它们有自己一套复杂的排版系统。如果你在 Word 里输入 # 标题，它只会把你输入的 # 当成一个普通的标点符号，并不会施展魔法把它变成大号字体的标题。

## 💡 2. 本质揭秘：可以在普通的“记事本”里写吗？

答案是：完全可以，但你暂时“看”不到排版效果。

Markdown 的本质就是纯文本（Plain Text）。这意味着，你完全可以在电脑自带的“记事本”（Windows）或“文本编辑”（Mac）里敲打这些带有 # 和 * 的内容。

会发生什么？在记事本里，它依然是一堆干巴巴的普通文字。

怎么变身？你只需要把这个记事本文件保存下来，将文件后缀名从 .txt 改成.md。这就是一份标准的 Markdown 文件了（虽然在“记事本”还是看不到效果）！

> 🤖 这也是为什么 AI 最懂 Markdown 的原因：  
> 正因为它是纯文本，没有任何 Word 里那种肉眼看不见的复杂排版代码，所以不管你是在记事本里写，还是在网页里敲，AI 都能瞬间看懂你的层级、列表和重点，绝对不会出现格式错乱！

## ✅ 3. 正确姿势：使用支持 Markdown 的编辑器

既然 Markdown 是一堆带有符号的纯文本，怎么才能看到它最终漂亮的排版效果呢？

你需要一个支持渲染 Markdown 的“魔法笔记本”（编辑器）。

强烈推荐初学者使用以下软件：

- Obsidian（黑曜石）：一款非常强大的笔记软件，完美支持 Markdown，你打出符号的同时，它就能立刻给你展示排版效果。
    
- 各大 AI 工具：没错，直接把你的 Markdown 文本发给 ChatGPT 或 Kimi，它们也能完美识别！
    

🎉 恭喜你！

看到这里，你已经掌握了 Markdown 90% 的常用操作。现在就打开一个支持 Markdown 的软件，试着敲下 # 我的第一篇 Markdown 吧！
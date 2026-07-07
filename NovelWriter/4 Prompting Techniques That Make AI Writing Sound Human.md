



# 让 AI 写作更像人类的 4 种提示词技巧

这里有四个提示词（Prompting）技巧，只要掌握了它们，你写出的书就能从显而易见的“AI批量生产的垃圾（AI slop）”，蜕变成完全没有人能猜出是由AI代笔的佳作。效果就是这么好。

在我的自动化工作流中，我重度依赖这些技巧。目前我正在开发自己的AI写作工具，并在所有这些技巧上加倍投入。我相信，只要你能搞懂这四个技巧，它们将对你的写作过程产生极大的帮助。

现在大多数人并没有使用这些技巧，坦白说，如果你在聊天机器人里手动使用它们，过程会有些繁琐，而大多数人并不喜欢那样。这也是为什么我大量使用自动化程序的原因：它可以在不需要我监督的情况下，自动跑完这些步骤和技巧。但毫无疑问，你完全可以在你的写作流程中手动使用它们。

接下来，让我们深入探讨这四个技巧，看看如何利用它们来提升你的写作水平。

---

## 技巧一：对作品进行“检查与审查”（Checks or Critiques）

这个听起来可能很简单，但很多人都做错了。

假设你刚刚通过向AI下达指令写完了一个章节。刚出炉的草稿一定会有很多问题：它会包含大量的“AI惯用语（AISMs）”，还可能存在一些糟糕的写作示例，比如用了太多的副词等等。理想情况下，你肯定希望能尽可能多地过滤掉这些问题，这样你就不需要手动去修改了。当你亲自上手润色时，你只需要专注于世界观、时间线，让它尽可能契合你自己的愿景，或许再添加一些AI无法理解的“人类特有的灵气”。但至少，我们可以把AI本身的毛病降到最低。这样，你就不用像玩“打地鼠”一样去应付满篇的错误，而是可以从一份相当干净的草稿开始工作。

**具体操作方法如下：**

1. **制定改进计划：** 拿着你的章节草稿，向AI输入一段类似这样的提示词：“我希望你搜索所有多余的副词，并给出一份删除这些副词的改进计划。”
   * **核心要点：** 我们**不要**让它直接重写任何内容。我们只是让它制定一个修改计划。这能让它专注于一组非常狭窄的参数。在“检查”方法中，最关键的一点就是：**每次检查最好只专注于几个特定的问题。**
   * **优势：** 值得庆幸的是，如果你把范围缩得足够小（比如我们只关注副词），你就可以使用像 Gemini 3 Flash 这样非常廉价的模型来完成这项检查。如果你在一个检查里塞进一大堆需要注意的事项清单，那就有让AI注意力过度分散的风险。只要我们聚焦它所查看的内容，就能行得通，随后我们可以运行多次不同的检查来修复整篇文章。

2. **执行修改：** 在第二步中，你要求AI整合刚刚那份改进计划中的反馈，**并且除了改进计划上的内容外，不要更改任何其他东西。**
   * **核心要点：** 这是另一个极其关键的环节。如果你不这样要求，它很可能会重写整个章节，而且写得可能比初稿还要糟糕（特别是当你在重写过程中使用的是能力较弱的模型时）。但如果你只要求它修改改进计划里的内容，保留其他所有内容不变，你就可以用一个较基础的模型来实质性地提升你的草稿。

因为在简单的聊天机器人中跑完所有这些检查需要花费大量精力，所以使用这个技巧的人还不够多（尽管你完全可以手动做）。这也是为什么我把它们放进我的自动化程序里，让它自动执行一系列设定好的步骤。

你可以设置各种各样的检查：
* 检查副词
* 检查对话标签
* 检查场景的逻辑性和合理性
* 检查各类“AI惯用语”。比如，你知道AI非常喜欢用“它不仅是这个，而且还是那个（it's not just this, but it is also that）”这种句式。你可以专门创建一个检查来寻找这种特定的措辞，并让它提供一个替代说法。

运行这些检查并过滤掉问题，是将整个内容“人性化”的绝佳方式。只要你有一套扎实的检查流程，并为每一项检查配备好相应的提示词，这就是提升写作质量最强大的方法之一。

---

## 技巧二：上下文工程的价值（Context Engineering）

第二个重要的提示词技巧，其重要性远远超出了人们的认知，那就是“上下文工程”。

最近出现了这样一个概念：与其说关键在于提示词本身，不如说关键在于**你提供给AI的上下文质量**。从小说作者的角度来看，这是显而易见的。这意味着你需要提供给它所有关于你的世界观、情节以及你希望它知道的角色信息。如果你不提供，它就不会知道，它只会编造出一些不符合你愿景的通用内容。

但这个技巧还要更深入一些。

例如，当你正在写一个章节并给AI提供了一大堆信息时，它可能会挑选出**错误的信息片段**来写这一章。相反，我们想要精心策划（Curate）在AI写这一章时到底该输入什么内容。也许只输入该场景中出现的角色，或者只输入该场景需要的关键细节。

* **工具推荐：** 如果你使用像 Novelcrafter 这样的工具，它在管理上下文方面极其出色。它能确保AI只知道写入当前场景所必需的那一小部分信息。虽然 Novelcrafter 这个平台稍微有点复杂，但它是上下文工程的利器。
* **自动化操作：** 在我的自动化流程中（这也是我目前 90% AI 写作的方式），我会加入一些步骤，让程序先看看需要写什么内容，然后再查看整体的角色设定表等资料，**仅仅挑选出该特定场景需要用到的片段**，并在写这一章时只传递这些片段。

**切记：不要给AI过多的上下文**

这不仅仅是因为你不想给它不需要的信息，更是因为**这实际上会冲淡你的提示词**。我见过太多这样的例子：人们在写第二本书时，把整本第一书的内容都塞进上下文里；或者即使在写第一本书时，他们在写下一章时，也会把之前写过的所有内容都放进上下文里。

我强烈建议你不要这么做。因为你正在稀释提示词。你让AI在需要提取某些细节时，变得像“大海捞针”一样困难。

**解决方案：提供精简且重要的摘要**

上下文工程的一部分，是为AI提供它所需文本的简明重要摘要。
这也是为什么我会使用一个名为“创建 Summary Plus（摘要加强版）文档”的自动化流程。它会扫描你的整本书，将每一章逐一总结成只包含该场景关键细节的内容。比如：
* 一段话的场景摘要
* 该场景中的角色列表及角色描述
* 角色遭遇了什么，以及一些其他类似细节

它将使用的文本量或整本书浓缩成AI更容易理解和管理的形式。同时，它会对所有内容添加**路标（Signposts）**，以便AI能迅速找到它想要寻找的内容。

这比直接把整本书扔进去，然后祈祷它知道书里的一切要好得多。即使整本书据说都在它的“上下文窗口”限制内，但AI的运作方式并非如此：**上下文越大，它需要筛选的内容就越多，它在识别场景所需的相关细节方面就会变得越糟糕。**

所以，我建议大家尽量缩小上下文范围。如果可以的话，尽量将其保持在 **50,000 个 Token 以下**，因为这会直接带来更高质量的输出。


---

## 技巧三：叙事物理学与滑块（Narrative Physics & Sliders）

第三个主要的提示词技巧是一个让我非常兴奋的新概念。

最初是 Future Fiction Academy（未来小说学院）提出了这个被称为“叙事物理学（Narrative physics）”的想法。我在它的基础上做了一些扩展，我将其理解为针对你世界观中不同方面的 **“滑块（Sliders）”** 或者你可以把它看作是 **“游戏属性值（Game Stats）”** 。

这仍然只是一种提示词技巧，并没有什么疯狂之处，但我给你举个例子看看它是什么样的（未来我可能会专门做一期视频深入讲解）。

**核心理念：**
假设你的书里有一个角色，你有一份角色小传，并且在这个角色出现的每个场景中你都包含了这份小传。但是，如果这个角色在故事发展过程中发生了变化怎么办？如果他们的情绪处于不同的状态，导致他们做出不同的反应怎么办？

比如，你可能有一个平时非常善良的角色，但在巨大的压力下可能会崩溃甚至杀人（如果在适当的情况下）。我觉得这里有点像《蝙蝠侠：黑暗骑士》里小丑的那个梗：**如果你只给人们轻轻一推，他们什么都做得出来。** 这就是人们在不同情况下表现不同的概念。

虽然“叙事物理学”是未来小说学院提出的，但我没看过他们的提示词，也不知道他们具体怎么操作。我根据他们的概念想出了自己的方法——**滑块（Sliders）**。

**滑块的实际应用：**
对于每个角色，我现在会给他们设定一些滑块，比如从“压力（Stress）”到“和谐/平静（Harmony / Peace）”。
* 如果他们在和谐这一端是 **数值 10**，那他们可能和谐过头了，有点恍惚，甚至可能像是吸毒了之类的状态。
* 但如果他们走向滑块的另一个极端，比如在压力这一端是 **-10**，那他们就是压力大到正在经历恐慌发作，字面意义上处于濒死边缘。
* 我们可以选择中间的某个数值作为他们的**基线（Baseline）**。

然后，对于每一个场景，我们可以让AI去识别：**“好的，他们现在是还处于基线状态，还是从基线向上或向下移动了？”**
这样做可以让角色发生转变，并对场景做出更真实的反应。这是一个让你的角色获得更多变化、避免听起来总是单调乏味的绝佳技巧。

**其他应用场景：**
* **魔法系统：** 这个系统的规则是什么？它是如何运作的？代价是什么？用类似计算机或游戏般具体的属性数值来建立这些规则，并在整本书的过程中让它们改变和进化。
* **场景张力：** 你想在故事中传达的特定情绪，比如一个场景中的紧张程度，在滑块上看起来是怎样的？
* **亲密/火辣程度（Spiciness）：** 场景的热辣程度在滑块上是怎样的？有时因为角色互相讨厌，火辣度为 0。在爱情小说里，它可能会起起伏伏，但慢慢变得越来越强，然后突然“砰”的一下爆发。你可以把它拉满到数值 10，那就是色情文学（Pornographic erotica）级别了。

通过不同的滑块，我们可以告诉AI：“这就是我们想要的紧张程度”、“这就是角色目前在自己滑块上的位置”等等。这是一个非常酷的技巧。

---

## 技巧四：分层处理（Layering）

最后一个我想重点讨论的技巧，因为没有更好的词，我姑且叫它“分层（Layering）”。

它的核心思想是：**我们实际上可以在同一个批次中，利用多个不同大语言模型（LLMs）各自的优势。**

与其只选择一个 LLM 并指望它给我们提供想要的一切，不如将任务分步，并在每一步使用不同的 LLM。这不仅能让我们发挥各个模型的长处，还能避免单一模型带来的“同质化（sameness）”。

举个例子，我非常喜欢 Claude 模型，比如在我录制这个视频时最新的 Claude 4.6 Opus。但是当我长时间用它工作时，它从头到尾听起来都会是某种非常相似的语调。分层技巧可以打破这种单一感，让作品变得更好。

**在实践中，它是这样运作的：**

1. **逻辑与结构（使用 Gemini 或 ChatGPT）：** 这两个模型通常在逻辑思维和结构搭建上非常出色。所以我们可以从它们开始，让它们查看我们提供的场景信息并说：“好的，让我们扩展这些内容并创建一个场景大纲（Scene Brief）。”它会创建大纲以及我们需要它包含的所有小细节。
2. **对话撰写（使用 Grok）：** 我们知道 Grok 在写对话方面非常棒。所以我们可以把场景大纲传给 Grok，说：“你能根据这个写一个只包含对话的草稿吗？在对话之间用占位符随便写一点动作提示即可。”
3. **日常散文与描写（使用 Gemini）：** 接着，我们把它交给 Gemini。Gemini 在整体散文（Prose）方面表现不错，但在其他方面可能稍逊一筹。所以我们说：“填补所有的散文描写，识别出那些舒缓的日常场景，并为这些内容写下描写。”
4. **高潮与戏剧冲突（使用 Claude Opus 4.6）：** 最后，把它交给 Claude Opus 4.6，告诉它：“你非常擅长写严肃、戏剧性、高潮迭起的场景。过一遍这个场景里剩下的所有部分，写下那些关键片段，然后把所有内容融合在一起。”

最终，**你会得到一个经过四五个不同 LLM 处理过的章节，每个模型都贡献了它们独有的特长。** 相比于你直接去找 Claude 或 Gemini 让它一次性写完整个章节，这种方法得出的结果绝对是令人震惊（Mindblowing）的。

这是一个非常强大的技巧，我认为很多人都没有利用起来。诚然，这样做会增加你的成本，特别是如果你使用的是 API，尤其是在自动化格式下执行，这会花费更多的钱。但如果资金对你来说不是问题，这绝对是从 LLM 中获取极高质量结果的绝佳途径。

---

## 结语

如果你将**上下文工程**、**检查与审查**、**叙事物理学与滑块**以及**分层技巧**全部结合起来，你将会得到非常惊艳的成果。

这四个相当高级的工具/技巧对你的创作将大有裨益。如果你想获取我的很多资源，包括我目前正在构建的、涉及上述内容的自动化工作流，你可以通过下方的链接访问 Story Hacker Gold 群组。如果你加入时它还在候补状态，你也会立刻通过邮件免费获得一大批我的提示词。等 Story Hacker Gold 群组正式公开开放时，你就可以随时加入了。

---
【附录】
# 【AI写作实操解密】如何在提示词中真正落地“滑块（Sliders）”技巧？

基于原作者在分享中的详细描述，虽然他提到未来可能会专门做一期视频来深入讲解这个技巧的具体提示词，但他已经在本次分享中清晰地勾勒出了“滑块”技巧的**具体实操逻辑和工作流**。

请务必记住，原作者明确表示他没有看过 Future Fiction Academy（该概念最初提出者）的提示词，完全是基于“叙事物理学”的概念自己摸索出的这套“滑块”方案。

以下是严格根据原作者的实操经验整理的落地指南，你可以将其直接应用到你的提示词构建中：

### 第一步：在“角色小传”中植入滑块设定
在实操的第一步，你需要修改你的角色设定库。
*   **操作方法：** 假设你有一份书中角色的“角色小传（Character Bio）”，你需要确保**在这个角色出现的每一个场景中，都将这份角色小传包含在发给 AI 的上下文里**。
*   **添加滑块：** 现在，你要在这份角色小传中为他们添加具体的“滑块”。例如，设定一个从“压力（Stress）”到“和谐或平静（Harmony / Peace）”的滑块。

### 第二步：像设定“游戏属性值”一样量化极端数值
实操的关键在于使用**具体的数字属性（Actual numbered stats）**，以几乎类似计算机或游戏的方式来建立这些设定。
*   **定义正向极端（如 数值 10）：** 你需要在提示词中告诉 AI 这个数值代表的具体状态。比如，如果他们在和谐这一端是“数值 10”，这实际上代表他们“和谐过头了（too harmonious）”，有点恍惚，感觉可能像是吸毒了之类的。
*   **定义负向极端（如 数值 -10）：** 走向滑块的另一边，比如在压力这一端是“-10”，你设定这就代表他们压力太大了，正在经历恐慌发作，字面意义上处于濒死的边缘。

### 第三步：确立角色的“基准线（Baseline）”
*   **操作方法：** 在滑块的两个极端之间，你可以选择中间的某个位置作为该角色平时的“基线（Baseline）”。这个基线就是角色在正常状态下的默认数值。

### 第四步：在每个特定场景中让 AI 进行“数值识别与偏移”
这是让滑块真正发挥作用的动态实操环节。
*   **场景识别提示：** 对于你要写的每一个场景，你可以在提示词中让 AI 去识别：**“好的，他们现在是还处于基线状态，还是从基线向上或向下移动了？”**
*   **指令传达：** 你需要用不同的方式告诉 AI：“这就是角色目前在他们自己滑块上的位置。”
*   **实操效果：** AI 会根据识别到的滑块数值，让角色在当前场景中发生转变，并做出更加真实的反应，而不是永远保持单调同一的语调。

### 第五步：将滑块实操复制到世界观的其他维度
一旦你掌握了角色的情绪滑块实操，你可以用同样的“数字属性”逻辑去构建其他设定，并在整本书的推进过程中让这些数值改变和进化：

*   **魔法系统的实操：** 为魔法系统设定具体的数值规则——它是如何运作的？代价是什么？确保你像设定游戏属性一样确立这些规则，并在提示词中用数字去控制它的变化。
*   **场景张力的实操：** 在提示词中告诉 AI 当前场景的张力滑块数值，明确传达“这就是我们正在寻找的紧张程度”。
*   **火辣程度（Spiciness）的实操：**
    *   告诉 AI 当前场景的火辣度数值是 0（比如因为角色互相讨厌）。
    *   或者告诉 AI 这是一个浪漫场景，要求它在描写时让火辣度的滑块起起伏伏（up and down），但整体趋势慢慢变得越来越强，然后突然“砰”的一下爆发。
    *   如果你想要写色情文学（Pornographic erotica）级别的内容，直接在提示词中告诉 AI 把它一路拉满到“数值 10”。

**总结实操心法：** 
在你的提示词和上下文管理中，放弃模糊的情绪描述，转而建立一套**带有明确基线、正负极端定义，并在每个场景前向 AI 下达具体数值偏移指令**的系统。这就是原作者利用滑块技巧，告诉 AI 角色当前状态并实现完美控制的核心操作模式。

# 4 Prompting Techniques That Make AI Writing Sound Human

https://www.youtube.com/watch?v=pDQDgSm43pw



为了方便阅读，我将你提供的原英文文本去除了时间戳，并按照视频的讲述逻辑（四个技巧）为你进行了合并与段落整理，**英文内容本身未做任何删改**：

***

Here are four prompting techniques that will make it so that your books will go from being obvious AI slop to being something that nobody would guess is actually written by AI. It's that good. I use these techniques heavily in my automations. I'm doubling down on all of them as I'm going through and creating my own tool for writing with AI. And this is I believe these these four techniques if you can figure this out this is going to be extremely helpful for you in the writing process. 

Now most people are not using these techniques because frankly if you're using them inside of a chatbot or something like that it might get a little tedious and most people aren't into that. And that's why I use automations for a lot of these because it can run through several of these steps and techniques without me really having to supervise it. it just does it automatically. But you can absolutely use all of these in the process. So let's dive into these four techniques and figure out how can you level up your writing using all of these.

### 1. Checks or Critiques
The first is by utilizing checks or critiques of your work. Now this might sound simple, but a lot of people get this wrong. Let's say you've written a chapter using AI based on what you told it to do. There are going to be a lot of issues with that chapter right out of the gate. It's going to have a lot of AISMs in it. It's going to probably have some poor writing examples in there, like maybe too many adverbs or something like that. And you ideally would love to filter out as many of those things as possible so that you don't have to change it manually. And then when you go in to fix it up yourself, you're only focusing on those aspects of the the world, the chronology, and just making it match your own vision as much as possible. And maybe just adding a little bit extra human uh flare to it uh that the AI wouldn't necessarily get, but we can at least minimize a whole lot of the issues the AI has. So you're not just playing whack-a-ole with all of these issues that you're actually starting with a fairly clean draft from for you to work on. 

The way this would work is you take your chapter and you would run a prompt on it that says something to the effect of I want you to search for all instances of superfluous adverbs and come up with an improvement plan to remove these adverbs. Now this is the key point of a check like this. We're not going to ask it to rewrite anything. We're just going to ask it to create a plan on what it would change. This allows it to focus on a very narrow set of parameters. And this is key to the uh to the checks approach is that ideally you want to focus on just a few things with each check. And thankfully, if you narrow it down enough, you can use a really inexpensive model like say Gemini 3 Flash or or one of those to do this check. Uh because you've narrowed it down, like let's say we're only focusing on adverbs. You could have a check that includes a giant list of a whole bunch of things that you wanted to watch out for, but that runs the risk of it getting uh too spread out in what it does. If we focus what it what it looks at, then we can do this. And then we can run multiple checks uh to fix this thing up. 

So you ask it for an improvement plan and then in a second step to this, you ask it to incorporate the feedback from the improvement plan but to change nothing else other than what was on the improvement plan. This is another key aspect to it because if you don't do that, it's likely to rewrite the entire thing and do it probably worse than the original uh draft was, especially if you're using a less powerful model in that reddraft process. But if you just asked it to change what was in the improvement plan and leave everything else the same, you can use a lesser model to essentially improve your your draft. 

So, this is a technique that not enough people are using partly because it takes quite a lot to go through all of these checks if you're just using a simple chatbot. Though, you can do it. This is why I do it inside my automations where I will just have a series of these steps that it goes through and it just does them automatically. And you can have all kinds of checks. So you can have checks for adverbs, check for dialogue tags, checks for the logic and plausibility of the scene, checks for various types of AISMs. Like you know that thing that AI does a lot where it says it's not just this, but it is also that. That's something the AI does quite a bit. You could create a check that specifically looks for that particular type of phrasing and gives you an alternative to say instead. And then you just run that check and it filters out all of those things. It's the great way to to utilize humanization in this whole thing. So, that's the checks or critiques process and creating the improvement plan. It's one of the most powerful ways to improve your writing as long as you have a solid series of checks and prompts for each one to go through and filter these things out. 

### 2. Context Engineering
All right, the second key prompting technique that I think is much more important than people give it credit for is the value of context engineering. So context engineering is this term that's come up recently. This idea of just like it's not really about the prompt so much as the quality of the context that you give the AI. So from a fiction writer's perspective, this is pretty obvious. This means like you give it all of the information about your world, about your plot, about your characters that you want it to know. If you don't give that information, it won't know. You know, it'll come up with something more generic that uh doesn't match your vision. 

Uh, but it actually goes a little bit beyond this. For instance, if you're writing a chapter and you're providing it with a whole bunch of information, it might pick the wrong bits of information to write that chapter. Instead, we kind of want to curate what gets fed into the AI's input when it's writing this chapter. So, maybe only the characters that are in that scene or uh just the key details that it needs to know for that scene. And if you're using a tool like Novelcfter, Novelcfter actually is excellent at managing your context and making sure that only the little bits of information that the AI needs to know for that scene that you're writing is the stuff that the AI knows. Um, Novelcfter can be a little bit of a complex platform, but it is excellent at context engineering. If you're running say an automation, which is how I do like 90% of my AI writing these days, I would put some steps in there that kind of look at what needs to be written and then looks at the total character sheet and all of that and just selects the pieces that need to be used in that particular scene. And then those pieces are the ones that are passed on when writing the chapter. 

Another key aspect of context engineering that you need to keep in mind is not giving it too much context. This is not just because you don't want to give it information it doesn't need, but also because this can actually water down the prompt. I've seen too many of examples of people putting their entire first book into the context while they're writing their second book. or even if they're writing just the first book, they're they might have the entirety of everything that's been written up to that point available in the context as they're writing the next chapter. And I strongly advise you don't do this because what you're doing is you're watering down the prompt. You're making it so that if it needs to access certain details, it's like a needle in a hay stack. 

So part of context engineering is also providing the AI with succinct and important summaries of the text that it needs to know. This is why I actually have an automation that I use called creating a summary plus document. One that scans through your entire book and summarizes each chapter one by one with just the key details from that scene like uh like it gives a a one paragraph summary of the scene. It gives the list of characters that are in the scene and any descriptors of that character, what happens to them and a few other details like that. And it condenses the amount of text that is used or it condenses the entire book into something that's much more manageable for the AI to understand. And it also signposts everything so the AI can quickly find what it's looking for, [gasps] which is much better than just trying to dump the whole book in there and just hoping that it knows everything that's in the book, which even though it's supposedly in its context window, that's not really how it works. The bigger the context, the more it has to sift through, the worse it gets at actually identifying relevant details that it needs for the scene. So, this is why I tell people that you should try to minimize your context. Try to keep it under 50,000 tokens if you can because that's just going to result in a higher quality output because of that. 

*Quick pause. If you're an author who wants to start writing more books, I put together my complete AI prompt pack that helped me and many others in my community write a book in a month. It's completely free. Hit the link in the description. Join the free weight list for StoryHacker Gold. Then you just answer a couple quick questions and I'll send you the full prompt list plus a few extra free goodies. I'll also email you when I open the paid Story Hacker Gold group so you can join if it feels right. There's no commitment to join, though, and you'll still be able to get all of the freebies you signed up for either way. All right, back to the video.*

### 3. Narrative Physics (Sliders)
All right, the third major prompting technique is one I'm kind of excited about and kind of a new one, too. Uh, this was first Future Fiction Academy came up with this idea that they call narrative physics. And I've expanded on it a little bit to where I think of it as sliders or you can think of it as game stats for different aspects of your world. Now, this is still just a prompting technique. There's really nothing crazy about it, but I'll give you an example of how this looks. And in the future, I'll probably make a whole video getting going deep on one or more of these techniques, but uh here's the idea. 

If you have a character, let's say you have a character bio for a character that's in your book, and you include that character bio in every scene that that character shows up in. Well, what if that character changes across the course of the story? And what if their emotions are in the same in a different place so that they react differently? Like you might have a character who is normally a very nice person but under a massive amount of stress might break and like kill somebody, you know, like under the right circumstances. I feel like there's a a joke there from like the Dark Knight and the Joker that if you just give people a little push, they'll do anything, right? That's this idea that people behave differently in different situations. 

And so what I came up with and this the while the concept of these narrative physics is something that feature fiction academy came up with. I have not seen any of their prompts. I have no idea how they do what they do. I came up with my own based on their concept. And the way I came up with it was this idea of sliders. [snorts] Um, so for every character, I will now give them sliders for things like stress to uh harmony uh or or peace, right? And if they're like uh a number 10 on the harmony side, there might actually be like two harmonious and a little bit too out of it, like maybe they're on drugs or something. Uh, but if they go all the way to the other side of the slider, like a -10 on the stress side, they're like so stressed, they're having a panic attack, they're they're literally on the verge of dying. Um, whereas we can pick somewhere in the middle is where their baseline is. And then for each scene, we can get the AI to identify, okay, where are they still at their baseline or have they moved up or down from that baseline. And what this does is is it allows the characters to shift and react more realistically to the scene. And so this is an excellent technique to get a little bit more variation about your character so they don't always sound monotone and the same all the time. 

It's also an excellent technique if you use something similar for say you have a magic system, right? How does what are the rules of that magic system? How does it work? What are the costs? All of that. making sure you you establish all of those things in almost a computer-like or gamelike way with actual numbered stats and things like that that can then change and evolve over the course of the book. You can even do this with certain emotions that you want to get across inside of the of the story, like the amount of tension that's in a scene. You know, what's that look like on a slider, right? uh or the amount of uh spiciness in a scene. What's that look like on a slider? Right? Sometimes you're going to have zero spiciness because the characters hate each other or something like that. Some sometimes you're going to have like in a romance you'll have it go up and down, up and down and up and down, but slowly getting bigger and bigger and then suddenly like bam, right? Uh you can take it all the way to a number 10, which would be like pornographic erotica, right? 

Um, so that's the kind of thing we're talking about here is different sliders, different ways of telling the AI this is the sort of tension that we're looking for. This is where the character is at in terms of their own sliders and so on. And so this is a really cool technique that I'm excited to be playing with more in the future. 

### 4. Layering
All right, the last technique that I really want to talk about is for lack of a better term, I'm just calling calling it layering. All right. And this is the idea that we can actually utilize multiple strengths of multiple different LLMs in one batch. And rather than just choosing one LLM to give us everything that we want it to give us, we can take it in steps and use different LLMs for each step. This not only allows us to play to the strengths of the LLM, but it also allows us to kind of avoid some of the sameness that we get from any one LLM. For instance, I love the Claude models. I love Claude 4.6 Opus, which is the most recent one as I'm recording this. And but when I work with it too long, it starts to all sound a very similar kind of tone all the way through. This layering technique allows us to mix it up a little bit and make it a little bit better. 

So what would this look like in practice? So for instance, the Gemini and the chat GBT models tend to be really good at uh logical thinking and structuring things. And so maybe we could start out by having them look at the information we provided about the scene and say, "Okay, let's expand this and create a scene brief." And so it creates the scene brief along with all the little things that we need it to have. And then uh we know Grock is really good at dialogue. So then maybe we could pass the scene brief over to Grock and be like, "Can you create a dialogue only draft of this and just put in little placeholders with a little bit of blocking for what happens in between the dialogue?" And then from there, we pull it over to let's say Gemini. And uh Gemini is pretty good at pros overall, but uh not as good at other things. So we can say, "Write all the pros, you know, fill in all the pros for this. identify the chill scenes and write all the pros for this stuff. And uh then we pass it over to Claude Opus 4.6 and be like, "You're really good at writing really serious, dramatic, climactic scenes. go through anything that's left in this scene and write in those little bits and uh and bringing all bring it all together so that now you have a chapter that's been gone over by like four or five different LLMs all providing what makes them unique to them and you end up with a chapter that is absolutely mindblowing compared to what you would get if you just went to Claude or Gemini and asked it to write the whole chapter in one go. 

This is a really powerful technique that I think a lot of people aren't utilizing. It does admittedly increase your costs of being able to do this. Um, especially if you're using an API, it's going to take more, especially if you're doing this in like an automation type of format. It's going to take a lot more money to do that. But if that isn't an issue for you, this could be an incredible way to get really, really good results out of your LLM, especially if you combine it with the context engineering and the checks and critiques and the uh narrative physics and the sliders. You combine all of these together, you're going to get some pretty fantastic results. 

### Conclusion
Uh, so these are some four pretty advanced tools that I think are really helpful for you if you want to get access to a lot of my stuff, uh, including all of my automations that get into this sort of thing that I'm currently building as we speak. Um, you can access the story hacker gold group down below. And if it's on the waiting list when you join, you'll actually get a whole bunch of my prompts all for free that you'll that'll just be sent to your email when you join the wait list. And then you can, you know, join the story hacker gold group when it opens more publicly.
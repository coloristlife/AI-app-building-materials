如果把动态渲染比作“现场炒菜”，那么 **SSG / Static Rendering（静态站点生成 / 静态渲染）** 就是 Next.js 性能强悍的**真正底牌**。

它是 Next.js 的**默认渲染模式**。只要一个页面具备静态渲染的条件，Next.js 就会毫不犹豫地把它做成静态文件。

---

### 1. 什么是静态渲染（Static Rendering / SSG）？

**静态渲染**是指：在你在电脑或服务器上运行 `npm run build` 打包的那一刻，Next.js 就去执行代码、查数据库，并把这个页面渲染成一个**完全做好的静态 HTML 文件和数据快照**，直接存到磁盘上。

当后续无论 1 个用户还是 1,000,000 个用户访问这个网址时，服务器**连代码都不需要重新运行**，直接把这个做好的 HTML 文件丢给用户。

---

### 2. 为什么它是性能与 SEO 的“天花板”？

1.  **全球 CDN 极速分发（秒开）：** 静态 HTML 文件可以轻松分发到全球的 CDN 节点（比如离用户最近的边缘服务器）。无论用户在东京、纽约还是北京，打开网页的时间通常只有 **几毫秒到几十毫秒**。
2.  **服务器零开销（省钱）：** 服务器不需要在每次访问时去跑复杂的 JavaScript，也不需要去查数据库，CPU 占用率接近 0。
3.  **SEO 满分：** 百度/谷歌爬虫一来，看到的就是完整、干净、带标题和内容的成品 HTML，权重极高。

---

### 3. 核心大招：动态路由怎么做静态渲染？（`generateStaticParams`）

这里有个常见的疑问：

> *“对于普通页面 `/about`，打包做成静态 HTML 很简单。但如果是动态路由 `/blog/[slug]`，打包时 Next.js 怎么知道有哪几篇文章、该生成哪些静态 HTML 呢？”*

这时候就需要用到 Next.js 专门提供的神级函数：**`generateStaticParams`**。

它专门用来在打包时告诉 Next.js：“**请提前帮我把这几篇文章生成好静态 HTML！**”

```tsx
// app/blog/[slug]/page.tsx
import prisma from '@/lib/prisma';

// 1. 告诉 Next.js：打包时去数据库里把所有的 slug 查出来，提前生成静态 HTML！
export async function generateStaticParams() {
  const posts = await prisma.post.findMany({
    select: { slug: true },
  });

  // 返回格式必须是数组：[{ slug: 'post-1' }, { slug: 'post-2' }]
  return posts.map((post) => ({
    slug: post.slug,
  }));
}

// 2. 页面组件
export default async function BlogPostPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const post = await prisma.post.findUnique({ where: { slug } });

  return (
    <article className="p-8">
      <h1>{post?.title}</h1>
      <p>{post?.content}</p>
    </article>
  );
}
```

**运行 `npm run build` 时发生了什么？**
Next.js 会先运行 `generateStaticParams`，假如有 100 篇文章，它就会在后台**一次性把这 100 篇文章全部做成 100 个静态 HTML 文件**！
当读者打开任何一篇文章时，都是从 CDN 瞬间秒开！

---

### 4. 两种触发静态渲染的方式

#### ① 自动触发（默认）
只要你的页面里**没有使用**任何动态信号（没有 `cookies()`、没有 `headers()`、没有 `searchParams`、没有未缓存请求），Next.js 就会在打包时**自动**把该页面设为 Static Rendering。

#### ② 手动强制触发
如果你想显式声明这个页面必须是静态的：
```tsx
// app/about/page.tsx

// 强制静态渲染！如果页面里误写了动态代码，打包时会报错提醒你
export const dynamic = 'force-static';

export default function AboutPage() {
  return <div>关于我们</div>;
}
```

---

### 5. 静态渲染的“终极进化体”：ISR（增量静态再生）

很多初学者觉得：“静态渲染好是好，但内容死了不能变啊。”

 Next.js 提出了著名的 **ISR（Incremental Static Regeneration）** 概念：

> **“既要静态渲染的秒开速度，又要有动态渲染的更新能力。”**

通过配合我们前面学的 `revalidate`：
```tsx
// 既是在打包时生成了静态 HTML（秒开），
// 又能在后台每隔 60 秒自动更新一次静态 HTML（保持新鲜）！
fetch('https://...', { next: { revalidate: 60 } })
```

---

### 💡 静态渲染 vs 动态渲染 终极速查表

| 维度                 | 静态渲染 (SSG / Static)           | 动态渲染 (Dynamic)                                |
| :----------------- | :---------------------------- | :-------------------------------------------- |
| **渲染时间点**          | **打包时 (Build Time)**          | **用户访问时 (Request Time)**                      |
| **访问速度**           | ⚡⚡⚡ 极致秒开 (几毫秒)                | ⚡ 依赖服务器计算时间 (几百毫秒)                            |
| **数据源**            | 相对稳定（博客、官网、产品展示）              | 频繁变动 / 个人隐私（购物车、后台）                           |
| **底层标识 (Build输出)** | `○ (Static)`                  | `ƒ (Dynamic)`                                 |
| **如何使用**           | 默认开启 / `generateStaticParams` | 用了 `cookies()`/`searchParams`/`force-dynamic` |


# 为什么headers() 是动态信号


这个问题问到了 HTTP 协议和 Web 渲染的核心底层！

为什么只要在 Next.js 里一写 `headers()`，页面就会被**强制切到动态渲染（Dynamic Rendering）**？

一句话核心原因：**因为 HTTP 请求头（Headers）里的数据，只有在“真实用户发起访问的那一整个瞬间”才会产生。在打包（Build）阶段，服务器根本无法预知未来的用户会带着什么请求头过来！**

---

### 1. HTTP 请求头（Headers）里到底藏着什么？

当你的浏览器向服务器发送请求时，会偷偷附带一份**“用户的随身身份档案”**，这就是 Headers。里面包含了：

*   **`User-Agent`**：用户的设备型号（是 iPhone 15？还是 Windows 电脑？还是微信内置浏览器？）。
*   **`Accept-Language`**：用户的浏览器语言偏好（是 `zh-CN` 中文？还是 `en-US` 英文？）。
*   **`Authorization`**：用户的身份令牌（Token/密钥）。
*   **`X-Forwarded-For`**：用户的真实 IP 地址和网络地理位置。

---

### 2. 为什么打包时（Build Time）做不了？

回想一下我们前面讲的**静态渲染（SSG）**：
静态渲染要求在运行 `npm run build`（打包那一天）就把 HTML 页面完全拼好、做成死文件存起来。

假设你的代码里写了这样一段逻辑：

```tsx
import { headers } from 'next/headers';

export default async function Page() {
  const headersList = await headers();
  const userAgent = headersList.get('user-agent');

  // 如果是手机访问，展示简版界面；如果是电脑访问，展示豪华界面
  const isMobile = userAgent?.includes('Mobile');

  return (
    <div>{isMobile ? '手机版界面' : '电脑版界面'}</div>
  );
}
```

**Next.js 在打包时遇到了巨大难题：**
在 `npm run build` 打包的那一时刻，**根本没有真实用户在访问网站**！
Next.js 怎么可能提前知道未来第一个访问网站的人是用 iPhone 还是用电脑？怎么可能提前知道他的 IP 地址是北京还是纽约？

**因此，Next.js 只能得出唯一的结论：**
> *“既然这个页面需要根据访问者的手机型号、IP 地址或语言偏好来决定渲染什么内容，那我**绝不能在打包时把它做成固定的静态 HTML**。我必须等到用户真正敲网址访问的那一刻，拿到他的 HTTP Headers，现场读取、现场生成 HTML（动态渲染）！”*

---

### 3. 大白话比喻：“机场海关查护照”

*   **静态渲染（SSG）：** 相当于电影院提前印好了 10,000 张门票。无论谁来买票，拿到的都是一模一样的印好座位的门票。
*   **`headers()` 动态渲染：** 相当于**机场海关检查护照**。
    海关官员（服务器）不可能在旅客到达之前，就把护照盖章（渲染 HTML）给准备好。海关官员必须等旅客（用户）**亲自站在柜台前，把护照（HTTP Headers）递过来**的那一秒，现场看护照信息，现场决定是否盖章放行（现场动态渲染）。

---

### 总结

在 Next.js 中，只要你的代码试图去读取那些**“因人而异、因请求而异”**的信息（如 `cookies()`、`headers()`、`searchParams`），Next.js 就会自动判定这个页面无法提前做成通用静态文件，从而自动开启 **Dynamic Rendering（动态渲染）**。
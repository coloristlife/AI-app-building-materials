在 Web 开发中，并不是每一个网址都能提前写死。

比如电商网站有几万个商品（`/product/1`、`/product/2`...），或者博客有成千上万篇文章（`/blog/hello`、`/blog/nextjs`...）。你不可能在文件夹里建几万个子文件夹。

这时候，就需要用到 **动态路由（Dynamic Routes）**，以及随之而来的两个核心概念：**`params`（路径参数）** 与 **`searchParams`（查询参数）**。

---

### 1. 核心概念对比：`params` vs `searchParams`

用一句话区分它们：

*   **`params`（路径参数）**：网址路径的一部分，用来决定**“看哪一个具体资源”**。
    *   例如：`/product/123` 里的 `123`。
*   **`searchParams`（查询参数）**：网址末尾 `?` 后面跟着的内容，用来决定**“怎么看这个资源（排序、筛选、页码）”**。
    *   例如：`/product/123?color=red&size=XL` 里的 `color=red` 和 `size=XL`。

---

### 2. 如何创建动态路由（使用 `[方括号]`）

在 Next.js 的 App Router 里，创建动态路由极其直观：**把文件夹的名字用 `[方括号]` 包起来**。

#### 文件目录结构：
```text
app/
 └── blog/
      └── [slug]/          <-- 动态文件夹（slug 代表文章别名）
           └── page.tsx    <-- 对应的页面
```

这个 `[slug]` 就像是一个**通配符占位符**。
*   用户访问 `/blog/hello-world` ➔ 匹配 `app/blog/[slug]/page.tsx`
*   用户访问 `/blog/react-guide` ➔ 同样匹配 `app/blog/[slug]/page.tsx`

---

### 3. 在服务端组件中使用 `params` 与 `searchParams`（⚠️ Next.js 15+ 重磅变化）

> 🚨 **注意**：在最新的 Next.js 15 及更高版本中，为了提升性能，`params` 和 `searchParams` 被升级为了 **Promise（异步承诺）**！在你读取它们之前，**必须使用 `await` 展开它们**。

让我们看一个标准的服务端组件代码：

```tsx
// 访问网址：http://localhost:3000/blog/nextjs-tutorial?lang=zh&page=2

type Props = {
  // 定义类型：在 Next.js 15+ 中，它们都是 Promise
  params: Promise<{ slug: string }>;
  searchParams: Promise<{ lang?: string; page?: string }>;
};

export default async function BlogPostPage({ params, searchParams }: Props) {
  // 1. 使用 await 拿到具体的路径参数 (params)
  const { slug } = await params; // slug 的值是 "nextjs-tutorial"

  // 2. 使用 await 拿到问号后面的查询参数 (searchParams)
  const { lang, page } = await searchParams; // lang 是 "zh", page 是 "2"

  return (
    <main className="p-10">
      <h1>文章别名 (params): {slug}</h1>
      <p>当前语言 (searchParams): {lang}</p>
      <p>当前页码 (searchParams): {page}</p>
    </main>
  );
}
```

---

### 4. 如果是在客户端组件（`'use client'`）里怎么拿？

在标记了 `'use client'` 的客户端组件中，你不需要通过页面属性传递，Next.js 提供了 **两个专属的 Hook 轮子**：

```tsx
'use client';

// 引入 Next.js 专属 Hook
import { useParams, useSearchParams } from 'next/navigation';

export default function ClientComponent() {
  // 1. 获取路径参数 params
  const params = useParams(); // 例如: { slug: 'nextjs-tutorial' }
  
  // 2. 获取查询参数 searchParams
  const searchParams = useSearchParams();
  const lang = searchParams.get('lang'); // 拿到 'zh'
  const page = searchParams.get('page'); // 拿到 '2'

  return (
    <div>
      <p>客户端拿到的 slug: {params.slug}</p>
      <p>客户端拿到的 lang: {lang}</p>
    </div>
  );
}
```

---

### 5. 进阶动态路由语法（补充速查）

除了单层 `[slug]`，Next.js 还支持更高级的文件夹命名捕获：

| 文件夹语法 | 匹配的网址示例 | `params` 拿到的对象结构 | 适用场景 |
| :--- | :--- | :--- | :--- |
| **`[id]`** (单层捕获) | `/goods/100` | `{ id: '100' }` | 商品详情页、博客详情页 |
| **`[...slug]`** (多级捕获 Catch-all) | `/docs/v1/install/mac` | `{ slug: ['v1', 'install', 'mac'] }` | 文档系统、多级分类菜单 |
| **`[[...slug]]`** (可选多级捕获) | `/docs` 或 `/docs/a/b` | `{}` 或 `{ slug: ['a', 'b'] }` | 首页和深层页面用同一个文件 |

---

### 💡 总结 Cheat Sheet

1.  **想做动态网址？** 给文件夹加方括号 `app/posts/[id]/page.tsx`。
2.  **`params` 是什么？** 网址里的核心路径（`/posts/123` 里的 `123`），用来代表**“是谁”**。
3.  **`searchParams` 是什么？** 网址问号后面的过滤条件（`?sort=new`），用来代表**“怎么展示”**。
4.  **在 Next.js 15 页面里怎么用？** 它们都是 Promise，必须 `await params` 和 `await searchParams`！


# 文件夹命名

*   从**操作系统（硬盘文件）**的角度看：它就是**真实的文件夹名称**（你必须在电脑里创建一个带有方括号的文件夹，名字就叫 `[slug]`）。
*   从 **Next.js 框架**的角度看：它是你给动态路由定义的**变量占位符（Placeholder / Variable）**。

---

### 1. 方括号 `[ ]` 与内部名字的奥秘

你可以把 `[slug]` 拆成两部分来理解：

1.  **外面的方括号 `[ ]` —— 魔法开关**
    告诉 Next.js：“注意！这个文件夹不是一个固定网址，而是一个**占位符（Placeholder）**，凡是这一层的网址，全都由我来接管！”
2.  **里面的单词 `slug` —— 变量名（Key）**
    这是你**自定义的变量名字**。你在方括号里写什么，代码里的 `params` 对象就会用什么 key 来接收数据。

---

### 2. 拿具体的例子对比一下：

#### 情况 A：你把文件夹命名为 `[slug]`
*   **磁盘路径**：`app/blog/[slug]/page.tsx`
*   **用户访问**：`/blog/learn-nextjs`
*   **代码里拿到的对象**：`params.slug` 等于 `'learn-nextjs'`

#### 情况 B：你把文件夹命名为 `[id]`
*   **磁盘路径**：`app/blog/[id]/page.tsx`
*   **用户访问**：`/blog/12345`
*   **代码里拿到的对象**：`params.id` 等于 `'12345'`

#### 情况 C：你把文件夹命名为 `[article_title]`
*   **磁盘路径**：`app/blog/[article_title]/page.tsx`
*   **用户访问**：`/blog/hello`
*   **代码里拿到的对象**：`params.article_title` 等于 `'hello'`

---

### 3. 补充一个小知识：为什么大家都喜欢用 `slug` 这个单词？

初学者经常被 `slug` 这个英文单词搞懵。其实 `slug` 是出版业和 Web 开发里含义非常具体的一个**行业术语**：

*   **`id`**：通常指纯数字的数据库主键，比如 `/article/8832`。
*   **`slug`**：特指**为了 SEO 优化、用连字符 `-` 连接的可读性网址文本**。
    *   例如文章标题是《Next.js 极速入门》，它的 slug 通常会写成 `nextjs-quick-start`。
    *   网址就会变成 `/blog/nextjs-quick-start`（这对搜索引擎极其友好，比乱码或纯数字排名更高）。

所以，`[slug]` 只是社区最习惯使用的文件夹命名范例，你完全可以根据自己的喜好把它改叫 `[id]` 或 `[productId]`！




Next.js 的**缓存机制（Caching）**是它性能超越绝大多数前端框架的核心秘密武器，但也曾经是初学者觉得最“玄学”、最容易踩坑的地方。

值得庆幸的是，在最新的 **Next.js 15 / 16** 中，官方监听了社区反馈，做了一个极重大的改变：**默认不再强行缓存数据（Uncached by Default）**！这让缓存变得极其透明、可控。

我们用最通俗的方式，拆解 Next.js 的缓存机制。

---

### 1. 数据的三种缓存模式（控制 `fetch`）

现在，当你使用 `fetch()` 请求外部接口或数据时，你可以明确告诉 Next.js 你想要哪种缓存策略：

#### ① 实时模式（默认 / `no-store`）：永远拿最新数据
如果你不写任何缓存配置，或者明确写上 `cache: 'no-store'`，Next.js 每次收到请求都会去重新拉取数据。
*   **适用场景：** 股票价格、用户实时余额、聊天消息。
```typescript
// 每次访问都重新请求，确保数据 100% 最新
const res = await fetch('https://api.example.com/stock', { 
  cache: 'no-store' 
});
```

#### ② 永久静态缓存（`force-cache`）：打包时拿一次，永久保存
如果你希望把数据当成静态资源，打包（Build）时请求一次后就再也不更新。
*   **适用场景：** 隐私政策、关于我们、历史归档文章。
```typescript
// 永久缓存数据，请求速度极快（毫秒级）
const res = await fetch('https://api.example.com/privacy', { 
  cache: 'force-cache' 
});
```

#### ③ 定时增量刷新（ISR / `revalidate`）：隔一段时间刷新一次
这是 Next.js 最绝杀的功能！叫 **增量静态再生（ISR）**。
你可以设置一个时间（比如 60 秒）。在 60 秒内，所有用户访问看到的都是高速缓存；60 秒后，第一个访问的用户会触发后台静默刷新，随后的用户就能看到最新数据。
*   **适用场景：** 电商商品列表、博客首页、新闻列表。
```typescript
// 每 60 秒在后台自动刷新一次缓存
const res = await fetch('https://api.example.com/posts', { 
  next: { revalidate: 60 } 
});
```

---

### 2. 如何手动精准清空缓存？（Cache Invalidation）

假设你设置了定时缓存 1 小时，但管理员刚刚在后台发布了一篇紧急通告，等不及 1 小时了，怎么**立刻清空缓存**？

在 Server Actions 或 API 接口里，Next.js 提供了两个“清缓存大招”：

#### 方案 A：按页面路径清空 `revalidatePath`
```typescript
import { revalidatePath } from 'next/cache';

async function updatePost() {
  'use server';
  // 修改数据库...
  
  // 告诉 Next.js：“立刻清空 /blog 这个页面的所有缓存，重新渲染！”
  revalidatePath('/blog');
}
```

#### 方案 B：按标签清空 `revalidateTag`（更高级、更精准）
你可以在请求时给数据打上“标签（Tag）”，清空时只清空带这个标签的数据：
```typescript
// 1. 请求时打上标签 'posts-data'
fetch('https://api.example.com/posts', { 
  next: { tags: ['posts-data'] } 
});

// 2. 在 Server Action 里精准按标签爆破缓存
import { revalidateTag } from 'next/cache';

async function createPost() {
  'use server';
  // 插入数据库...
  
  // 只清空带 'posts-data' 标签的缓存，其他无关页面的缓存不受影响
  revalidateTag('posts-data');
}
```

---

### 3. 一图看懂：Next.js 的“四层缓存大厦”

除了你自己控制的数据缓存外，Next.js 还在后台默默为你运行着 4 个不同层级的缓存（心智模型）：

```text
[ 用户点击网页 ] 
       │
       ▼
1. 客户端路由缓存 (Router Cache) ──▶ (浏览器内存中，短暂停留，防止重复渲染)
       │
       ▼
2. 全局静态页面缓存 (Full Route Cache) ──▶ (服务器直接返回预先编译好的 HTML)
       │
       ▼
3. 数据缓存 (Data Cache) ──▶ (跨请求、跨用户共享的 fetch/数据库结果)
       │
       ▼
4. 请求去重 (Request Memoization) ──▶ (同一次页面渲染中，重复的 fetch 自动合并为 1 次)
```

1.  **请求去重（Request Memoization）：** 如果你在一个页面的顶部、中部、底部都写了 `fetch('/api/user')`，React 会极其聪明地**只向服务器发 1 次请求**，另外两次自动复用结果。
2.  **数据缓存（Data Cache）：** 就是我们第一点讲的 `force-cache` 或 `revalidate`，保存在服务器硬盘/内存里。
3.  **全页面缓存（Full Route Cache）：** Next.js 在打包时直接把某些静态页面编译成了死 HTML 文件。
4.  **客户端路由缓存（Router Cache）：** 当你在页面间点 `<Link>` 跳转时，浏览器会把访问过的 RSC 载荷在内存里存几秒钟，当你点“后退”按钮时，瞬间呈现，零等待。

---

### 💡 总结给初学者的黄金法则

1.  **不用怕乱缓存：** 在 Next.js 15/16 中，默认的数据请求**不缓存**，数据改了页面立马变，不会再出现“明明改了数据库页面就是不更新”的困扰。
2.  **需要性能提升时：** 给不需要频繁变动的数据加上 `{ next: { revalidate: 3600 } }`（比如 1 小时刷新一次）。
3.  **用户提交修改后：** 在 Server Action 里面加一句 `revalidatePath('/你的页面')`，瞬间刷新最新界面。


# 标签（Tags）

回答这个问题的核心在于：**标签（Tags）不是 Next.js 自动生成的，它完全是由你（开发者）自己起的名字和定义的！**

Next.js 内部有一个专门的 **“缓存索引字典”**。
当你给 `fetch` 打上标签时，Next.js 就默默在后台把**你的这个标签名**和**那份缓存数据**绑在一起；当你调用 `revalidateTag` 时，Next.js 就会拿着这个名字去字典里搜，把对应的缓存全部作废。

下面为你拆解：**Next.js 是怎么知道的？以及我们在实际项目中该怎么规范地管理这些标签？**

---

### 1. 它是怎么绑定的？（Next.js 的内部账本）

整个过程分为三步：

1.  **你贴标签（注册）：**
    你在获取数据时写了 `next: { tags: ['posts-data'] }`。
     Next.js 在服务器里存下这份数据，并在账本上记下一笔：
    > *“账本记录：数据 A（文章列表）关联的标签是 `posts-data`。”*
2.  **你撕标签（刷新）：**
    当用户发表了新文章，你在 Server Action 里调用了 `revalidateTag('posts-data')`。
3.  **Next.js 查账本（撕毁）：**
    Next.js 收到指令，去账本里翻找：“谁身上贴了 `posts-data`？” 找到数据 A，立刻把数据 A 清空！

---

### 2. 那如果不用 `fetch`，用 Prisma 查数据库怎么打标签？

前面我们学过，在 Next.js 里可以直接用 `prisma.post.findMany()` 查数据库。
但 `prisma` 并没有 `fetch` 里的 `next: { tags: [...] }` 选项，**那怎么给 Prisma 查出来的数据打标签呢？**

Next.js 专门提供了一个叫 **`unstable_cache`** 的函数，用来给**任何非 fetch 的数据（比如 Prisma）**打包打标签：

```typescript
// lib/data.ts
import { unstable_cache } from 'next/cache';
import prisma from '@/lib/prisma';

// 用 unstable_cache 把 Prisma 查询包裹起来
export const getCachedPosts = unstable_cache(
  async () => {
    return await prisma.post.findMany(); // 真实的数据库查询
  },
  ['posts-list-internal-key'], // 参数1：内部唯一的 Key
  { 
    tags: ['posts-data'] // 参数2：你自己起的名字！打上标签！
  }
);
```

这样，你在页面里调用 `getCachedPosts()` 时，数据就被打上了 `'posts-data'` 标签！
之后你只要执行 `revalidateTag('posts-data')`，Prisma 的缓存也会被精准清空！

---

### 3. 实战避坑：项目大了，怎么知道有哪些标签？（最佳实践）

初学者最容易踩的坑就是**拼写错误**！
比如在页面里打了标签 `'posts-data'`（带 s），结果在 Server Action 清缓存时手滑写成了 `'post-data'`（没带 s）。
Next.js 查账本找不到 `'post-data'`，**缓存就不会清空**，你还不报错，找 BUG 找到头秃。

#### 💡 行业标准解决方案：建立全局“标签字典”文件

在项目里专门建一个 `lib/constants.ts` 文件，集中管理所有的标签名，绝不手写字符串！

```typescript
// lib/constants.ts (全局标签字典)

export const CACHE_TAGS = {
  // 静态标签
  POSTS_LIST: 'posts:list',
  CATEGORIES: 'categories:all',

  // 动态标签函数（针对特定 ID 的数据）
  POST_DETAIL: (id: string | number) => `post:${id}`,
  USER_PROFILE: (userId: string) => `user:${userId}`,
};
```

#### 在代码里优雅地使用：

**1. 打标签时：**
```typescript
import { CACHE_TAGS } from '@/lib/constants';

fetch('https://api.example.com/posts', {
  next: { tags: [CACHE_TAGS.POSTS_LIST] } // 使用字典里的变量
});
```

**2. 针对特定文章打标签：**
```typescript
fetch(`https://api.example.com/posts/${id}`, {
  next: { tags: [CACHE_TAGS.POST_DETAIL(id)] } // 生成比如 'post:123' 的专属标签
});
```

**3. 清缓存时：**
```typescript
import { revalidateTag } from 'next/cache';
import { CACHE_TAGS } from '@/lib/constants';

async function updatePost(id: string) {
  'use server';
  // 修改数据库...

  // 1. 只清空这篇文章自己的缓存！
  revalidateTag(CACHE_TAGS.POST_DETAIL(id)); 

  // 2. 顺便清空整张文章列表的缓存！
  revalidateTag(CACHE_TAGS.POSTS_LIST); 
}
```

---

### 总结

1.  **谁知道标签？** Next.js 知道，因为它在后台维护了一个“标签 ➔ 缓存”的映射账本。
2.  **标签谁定的？** 你定的！想怎么起名就怎么起名。
3.  **Prisma 怎么用？** 用 `unstable_cache` 包起来打标签。
4.  **防拼错秘诀：** 建立全局 `CACHE_TAGS` 常量文件，统一管理所有标签名，告别拼写错误！

# 默认换成行为

在最新的 Next.js（Next.js 15 / 16 及更新版本）中，默认的缓存行为哲学已经全面转向：

👉 **“默认不缓存，按需开启（Uncached by Default）”**

我们可以把 Next.js 在**不写任何特殊配置**时的默认行为，分为以下 4 种具体场景：

---

### 1. 数据请求（`fetch`）：**默认 100% 不缓存**

当你在代码里直接写 `await fetch('https://api.example.com/data')` 时：

*   **默认行为**：效果等同于隐式加了 `{ cache: 'no-store' }`。
*   **实际表现**：每次用户刷新页面或发送请求，Next.js 都会实时跑去目标 API 拉取最新的数据。
*   **好处**：彻底消除了过去“明明修改了数据库，页面却死活显示旧数据”的困扰。

---

### 2. API 接口（`route.ts` GET 请求）：**默认 100% 不缓存**

当你在 `app/api/user/route.ts` 里写了一个 `export async function GET()` 接口时：

*   **默认行为**：默认是**动态接口（Dynamic）**。
*   **实际表现**：每次外部访问 `http://.../api/user`，服务端都会重新运行这个 GET 函数并返回最新的 JSON。

---

### 3. 页面渲染（Page Rendering）：**自动判断“静态”或“动态”**

对于整个 `page.tsx` 页面，Next.js 会根据你在页面里用了什么代码，**智能二选一**：

#### 🅰️ 如果你的页面是“纯静态”的：
如果页面里没有使用任何个人数据、没有问号参数、没有 Cookies：
*   **默认行为**：自动识别为 **静态页面（Static Route）**。
*   **实际表现**：Next.js 在执行 `npm run build` 打包时，会直接把这个页面编译成一个**死 HTML 文件**缓存起来。以后所有用户访问，都极速返回这个编译好的 HTML。

#### 🅱️ 如果你的页面用到了“动态数据”：
只要你的页面代码里包含了以下任意**“动态信号”**：
1. 使用了 `cookies()` 或 `headers()`
2. 使用了 `searchParams`（网址问号参数）
3. 使用了默认的未缓存 `fetch()`
4. 使用了直接查数据库的 Prisma 代码

*   **默认行为**：自动切换为 **动态页面（Dynamic Route）**。
*   **实际表现**：每次有用户访问该网址，服务器都会**现场重新计算、现场查库、现场拼接 HTML** 发给用户。

---

### 4. 客户端页面跳转缓存（Router Cache）：**默认 0 秒（实时刷新）**

当用户在浏览器里点击 `<Link href="/about">` 跳转页面时：

*   **默认行为**：对于动态页面，客户端内存缓存时间（`staleTime`）**默认是 0 秒**。
*   **实际表现**：用户每次点击链接跳转，Next.js 都会向服务器请求最新的页面数据，确保用户看到的永远是最新的界面（不会因为退回上页看到旧缓存）。

---

### 💡 总结 Cheat Sheet

如果你什么额外的缓存代码都不写，Next.js 的默认状态是：

1.  **数据 Fetch** ➔ 每次都拉最新的（不缓存）。
2.  **API 接口** ➔ 每次都重新跑（不缓存）。
3.  **有动态数据的页面** ➔ 每次访问都现场生成（不缓存）。
4.  **毫无变化的纯静态页面** ➔ 打包时编译成 HTML（自动永久静态缓存）。

**一句话：现代 Next.js 的默认态度是“保新鲜”。只有当你觉得某个数据太慢、想提高性能时，你才手动去加 `revalidate: 60` 或 `cache: 'force-cache'` 开启缓存！**



# 内部唯一的身份证号（Cache Key）
```
['posts-list-internal-key'], // 参数1：内部唯一的 Key这句是什么意思
```
这行代码是 `unstable_cache` 函数的核心参数之一。

简单直接地说：**这行代码是给这份缓存数据在服务器里起一个“内部唯一的身份证号（Cache Key）”。**

---

### 1. 为什么必须给它一个“身份证号”？

我们对比一下就明白了：

*   **用 `fetch()` 时：**
    `fetch('https://api.example.com/posts')`
    Next.js 自动拿请求的**网址 URL** 作为这份缓存的唯一身份证号。
*   **用 Prisma 查数据库时：**
    `async () => prisma.post.findMany()`
    这只是一段普通的 JavaScript 代码，**没有任何网址**。如果不传名字，Next.js 的缓存系统根本不知道该把这段代码查出来的结果存在哪、叫什么名字。

所以，你必须手动给它一个字符串数组 `['posts-list-internal-key']`，告诉 Next.js：
> **“请把这段 Prisma 代码查出来的结果，存到名字叫 `posts-list-internal-key` 的保险柜里！”**

---

### 2. 最容易混淆的点：它和后面的 `tags` 有什么区别？

很多初学者会懵：“前面有个 key，后面又有个 `tags`，它们俩不都是名字吗？”

用**快递柜**打个比方，你就彻底通透了：

| 概念 | 代码位置 | 比喻 | 规则 | 作用 |
| :--- | :--- | :--- | :--- | :--- |
| **Key (参数1)** | `['post-101-key']` | **快递柜的柜门号** (如 101号柜) | **必须唯一！** 不能重复 | 告诉 Next.js 应该去哪个具体位置存取数据，防止覆盖别的缓存。 |
| **Tag (参数3)** | `tags: ['article-tag']` | **贴在柜门上的彩色贴纸** | **可以共享！** 多份缓存可以贴同一个标签 | 告诉你（开发者）将来喊 `revalidateTag` 时，可以按颜色批量清空哪些柜子。 |

---

### 3. 实战栗子：如果带参数（如查单篇文章），这个 Key 怎么写？

如果你的查询是带动态参数的（比如根据文章 ID 查文章），**这个 Key 必须把 ID 包含进去**，保证每一个文章都有自己独立的“柜门号”：

```typescript
import { unstable_cache } from 'next/cache';
import prisma from '@/lib/prisma';

export const getPostById = (id: string) =>
  unstable_cache(
    async () => {
      return await prisma.post.findUnique({ where: { id } });
    },
    // 1. Key (柜门号)：必须把 id 动态放进去！
    // 这样文章 1 存进 ['post-detail', '1']，文章 2 存进 ['post-detail', '2']，绝不串套！
    ['post-detail-key', id], 
    
    // 2. Tag (贴纸)：可以都贴上 'posts-data'
    { tags: ['posts-data'] }
  )();
```

---

### 总结

`['posts-list-internal-key']` 就是 Next.js 数据缓存字典里的 **键（Key）**。

它保证了这段 Prisma 查询结果在 Next.js 的服务器硬盘里拥有一个**独一无二、不会跟其他查询混淆的“文件存储名”**。


===
```
export const getCachedPosts = unstable_cache(  
async () => {  
	return await prisma.post.findMany(); // 真实的数据库查询  
	},  
	['posts-list-internal-key'], // 参数1：内部唯一的 Key  
	{  
	tags: ['posts-data'] // 参数2：你自己起的名字！打上标签！  
	}  
);
```

> **“创建一个自带‘自动缓存’和‘标签打标’功能的数据库查询函数 `getCachedPosts`。”**

如果没有这段代码，你每次访问页面，Next.js 都会去连接数据库查一次；有了这段代码，Next.js 第一次查完数据库后，就会把结果**存进服务器内存/硬盘**里。下次再有人访问，**直接从缓存里拿，0 毫秒响应，完全不打扰数据库！**

我们把这段代码拆成 4 个模块来逐行解读：

---

### 1. 逐行拆解代码

```typescript
// ① 导出函数名：定义一个叫 getCachedPosts 的函数，供其他 page.tsx 引入使用
export const getCachedPosts = unstable_cache(

  // ② 【真正的查库逻辑】：告诉 Next.js 没缓存时去哪里拿数据
  async () => {
    return await prisma.post.findMany(); // 执行 Prisma 语句，去数据库查所有文章
  },

  // ③ 【保险柜钥匙/内部 Key】：这份缓存数据在 Next.js 服务器里的唯一存储位置
  ['posts-list-internal-key'], 

  // ④ 【标签选项】：给这份缓存贴上分类标签
  { 
    tags: ['posts-data'] // 方便以后用 revalidateTag('posts-data') 一键刷新它
  }
);
```

---

### 2. 在页面（`page.tsx`）里怎么使用它？

定义好之后，你在任何服务端组件里都可以像调用普通函数一样使用它：

```tsx
// app/posts/page.tsx
import { getCachedPosts } from '@/lib/data';

export default async function PostsPage() {
  // 1. 用户 A 访问：发现没有缓存 ➔ 执行里面的 Prisma 代码，去数据库查数据 ➔ 把结果存入缓存
  // 2. 用户 B 访问：发现有缓存 ➔ 直接从 Next.js 缓存里拿，压根不走 Prisma，0 毫秒出结果！
  const posts = await getCachedPosts();

  return (
    <ul>
      {posts.map(post => <li key={post.id}>{post.title}</li>)}
    </ul>
  );
}
```

---

### 3. 当数据更新时，缓存如何失效？

假设管理员在后台发表了新文章，调用了 Server Action：

```typescript
import { revalidateTag } from 'next/cache';

async function createNewPost() {
  'use server';
  await prisma.post.create({ ... }); // 写入数据库
  
  // 一句话！让上面那个 getCachedPosts 里的缓存立刻作废！
  // 下一个访问 /posts 页面的用户就会重新去查数据库，拿到最新的文章列表。
  revalidateTag('posts-data'); 
}
```

---

### 💡 顺便科普：为什么函数名叫 `unstable_cache`？

很多初学者看到 `unstable_`（不稳定的）会被吓一跳，以为这个功能很容易报错。

其实不是！在 Next.js 的命名习惯里：
*   **`unstable_`** 意思是：**“这个功能的核心逻辑很稳定，但官方未来可能会微调它的参数写法或名字。”**
*   因为原生 `fetch()` 自带缓存语法，但像 Prisma、Drizzle 这种直接连数据库的代码没有原生 `fetch`，所以 Next.js 官方专门提供了 `unstable_cache` 这个包装器轮子，给非 fetch 的数据加缓存。在目前的 App Router 开发中，它是给数据库查询做缓存的**标准标准做法**。

你的观察**极其敏锐！** 简直一下子抓住了很多开发者刚接触 Next.js 缓存时最疑惑的点。

你说得完全正确：**在后面的业务代码里（比如在 Server Action 或清缓存的代码里），我们确实再也不会去写 `posts-list-internal-key` 这个字符串。**

那么问题来了：既然我们自己不用它，凭什么强制要求我们传这个参数呢？

---

### 1. 答案：这个 Key 是写给“Next.js 框架自己”看的，不是写给我们写的！

我们再用**“图书馆存书”**的比喻来揭秘背后的真相：

*   **`posts-list-internal-key` (Key) ➔ 图书在书架上的“物理定位索书号（如：A-03-05）”**
    *   **使用者：** **Next.js 框架本身。**
    *   **作用：** 每次你调用 `getCachedPosts()` 时，Next.js 会拿着 `A-03-05` 这个索书号，直接去服务器内存里找：“03排05号书架上的数据还在吗？”如果这个 Key 不存在，Next.js 在内部字典里就根本找不到这份数据存在哪。
*   **`posts-data` (Tag) ➔ 贴在图书封面上的“分类彩色贴纸（如：历史类）”**
    *   **使用者：** **开发者（你和我）。**
    *   **作用：** 当你想清缓存时，你不可能去记几百个具体的索书号。你只需要跟 Next.js 喊一声：“把贴着‘历史类’贴纸的书全给我销毁！”（`revalidateTag('posts-data')`）。

---

### 2. 后台发生了什么？（幕后工作流）

当你执行 `revalidateTag('posts-data')` 时，Next.js 在后台默默做了这件事：

1.  Next.js 收到你的指令：`清空 'posts-data'`。
2.  Next.js 翻开它的内部账本，查找哪些 Key 绑定了这个 Tag：
    > *账本查到：标签 `'posts-data'` 对应着索书号 `['posts-list-internal-key']`。*
3.  Next.js 拿着这个索书号 `['posts-list-internal-key']`，精准定位到内存位置，把数据清空！

你看，**我们通过 Tag 间接指挥了 Next.js，而 Next.js 必须依靠我们提供的 Key 才能找到具体的缓存位置。**

---

### 总结

*   **`tags`（标签）：** 程序员用来**清缓存**的握把。
*   **`keyParts`（Key）：** Next.js 内部用来**存取数据**的索引名。

这就是为什么你后面代码里看不到它，但前面定义时却少不了它的原因！
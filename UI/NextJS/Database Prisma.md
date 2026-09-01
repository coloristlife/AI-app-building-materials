在 Next.js（特别是 App Router 全栈架构）中，**Prisma** 是目前最流行、体验最好的 **ORM（对象关系映射工具）**。

如果你想在 Next.js 里连接数据库（如 PostgreSQL、MySQL、SQLite、MongoDB 等），Prisma + Next.js 的组合简直就是“天作之合”。

我们继续用通俗的比喻和清晰的步骤，看看如何用 Prisma 在 Next.js 中极其优雅地读取和写入数据。

---

### 1. 什么是 Prisma？（心智模型）

把数据库想象成一个存储着海量表格的仓库。

*   **原始 SQL 语句：** 就像用繁琐的专业暗号去向仓库管理员要数据（容易写错，而且没有类型提示）。
*   **Prisma：** 就像你的**专属智能翻译官**。你只需要用 TypeScript 写 `prisma.user.findMany()`，Prisma 会自动把这段话翻译成高效的 SQL 语句去查数据库，并且**带着 100% 完美的 TypeScript 类型**把数据交还给你。

---

### 2. Next.js + Prisma 最重要的一步：防止数据库连接爆满 (Singleton 单例模式)

这是 99% 的初学者在 Next.js 里用 Prisma 时会踩的坑！

在开发阶段（`npm run dev`），每次你修改保存代码，Next.js 都会热更新（Hot Reload）重新加载文件。如果你在每个文件里都 `new PrismaClient()`，**每次保存都会新建一个数据库连接**，几分钟内你的数据库连接池就会被撑爆报错！

**解决方案：** 建立一个全局单例文件 `lib/prisma.ts`。

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client';

// 声明全局变量，防止热更新时重复创建 Prisma 实例
const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;

export default prisma;
```

> **以后在任何地方需要查数据库，都只需要 `import prisma from '@/lib/prisma'` 即可！**

---

### 3. 在服务端组件（`page.tsx`）里读取数据（Fetch）

还记得我们前面讲过的吗？在 Next.js 的服务端组件里，你可以直接 `async/await`，**不需要写 API 接口，直接在组件里查数据库！**

```tsx
// app/posts/page.tsx
import prisma from '@/lib/prisma'; // 引入上面建好的单例

export default async function PostsPage() {
  
  // 1. 直接在服务器端用 Prisma 查数据库！
  // 这里有完美的 TypeScript 自动补全，你可以点出每一个字段
  const posts = await prisma.post.findMany({
    where: { 
      published: true // 只查已发布的文章
    },
    orderBy: { 
      createdAt: 'desc' // 按时间倒序排列
    },
    select: {
      id: true,
      title: true,
      author: {
        select: { name: true } // 连表查询作者的名字
      }
    }
  });

  // 2. 查出来的 posts 直接就是带着类型的数组，直接渲染！
  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">文章列表</h1>
      <ul className="space-y-4">
        {posts.map((post) => (
          <li key={post.id} className="border p-4 rounded">
            <h2 className="font-semibold">{post.title}</h2>
            <p className="text-gray-500 text-sm">作者：{post.author.name}</p>
          </li>
        ))}
      </ul>
    </main>
  );
}
```

**为什么这种方式极其强悍？**
1. **零 API 路由：** 你不需要写 `app/api/posts/route.ts`。
2. **零前端体积：** Prisma 的所有代码、数据库密码，**100% 留在服务器端**，绝对不会打包发送给用户的浏览器。
3. **极速：** 服务器直接连数据库拿数据拼成 HTML 发给浏览器，速度飞快。

---

### 4. 结合 Server Actions 写入数据（Insert/Update）

查数据用服务端组件，那**新增文章**怎么办？结合我们上一节学的 **Server Actions**，体验爽到飞起！

```tsx
// app/posts/create/page.tsx
import prisma from '@/lib/prisma';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

export default function CreatePostPage() {
  
  // 1. 定义一个 Server Action 函数
  async function createPost(formData: FormData) {
    'use server';

    const title = formData.get('title') as string;
    const content = formData.get('content') as string;

    // 2. 用 Prisma 直接插入数据库！
    await prisma.post.create({
      data: {
        title,
        content,
        published: true,
        // 假设这里关联作者 ID
        authorId: 1, 
      },
    });

    // 3. 刷新列表页面的缓存，并自动跳转过去
    revalidatePath('/posts');
    redirect('/posts');
  }

  // 4. 前端表单直接挂载 Action
  return (
    <form action={createPost} className="p-8 flex flex-col gap-4 max-w-md">
      <input 
        name="title" 
        placeholder="文章标题" 
        required 
        className="border p-2 rounded"
      />
      <textarea 
        name="content" 
        placeholder="文章内容" 
        className="border p-2 rounded"
      />
      <button type="submit" className="bg-blue-500 text-white p-2 rounded">
        发布文章
      </button>
    </form>
  );
}
```

---

### 5. 高级技巧：配合动态路由获取单条数据

如果结合我们刚学的动态路由 `[id]`：

```tsx
// app/posts/[id]/page.tsx
import prisma from '@/lib/prisma';
import { notFound } from 'next/navigation';

type Props = {
  params: Promise<{ id: string }>;
};

export default async function PostDetailPage({ params }: Props) {
  // 1. 解构并等待拿到网址里的 id ( Next.js 15 规范 )
  const { id } = await params;

  // 2. 用 Prisma 根据 id 查询单条数据
  const post = await prisma.post.findUnique({
    where: { id: Number(id) },
  });

  // 3. 如果数据库里没查到这篇文章，直接触发 404 页面！
  if (!post) {
    notFound();
  }

  return (
    <article className="p-8">
      <h1 className="text-3xl font-bold">{post.title}</h1>
      <p className="mt-4">{post.content}</p>
    </article>
  );
}
```

---

### 💡 总结最佳实践口诀：

1.  **全局单例：** 用 `lib/prisma.ts` 导出 `prisma`，防止开发时数据库连接数爆满。
2.  **读数据 (Read)：** 放在服务端组件（`page.tsx`）里直接 `await prisma.xxx.findMany()`。
3.  **写数据 (Write)：** 放在 Server Actions 函数里 `await prisma.xxx.create()`，顺手调用 `revalidatePath()` 刷新页面。
4.  **查不到？：** `if (!data) notFound()` 优雅跳 404。
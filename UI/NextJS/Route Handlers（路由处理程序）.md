在前面我们聊过，Next.js 是一个自带 Node.js 后端的全栈框架。

除了用 `page.tsx` 端出完整的 HTML 网页，用 Server Actions 处理表单之外，Next.js 还要能对外提供纯粹的 RESTful API 接口（返回 JSON 数据、处理文件上传等）。

在 App Router 架构中，用来写 API 接口的技术叫 **Route Handlers（路由处理程序）**。

---

### 1. 核心命名暗号：`route.ts`

在 Next.js 里，写 API 接口的规则极其直观：

*   想做**网页**？文件叫 **`page.tsx`**
*   想做**API 接口**？文件叫 **`route.ts`**（或 `.js`）

#### 目录与 URL 映射规则：
```text
app/
 └── api/
      ├── users/
      │    └── route.ts     <-- 对应网址: GET/POST /api/users
      └── posts/
           └── [id]/
                └── route.ts <-- 对应网址: GET/DELETE /api/posts/123
```

> ⚠️ **死律：** 在同一个文件夹下，**`page.tsx` 和 `route.ts` 不能同时存在！** 
> 因为一个文件夹要么负责渲染网页 UI，要么负责返回纯 API 数据，不能既要又要。

---

### 2. 标准 HTTP 方法写法

Route Handlers 完全遵循 Web 标准的 HTTP 动词。你在 `route.ts` 里直接导出对应名字的大写函数即可：

```typescript
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';

// 1. 处理 GET 请求 (获取用户列表)
export async function GET(request: NextRequest) {
  const users = await prisma.user.findMany();
  // 返回 JSON 格式的数据，状态码默认 200
  return NextResponse.json(users);
}

// 2. 处理 POST 请求 (新建用户)
export async function POST(request: NextRequest) {
  // 解析客户端传过来的 JSON 请求体 (Body)
  const body = await request.json(); 
  
  const newUser = await prisma.user.create({
    data: { name: body.name, email: body.email }
  });

  // 返回新建好的数据，状态码设为 201 Created
  return NextResponse.json(newUser, { status: 201 });
}
```

Next.js 支持所有标准的 HTTP 方法：`GET`、`POST`、`PUT`、`PATCH`、`DELETE`、`HEAD`、`OPTIONS`。

---

### 3. 如何读取网址参数、Body 和 Cookies？

`NextRequest` 提供了非常方便的 API：

```typescript
// app/api/search/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  // 1. 读取网址问号参数 (?q=iphone&page=2)
  const searchParams = request.nextUrl.searchParams;
  const query = searchParams.get('q');
  const page = searchParams.get('page');

  // 2. 读取 Headers (请求头)
  const authHeader = request.headers.get('authorization');

  // 3. 读取 Cookies
  const token = request.cookies.get('token')?.value;

  return NextResponse.json({ query, page, token });
}
```

---

### 4. 动态 API 路由（如 `/api/posts/[id]`）

如果你需要根据 URL 里的动态 ID 处理特定的数据（比如删除某篇文章）：

```typescript
// app/api/posts/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';
import prisma from '@/lib/prisma';

type Props = {
  params: Promise<{ id: string }>;
};

// 处理 DELETE /api/posts/123 请求
export async function DELETE(request: NextRequest, { params }: Props) {
  // 1. 在 Next.js 15+ 中，使用 await 拿到动态参数 id
  const { id } = await params;

  // 2. 去数据库删除
  await prisma.post.delete({
    where: { id: Number(id) }
  });

  return NextResponse.json({ message: `文章 ${id} 已成功删除` });
}
```

---

### 5. 缓存行为（Next.js 15+ 最新规则）

在最新的 Next.js 15/16 中，Route Handlers 的 `GET` 请求**默认是不缓存的（Uncached by Default）**。每次被访问都会现场执行。

如果你想让某个 `GET` 接口变成**静态缓存接口**（比如输出固定的公开配置）：

```typescript
// 强制这个 API 接口静态化缓存！
export const dynamic = 'force-static';

export async function GET() {
  return NextResponse.json({ version: '1.0.0' });
}
```

---

### 💡 终极决策：Route Handlers vs Server Actions

既然 Route Handlers 和 Server Actions 都能在服务器跑 Node.js，**到底什么时候该用谁？**

| 场景 | 应该用什么？ | 理由 |
| :--- | :--- | :--- |
| **你的 Next.js 网站内部提交表单、点赞、增删改查** | 🟢 **Server Actions** | **首选！** 代码量少 50%，不需要写 `fetch` 和 API 路由，类型安全，自动刷新 UI。 |
| **给外部系统提供标准 REST API**（如手机 App、微信小程序、桌面客户端） | 🔵 **Route Handlers (`route.ts`)** | 外部系统只认识标准的 JSON 和 REST HTTP 请求。 |
| **接收第三方系统的 Webhook 回调通知**（如微信支付成功回调、Stripe 结算通知） | 🔵 **Route Handlers (`route.ts`)** | 微信/Stripe 需要向特定的 URL（如 `/api/pay-notify`）发送标准 POST 请求。 |
| **文件/大视频下载与流式导出**（如导出 CSV 表格） | 🔵 **Route Handlers (`route.ts`)** | 可以灵活控制 Response Headers（如 `Content-Type: text/csv`）。 |

### 总结

*   `route.ts` 是 Next.js 对外提供的 **“标准外卖窗口”**（RESTful API）。
*   如果你只是做自己网站内部的交互，优先用 **Server Actions**。
*   如果你要和外部系统、移动端 App、Webhook 打交道，选择 **Route Handlers (`route.ts`)**！
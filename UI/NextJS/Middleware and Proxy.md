在 Next.js 的全栈开发体系中，**Middleware（中间件）** 和 **Proxy（代理转发）** 是两个经常被放在一起讨论、但**职责完全不同**的网络层技术。

很多初学者容易把它们混淆，甚至把所有的代理转发逻辑都硬塞进中间件里，导致网页加载极其卡顿。

我们用最形象的**“大楼物业”**比喻，彻底分清这两个概念。

---

### 一、 核心定位与比喻

*   **Middleware（中间件） ➔ 大楼门口的“安检保安”**
    *   **职责**：在任何请求**到达页面之前**进行拦路盘查。
    *   **常见动作**：检查有没有带通行证（Cookie/Token）、没带就直接按住并踢去登录页（Redirect）、或者根据国家语言重定向（i18n）。
*   **Proxy（代理转发） ➔ 隐形中转“快递站”**
    *   **职责**：掩盖真实的后端地址，帮你把请求安全地转接给另一个服务器。
    *   **常见动作**：前端请求 `/api/java-backend/users`，Proxy 在后台悄悄把请求转发给局域网深处的 `https://real-java-server.com/v1/users`，解决跨域（CORS）并隐藏真实服务器 IP。

---

### 二、 Middleware（中间件）详解与实战

Middleware 放在你项目的**根目录**（`middleware.ts`），它会在**每一个匹配的路由渲染之前**运行。

#### 1. 核心代码示例（身份拦截）：

```typescript
// middleware.ts (必须放在项目根目录，和 app 文件夹平级)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // 1. 读取用户浏览器里的 Token Cookie
  const token = request.cookies.get('session_token')?.value;

  // 2. 如果用户访问的是后台页面 (/dashboard)，且没有登录 Token
  if (request.nextUrl.pathname.startsWith('/dashboard') && !token) {
    // 3. 保安直接拦截！强行重定向到登录页！
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // 4. 检查通过，放行！继续前往目标页面
  return NextResponse.next();
}

// 匹配器（Matcher）：告诉保安只需要检查哪些网址，避免乱检查静态图片
export const config = {
  matcher: ['/dashboard/:path*', '/profile/:path*'],
};
```

#### ⚠️ Middleware 避坑死律：
**千万不要在 `middleware.ts` 里连接数据库，或者发重度的网络 `fetch` 请求！**
因为 Middleware 拦截的是每一个请求，如果在保安检查阶段耗时 1 秒，**你整站所有的网页打开都会变慢 1 秒**！保安必须极速放行。

---

### 三、 Proxy（代理转发）详解与实现方式

当你需要把前端的请求转发给现有的 Java / Python / Go 主后端，或者为了**解决跨域（CORS）问题**时，你需要使用 Proxy。

在 Next.js 里，做 Proxy 转发有 **2 种最优雅的方式**（完全不需要占用 Middleware）：

#### 方式 A：在 `next.config.mjs` 中用 `rewrites`（官方最推荐⭐️）
这是性能最高、零代码侵入的全局重写代理：

```javascript
// next.config.mjs
/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        // 1. 前端在代码里请求的“伪装地址”
        source: '/api/backend/:path*', 
        // 2. 真实转发到的“远端主后端地址”
        destination: 'https://java-api.mycompany.com/v1/:path*', 
      },
    ];
  },
};

export default nextConfig;
```
*   **效果：** 前端在代码里 `fetch('/api/backend/users')`，浏览器以为请求的是同源地址，实际上 Next.js 服务器在后台自动帮传到了 `https://java-api.mycompany.com/v1/users`，完美解决跨域且不暴露真实后端域名！

#### 方式 B：用 Route Handler 做自定义代理（适合需要改写 Header 的场景）
如果转发前需要动态添加通关密钥，可以在 `app/api/proxy/[...path]/route.ts` 接口里用 `fetch` 手动转接：

```typescript
// app/api/proxy/[...path]/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  // 截取动态路径，手动转发给远端后端，并附带服务器端秘钥
  const res = await fetch('https://java-api.com/...', {
    headers: { 'X-Internal-Secret': process.env.SECRET_KEY! }
  });
  const data = await res.json();
  return NextResponse.json(data);
}
```

---

### 💡 Middleware vs Proxy 对比与选型表

| 维度 | Middleware (`middleware.ts`) | Proxy (`rewrites` / Route Handler) |
| :--- | :--- | :--- |
| **主要职责** | **安全拦截、身份鉴权、重定向、i18n 多语言** | **跨域转发、隐藏真实 API 域名、请求中继** |
| **比喻** | 门口核验身份的保安 | 转发包裹的隐形快递中转站 |
| **运行节点** | 边缘网络 / 页面渲染之前的关口 | 网络层路径重写 / 节点中转 |
| **性能要求** | **必须极快**（毫秒级，决不能连数据库） | 视目标后端响应速度而定 |
| **常见函数** | `NextResponse.redirect()` / `NextResponse.rewrite()` | `next.config.mjs` 里的 `rewrites()` |

### 总结

1.  需要**判断用户有没有登录、没登录不让看页面** ➔ 用 **Middleware (`middleware.ts`)**。
2.  需要**把前端的 `/api/v1` 请求转发给公司的 Java/Python 服务器、解决跨域** ➔ 用 **`next.config.mjs` 的 `rewrites`**。
3.  保持 Middleware 干净轻量，绝不在里面查数据库，你的 Next.js 网站就能既安全又极速！


# `middleware.ts` 改名为 proxy.ts

https://nextjs.org/docs/messages/middleware-to-proxy

👉 **在 Next.js 16 及更新版本中，过去的 `middleware.ts`（中间件）被正式重命名为了 `proxy.ts`（代理文件）！**

台词里的第一句话：
> *"So when there is an incoming request to the server side it can go through a proxy. This used to be called middleware..."*
> （当有一个请求发送到服务端时，它会经过一个代理。**这在过去被称为 middleware（中间件）……**）

---

### 一、 官方为什么要将 `middleware.ts` 改名为 `proxy.ts`？

过去几年，很多开发者对 `middleware.ts` 存在极大的**误解与误用**：

1. **混淆 Express.js 中间件**：很多人以为它就像 Node.js/Express 里的中间件一样，在里面写重度的业务逻辑、查数据库、做复杂的 Auth 鉴权。
2. **引发性能与安全隐患**：`middleware.ts` 跑在所有请求的最前面。如果你在里面做重度的数据库或 API 操作，整个网站都会变慢；甚至在过去还引发过通过伪造 Header 绕过中间件安全检查的漏洞。

因此，官方决定在 Next.js 16 中**正名**：将其重命名为 **`proxy.ts`**。

**“Proxy（代理）”** 这个名字准确表达了它的物理本质：**它就是立在你的应用最前方的一道网络边缘关卡（Network Gateway）**。它的职责不是处理复杂业务，而是对进来的请求做**“快、准、狠”的拦截与转接**。

---

### 二、 哪些工作应该交给 `proxy.ts` 做？

台词里列举得非常地道：

#### 1. 修改请求信息 (Modify Incoming Requests)
在请求到达你的 Server Actions、API 接口或者页面组件之前，对请求头（Headers）或 Cookies 进行微调。

#### 2. URL 重写 (Rewrite the URL)
用户访问的是 `/shop`，但你可以根据用户的地理位置，在后台默默把请求重写（Rewrite）到 `/shop/jp`（日本区），而用户的浏览器地址栏依然显示 `/shop`。

#### 3. A/B 测试 (A/B Testing)
当一个请求进来时，`proxy.ts` 可以随机把 50% 的流量重定向到新页面 `/feature-b`，另外 50% 留给老页面 `/feature-a`，从而在网络最前端实现零延迟的 A/B 测试。

#### 4. 轻量级重定向 (Redirects)
检查请求里有没有带着 Token Cookie，如果没有，在它接触到后端数据库之前，直接弹回 `/login` 登录页。

---

### 三、 从 `middleware.ts` 到 `proxy.ts` 的写法变化

在代码层面，它的功能完全继承，只是文件名和函数名变了：

#### 旧写法 (Next.js 15 及之前)：
```typescript
// middleware.ts (旧文件)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  return NextResponse.next();
}
```

#### 新写法 (Next.js 16 及之后)：
```typescript
// proxy.ts (新文件，位于项目根目录或 src/ 下)
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function proxy(request: NextRequest) {
  // 对进来的请求做快速处理...
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'], // 匹配器
};
```

---

### 💡 总结最佳实践

*   **`proxy.ts`（原 `middleware.ts`）的定位：** **高速网络门卫**。只做轻量的重定向、URL 重写、Header 修改、A/B 测试。
*   **不要在 `proxy.ts` 里做什么：** 不要连数据库！不要做重的 API Fetch 请求！重度的身份校验和数据查询，请统统放在 **Server Components** 或 **Server Actions** 里完成！
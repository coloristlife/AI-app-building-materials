在 Next.js 全栈应用中，**Authentication（身份验证与登录认证）** 是每一个真实项目都绕不开的核心关卡。

搞懂 Next.js 的认证，你需要先分清两个概念：
1.  **Authentication（认证 - 简称 AuthN）：** 证明**“你是谁”**（比如输入账号密码、谷歌一键登录、微信扫码）。
2.  **Authorization（授权 - 简称 AuthZ）：** 证明**“你能干什么”**（比如检查你是不是 VIP、是不是管理员、有没有权限删文章）。

我们用最形象的**“游乐园手环”**比喻，结合现代 Next.js App Router 的架构，把身份认证彻底讲透。

---

### 一、 核心心智模型：游乐园手环（Session / Cookie）

整个认证流程其实就像去游乐园玩：

1.  **登录（Authentication）：** 你在售票处（登录页）出示身份证、付款。
2.  **发手环（Session/JWT）：** 售票员确认无误后，在你手腕上系上一个**防伪手环（加密的 HTTP-Only Cookie）**。
3.  **游玩项目（Authorization）：** 你去玩过山车（访问 `/dashboard` 或执行 Server Action），工作人员看一眼你手腕上的手环，确认有效后放行。

---

### 二、 现代 Next.js 的“三层安全防护网”

在 Next.js App Router 架构中，一个安全的认证系统必须建立 **三层防线**：

```text
[ 用户请求访问 /dashboard ]
            │
            ▼
【 第一层防线：网络边缘 (proxy.ts / 原 middleware) 】
  看一眼有没有 Cookie。没有？立刻重定向踢去 /login！
            │
            ▼
【 第二层防线：数据访问层 (DAL / Server Component) 】
  在 page.tsx 真正查数据库前，解密 Cookie 拿到真实 UserId。
            │
            ▼
【 第三层防线： Server Actions 】
  用户点击“删除文章”按钮时，在 Action 内部再次校验身份，防越权。
```

#### 1. 第一层：`proxy.ts`（原 `middleware.ts`）做粗粒度拦截
```typescript
// proxy.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function proxy(request: NextRequest) {
  const sessionToken = request.cookies.get('session_token')?.value;

  // 如果访问敏感页面且没有 Token，拦截到登录页
  if (request.nextUrl.pathname.startsWith('/dashboard') && !sessionToken) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  return NextResponse.next();
}
```

#### 2. 第二层：数据访问层（DAL）做细粒度鉴权
在服务端组件（`page.tsx`）里，编写专门的校验函数 `verifySession()`，绝对不相信客户端传来的数据：

```typescript
// lib/dal.ts (数据访问层)
import { cookies } from 'next/headers';
import { redirect } from 'next/navigation';

export async function verifySession() {
  const cookie = (await cookies()).get('session_token')?.value;
  const session = await decryptToken(cookie); // 解密 Token

  if (!session?.userId) {
    redirect('/login');
  }

  return { isAuth: true, userId: session.userId };
}
```

---

### 三、 会话（Session）存储的两大主流方式

拿到登录凭证后，手环（Session）的数据怎么存？

| 方案 | 运行机制 | 优点 | 缺点 |
| :--- | :--- | :--- | :--- |
| **JWT（无状态 Token）** | 用户信息加密后，直接写在 Cookie 里。 | 速度极快！服务器不需要连数据库解密。 | 令牌发出去后，很难在到期前强行作废（除非换密钥）。 |
| **Database Session（有状态）** | Cookie 里只存一个随机 ID，每次访问去数据库/Redis 查这个 ID 对应的用户。 | 控制力极强！可以随时在后台封禁某个账号、强踢下线。 | 每次页面渲染都要多查一次数据库/Redis。 |

---

### 四、 Next.js 圈子最主流的 3 大落地方案（不用手造轮子）

在实际项目中，**千万不要自己从零手写密码哈希和加密逻辑（极易留安全漏洞）**！行业里有成熟的“超级轮子”：

#### 方案 1：Auth.js (原 NextAuth.js) —— **开源免费王者 🏆**
*   **定位：** Next.js 社区第一大开源免费认证库。
*   **特点：** 原生支持 GitHub、Google、微信、账号密码等几十种登录方式。完美集成 Prisma，自动在你的数据库里生成 `User` 和 `Session` 表。
*   **适合：** 想完全掌握数据所有权、不想花钱买第三方认证服务的项目。

#### 方案 2：Clerk —— **托管 SaaS 天花板 🚀**
*   **定位：** 专为 Next.js 打造的第三方认证云服务（极受独立开发者和硅谷公司喜爱）。
*   **特点：** 极致的 DX（开发者体验）！官方直接提供做好的 React 组件：
    ```tsx
    import { SignIn, UserButton } from '@clerk/nextjs';
    // 放入这个组件，直接变出一个包含手机验证码、Passkey、Google 登录的精美弹窗！
    ```
*   **适合：** 想 10 分钟搞定复杂登录逻辑、支持手机短信验证码、不在乎使用第三方托管的项目。

#### 方案 3：Supabase Auth —— **BaaS 平台集成**
*   **定位：** 如果你的数据库用的是 Supabase，直接用它配套的 Auth 功能。
*   **特点：** 开箱即用，支持邮件魔术链接（Magic Link）、第三方 OAuth，且直接和数据库的行级安全策略（RLS）绑定。

---

### 💡 生产安全三大铁律 🔒

1.  **Cookie 必须设置 `httpOnly: true`：** 禁止 JavaScript 读取 Cookie，彻底封死 XSS 跨站脚本攻击。
2.  **Cookie 必须设置 `secure: true`：** 确保 Token 只能在 HTTPS 加密网络下传输。
3.  **绝对不要在客户端组件里存储敏感 Token：** 比如存放在 `localStorage` 里是极其危险的做法，一不小心就会被恶意第三方脚本盗取。

### 总结

*   **不要手写加密：** 优先选择 **Auth.js** 或 **Clerk**。
*   **分层防御：** `proxy.ts` 负责大门粗拦截，服务端组件 / Server Actions 内部负责精准鉴权。
*   **Cookie 传凭证：** 用 HTTP-Only Cookie 传递 Session/JWT，兼顾安全与全栈 SSR 体验。
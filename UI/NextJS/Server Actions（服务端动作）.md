前面我们初步感受过 **Server Actions（服务端动作）** 的神奇之处——前端的表单和按钮可以直接调用服务端的函数。

现在，伴随着我们学过的 `async/await`、缓存刷新（`revalidateTag`）以及 `'use cache'` 指令，是时候把 Server Actions 的**进阶实战打法、安全法则与 UI 结合套件**完整串联起来了！

---

### 1. Server Actions 的两种文件写法

在实际项目中，Server Actions 有两种存放方式：

#### 方式 A：独立文件集中管理（生产环境强烈推荐 ⭐️）
建立一个专门的文件 `app/actions.ts`，在最顶部写上 `'use server'`。这样文件里的所有导出的函数都会自动变成 Server Action。

```typescript
// app/actions.ts
'use server'; // 这个文件里的函数全部运行在服务器端！

import prisma from '@/lib/prisma';
import { revalidatePath } from 'next/cache';

export async function createComment(formData: FormData) {
  const content = formData.get('content') as string;
  await prisma.comment.create({ data: { content } });
  revalidatePath('/blog');
}
```

#### 方式 B：在服务端组件内内联（适合极简小页面）
直接在服务端组件（`page.tsx`）的函数内部第一行写 `'use server'`。

---

### 2. 打造顶级体验的“全家桶 Hooks”

光能提交表单还不够，用户需要看到**“加载中...”、“提交失败提示”**以及**“瞬间反应的 UI”**。

React 提供了 3 个专门配合 Server Actions 的神级 Hooks：

#### 🛠️ Hook 1: `useActionState` —— 接收服务端返回的错误或结果
专门用来处理 Server Action 的返回值（比如密码输错了、格式不对）。

```tsx
'use client';
import { useActionState } from 'react';
import { loginAction } from '@/app/actions';

export default function LoginForm() {
  // state: 服务器返回的结果（比如 { error: '密码错误' }）
  // formAction: 包装后的提交函数
  // isPending: 是否正在提交中
  const [state, formAction, isPending] = useActionState(loginAction, null);

  return (
    <form action={formAction}>
      <input name="email" type="email" />
      <input name="password" type="password" />

      {/* 展示服务端的错误提示 */}
      {state?.error && <p className="text-red-500">{state.error}</p>}

      <button disabled={isPending}>
        {isPending ? '登录中...' : '登录'}
      </button>
    </form>
  );
}
```

#### 🛠️ Hook 2: `useFormStatus` —— 局部获取提交状态
如果你的提交按钮是个独立的子组件，用它可以在子组件里直接知道表单是否在提交中，不用一层层传 props：

```tsx
'use client';
import { useFormStatus } from 'react-dom';

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button disabled={pending}>
      {pending ? '正在保存...' : '保存'}
    </button>
  );
}
```

#### ⚡ Hook 3: `useOptimistic` —— 乐观 UI 渲染（丝滑体验的天花板）
什么叫“乐观 UI”？
**当用户点击“点赞”时，不等服务器返回结果，UI 立刻在 0 毫秒内把点赞数 +1；后台去跑 Server Action，如果万一失败了，UI 自动弹回。**

```tsx
'use client';
import { useOptimistic } from 'react';
import { likePostAction } from '@/app/actions';

export function LikeButton({ currentLikes }: { currentLikes: number }) {
  // 1. 设置乐观状态：默认等于真实数据，点击时立刻 +1
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    currentLikes,
    (state, amount: number) => state + amount
  );

  return (
    <button
      onClick={async () => {
        addOptimisticLike(1); // 0毫秒！UI 立刻更新成 +1！
        await likePostAction(); // 后台安静地去跑 Server Action 查库
      }}
    >
      👍 点赞 ({optimisticLikes})
    </button>
  );
}
```

---

### 3. 生产环境两大安全死律 🔒

Server Actions 用起来太爽了，以至于很多初学者会犯安全错误。请死记以下两条生产安全死律：

#### ⚠️ 死律一：永远不要信任客户端传来的数据（一定要用 Zod 校验！）
在网络层面，**Server Action 本质上是一个隐藏的 HTTP POST 接口**。恶意黑客可以用 Postman 直接向你的 Server Action 发送任意垃圾数据。

**正确做法：** 在 Server Action 内部使用 **Zod** 等库进行严格校验：

```typescript
'use server';
import { z } from 'zod';

// 定义严格的数据校验规则
const schema = z.object({
  email: z.string().email('邮箱格式不正确'),
  age: z.number().min(18, '必须年满18岁'),
});

export async function registerUser(prevState: any, formData: FormData) {
  // 校验客户端输入
  const validatedFields = schema.safeParse({
    email: formData.get('email'),
    age: Number(formData.get('age')),
  });

  // 如果校验失败，立刻返回错误，绝不查库！
  if (!validatedFields.success) {
    return { error: validatedFields.error.flatten().fieldErrors };
  }

  // 校验通过，安全写入数据库
  await db.user.create({ data: validatedFields.data });
}
```

#### ⚠️ 死律二：永远在 Server Action 内部重新做身份验证（鉴权）
千万不要从前端把 `userId` 当成参数传给 Server Action！黑客可以把 `userId` 改成管理员的 ID。

**正确做法：** 在 Server Action 内部从 `cookies()` 或 Session 里读取当前登录用户的 ID。

```typescript
'use server';
import { cookies } from 'next/headers';

export async function deletePost(postId: string) {
  // 1. 在服务端内部验证当前登录者
  const session = await getSessionFromCookies(await cookies());
  if (!session) throw new Error('未登录');

  // 2. 检查这篇文章是不是属于当前登录者，安全删除
  await db.post.delete({
    where: { id: postId, authorId: session.userId }
  });
}
```

---

### 💡 Server Actions 完整工作全景图

```text
[ 用户点击/提交 ] 
       │
       ▼
[ 前端 UI ]: 触发 `useOptimistic` (0ms 界面响应)
       │
       ▼
[ Server Action ]: `'use server'` 接收请求
       │
       ├─▶ 1. 鉴权 (校验 Cookies / Session)
       ├─▶ 2. 校验 (用 Zod 验证输入合法性)
       └─▶ 3. 执行 (Prisma 写入数据库)
       │
       ▼
[ 刷新缓存 ]: `revalidatePath()` / `revalidateTag()`
       │
       ▼
[ 最新状态 ]: 页面内容自动更新，完美闭环！
```

这就是现代 Next.js 中完整的 Server Actions 全貌！它将原本零散的前端状态、网络请求、后端 API、数据库写入和缓存刷新的逻辑，高度凝聚成了一个优雅、安全的整体。



# 特意给 Server Action 划红线、单独强调安全死律呢

你说得完全正确：**原则上，任何网络接口（无论是 REST API 的 GET/POST、GraphQL 还是 Server Actions），都必须做鉴权和数据校验。** 

那为什么几乎所有 Next.js 的资深开发者和官方文档，都要**特意给 Server Action 划红线、单独强调安全死律呢？**

这是因为：**Server Actions 带来了一种极其危险的“语法假象（Syntactic Illusion）”，它太像普通的 JavaScript 函数了，以至于极易诱使开发者产生安全麻痹。**

具体有以下 **4 个让初学者极易踩坑的“安全陷阱”**：

---

### 陷阱一：心理防御机制降级（“普通函数”的假象）

*   **写传统 REST API (`app/api/user/route.ts`) 时：**
    你很清楚自己在写一个后端文件。当你写下 `export async function POST(req)` 的那一刻，你的大脑会自动切换到“后端防御模式”——你会立马意识到：“这是个暴露在公网上的接口，我要读取 `req.json()`，我要校验数据，我要查 Cookie Token。”
*   **写 Server Action 时：**
    你写的是 `async function deleteUser(id)`。
    因为它**长得和前端的普通函数一模一样**，甚至可以直接在前端组件里 `import` 调用。这会在无意中降低程序员的心理防御，让你误以为：“这只是我本地写的一个辅助函数而已，不用搞得那么严肃吧？”

**真相是：** Next.js 在打包时，会在后台默默把每一个 Server Action 编译成一个**完全公开的 HTTP POST 接口（带着一串哈希 ID）**。黑客根本不需要看你的前端界面，直接向这个网址发 POST 请求就能执行它！

---

### 陷阱二：UI 权限带来的“假安全感”

这是初学者犯得最多的错误！

很多人在前端界面写了这样的代码：
```tsx
// 前端组件
export default function AdminPanel({ user }) {
  // 开发者以为：只要不是管理员，按钮压根不会渲染，那就安全了！
  if (!user.isAdmin) return <p>你不是管理员</p>;

  return (
    <button onClick={() => deleteDatabaseAction()}>
      删库（危险）
    </button>
  );
}
```

**开发者产生的幻觉：** “既然普通用户根本看不到这个按钮，那绑定的 `deleteDatabaseAction` 肯定就是安全的了，里面不需要再查权限了。”

**黑客的做法：** 黑客打开浏览器控制台，找到 `deleteDatabaseAction` 对应的 Action ID，然后用脚本伪造一个 HTTP POST 请求直接发送给服务器。**如果你的 Server Action 内部没有重新校验 `user.isAdmin`，服务器就会直接删库！**

---

### 陷阱三：TypeScript 带来的“类型安全假象”

在传统 API 里，你拿到的是 `req.json()`（未知数据），你自然会去校验它。

而在 Server Action 里，TypeScript 会给你美好的提示：
```typescript
async function updateAge(age: number) {
  'use server';
  // TS 告诉你 age 是个 number，你就以为万事大吉了？
}
```

**致命误区：** TypeScript 的类型检查**只存在于编译期**！
在运行期间，黑客可以通过 HTTP 请求给 `age` 传进 `-999`、`null`、甚至一段恶意的 SQL 注入字符串。TypeScript 无法在运行时阻挡恶意数据，你**必须在 Server Action 内部使用 Zod 进行运行时校验**。

---

### 陷阱四：越权漏洞（Horizontal Privilege Escalation）

假设你写了一个修改用户头像的函数：
```typescript
// 错误示范：直接接收前端传来的 userId
export async function updateAvatar(userId: string, newAvatarUrl: string) {
  'use server';
  await db.user.update({ where: { id: userId }, data: { avatar: newAvatarUrl } });
}
```
*   **正常用户：** 前端自动传入自己的 `userId = "123"`。
*   **恶意用户：** 通过 Postman 调用这个 Server Action，把 `userId` 改成 `"456"`（别人的 ID）。
*   **结果：** 恶意用户把别人的头像给改了（越权漏洞）。

在 Server Action 里，**绝不能相信前端传过来的身份 ID**。必须在服务端内部通过 `cookies()` 或 Session 拿到当前真正登录的人。

---

### 💡 总结比喻

*   **传统 REST API：** 就像是在房子外面建造了一个大铁门（明显的 `/api/xxx` 网址）。因为大铁门很显眼，所有人走到门前都会本能地记得“要装锁”（做鉴权和校验）。
*   **Server Actions：** 就像是框架在房子墙上自动开了无数个**“隐形传送门”**。虽然本质上也是门（也是 HTTP POST），但因为它们看起来就像自家墙壁上的一个普通按钮，开发者极易忘记给这扇隐形门上锁！

所以，特别强调生产安全死律，是为了提醒大家：**切勿被 Server Action 优雅简洁的函数语法所欺骗，请随时记住——它的本质永远是一个暴露在公网上的 HTTP POST 接口！**
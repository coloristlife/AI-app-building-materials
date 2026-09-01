在前面，我们讨论过用 `unstable_cache` 给数据库查询加缓存，也讨论过在 `fetch` 里配置缓存。

但是，Next.js 团队觉得这些写法还是不够优雅、不够符合 React 的直觉。

于是，在最新的 Next.js 版本中，官方推出了一个最具变革性的新指令——**`'use cache'`（组件级缓存 / 函数级缓存）**。

这是继 `'use client'`（客户端组件）和 `'use server'`（服务端 Action）之后，Next.js 带来的**第三个核心指令**！

---

### 1. 什么是 Cache Components（`'use cache'`）？

一句话概括：
**只要你在一个组件（Component）或函数（Function）的顶部写上一行 `'use cache'`，Next.js 就会自动把这个组件计算出来的 HTML 结果或函数的返回值给“记住”（缓存起来）！**

在以前，缓存是针对“网络请求（`fetch`）”或者“整个页面（`page.tsx`）”的。
而 `'use cache'` 让你拥有了**精准控制某一个具体 React 组件**是否要缓存的超能力。

---

### 2. 代码实战：如何使用 `'use cache'`？

#### 用法 A：直接缓存一个独立的 Server Component

假设你有一个天气预报组件，去第三方 API 查数据比较慢。你希望这个组件**独立缓存**，不拖慢页面其他部分：

```tsx
// app/components/WeatherWidget.tsx

// 1. 在组件函数内部第一行写上 'use cache'！
export async function WeatherWidget() {
  'use cache'; // 魔法暗号：把这个组件渲染出来的 HTML 结果存入缓存！

  // 这里可以是慢 fetch，也可以是复杂的 Prisma 数据库查询
  const res = await fetch('https://api.weather.com/v1');
  const weather = await res.json();

  return (
    <div className="border p-4 rounded">
      <h3>当前天气：{weather.temp}°C</h3>
    </div>
  );
}
```

**发生了什么？**
当这个组件第一次渲染时，Next.js 会跑一次逻辑并记住结果。以后任何页面只要引用了 `<WeatherWidget />`，Next.js **直接从缓存里把做好的 HTML 吐出来**，零延迟，也不再去调用任何数据接口！

---

#### 用法 B：用 `cacheLife` 控制组件的缓存寿命

你可以通过 Next.js 提供的 `cacheLife` 函数，极度优雅地控制这个组件要缓存多久：

```tsx
import { cacheLife } from 'next/cache';

export async function StockWidget() {
  'use cache';
  
  // 告诉 Next.js：这个组件的缓存寿命按照 "minutes"（分钟级）来管理
  // 可选值包括: 'seconds' | 'minutes' | 'hours' | 'days' | 'weeks' | 'max'
  cacheLife('minutes'); 

  const stocks = await getStockPrices();
  return <div>股票行情：{stocks.btc}</div>;
}
```

#### Next.js 官方提供的内置缓存“档位”大全

为了不让开发者去死记硬背 86400 秒 这种难懂的数字，Next.js 像汽车的挡位一样，直接给你提供了语义化的名称：
https://nextjs.org/docs/15/app/api-reference/functions/cacheLife

|   |   |   |
|---|---|---|
|档位名称|缓存寿命大致范围|适用场景|
|cacheLife('seconds')|数秒级|实时股票行情、秒杀库存|
|cacheLife('minutes')|数分钟级|微博热搜榜、实时新闻列表|
|cacheLife('hours')|数小时级|天气预报、汇率换算、热门文章|
|**cacheLife('days')**|**天级（约 24 小时）**|**每日推荐商品、每日一言、博客文章、排行榜**|
|cacheLife('weeks')|周级|每周精选、月度报告|
|cacheLife('max')|极长/近乎永久|隐私政策、关于我们、历史归档数据|

---
---

#### 用法 C：用 `cacheTag` 给组件打标签（方便手动清空）

还记得我们前面学的 `revalidateTag` 吗？配合 `'use cache'`，你可以直接给某个组件打上专属标签：

```tsx
import { cacheTag } from 'next/cache';

export async function UserProfileCard({ userId }: { userId: string }) {
  'use cache';
  
  // 给这个特定用户的卡片打上专属标签
  cacheTag(`user-${userId}`);

  const user = await prisma.user.findUnique({ where: { id: userId } });
  return <div>用户名：{user.name}</div>;
}
```

**之后在 Server Action 里刷新它：**
```typescript
import { revalidateTag } from 'next/cache';

async function updateUserName(userId: string) {
  'use server';
  // 修改数据库...

  // 完美！精准只作废这一个用户卡片组件的缓存！
  revalidateTag(`user-${userId}`);
}
```

---

### 3. 三大指令终极心智模型（对比 Cheat Sheet）

现在，Next.js 拥有了完整的**三大指令阵营**，它们各司其职：

| 指令 | 官方名字 | 核心作用 | 所在位置/比喻 |
| :--- | :--- | :--- | :--- |
| **`'use client'`** | 客户端组件 | **开启交互**（可以使用 `useState`、`onClick`，代码发给浏览器） | 餐厅前厅（服务员） |
| **`'use server'`** | 服务端 Action | **开启数据修改**（前端直接调用的服务端函数） | 直通后厨的热线电话 |
| **`'use cache'`** | 缓存组件/函数 | **开启结果暂存**（把计算好的 HTML 或数据冷藏起来备用） | 后厨的保鲜冷库 |

---

### 4. `'use cache'` 与 PPR（局部预渲染）的完美合体

上一节我们讲了 PPR（静态外壳 + 动态挖孔）。

当你在项目里开启了 PPR 时，`'use cache'` 扮演了至关重要的角色：

*   如果一个组件加了 `'use cache'`，Next.js 在打包时就知道：*“哦！这个组件的结果是可以被记住的！”* 它就会把这个组件**自动缝合进 PPR 的“静态外壳（Static Shell）”里**，随 CDN 0 毫秒吐给用户。
*   只有那些没有加 `'use cache'`、并且读取了 `cookies()` 的纯动态组件，才会留在 `<Suspense>` 的动态空洞里流式传输。

### 总结

`'use cache'` 是 Next.js 简化缓存架构的**里程碑**功能。

它摆脱了以前针对整个页面或复杂的 `unstable_cache` 包装函数的繁琐，让你能像搭积木一样，**按需给任何一个微小的 React 组件加上缓存保鲜膜**。代码更少，语义更清晰，性能更狂暴！
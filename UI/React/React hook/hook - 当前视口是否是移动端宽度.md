```ts
const MOBILE_BREAKPOINT = 768

export function useIsMobile() {
  const [isMobile, setIsMobile] = React.useState<boolean | undefined>(undefined)

  React.useEffect(() => {
    const mql = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`)
    const onChange = () => {
      setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)
    }
    mql.addEventListener("change", onChange)
    setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)
    return () => mql.removeEventListener("change", onChange)
  }, [])

  return !!isMobile
}

```

这段代码是一个检测「当前视口是否是移动端宽度」的 hook，思路和 `use-toast.ts` 里的 pub-sub 完全不同——这里用的是浏览器原生的 **`matchMedia` API + 事件监听**，配合 `useEffect` 做订阅/清理。逐行拆解：

## 1. 常量

```js
const MOBILE_BREAKPOINT = 768
```

定义"移动端"的分界线：视口宽度小于 768px 算移动端。

## 2. 初始状态

```js
const [isMobile, setIsMobile] = React.useState(undefined)
```

初始值是 `undefined`（不是 `false`！这点很关键，后面会讲为什么）——因为组件第一次渲染时（尤其在服务器端渲染 SSR 场景下），还没办法安全地读取 `window.innerWidth`，所以先给个"未知"状态。

## 3. `matchMedia` 是什么

```js
const mql = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`)
```

`matchMedia` 是浏览器提供的 API，传入一段 CSS 媒体查询字符串（这里是 `(max-width: 767px)`），返回一个 `MediaQueryList` 对象 `mql`。这个对象：

- `mql.matches` 是个布尔值，表示"当前视口是否匹配这个查询"
- 更重要的是，它可以被"监听"——当匹配状态发生变化时（比如用户缩放浏览器窗口，跨过了 767px 这条线），会触发一个 `"change"` 事件

这比你自己写 `window.addEventListener("resize", ...)` 再手动比较宽度更高效：浏览器只在真正跨过这条阈值线时才通知你，而不是每次像素级的 resize 都通知你。

## 4. 变化时的回调

```js
const onChange = () => {
  setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)
}
```

定义一个函数：每当 `mql` 触发 `"change"` 事件（即跨过了 767/768 这条线），就重新读取 `window.innerWidth`，更新 `isMobile` 状态，从而触发这个组件重新渲染。

注意这里没有直接用 `mql.matches`，而是重新算了一遍 `window.innerWidth < MOBILE_BREAKPOINT`——效果上是等价的，只是写法上重新查了一次真实宽度而不是复用 `mql` 自带的判断结果。

## 5. 订阅 + 立即执行一次

```js
mql.addEventListener("change", onChange)
setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)
```

- `addEventListener` 订阅未来的变化（跨越阈值时才会触发）
- 紧接着**立刻手动调用一次**同样的判断逻辑来设置初始值——因为 `addEventListener` 只会在"未来发生变化"时触发，不会在订阅的瞬间自动触发一次。如果没有这一行，`isMobile` 会一直停留在初始值 `undefined`，直到用户真的调整了窗口大小才会第一次更新。

这也解释了第 2 步为什么初始值是 `undefined` 而不是 `false`：这两行加起来，才是真正计算出第一个有效值的地方，`useState(undefined)` 只是个临时占位。

## 6. 清理函数

```js
return () => mql.removeEventListener("change", onChange)
```

组件卸载时，取消订阅，防止内存泄漏（否则 `mql` 会一直持有对 `onChange`、进而对这个已经不存在的组件的引用）。

## 7. 依赖数组 `[]`

```js
}, [])
```

空数组表示：这个 effect **只在组件挂载时执行一次**，卸载时执行一次清理，中间不会重复执行。这正是上一段 `use-toast.ts` 里我提到"理想情况应该用 `[]`"的写法——这里用对了。

## 8. 返回值

```js
return !!isMobile
```

`!!` 是"双重取反"，把任意值强制转换成布尔值：

- `!!undefined` → `false`
- `!!true` → `true`
- `!!false` → `false`

所以即使内部状态一开始是 `undefined`（"还不知道"），对外暴露给使用者的永远是一个干净的 `boolean`（`true`/`false`），调用者不需要处理"未知"这个第三种状态。

## 整体流程图

```
组件挂载
   │
   ▼
useEffect 执行一次：
   1. 创建 mql（一条"是否 < 768px"的查询）
   2. 订阅 mql 的 change 事件 → onChange
   3. 立即手动算一次当前宽度，setIsMobile(...)
   │
   ▼
用户缩放窗口，跨过 768px 这条线
   │
   ▼
浏览器触发 mql 的 "change" 事件 → onChange 执行 → setIsMobile(新值) → 组件重新渲染
   │
   ▼
组件卸载 → 清理函数执行 → removeEventListener，停止监听
```

这里有没有哪一部分需要我再展开讲讲——比如 `matchMedia` 和普通的 `resize` 事件监听相比到底好在哪，或者为什么 SSR 场景下不能一开始就读 `window.innerWidth`？
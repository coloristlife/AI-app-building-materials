`useEffect` 是 React 中最常用但也最容易被误用的内置 Hook 之一。

简单来说，它的作用是：**允许你在函数组件中处理“副作用（Side Effects）”**。

---

### 一、 什么是“副作用（Side Effect）”？

React 组件的核心任务是：**输入（Props / State） $\rightarrow$ 纯粹地输出（JSX）**。

>在 **React** 的语境下，**JSX 可以简单理解成：让你在 JavaScript 里写“类似 HTML 的 UI 代码”的语法。**

除此之外，任何**与外部世界进行交互或改变外部状态**的操作，都叫副作用。例如：
* 发送 HTTP 网络请求（Fetch API / Axios）
* 手动修改 DOM 节点（如 `document.title = "新标题"`）
* 设置定时器（`setTimeout` / `setInterval`）
* 订阅/监听事件（`window.addEventListener`）
* 记录日志、操作 LocalStorage

`useEffect` 的出现，就是为了让你**在组件渲染到屏幕之后**，安全地执行这些副作用。

---

### 二、 基础语法与三种使用模式

`useEffect` 接收两个参数：一个**回调函数**和一个可选的**依赖项数组（Dependency Array）**。

```typescript
useEffect(() => {
  // 1. 副作用逻辑代码

  return () => {
    // 2. 清理函数（可选）：在组件卸载或下次效应执行前运行
  }
}, [依赖项1, 依赖项2]) // 3. 依赖项数组
```

依赖项数组决定了 `useEffect` 的**执行时机**，共有 **3 种模式**：

#### 1. 不传依赖项数组 $\rightarrow$ **每次渲染后都执行**
```typescript
useEffect(() => {
  console.log("组件重新渲染了！")
}) // 没传第二个参数
```
* **时机**：首次挂载时执行，**之后每次组件重新渲染后都会执行**。
* **风险**：如果在里面更新 state，会导致死循环！

#### 2. 传空数组 `[]` $\rightarrow$ **只在首次挂载时执行一次**
```typescript
useEffect(() => {
  console.log("组件挂载完成（只运行一次）")
}, []) // 空数组
```
* **时机**：只在组件**第一次显示到屏幕上（Mount）**时执行一次。
* **用途**：页面加载时初始化数据、发送一次性 API 请求。

#### 3. 传带有变量的数组 `[a, b]` $\rightarrow$ **依赖项改变时执行**
```typescript
useEffect(() => {
  console.log(`userId 变成了: ${userId}`)
}, [userId]) // 监听 userId
```
* **时机**：首次挂载时执行一次；之后只要数组里的 `userId` 发生变化，就会重新执行。

---

### 三、 什么是“清理函数（Cleanup Function）”？

如果你的副作用创建了全局监听、定时器或订阅，你必须在 `useEffect` 中返回一个**清理函数**，否则会导致**内存泄漏**。

```typescript
useEffect(() => {
  const handleResize = () => console.log(window.innerWidth)
  
  // 1. 添加监听
  window.addEventListener('resize', handleResize)

  // 2. 返回清理函数
  return () => {
    // 移除监听
    window.removeEventListener('resize', handleResize)
  }
}, [])
```

#### 清理函数的执行时机：
1. **组件卸载（Unmount）时**（例如用户切换了页面）。
2. **下一次 `useEffect` 执行前**（用于清理上一次残留的副作用）。

---

### 四、 最佳实践与避坑指南（Best Practices）

#### 1. ❌ 不要为了“计算派生数据”使用 `useEffect`
**常见错误：**
```typescript
// ❌ 错误：多余的 state 和 useEffect
const [firstName, setFirstName] = useState('Alex')
const [lastName, setLastName] = useState('Smith')
const [fullName, setFullName] = useState('')

useEffect(() => {
  setFullName(firstName + ' ' + lastName)
}, [firstName, lastName])
```
**正确做法：直接在渲染时计算**
```typescript
// ✅ 正确：在渲染逻辑中直接计算，不需要 useEffect！
const [firstName, setFirstName] = useState('Alex')
const [lastName, setLastName] = useState('Smith')

const fullName = firstName + ' ' + lastName // 渲染时自动计算
```

---

#### 2. ❌ 不要为了“响应用户操作”使用 `useEffect`
如果某个逻辑是**因为用户点击了按钮**而触发的，应该写在 `onClick` 事件处理函数里，而不是写在 `useEffect` 里面。

**常见错误：**
```typescript
// ❌ 错误：用 useEffect 去监测提交状态
const [isSubmitted, setIsSubmitted] = useState(false)

useEffect(() => {
  if (isSubmitted) {
    postData()
  }
}, [isSubmitted])
```
**正确做法：**
```typescript
// ✅ 正确：直接在事件句柄中执行
const handleSubmit = () => {
  postData()
}
```

---

#### 3. 遵守“诚实依赖”原则（不要对依赖项撒谎）
如果在 `useEffect` 内部使用了某个外部变量（`props`、`state` 或函数），**必须**把它放入依赖项数组中。

```typescript
// ❌ 隐瞒依赖项：使用了 count 但依赖项写了 []，会导致闭包陷阱（拿到的 count 永远是初始值 0）
useEffect(() => {
  console.log(count)
}, []) 

// ✅ 诚实声明依赖
useEffect(() => {
  console.log(count)
}, [count])
```
*建议使用 ESLint 插件 `eslint-plugin-react-hooks`，它会自动提醒你缺少了哪些依赖项。*

---

#### 4. 处理网络请求时，注意清理“未完成的请求”
如果用户频繁切换页面或重复操作，旧的网络请求可能在新的请求之后才返回（竞态条件 Race Condition）。

```typescript
useEffect(() => {
  let isCancelled = false

  fetchData(userId).then(data => {
    // 只有当组件依然有效且没切换 userId 时，才更新 state
    if (!isCancelled) {
      setData(data)
    }
  })

  return () => {
    isCancelled = true // 标记旧请求已失效
  }
}, [userId])
```

---

#### 5. 理解 React 18 严格模式下的“双重执行”
在开发环境（`npm run dev`）下，如果你开启了 `<React.StrictMode>`，你会发现 `useEffect` **在页面加载时会执行两次**：
$$\text{挂载} \rightarrow \text{卸载} \rightarrow \text{再次挂载}$$
* **为什么？** 这是 React 故意设计的，目的是帮你测试**清理函数（Cleanup Function）是否写得完善**。
* **生产环境（Build 后）** 只会执行一次，不用担心。

---

### 总结口诀

1. **想在加载/销毁/变量变化时做点事？** $\rightarrow$ 用 `useEffect`。
2. **需要清理定时器/监听器？** $\rightarrow$ 在 `useEffect` 里 `return () => {}`。
3. **渲染时就能直接算出来的变量？** $\rightarrow$ **不要**用 `useEffect`（派生类对应的例子）。
4. **用户点击按钮触发的操作？** $\rightarrow$ 写在 `onClick` 里，**不要**用 `useEffect`。
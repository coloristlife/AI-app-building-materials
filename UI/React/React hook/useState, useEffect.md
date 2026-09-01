

```ts
function useToast() {

const [state, setState] = React.useState<State>(memoryState)

  

React.useEffect(() => {

	listeners.push(setState)

	return () => {
	
		const index = listeners.indexOf(setState)
		
		if (index > -1) {
		
		listeners.splice(index, 1)
	
	}
	
	}

}, [state])

  

return {

	...state,
	
	toast,
	
	dismiss: (toastId?: string) => dispatch({ type: "DISMISS_TOAST", toastId }),

}

}
```
### **Overview**
This is a custom React hook (commonly used in UI libraries like **shadcn/ui**) that manages popup notifications ("toasts"). 

It allows **any component in your app** to create, view, or dismiss toasts, keeping all components synced using a shared global state outside of React Context.

---

### **Line-by-Line Breakdown**

## 1 Setting Up State
```typescript
const [state, setState] = React.useState<State>(memoryState)
```
* **What it does:** Creates a local React state for the component using this hook.
* **Initial Value:** It loads its starting value from `memoryState` (a variable shared globally outside this component).

`setState` isn't something written anywhere in this file. It's **created and returned by React itself**, from the call to `React.useState(memoryState)` on line 175.

`useState` returns an array of exactly two things: `[currentValue, updaterFunction]`. React generates that `updaterFunction` internally — it's a closure that knows which component instance it belongs to and how to trigger that component's re-render. You never define its body; you just destructure it out and give it a name (here, `setState`).

So the naming is entirely up to you — `const [state, setState] = React.useState(...)` and `const [count, setCount] = React.useState(...)` are the identical mechanism, just with different variable names chosen at the destructuring site. React doesn't care what you call them; it only cares about the _position_ in the array (first = value, second = setter).

---

## 2 Subscribing to Global Updates (The Listener Pattern)
```typescript
React.useEffect(() => {
  listeners.push(setState)
  return () => {
    const index = listeners.indexOf(setState)
    if (index > -1) {
      listeners.splice(index, 1)
    }
  }
}, [state])
```
* **Adding to listeners (`listeners.push(setState)`):** Registers this component’s `setState` function into a global `listeners` array. When a toast is added or removed anywhere in the app, the system loops through `listeners` and calls `setState`, causing this component to update automatically.
> **把当前这个 React Component 的“更新函数”登记到一个全局名单里，以后外部发生变化时，可以通过这个名单通知它重新渲染。**

你可以把 `listeners` 理解成一个**通知名单 / 订阅者列表**。

在 React 里，**`useEffect` 的执行时机**可以先记住一句话：

> **Component render 完成、DOM 更新之后，React 才会执行 `useEffect`。**

也就是说，它**不是在 render 的过程中执行**。
第一次加载时，大致是：

```
Component 开始 render
       ↓
执行 App()
       ↓
得到 JSX
       ↓
React 更新 DOM
       ↓
浏览器准备显示
       ↓
执行 useEffect
```



* **Cleanup (`return () => ...`):** When the component unmounts (leaves the screen), it removes its `setState` function from the `listeners` array. This prevents memory leaks and avoids trying to update a component that is no longer visible.

### State 什么时候变化：


`state` 在 `useToast()` 内部是通过 `React.useState(memoryState)` 声明的局部状态，它的值只在 **`setState` 被调用时**才会变化——而这里 `setState` 只有一个地方会被调用：`dispatch` 函数内部。

### 具体触发链条

```
function dispatch(action) {
  memoryState = reducer(memoryState, action)   // 1. 计算出新的 memoryState
  listeners.forEach((listener) => listener(memoryState))  // 2. 依次调用每个订阅者的 setState
}
```

而 `dispatch` 会在这三种情况下被调用：

1. 调用 `toast({...})` 时 → 内部 `dispatch({ type: "ADD_TOAST", ... })`
2. 调用某个 toast 的 `handle.update({...})` 时 → `dispatch({ type: "UPDATE_TOAST", ... })`
3. 调用 `dismiss()` 或 `handle.dismiss()` 时 → `dispatch({ type: "DISMISS_TOAST", ... })`
4. 以及那个延迟队列 `addToRemoveQueue` 里的 `setTimeout` 到期后 → `dispatch({ type: "REMOVE_TOAST", ... })`

所以完整链条是：

```
你调用 toast(...) / update(...) / dismiss(...)
        │
        ▼
   dispatch(action) 被调用
        │
        ▼
memoryState = reducer(memoryState, action)   // 产生一个全新的对象
        │
        ▼
listeners.forEach(listener => listener(memoryState))
        │
        ▼
每个订阅了的组件里，那个组件自己的 setState(memoryState) 被执行
        │
        ▼
该组件的 state 变了 → 触发重新渲染 → 也顺带重新触发了那个 [state] 依赖的 useEffect
```

一句话总结：**`state` 本身不会自己变化**，它只在别处（任意地方）调用了 `toast`/`update`/`dismiss` 从而间接触发 `dispatch` 时，被 `dispatch` 通过 `listeners` 数组"推"着变了一次。这也是为什么这个 hook 能做到"在 A 组件里点按钮，B 组件的 toast 列表也跟着更新"——因为 B 组件的 `setState` 也在 `listeners` 里，同样会被 `dispatch` 调用到。

这个质疑很有道理——让我们精确地界定一下这里“全局（global）”的意思，因为你说的对，它并不是 `window.listeners` 这种挂载在 window 上的全局变量。

## `listeners` 到底存在于哪里

`listeners` 是在 **`use-toast.ts` 文件的最外层（顶层）** 使用 `const` 声明的，位于任何函数之外。这使得它属于**模块作用域（module-scoped）**，而不是 window 全局变量。只有该文件内部的代码才能直接引用 `listeners` 这个变量名。
```
const listeners: Array<(state: State) => void> = []
```

## 为什么它依然像是一个全应用共享的/全局的 Store

JavaScript 模块有一个关键特性：**无论有多少其他文件导入（import）它，模块文件只会被执行一次**。当第一次有代码执行 `import { useToast } from "./use-toast"` 时，Node 或打包工具（bundler）会从头到尾严格执行一次 `use-toast.ts`，创建出 `listeners = []` 和 `memoryState = {...}`，然后将这个结果缓存起来。之后任何其他文件进行的每一次 `import`，获取到的都是**同一个已经创建好的模块引用**，而不是重新复制一份。

所以：
- `ComponentA.tsx` 执行 `import { toast } from "@/hooks/use-toast"`
- `ComponentB.tsx` 执行 `import { useToast } from "@/hooks/use-toast"`

两者都是从**同一个已执行的模块实例**中导入的。A 中使用的 `toast()` 和 B 中使用的 `useToast()` 都是闭包，它们在内存中看到的是完全相同的 `listeners` 数组和 `memoryState` 变量——因为从头到尾只有一份在首次导入时创建的副本。

## 真正重要的对比

真正重要的区别并不是“模块作用域 vs. window 全局作用域”，而是**“模块作用域 vs. 组件作用域”**：
- 如果 `listeners` 是在 `useToast()` 函数体*内部*声明的（或者在组件内部使用 `useState`/`useRef`），那么每个组件实例都会拥有**属于自己的独立副本**，它们永远无法看到彼此的修改。
- 但因为它是在所有函数*之外*、也就是模块顶层声明的，所以全内存中只有唯一的一份副本被所有导入者共享——因此，即便它没有挂载到 `window` 上，在功能上也起到了“应用级全局共享”的作用。

这就是为什么我之前称它为共享/全局 Store——第一次没有明确指出它是“模块作用域单例（module-scoped singleton）”确实不够严谨，这才是最准确的术语。通过这种模块缓存机制（首次 import 执行一次文件，之后的 import 复用它）来实现状态共享，逻辑是否清晰易懂了？

---

## 3 Returning Tools to the Component
```typescript
return {
  ...state,
  toast,
  dismiss: (toastId?: string) => dispatch({ type: "DISMISS_TOAST", toastId }),
}
```
This hook returns an object containing:
1. **`...state`**: The current list of toasts (and any other toast-related settings).
2. **`toast`**: A helper function you can call to create a new toast (e.g., `toast({ title: "Saved!" })`).
3. **`dismiss`**: A function to hide a specific toast by its ID (or hide all toasts if no ID is provided).

---

### **Summary of How It Works in Practice**

1. You call `const { toast, toasts } = useToast()` in your component.
2. The component subscribes to the global `listeners` list.
3. If you call `toast({ title: "Hello" })` anywhere in the app, the global store updates `memoryState` and notifies all registered `listeners`.
4. Your component automatically re-renders with the latest toast list.
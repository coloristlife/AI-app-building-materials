
`setState` **is** in this file, and it **is** being called! 

It might look like it's missing because it gets called **indirectly** through the `listeners` array under a different name (`listener`).

Here is step-by-step proof of where `setState` is created, stored, and called, followed by why it is necessary.

---

### 1. Where `setState` comes from and where it is called

Trace these 3 parts in your code:

#### **Step 1: `setState` is created**
Inside `useToast()`:
```typescript
const [state, setState] = React.useState<State>(memoryState)
```
React creates the `setState` function for whichever component called `useToast()`.

---

#### **Step 2: `setState` is saved into an array**
Inside the `useEffect` of `useToast()`:
```typescript
listeners.push(setState)
```
Instead of calling `setState` immediately, the hook stores `setState` inside the `listeners` array defined at the top of the file: `const listeners = []`.

---

#### **Step 3: `setState` IS CALLED here!**
Inside the `dispatch` function:
```typescript
listeners.forEach((listener) => {
  listener(memoryState) // 👈 THIS IS CALLING setState(memoryState)!
})
```
When `dispatch` loops through `listeners`, each `listener` in that array **is** one of the `setState` functions pushed in Step 2. 

Calling `listener(memoryState)` is literally executing `setState(memoryState)`.

---

### 2. Why do we need `setState` here?

`memoryState` is just a normal, plain JavaScript object living in memory.

If you change `memoryState` (for example, adding a new toast), **React has no idea that anything changed.** A JavaScript object changing will **never** trigger a UI re-render on its own.

#### Without `setState`:
1. You call `toast({ title: "Hello" })`.
2. `memoryState` gets updated in JavaScript memory.
3. **Nothing happens on screen.** The toast never appears because React doesn't know it needs to redraw the component.

#### With `setState`:
1. You call `toast({ title: "Hello" })`.
2. `memoryState` gets updated.
3. `dispatch` loops through `listeners` and calls `setState(memoryState)`.
4. React receives the `setState` signal and **re-renders your UI**, displaying the toast on screen.

### Summary
`setState` is the **bridge** that connects the plain JavaScript `memoryState` to React's rendering system. Without it, your toasts would exist in code memory, but users would never see them on screen.


----
#  Immutability with Objects and Arrays inside [[useState]]

在这套代码中，不可变性（Immutability）是通过 **`reducer` 函数** 来严格保证的。

我们来分析一下它是如何一步步做到符合 React 的不可变性要求的：

---

### 1. `reducer` 每次都返回一个全新引用的对象

React 的 `setState` 依赖**浅比较（Shallow Comparison / `Object.is`）**来判断数据是否改变。如果引用的内存地址没变，React 就认为数据没变，不会刷新 UI。

在这段代码中，`reducer` 的每一个分支都使用了**浅拷贝**和**非破坏性数组方法**，确保每次都生成全新的对象和全新的数组：

#### 示例 1：添加 Toast (`ADD_TOAST`)
```typescript
return {
  ...state, // 1. 展开旧 state，创建一个新的 state 对象
  toasts: [action.toast, ...state.toasts].slice(0, TOAST_LIMIT), 
  // 2. 用数组展开运算符 [...] 创建一个全新的 toasts 数组
}
```
* 没有使用 `push()`（这会修改原数组）。
* 使用了 `[action.toast, ...state.toasts]`，生成了一个**全新的数组内存地址**。

#### 示例 2：更新 Toast (`UPDATE_TOAST`)
```typescript
return {
  ...state,
  toasts: state.toasts.map((t) => // .map() 永远返回一个全新数组
    t.id === action.toast.id 
      ? { ...t, ...action.toast } // 创建全新的 Toast 对象
      : t
  ),
}
```
* 没有直接修改原对象（如 `t.title = "xxx"`）。
* 使用 `.map()` 返回新数组，配合 `{ ...t, ...action.toast }` 返回全新的 Toast 单体对象。


这段代码是 JavaScript/TypeScript 中用于**更新数组中某个特定对象**的最经典写法。

简单来说，它的意思是：
> **“找到那个要修改的 Toast，把新数据合并进去；至于其他不需要修改的 Toast，保持原样不动。”**

---

##### 一、 拆解三元运算符 (`条件 ? 成立时 : 不成立时`)

这段代码包含三个部分：

```typescript
  条件判断                     如果成立（是我们要找的 Toast）     如果不成立（不是要找的 Toast）
👇-------------------👇       👇-------------------------👇   👇--👇
t.id === action.toast.id  ?   { ...t, ...action.toast }   :   t
```

---

##### 二、 核心语法逐项剖析

###### 条件部分：`t.id === action.toast.id`
* **含义**：判断当前遍历到的 Toast（`t`）的 ID，是否等于你想更新的那个 Toast 的 ID。

###### 如果成立（`?` 后面）：`{ ...t, ...action.toast }`
这是最精彩的部分，用到了 **对象展开运算符（Spread Operator `...`）**。

它的合并逻辑是：
1. `...t`：把原 Toast 的**所有旧属性**解构复制一份放进来（比如 `id`, `open`, `title` 等）。
2. `...action.toast`：把**想要更新的新属性**解构复制放进来。
3. **同名覆盖**：如果新数据和旧数据有同名的属性（例如 `title` 从 `"加载中..."` 变成了 `"成功！"`），**后面的新属性会覆盖掉前面的旧属性**；而没有传的新属性（例如 `id`）则会原样保留。

###### 如果不成立（`:` 后面）：`t`
* **含义**：如果当前 Toast 的 ID 对不上，说明它不是我们要修改的对象，直接返回原来的 `t`，不做任何更改。

---

##### 三、 举个具体的例子

假设你现在屏幕上有两个 Toast：

**当前状态（`state.toasts`）：**
```javascript
[
  { id: "1", title: "正在上传文件...", open: true },
  { id: "2", title: "欢迎回来", open: true }
]
```

现在你想把 ID 为 `"1"` 的 Toast 标题改成 `"上传成功！"`，你派发了一个 action：
```javascript
action.toast = { id: "1", title: "上传成功！" }
```

当 `.map()` 遍历这个数组时：

1. **遍历到第 1 个 Toast（`id: "1"`）：**
   * 条件 `t.id === "1"` 成立！
   * 执行 `{ ...t, ...action.toast }`
   * 合并结果：`{ id: "1", title: "上传成功！", open: true }` （`open: true` 被保留了，`title` 被更新了）。

2. **遍历到第 2 个 Toast（`id: "2"`）：**
   * 条件 `t.id === "1"` 不成立（因为它的 id 是 "2"）。
   * 直接返回原样 `t`：`{ id: "2", title: "欢迎回来", open: true }`。

**最后得到的新数组：**
```javascript
[
  { id: "1", title: "上传成功！", open: true }, // 恰到好处地修改了
  { id: "2", title: "欢迎回来", open: true }   // 完好无损地保留了
]
```

---

##### 总结
这种写法既保证了**只修改目标对象**，又通过创建全新的对象和数组满足了 React 的**不可变性要求（Immutability）**。

#### 示例 3：删除 Toast (`REMOVE_TOAST`)
```typescript
return {
  ...state,
  toasts: state.toasts.filter((t) => t.id !== action.toastId), // .filter() 永远返回全新数组
}
```
* 没有使用 `splice()`（这会改变原数组）。
* 使用 `.filter()` 过滤出符合条件的新数组。

---

### 2. `dispatch` 重新赋值并触发 `setState`

当你在代码里调用 `toast()` 时，流程如下：

```typescript
function dispatch(action: Action) {
  // 1. reducer 执行，返回一个全新的不可变对象，覆盖 memoryState
  memoryState = reducer(memoryState, action) 

  // 2. 遍历调用每一个组件的 setState(memoryState)
  listeners.forEach((listener) => {
    listener(memoryState)
  })
}
```

#### React 内部接收到 `setState(memoryState)` 时发生了什么？
1. React 比较 `组件旧的 state` 和 `新的 memoryState` 的内存地址：
   $$\text{旧地址} \neq \text{新地址} \quad (\text{因为 } \text{reducer} \text{ 返回了新对象})$$
2. React 判定：“**数据确实变了！**”
3. React 触发组件的重新渲染，将最新的 Toast 顺利绘制到屏幕上。

---

### 总结

这段代码完全遵循了 **Immutability（不可变性）** 原则：
1. **不直接修改原变量**：不使用 `push`、`splice` 或直接给对象属性赋值（如 `state.toasts = ...`）。
2. **纯函数返回新引用**：通过 `...` 展开运算符、`.map()`、`.filter()` 生成新对象/新数组。
3. **保证 React 能感知变化**：全新的内存地址让 `setState` 能够成功触发 UI 重新渲染。


original code :
```ts
"use client"

  

// Inspired by react-hot-toast library

import * as React from "react"

  

import type {

ToastActionElement,

ToastProps,

} from "@/components/ui/toast"

  

const TOAST_LIMIT = 1

const TOAST_REMOVE_DELAY = 1000000

  

type ToasterToast = ToastProps & {

id: string

title?: React.ReactNode

description?: React.ReactNode

action?: ToastActionElement

}

  

const actionTypes = {

ADD_TOAST: "ADD_TOAST",

UPDATE_TOAST: "UPDATE_TOAST",

DISMISS_TOAST: "DISMISS_TOAST",

REMOVE_TOAST: "REMOVE_TOAST",

} as const

  

let count = 0

  

function genId() {

count = (count + 1) % Number.MAX_SAFE_INTEGER

return count.toString()

}

  

type ActionType = typeof actionTypes

  

type Action =

| {

type: ActionType["ADD_TOAST"]

toast: ToasterToast

}

| {

type: ActionType["UPDATE_TOAST"]

toast: Partial<ToasterToast>

}

| {

type: ActionType["DISMISS_TOAST"]

toastId?: ToasterToast["id"]

}

| {

type: ActionType["REMOVE_TOAST"]

toastId?: ToasterToast["id"]

}

  

interface State {

toasts: ToasterToast[]

}

  

const toastTimeouts = new Map<string, ReturnType<typeof setTimeout>>()

  

const addToRemoveQueue = (toastId: string) => {

if (toastTimeouts.has(toastId)) {

return

}

  

const timeout = setTimeout(() => {

toastTimeouts.delete(toastId)

dispatch({

type: "REMOVE_TOAST",

toastId: toastId,

})

}, TOAST_REMOVE_DELAY)

  

toastTimeouts.set(toastId, timeout)

}

  

export const reducer = (state: State, action: Action): State => {

switch (action.type) {

case "ADD_TOAST":

return {

...state,

toasts: [action.toast, ...state.toasts].slice(0, TOAST_LIMIT),

}

  

case "UPDATE_TOAST":

return {

...state,

toasts: state.toasts.map((t) =>

t.id === action.toast.id ? { ...t, ...action.toast } : t

),

}

  

case "DISMISS_TOAST": {

const { toastId } = action

  

// ! Side effects ! - This could be extracted into a dismissToast() action,

// but I'll keep it here for simplicity

if (toastId) {

addToRemoveQueue(toastId)

} else {

state.toasts.forEach((toast) => {

addToRemoveQueue(toast.id)

})

}

  

return {

...state,

toasts: state.toasts.map((t) =>

t.id === toastId || toastId === undefined

? {

...t,

open: false,

}

: t

),

}

}

case "REMOVE_TOAST":

if (action.toastId === undefined) {

return {

...state,

toasts: [],

}

}

return {

...state,

toasts: state.toasts.filter((t) => t.id !== action.toastId),

}

}

}

  

const listeners: Array<(state: State) => void> = []

  

let memoryState: State = { toasts: [] }

  

function dispatch(action: Action) {

memoryState = reducer(memoryState, action)

listeners.forEach((listener) => {

listener(memoryState)

})

}

  

type Toast = Omit<ToasterToast, "id">

  

function toast({ ...props }: Toast) {

const id = genId()

  

const update = (props: ToasterToast) =>

dispatch({

type: "UPDATE_TOAST",

toast: { ...props, id },

})

const dismiss = () => dispatch({ type: "DISMISS_TOAST", toastId: id })

  

dispatch({

type: "ADD_TOAST",

toast: {

...props,

id,

open: true,

onOpenChange: (open) => {

if (!open) dismiss()

},

},

})

  

return {

id: id,

dismiss,

update,

}

}

  

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

  

export { useToast, toast }
```
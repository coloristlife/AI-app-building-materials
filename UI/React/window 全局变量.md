在浏览器端的 JavaScript 中，`window` 是浏览器提供给你的**最顶层全局对象**（Global Object）。它代表了当前的浏览器窗口或标签页。

所谓的 **`window` 全局变量**，就是**直接挂载在 `window` 对象上的变量或属性**。

---

### 1. 它的核心特点：任何地方都能直接用，无需 `import`

只要一个变量成了 `window` 全局变量，**在这个网页的任何文件、任何函数、任何组件里**，你不需要做任何 `import`（导入），就可以直接读取或修改它。

#### 示例：
```javascript
// 方式一：显式挂载到 window 上
window.userLanguage = "zh-CN";

// 方式二：在传统的脚本（非 ES Module）的最外层用 var 声明
var siteName = "我的博客"; // 会自动变成 window.siteName
```

在项目的**其他任何文件**里，你可以直接这么用：
```javascript
// 无论在哪个 .js 或 .tsx 文件里，都能直接访问：
console.log(window.userLanguage); // 输出: "zh-CN"
console.log(userLanguage);        // 甚至可以省略 "window."，直接写变量名！
```

---

### 2. 结合上一问：它和“模块作用域”有什么区别？

上一问提到的 `use-toast.ts` 里的 `const listeners = []`，和 `window` 全局变量形成了鲜明的对比：

| 特性 | `window` 全局变量 (`window.listeners`) | 模块作用域 (`const listeners` 在文件顶层) |
| :--- | :--- | :--- |
| **生性范围** | **完全公开**（大广场） | **文件内部私有**（封闭的房间） |
| **如何访问** | 任何文件不需要 `import`，直接拿来用 | 只有 `use-toast.ts` 文件内部能看得到这个变量 |
| **对外暴露** | 无法控制，谁都可以修改它 | 只能通过该文件 `export` 出来的函数（如 `useToast`）间接操作 |
| **安全程度** | 极低（容易被其他库覆盖或篡改） | 极高（变量名被封装在模块内部） |

#### 形象的比喻：
* **`window` 全局变量**：就像把钥匙扔在**小区的大广场中央**。任何路人（包括第三方插件、你自己写的其他代码）都能捡起来，甚至不小心把它踹飞（重写覆盖）。
* **模块作用域变量**：就像把钥匙放在**你的私人房间里**。外面的人根本不知道这把钥匙的存在，只能敲门让房主人（`toast()` 函数）帮他们开门。

---

### 3. 为什么现代前端（React / Vue）尽量避免使用 `window` 全局变量？

在早期的网页开发中（比如 jQuery 时代），`window` 全局变量非常常见（比如 `window.$`）。但在现代开发中，大家尽量避免使用它，原因有三点：

1. **命名冲突（全局污染）：**
   如果你定义了 `window.user = "Alex"`，而你引入的一个第三方 npm 包也写了 `window.user = "Admin"`，后写的就会**直接覆盖**掉先写的，导致难以排查的 Bug。

2. **难以追踪代码来源：**
   如果你在某个页面看到一行 `console.log(currentUser)`，由于它没有 `import` 语句，你根本不知道这个 `currentUser` 是在哪个文件的哪一行被创建或修改的。

3. **破坏服务端渲染（SSR，如 Next.js）：**
   React 框架（如 Next.js）会在服务器端（Node.js 环境）先运行一遍你的代码。**Node.js 环境里是没有 `window` 对象的！** 
   如果你在代码里直接写了 `window.xxx`，服务器就会直接报错崩溃：`ReferenceError: window is not defined`。
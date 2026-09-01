```ts
  

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
```

---

### **Overview**
A **reducer** is a function that decides how the application state should change based on an action you trigger. 

This specific reducer manages the **lifecycle of toasts**: adding them, updating their contents, hiding them (dismissing), and completely deleting them from memory.

---

### **Action-by-Action Breakdown**

#### 1. `ADD_TOAST`
```typescript
case "ADD_TOAST":
  return {
    ...state,
    toasts: [action.toast, ...state.toasts].slice(0, TOAST_LIMIT),
  }
```
* **What it does:** Adds a new toast to the **front** of the list (so newer toasts show up on top/first).
* **The Limit:** `.slice(0, TOAST_LIMIT)` ensures the screen doesn't get flooded. If `TOAST_LIMIT` is set to `3`, it keeps only the 3 newest toasts and drops any older ones.

---

#### 2. `UPDATE_TOAST`
```typescript
case "UPDATE_TOAST":
  return {
    ...state,
    toasts: state.toasts.map((t) =>
      t.id === action.toast.id ? { ...t, ...action.toast } : t
    ),
  }
```
* **What it does:** Updates the properties of an existing toast (e.g., changing its message, title, or status from "Loading..." to "Success!").
* **How:** It searches the `toasts` array for the toast with a matching `id` and merges the new data into it.

---

#### 3. `DISMISS_TOAST`
```typescript
case "DISMISS_TOAST": {
  const { toastId } = action

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
        ? { ...t, open: false }
        : t
    ),
  }
}
```
* **What it does:** Closes/hides the toast visually without immediately deleting it from state.
* **If a `toastId` is provided:** It dismisses just that specific toast.
* **If NO `toastId` is provided (`undefined`):** It dismisses **all** active toasts.
* **Why set `open: false` instead of deleting?** Setting `open: false` allows UI animations (like a fade-out or slide-out effect) to run before the toast is completely removed.
* **`addToRemoveQueue(...)`**: Schedules a timer to trigger a `REMOVE_TOAST` action shortly after the closing animation finishes.

---

#### 4. `REMOVE_TOAST`
```typescript
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
```
* **What it does:** Completely deletes the toast from the React state array.
* **If no `toastId`:** Clears all toasts completely (`toasts: []`).
* **If `toastId` is specified:** Filters out that specific toast from the array.

---

### **Summary of a Toast's Life Cycle**

1. **`ADD_TOAST`**: A toast is created and shown on screen (`open: true`).
2. **`UPDATE_TOAST`** *(optional)*: Toast content or state gets updated while visible.
3. **`DISMISS_TOAST`**: Toast closes visually (`open: false`) to trigger a exit animation, and gets added to a removal queue.
4. **`REMOVE_TOAST`**: Once the exit animation finishes, the toast is wiped out of state memory completely.
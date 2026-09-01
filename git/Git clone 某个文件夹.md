Git 本身没有传统意义上的“只 clone 某个文件夹”的普通 `git clone` 参数，但有几种方法。

### 1. 最推荐：Sparse Checkout

如果你想保留 Git 仓库能力，但只下载某一个目录：

```bash
git clone --filter=blob:none --no-checkout https://github.com/USER/REPO.git
cd REPO

git sparse-checkout init --cone
git sparse-checkout set path/to/folder

git checkout
```

例如：

```bash
git clone --filter=blob:none --no-checkout https://github.com/anthropics/skills.git
cd skills

git sparse-checkout init --cone
git sparse-checkout set skills/skill-creator
git checkout
```

最终本地只会看到：

```text
REPO/
└── skills/
    └── skill-creator/
```

这种方式特别适合你现在这种 **GitHub repo 里只想拿一个 Skill 文件夹** 的场景。

---

### 2. GitHub 网页直接下载一个文件夹

GitHub 网页本身通常不能直接下载单个 folder。

可以使用：

```text
https://download-directory.github.io/
```

把 GitHub 文件夹 URL 粘进去，它会把这个目录打包下载。

不过这不是 Git clone，下载下来之后没有 Git history。

---

### 3. 如果你只想拿文件，不需要 Git

可以直接：

```bash
curl -O https://raw.githubusercontent.com/USER/REPO/main/path/to/file
```

但如果是一个文件夹，里面有很多文件，Sparse Checkout 更合适。

---

### 4. 如果你只想要某个 folder，并且以后还要 `git pull`

**强烈推荐 Sparse Checkout：**

```bash
git clone --filter=blob:none --no-checkout <repo-url>
cd <repo>

git sparse-checkout init --cone
git sparse-checkout set <folder>
git checkout
```

之后正常：

```bash
git pull
```

就可以了。

**简单理解：**

|方法|只下载目标目录|保留 Git|后续 pull|推荐|
|---|--:|--:|--:|--:|
|`git clone`|❌|✅|✅|⭐|
|Sparse Checkout|✅|✅|✅|⭐⭐⭐⭐⭐|
|download-directory|✅|❌|❌|⭐⭐⭐|
|`curl/wget`|文件级|❌|❌|⭐⭐|

如果你告诉我具体的 **GitHub repo URL + 想 clone 的文件夹路径**，我可以直接给你一条可以复制执行的命令。

## how to merge the resports after running the shell

因为你是逐个 Probe 分开运行的，Garak 在 `resilient_scan_results` 文件夹里为你生成了大量零散的文件（每个 Probe 都有独立的 `.report.jsonl`、`.hitlog.jsonl` 和 `.html`）。

要将它们合并成**一个全局的 HTML 报告和日志**，非常简单。Garak 原生支持对多份 JSONL 报告进行聚合（因为 JSONL 的特性就是一行一个 JSON，非常适合合并）。

以下是合并所有扫描结果的标准操作流程（SOP）：

### 第一步：合并所有的原始数据 (`.report.jsonl`)
Garak 官方提供了一个内部聚合脚本 `aggregate_reports`，它可以完美合并多个报告文件并重新计算总分。

在终端中运行以下命令：
```bash
cd ~/garak_scans

# 使用 Garak 自带的分析工具合并所有的报告数据
python3 -m garak.analyze.aggregate_reports resilient_scan_results/*.report.jsonl > final_merged_scan.report.jsonl
```
*(注意：如果你运行这行代码报错，那是因为旧版本 Garak 路径不同。作为备用方案，你可以直接暴力拼接它们：`cat resilient_scan_results/*.report.jsonl > final_merged_scan.report.jsonl`)*

### 第二步：生成全局统一的 HTML 报告
现在你已经有了一个包含所有 Probe 结果的巨大 `.jsonl` 文件，你可以让 Garak 为它生成一张包含所有数据的综合 HTML 面板。

运行以下命令：
```bash
python3 -m garak.report final_merged_scan.report.jsonl
```
*(或者在某些系统/版本上使用：`python3 -m garak.analyze.report_html final_merged_scan.report.jsonl`)*

这会在当前目录下生成一个类似 `garak.<时间戳>.report.html` 的文件。这个 HTML 就是你想要的**全量扫描结果看板**。

### 第三步：合并“高危漏洞命中日志” (`.hitlog.jsonl`)
除了 HTML 报告，你肯定也想知道具体是哪些 Prompt 成功“越狱”了模型。Garak 把这些记录在 `hitlog` 里。

因为 hitlog 是纯文本，你可以直接用 Linux 的 `cat` 命令把它们无缝拼接成一个总文件：
```bash
cat resilient_scan_results/*.hitlog.jsonl > final_merged_scan.hitlog.jsonl
```

---

### 自动化合并脚本 (可选)
为了方便，你可以运行 `merge_garak_results.sh`。每次你的断点续传脚本跑完后，运行一下这个脚本，就能直接拿到最终的总报告

如果你的目标是 **RAG 中对复杂表格（Merged Cell、Nested Table）、图文混排 PDF、扫描版 PDF** 做高质量 Parsing，那么目前 GitHub 上已经形成了几条技术路线。

下面按照目前企业应用中的效果（2025-2026）来分类。

---

# 第一梯队（目前效果最好）

## 1. MinerU（原 Magic-PDF） ⭐⭐⭐⭐⭐（国内最强之一）

[MinerU GitHub](https://github.com/opendatalab/MinerU?utm_source=chatgpt.com)

这是目前国内 RAG 社区使用最多的 PDF Parser。

### 优点

* 对中文支持极好
* 表格恢复效果很好
* 图片位置保留
* OCR + Digital PDF 自动判断
* Layout Detection
* Reading Order
* Markdown 输出

例如

PDF

```
-----------------------
| image              |
-----------------------
| table              |
-----------------------
paragraph
```

输出

```
![](figure1.png)

| table |
|-------|

paragraph
```

RAG 非常舒服。

支持

* Markdown
* JSON
* HTML

---

适合

✅ 企业知识库

✅ RAG

✅ 法律文档

✅ 金融报告

---

## 2. Docling ⭐⭐⭐⭐⭐（IBM）

[Docling GitHub](https://github.com/docling-project/docling?utm_source=chatgpt.com)

这是 IBM 做的。

目前国外很多 Benchmark 第一。

特点：

几乎支持所有 Office

```
PDF

DOCX

PPT

Excel

HTML
```

统一输出

```
Docling Document
```

再导出

Markdown

JSON

HTML

Text

---

最大的优点：

对于复杂 Table

恢复率非常高。

---

Docling 内部用了

Layout Detection

Reading Order

Table Structure

OCR

Vision Model

全部串起来。

---

很多 RAG Pipeline

现在已经直接换成 Docling。

---

## 3. Marker ⭐⭐⭐⭐⭐

[Marker GitHub](https://github.com/datalab-to/marker?utm_source=chatgpt.com)

Marker 是目前 Markdown 输出最漂亮的。

特点：

PDF →

Markdown

效果极好。

支持：

* Latex
* 数学公式
* 图片
* Caption
* Table

很多论文 RAG

都在用 Marker。

---

## 4. OmniParser（Microsoft）

[OmniParser GitHub](https://github.com/microsoft/OmniParser?utm_source=chatgpt.com)

注意：

很多人误会。

OmniParser 不是 PDF Parser。

它主要解析：

GUI

Screen

Image

但是现在很多人把 PDF Page

转成 Image

再交给 OmniParser。

对于复杂页面：

效果很好。

适合：

视觉 Agent。

---

# 第二梯队（企业应用很多）

## 5. Unstructured

[Unstructured GitHub](https://github.com/Unstructured-IO/unstructured?utm_source=chatgpt.com)

这是 LangChain 最经典的。

支持

```
PDF

Word

PowerPoint

Email

HTML

Markdown
```

最大的优点：

生态。

几乎所有 Framework

都有它。

缺点：

Table 不如 MinerU。

---

## 6. LlamaParse ⭐⭐⭐⭐

[LlamaParse](https://www.llamaindex.ai/llamaparse?utm_source=chatgpt.com)

不是开源。

但是很多人拿来比较。

特点：

非常适合

复杂 PDF

尤其 Annual Report。

---

# 第三梯队（Layout Detection）

这些不是完整 Parser。

而是 Parser 组件。

---

## Layout Parser

[Layout Parser GitHub](https://github.com/Layout-Parser/layout-parser?utm_source=chatgpt.com)

做：

```
Title

Paragraph

Table

Figure

Formula
```

检测。

---

## PaddleOCR

[PaddleOCR GitHub](https://github.com/PaddlePaddle/PaddleOCR?utm_source=chatgpt.com)

OCR

中文最佳之一。

MinerU 里面大量借鉴了类似能力。

---

## Surya

[Surya GitHub](https://github.com/VikParuchuri/surya?utm_source=chatgpt.com)

OCR

Layout

Reading Order

Table

目前国外社区评价非常高。

Marker 也会结合它。

---

# 第四梯队（Table 专项）

## Table Transformer（Microsoft）

[Table Transformer GitHub](https://github.com/microsoft/table-transformer?utm_source=chatgpt.com)

微软的 Table Detection。

非常适合：

复杂表格。

---

## Camelot

[Camelot GitHub](https://github.com/camelot-dev/camelot?utm_source=chatgpt.com)

经典。

但是：

仅适合

Digital PDF。

扫描版几乎不行。

---

## pdfplumber

[pdfplumber GitHub](https://github.com/jsvine/pdfplumber?utm_source=chatgpt.com)

最经典。

适合：

程序员二次开发。

---

# 第五梯队（Vision Parser）

近年来越来越流行。

直接：

PDF →

图片 →

VLM

例如：

```
GPT-4.1

GPT-5 Vision

Qwen2.5-VL

Qwen3-VL

Gemini

Claude
```

让模型：

直接理解。

优点：

复杂表格

图片

流程图

组织结构图

全部理解。

缺点：

成本高。

---

# 企业 RAG 最佳组合（2025–2026）

如果你做企业级 RAG，我比较推荐以下组合：

| 场景                 | 推荐方案                                            | 原因                       |
| ------------------ | ----------------------------------------------- | ------------------------ |
| 中文 PDF + 表格        | MinerU                                          | 中文、OCR、表格恢复能力强           |
| 英文技术文档             | Docling                                         | 综合解析能力优秀，格式保留好           |
| 学术论文               | Marker + Surya                                  | Markdown、公式、图片效果突出       |
| 多格式企业知识库           | Docling + Unstructured                          | Office 文档生态完善            |
| 财报、合同、法律文档         | MinerU + Docling                                | 对复杂版式和长文档表现稳定            |
| 极复杂图文（流程图、组织架构、图表） | Parser + Vision Model（如 Qwen VL 或 GPT-5 Vision） | 可理解纯视觉内容，弥补传统 Parser 的不足 |

---

## 如果只推荐 **Top 5 开源 GitHub 项目**

按目前社区活跃度、解析质量和企业 RAG 实践来看，我会推荐：

1. **MinerU（Magic-PDF）** —— 中文 PDF、复杂表格、扫描件的首选。
2. **Docling（IBM）** —— 综合能力最强，适合多格式企业知识库。
3. **Marker** —— 学术论文、Markdown 输出质量优秀。
4. **Unstructured** —— RAG 生态最成熟，集成成本低。
5. **Surya** —— 高质量 OCR、版面分析和阅读顺序恢复，可作为其他 Parser 的核心组件。

如果你的目标是**复杂表格 + 图文混排 PDF 在企业 RAG 中尽可能接近人工阅读效果**，目前很多成熟方案已经不是单一 Parser，而是采用 **Docling / MinerU + Vision Language Model（如 Qwen VL 或 GPT-5 Vision）** 的两阶段架构：先恢复文档结构，再让视觉模型补充理解图表、流程图和复杂跨页表格。这也是目前越来越多企业级 RAG 系统采用的方向。

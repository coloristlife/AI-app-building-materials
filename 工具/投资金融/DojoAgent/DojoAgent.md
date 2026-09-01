# MKdocs
```
uv pip install -e ".[docs]"
```
if still facing the unknown module, install them individually.

### 重点是 `.[docs]`

假设 DojoAgents 的 `pyproject.toml` 里面定义了：

[project.optional-dependencies]

docs = [

    "mkdocs",

    "mkdocs-material",

    "mkdocs-static-i18n",

    "pymdown-extensions",

]

那么：
```
uv pip install -e ".[docs]"

```


就相当于告诉 Python：

> **把当前 DojoAgents 项目安装到当前环境中，并且把它为了构建 documentation 所需要的所有依赖也一起安装。**

after all installed run the command below:
```


mkdocs serve
```

通常会看到：

Serving on http://127.0.0.1:8000/

然后浏览器打开：

http://127.0.0.1:8000/

# Skill view
Yes. I inspected the actual `SkillManager` source, and I need to correct one important point from my previous answer:

**The DojoAgents version I inspected does not contain a `skill_view()` implementation inside `SkillManager`.** The `SkillManager` builds the skill catalog/prompt, while the actual `skill_view` tool must be implemented elsewhere in the agent/tool layer.

Here is what the source confirms.

### 1. `SkillManager` only discovers `SKILL.md`

The key code is:

```python
for root in self.skill_dirs:
    ...
    for skill_file in sorted(root.glob("*/SKILL.md")):
```

So DojoAgents expects:

```text
skills/
├── skill-a/
│   └── SKILL.md
├── skill-b/
│   └── SKILL.md
└── skill-c/
    └── SKILL.md
```

It **does not recursively search** for arbitrary nested `SKILL.md` files.

That means my earlier suggestion of arbitrary nested structures was too generous.

---

## 2. What happens when `lazy_skills=True`

This is the most interesting part.

The default is:

```python
lazy_skills=True
```

The manager initially does **not inject the complete skill content** into the prompt.

Instead it generates something conceptually like:

```text
## Available Skills (Mandatory Lazy Loader)

You have access to the following skills.
Do NOT guess their instructions.

You MUST call:
skill_view(name='<skill_name>')

before performing any workflow related to these skills.

Skill Catalog:

  Category: investment
    - stock-analysis: Analyze stocks using my investment methodology.
    - valuation: Evaluate company valuation.
```

This behavior is directly visible in the source.

So the architecture is:

```text
                 System Prompt
                      │
                      ▼
              Skill Catalog
             name + description
                      │
                      │ Agent decides skill is relevant
                      ▼
                skill_view()
                      │
                      ▼
                 SKILL.md
                      │
                      ▼
                 Agent executes
```

That's a good **progressive-disclosure** design.

---

## 3. But where is `skill_view()`?

This is the part we haven't established yet from the `SkillManager` source.

The manager literally tells the LLM:

> `You MUST call skill_view(name='<skill_name>')`

but `SkillManager` itself doesn't define that function.

So there must be another layer responsible for registering/executing that tool.

This is important because **that implementation determines whether DojoAgents actually supports the richer Agent Skills structure**:

```text
my-skill/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

The `SkillManager` source we inspected only reads:

```text
SKILL.md
```

It does **not** itself load:

```text
references/*
scripts/*
assets/*
```

So we shouldn't yet assume those are automatically supported.

---

## 4. What DojoAgents definitely supports

From the source:

### Custom skill directories

Yes:

```python
SkillManager(skill_dirs=[...])
```

The constructor explicitly accepts `skill_dirs`.

### YAML frontmatter

Yes.

It parses:

```yaml
---
name: stock-analysis
description: Analyze stocks...
category: investment
---
```

using YAML.

### Categories

Yes:

```yaml
category: investment
```

The category is used when constructing the skill catalog.

### Tool requirements

This is particularly interesting:

```yaml
requires_tools:
  - market_data
  - calculator
```

The source checks `requires_tools` against the tools loaded in the agent.

So your investment skill could potentially say:

```yaml
---
name: stock-analysis
description: Analyze individual stocks using my investment methodology.
category: investment
requires_tools:
  - market_data
  - financial_calculator
---
```

and DojoAgents can exclude that skill if those tools aren't available.

### Platform restrictions

It also supports:

```yaml
platforms:
  - linux
```

or similar platform declarations.

---

## 5. For your investment use case, this is actually quite nice

You could create:

```text
my-investment-skills/
│
├── stock-analysis/
│   └── SKILL.md
│
├── valuation-analysis/
│   └── SKILL.md
│
├── portfolio-analysis/
│   └── SKILL.md
│
├── risk-analysis/
│   └── SKILL.md
│
└── investment-decision/
    └── SKILL.md
```

Then initialize DojoAgents with something conceptually like:

```python
SkillManager(
    skill_dirs=[
        "./my-investment-skills"
    ]
)
```

The agent initially gets only:

```text
stock-analysis
valuation-analysis
portfolio-analysis
risk-analysis
investment-decision
```

and their descriptions.

When it decides it needs `stock-analysis`, it calls:

```text
skill_view("stock-analysis")
```

and loads the detailed instructions.

---

## 6. But I would NOT put your entire investment experience into these skills

This source-code inspection reinforces the architecture we discussed earlier.

I'd separate:

```text
                  Your Investment System
                           │
           ┌───────────────┴───────────────┐
           │                               │
        Skills                         Knowledge
           │                               │
      "How I think"                 "What I learned"
           │                               │
           ▼                               ▼
      SKILL.md                         Personal KB
           │                               │
           └───────────────┬───────────────┘
                           │
                           ▼
                      DojoAgents
                           │
                      Agent Harness
```

For example:

### Skill

```text
How I evaluate a company
```

### Personal KB

```text
In 2019 I observed this pattern...
In 2021 this assumption failed because...
When revenue grows but FCF deteriorates...
```

### Tool

```text
Calculate DCF
Calculate CAGR
Calculate drawdown
Get current financial data
```

### Memory

```text
Why I bought NVDA
Why I sold AAPL
What mistakes I made
```

That's much more powerful than one huge `SKILL.md`.

---

## 7. One important conclusion about Agent Skills compatibility

At this point I would **not yet say that DojoAgents is fully Agent Skills-spec compatible**.
MK
What we can confidently say from the source is:

> **DojoAgents implements its own SKILL.md-based skill system with YAML metadata, custom skill directories, tool requirements, categories, platform filtering, caching, and lazy loading.**

That's very similar to the Agent Skills concept.

But we still need to inspect the actual **`skill_view` implementation** before we can answer whether this works:

```text
my-skill/
├── SKILL.md
├── references/
│   ├── valuation.md
│   └── examples.md
├── scripts/
│   └── calculate_dcf.py
└── assets/
```

and, specifically, whether:

```text
skill_view("stock-analysis", "references/valuation.md")
```

is supported.

### So the next source-code target is clear

We need to trace:

```text
skill_view
   ↓
tool registration
   ↓
tool execution
   ↓
SkillManager / file loading
```

**That will give us the definitive answer on how to embed your existing AgentSkills/Goose skills into DojoAgents, including `references/` and `scripts/`.**
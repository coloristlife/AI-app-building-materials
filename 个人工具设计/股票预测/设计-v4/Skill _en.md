---
name: investment-rule-router
description: Route a user's natural-language description of a stock/market situation to one or more matching Investment Rules from their personal rule library, work out what info is still missing to evaluate those rules, ask for it all in one batched question (not one question per rule), then evaluate every matched rule in parallel and flag conflicts between their suggested actions. Use whenever the user describes a trading situation (price position, volume, candlestick pattern, sentiment, account/position status, consecutive losses, etc.) and asks "what should I do" or "which rule applies here". Also use to add a new rule to the library or list matching rules. Do not use for general market questions unrelated to the user's rule library, or for drafting a brand-new rule alone (separate task) unless routing/evaluation is also wanted.
---

# Investment Rule Router

This skill turns a user's personal Investment Rule library (each rule follows the 7-part
Rule Contract: Purpose / Applicability / Required Inputs / Evidence Source / Evaluation /
Output / Limitations) into something *usable* in a live conversation: given a plain-language
description of a market situation, it finds every rule that could apply, works out what's
still missing to actually evaluate them, asks the user for the missing pieces **once, in one
batch**, and then evaluates everything together — surfacing any place where two matched rules
give contradictory advice.

The full rule library, the canonical (deduplicated) input schema, and the known conflict
matrix live in `references/rule_library.md`. Load that file before doing any matching or
evaluation — it is the source of truth, not this file.

## Core principle: one query can, and often does, match multiple rules

Do not look for a single "best" rule. A real trading situation almost always sits at the
intersection of several dimensions (price position, volume, sentiment, account discipline
state), and the rule library was deliberately built with one rule per dimension rather than
one giant rule. Treat "how many rules matched" as an open question you answer empirically
each time, not something to minimize.

## Workflow

Follow these steps in order every time the skill triggers. Do not skip the batching step —
it is the entire point of this skill; asking the user the same underlying question five times
in five different rules' wording is the failure mode this skill exists to prevent.

### Step 1 — Extract situation tags

Read `references/rule_library.md` → "Situation Tag Vocabulary". Tag the user's message against
every dimension it plausibly touches (price position, volume, price speed, candle pattern,
consolidation, timing, sentiment, news, MA250 trend, stock-type, account/position state). A
single sentence commonly produces tags across 3–5 dimensions at once — that's expected, not a
sign of over-tagging.

If the message is too vague to produce *any* tag (e.g. "should I buy this stock"), do not
guess — ask one clarifying question about the situation itself before going further, per the
Rule Contract's ambiguity-handling principle (make the minimum necessary interpretation, or
mark as UNKNOWN — never invent thresholds the user never gave).

### Step 2 — Match candidate rules

Read `references/rule_library.md` → "Rule Index" table. A rule is a candidate if its trigger
tags have non-empty intersection with the tags extracted in Step 1. Return **all** candidates,
not just the top match. For each, note whether the match is "full" (every trigger tag for that
rule is present) or "partial" (some trigger tags present, others unknown/need confirmation).

If zero rules match, say so plainly and ask what's missing — don't force a match.

### Step 3 — Aggregate required inputs (dedup pass)

Read `references/rule_library.md` → "Canonical Input Schema". For every candidate rule from
Step 2, look up its Required Inputs and map each one onto the shared field IDs in that schema.
Union the field lists across all candidate rules — this union, not any single rule's input
list, is what you actually need to fill.

This is the step that prevents redundant questions: e.g. `price_position` is needed by ~6
different rules but should only ever be resolved/asked once per conversation turn.

### Step 4 — Resolve what you can without asking

For every field in the deduplicated union, resolve in this priority order (this mirrors the
Rule Contract's own Input Resolution Rule):

1. **Already stated in the user's message** — use it directly, don't re-ask.
2. **Evidence source = MARKET_DATA / NEWS_DATA / DERIVED** — try to obtain or compute it
   yourself (use web_search / any available market-data tool for price, volume, moving
   averages, news; compute derived fields like "price position" or "volume ratio" from raw
   data you can obtain). Only fall through to asking the user if the tool genuinely can't get
   it (e.g. no market-data tool available, or the ticker isn't identified).
3. **Evidence source = USER_CONTEXT / USER_CONFIRMATION** — these can only come from the
   user (position size, entry cost, total capital, recent trade results, original thesis,
   subjective sentiment read, etc.). These go into the batched question in Step 5.
4. If a field is genuinely non-essential to reaching a Rule Status for every candidate rule,
   mark it UNKNOWN instead of blocking on it — don't manufacture precision the user never gave
   (thresholds for "high/low position", "急跌/缓跌" etc. stay qualitative unless the user
   states a number).

### Step 5 — Ask once, batched

If any fields remain unresolved after Step 4 and are *necessary* to reach a Rule Status for at
least one candidate rule, ask for all of them in a single turn, grouped by topic (position/
account info together, subjective read together), not repeated per rule. Use
`ask_user_input_v0` when the missing fields reduce to a small set of discrete choices (e.g.
"是否持仓？" yes/no, "止损结果" yes/no); use plain prose questions when a number or free-text
answer is needed (e.g. entry cost, total capital). Never send more than one round of
questions for the same batch — if the user's answer still leaves something out, note it as a
remaining "Missing Input" in the final output rather than asking again.

Do not proceed to Step 6 until this round is answered (end your turn after asking).

### Step 6 — Evaluate every candidate rule in parallel

With the shared input pool now as complete as it's going to get, evaluate each candidate
rule's IF/AND/THEN logic independently, producing for each: Rule Status (TRIGGERED /
NOT_TRIGGERED / INCONCLUSIVE / INSUFFICIENT_DATA), Interpretation, Suggested Action, Evidence,
Missing Inputs. Use the per-rule Evaluation logic recorded in `references/rule_library.md` —
do not re-derive it from scratch or drift from the wording already established there.

### Step 7 — Conflict check and synthesis

Read `references/rule_library.md` → "Conflict Matrix". Check whether any pair of TRIGGERED
rules from Step 6 appears in that matrix. If so, surface it explicitly rather than silently
listing both suggested actions side by side — a user reading "试仓" and "暂停交易" back to
back with no framing will not know which one wins.

**Priority default when a conflict involves an account-discipline rule (the 法则八 series —
仓位纪律/连续止损熔断/止损铁律) versus a signal rule (price/volume/pattern-based rules):
present the discipline rule's action as the one to follow first**, and frame the signal rule's
conclusion as informational context rather than an instruction to act on immediately. This
mirrors the source material's own framing — discipline rules exist specifically to override
in-the-moment signal reads.

For conflicts not involving a discipline rule, do not pick a winner yourself — present both
readings side by side with the specific condition that would resolve which one actually
applies (e.g. "if this is 下跌初期 → 法则五-A wins; if this is 恐慌尾声的急跌 → 法则六-B
wins — which does this look like to you?").

Present the final answer as:
1. A one-line plain-language bottom line.
2. Which rule(s) triggered and their suggested actions.
3. Any conflict/priority note.
4. Evidence and Missing Inputs per rule, kept brief — don't repeat the full Rule Contract text
   back at the user unless they ask for it.

## Handling requests to add a new rule

If the user describes a new experience and wants it turned into a rule (rather than routed
against existing ones), that is the separate Rule Extraction task described at the top of
`references/rule_library.md`'s "Source Instructions" section — follow that contract, then
append the resulting rule to the Rule Index and Canonical Input Schema in
`references/rule_library.md` so future routing can find it. Confirm the addition with the user
before treating it as part of the routable library.

## What this skill is not for

- 法则十三 (显而易见法则) and any other non-operationalizable "meta-principle" rules should
  never be auto-matched into the candidate list in Step 2 — they have no situation tags. Only
  surface them if the user explicitly asks for a reflective/meta-level check on an opportunity.
- This skill does not replace the user's own risk judgment — every output should retain the
  Limitations of whichever rules triggered, not present conclusions as certainties.
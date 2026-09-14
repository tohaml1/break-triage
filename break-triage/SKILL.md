---
name: break-triage
description: Triage reconciliation breaks between two records of the same payment flow — on-chain vs ledger, PSP report vs accounting, bank statement vs internal books. Turns a raw list of unmatched or mismatched items into a prioritised investigation queue with root-cause hypotheses, exposure figures, and a ready-to-send escalation memo. Use this skill whenever the user mentions reconciliation breaks, unmatched transactions, exceptions, discrepancies between two systems, settlement differences, a breaks file or exceptions report, or asks what to do with items a reconciliation just flagged — even if they do not use the word "triage".
---

# Break Triage

A reconciliation tool tells you *that* two records disagree. This skill covers what comes next: deciding which disagreements matter, why they happened, and who needs to hear about them.

## When to use this

The user has a list of breaks (CSV, spreadsheet, pasted table, or output from a reconciliation script) and needs to turn it into something actionable. Typical phrasings: "we have 40 unmatched items", "here's the exceptions report", "the PSP report doesn't tie to our books", "what do I do with these breaks".

If the user has not yet run a reconciliation and only has two raw data sets, say so and reconcile first — this skill starts from the breaks, not from the source data.

## Workflow

### 1. Understand what the two sources are

Before classifying anything, establish:

- **Source A and source B** — which system produced each record, and which one is authoritative for what. On-chain data is authoritative for settlement; the ledger is authoritative for intent and booking.
- **Cut-off** — the period covered, and whether both sources use the same timezone and the same cut-off moment. A large share of apparent breaks are timing, not errors.
- **Completeness** — whether the export covers all transaction categories. For on-chain data, normal transactions, internal transactions and token transfers are separate exports; a missing export creates dozens of false breaks.

Ask the user if any of these is unclear. Do not guess at the cut-off.

### 2. Classify each break

Assign every item a root-cause category. Read `references/break-taxonomy.md` for the full list with detection rules and typical causes.

Never classify on the amount alone. A difference that exactly equals the fee is a fee booking issue; the same difference with no matching fee is something else entirely.

### 3. Quantify exposure

Run `scripts/triage.py` on the breaks file to produce counts, gross and net exposure per category, and an ageing profile. Net exposure matters more than gross: forty breaks that offset each other are a process problem, while one unoffset break is a money problem.

Present both. A category with many items but near-zero net is a control weakness to fix; a category with one item and large net is an incident to escalate today.

### 4. Prioritise

Rank by this order, not by size:

1. **Possible loss of funds** — value left the business and no counterpart record exists anywhere.
2. **Control failure** — the break reveals a process that will keep producing breaks (failed transactions booked as settled, fees never posted).
3. **Compliance-relevant** — the break touches transaction monitoring: transfers to or from an address not in the expected counterparty set, activity outside the expected pattern, or anything the user's AML process would want to see. Flag it for the compliance owner; do not make the AML determination inside this skill.
4. **Booking noise** — timing, rounding, formatting. Fix in bulk, do not escalate individually.

### 5. Write the output

Produce two artefacts:

- **Investigation queue** — one row per break: identifier, category, exposure, hypothesis, what evidence would confirm it, owner, priority.
- **Escalation memo** — short, for the finance or payment operations lead. Use `references/escalation-memo-template.md`.

Write hypotheses as hypotheses. "Difference equals the gas fee, so the fee was likely posted to a separate account — confirm against the fee account" is useful. "The fee was posted incorrectly" is a claim the evidence does not yet support.

## Rules

- **Never silently drop a break.** Items below tolerance are reported as within tolerance, not omitted. The tolerance itself is stated in the output.
- **State the tolerance used** for amounts and for timing. A reader cannot judge the result without it.
- **Do not net across categories.** Netting a missing deposit against an unbooked fee hides both.
- **Do not fabricate identifiers.** If a transaction hash or reference is missing from the source, the field stays empty and the break is marked as lacking identification.
- **Escalate compliance-relevant items rather than resolving them.** Anything that looks like sanctions exposure, structuring, or an unexpected counterparty goes to the compliance owner with the evidence attached.

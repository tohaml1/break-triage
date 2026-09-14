# break-triage

A Claude Skill for the step that comes after a reconciliation: deciding which breaks matter, why they happened, and who needs to know.

Reconciliation tools output a list of items that did not match. Turning that list into a prioritised queue and an escalation memo is analyst work — this skill encodes how that work is done so it can be run consistently.

Companion to [onchain-reconciliation](https://github.com/tohaml1/onchain-reconciliation), which produces the breaks file this skill consumes. It also works on any exceptions report: PSP settlement vs accounting, bank statement vs internal books.

## What it does

Given a breaks file, the skill:

1. Establishes what the two sources are, which is authoritative for what, and what cut-off and timezone each uses.
2. Classifies every break into a root cause — fee not booked, decimals error, dropped transaction, timing, status mishandled, duplicate export window.
3. Quantifies gross and net exposure per category, with an ageing profile.
4. Prioritises by possible loss of funds, then control failure, then compliance relevance, then booking noise.
5. Produces an investigation queue and a one-page escalation memo.

## Structure

```
break-triage/
├── SKILL.md                              workflow and rules
├── references/
│   ├── break-taxonomy.md                 detection rules and root causes per break type
│   └── escalation-memo-template.md       the memo format, with notes on writing it
└── scripts/
    └── triage.py                         counts, gross/net exposure per category, ageing
```

## Design notes

Three rules shaped the skill:

**Never net across categories.** A missing deposit offset against an unbooked fee produces a clean-looking total and hides both problems. Exposure is reported per category.

**Never silently drop an item.** Breaks below tolerance are reported as within tolerance, with the tolerance stated. A one-directional rounding remainder is a real issue even when each item is trivial.

**Separate what is known from what is suspected.** "The difference equals the gas fee" is an observation. "The fee was posted to the wrong account" is a hypothesis until the fee account confirms it. The skill writes hypotheses as hypotheses.

## Using the script standalone

```bash
python break-triage/scripts/triage.py breaks.csv
```

Column names are auto-detected, or set explicitly with `--category`, `--amount`, `--date`.

## Installing as a skill

Point Claude at the `break-triage/` folder, or package it and add it through the skills interface. The skill triggers on mentions of reconciliation breaks, unmatched transactions, exceptions reports, or settlement differences.

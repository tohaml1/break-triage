# Escalation memo template

Keep it to one screen. The reader wants to know what is broken, what it costs, and what is needed from them.

---

**Subject:** Reconciliation breaks — [source A] vs [source B], [period]

**Scope.** [N] transactions in [source A] against [M] records in [source B], covering [period, timezone]. Tolerances applied: [amount tolerance], [timing tolerance].

**Result.** [X] items matched cleanly ([Y]%). [Z] breaks identified across [n] categories.

**Requires a decision**

1. **[Category]** — [count] items, net exposure [amount]. [One sentence: what happened and the leading hypothesis.] Needs: [specific action and owner].
2. [Second item, same shape.]

**Being handled**

- **[Category]** — [count] items, net [amount]. [Cause in one clause.] [Action being taken, by whom, by when.]

**Within tolerance**

[count] items below [tolerance], net [amount]. Listed in the attached file, no action proposed.

**Flagged to compliance**

[count] items referred to [owner] with supporting evidence. No determination made here.

**Attached.** Investigation queue with all [Z] breaks, one row each.

---

## Notes on writing it

- Lead with the decision the reader has to make, not with the methodology.
- Separate what you know from what you suspect. "Difference equals the fee" is known; "the fee was posted to the wrong account" is the hypothesis until the fee account confirms it.
- Give net exposure per category, never one total across all categories.
- Name an owner for every open item. An item with no owner does not get closed.
- If a category is recurring rather than a one-off, say so — that turns a cleanup task into a process fix.

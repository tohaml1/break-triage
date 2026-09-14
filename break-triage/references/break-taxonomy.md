# Break taxonomy

Detection rules and root causes for reconciliation breaks between a settlement record (source A) and a booking record (source B).

## Contents

- Missing on one side
- Amount differences
- Timing differences
- Status differences
- Identification and duplication
- Category-specific notes for crypto flows

---

## Missing on one side

**Present in settlement, absent from booking.** The value moved but nobody recorded it.

Typical causes: an internal transaction or contract-initiated transfer that the standard export does not contain; a payment method or provider not wired into the booking process; a manual payment made outside the normal flow.

Evidence to request: the full set of exports for the period, including internal transactions and token transfers; the provider's own report for the same window.

**Present in booking, absent from settlement.** The business believes value moved and it did not.

Typical causes: transaction dropped, stuck in the mempool, or replaced by a later one with a higher fee; a payment instruction created and never executed; a booking made in advance of settlement.

Priority note: this category is the one that can mean real loss. Check whether the funds are still in the originating account before treating it as a booking error.

---

## Amount differences

**Difference equals the fee.** Detect by comparing the absolute difference against the recorded fee within tolerance. Cause: the fee is posted to a separate account, posted in a different period, or not posted at all.

**Difference is a power of ten.** Almost always a decimals error — a token with 6 decimals handled as 18, or a value read as whole units instead of the smallest unit.

**Difference is a rounding remainder.** Below tolerance. Report as within tolerance rather than dropping it; a systematic one-directional remainder is a real issue even when each item is trivial.

**Difference is arbitrary.** Partial fill, wrong asset matched to the record, or the wrong exchange rate applied at booking. Ask which rate and which source the booking used.

---

## Timing differences

Same identifier on both sides, timestamps apart by more than tolerance.

Causes: settlement occurred close to the period cut-off and was booked in the next period; the two sources use different timezones; the booking was made manually days later.

Test before treating as an error: check whether the gap is roughly constant across many items. A constant offset is a timezone configuration problem and is fixed once, not item by item.

---

## Status differences

**Failed or reverted on the settlement side, settled on the booking side.** The ingestion process is not checking the status field. This is a control failure: it will recur on every failed transaction until the process changes, and it overstates both volume and value.

**Pending on one side, final on the other.** Usually timing. Confirm at the next cut-off before investigating further.

---

## Identification and duplication

**Same identifier appearing more than once in one source.** Usually overlapping export windows. Deduplicate before classifying anything else, or every downstream count is wrong.

**No identifier at all.** Match on the combination of amount, date and counterparty, and mark the match as unconfirmed. Never assign an identifier that the source did not provide.

---

## Category-specific notes for crypto flows

- Internal transactions are invisible in the normal transaction export on most explorers. Missing them is the single most common source of false breaks.
- The fee is paid by the sender in the native asset, not in the asset transferred. A token transfer reconciliation still needs the native-asset fee accounted for somewhere.
- A failed transaction still consumes a fee. The transfer did not happen; the cost did.
- The same nonce can appear twice when a transaction is replaced. Only one of them settled.
- An address is not a counterparty. Several addresses can belong to one counterparty, and one deposit address can be shared across customers by a provider — confirm the mapping with the provider rather than inferring it from the chain.

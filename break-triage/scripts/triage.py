"""
Quantify a breaks file: counts, gross and net exposure per category, ageing.

Input: a CSV of breaks with at least a category column. Amount and date columns
are used when present. Column names are auto-detected from the candidates below;
override with --category / --amount / --date.

Usage:
  python triage.py breaks.csv
  python triage.py breaks.csv --category break_type --amount diff --date time_onchain
"""

import argparse
import sys
from decimal import Decimal, InvalidOperation

import pandas as pd

CATEGORY_CANDIDATES = ["break_type", "category", "reason", "break", "type"]
AMOUNT_CANDIDATES = ["diff", "difference", "amount", "exposure", "value", "amount_onchain"]
DATE_CANDIDATES = ["date", "time", "time_onchain", "time_ledger", "datetime", "DateTime (UTC)"]


def pick(df, explicit, candidates, required=False, label=""):
    if explicit:
        if explicit not in df.columns:
            sys.exit(f"column '{explicit}' not in file. Columns: {list(df.columns)}")
        return explicit
    for c in candidates:
        if c in df.columns:
            return c
    if required:
        sys.exit(f"could not find a {label} column. Columns: {list(df.columns)}")
    return None


def to_dec(x):
    text = str(x).replace(",", "").strip()
    if text in ("", "nan", "NaN", "None", "NaT"):
        return None
    try:
        value = Decimal(text)
    except (InvalidOperation, AttributeError):
        return None
    return None if value.is_nan() else value


def exposure(row, columns):
    """First usable amount for a row: an explicit difference beats a raw amount."""
    for col in columns:
        value = to_dec(row.get(col))
        if value is not None:
            return value
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("breaks_csv")
    ap.add_argument("--category")
    ap.add_argument("--amount")
    ap.add_argument("--date")
    args = ap.parse_args()

    df = pd.read_csv(args.breaks_csv)
    cat_col = pick(df, args.category, CATEGORY_CANDIDATES, required=True, label="category")
    amt_col = pick(df, args.amount, AMOUNT_CANDIDATES)
    amt_cols = [args.amount] if args.amount else [c for c in AMOUNT_CANDIDATES if c in df.columns]
    date_col = pick(df, args.date, DATE_CANDIDATES)

    print(f"Breaks file        : {args.breaks_csv}")
    print(f"Total breaks       : {len(df)}")
    print(f"Category column    : {cat_col}")
    print(f"Amount column      : {amt_col or 'none found - counts only'}")
    print()

    header = f"{'CATEGORY':<34}{'COUNT':>7}"
    if amt_col:
        header += f"{'GROSS':>16}{'NET':>16}"
    print(header)
    print("-" * len(header))

    for cat, group in df.groupby(cat_col, sort=False):
        line = f"{str(cat):<34}{len(group):>7}"
        if amt_col:
            values = [exposure(r, amt_cols) for _, r in group.iterrows()]
            values = [v for v in values if v is not None]
            gross = sum(abs(v) for v in values)
            net = sum(values)
            unpriced = len(group) - len(values)
            line += f"{gross:>16}{net:>16}"
            if unpriced:
                line += f"   ({unpriced} without an amount)"
        print(line)

    if amt_col:
        values = [exposure(r, amt_cols) for _, r in df.iterrows()]
        values = [v for v in values if v is not None]
        print("-" * len(header))
        print(f"{'TOTAL':<34}{len(df):>7}{sum(abs(v) for v in values):>16}{sum(values):>16}")
        print()
        print("Net is per category above; the total net is shown only for completeness.")
        print("Do not present one net figure across categories - it hides offsetting breaks.")

    if date_col:
        dates = pd.to_datetime(df[date_col], utc=True, errors="coerce").dropna()
        if not dates.empty:
            print()
            print(f"Oldest break       : {dates.min().date()}")
            print(f"Newest break       : {dates.max().date()}")
            print(f"Span               : {(dates.max() - dates.min()).days} days")


if __name__ == "__main__":
    main()

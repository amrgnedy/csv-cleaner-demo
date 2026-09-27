#!/usr/bin/env python3
"""Preview and clean a CSV without changing the original file."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

def clean_header(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_") or "column"

def read_and_clean(source: Path):
    with source.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames:
            raise ValueError("CSV needs a header row")
        headers = [clean_header(header) for header in reader.fieldnames]
        if len(set(headers)) != len(headers):
            raise ValueError("Headers become duplicates after normalization")
        rows, seen = [], set()
        empty_rows = duplicate_rows = 0
        for original in reader:
            row = {header: (original.get(old_header) or "").strip() for header, old_header in zip(headers, reader.fieldnames)}
            key = tuple(row[header] for header in headers)
            if not any(key):
                empty_rows += 1
            elif key in seen:
                duplicate_rows += 1
            else:
                seen.add(key)
                rows.append(row)
    return headers, rows, empty_rows, duplicate_rows

def main() -> int:
    parser = argparse.ArgumentParser(description="Clean a CSV while preserving the original.")
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--apply", action="store_true", help="Write the cleaned CSV")
    args = parser.parse_args()
    if not args.source.is_file():
        parser.error("source must be an existing file")
    if args.source.resolve() == args.destination.resolve():
        parser.error("destination must be different from source")
    headers, rows, empty_rows, duplicate_rows = read_and_clean(args.source)
    print(f"Would write {len(rows)} rows with headers: {', '.join(headers)}")
    print(f"Skipped {empty_rows} empty rows and {duplicate_rows} duplicate rows.")
    if not args.apply:
        print("Preview only. Add --apply to write the cleaned CSV.")
        return 0
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    with args.destination.open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {args.destination}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

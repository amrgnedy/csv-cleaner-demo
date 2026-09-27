# CSV Cleaner — demonstration project

A small Python script that previews a cleaned CSV before writing it. Built with AI assistance. This is a demonstration, not past client work.

It normalizes header names, trims whitespace, removes fully empty rows, and keeps the first copy of an otherwise identical row. The original file is never changed.

## Run

Requires Python 3 and no extra packages.

```bash
python3 clean_csv.py input.csv cleaned.csv
python3 clean_csv.py input.csv cleaned.csv --apply
```

The first command only previews the result. The `--apply` command creates a new file and refuses to overwrite an existing destination.

## Limits

This is intended for ordinary comma-separated files with a header row. It does not guess column meanings or change values beyond trimming surrounding whitespace. A custom project should define its exact cleanup rules with the client before work begins.

## Validation

Run `python3 test_clean_csv.py`. The test checks preview mode, normalized headers, whitespace trimming, duplicate removal, empty-row removal, source preservation, and safe destination creation.

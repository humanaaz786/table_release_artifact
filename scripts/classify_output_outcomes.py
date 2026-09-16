#!/usr/bin/env python3
"""Assign mutually exclusive OCR output outcomes before output cleanup.

Usage: python classify_output_outcomes.py INPUT.csv OUTPUT.csv
The input must contain id, gt_text, prediction, and status columns.
"""
from __future__ import annotations

import csv
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

REFUSAL_RE = re.compile(r"(?:cannot|can't|unable to|i am sorry|i'm sorry|لا أستطيع|عذرا|آسف)", re.I)
MARKUP_RE = re.compile(r"(?:<[^>]+>|```|^\s*(?:transcription|text|answer)\s*[:：])", re.I)
ARABIC_RE = re.compile(r"[\u0600-\u06ff]")
STATUS_FAILURE = {"error", "missing_image", "provider_error", "api_error", "quota_error"}


def normalized_chars(text: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFKC", text) if ch.isalnum())


def repeated(text: str) -> bool:
    text = normalized_chars(text)
    for n in range(4, min(12, len(text)) + 1):
        counts = Counter(text[i:i + n] for i in range(len(text) - n + 1))
        if any(count >= 3 for count in counts.values()):
            return True
    return False


def category(row: dict[str, str]) -> str:
    status = (row.get("status") or "").strip().lower()
    prediction = (row.get("prediction") or "").strip()
    reference = (row.get("gt_text") or "").strip()
    if status in STATUS_FAILURE:
        return "provider_api_failure"
    if REFUSAL_RE.search(prediction):
        return "refusal"
    if not prediction:
        return "empty_output"
    if MARKUP_RE.search(prediction):
        return "formatting_violation"
    if repeated(prediction):
        return "repetitive_generation"
    letters = normalized_chars(prediction)
    arabic = len(ARABIC_RE.findall(letters))
    shared = set(ARABIC_RE.findall(letters)) & set(ARABIC_RE.findall(normalized_chars(reference)))
    if letters and (arabic / len(letters) < 0.5 or not shared):
        return "non_arabic_unrelated_generation"
    if len(prediction) > 2 * max(1, len(reference)):
        return "overlong_generation"
    return "valid_transcription"


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    source, destination = map(Path, sys.argv[1:])
    with source.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0]) if rows else []
    required = {"id", "gt_text", "prediction", "status"}
    if not required.issubset(fields):
        raise SystemExit(f"Missing required fields: {required - set(fields)}")
    for row in rows:
        row["outcome_category"] = category(row)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields + ["outcome_category"])
        writer.writeheader()
        writer.writerows(rows)
    counts = Counter(row["outcome_category"] for row in rows)
    print(f"classified {len(rows)} rows: {dict(sorted(counts.items()))}")


if __name__ == "__main__":
    main()

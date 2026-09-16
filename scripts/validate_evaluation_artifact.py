#!/usr/bin/env python3
"""Validate the canonical OCR evaluation artifact before table generation."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ROW_SOURCE = ROOT / "final_row_level_metric_source.csv"
ID_MANIFEST = ROOT / "handwritten_919_retained_ids.csv"
TABLE_AUDIT = ROOT / "table_generation_audit.csv"
REQUIRED_ROW_FIELDS = {
    "id", "font", "char_edits", "char_ref_len", "word_edits",
    "word_ref_len", "exact", "model", "split",
}
EXPECTED_HANDWRITTEN_MODELS = {
    "AIN 7B", "EasyOCR", "GPT-5.4 mini", "Gemini Flash", "Gemini Pro",
    "Gemma-3-27B", "Qari-OCR v0.3", "Qwen2.5-VL-72B", "Qwen3-VL-32B",
    "Qwen3-VL-8B",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    rows = read_csv(ROW_SOURCE)
    if not rows or not REQUIRED_ROW_FIELDS.issubset(rows[0]):
        raise SystemExit(f"Invalid canonical schema: {ROW_SOURCE}")

    manifest_rows = read_csv(ID_MANIFEST)
    if not manifest_rows or set(manifest_rows[0]) != {"id"}:
        raise SystemExit(f"Invalid ID manifest schema: {ID_MANIFEST}")
    frozen_ids = {row["id"] for row in manifest_rows}
    if len(frozen_ids) != 919 or len(manifest_rows) != 919:
        raise SystemExit(f"Expected 919 unique frozen handwritten IDs, found {len(frozen_ids)}")

    by_model: dict[str, set[str]] = {}
    for row in rows:
        if row["split"] != "handwritten":
            continue
        by_model.setdefault(row["model"], set()).add(row["id"])

    if set(by_model) != EXPECTED_HANDWRITTEN_MODELS:
        missing = EXPECTED_HANDWRITTEN_MODELS - set(by_model)
        unexpected = set(by_model) - EXPECTED_HANDWRITTEN_MODELS
        raise SystemExit(f"Unexpected handwritten model set; missing={missing}, extra={unexpected}")
    for model, ids in sorted(by_model.items()):
        if ids != frozen_ids:
            raise SystemExit(
                f"Handwritten ID mismatch for {model}: "
                f"missing={len(frozen_ids - ids)}, extra={len(ids - frozen_ids)}"
            )

    audit_rows = read_csv(TABLE_AUDIT)
    for row in audit_rows:
        if row.get("status") != "pass" or row.get("fields_per_data_row") != "11":
            raise SystemExit(f"Table-generation audit failed: {row}")

    print(
        "PASS: canonical source has %d rows; all %d complete handwritten "
        "models share the frozen 919-ID manifest; table rows have 11 fields."
        % (len(rows), len(by_model))
    )


if __name__ == "__main__":
    main()

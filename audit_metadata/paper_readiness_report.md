# Paper-Oriented Analysis Additions

## Added Artifacts

- `dataset_coverage.csv`
- `normalized_arabic_metrics.csv`
- `printed_by_font_metrics.csv`
- `printed_font_robustness.csv`
- `qualitative_error_cases.csv`

Plots are in `plots/`: micro CER, exact match, character F-score, per-font robustness, and cost-latency tradeoff.

## Method Notes

- Raw metrics preserve punctuation, hamza/alef variants, taa marbuta, yaa/alef maqsura, and diacritics.
- Normalized Arabic metrics remove diacritics/tatweel, normalize alef forms, normalize yaa/alef maqsura, hamza seats, taa marbuta, punctuation, and whitespace.
- Hallucination is rule-based: empty output, extreme over-generation, repeated spans/tokens, HTML/code-like artifacts.
- AIN handwritten combines original full run, A4500 retry, and A100 retry to obtain 919/919 coverage.
- Gemini Pro printed is reported as a full backfilled result: budget-error rows from the fresh run are filled from the older Gemini Pro output and should be described transparently.
- Gemini Flash evaluation uses existing eval tables with different sample counts, so state the split difference clearly.

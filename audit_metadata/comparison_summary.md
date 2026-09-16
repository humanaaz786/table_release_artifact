# OCR/VLM Comparison Summary

Generated from the corrected final metrics tables. Gemini Pro printed uses the full 11,392-row backfilled file, where failed fresh-run rows were filled from the older Gemini Pro output.

## Closed

| Model | Split | Rows | Status | CER | WER | Micro CER | Micro WER | Exact Match | Char F-score | Hallucination | Cost | Latency | Note |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| GPT-5.4 mini | handwritten | 919 | ok:919 | 0.3366 | 0.7541 | 0.3343 | 0.7452 | 0.0065 | 0.7285 | 0.0000 | 0.8301 | 1.2450 | full |
| GPT-5.4 mini | printed | 11392 | ok:11392 | 0.1000 | 0.3135 | 0.0977 | 0.3027 | 0.1111 | 0.9243 | 0.0001 | 4.0068 | 1.2574 | partial/running if rows<11392 |
| Gemini Flash | handwritten | 919 | ok:915; unknown:3; error:1 | 0.3118 | 0.4643 | 0.3300 | 0.4574 | 0.0555 | 0.6700 | 0.0022 | 4.6753 | 1.9503 | standardized 919-row handwritten subset from raw Flash file |
| Gemini Flash | printed | 7819 | ok:7819 | 0.0312 | 0.1542 | 0.0292 | 0.1422 | 0.3581 | 0.9708 | 0.0000 | 39.3580 | 3.9261 | existing filtered printed Flash evaluation with hallucination/Char F1 added |
| Gemini Pro | handwritten | 919 | ok:910; empty_prediction:9 | 0.6005 | 0.7409 | 0.6407 | 0.7609 | 0.0196 | 0.5143 | 0.0098 | 4.9920 | 5.2204 | full clean-ish |
| Gemini Pro | printed | 11392 | ok:11271; empty_prediction:121 | 0.6612 | 0.7090 | 0.7027 | 0.7393 | 0.0360 | 0.4640 | 0.0120 | 61.4108 | 4.6303 | full printed run; budget-error rows backfilled from older Gemini Pro output |

## Open/General

| Model | Split | Rows | Status | CER | WER | Micro CER | Micro WER | Exact Match | Char F-score | Hallucination | Cost | Latency | Note |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| EasyOCR | handwritten | 919 | ok:918; empty_prediction:1 | 0.4895 | 1.1229 | 0.4833 | 1.1007 | 0.0000 | 0.5825 | 0.0011 | 0.0000 | 0.0904 | full local |
| EasyOCR | printed | 11392 | ok:11372; empty_prediction:20 | 0.0924 | 0.3780 | 0.0865 | 0.3608 | 0.0629 | 0.9378 | 0.0018 | 0.0000 | 0.0471 | full local |
| Gemma-3-27B | handwritten | 919 | ok:919 | 0.8798 | 1.2541 | 0.9414 | 1.3008 | 0.0033 | 0.4117 | 0.0141 | 0.0336 | 1.2785 | full |
| Gemma-3-27B | printed | 11392 | ok:11150; empty_prediction:197; error:45 | 0.6129 | 0.8876 | 0.6755 | 0.9340 | 0.0335 | 0.5113 | 0.0322 | 0.3931 | 2.1081 | full strict prompt |
| Qwen 32B | handwritten | 919 | ok:919 | 0.5767 | 0.8208 | 0.5675 | 0.8127 | 0.0098 | 0.6420 | 0.0076 | 0.7817 | 1.7112 | full |
| Qwen 32B | printed | 11392 | ok:11392 | 0.0469 | 0.1754 | 0.0445 | 0.1687 | 0.3259 | 0.9682 | 0.0000 | 3.9488 | 1.3011 | full |
| Qwen 8B | handwritten | 919 | ok:919 | 0.4784 | 0.7567 | 0.4799 | 0.7555 | 0.0120 | 0.6837 | 0.0087 | 0.7700 | 1.4085 | full |
| Qwen 8B | printed | 11392 | ok:11392 | 0.0451 | 0.1667 | 0.0405 | 0.1564 | 0.3336 | 0.9705 | 0.0001 | 3.9424 | 1.0033 | full |

## Open/General

| Model | Split | Rows | Status | CER | WER | Micro CER | Micro WER | Exact Match | Char F-score | Hallucination | Cost | Latency | Note |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Qwen2.5-VL-72B | handwritten | 919 | ok:919 | 0.3800 | 0.6872 | 0.3666 | 0.6697 | 0.0141 | 0.6334 | 0.0033 | 0.4871 | 2.3981 | full 919-row handwritten run via OpenRouter |

## Arabic Specialized

| Model | Split | Rows | Status | CER | WER | Micro CER | Micro WER | Exact Match | Char F-score | Hallucination | Cost | Latency | Note |
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| AIN 7B | handwritten | 919 | ok:919 | 0.0664 | 0.2501 | 0.0690 | 0.2544 | 0.2100 | 0.9452 | 0.0000 | 0.0000 | 1.1972 | merged original+A4500 retry+A100 retry |
| AIN 7B | printed | 11392 | ok:11392 | 0.0076 | 0.0445 | 0.0073 | 0.0447 | 0.7329 | 0.9947 | 0.0000 | 0.0000 | 0.9829 | full after five-row retry |
| Qari-OCR v0.3 | handwritten | 919 | ok:913; error:6 | 0.6802 | 1.1444 | 0.6660 | 1.0709 | 0.0033 | 0.5878 | 0.0816 | 0.0000 | 2.0686 | full, html stripped |
| Qari-OCR v0.3 | printed | 11392 | ok:11379; error:5; empty_prediction:8 | 0.0924 | 0.1979 | 0.0889 | 0.1850 | 0.3808 | 0.9472 | 0.0157 | 0.0000 | 0.7456 | full, html stripped |

## Preprocessing / Postprocessing

| Model/group | Processing used |
|---|---|
| GPT/OpenAI via OpenRouter | Unsupported TIFF/extensionless images converted to PNG before API call; strict OCR prompt; whitespace normalization. |
| Gemini/Qwen/Gemma via OpenRouter | Base64 image API input; strict OCR prompt where configured; whitespace normalization. |
| Qari-OCR | HTML/Markdown tags stripped with deterministic postprocessing; whitespace normalized. |
| AIN | Printed and handwritten local inference; A100/A6000 retries used for failed rows; whitespace normalized. |
| EasyOCR | Local RGB/TIFF fallback image loader; zero API cost. |

## Coverage Notes

- Gemini Pro printed is included as a full backfilled result: 7,520 rows from the fresh rerun plus older Gemini Pro rows for the budget-error rows, resulting in 11,271 ok rows and 121 empty predictions.
- Gemini Flash printed uses the existing 7,819-row filtered evaluation, so it should be reported with its coverage difference.
- Qwen2.5-VL-72B printed remains a 200-image balanced pilot unless the full printed run is completed.

# Assignment 3

This folder holds the work for **Assignment 3: Transformer is All You Need**, implementing and training a small decoder-only Transformer in PyTorch for next-token prediction on Tiny Shakespeare, then visualizing its attention.

## Layout

```
assignment3/
├── Assignment3.pdf              # Official assignment handout
├── AGENTS.md                    # Workflow / AI guardrails used while building the work
├── README.md                    # This file
├── artifacts/                   # Saved tokenizer and selected checkpoint (from the Colab run)
├── assets/                      # Report figures exported from the Colab run
├── data/
│   ├── input.txt                # Tiny Shakespeare corpus used by the notebook
│   └── raw-url.txt              # Source URL of input.txt
├── notebook/
│   └── assign3-ms7556.ipynb     # Runnable notebook (executed in Colab, outputs saved)
└── report/                      # Written report (no code)
```

## Status

| Step | Content | State |
|---|---|---|
| Setup | Environment, data loading, source/date/SHA-256 record | Scaffolded |
| 1 | Positional 80/20 split, BPE tokenizer, token windows | Not started |
| 2 | Tiny Transformer, causality checks, baseline + controlled change | Not started |
| 3 | Loss curves, validation loss and perplexity, attention heatmaps | Not started |
| 4 | Comparison table and discussion | Not started |
| Report | `report/Assignment3_Report.pdf` with Colab link at the end | Not started |

## What each part contains

### `Assignment3.pdf`

The course specification for Assignment 3. It defines the four steps (data preparation → implement and train a tiny Transformer → visualization and interpretation → discussion), the implementation restrictions on attention, the evaluation rules, the report format, the rubric, and the Colab access requirement.

### `AGENTS.md`

Local instructions that govern how the notebook and report are produced with AI assistance: assignment-first compliance, split-before-tokenizer data preparation, a from-scratch causal attention implementation, one controlled change under a fixed budget, correct loss and perplexity, and the report expectations.

### `artifacts/`

The BPE tokenizer and the selected model checkpoint saved by the notebook, so the reported results can be reproduced.

### `assets/`

Figures saved by the notebook (loss curves and attention heatmaps). The report embeds the required ones.

### `data/`

| File | Role |
|------|------|
| `input.txt` | Tiny Shakespeare (1,115,394 characters, 40,000 lines) from Karpathy's char-rnn repository, downloaded 2026-11-21. The notebook reads it from the Colab working directory, or downloads it from the source URL if it was not uploaded, and checks its SHA-256. |
| `raw-url.txt` | The source URL of `input.txt`. |

### `notebook/assign3-ms7556.ipynb`

The submission notebook, built one step at a time. It will cover:

1. Data loading with source, download date, and checksum
2. Positional 80/20 train/validation split, a BPE tokenizer (vocabulary ≤ 500) fitted on training text only, and token windows
3. A decoder-only Transformer built from basic layers (sinusoidal positions, causal multi-head attention, RMSNorm, feed-forward), with causality checks
4. A baseline and one controlled change trained under the same step budget, with checkpoint selection by validation cross-entropy
5. Training and validation loss curves, validation perplexity, attention heatmaps, and a comparison table

### `report/`

Will hold `Assignment3_Report.pdf`, the 5–7 page written report (analysis only; no code) with a page map, embedded figures and tables, AI Tool Usage Disclosure, references, and the Colab link at the end.

## Related paths outside this folder

Repository-level CI lives under `.github/workflows/` at the repo root and validates notebooks/Python across all assignments.

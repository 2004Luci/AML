# Assignment 3

This folder holds the work for **Assignment 3: Transformer is All You Need**, implementing and training a small decoder-only Transformer in PyTorch for next-token prediction on Tiny Shakespeare, then visualizing its attention.

## Layout

```
assignment3/
├── Assignment3.pdf                 # Official assignment handout
├── AGENTS.md                       # Workflow / AI guardrails used while building the work
├── README.md                       # This file
├── artifacts/                      # Saved tokenizer and selected checkpoint (from the Colab run)
├── assets/                         # Report figures exported from the Colab run
├── data/
│   ├── input.txt                   # Tiny Shakespeare corpus used by the notebook
│   └── raw-url.txt                 # Source URL of input.txt
├── notebook/
│   ├── submission/                 # Clean step notebooks (source of truth for correctness)
│   │   └── assign3_step0.ipynb
│   ├── learning/                   # Same code + learning notes, self-checks, report prompts
│   │   └── assign3_step0.ipynb
│   └── assign3-ms7556.ipynb        # Consolidated Colab deliverable (after Steps 1–4)
└── report/                         # Written report (no code)
```

## Dual-track notebooks

Until Steps 1–4 are finished, every step has **two** notebooks (same pattern as early Assignments 1 and 2):

| Track | Folder | Role |
|------|--------|------|
| Submission | `notebook/submission/` | Runnable and submission-ready; no TODOs or grader meta notes |
| Learning | `notebook/learning/` | Mirrors submission, plus teaching notes and self-check questions |

When all steps are done, consolidate the submission track into `notebook/assign3-ms7556.ipynb`, run it in Colab with outputs saved, and clean up the intermediate step notebooks.

## Status

| Step | Content | Submission | Learning |
|---|---|---|---|
| 0 Setup | Environment, data loading, source/date/SHA-256 | `assign3_step0.ipynb` | `assign3_step0.ipynb` |
| 1 | Positional 80/20 split, BPE tokenizer, token windows | Not started | Not started |
| 2 | Tiny Transformer, causality checks, baseline + controlled change | Not started | Not started |
| 3 | Loss curves, validation loss and perplexity, attention heatmaps | Not started | Not started |
| 4 | Comparison table and discussion | Not started | Not started |
| Consolidate | `assign3-ms7556.ipynb` executed in Colab | Pending | — |
| Report | `report/Assignment3_Report.pdf` with Colab link at the end | Not started | — |

## What each part contains

### `Assignment3.pdf`

The course specification for Assignment 3. It defines the four steps (data preparation → implement and train a tiny Transformer → visualization and interpretation → discussion), the implementation restrictions on attention, the evaluation rules, the report format, the rubric, and the Colab access requirement.

### `AGENTS.md`

Local instructions that govern how the notebooks and report are produced with AI assistance: dual-track workflow, assignment-first compliance, split-before-tokenizer data preparation, a from-scratch causal attention implementation, one controlled change under a fixed budget, correct loss and perplexity, and the report expectations.

### `artifacts/`

The BPE tokenizer and the selected model checkpoint saved by the notebook, so the reported results can be reproduced.

### `assets/`

Figures saved by the notebook (loss curves and attention heatmaps). The report embeds the required ones.

### `data/`

| File | Role |
|------|------|
| `input.txt` | Tiny Shakespeare (1,115,394 characters, 40,000 lines) from Karpathy's char-rnn repository, downloaded 2026-11-21. The notebook reads it from the Colab working directory, or downloads it from the source URL if it was not uploaded, and checks its SHA-256. |
| `raw-url.txt` | The source URL of `input.txt`. |

### `notebook/submission/` and `notebook/learning/`

Step notebooks built one PR at a time. Step 0 covers setup and data loading. Later steps add:

1. Positional 80/20 train/validation split, a BPE tokenizer (vocabulary ≤ 500) fitted on training text only, and token windows
2. A decoder-only Transformer built from basic layers (sinusoidal positions, causal multi-head attention, RMSNorm, feed-forward), with causality checks
3. A baseline and one controlled change trained under the same step budget, with checkpoint selection by validation cross-entropy
4. Training and validation loss curves, validation perplexity, attention heatmaps, and a comparison table

### `report/`

Will hold `Assignment3_Report.pdf`, the 5–7 page written report (analysis only; no code) with a page map, embedded figures and tables, AI Tool Usage Disclosure, references, and the Colab link at the end.

## Related paths outside this folder

Repository-level CI lives under `.github/workflows/` at the repo root and validates notebooks/Python across all assignments.

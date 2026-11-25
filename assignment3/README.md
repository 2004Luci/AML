# Assignment 3

This folder holds the completed work for **Assignment 3: Transformer is All You Need**, implementing and training a small decoder-only Transformer in PyTorch for next-token prediction on Tiny Shakespeare, then visualizing its attention.

## Layout

```
assignment3/
├── Assignment3.pdf              # Official assignment handout
├── AGENTS.md                    # Workflow / AI guardrails used while building the work
├── README.md                    # This file
├── artifacts/                   # Tokenizer and selected checkpoint from the Colab run
├── assets/                      # Report figures exported from the Colab run
├── data/
│   ├── input.txt                # Tiny Shakespeare corpus used by the notebook
│   └── raw-url.txt              # Source URL of input.txt
├── notebook/
│   └── assign3-ms7556.ipynb     # Final runnable notebook (executed in Colab, outputs saved)
└── report/
    └── Assignment3_Report.pdf   # Final written report (no code)
```

## What each part contains

### `Assignment3.pdf`

The course specification for Assignment 3. It defines the four steps (data preparation → implement and train a tiny Transformer → visualization and interpretation → discussion), the implementation restrictions on attention, the evaluation rules, the report format, the rubric, and the Colab access requirement.

### `AGENTS.md`

Local instructions that governed how the notebook and report were produced with AI assistance: assignment-first compliance, split-before-tokenizer data preparation, a from-scratch causal attention implementation, one controlled change under a fixed budget, correct loss and perplexity, and the final report expectations.

### `artifacts/`

| File | Role |
|------|------|
| `tokenizer.json` | Character-level BPE tokenizer (vocabulary 500) fitted on training text only |
| `selected_checkpoint.pt` | Lowest-validation-loss weights among the three learning-rate runs (CPU tensors) |
| `training_histories.json` | Per-step training and validation losses for every configuration |
| `comparison.json` | The comparison table (configurations, parameters, training time, best validation loss, PPL) |

### `assets/`

The five figures saved by the notebook (training/validation loss curves, validation-and-gap plot, layer-1 and layer-2 attention heatmaps, before/after attention). The report embeds them.

### `data/`

| File | Role |
|------|------|
| `input.txt` | Tiny Shakespeare (1,115,394 characters, 40,000 lines) from Karpathy's char-rnn repository, downloaded 2026-11-21. The notebook reads it from the Colab working directory, or downloads it from the source URL if it was not uploaded, and checks its SHA-256. |
| `raw-url.txt` | The source URL of `input.txt`. |

### `notebook/assign3-ms7556.ipynb`

The final consolidated notebook, executed top-to-bottom in Google Colab with all outputs saved. It covers:

1. Data loading with source URL, download date, and SHA-256 verification
2. Positional 80/20 split, character-level BPE (vocabulary 500) fitted on training text only, and token windows (`N` = 64)
3. A decoder-only Transformer built from basic layers (sinusoidal positions, causal multi-head attention, RMSNorm, feed-forward), with both causality checks
4. Three learning-rate configurations under a fixed 5,000-step budget; checkpoint selection by validation cross-entropy
5. Loss curves, validation perplexity, attention heatmaps and head statistics, a comparison table, a positional-encoding probe, runtime/memory measurements, an optional sample, and a discussion

All code, figures, and in-notebook explanations for the submission live here.

### `report/Assignment3_Report.pdf`

The 7-page written report for submission (analysis only; no code). It includes:

- Title page with author, Colab notebook line, page map for Steps 1–4, and summary
- Introduction, Methods, Results, Discussion
- AI Tool Usage Disclosure, References, and the Colab notebook link at the end

Required figures and tables from the notebook are embedded in the PDF.

## Related paths outside this folder

Repository-level CI lives under `.github/workflows/` at the repo root and validates notebooks/Python across all assignments.

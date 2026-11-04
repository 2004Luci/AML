# Assignment 2

This folder holds the completed work for **Assignment 2: From Trees to Neural Networks**, comparing gradient-boosted decision trees (XGBoost) with a multi-layer perceptron (scikit-learn) on the UCI Bank Marketing dataset.

## Layout

```
assignment2/
├── Assignment2.pdf              # Official assignment handout
├── AGENTS.md                    # Workflow / AI guardrails used while building the work
├── README.md                    # This file
├── assets/                      # Report figures exported from the Colab run
├── data/
│   └── bank-additional-full.csv # UCI Bank Marketing data used by the notebook
├── notebook/
│   └── assign2-ms7556.ipynb     # Final runnable notebook (executed in Colab, outputs saved)
└── report/
    └── Assignment2_Report.pdf   # Final written report (no code)
```

## What each part contains

### `Assignment2.pdf`

The course specification for Assignment 2. It defines the five steps (data preparation → GBDT → MLP → evaluation and comparison → report), the experiment and metric rules, the report format, the rubric, and the Colab access requirement.

### `AGENTS.md`

Local instructions that governed how the notebook and report were produced with AI assistance: assignment-first compliance, leakage-safe preprocessing, controlled experiments, test-set isolation, and the final report expectations.

### `assets/`

The eight figures saved by the notebook (GBDT learning-rate and selected-model log-loss curves, GBDT feature importance, MLP architecture comparison, learning-rate and selected-model loss curves, PR curves, confusion matrices). The report embeds the required ones.

### `data/`

| File | Role |
|------|------|
| `bank-additional-full.csv` | UCI Bank Marketing (41,188 calls, 20 predictors, target `y`; semicolon-separated). The notebook reads it from the Colab working directory, or downloads this file from the repository if it was not uploaded. |

### `notebook/assign2-ms7556.ipynb`

The final consolidated notebook, executed top-to-bottom in Google Colab with all outputs saved. It covers:

1. Data audit and cleaning (`duration` dropped as leakage, `pdays = 999` flag, `"unknown"` kept as a category)
2. Stratified 70/15/15 split and preprocessing fitted on training rows only (63 features for both models)
3. XGBoost experiments: learning rate, depth, and row subsampling with validation early stopping (8 configurations)
4. MLP experiments: architecture, learning rate, and L2 `alpha` with convergence tracking (8 configurations)
5. Validation-AP model selection, one-time test evaluation (AP, accuracy, precision, recall, F1 at 0.5), PR curves, confusion matrices, timing, and a summary of findings

All code, figures, and in-notebook explanations for the submission live here.

### `report/Assignment2_Report.pdf`

The 7-page written report for submission (analysis only; no code). It includes:

- Title page with author, Colab notebook line, page map for Steps 1–5, and summary
- Introduction, Methods, Results, Discussion
- AI Tool Usage Disclosure, References, and the Colab notebook link at the end

Required figures and tables from the notebook are embedded in the PDF.

## Related paths outside this folder

Repository-level CI lives under `.github/workflows/` at the repo root and validates notebooks/Python across all assignments.

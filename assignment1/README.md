# Assignment 1

This folder holds the completed work for **Assignment 1: From Dirty Data to Predictive Models**, using the Kaggle Titanic survival dataset.

## Layout

```
assignment1/
├── Assignment1.pdf              # Official assignment handout
├── AGENTS.md                    # Workflow / AI guardrails used while building the work
├── README.md                    # This file
├── data/                        # Titanic CSVs used by the notebook
│   ├── train.csv
│   ├── test.csv
│   └── gender_submission.csv
├── notebook/
│   └── assign1-ms7556.ipynb     # Final runnable notebook
└── report/
    └── Assignment1_Report.pdf   # Final written report (no code)
```

## What each part contains

### `Assignment1.pdf`

The course specification for Assignment 1. It defines the required end-to-end pipeline (cleaning → feature engineering → model training → evaluation → report) and the submission rules for the notebook and PDF.

### `AGENTS.md`

Local instructions that governed how the notebook and report were produced with AI assistance: assignment-first compliance, leakage-safe preprocessing, and the final report expectations.

### `data/`

Local copies of the Titanic files used by the notebook:

| File | Role |
|------|------|
| `train.csv` | Labeled passenger rows used for the stratified train/test split, cleaning, modeling, and evaluation |
| `test.csv` | Unlabeled Kaggle test set (present for completeness; modeling and metrics in this assignment use the labeled split from `train.csv`) |
| `gender_submission.csv` | Sample Kaggle submission format |

### `notebook/assign1-ms7556.ipynb`

The final consolidated Jupyter notebook for this assignment. It covers:

1. Data loading and quality audit  
2. Leakage-safe cleaning and imputation (fit on train, transform train and held-out test)  
3. Feature engineering and the two feature views used by Naive Bayes and the linear models  
4. Training of Bernoulli Naive Bayes (multiple smoothing strengths), Linear Regression, Ridge, and LASSO  
5. Evaluation (accuracy with uncertainty, precision/recall/F1, confusion matrices, ROC/AUC) and the smoothing / small-sample diagnostics  

All code, figures, and in-notebook explanations for the submission live here.

### `report/Assignment1_Report.pdf`

The written report for submission (analysis only; no code). It includes:

- Title page with author, Colab notebook line, page map, and summary  
- Introduction, Data Cleaning, Feature Engineering, Model Comparison, Discussion  
- AI Tool Usage Disclosure  

Figures from the notebook are embedded in the PDF.

## Related paths outside this folder

Repository-level CI lives under `.github/workflows/` at the repo root and validates notebooks/Python across all assignments.

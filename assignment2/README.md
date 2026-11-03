# Assignment 2 — From Trees to Neural Networks

This folder contains the work for **Assignment 2**, which compares gradient-boosted decision trees (GBDT) with a multi-layer perceptron (MLP) on one tabular dataset.

The assignment focuses on controlled experiments, predictive performance, learning behavior, runtime, and interpretability. A GPU is not required.

## Status

- [x] Assignment specification added (`Assignment2.pdf`)
- [x] Workflow guardrails added (`AGENTS.md` and `.cursor/rules/assignment2-workflow.mdc`)
- [x] Dataset selected: **Bank Marketing** (`data/bank-additional-full.csv`)
- [x] Dual notebook tracks scaffolded (`notebook/final/` + `notebook/learning/`)
- [x] Step 0 scaffold kept (`assign2-bank_step0.ipynb` in both tracks)
- [x] Step 1 data preparation, 70/15/15 split, and preprocessing implemented (`assign2-bank_step1.ipynb`); Colab run pending
- [x] Step 2 GBDT experiments implemented (`assign2-bank_step2.ipynb`, 8 configurations); verified in Colab
- [x] Step 3 MLP experiments implemented (`assign2-bank_step3.ipynb`, 8 configurations); verified in Colab
- [x] Step 4 final comparison implemented (`assign2-bank_step4.ipynb`: one-time test evaluation, PR curves, confusion matrices, timing); verified in Colab
- [ ] Consolidated `final/assign2-ms7556.ipynb` (copy of Step 4 final + author line) verified top-to-bottom in Colab
- [x] 7-page report drafted (`report/Assignment2_Report.pdf`); Colab link still to be inserted
- [ ] Colab Viewer access verified using Columbia LionMail

**Chosen dataset: Bank Marketing.** Local file: `data/bank-additional-full.csv` (semicolon-separated; 41,188 rows). Drop `duration`; explain `pdays=999` and literal `unknown` categories. Home Credit is not used.

### Planned work order (same dual-notebook style as Assignment 1)

For each step: explain in chat → update `notebook/final/` → mirror into `notebook/learning/` with learning notes → run/verify with real outputs.

1. ~~Choose dataset → download to `data/`~~  
2. Step 1 — audit / clean / stratified 70/15/15 / leakage-safe preprocessing  
3. Step 2 — GBDT controlled experiments (~6–10 configs)  
4. Step 3 — MLP controlled experiments (~6–10 configs)  
5. Step 4 — validation AP selection → one-time test evaluation → timing/PR/confusion figures  
6. Consolidate to `final/assign2-ms7556.ipynb` → write the 5–7 page report → verify LionMail Viewer access

## Repository layout

```text
assignment2/
├── Assignment2.pdf
├── AGENTS.md
├── README.md
├── .cursor/
│   └── rules/
│       └── assignment2-workflow.mdc
├── data/
│   └── bank-additional-full.csv     # Chosen dataset (not embedded in notebook)
├── notebook/
│   ├── final/                       # Submission-quality step notebooks
│   │   ├── assign2-bank_step0.ipynb
│   │   ├── assign2-bank_step1.ipynb
│   │   ├── assign2-bank_step2.ipynb
│   │   ├── assign2-bank_step3.ipynb
│   │   ├── assign2-bank_step4.ipynb
│   │   └── assign2-ms7556.ipynb     # Consolidated submission notebook (Colab link)
│   └── learning/                    # Learning / report-prep step notebooks
│       ├── assign2-bank_step0.ipynb
│       ├── assign2-bank_step1.ipynb
│       ├── assign2-bank_step2.ipynb
│       ├── assign2-bank_step3.ipynb
│       └── assign2-bank_step4.ipynb
└── report/
    ├── Assignment2_Report.pdf      # Final 5–7 page report
    └── build_report.py             # Regenerates the PDF from assets/ (set COLAB_URL first)
```

## What each part contains

### `Assignment2.pdf`

The official assignment handout and source of truth for the objective, dataset choices, five steps, experiment requirements, evaluation, report rules, rubric, and Colab access requirements.

### `AGENTS.md`

The detailed project guardrails for AI-assisted development. It records the dataset-specific constraints, leakage rules, controlled experiment requirements, evaluation protocol, report checklist, and definition of done.

### `.cursor/rules/assignment2-workflow.mdc`

A concise always-on Cursor rule. It points Cursor to `AGENTS.md` and reinforces the most important notebook, dataset, experiment, evaluation, and report constraints.

### `data/`

Store the selected dataset's original downloaded file(s) here (currently `bank-additional-full.csv`). Keep data separate from notebook code. Do not download unnecessary tables or files. In Colab, upload the CSV into the notebook working directory (or Drive) rather than depending on this local path.

### `notebook/final/` and `notebook/learning/`

Same dual-track layout as Assignment 1 (`primary`/`stub` there; clearer `final`/`learning` names here):

| Track | Role |
|---|---|
| `notebook/final/assign2-bank_step<N>.ipynb` | Submission-quality code + professional Markdown |
| `notebook/learning/assign2-bank_step<N>.ipynb` | Same implementation + learning notes, TODOs, self-checks, report prompts |

When all steps are done, consolidate the final track into `notebook/final/assign2-ms7556.ipynb` for the Colab link in the PDF. The learning notebooks are for study/report prep and are not the graded Colab artifact.

### `report/Assignment2_Report.pdf`

The final report submitted on Gradescope. It must be 5–7 pages including figures and references, show a page map for Steps 1–5, embed all required figures/tables, and contain no code. The Colab notebook link must be at the very end of the PDF.

## Dataset options and download instructions

Choose exactly one dataset as specified in `Assignment2.pdf`.

### Chosen — Bank Marketing

- Source: UCI Bank Marketing (`bank-additional.zip` → `bank-additional-full.csv`).
- Local path: `data/bank-additional-full.csv`.
- Read with a semicolon delimiter (`sep=";"`).
- Predict `y`; treat `yes` as the positive class.
- **Exclude `duration` from all predictors** because the completed call duration is not available before the call and is a leakage risk.
- Explain how literal `unknown` category values are handled and how `pdays = 999` is represented, since 999 means there was no previous contact.
- Note in the report that a random split does not measure generalization to future campaigns.

### Not used — Home Credit Default Risk

Documented in `Assignment2.pdf` / `AGENTS.md` for completeness only. Do not download or mix with Bank Marketing.

## Environment setup

The assignment suggests pandas, NumPy, scikit-learn, XGBoost, and matplotlib/seaborn. A typical local setup is:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
python -m pip install pandas numpy scikit-learn xgboost matplotlib seaborn jupyter
```

In Google Colab, install any missing packages in a setup cell only when needed. Record the actual package versions and runtime/hardware used for the final comparison; do not assume the environment versions.

## Experimental protocol at a glance

1. Audit the selected dataset: row count, feature types, positive-class proportion, missing values, and special values.
2. Create one stratified **70/15/15 train/validation/test split** with `random_state=42` (after the required Home Credit sample, if applicable).
3. Fit imputation, one-hot encoding, and scaling on training data only. Apply the fitted transforms to validation and test. Scale numeric features for MLP; tree scaling is optional.
4. Train `xgboost.XGBClassifier(tree_method="hist")`. Compare at least three learning rates, then vary max depth and one regularization control. Use validation-based early stopping and monitor logloss.
5. Train `MLPClassifier(solver="adam")`. Compare at least three architectures, then vary learning rate and one of activation/alpha. Use a documented `max_iter` budget and report convergence warnings.
6. Aim for roughly 6–10 configurations per model, record every run, and keep search effort comparable.
7. Select one configuration per model using **validation Average Precision (AP)**. Do not use the test set for tuning.
8. After all choices are fixed, evaluate the selected models on the test set. Use threshold 0.5 for Accuracy, Precision, Recall, and F1; calculate AP from positive-class probabilities with `average_precision_score`.
9. Compare both PR curves (including the test positive-class proportion reference), confusion matrices, fit times, separately measured preprocessing times, model behavior, and interpretability.

The exact requirements and important implementation details are in `Assignment2.pdf` and `AGENTS.md`.

## Required report content and visuals

The report is 5–7 pages including figures and references and should include a page map showing Steps 1–5. A compact structure is:

- **Introduction:** prediction task, positive class, selected dataset, and source.
- **Methods:** data preparation, sampling/split, preprocessing, GBDT and MLP settings, and controlled tuning experiments.
- **Results:** experiment tables, selected-model metrics, training curves, feature importance, PR curves, confusion matrices, and timing comparison.
- **Discussion:** predictive performance, learning behavior, bias/variance, interpretability, preprocessing, and limitations.
- **AI Tool Disclosure:** tools used, their roles, and what was personally checked, changed, executed, and interpreted.

Required visuals include the GBDT training-versus-validation log-loss plot, selected GBDT feature importance with the importance measure named, selected MLP `loss_curve_`, validation performance versus MLP architecture, both models' PR curves with the test prevalence reference, and confusion matrices. Include clear captions and readable labels. **Do not put code in the PDF.**

## Submission checklist

- [ ] One dataset selected; source and data-loading instructions documented.
- [ ] Dataset-specific rules followed (Bank `duration` / `pdays=999`, or Home Credit 30,000-row stratified sample / `SK_ID_CURR`).
- [ ] One stratified 70/15/15 split with seed 42 reused for every experiment.
- [ ] Learned preprocessing fitted on training data only.
- [ ] Same split rows and underlying input information used for GBDT and MLP; MLP numeric features scaled.
- [ ] 6–10 approximately controlled configurations recorded for each model.
- [ ] XGBoost early stopping and validation ordering follow the handout.
- [ ] MLP convergence warnings, architecture comparison, and loss curve are reported.
- [ ] Final configurations selected using validation AP; test set held back until choices are fixed.
- [ ] AP computed from positive-class probabilities with `average_precision_score`.
- [ ] Test metrics use the required threshold 0.5; PR curves, test prevalence reference, and confusion matrices included.
- [ ] Fit time and preprocessing time reported separately on the same runtime; hardware, versions, and seeds recorded.
- [ ] Notebook runs top-to-bottom and all reported results match its actual outputs.
- [ ] PDF is 5–7 pages, includes a page map for Steps 1–5, references, required embedded visuals, and AI disclosure; no code is included.
- [ ] Colab notebook link appears at the very end of the PDF.
- [ ] Colab sharing allows anyone signed in with a Columbia LionMail account to open as Viewer; access has been verified.

## Grading weights (from the handout)

| Category | Weight |
|---|---|
| Data Preparation | 15% |
| GBDT Implementation | 15% |
| MLP Implementation | 15% |
| GBDT vs. MLP Comparison | 25% |
| Evaluation & Visualization | 20% |
| AI Tool Usage Disclosure | 10% |

There is no minimum F1/AP score and neither model is required to win. Fair comparison, correct metrics/figures, and honest interpretation matter more than forcing a winner.

## Important submission reminder

The Colab link is not just a convenience: the assignment states that **10 points will be deducted** if the grader cannot open the notebook using a Columbia LionMail account. Verify the sharing setting and test access before submitting.

## Workflow reference

Use `AGENTS.md` and `.cursor/rules/assignment2-workflow.mdc` the same way Assignment 1 used its guardrails: explain before editing, update the final notebook and the learning notebook for each step, validate with real outputs, and keep the final track submission-ready.

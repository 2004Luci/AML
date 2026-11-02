# Assignment 2 — From Trees to Neural Networks

This folder contains the work for **Assignment 2**, which compares gradient-boosted decision trees (GBDT) with a multi-layer perceptron (MLP) on one tabular dataset.

The assignment focuses on controlled experiments, predictive performance, learning behavior, runtime, and interpretability. A GPU is not required.

## Status

- [x] Assignment specification added (`Assignment2.pdf`)
- [x] Workflow guardrails added (`AGENTS.md` and `.cursor/rules/assignment2-workflow.mdc`)
- [ ] Dataset selected and downloaded
- [ ] Data preparation and 70/15/15 split implemented
- [ ] GBDT experiments completed
- [ ] MLP experiments completed
- [ ] Final validation-based model selection and one-time test evaluation completed
- [ ] Notebook verified top-to-bottom in Colab
- [ ] 5–7 page report completed and checked
- [ ] Colab Viewer access verified using Columbia LionMail

**Dataset selection is still pending.** The handout describes Bank Marketing as the simpler option to download and run. Both dataset choices receive the same grading treatment. Choose one before implementing the dataset-specific notebook path; do not combine them.

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
│   └── raw/                         # Downloaded source data (not embedded in notebook)
├── notebook/
│   └── assign2-ms7556.ipynb         # Final consolidated, runnable notebook
└── report/
    └── Assignment2_Report.pdf      # Final 5–7 page report
```

## What each part contains

### `Assignment2.pdf`

The official assignment handout and source of truth for the objective, dataset choices, five steps, experiment requirements, evaluation, report rules, rubric, and Colab access requirements.

### `AGENTS.md`

The detailed project guardrails for AI-assisted development. It records the dataset-specific constraints, leakage rules, controlled experiment requirements, evaluation protocol, report checklist, and definition of done.

### `.cursor/rules/assignment2-workflow.mdc`

A concise always-on Cursor rule. It points Cursor to `AGENTS.md` and reinforces the most important notebook, dataset, experiment, evaluation, and report constraints.

### `data/raw/`

Store the selected dataset's original downloaded file(s) here. Keep raw data separate from notebook code. Do not download unnecessary tables or files.

### `notebook/assign2-ms7556.ipynb`

The primary technical deliverable. It should contain setup and data-loading instructions, the complete reproducible analysis, actual outputs, report-ready figures, and enough professional Markdown to explain the decisions. The notebook should run top-to-bottom in Colab.

### `report/Assignment2_Report.pdf`

The final report submitted on Gradescope. It must be 5–7 pages including figures and references, show a page map for Steps 1–5, embed all required figures/tables, and contain no code. The Colab notebook link must be at the very end of the PDF.

## Dataset options and download instructions

Choose exactly one dataset as specified in `Assignment2.pdf`.

### Option A — Bank Marketing (simpler option in the handout)

- Download `bank-additional.zip` from the UCI Bank Marketing source linked in the assignment handout.
- Extract `bank-additional-full.csv`.
- Place it at `data/raw/bank-additional-full.csv`.
- Read it with a semicolon delimiter (`sep=";"`).
- Predict `y`; treat `yes` as the positive class.
- **Exclude `duration` from all predictors** because the completed call duration is not available before the call and is a leakage risk.
- Explain how literal `unknown` category values are handled and how `pdays = 999` is represented, since 999 means there was no previous contact.
- Note in the report that a random split does not measure generalization to future campaigns.

### Option B — Home Credit Default Risk

- Download `application_train.csv` from the Kaggle Home Credit Default Risk competition, after accepting the relevant data terms if required.
- Place it at `data/raw/application_train.csv`.
- Use this file only; do not join the other competition tables.
- Separate `TARGET` from predictors and drop `SK_ID_CURR`.
- Before splitting, take one **30,000-row sample stratified on `TARGET` with `random_state=42`**. Reuse exactly this sample for every experiment.

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

## Important submission reminder

The Colab link is not just a convenience: the assignment states that **10 points will be deducted** if the grader cannot open the notebook using a Columbia LionMail account. Verify the sharing setting and test access before submitting.

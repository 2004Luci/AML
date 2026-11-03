# Assignment 2 — AI/ML Workflow Guardrails

## 0. Purpose and source of truth

This repository contains the work for **Assignment 2: From Trees to Neural Networks**.

The authoritative specification is `Assignment2.pdf`. It is the source of truth for the objective, permitted datasets, required experiments, evaluation procedure, report requirements, rubric, AI disclosure, and submission/access rules. Do not replace its instructions with generic machine-learning conventions or assumptions from Assignment 1.

### Deliverables

1. A runnable Jupyter/Colab notebook (`.ipynb`) containing setup, data-loading instructions, code, explanations, and outputs needed to reproduce the results.
2. A **5–7 page PDF report**, including figures and references, submitted on Gradescope. The report must include a page map showing where Steps 1–5 are addressed.

The Google Colab notebook link must appear **at the very end of the PDF report**. Set notebook sharing so anyone signed in with a Columbia LionMail account can open it as a Viewer without requesting access. Verify this before submission; the handout states that inaccessible notebooks incur a 10-point deduction.

### Required notebook locations

Maintain the two notebook tracks in these exact directories (same dual-track workflow as Assignment 1; folder names updated for clarity):

- **Final / submission notebooks:** `/notebook/final/`
- **Learning notebooks:** `/notebook/learning/`

For step `N`, use:

- `/notebook/final/assign2-bank_step<N>.ipynb`
- `/notebook/learning/assign2-bank_step<N>.ipynb`

After all steps are complete, consolidate the submission track into the Colab deliverable:

- `/notebook/final/assign2-ms7556.ipynb`

Do not place step-specific notebooks elsewhere unless explicitly requested. The `.ipynb` is the primary technical deliverable; repository polish must not take priority over notebook correctness, reproducibility, student understanding, or assignment compliance.

### Rubric weights (from `Assignment2.pdf`)

| Category | Weight | Focus |
|---|---|---|
| Data Preparation | 15% | Correct split and preprocessing; justified choices; no leakage |
| GBDT Implementation | 15% | Correct training, controlled tuning, early stopping, learning dynamics |
| MLP Implementation | 15% | Correct scaling, training, controlled tuning, learning dynamics |
| GBDT vs. MLP Comparison | 25% | Fair comparison of performance, time, and behavior; thoughtful analysis |
| Evaluation & Visualization | 20% | Correct metrics and clear required figures embedded in the PDF |
| AI Tool Usage Disclosure | 10% | Transparent account of AI assistance and student verification |

Comparison and evaluation together are 45% of the grade. Do not underinvest in fair comparison, required figures, or interpretation just to add more tuning runs.

---

## 1. Non-negotiable working protocol

For every meaningful assignment step, follow this three-part sequence (matching Assignment 1).

### A. Explain before implementing

Explain the work in chat before making substantial notebook changes. Assume the student may be learning the practical concepts for the first time. Cover:

1. What is being done and why.
2. The problem it solves and the underlying concept.
3. What the important code and parameters mean.
4. Reasonable alternatives and why the selected approach is appropriate.
5. Risks, assumptions, and possible failure modes.
6. How the choice satisfies the assignment.
7. What the student should be able to explain in a code review/oral discussion.
8. What outputs, figures, and observations belong in the report.

Do not merely paste code without teaching the decision behind it.

### B. Update the final / submission notebook

Create/update the submission-quality notebook for the current step:

`/notebook/final/assign2-bank_step<N>.ipynb`

This is the primary deliverable track. Preserve working sections and previous verified decisions. Avoid broad rewrites when a small, targeted edit is sufficient.

The final notebook must:

- run top-to-bottom in the intended Jupyter/Colab environment;
- include setup and clear data-loading instructions;
- be reproducible through fixed, documented random seeds;
- use clear names and modular, readable cells;
- contain professional Markdown explaining methodology and interpretation;
- include actual, relevant outputs and report-ready figures;
- avoid tutorial clutter, temporary debugging cells, stale output, and unresolved TODOs in the final version;
- avoid dead code and unnecessary imports;
- avoid submission-noise aimed at graders or process notes such as “checkpoint”, “current scope”, “notebook goal”, or step-handoff text;
- never contain fabricated results or claims of execution that did not occur.

Production-style does not mean explanation-free: retain enough Markdown for a reader to understand the analysis and the reasons for important decisions.

### C. Update the learning notebook

Create/update the parallel learning notebook for the same step:

`/notebook/learning/assign2-bank_step<N>.ipynb`

This is **not** the Colab submission artifact. It should use the same correct implementation as the final notebook, plus:

- detailed explanations and conceptual reminders;
- TODOs and “why are we doing this?” notes;
- questions the student should be able to answer;
- report-writing prompts;
- places to record observations after Colab runs;
- reminders about assignment/rubric compliance.

The learning notebook may be verbose and pedagogical. Keep it in sync with the final notebook for each step.

### D. Run, inspect, and checkpoint

Never invent runtime-dependent results. Ask the student to run the notebook in Colab when execution is required, then inspect the actual outputs they provide before interpreting results or making subsequent data-dependent decisions.

At each checkpoint verify that the relevant cells run, outputs are genuine, the assignment requirements for that stage are covered, and report-relevant observations are recorded.

---

## 2. Priority order

Always prioritize:

1. `Assignment2.pdf` compliance.
2. Technical correctness and leakage prevention.
3. Fair, controlled GBDT-versus-MLP experiments.
4. A reproducible, high-quality submission notebook.
5. Student understanding and ability to defend decisions.
6. Report readiness and accurate interpretation.
7. Repository organization and cosmetic polish.

Do not optimize solely for the highest score. The handout explicitly states that neither model is required to win and there is no fixed minimum F1 or AP score for full credit. A defensible experiment and honest analysis are more important than manufacturing a favorable result.

Do not add complex techniques, extensive searches, or extra models that are not needed for the assignment.

---

## 3. Dataset choice and dataset-specific guardrails

**Chosen dataset: Bank Marketing.** Local file: `data/bank-additional-full.csv`. Do not switch to Home Credit or mix the two datasets.

### Bank Marketing (active)

- Use `bank-additional-full.csv` (41,188 rows) from `bank-additional.zip`.
- Repository path: `assignment2/data/bank-additional-full.csv` (flat `data/` folder; no `raw/` subdirectory).
- Read the CSV with a semicolon separator (`sep=";"`).
- Predict whether a client subscribes to a term deposit.
- Treat `y = "yes"` as the positive class and encode the target consistently as 1; `"no"` is 0.
- **Drop `duration` from predictors.** It is the completed call duration and is unavailable before the call, so including it would leak information unavailable at prediction time. Do not reintroduce it through derived features.
- Inspect and explain how literal `unknown` category values are handled. They are dataset values, not automatically the same thing as a previously unseen category.
- Explain how `pdays = 999` is handled. It means there was no previous contact; do not silently interpret it as 999 elapsed days, discard it, or replace it without preserving/explaining its meaning. A documented indicator plus a justified numeric representation is one possible strategy; other approaches are acceptable if reasoned and applied consistently.
- A random split does not establish generalization to future campaigns. State this limitation in the report.
- The handout treats this as a historical benchmark, not evidence of current banking performance.
- Notebooks are written for **Google Colab submission**: expect `bank-additional-full.csv` in the notebook working directory via Colab Files → Upload. Do not hard-code this git repo’s paths (`assignment2/data/`, `../data`, GitHub raw URLs, etc.) inside `.ipynb` code. The student copies the `.ipynb` into Colab; the notebook must run there standalone.

### Step 1 decisions (fixed; verified by running the notebook)

Audit facts: 41,188 × 21; 10 numeric + 10 nominal + target; positive rate 11.27%; no NaNs; literal `"unknown"` in `default` (8,597), `education` (1,731), `housing`/`loan` (990), `job` (330), `marital` (80); `pdays = 999` in 39,673 rows (96.32%), real range 0–27; 12 exact duplicates.

| Item | Decision |
|---|---|
| Target | `y == "yes"` → 1 |
| `duration` | Dropped |
| `pdays = 999` | `previously_contacted` 0/1 flag; `pdays` → −1 when no contact |
| `"unknown"` | Kept as its own category, one-hot encoded |
| NaN | None; no imputer |
| Duplicates | Kept (no ID; 12 rows) |
| Split | Two-stage stratified 70/15/15, `random_state=42` → 28,831 / 6,178 / 6,179 rows |
| Preprocessing | `ColumnTransformer` fit on train only: one-hot (`handle_unknown="ignore"`) for 10 categoricals; numeric passthrough for GBDT, `StandardScaler` for MLP; 63 encoded features for both |
| Timing | `PREPROCESSING_TIME_SEC` recorded per model input, separately from fit time |

Variables later steps rely on: `X_train_tree/X_valid_tree/X_test_tree`, `X_train_mlp/X_valid_mlp/X_test_mlp`, `y_train/y_valid/y_test`, `PREPROCESSING_TIME_SEC`, `RANDOM_STATE`.

### Step 2 design (GBDT; verified in Colab after cap change)

- Fixed: `tree_method="hist"`, `n_estimators=5000` cap, `early_stopping_rounds=50` and `eval_metric="logloss"` in the constructor, `eval_set=[train, validation]` (validation last), `random_state=42`, other params default.
- Reference config: `learning_rate=0.1`, `max_depth=4`, `subsample=1.0`.
- Phase A: `learning_rate` ∈ {0.01, 0.1, 0.3}. Phase B: `max_depth` ∈ {2, 4, 6, 8} at best lr. Phase C (regularization): `subsample` ∈ {1.0, 0.8, 0.6} at best lr + depth. 8 configurations total (reference shared).
- Selection: highest validation AP (`average_precision_score` on `predict_proba[:, 1]`). Colab (source of truth) selected G7: lr 0.01, depth 4, subsample 0.8, AP 0.4923; AP range 0.4818–0.4923. Local macOS/XGBoost 2.1.4 picks a different path (lr 0.1 → G8) because phase-A AP gaps are ~0.002; notebook interpretation follows Colab.
- Cap raised 3000 → 5000 after Colab showed depth 2 at lr 0.01 hitting the cap; `hit_cap` column flags any unconverged run. Colab rerun: 0 runs at cap (G4 now stops at 3,136), selection unchanged (G7).
- Colab runtime for the report: Python 3.13.18, pandas 2.2.3, numpy 2.4.6, scikit-learn 1.6.1, xgboost 3.4.1, matplotlib 3.10.0, Linux x86_64, 2 CPU cores.
- Per-config `fit_sec` is noisy on Colab's shared 2 cores (G8 16.4 s vs G7 6.1 s with similar tree counts). Step 4 must re-time the selected GBDT and MLP with repeats on the same runtime instead of reusing these values.
- Selection uses unrounded `valid_AP` from `gbdt_records` (not the 4-dp rounded `gbdt_results` table).
- Importance: **total gain** share over trees `0..best_iteration` inclusive (`trees_to_dataframe`), top 15 — not average gain via `get_score("gain")`. Figures saved as `fig_gbdt_learning_rates.png`, `fig_gbdt_selected_logloss.png`, `fig_gbdt_feature_importance.png`.
- Variables for later steps: `gbdt_selected`, `GBDT_SELECTED_ID`, `GBDT_FIT_TIME_SEC`, `gbdt_results`.

### Step 3 design (MLP; verified in Colab)

- Fixed: `MLPClassifier(solver="adam", activation="relu", max_iter=200, early_stopping=False, random_state=42)`, `batch_size="auto"`, `tol=1e-4`, `n_iter_no_change=10` (defaults) on `X_train_mlp` (scaled numerics + one-hot).
- Reference config: `hidden_layer_sizes=(64,)`, `learning_rate_init=0.001`, `alpha=0.0001` (scikit-learn defaults for lr/alpha).
- Phase A: `hidden_layer_sizes` ∈ {(64,), (128, 64), (128, 64, 32)}. Phase B: `learning_rate_init` ∈ {0.0001, 0.001, 0.01} at best architecture. Phase C (regularization): `alpha` ∈ {0.0001, 0.01, 0.1, 1.0} at best architecture + lr. 8 configurations total (matches GBDT).
- `ConvergenceWarning`s are captured per run, printed with the config ID, and stored in `converged`; other warnings are re-emitted. `final_train_loss` (last `loss_curve_` value) includes the L2 penalty; `train_logloss`/`valid_logloss` are penalty-free and comparable with GBDT.
- Selection: highest unrounded validation AP from `mlp_records`.
- No per-epoch validation curve: `partial_fit` replay does not reproduce `fit` exactly, so the selected-model figure shows `loss_curve_` plus final train/validation log loss lines.
- Colab (source of truth) selected M6: (64,), lr 0.0001, alpha 0.01, validation AP 0.4825; AP range 0.3180–0.4825. M1–M3 overfit at default lr/alpha (AP 0.410 / 0.318 / 0.350; validation log loss up to 1.13). 4 of 8 runs (M1, M2, M4, M5) hit the 200-epoch budget with `ConvergenceWarning`. Local macOS run matches except M3 (133 vs 150 epochs, AP 0.3448 vs 0.3505); selection path identical. Local runs also print spurious numpy/Accelerate `matmul` RuntimeWarnings (macOS BLAS artifact; absent on Colab).
- Colab `fit_sec` 9–49 s per config (M6 14.2 s); noisy on shared cores, re-time in Step 4.
- Figures: `fig_mlp_architectures.png`, `fig_mlp_learning_rates.png`, `fig_mlp_selected_loss.png`.
- Variables for later steps: `mlp_selected`, `MLP_SELECTED_ID`, `MLP_FIT_TIME_SEC`, `mlp_results`.

### Home Credit Default Risk (not used)

Kept only so the handout alternative remains documented. Do not download, sample, or implement this path unless the student explicitly changes the dataset choice.

- Would use `application_train.csv` only; drop `SK_ID_CURR`; separate `TARGET`; take one 30,000-row TARGET-stratified sample with `random_state=42` before splitting.

### Dataset-neutral rule

Use only the permitted Bank Marketing source file, document the source and the actual shape, and never change the dataset or sample silently after experiments begin.

---

## 4. Step 1 — Data preparation

The handout requires the following:

### 4.1 Initial data audit

Report:

- number of rows and columns;
- feature types (numeric, nominal categorical, and any other relevant types);
- positive-class proportion;
- missing values and meaningful special/sentinel values;
- cleaning decisions and their justifications.

Inspect the actual chosen dataset. Do not assume missingness, category names, invalid values, or class balance before checking the data.

### 4.2 Train/validation/test split

Create a stratified **70/15/15 train/validation/test split** with `random_state = 42`.

For Home Credit, perform the required stratified 30,000-row sample first, then create this split. The selected sample and split rows must remain identical across all GBDT and MLP experiments.

Use the validation set for model selection and early-stopping decisions as specified. Keep the test set untouched until both final configurations and all analytical choices are fixed.

### 4.3 Leakage-safe preprocessing

- Fit every learned preprocessing operation on training data only.
- Apply the already-fitted transformations to validation and test data.
- Use one-hot encoding for nominal categorical features.
- Handle categories not observed during training safely, e.g. with an encoder configured to ignore unseen categories; separately explain literal `unknown` values present in Bank Marketing.
- Handle missing values with a justified strategy fitted on training data only.
- Scale numeric features for the MLP. Scaling is optional for trees.
- Keep the same underlying input information and the exact same split rows for both models. Model-specific transformations such as numeric scaling are acceptable and should be explained; do not give one model extra target information or different source rows.
- Keep the target out of the predictors.

Prefer `ColumnTransformer` and `Pipeline` where practical. If transformations are performed outside a pipeline for XGBoost early stopping, fit them only on training data and apply the same fitted transformer to the training, validation, and test partitions.

Be able to explain the distinction between `fit` / `fit_transform` on training data and `transform` on validation/test data.

---

## 5. Step 2 — Gradient Boosted Decision Trees (GBDT)

The required estimator is `xgboost.XGBClassifier` with `tree_method="hist"`.

### Required controlled experiments

- Use binary log loss (`logloss`) to monitor training and validation performance.
- Compare at least three `learning_rate` values (examples in the handout: `0.01`, `0.1`, `0.3`) while holding other settings fixed.
- Then vary `max_depth` and **one** regularization control: `subsample`, `reg_alpha`, or `reg_lambda`.
- Aim for roughly 6–10 total configurations for this model. A full Cartesian grid is not required. Keep search effort comparable to the MLP experiments.
- Record every configuration tried and its validation score. Do not omit failed, interrupted, or warning-producing runs if they are part of the actual experiment history; describe them accurately.

### Early stopping requirements

- Set a reasonable upper limit on `n_estimators`.
- Use validation-based early stopping.
- Put `early_stopping_rounds` and `eval_metric` in the `XGBClassifier` constructor, as specified by the handout.
- Pass transformed training and validation data to `fit()` through `eval_set`.
- Put the validation set **last** in `eval_set` so it controls early stopping.
- Never use the test set as an early-stopping set or in hyperparameter selection.
- Record the best iteration / stopping behavior and distinguish the early-stopping monitor (`logloss`) from the primary cross-configuration selection metric (`validation AP`).

### Required GBDT outputs

- training-versus-validation log-loss plot for the selected model;
- feature-importance plot for the selected model;
- table of tried settings and validation scores;
- explicit statement of the feature-importance measure used (for example, gain);
- explanation of how learning rate, depth/tree complexity, and the selected regularization control affected convergence or overfitting.

Feature importance is an association-based model explanation, not a causal claim. Report transformed feature names clearly if one-hot encoding is used.

---

## 6. Step 3 — Multi-Layer Perceptron (MLP)

Use `sklearn.neural_network.MLPClassifier` with `solver="adam"`.

### Required controlled experiments

- Compare at least three `hidden_layer_sizes` settings (examples in the handout: `(64,)`, `(128, 64)`, `(128, 64, 32)`) while holding other settings fixed.
- Then vary `learning_rate_init` and **one** of `activation` or `alpha` (L2 regularization).
- Aim for roughly 6–10 total configurations. Record every configuration tried and keep the search effort comparable to GBDT.
- Use `max_iter` as a fixed/documented training budget across comparable configurations where possible.
- Capture and report convergence warnings. Do not hide or silently suppress them.
- For the simple comparison recommended in the handout, use `early_stopping=False`.

If built-in MLP early stopping is enabled instead:

- explain that scikit-learn reserves an internal validation subset from the training data;
- document the choice and its implications for the effective training subset;
- continue using the shared external validation set for final model selection;
- do not replace or tune against the external test set.

### Required MLP outputs

- selected model's training-loss curve from `loss_curve_`;
- plot or table of validation performance versus architecture;
- record of configurations and validation scores;
- explanation of how width/depth, learning rate, and the varied regularization/activation choice affected results;
- discussion of convergence warnings and the chosen `max_iter` budget.

Numeric scaling must be fitted on training data only. Do not use unscaled numerical features for MLP merely to make its code match the tree pipeline.

---

## 7. Experiment budget and fair comparison

The handout recommends approximately **6–10 configurations per model**. Experiments may share a configuration where sensible; a full Cartesian product is unnecessary.

- Keep the search effort broadly comparable across GBDT and MLP.
- Use controlled comparisons: change the parameter being studied while keeping other settings fixed for that comparison.
- Record every tried configuration and its validation AP; include relevant convergence/early-stopping information.
- Use the same training and validation rows for every configuration and both model families.
- Use the same target definition and underlying predictor information.
- Fix and document random seeds.
- Avoid searching against the test set or selecting settings after looking at test metrics.

Do not claim a controlled experiment if several parameters changed at once. Explain when a configuration is an exploratory follow-up rather than a one-variable comparison.

---

## 8. Step 4 — Model evaluation and comparison

### 8.1 Primary model-selection metric

The primary metric is **validation Average Precision (AP)** for the positive class.

- Use positive-class probabilities, e.g. `predict_proba(X_valid)[:, 1]`.
- Compute AP with `sklearn.metrics.average_precision_score`.
- Do not compute AP from thresholded labels.
- Do not substitute trapezoidal area under the precision-recall curve for average precision.
- Choose one final configuration per model using validation AP.
- Keep the test set untouched until both configurations and analysis decisions are fixed.

For XGBoost, early stopping is monitored by validation logloss as required, while the choice among experiment configurations is based on validation AP. Explain this distinction.

### 8.2 Final test evaluation

After choices are fixed, evaluate the selected fitted GBDT and MLP once on the test set.

Report for the positive class:

- Accuracy;
- Precision;
- Recall;
- F1;
- Average Precision (AP).

Use a classification threshold of **0.5** for Accuracy, Precision, Recall, and F1. AP uses probabilities and is threshold-independent. If any additional threshold is tuned, select it using validation data only and clearly label it as an additional analysis; preserve the required 0.5-threshold results.

Include:

- both models' precision-recall curves;
- the test set's positive-class proportion as the PR-curve reference level;
- confusion matrices for both models;
- a side-by-side final comparison table.

### 8.3 Runtime and environment comparison

- Measure final-model fit time on the same machine/runtime and report preprocessing time separately.
- Use the same hardware/runtime for both fit-time measurements.
- Do not compare a CPU run with a GPU run as if hardware were identical.
- Record hardware/runtime details, package versions, and random seeds.
- Keep preprocessing time distinct from model fitting time; state clearly what each timing includes.

### 8.4 Interpretation

Discuss:

- when GBDT may be preferred over MLP and vice versa for tabular data;
- sensitivity to learning rate, tree complexity, architecture, scaling, and regularization;
- predictive performance versus training behavior and fit time;
- how missing values and categorical features were handled;
- bias/variance and generalization limitations;
- the limits of feature importance (association, not causation).

The handout explicitly permits either model to perform better. Do not force a winner or imply that a higher score alone proves a better general model.

---

## 9. Step 5 — PDF report guardrails

The report must be **5–7 pages including figures and references** and submitted on Gradescope.

Include a page map showing where Steps 1–5 are covered. A clear structure is:

1. Introduction — task, target/positive class, dataset, data source.
2. Methods — sample/split, cleaning, preprocessing, model setup, controlled tuning experiments.
3. Results — experiment tables, selected model metrics, PR curves, confusion matrices, loss curves, feature importance, and training/preprocessing time.
4. Discussion — GBDT versus MLP, learning behavior, bias/variance, interpretability, limitations.
5. AI Tool Disclosure — tools, their roles, and what the student personally checked, changed, ran, and interpreted.

Report requirements:

- Embed every required graph and table directly in the PDF. The grader will not open the notebook to locate missing figures.
- Use readable axes, labels, legends, captions, and tables. Do not shrink figures excessively to fit more experiments.
- Keep code out of the report, including appendices.
- Include references for the dataset and relevant external documentation.
- Put the Colab notebook link at the **very end** of the PDF.
- Verify the Colab Viewer permission using a Columbia LionMail account before submission.

Figures/tables should be generated from actual notebook outputs. Do not manually type results that differ from the notebook.

---

## 10. AI usage disclosure

AI tools are explicitly permitted, but the final report must transparently disclose:

- the tools used;
- what each tool contributed;
- what the student checked, changed, executed, validated, and interpreted personally.

Do not claim AI-generated code was independently authored. Do not understate AI assistance or invent contributions. Make sure the disclosure matches the actual workflow (for example, ChatGPT, Cursor, and any other tool actually used).

The student should be able to explain the implementation, including preprocessing, leakage prevention, XGBoost early stopping, learning-rate effects, MLP scaling/architecture, convergence warnings, AP, and the final comparison.

---

## 11. Notebook organization and technical style

Build step notebooks incrementally under `final/` and `learning/`. Each step notebook should include the prior verified pipeline plus the new step’s work, so it remains runnable top-to-bottom.

Typical section order across the full assignment:

1. Title, objective, dataset/source, and reproducibility notes.
2. Environment/setup and imports.
3. Data loading instructions and initial audit.
4. Target definition and leakage exclusions (`duration`, `pdays=999`, `unknown`).
5. Stratified 70/15/15 split.
6. Preprocessing fitted on training data only.
7. GBDT controlled experiments and selected-model diagnostics.
8. MLP controlled experiments and selected-model diagnostics.
9. Validation-based model selection.
10. One-time final test evaluation and runtime comparison.
11. Interpretation, limitations, and report-ready findings.

Follow this cell pattern where useful:

- Markdown: what is being done and why.
- Code: implement one logical unit.
- Output: show actual results.
- Markdown: interpret what the results support and what they do not support.

In the **learning** notebook, additionally use blockquotes for learning notes, TODOs, self-check questions, and report prompts.

Avoid giant monolithic cells. Comments should explain intent, non-obvious assumptions, and risks rather than restating obvious syntax.

Include clear instructions for locating/uploading the data in Colab. Do not assume a local filesystem path is available in Colab. Keep raw data out of the notebook itself.

At the start or end, include a reproducibility/environment summary with at least Python, pandas, NumPy, scikit-learn, XGBoost, and relevant plotting-library versions, random seeds, and runtime/hardware information.

---

## 12. What Cursor must not do

Do not:

- silently choose or switch the dataset;
- use both datasets in one experiment;
- use the Bank Marketing `duration` predictor or a derivative of it;
- ignore the meaning of `pdays = 999`;
- forget the required Home Credit 30,000-row stratified sample or perform it after the train/validation/test split;
- use Home Credit tables beyond `application_train.csv`;
- keep `SK_ID_CURR` as a predictor;
- alter the selected sample or split rows between experiments;
- fit imputation, encoding, scaling, or other learned preprocessing on validation/test data;
- scale only one model's features in a way that changes the underlying input information;
- omit either model family or replace either required estimator with another model;
- omit any required controlled hyperparameter comparison;
- exceed the intended experiment budget without a reason;
- put XGBoost `early_stopping_rounds` or `eval_metric` only in `fit()` instead of the classifier constructor;
- place validation before training in the XGBoost `eval_set` ordering (validation must be last);
- use the test set for early stopping, tuning, or model selection;
- choose final models using test AP;
- compute AP from thresholded labels or trapezoidal PR area;
- omit the test-prevalence reference level from the PR plot;
- hide MLP convergence warnings;
- report training time and preprocessing time as if they were the same measurement;
- compare timings from different hardware as if comparable;
- fabricate or hand-edit results that do not match notebook outputs;
- claim feature importance proves causality;
- assume one model must win or a minimum score is required;
- omit required graphs/tables from the PDF;
- put code in the PDF;
- omit AI disclosure;
- omit the Colab link at the end of the PDF or fail to verify LionMail Viewer access;
- silently contradict `Assignment2.pdf`.

---

## 13. Definition of done

The Assignment 2 work is ready only when:

### Data preparation

- one permitted dataset is selected and its source documented;
- the actual dataset audit reports size, feature types, positive-class proportion, missing values, and special values;
- dataset-specific rules are followed (Bank `duration` exclusion and `pdays=999` explanation, or Home Credit 30,000-row stratified sample and identifier/target exclusions);
- a stratified 70/15/15 split with `random_state=42` is created and reused;
- all learned preprocessing is fitted on training data only;
- nominal categoricals are one-hot encoded;
- MLP numeric features are scaled;
- both models use the same rows and underlying input information.

### GBDT

- `XGBClassifier(tree_method="hist")` is trained;
- logloss is monitored on training and validation data;
- at least three learning rates are compared with other settings held fixed;
- max depth and one regularization control are varied;
- roughly 6–10 configurations are recorded;
- early stopping is configured in the estimator constructor and validation is last in `eval_set`;
- training/validation log-loss and feature-importance plots are present;
- the importance measure is named and results are interpreted.

### MLP

- `MLPClassifier(solver="adam")` is trained on scaled numeric inputs;
- at least three architectures are compared with other settings held fixed;
- learning rate and one of activation/alpha are varied;
- roughly 6–10 configurations are recorded;
- max iteration budget and convergence warnings are reported;
- early-stopping choice is documented;
- selected-model `loss_curve_` and validation-performance-by-architecture output are present.

### Evaluation and report

- final configurations are selected by validation AP;
- test set remains untouched until choices are fixed and is evaluated only for final reporting;
- AP uses positive-class probabilities with `average_precision_score`;
- classification metrics use threshold 0.5;
- both PR curves, test positive-class reference level, confusion matrices, and a comparison table are present;
- final fit time and preprocessing time are separately measured on the same runtime;
- hardware, package versions, and random seeds are recorded;
- the PDF is 5–7 pages, contains a page map for Steps 1–5, embeds required figures/tables, includes references and AI disclosure, and contains no code;
- Colab link is at the very end and LionMail Viewer access is verified;
- the notebook runs top-to-bottom and all reported results match its real outputs.

---

## 14. Change protocol

When asked to continue or edit a step:

1. **Inspect** the current final + learning notebooks, `Assignment2.pdf`, `AGENTS.md`, and any real execution outputs the student provides.
2. **Explain** the planned change in chat before substantial notebook edits.
3. **Edit** `/notebook/final/assign2-bank_step<N>.ipynb` with the smallest sufficient change. Preserve working, verified sections.
4. **Mirror** the same implementation into `/notebook/learning/assign2-bank_step<N>.ipynb`, adding or updating learning notes, TODOs, self-check questions, and report prompts.
5. **Verify** with real runs (student Colab or local). Never invent outputs.
6. **Confirm** the change still meets the relevant assignment requirements before moving on.
7. **Record** durable decisions that should persist across sessions (dataset choice, cleaning rules, selected hyperparameters, seeds) back into `AGENTS.md` or the notebook Markdown when they become fixed.

Suggested step notebooks (Assignment 1 style):

| Step | Focus | Notebooks |
|---|---|---|
| 0 | Scaffold: setup + Colab data upload + initial load (kept for history) | `assign2-bank_step0.ipynb` |
| 1 | Audit, clean, 70/15/15 split, leakage-safe preprocessing | `assign2-bank_step1.ipynb` in `final/` and `learning/` |
| 2 | GBDT controlled experiments + selected-model diagnostics | `assign2-bank_step2.ipynb` |
| 3 | MLP controlled experiments + selected-model diagnostics | `assign2-bank_step3.ipynb` |
| 4 | Validation AP selection, one-time test eval, timing/PR/confusion | `assign2-bank_step4.ipynb` |
| Final | Consolidated Colab submission notebook | `final/assign2-ms7556.ipynb` |
| Report | 5–7 page PDF + LionMail Viewer verification | `report/Assignment2_Report.pdf` |

Dataset download into `data/` is done (Bank Marketing). Do not start report writing before the notebook’s final figures and tables exist. Do not inspect the test set for model selection.

---

## 15. Final principle

The objective is not simply to execute two classifiers. It is to produce a technically correct, reproducible, controlled comparison of gradient-boosted trees and an MLP on one permitted tabular dataset, understand how their learning behavior and preprocessing differ, evaluate them without test leakage, and communicate the evidence accurately.

When in doubt:

**`Assignment2.pdf` → correctness and leakage control → fair experiments → notebook reproducibility → student understanding → report quality → repository polish.**

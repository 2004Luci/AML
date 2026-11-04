# Assignment 2 — Workflow Guardrails

## 0. Purpose

This folder holds **Assignment 2: From Trees to Neural Networks** (COMS W4995 Applied Machine Learning).

### Deliverables

| Deliverable | Path |
|---|---|
| Runnable notebook (Colab, outputs saved) | `/notebook/assign2-ms7556.ipynb` |
| Written report (5–7 pages, no code) | `/report/Assignment2_Report.pdf` |
| Report figures | `/assets/` |
| Assignment handout | `Assignment2.pdf` |

`Assignment2.pdf` is the source of truth for requirements, experiments, metrics, report rules, rubric, AI disclosure, and Colab access.

The notebook is the technical deliverable: all code, outputs, figures, and technical reasoning live there. The PDF is written from those results. Repository layout is secondary.

The notebook reads `bank-additional-full.csv` from its working directory (Colab upload) and otherwise downloads the same file from this repository's `assignment2/data/` on GitHub. Colab is the source of truth for every reported number.

---

# 1. Workflow for each change

## A — Explain in chat

Before a meaningful change, explain:

1. What is being done
2. Why
3. What problem it solves
4. What important code means
5. Alternatives and why this choice
6. Risks / failure modes
7. How it satisfies `Assignment2.pdf`
8. What the student should be able to defend in review
9. What belongs in the PDF report

Do not assume prior ML background.

## B — Update the notebook

Edit `/notebook/assign2-ms7556.ipynb`.

The notebook must:

- run top-to-bottom without errors in Colab
- be reproducible (`RANDOM_STATE = 42`, documented split)
- use clear names and short comments only where intent is non-obvious
- use Markdown for methodology, decisions, and interpretation
- show real outputs and figures (never invent results)
- avoid TODOs, placeholders, dead code, and meta/process notes aimed at graders
- comply with `Assignment2.pdf`

Student-facing teaching can stay in chat. The notebook itself should read as a finished submission.

## C — Re-run and re-sync

Any code change requires a fresh Colab run. After it, update the notebook's interpretation text and the report so every number matches the new outputs (timings change between runs).

---

# 2. Priorities

1. `Assignment2.pdf` compliance
2. Correctness and leakage control
3. Fair, controlled GBDT-versus-MLP comparison
4. Clear, defensible notebook
5. Student understanding
6. Report readiness
7. Repository polish

Neither model is required to win and there is no minimum AP/F1. Do not add unrequested models or large searches.

---

# 3. Required pipeline

audit → cleaning → split → leakage-safe preprocessing → GBDT experiments → MLP experiments → validation-AP selection → one-time test evaluation → interpretation → report

---

# 4. Dataset rules

Dataset: **UCI Bank Marketing**, `bank-additional-full.csv` (`sep=";"`). Home Credit is not used.

- Predict `y`; `"yes"` = 1 is the positive class
- Drop `duration` (known only after the call: leakage)
- Explain `pdays = 999` and literal `"unknown"` values
- A random split does not test future campaigns; the data are a historical benchmark (2008–2010)

---

# 5. Known audit facts

- 41,188 × 21; 10 numeric + 10 nominal predictors + target
- Positive rate 11.27% (4,640 yes)
- No NaNs; `"unknown"` in `default` 8,597, `education` 1,731, `housing`/`loan` 990, `job` 330, `marital` 80
- `pdays = 999` in 39,673 rows (96.32%); real values 0–27; 4,110 of those rows have `previous > 0`
- 12 exact duplicates (1,784 after dropping `duration`); `default = "yes"` in 3 rows

State audit results honestly; do not fabricate problems.

---

# 6. Cleaning and preprocessing decisions

| Item | Decision |
|---|---|
| Target | `y == "yes"` → 1; any other value raises an error |
| `duration` | Dropped |
| `pdays = 999` | `pdays_recorded` 0/1 flag; `pdays` → −1 when 999 |
| `"unknown"` | Kept as its own category (informative on training rows: `default` unknown 5.3% vs 12.9% known) |
| Duplicates / rare levels | Kept |
| Split | Two-stage stratified 70/15/15, `random_state=42` → 28,831 / 6,178 / 6,179 rows |
| Encoding | `ColumnTransformer` fitted on train only; one-hot with `handle_unknown="ignore"`; 63 features for both models |
| Scaling | `StandardScaler` (train only) for the MLP; numeric passthrough for GBDT |

---

# 7. Leakage and test-set isolation

For any fit that learns from data (encoding, scaling):

1. Split first
2. Fit on training data only
3. Transform validation and test with that fit

The test set is not used for early stopping, tuning, or selection, and its labels are not inspected before Section 7 (the split summary shows test row count only). Be able to explain `fit_transform(X_train)` vs `transform(X_test)`.

---

# 8. Model experiments

**GBDT:** `XGBClassifier(tree_method="hist", n_estimators=5000, early_stopping_rounds=50, eval_metric="logloss", random_state=42, device="cpu")`; `eval_set=[train, validation]` with validation last. Phases: A `learning_rate` {0.01, 0.1, 0.3}; B `max_depth` {2, 4, 6, 8}; C `subsample` {1.0, 0.8, 0.6}. 8 configurations (G1–G8). The cap was raised from 3,000 after the depth-2 run hit it; no run reaches 5,000. Importance = total-gain share over trees `0..best_iteration`.

**MLP:** `MLPClassifier(solver="adam", activation="relu", max_iter=200, early_stopping=False, random_state=42)` on scaled inputs. Phases: A `hidden_layer_sizes` {(64,), (128, 64), (128, 64, 32)}; B `learning_rate_init` {1e-4, 1e-3, 1e-2}; C `alpha` {1e-4, 1e-2, 1e-1, 1.0}. 8 configurations (M1–M8). `ConvergenceWarning`s captured per run, not silenced. `loss_curve_` includes the L2 penalty; train/validation log loss in tables are penalty-free, so the selected-model figure plots `loss_curve_` alone as the training objective.

Each phase changes one setting and carries forward the best value; selection uses unrounded validation AP.

---

# 9. Evaluation

| Item | Rule |
|---|---|
| Selection metric | Validation AP from `predict_proba[:, 1]` with `average_precision_score` |
| Test metrics | AP; accuracy, precision, recall, F1 for the positive class at threshold 0.5 (not tuned) |
| Figures | Both PR curves with the test positive-class rate as reference; both confusion matrices |
| Timing | Selected models refitted 3× on the same Colab CPU runtime (median, min, max); every refit verified to reproduce the selected model; preprocessing timed separately |
| Environment | Versions, platform, CPU model, cores, seed recorded in the notebook |

Figures used in the PDF must be embedded in the PDF; graders will not open the notebook to find graphs.

---

# 10. Final results (Colab run in the submitted notebook)

- Selected: **G7** (lr 0.01, depth 4, subsample 0.8, 863 trees; validation AP 0.4923) and **M6** ((64,), lr 1e-4, alpha 0.01, 135 epochs; validation AP 0.4825)
- Test (6,179 rows, 696 positives, rate 0.1126), GBDT vs MLP: AP 0.4819 / 0.4771; accuracy 0.9022 / 0.9003; precision 0.6917 / 0.6460; recall 0.2385 / 0.2543; F1 0.3547 / 0.3649
- Median fit time: 9.994 s (7.278–10.046) vs 27.818 s (27.631–27.993), GBDT about 2.8× faster; preprocessing 0.141 / 0.146 s
- Runtime: Python 3.13.18, pandas 2.2.3, NumPy 2.4.6, scikit-learn 1.6.1, XGBoost 3.4.1, matplotlib 3.10.0; Linux x86_64, Intel Xeon 2.20 GHz, 2 cores, CPU only

Local macOS runs differ slightly (GBDT selects G8; spurious `matmul` warnings); report only Colab numbers.

---

# 11. Notebook writing style

Pattern for analysis sections:

1. Markdown: what and why
2. Code: implement
3. Output: real result
4. Markdown: interpret

Prefer small logical cells. Comments explain intent, assumptions, or risks — not restating obvious code.

Avoid submission-noise: "checkpoint", "current scope", "notebook goal", step-handoff notes, and grader checklists.

---

# 12. Report

PDF: **5–7 pages** including figures and references; no code in body or appendix.

Page 1: title block, Colab notebook line, page map for Steps 1–5, summary.

Structure:

1. Introduction
2. Methods
3. Results
4. Discussion (bias/variance, when to prefer each model, sensitivity to tuning and scaling, categorical/missing handling, importance as association only, limitations)
5. AI Tool Usage Disclosure
6. References

The Colab link must be at the very end, shared so any Columbia LionMail account can open it as Viewer (10-point deduction otherwise). Embed all required figures; do not shrink them to fit more experiments.

---

# 13. Rubric weights

- Data Preparation — 15%
- GBDT Implementation — 15%
- MLP Implementation — 15%
- GBDT vs. MLP Comparison — 25%
- Evaluation & Visualization — 20%
- AI Tool Usage Disclosure — 10%

---

# 14. AI disclosure

AI use is allowed and must be disclosed in the report.

Tools used on this work have included ChatGPT, Cursor, and CodeRabbit. Disclosure must accurately separate what AI did from what the student did (direction, review, Colab runs, decisions, ownership of correctness).

Do not claim AI-written code or text was independently authored by the student.

---

# 15. Change protocol

When asked to continue or edit:

1. **Inspect** the current notebook, `Assignment2.pdf`, and real Colab outputs.
2. **Explain** the change in chat.
3. **Edit** `/notebook/assign2-ms7556.ipynb` with the smallest sufficient change.
4. **Verify** with a real Colab run. Never invent outputs.
5. **Sync** the notebook text and the report to the new outputs, then confirm the assignment requirements are still met.

---

# 16. Do not

- Use `duration` or anything derived from it
- Switch or mix datasets
- Fit preprocessing on validation/test rows, or use different splits per model
- Use the test set for early stopping, tuning, or selection, or inspect test labels before final evaluation
- Put `early_stopping_rounds` / `eval_metric` only in `fit()`, or place validation before training in `eval_set`
- Compute AP from thresholded labels or trapezoidal PR area
- Hide MLP convergence warnings
- Compare timings across different hardware, or merge fit and preprocessing time
- Claim feature importance is causal
- Invent results or report numbers that differ from the notebook
- Put code in the PDF or omit the AI disclosure or Colab link
- Contradict `Assignment2.pdf`

---

# 17. Done when

**Notebook**

- Runs top-to-bottom in Colab with outputs saved
- Audit, cleaning, split, and preprocessing match `Assignment2.pdf`; no leakage
- 8 controlled configurations per model; early stopping and convergence reported
- Selection by validation AP; test used once; required metrics and figures present
- Timing, environment, and seed recorded; interpretations match outputs

**Report**

- 5–7 pages, page map for Steps 1–5, embedded figures and tables, no code
- Discussion covers the Step 4f points and limitations; references and AI disclosure included
- Numbers match the notebook; Colab link at the end with LionMail Viewer access verified

---

# 18. Tie-break

**`Assignment2.pdf` > correctness and leakage control > fair comparison > clear notebook > report readiness > repo polish.**

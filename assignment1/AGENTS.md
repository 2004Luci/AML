# Assignment 1 — Workflow Guardrails

## 0. Purpose

This folder holds **Assignment 1: From Dirty Data to Predictive Models** (COMS W4995 Applied Machine Learning).

### Deliverables

| Deliverable | Path |
|---|---|
| Runnable notebook | `/notebook/assign1-ms7556.ipynb` |
| Written report (no code) | `/report/Assignment1_Report.pdf` |
| Assignment handout | `Assignment1.pdf` |

`Assignment1.pdf` is the source of truth for requirements, models/metrics, report rules, rubric, and AI disclosure.

The notebook is the technical deliverable: all code, outputs, figures, and technical reasoning live there. The PDF is written from those results. Repository layout is secondary.

The notebook expects `train.csv` in its working directory (e.g. Colab upload). Do not depend on a local `data/` path inside the notebook.

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
7. How it satisfies `Assignment1.pdf`
8. What the student should be able to defend in review
9. What belongs in the PDF report

Do not assume prior ML background.

## B — Update the notebook

Edit `/notebook/assign1-ms7556.ipynb` (or a clearly named notebook under `/notebook/` if the user asks for a separate file).

The notebook must:

- run top-to-bottom without errors
- be reproducible (`RANDOM_STATE`, documented split)
- use clear names and short comments only where intent is non-obvious
- use Markdown for methodology, decisions, and interpretation
- show real outputs and figures (never invent results)
- avoid TODOs, placeholders, dead code, and meta/process notes aimed at graders
- comply with `Assignment1.pdf`

Student-facing teaching can stay in chat. The notebook itself should read as a finished submission, not a tutorial checklist.

---

# 2. Priorities

1. `Assignment1.pdf` compliance  
2. Correctness  
3. Clear, defensible notebook  
4. Student understanding  
5. Report readiness  
6. Repository polish  

Do not optimize for Kaggle score, unrequested models, heavy tuning, or README polish at the expense of the notebook.

---

# 3. Required pipeline

raw data → cleaning → feature engineering → model training → evaluation → interpretation → report

## Data cleaning

- Handle missing values; address inconsistent text if present
- Justify impute vs drop vs flag
- Do not invent invalid/noisy values if the audit finds none

## Feature engineering

- Appropriate transforms and categorical encoding
- Optional constructed features only when justified

## Model training

**Naive Bayes:** `BernoulliNB` or `GaussianNB` with Laplace/add-α smoothing; compare at least two α values (e.g. `1.0` and `0.01`).

**Linear Regression:** required for the binary task with threshold `0.5`. Do not replace it with Logistic Regression.

**Ridge / LASSO:** encouraged; include when used and explain their role.

**Fair comparison:** one shared train/test split for every model.

---

# 4. Evaluation

| Level | Metrics |
|---|---|
| Required | Accuracy, confusion matrix |
| Encouraged | Precision, recall, F1 |
| Bonus | ROC, AUC |

At least one clear visualization (e.g. confusion-matrix heatmap, ROC). Figures used in the PDF must be embedded in the PDF; graders will not open the notebook to find graphs.

Discuss smoothing vs no smoothing with evidence.

---

# 5. Dataset rules

Dataset: **Titanic** (`train.csv` with `Survived`).

Kaggle `train.csv` / `test.csv` are **not** the assignment split.

- Build the assignment train/test split from labeled `train.csv`
- Evaluate on the held-out labeled portion
- Use the same split for all models
- Do not evaluate on Kaggle `test.csv` (no labels)
- `gender_submission.csv` is not required

---

# 6. Known audit facts (Titanic `train.csv`)

- 891 × 12  
- Missing: Cabin 77.10%, Age 19.87%, Embarked 0.22%  
- Target: 61.62% died / 38.38% survived  
- No invalid Age/Fare/SibSp/Parch/Pclass/Survived values in the audit  

State audit results honestly; do not fabricate problems.

---

# 7. Leakage

Never use `Survived` to build features.

For any fit that learns from data (imputation, scaling, encoding categories, bin edges):

1. Split first  
2. Fit on training data only  
3. Transform train and test with that fit  

Be able to explain `fit_transform(X_train)` vs `transform(X_test)`.

---

# 8. Feature rules

Possible features: `FamilySize`, `IsAlone`, `CabinKnown`, `Title` from `Name`, justified fare transforms.

Include a feature only if it has a clear meaning, no target leakage, and can be defended in the report. Do not add Titanic “tricks” by default.

Treat `PassengerId`, raw `Name`, `Ticket`, and sparse raw `Cabin` as non-predictors unless a justified derived feature replaces them.

---

# 9. Cleaning decisions used in this assignment

| Column | Decision |
|---|---|
| `Age` | Median imputation, fit on train only |
| `Embarked` | Most-frequent imputation, fit on train only |
| `Cabin` | Do not impute IDs; use `CabinKnown` |
| Text fields | Trim / normalize case before encoding |
| Numeric validity | No fabricated corrections |
| Zero `Fare` | Left as-is; skew handled by transform |

---

# 10. Reproducibility

- `RANDOM_STATE = 42`  
- Documented test size (e.g. `TEST_SIZE = 0.20`)  
- Same split for all models  
- Stratify on `Survived` when splitting  

---

# 11. Notebook writing style

Pattern for analysis sections:

1. Markdown: what and why  
2. Code: implement  
3. Output: real result  
4. Markdown: interpret  

Prefer small logical cells. Comments explain intent, assumptions, or risks — not restating obvious code.

Avoid submission-noise: “checkpoint”, “current scope”, “notebook goal”, step-handoff notes, and grader checklists.

---

# 12. Report

PDF: **10–12 pages**, no code in body or appendix.

Page 1: Colab link; page map for Steps 1–5 and AI Disclosure.

Structure:

1. Introduction  
2. Data Cleaning  
3. Feature Engineering  
4. Model Comparison  
5. Discussion  
6. AI Tool Usage Disclosure  

Embed all figures in the PDF. All code stays in the `.ipynb`.

---

# 13. Rubric weights

- Data Cleaning & Transformation — 20%  
- Feature Engineering — 20%  
- Model Implementation — 20%  
- Evaluation & Visualization — 15%  
- Discussion & Interpretation — 15%  
- AI Tool Usage Disclosure — 10%  

Do not chase accuracy at the expense of cleaning, features, interpretation, or disclosure.

---

# 14. AI disclosure

AI use is allowed and must be disclosed in the report.

Tools used on this work have included ChatGPT, Cursor, and CodeRabbit. Disclosure must accurately separate what AI did from what the student did (direction, review, Colab runs, decisions, ownership of correctness).

Do not claim AI-written code or text was independently authored by the student.

---

# 15. Change protocol

When asked to continue or edit:

1. **Inspect** the current notebook, `Assignment1.pdf`, and real outputs.  
2. **Explain** the change in chat.  
3. **Edit** the notebook under `/notebook/` with the smallest sufficient change.  
4. **Verify** with real runs (user Colab or local). Never invent outputs.  
5. **Confirm** the change still meets the relevant assignment requirements before moving on.

---

# 16. Do not

- Rewrite the whole notebook without need  
- Delete prior analysis casually  
- Invent results or missing/noisy data  
- Switch datasets silently  
- Use Kaggle `test.csv` as the evaluation set  
- Replace Linear Regression with Logistic Regression  
- Skip the required α comparison  
- Fit preprocessing on data that includes the held-out test rows  
- Different splits per model  
- Put code in the PDF  
- Omit AI disclosure  
- Call a recommendation a hard requirement  
- Contradict `Assignment1.pdf`  

---

# 17. Done when

**Notebook**

- Runs top-to-bottom  
- Cleaning, features, models, and evaluation match `Assignment1.pdf`  
- Shared split; Linear Regression at 0.5; ≥2 Naive Bayes α values  
- Accuracy + confusion matrices; figures present  
- Smoothing discussed; limitations stated  
- No fabricated outputs; reproducible  

**Report**

- 10–12 pages, embedded figures, no code, page-1 map + Colab link, AI disclosure  

---

# 18. Tie-break

**`Assignment1.pdf` > correctness > clear notebook > student understanding > report readiness > repo polish.**

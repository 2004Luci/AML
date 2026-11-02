# Assignment 1 — AI/ML Workflow Guardrails

## 0. Purpose

This repository contains the work for **Assignment 1: From Dirty Data to Predictive Models**.

### Required notebook locations

Maintain the two notebook tracks in these exact directories:

- **Primary/submission notebooks:** `/notebook/primary/`
- **Learning/maintenance notebooks:** `/notebook/stub/`

For step `N`, use:

- `/notebook/primary/assign1-titanic_step<N>_submission.ipynb`
- `/notebook/stub/assign1-titanic_step<N>_learning.ipynb`

Do not place the step-specific notebooks elsewhere unless explicitly requested.

The authoritative assignment specification is `Assignment1.pdf`. Treat that PDF as the source of truth for:

- objective
- required workflow
- required/encouraged/bonus models and metrics
- report requirements
- visualization requirements
- grading rubric
- AI disclosure requirements
- submission requirements

The assignment's primary technical deliverable is the **runnable `.ipynb` notebook**. The eventual PDF report is built from the completed notebook's analysis and outputs. GitHub/repository organization is secondary.

---

# 1. Non-Negotiable User Workflow

For EVERY assignment step, follow this three-part workflow.

## Part A — Detailed explanation in chat

Before implementing a meaningful step, explain it thoroughly to the student.

Explain even beginner-level/trivial concepts when relevant.

For each step cover:

1. What are we doing?
2. Why are we doing it?
3. What problem does it solve?
4. What does each important line/block mean?
5. What alternatives exist?
6. Why did we choose this approach?
7. What could go wrong?
8. How does this satisfy the assignment?
9. What should the student understand for an oral/code review?
10. What information/results should eventually go into the PDF report?

Do not assume the student already understands practical ML.

---

## Part B — Submission notebook

Create/maintain a **submission-quality `.ipynb`** for each step.

Naming convention:

`/notebook/primary/assign1-titanic_step<N>_submission.ipynb`

This notebook is the PRIMARY DELIVERABLE.

Treat the notebook as if it were a production-quality data-science codebase.

The submission notebook should:

- be runnable top-to-bottom
- be reproducible
- use clear variable names
- use concise, professional comments
- avoid tutorial-style clutter
- avoid TODOs/placeholders in final sections
- contain professional Markdown explaining analytical decisions
- contain actual outputs/visualizations
- contain no fabricated results
- preserve prior working sections
- avoid unnecessary rewrites
- avoid dead code and unnecessary imports
- make important decisions explicit
- comply with `Assignment1.pdf`

"Production-style" does NOT mean removing all explanation. The notebook must still contain enough professional Markdown to explain methodology, decisions, and interpretation.

---

## Part C — Learning/maintenance notebook

Create/maintain a SECOND notebook for the student's learning and report preparation.

Naming convention:

`/notebook/stub/assign1-titanic_step<N>_learning.ipynb`

This notebook is NOT the primary submission artifact.

It should contain:

- detailed explanations
- TODOs
- learning notes
- conceptual reminders
- "why are we doing this?" notes
- questions the student should be able to answer
- report-writing prompts
- places to record observations
- reminders about assignment/rubric compliance

The learning notebook may be verbose and pedagogical.

It should use the same correct implementation as the submission notebook, but with additional educational material.

---

# 2. Notebook Hierarchy

Always prioritize:

1. **Assignment1.pdf compliance**
2. **Correctness**
3. **Final submission `.ipynb` quality**
4. **Student understanding**
5. **Report readiness**
6. Repository organization

Do NOT optimize for:

- Kaggle leaderboard score
- fancy ML techniques not requested
- unnecessary hyperparameter searches
- excessive abstraction
- a polished README at the expense of the notebook
- blindly following scaffold examples

---

# 3. Assignment Specification

The assignment objective is to build an end-to-end workflow:

raw data
→ data cleaning
→ feature engineering
→ model training
→ model evaluation
→ interpretation
→ report

The assignment requires:

## Step 1 — Data Cleaning

- handle missing values
- address noisy/inconsistent values
- justify choices such as impute vs. drop vs. flag

## Step 2 — Feature Engineering

- appropriate transformations
- categorical encoding
- optional meaningful constructed features

## Step 3 — Model Training

### Naive Bayes

Use either:

- `BernoulliNB`
- `GaussianNB`

depending on the processed feature representation.

Must use Laplace/add-alpha smoothing.

Must experiment with at least two alpha values, e.g.:

- `alpha = 1.0`
- `alpha = 0.01`

Compare results.

### Linear Regression

Train `LinearRegression`.

The assignment explicitly requires applying Linear Regression to the binary classification task using a threshold of `0.5`.

Do NOT silently replace Linear Regression with Logistic Regression.

### Regularization

Ridge and LASSO are encouraged:

- Ridge = L2 regularization
- LASSO = L1 regularization

Include them when practical and explain their role.

### Fair comparison

All models must use the SAME train/test split.

---

# 4. Model Evaluation Requirements

Required:

- Accuracy
- Confusion Matrix

Encouraged:

- Precision
- Recall
- F1-score

Bonus:

- ROC
- AUC

At least one meaningful visualization is required.

Suitable visualizations include:

- confusion-matrix heatmap
- ROC curve

Visualizations must be readable and report-ready.

The assignment explicitly says graphs must be visible in the PDF report; the grader will not open the notebook just to find them.

---

# 5. Dataset Guardrail

We selected the **Titanic Survival Dataset**.

Available Kaggle files:

- `train.csv`
- `test.csv`
- `gender_submission.csv`

## Important distinction

Kaggle's `train.csv` / `test.csv` are NOT the assignment's train/test split.

For this assignment:

- use `train.csv` as the main labeled dataset
- `train.csv` contains `Survived`
- create our OWN train/test split from `train.csv`
- evaluate on the held-out portion because its true `Survived` values are known
- use the SAME split for all models
- do NOT use Kaggle `test.csv` for model evaluation
- `gender_submission.csv` is not required

The Kaggle `test.csv` is a separate competition holdout without the target label and is therefore not appropriate for the required accuracy/confusion-matrix evaluation.

---

# 6. Current Dataset Findings

The actual Titanic `train.csv` audit found:

- 891 rows
- 12 columns
- `Survived`: 891 non-null
- `Age`: 714 non-null → 177 missing → 19.87%
- `Cabin`: 204 non-null → 687 missing → 77.10%
- `Embarked`: 889 non-null → 2 missing → 0.22%

Target:

- `Survived = 0`: 549 → 61.62%
- `Survived = 1`: 342 → 38.38%

Numeric validity audit found:

- Age below zero: 0
- Fare below zero: 0
- SibSp below zero: 0
- Parch below zero: 0
- invalid Pclass: 0
- invalid Survived: 0

Do not fabricate noisy/invalid values. If the audit finds no invalid numeric values, state that honestly.

---

# 7. Data Leakage Guardrail

Prevent data leakage.

Never use target information (`Survived`) to create features.

For preprocessing that learns parameters from data:

- split first where appropriate
- fit preprocessing on training data
- transform training data
- transform test data using the already-fitted preprocessing

Do not calculate train/test-dependent imputation/scaling statistics from the combined dataset.

Be able to explain:

`fit_transform(X_train)` vs. `transform(X_test)`.

---

# 8. Feature Engineering Guardrails

Potential Titanic features may include:

- `FamilySize`
- `IsAlone`
- `CabinKnown`
- `Title` extracted from `Name`
- justified fare-related features

Do NOT add features merely because they are common Titanic tricks.

A feature should be included only if:

1. it has a meaningful interpretation;
2. it is available without target leakage;
3. it is technically appropriate;
4. it can be explained in the report;
5. it contributes meaningfully or is justified by the assignment.

Raw identifier-like columns such as `PassengerId` should not automatically be used as predictive features.

Be deliberate about `Name`, `Ticket`, and `Cabin`.

---

# 9. Cleaning Decision Guardrails

Based on the actual audit:

### Age

19.87% missing.

Likely approach:

- retain rows
- median imputation
- fit median on training data only

Explain why median is preferable to blindly dropping approximately 20% of observations.

### Embarked

Only 2 missing values.

Likely approach:

- most-frequent-category imputation
- fit on training data only

### Cabin

77.10% missing.

Do NOT invent cabin identifiers.

Prefer representing cabin availability as a feature such as:

`CabinKnown = 1 if cabin observed else 0`

Optionally consider deck information if justified.

### Numeric validity

No invalid numeric values were found in the initial audit.

Do not create artificial cleaning operations just to satisfy the rubric.

### Categorical normalization

Normalize whitespace/case where appropriate before encoding.

---

# 10. Reproducibility

Use a fixed random seed, e.g.:

`RANDOM_STATE = 42`

Use a documented test size, e.g.:

`TEST_SIZE = 0.20`

Use the same split for all models.

Stratification by `Survived` may be used if appropriate for maintaining class proportions.

Do not independently split for different models.

---

# 11. Notebook Style

Use this structure:

Markdown:
"What are we doing and why?"

Code:
"Implement it."

Output:
"Show actual result."

Markdown:
"Interpret the result."

Do not write huge monolithic cells.

Prefer logical, testable cells.

Avoid excessive comments that merely restate obvious code.

Bad:

```python
# Read the CSV file
df = pd.read_csv("train.csv")
```

when the surrounding Markdown already explains it.

Better:

```python
df = pd.read_csv(TRAIN_PATH)
```

with a nearby Markdown explanation of why the dataset is being loaded.

Comments should explain intent, non-obvious decisions, assumptions, or risks.

---

# 12. Scaffold Rules

A scaffolded `assign1-titanic.ipynb` was provided.

Use it as the starting structure.

Do NOT blindly accept scaffold/example decisions.

Some scaffold cells may be explicitly marked as examples/stubs.

For every example:

- inspect the actual data
- decide whether the approach is appropriate
- replace it if necessary
- document the final decision

Preserve useful scaffold structure unless there is a strong reason to change it.

---

# 13. Report Guardrails

The final PDF report must be 10–12 pages.

Page 1 must include:

- Colab link
- page map showing where Steps 1–5 and AI Disclosure are covered

Required report content:

1. Introduction
   - problem definition
   - dataset description

2. Data Cleaning
   - steps
   - reasoning
   - before/after examples

3. Feature Engineering
   - transformations
   - encodings
   - constructed features

4. Model Comparison
   - training setup
   - evaluation results

5. Discussion
   - interpretation
   - strengths
   - limitations

6. AI Tool Usage Disclosure
   - tools used
   - what they contributed
   - what the student contributed

No code blocks in the PDF body or appendix.

All code belongs in the `.ipynb`.

All important graphs, confusion matrices, and figures must be directly embedded in the PDF.

Therefore, notebook visualizations should be generated cleanly enough to reuse in the report.

---

# 14. Grading Rubric Guardrail

Optimize for the actual rubric:

- Data Cleaning & Transformation — 20%
- Feature Engineering — 20%
- Model Implementation — 20%
- Evaluation & Visualization — 15%
- Discussion & Interpretation — 15%
- AI Tool Usage Disclosure — 10%

Do not spend disproportionate effort optimizing model accuracy while neglecting cleaning, feature engineering, interpretation, and disclosure.

---

# 15. AI Usage Guardrail

AI usage is allowed by the assignment.

Do not conceal it.

The final report must transparently disclose AI usage.

Likely tools used:

- ChatGPT
- Cursor

The disclosure should accurately describe contributions such as:

- starter-code generation
- code refinement
- debugging
- conceptual explanations
- notebook organization

Do not claim that AI-generated code was independently written by the student.

The student's own contribution includes:

- understanding the workflow
- reviewing code
- making/approving decisions
- running and inspecting results
- interpreting results
- writing/validating the analysis
- preparing the final submission

---

# 16. Step-by-Step Execution Protocol

When the user asks to proceed to a new step, follow this sequence.

## Phase 1 — Inspect

Inspect:

- current `.ipynb`
- `Assignment1.pdf`
- existing outputs
- current data/results
- previous step's decisions

Do not assume a previous result if it is not present.

## Phase 2 — Explain

Explain the step thoroughly in chat before making substantial changes.

Cover beginner concepts and rationale.

## Phase 3 — Submission notebook

Create/update:

`assign1-titanic_step<N>_submission.ipynb`

Keep it production-style and assignment-compliant.

## Phase 4 — Learning notebook

Create/update:

`assign1-titanic_step<N>_learning.ipynb`

Add:

- TODOs
- learning notes
- conceptual explanations
- report prompts
- questions to self-test

## Phase 5 — Run/verify

Never fabricate outputs.

If a result depends on runtime execution, say so and have the user run it in Colab.

After execution, inspect actual outputs before making data-dependent decisions.

## Phase 6 — Checkpoint

Before proceeding, confirm:

- notebook runs
- no errors
- requirements for that step are satisfied
- important outputs are captured
- report-relevant observations are recorded

---

# 17. Current Step Status

Completed:

- dataset selection: Titanic
- Kaggle files obtained
- Colab configured
- scaffolded notebook established
- Step 0 setup completed
- Step 1 data audit completed

Actual audit results:

- 891 rows × 12 columns
- Cabin: 77.10% missing
- Age: 19.87% missing
- Embarked: 0.22% missing
- target: 61.62% class 0 / 38.38% class 1
- no invalid numeric/domain values found in the audited fields

Next logical work:

**Implement the justified data-cleaning/preprocessing strategy without leakage.**

---

# 18. What Cursor Must NOT Do

Do not:

- rewrite the whole notebook unnecessarily
- delete previous analysis
- invent results
- invent missing/noisy data
- silently switch datasets
- use Kaggle `test.csv` as the assignment test set
- replace Linear Regression with Logistic Regression
- omit the required alpha comparison
- create separate train/test splits for different models
- calculate preprocessing statistics using the held-out test data
- add arbitrary ML techniques
- optimize for Kaggle leaderboard performance
- put code into the PDF
- omit required AI disclosure
- remove important assignment-required reasoning
- claim something is required if it is only a recommendation
- silently contradict `Assignment1.pdf`

---

# 19. Definition of Done

The final `.ipynb` is considered ready only when:

- it runs top-to-bottom in Colab;
- all required assignment steps are present;
- data-cleaning decisions are justified;
- feature engineering is justified;
- categorical variables are appropriately encoded;
- transformations are appropriate;
- Naive Bayes is implemented correctly;
- at least two alpha values are compared;
- Linear Regression is implemented with the required 0.5 threshold;
- Ridge/LASSO are included if used and interpreted;
- all models use the same split;
- accuracy and confusion matrices are present;
- meaningful visualizations are present;
- optional/bonus metrics are correctly implemented if included;
- smoothing results are discussed;
- model comparison is fair;
- limitations are discussed;
- AI usage disclosure is present;
- there are no fabricated outputs;
- the notebook is reproducible;
- the notebook contains the code and technical reasoning needed to support the PDF report.

The PDF is then created from the stable notebook outputs and must separately comply with the report formatting rules in `Assignment1.pdf`.

---

# 20. Final Principle

The goal is NOT merely to make the code execute.

The goal is:

**Produce a technically correct, reproducible, professionally structured, assignment-compliant `.ipynb` that the student understands and can defend, and then use that notebook to produce the required analytical report.**

When in doubt:

**Assignment1.pdf > correctness > notebook quality > student understanding > report readiness > repository polish.**

# Assignment 1: From Dirty Data to Predictive Models

Columbia AML — end-to-end supervised learning: clean messy data, engineer features, train models, evaluate, and write up results.

## Objective

Build a complete pipeline that turns a real dataset into predictive models:

- Clean and transform data with missing values, noise, and categorical variables
- Engineer features to improve performance
- Train and compare **Naive Bayes** (generative) and **Linear Regression** (discriminative, used as a binary classifier)
- Evaluate with metrics and visualizations
- Reflect on the workflow and disclose AI tool use

## Datasets (pick one)

| Dataset | Task | Link |
|--------|------|------|
| **Titanic Survival** | Predict passenger survival | [Kaggle Titanic](https://www.kaggle.com/competitions/titanic/data) (Kaggle account required) |
| **Heart Disease** | Predict presence of heart disease | [UCI Heart Disease](https://archive.ics.uci.edu/dataset/45/heart+disease) |

## Required steps

1. **Data cleaning** — handle missing values (impute / drop / flag), fix noisy or inconsistent values, and justify choices  
2. **Feature engineering** — normalize / standardize / log-scale; encode categoricals; optional new features (ratios, group stats)  
3. **Model training** (same train/test split for fair comparison)  
   - **Naive Bayes** (`BernoulliNB` or `GaussianNB`) with Laplace smoothing; try **at least two** `alpha` values (e.g. `1.0` vs `0.01`)  
   - **Linear Regression** as binary classification with threshold `0.5`; encouraged: Ridge (L2) and LASSO (L1)  
4. **Model evaluation**  
   - Required: accuracy + confusion matrix  
   - Encouraged: precision, recall, F1  
   - Bonus: ROC + AUC  
   - At least one visualization; discuss smoothing vs no smoothing  
5. **Report** (10–12 pages) — analysis only; **no code** in the PDF  

## Submission

| Deliverable | Notes |
|-------------|--------|
| Runnable Jupyter / Colab notebook (`.ipynb`) | All code lives here |
| PDF report (10–12 pages) | Analysis and insights only |

**Report page 1 must include:**

- Colab link  
- Page map for Steps 1–5 and the AI Disclosure  

**Report structure:** Introduction → Data Cleaning → Feature Engineering → Model Comparison → Discussion → AI Tool Usage Disclosure  

**Formatting rules:**

- Embed all plots/figures in the PDF (graders will not open the notebook for graphs)  
- No code in the report body or appendix  

## Suggested stack

- **Libraries:** `scikit-learn`, `pandas`, `numpy`, `matplotlib` / `seaborn`  
- **Split / metrics:** `train_test_split`, `classification_report`, `confusion_matrix` (`cross_val_score` optional)  
- **Models:** `BernoulliNB` / `GaussianNB`, `LinearRegression` (+ Ridge / LASSO)  
- **Plots:** seaborn heatmap for confusion matrix; optional `roc_curve` / `auc` for ROC  

## Grading rubric

| Category | Weight |
|----------|--------|
| Data Cleaning & Transformation | 20% |
| Feature Engineering | 20% |
| Model Implementation | 20% |
| Evaluation & Visualization | 15% |
| Discussion & Interpretation | 15% |
| AI Tool Usage Disclosure | 10% |

## AI use

AI tools are allowed and expected. You must still understand every line you submit, and the report must disclose which tools you used, what they contributed, and what you did yourself.

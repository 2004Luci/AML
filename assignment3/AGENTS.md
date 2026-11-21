# Assignment 3 — Workflow Guardrails

## 0. Purpose

This folder holds **Assignment 3: Transformer is All You Need** (COMS W4995 Applied Machine Learning).

### Deliverables

| Deliverable | Path |
|---|---|
| Consolidated Colab notebook (after all steps) | `/notebook/assign3-ms7556.ipynb` |
| Intermediate submission notebooks | `/notebook/submission/assign3_step<N>.ipynb` |
| Intermediate learning notebooks | `/notebook/learning/assign3_step<N>.ipynb` |
| Written report (5–7 pages, no code) | `/report/Assignment3_Report.pdf` |
| Report figures | `/assets/` |
| Saved tokenizer and selected checkpoint | `/artifacts/` |
| Assignment handout | `Assignment3.pdf` |

`Assignment3.pdf` is the source of truth for requirements, experiments, metrics, report rules, rubric, AI disclosure, and Colab access.

### Dual-track notebooks (same pattern as early Assignments 1 and 2)

Until Steps 1–4 are finished, maintain **two** tracks:

| Track | Path | Role |
|---|---|---|
| **Submission** | `/notebook/submission/assign3_step<N>.ipynb` | Clean, runnable, submission-ready. No grader checklists, TODOs, or process meta notes. |
| **Learning** | `/notebook/learning/assign3_step<N>.ipynb` | Same correct code as submission, plus learning notes, self-check questions, TODOs, and report prompts. |

Naming: `assign3_step0.ipynb` (setup), then `assign3_step1.ipynb` … `assign3_step4.ipynb`. Each step notebook carries forward the prior step's working cells.

When every step is done, consolidate the submission track into `/notebook/assign3-ms7556.ipynb` (executed in Colab with outputs saved), drop or archive the intermediate step notebooks in cleanup, and write the report from that consolidated run. Colab is the source of truth for every reported number.

The notebook reads `input.txt` from its working directory (Colab upload) and otherwise downloads it from Karpathy's char-rnn repository (`data/raw-url.txt`). A SHA-256 check guarantees every run uses the same text.

---

# 1. Workflow for each change

## A — Explain in chat

Before a meaningful change, explain:

1. What is being done
2. Why
3. What problem it solves
4. What important code means (tensor shapes for model code)
5. Alternatives and why this choice
6. Risks / failure modes
7. How it satisfies `Assignment3.pdf`
8. What the student should be able to defend in review
9. What belongs in the PDF report

Do not assume prior deep-learning background. The handout expects the student to answer, without notes: why targets are shifted, what prevents a token from seeing the future, and why a lower validation loss came from a fair experiment.

## B — Update both notebook tracks

For the current step `N`:

1. Edit `/notebook/submission/assign3_step<N>.ipynb` first (source of truth for correctness).
2. Mirror the same implementation into `/notebook/learning/assign3_step<N>.ipynb`, then add or refresh learning notes, self-checks, TODOs, and report prompts.

Both notebooks must:

- run top-to-bottom without errors (locally or in Colab)
- be reproducible (`SEED = 42`, fixed split; later steps save tokenizer and checkpoint)
- use clear names and short comments only where intent is non-obvious
- use Markdown for methodology, decisions, and interpretation
- show real outputs and figures (never invent results)
- comply with `Assignment3.pdf`

The **submission** notebook must stay clean: no TODOs, placeholders, dead code, or meta/process notes aimed at graders. Teaching content belongs in the **learning** notebook and in chat.

After Steps 1–4 are complete, consolidate submission into `/notebook/assign3-ms7556.ipynb` for the Colab deliverable.

## C — Re-run and re-sync

Any code change requires a fresh run. After the final Colab consolidation, update the notebook's interpretation text, the exported figures in `/assets/`, and the report so every number matches the new outputs (training times change between runs).

## D — Git workflow (same as Assignments 1 and 2)

- One branch and PR per step: `feature/step1-a3`, `feature/step2-a3`, `feature/step3-a3`, `feature/step4-a3`, then `feature/report-a3`; small fixes on `update/<topic>`
- Each step PR updates **both** `submission/` and `learning/` notebooks for that step
- Commit figures separately ("add png assets") after a Colab run
- CodeRabbit reviews each PR; triage every finding against the current code, fix only what is still valid, and commit as "review changes"
- Finish with cleanup: consolidate to `assign3-ms7556.ipynb`, then docs passes (README, AGENTS.md, notebook wording) before submission

---

# 2. Priorities

1. `Assignment3.pdf` compliance
2. Correctness: split before tokenizer, causal masking, shifted targets, correct loss and PPL
3. Fair, controlled experiment
4. Readable attention maps with evidence-based interpretation
5. Clear, defensible notebook
6. Report readiness
7. Repository polish

Neither configuration is required to win and there is no PPL threshold. Larger models or longer runs earn no credit by themselves; keep the model and training budget small.

---

# 3. Required pipeline

load and verify text → positional 80/20 split → BPE fitted on train → token windows → Transformer from basic layers → causality checks → baseline + controlled change (fixed budget) → checkpoint selection by validation CE → loss curves and PPL → attention heatmaps → comparison table → report

---

# 4. Dataset rules

Dataset: **Tiny Shakespeare** (`input.txt` from Karpathy's char-rnn repository). No account needed.

- Record the source URL and download date in the notebook and report
- Use the same text (verified by SHA-256) for every experiment
- No test set: all scores are validation results, not an unbiased final test score

---

# 5. Known data facts (`input.txt`)

- 1,115,394 characters (ASCII, 1 byte each); 40,000 lines; 65 unique characters
- SHA-256 `86c4e6aa9db7c042ec79f339dcb96d42b0075e16b8fc2e86bf0ca57e2dc565ed`
- Repository copy downloaded 2026-11-21
- 80/20 positional split at character 892,315 → 892,315 train / 223,079 validation characters; the cut falls mid-sentence
- Every validation character also appears in training text (still explain how unseen symbols would be handled)

---

# 6. Data preparation rules

| Item | Rule |
|---|---|
| Split | By position: first 80% train, final 20% validation; done on raw text **before** fitting the tokenizer or creating windows |
| Tokenizer | Subword BPE or WordPiece (Hugging Face `tokenizers` allowed), fitted on **training text only**; total vocabulary ≤ 500 including special tokens; reused unchanged for validation and every configuration |
| Unseen symbols | Explain the mechanism (for example an `[UNK]` token, or byte-level BPE where every byte is in the base alphabet) |
| Windows | `N + 1` tokens; input `z[0:N]`, target `z[1:N+1]`; built within each split, so no window crosses the boundary |
| Training windows | May overlap (random offsets) |
| Validation windows | Fixed, stride `N`, so each target position is scored once; state whether the final short window is dropped or padded with padded targets excluded; report the number of evaluated target tokens |
| Context length | Fixed for all configurations (handout example N = 50) |

---

# 7. Model rules

- PyTorch for model and training loop
- Components: token embedding, sinusoidal positional encoding added to embeddings (RoPE on queries/keys is an optional alternative), causal multi-head self-attention, residual connections, `nn.RMSNorm`, feed-forward network, vocabulary output projection
- Size: 1–2 blocks, hidden size ≤ 128, 2 or 4 heads, hidden size divisible by heads
- Attention written with tensor operations and basic layers: Q/K/V projections, scaled dot-product scores, causal mask, softmax over keys, head concatenation, output projection
- Allowed: `nn.Linear`, `nn.Embedding`, `nn.RMSNorm`
- Forbidden as the submitted attention: `nn.Transformer`, `nn.MultiheadAttention`, `F.scaled_dot_product_attention` (or any fused attention), pretrained models. A PyTorch reference may be used only to **check** an isolated attention calculation with the same weights, inputs, mask, and dropout setting
- Mask applied before softmax: query `i` attends only to keys `j <= i`
- Keep the post-softmax, pre-dropout attention probabilities accessible for heatmaps

## Causality checks (in `model.eval()`)

1. Attention weights above the diagonal are exactly zero
2. Changing future input tokens leaves earlier positions' logits unchanged

---

# 8. Training and experiment rules

- Loss: `cross_entropy` on raw logits and shifted target IDs; logits `(B, N, V)` → `(B·N, V)`, targets `(B, N)` → `(B·N)`; no softmax before the loss
- Checkpoint selected by validation cross-entropy
- Baseline plus **one** controlled change (for example learning rate or number of blocks); 2–3 configurations; no grid search
- Held fixed across configurations: split, tokenizer, context length, seed, training-step budget
- Record per configuration: optimizer, batch size, learning rate, steps, parameter count, hardware, package versions, seed, training time
- Save the tokenizer and the selected checkpoint to `/artifacts/`

---

# 9. Evaluation and visualization

| Item | Rule |
|---|---|
| Mode | `model.eval()` and `torch.no_grad()` |
| Validation loss | Total NLL ÷ number of non-padding target tokens over the fixed stride-`N` windows |
| Perplexity | `PPL = exp(validation loss)`; never average batch perplexities; compare PPL only with the same tokenizer, validation tokens, and window procedure |
| Loss curves | Training and validation cross-entropy vs training steps; state what each curve measures (for example mini-batch loss in train mode vs full validation loss in eval mode) and use them to discuss convergence/overfitting |
| Attention heatmaps | One fixed validation sequence; ≥ 2 heads or layers; axes labeled with actual token strings; query rows, key columns; layer/head and checkpoint in the title; probabilities after softmax, before dropout; fixed sequence and color scale when comparing checkpoints |
| Interpretation | 2–3 concrete patterns using the displayed tokens, including the causal boundary; attention weights describe the computation, not causal importance or understanding |
| Comparison table | Configurations, parameter counts, training time, best validation loss, PPL |
| Optional samples | Report prompt and decoding settings; they do not replace curves or attention analysis |

Figures used in the PDF must be embedded in the PDF; graders will not open the notebook to find graphs.

---

# 10. Planned defaults (confirm when implementing Step 2)

Starting point only; record the final values here once a Colab run fixes them.

- BPE via Hugging Face `tokenizers`, vocabulary 500 including special tokens
- N = 64 tokens of context
- d_model = 128, 4 heads, 2 blocks, feed-forward width 4 × d_model, small dropout
- AdamW, batch size 64, fixed step budget sized for a Colab CPU/T4 run in minutes
- Controlled change: learning rate (baseline vs one or two alternatives)

---

# 11. Notebook writing style

Pattern for analysis sections:

1. Markdown: what and why
2. Code: implement
3. Output: real result
4. Markdown: interpret

Prefer small logical cells. Comments explain intent, assumptions, shapes, or risks — not restating obvious code.

Avoid submission-noise: "checkpoint" process notes, "current scope", "notebook goal", Colab how-to blocks, step-handoff notes, and grader checklists. In Markdown, write sets and math-like text in backticks (for example `N` in `{50, 64}`) because Colab's MathJax swallows bare `{...}`.

---

# 12. Report

PDF: **5–7 pages** including figures and references; no code in body or appendix.

Page 1: title block, Colab notebook link, page map for Steps 1–4 and the AI disclosure, short summary.

Structure:

1. Introduction
2. Methods
3. Results
4. Discussion (what the attention maps revealed, effect of the controlled change on stability, roles of positional encoding and masking, runtime/memory bottlenecks, limitations)
5. AI Tool Usage Disclosure (same format as Assignments 1 and 2: tools used, what the tools contributed, self contribution)
6. References
7. Additional Resource (GitHub link and the Colab link)

The report is generated from the Colab results with a reportlab script (`report/build_report.py --colab <URL>`). The Colab link must appear **at the very end**, shared so any Columbia LionMail account can open it as Viewer (10-point deduction otherwise). Embed all required figures and tables; do not shrink them to fit more experiments.

---

# 13. Rubric weights

- Implementation & Training — 30%
- Attention Visualization & Analysis — 30%
- Experiment Design & Discussion — 20%
- Report Clarity & Presentation — 15%
- AI Tool Usage Disclosure — 5%

---

# 14. AI disclosure

AI use is allowed and must be disclosed in the report.

Tools used on this work have included ChatGPT, Cursor, and CodeRabbit. Disclosure must accurately separate what AI did from what the student did (direction, review, Colab runs, decisions, ownership of correctness).

Do not claim AI-written code or text was independently authored by the student.

---

# 15. Change protocol

When asked to continue or edit:

1. **Inspect** the current step notebooks, `Assignment3.pdf`, and real outputs.
2. **Explain** the change in chat.
3. **Edit** the submission step notebook with the smallest sufficient change, then mirror into learning.
4. **Verify** with a real run. Never invent outputs.
5. After consolidation: **Sync** `assign3-ms7556.ipynb`, `/assets/`, and the report to the Colab outputs, then confirm the assignment requirements are still met.

---

# 16. Do not

- Fit the tokenizer on validation text, or split after tokenizing or windowing
- Exceed 500 vocabulary entries (special tokens count)
- Let a window cross the train/validation boundary, or overlap validation windows
- Use `nn.Transformer`, `nn.MultiheadAttention`, fused attention, or a pretrained model as the submitted attention
- Apply the mask after softmax, or softmax before `cross_entropy`
- Average batch perplexities, or compare PPL across different tokenizers or window procedures
- Change more than one factor between configurations, or give configurations different step budgets
- Select checkpoints by anything other than validation cross-entropy
- Plot attention after dropout, or with unlabeled token axes
- Claim attention weights prove causal importance or understanding
- Invent results or report numbers that differ from the notebook
- Put code in the PDF or omit the AI disclosure or Colab link
- Contradict `Assignment3.pdf`

---

# 17. Done when

**Notebooks**

- Each step's submission and learning notebooks run top-to-bottom; learning mirrors submission correctness
- Final `assign3-ms7556.ipynb` runs in Colab with outputs saved
- Source, download date, and SHA-256 recorded; positional split before tokenizer; vocabulary ≤ 500; unseen-symbol handling explained
- Windows and validation token count reported; final short window handled and stated
- Transformer built from basic layers; both causality checks pass
- Baseline + one controlled change under a fixed budget; full run metadata recorded; tokenizer and checkpoint saved
- Loss curves, validation loss and PPL computed correctly, labeled attention heatmaps, comparison table; interpretations match outputs

**Report**

- 5–7 pages, page map for Steps 1–4 and AI disclosure, embedded figures and tables, no code
- Introduction, Methods, Results, Discussion, AI disclosure, references
- Numbers match the notebook; Colab link at the very end with LionMail Viewer access verified

---

# 18. Tie-break

**`Assignment3.pdf` > correctness and causality > fair comparison > attention analysis > clear notebook > report readiness > repo polish.**

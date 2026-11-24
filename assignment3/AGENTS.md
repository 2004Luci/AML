# Assignment 3 — Workflow Guardrails

## 0. Purpose

This folder holds **Assignment 3: Transformer is All You Need** (COMS W4995 Applied Machine Learning).

### Deliverables

| Deliverable | Path |
|---|---|
| Runnable notebook (Colab, outputs saved) | `/notebook/assign3-ms7556.ipynb` |
| Written report (5–7 pages, no code) | `/report/Assignment3_Report.pdf` |
| Report figures | `/assets/` |
| Saved tokenizer and selected checkpoint | `/artifacts/` |
| Assignment handout | `Assignment3.pdf` |

`Assignment3.pdf` is the source of truth for requirements, experiments, metrics, report rules, rubric, AI disclosure, and Colab access.

The notebook is the technical deliverable: all code, outputs, figures, and technical reasoning live there. The PDF is written from those results. Repository layout is secondary.

The notebook reads `input.txt` from its working directory (Colab upload) and otherwise downloads it from Karpathy's char-rnn repository (`data/raw-url.txt`). A SHA-256 check guarantees every run uses the same text. Colab is the source of truth for every reported number.

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

Do not assume prior deep-learning background.

## B — Update the notebook

Edit `/notebook/assign3-ms7556.ipynb`.

The notebook must:

- run top-to-bottom without errors in Colab
- be reproducible (`SEED = 42`, fixed positional split; tokenizer and checkpoint saved)
- use clear names and short comments only where intent is non-obvious
- use Markdown for methodology, decisions, and interpretation
- show real outputs and figures (never invent results)
- avoid TODOs, placeholders, dead code, and meta/process notes aimed at graders
- comply with `Assignment3.pdf`

Student-facing teaching can stay in chat. The notebook itself should read as a finished submission.

## C — Re-run and re-sync

Any code change requires a fresh Colab run. After it, update the notebook's interpretation text, `/assets/`, `/artifacts/`, and the report so every number matches the new outputs (training times change between runs).

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

# 6. Data preparation decisions

| Item | Decision |
|---|---|
| Split | By position: first 80% train, final 20% validation; done on raw text **before** fitting the tokenizer or creating windows |
| Tokenizer | Character-level BPE (Hugging Face `tokenizers`); newline isolated, Metaspace `▁` for spaces; vocabulary 500 = `[UNK]` + 65 characters + 434 merges; fitted on training text only; reused for validation and every configuration |
| Unseen symbols | Map to `[UNK]` (keeps sequence length, loses the symbol); no `[UNK]` in either split of this corpus |
| Windows | `N + 1` = 65 tokens; input `z[0:64]`, target `z[1:65]`; built within each split |
| Training windows | Random offsets (may overlap) |
| Validation windows | Stride 64; 1,655 windows → **105,920 evaluated target tokens**; final short window (42 targets) dropped |
| Context length | `N` = 64 for all configurations |

---

# 7. Model rules

- PyTorch for model and training loop
- Components: token embedding, sinusoidal positional encoding added to embeddings, causal multi-head self-attention, residual connections, `nn.RMSNorm`, feed-forward network, vocabulary output projection
- Size used here: 2 pre-norm blocks, hidden size 128, 4 heads, FFN 512 with GELU, dropout 0.1 → **524,660 parameters**
- Attention written with tensor operations and basic layers: Q/K/V projections, scaled dot-product scores, causal mask, softmax over keys, head concatenation, output projection
- Allowed: `nn.Linear`, `nn.Embedding`, `nn.RMSNorm`
- Forbidden as the submitted attention: `nn.Transformer`, `nn.MultiheadAttention`, `F.scaled_dot_product_attention` (or any fused attention), pretrained models. A PyTorch reference may be used only to **check** an isolated attention calculation with the same weights, inputs, mask, and dropout setting
- Mask applied before softmax: query `i` attends only to keys `j <= i`
- Keep the post-softmax, pre-dropout attention probabilities accessible for heatmaps

## Causality checks (in `model.eval()`)

1. Attention weights above the diagonal are exactly zero
2. Changing future input tokens leaves earlier positions' logits unchanged

Both checks pass on the untrained and the selected model.

---

# 8. Training and experiment rules

- Loss: `cross_entropy` on raw logits and shifted target IDs; logits `(B, N, V)` → `(B·N, V)`, targets `(B, N)` → `(B·N)`; no softmax before the loss
- Optimizer: AdamW, weight decay 0.01, constant learning rate, gradient-norm clipping at 1.0
- Budget: 5,000 steps; batch 64 windows × 64 tokens; validation every 100 steps (and at step 0) on all 105,920 targets
- Controlled change: **learning rate** `{3e-4, 1e-3 (baseline), 3e-3}`
- Held fixed: split, tokenizer, context length, model, seed 42, step budget, validation tokens
- Checkpoint selected by validation cross-entropy; tokenizer and selected checkpoint saved to `/artifacts/`

---

# 9. Evaluation and visualization

| Item | Rule |
|---|---|
| Mode | `model.eval()` and `torch.no_grad()` |
| Validation loss | Total NLL ÷ 105,920 scored targets over the fixed stride-`N` windows |
| Perplexity | `PPL = exp(validation loss)`; never average batch perplexities; compare PPL only with the same tokenizer, validation tokens, and window procedure |
| Loss curves | Training and validation cross-entropy vs training steps; state what each curve measures |
| Attention heatmaps | One fixed validation sequence (window 3, first 32 tokens); all 4 heads in both layers; axes labeled with actual token strings; post-softmax, pre-dropout; fixed 0–1 color scale; grey future mask |
| Head statistics | Mean previous/self/first/distance/entropy over all validation windows (query positions 16–63) |
| Comparison table | Configurations, parameter counts, training time, best validation loss, PPL |
| Optional probes | Positional encodings zeroed (no retraining); unigram baseline; runtime/memory; sample text |

Figures used in the PDF must be embedded in the PDF; graders will not open the notebook to find graphs.

---

# 10. Final results (Colab run in the submitted notebook)

- Selected: **lr 3e-3**, best validation loss **3.3632** at step 4,300 (PPL **28.88**); final gap 0.605 nats; training time 44–49 s per configuration (excludes ~3 s validation)
- Runtime: 8.28 ms per training step (~495,000 tokens/s); validation pass 0.06 s (5.9% of run time); GPU peak 185 MB during a step (86 MB already held)
- Other configs: 3e-4 → 3.4827 / 32.55 at step 4,600 (gap 0.343); 1e-3 → 3.3808 / 29.39 at step 4,300 (gap 0.510)
- Causality: future attention weight 0; earlier logits unchanged under a future edit; reference attention match within 1e-6
- Attention: layer-1 heads 1/3/4 are previous-token heads (0.40–0.54); head 2 is broader (distance 7.3); layer-2 heads look further back (5.8–6.7); first-token attention 0.00; uniform entropy 3.64
- Positional probe: unigram 5.5311 (PPL 252.42); encodings zeroed 4.5038 (90.36); full model 3.3632 (28.88) → keeps 47% of the gain over unigram
- Environment: Python 3.13.16, PyTorch 2.14.1+cu130, tokenizers 0.23.3, NumPy 2.4.6, matplotlib 3.10.0; Tesla T4 14.6 GB, Intel Xeon 2.00 GHz (2 cores)

Local macOS (MPS) runs differ slightly in timings and floating-point values; report only Colab numbers.

---

# 11. Notebook writing style

Pattern for analysis sections:

1. Markdown: what and why
2. Code: implement
3. Output: real result
4. Markdown: interpret

Prefer small logical cells. Comments explain intent, assumptions, shapes, or risks — not restating obvious code.

Avoid submission-noise: "checkpoint", "current scope", "notebook goal", step-handoff notes, and grader checklists. In Markdown, write sets and math-like text in backticks (for example `N` in `{50, 64}`) because Colab's MathJax swallows bare `{...}`.

---

# 12. Report

PDF: **5–7 pages** including figures and references; no code in body or appendix.

Page 1: title block, Colab notebook line, page map for Steps 1–4, summary.

Structure:

1. Introduction
2. Methods
3. Results
4. Discussion (what the attention maps revealed, effect of the controlled change on stability, roles of positional encoding and masking, runtime/memory bottlenecks, limitations)
5. AI Tool Usage Disclosure
6. References

The Colab link must be at the very end, shared so any Columbia LionMail account can open it as Viewer (10-point deduction otherwise). Embed all required figures and tables; do not shrink them to fit more experiments.

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

1. **Inspect** the current notebook, `Assignment3.pdf`, and real Colab outputs.
2. **Explain** the change in chat.
3. **Edit** `/notebook/assign3-ms7556.ipynb` with the smallest sufficient change.
4. **Verify** with a real Colab run. Never invent outputs.
5. **Sync** the notebook text, `/assets/`, `/artifacts/`, and the report to the new outputs, then confirm the assignment requirements are still met.

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

**Notebook**

- Runs top-to-bottom in Colab with outputs saved
- Source, download date, and SHA-256 recorded; positional split before tokenizer; vocabulary ≤ 500; unseen-symbol handling explained
- Windows and validation token count reported; final short window handled and stated
- Transformer built from basic layers; both causality checks pass
- Baseline + one controlled change under a fixed budget; full run metadata recorded; tokenizer and checkpoint saved
- Loss curves, validation loss and PPL computed correctly, labeled attention heatmaps, comparison table; interpretations match outputs

**Report**

- 5–7 pages, page map for Steps 1–4 and AI disclosure, embedded figures and tables, no code
- Discussion covers the Step 4 points and limitations; references and AI disclosure included
- Numbers match the notebook; Colab link at the end with LionMail Viewer access verified

---

# 18. Tie-break

**`Assignment3.pdf` > correctness and causality > fair comparison > attention analysis > clear notebook > report readiness > repo polish.**

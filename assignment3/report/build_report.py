"""Build report/Assignment3_Report.pdf from the Colab-verified results.

Usage (from the repo root):
    python assignment3/report/build_report.py --colab "https://colab.research.google.com/drive/<id>"
"""

import argparse
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

COLAB_PLACEHOLDER = '<font color="#C00000"><b>[COLAB LINK MISSING - rebuild with --colab URL]</b></font>'
COLAB_URL = COLAB_PLACEHOLDER  # set from --colab in main()
GITHUB_URL = "https://github.com/2004Luci/AML"
DATA_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
OUT = HERE / "Assignment3_Report.pdf"

# macOS Times New Roman / Arial if present; otherwise the metric-compatible Liberation fonts (Linux, Colab).
MAC_FONTS = Path("/System/Library/Fonts/Supplemental")
LIB_FONTS = Path("/usr/share/fonts/truetype/liberation")
FONT_FILES = {
    "Body": ("Times New Roman.ttf", "LiberationSerif-Regular.ttf"),
    "Body-Bold": ("Times New Roman Bold.ttf", "LiberationSerif-Bold.ttf"),
    "Body-Italic": ("Times New Roman Italic.ttf", "LiberationSerif-Italic.ttf"),
    "Body-BoldItalic": ("Times New Roman Bold Italic.ttf", "LiberationSerif-BoldItalic.ttf"),
    "Sans": ("Arial.ttf", "LiberationSans-Regular.ttf"),
    "Sans-Bold": ("Arial Bold.ttf", "LiberationSans-Bold.ttf"),
    "Sans-Italic": ("Arial Italic.ttf", "LiberationSans-Italic.ttf"),
    "Sans-BoldItalic": ("Arial Bold Italic.ttf", "LiberationSans-BoldItalic.ttf"),
}
for name, (mac_file, linux_file) in FONT_FILES.items():
    path = MAC_FONTS / mac_file if (MAC_FONTS / mac_file).exists() else LIB_FONTS / linux_file
    pdfmetrics.registerFont(TTFont(name, str(path)))
pdfmetrics.registerFontFamily(
    "Body", normal="Body", bold="Body-Bold", italic="Body-Italic", boldItalic="Body-BoldItalic"
)
pdfmetrics.registerFontFamily(
    "Sans", normal="Sans", bold="Sans-Bold", italic="Sans-Italic", boldItalic="Sans-BoldItalic"
)

PAGE_W, PAGE_H = letter
MARGIN = 0.7 * inch
TEXT_W = PAGE_W - 2 * MARGIN
ACCENT = colors.HexColor("#1F3B63")
GRID = colors.HexColor("#9AA5B1")
HEADER_BG = colors.HexColor("#E3E8EF")
HIGHLIGHT = colors.HexColor("#FFF4CC")

body = ParagraphStyle("body", fontName="Body", fontSize=10, leading=12.3, alignment=TA_JUSTIFY, spaceAfter=4)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=12, bulletIndent=2, spaceAfter=1.8)
sub_bullet = ParagraphStyle("sub_bullet", parent=body, leftIndent=26, bulletIndent=14, spaceAfter=1.0)
h1 = ParagraphStyle("h1", fontName="Sans-Bold", fontSize=13, leading=16, textColor=ACCENT, spaceBefore=5, spaceAfter=3, keepWithNext=1)
h2 = ParagraphStyle("h2", fontName="Sans-Bold", fontSize=10.8, leading=13.5, textColor=ACCENT, spaceBefore=4, spaceAfter=2, keepWithNext=1)
caption = ParagraphStyle("caption", fontName="Sans-Italic", fontSize=8.8, leading=11, alignment=TA_CENTER, spaceBefore=1, spaceAfter=5)
caption_keep = ParagraphStyle("caption_keep", parent=caption, keepWithNext=1)
cell = ParagraphStyle("cell", fontName="Sans", fontSize=8.6, leading=10.4)
cell_b = ParagraphStyle("cell_b", parent=cell, fontName="Sans-Bold")
title = ParagraphStyle("title", fontName="Sans-Bold", fontSize=17, leading=21, alignment=TA_CENTER, textColor=ACCENT)
subtitle = ParagraphStyle("subtitle", fontName="Sans", fontSize=11.5, leading=15, alignment=TA_CENTER)
small_c = ParagraphStyle("small_c", fontName="Body", fontSize=10.5, leading=13, alignment=TA_CENTER)


class Heading(Paragraph):
    """Paragraph that records the page it lands on, for the page map."""

    def __init__(self, text, style, key):
        super().__init__(text, style)
        self.key = key


class ReportDoc(BaseDocTemplate):
    def __init__(self, path, **kw):
        super().__init__(path, pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
                         topMargin=MARGIN, bottomMargin=MARGIN, **kw)
        frame = Frame(MARGIN, MARGIN, TEXT_W, PAGE_H - 2 * MARGIN, id="main",
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="page", frames=[frame], onPage=self._footer)])
        self.pages_of = {}

    def afterFlowable(self, flowable):
        if isinstance(flowable, Heading):
            self.pages_of.setdefault(flowable.key, self.page)

    @staticmethod
    def _footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Sans", 8.5)
        canvas.setFillColor(colors.grey)
        canvas.drawString(MARGIN, 0.45 * inch, "COMS W4995 Applied Machine Learning \u2013 Assignment 3 \u2013 Mit Sheth (ms7556)")
        canvas.drawRightString(PAGE_W - MARGIN, 0.45 * inch, f"Page {doc.page}")
        canvas.restoreState()


def P(text, style=body):
    return Paragraph(text, style)


def bullets(items):
    return [Paragraph(t, bullet, bulletText="\u2022") for t in items]


def sub_bullets(items):
    """Nested list items, matching Assignment 1's en-dash sub-bullets."""
    return [Paragraph(t, sub_bullet, bulletText="\u2013") for t in items]


def table(rows, widths, highlight_rows=(), bold_first_col=False):
    data = []
    for r, row in enumerate(rows):
        out = []
        for c, v in enumerate(row):
            style = cell_b if r == 0 or (bold_first_col and c == 0) else cell
            out.append(Paragraph(str(v), style))
        data.append(out)
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="CENTER")
    cmds = [
        ("GRID", (0, 0), (-1, -1), 0.5, GRID),
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 1.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8),
        ("LEFTPADDING", (0, 0), (-1, -1), 3.5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
    ]
    for r in highlight_rows:
        cmds.append(("BACKGROUND", (0, r), (-1, r), HIGHLIGHT))
    t.setStyle(TableStyle(cmds))
    return t


def figure(file, width_in, text, keep=True):
    path = ASSETS / file
    w, h = PILImage.open(path).size
    width = width_in * inch
    parts = [Image(str(path), width=width, height=width * h / w), P(text, caption)]
    return KeepTogether(parts) if keep else parts


def table_block(caption_text, tbl, splittable=False, lead=()):
    if splittable:
        return [P(caption_text, caption_keep), tbl, Spacer(1, 6)]
    return KeepTogether([*lead, P(caption_text, caption), tbl, Spacer(1, 6)])


def build_story(pages):
    def pg(*keys):
        nums = sorted({pages.get(k, 0) for k in keys})
        if len(nums) == 1:
            return str(nums[0])
        return f"{nums[0]}\u2013{nums[-1]}"

    s = []

    # ---------------------------------------------------------------- cover
    s += [
        P("COMS W4995 Applied Machine Learning", subtitle),
        Spacer(1, 3),
        P("Assignment 3: Transformer is All You Need", title),
        Spacer(1, 4),
        P("A tiny decoder-only Transformer for next-token prediction on Tiny Shakespeare", subtitle),
        Spacer(1, 6),
        P("<b>Author:</b> Mit Sheth | ms7556", small_c),
        P(f"<b>Colab notebook:</b> {COLAB_URL}", small_c),
        P("(the same link is repeated at the end of this report)", small_c),
        Spacer(1, 10),
    ]

    s.append(table_block(
        "Table 1. Page map: where each part of the assignment is addressed.",
        table([
            ["Assignment step", "Report section", "Pages"],
            ["Step 1 \u2013 Data preparation (positional split, BPE tokenizer, windows, validation targets)", "2.1", pg("m1")],
            ["Step 2 \u2013 Tiny Transformer, causality checks, training, baseline + controlled change", "2.2, 2.3, 3.1",
             pg("m2", "m3", "r1")],
            ["Step 3 \u2013 Loss curves, validation loss and perplexity, attention heatmaps", "3.1, 3.2", pg("r1", "r2")],
            ["Step 4 \u2013 Comparison table and discussion", "3.1, 3.3, 4", pg("r1", "r3", "d")],
            ["AI tool usage disclosure", "5", pg("ai")],
        ], [4.45 * inch, 1.25 * inch, 0.8 * inch]),
    ))

    s.append(P("Summary", h2))
    s += bullets([
        "<b>Task.</b> Train a 524,660-parameter decoder-only Transformer, written from basic PyTorch layers, to predict the "
        "next subword token of Tiny Shakespeare, and explain what it learned.",
        "<b>Setup.</b> Positional 80/20 split before tokenization; character-level BPE with 500 entries fitted on training "
        "text only; context <i>N</i> = 64; 2 pre-norm blocks, hidden size 128, 4 heads; both causality checks pass.",
        "<b>Controlled change: learning rate</b> (3e-4, 1e-3 baseline, 3e-3) under a fixed 5,000-step budget. Best "
        "validation loss 3.483 / 3.381 / 3.363 (perplexity 32.6 / 29.4 / 28.9) on the same 105,920 validation tokens; "
        "higher learning rates converge faster but overfit more (final train\u2013validation gap 0.34 / 0.51 / 0.61 nats).",
        "<b>Attention.</b> Layer 1 learned three previous-token heads and a head that links a line to the speaker "
        "name before it; layer-2 heads look further back, often within the same word. Without positional encodings the "
        "trained model keeps only 47% of its improvement over a context-free baseline.",
    ])

    # ---------------------------------------------------------- 1. intro
    s.append(Heading("1. Introduction", h1, "intro"))
    s.append(P(
        "A decoder-only Transformer [1] predicts each token from the tokens before it, using self-attention restricted by "
        "a causal mask. This report builds the smallest useful version of that model, trains it on a small literary "
        "corpus, and asks three questions: does the implementation respect causality, how does one controlled training "
        "setting (the learning rate) change learning behavior, and what do the learned attention patterns look like?"
    ))
    s.append(P(
        "<b>Dataset.</b> Tiny Shakespeare [2] (<i>input.txt</i> from Andrej Karpathy's char-rnn repository) is a 1.1 MB "
        "concatenation of Shakespeare plays: 1,115,394 characters in 40,000 lines with 65 distinct characters (52 letters, "
        "space, newline, the digit 3 and ten punctuation marks). Each speech starts with a speaker name on its own line "
        "ending in a colon. The file was downloaded on 2026-11-21 from " + DATA_URL + "; every run verifies its SHA-256 "
        "hash (86c4e6aa\u2026565ed), so all experiments use identical text. There is no test set: all scores below are "
        "validation results, not an unbiased estimate on new text."
    ))

    # ---------------------------------------------------------- 2. methods
    s.append(Heading("2. Methods", h1, "methods"))
    s.append(Heading("2.1 Data preparation (Step 1)", h2, "m1"))
    s += bullets([
        "<b>Split by position before anything is fitted.</b> The first 80% of characters (892,315) is training text and "
        "the final 20% (223,079) validation text. The cut falls mid-sentence, which is harmless because the two halves "
        "are tokenized and windowed separately. Every validation character also occurs in training text.",
        "<b>Tokenizer.</b> Character-level BPE [3] (Hugging Face <i>tokenizers</i> [4]) fitted on training text only, "
        "with exactly 500 entries: the special token [UNK], the 65 training characters and 434 learned merges. Each "
        "newline is its own token and spaces become a visible marker (_) attached to the next word, so merges never "
        "span a space or line break and decoding reproduces both splits exactly. A character absent from training text "
        "maps to [UNK], which keeps the sequence length but loses the symbol's identity; no [UNK] occurs in either "
        "split. Byte-level BPE would never need [UNK] but spends 256 of the 500 entries on raw bytes. The same "
        "tokenizer is reused for validation and every configuration.",
        "<b>Windows.</b> Training text yields 407,182 tokens (2.19 characters per token) and validation text 105,963 "
        "(2.11). A window holds <i>N</i> + 1 = 65 tokens <i>z</i>; the input is <i>z</i>[0:64] and the target "
        "<i>z</i>[1:65], i.e. each position predicts the next token. Training windows start at random offsets and may "
        "overlap. Validation windows start every 64 tokens, so consecutive windows share one boundary token and each "
        "target is scored exactly once: 1,655 windows, <b>105,920 evaluated target tokens</b>. The final short window "
        "(42 targets) is dropped, so no padding is needed. No window crosses the split.",
    ])

    s.append(Heading("2.2 Model and causality checks (Step 2)", h2, "m2"))
    s.append(P(
        "The model is written in PyTorch [5] from <i>nn.Embedding</i>, <i>nn.Linear</i> and <i>nn.RMSNorm</i> [6]; "
        "attention uses explicit tensor operations, without <i>nn.Transformer</i>, <i>nn.MultiheadAttention</i> or a "
        "fused attention function. Token embeddings (hidden size 128) are added to fixed sinusoidal positional encodings "
        "[1]. Each of the 2 pre-norm blocks [7] computes <i>x</i> + Attention(RMSNorm(<i>x</i>)) and then "
        "<i>x</i> + FFN(RMSNorm(<i>x</i>)), with a 128\u2192512\u2192128 GELU feed-forward network. Attention projects to "
        "queries, keys and values, splits them into 4 heads of size 32, computes scores <i>QK</i><sup>T</sup>/\u221a32, "
        "sets every score with key <i>j</i> &gt; query <i>i</i> to \u2212\u221e <b>before</b> the softmax over keys, "
        "concatenates the heads and applies an output projection. A final RMSNorm and a linear layer give raw logits "
        "over the 500 tokens. Dropout 0.1 is applied to embeddings, attention probabilities and residual branches; "
        "attention probabilities are stored after the softmax and before dropout for plotting. The model has "
        "<b>524,660 parameters</b> (embedding 64,000; blocks 396,032; output 64,628)."
    ))
    s.append(P(
        "Two causality checks run in evaluation mode, on the untrained and on the selected model: (1) every attention "
        "probability on a future key is exactly 0 in all layers and heads; (2) replacing tokens 32\u201363 of a "
        "validation window leaves the logits at positions 0\u201331 exactly unchanged (maximum difference 0), while later "
        "logits change (by up to 19.3 for the trained model). As an isolated correctness check, the first layer's "
        "attention output matches PyTorch's reference <i>scaled_dot_product_attention</i> with the same weights, inputs "
        "and causal mask to within 1e-6; the reference is not used in the model."
    ))

    s.append(Heading("2.3 Training and the controlled experiment (Step 2)", h2, "m3"))
    s += table_block(
        "Table 2. Training setup. Only the learning rate differs between configurations.",
        table([
            ["Setting", "Value"],
            ["Loss", "Cross-entropy on raw logits and shifted target IDs; logits (B, N, V) flattened to (B\u00b7N, V), targets to (B\u00b7N); no softmax before the loss"],
            ["Optimizer", "AdamW [8], weight decay 0.01, constant learning rate, gradient-norm clipping at 1.0"],
            ["Budget", "5,000 steps per configuration; batch 64 windows \u00d7 64 tokens (4,096 target tokens per step)"],
            ["Controlled change", "Learning rate 3e-4, <b>1e-3 (baseline)</b>, 3e-3"],
            ["Held fixed", "Split, tokenizer, context length, model, seed 42 (same initial weights and batch order), step budget, validation tokens"],
            ["Validation and selection", "Every 100 steps (and at step 0) on all 105,920 targets in eval mode under no_grad; each configuration keeps "
             "its lowest-validation-loss weights; the lowest of these is the selected checkpoint (saved with the tokenizer)"],
            ["Hardware and software", "Colab Tesla T4 GPU (14.6 GB), Intel Xeon 2.00 GHz (2 cores); Python 3.13.16, PyTorch 2.14.1+cu130, "
             "tokenizers 0.23.3, NumPy 2.4.6, matplotlib 3.10.0"],
        ], [1.5 * inch, 5.6 * inch], bold_first_col=True),
        splittable=True,
    )
    s.append(P(
        "Validation loss is the total negative log-likelihood over all scored targets divided by their number, and "
        "perplexity is PPL = exp(validation loss); batch perplexities are never averaged. Perplexity is per BPE token "
        "and is comparable only across these configurations, which share the tokenizer, validation tokens and windows."
    ))

    # ---------------------------------------------------------- 3. results
    s.append(Heading("3. Results", h1, "results"))
    s.append(Heading("3.1 Learning curves and comparison (Steps 2\u20134)", h2, "r1"))
    s.append(table_block(
        caption_text="Table 3. Configurations (524,660 parameters each, 5,000 steps, Colab T4). Training time excludes validation. "
        "Gap = final validation loss \u2212 mean training loss over the last 100 steps. Selected checkpoint highlighted.",
        tbl=table([
            ["Configuration", "Learning rate", "Training time", "Best step", "Best val loss", "PPL", "Final val loss", "Final gap"],
            ["Lower", "3e-4", "46.9 s", "4,600", "3.4827", "32.55", "3.4881", "0.343"],
            ["Baseline", "1e-3", "46.1 s", "4,300", "3.3808", "29.39", "3.3943", "0.510"],
            ["<b>Higher</b>", "3e-3", "45.8 s", "4,300", "<b>3.3632</b>", "<b>28.88</b>", "3.3798", "0.605"],
        ], [1.05 * inch, 0.9 * inch, 0.9 * inch, 0.75 * inch, 0.95 * inch, 0.6 * inch, 1.0 * inch, 0.8 * inch],
            highlight_rows=(3,)),
    ))
    s.append(figure("loss_curves.png", 6.8,
                    "Figure 1. Training cross-entropy (single mini-batches in training mode with dropout; faint) with a 100-step "
                    "moving average, and validation cross-entropy on all 105,920 targets in eval mode every 100 steps. The dashed "
                    "line marks each run's best validation step; the y-axis is cut at 4.6 (all runs start near 6.4)."))
    s.append(P(
        "Before training the loss is 6.35, close to ln 500 \u2248 6.21 for a uniform guess. All runs then fall quickly "
        "for about 500 steps and slowly afterwards. A higher learning rate descends faster: validation loss first reaches "
        "3.5 at step 4,300 with 3e-4, 1,500 with 1e-3 and 900 with 3e-3. In the first few hundred steps validation loss "
        "is below the training average, because that average still contains earlier, worse batches and training mode "
        "adds dropout; afterwards the gap widens steadily (Figure 2). Between steps 3,000 and 5,000, validation loss "
        "improves by 0.069 for 3e-4 but only 0.021 for 1e-3 and 0.002 for 3e-3, while training loss keeps falling: the "
        "extra steps mostly fit the training text, the onset of overfitting. The two faster runs reach their best "
        "validation loss at step 4,300 and end slightly higher, so the selected checkpoints are not the final weights; "
        "3e-4 has not converged within the budget."
    ))
    s.append(figure("validation_and_gap.png", 5.8,
                    "Figure 2. Left: validation cross-entropy of the three configurations. Right: validation loss minus the mean "
                    "training loss over the preceding 100 steps."))

    s.append(Heading("3.2 Attention maps (Step 3)", h2, "r2"))
    s.append(P(
        "All heatmaps use one fixed validation sequence: the first 32 tokens of validation window 3, "
        "\u201cel, if you give me love.\\n\\nISABELLA:\\nI know your virtue hath a licen\u201d. Rows are "
        "queries, columns are keys, labels are the actual tokens (_ = preceding space, \\n = newline), and values "
        "are probabilities after the softmax and before dropout on a fixed 0\u20131 color scale; grey cells are future "
        "keys removed by the mask. Rare words such as ISABELLA are split into single letters. Table 4 summarizes each "
        "head over all 1,655 validation windows (query positions 16\u201363) so that the patterns are not read from one "
        "example alone."
    ))
    s.append(table_block(
        caption_text="Table 4. Mean attention statistics per head over all validation windows (query positions 16\u201363). "
        "Previous/self/first = probability on key i\u22121, i and 0; distance = attention-weighted mean of i \u2212 j; "
        "entropy in nats (uniform attention: 3.64).",
        tbl=table([
            ["Layer, head", "Previous", "Self", "First", "Distance", "Entropy"],
            ["1, 1", "0.40", "0.10", "0.00", "3.7", "1.63"],
            ["1, 2", "0.06", "0.04", "0.00", "7.3", "2.06"],
            ["1, 3", "0.51", "0.10", "0.00", "2.3", "1.03"],
            ["1, 4", "0.54", "0.13", "0.00", "2.8", "1.27"],
            ["2, 1", "0.30", "0.08", "0.00", "5.8", "1.81"],
            ["2, 2", "0.17", "0.06", "0.00", "6.7", "2.17"],
            ["2, 3", "0.23", "0.07", "0.00", "6.2", "2.13"],
            ["2, 4", "0.29", "0.08", "0.00", "6.2", "1.95"],
        ], [1.0 * inch, 0.85 * inch, 0.7 * inch, 0.7 * inch, 0.85 * inch, 0.85 * inch]),
    ))
    s.append(figure("attention_layer1.png", 5.3,
                    "Figure 3. Layer 1, heads 1\u20134, selected checkpoint (learning rate 3e-3, step 4,300)."))
    s += bullets([
        "<b>Causal boundary.</b> Every cell above the diagonal is grey. The first query (el) can only attend to itself, "
        "so its row is a single cell with probability 1. The mask fixes this boundary; the pattern below it is learned "
        "(Figure 5).",
        "<b>Previous-token heads.</b> Layer-1 heads 1, 3 and 4 put 0.40\u20130.54 of their weight on the immediately "
        "preceding token, visible as a bright line just below the diagonal; for example each letter of I S A B E L L A "
        "attends to the letter before it. Before training the same head (layer 1, head 4) spreads attention almost "
        "evenly over the past (Figure 5).",
        "<b>Line structure.</b> Layer-1 head 2 is the broadest layer-1 head (entropy 2.06, mean distance 7.3); on this "
        "sequence, the queries of the line after the speaker name (_know, _your, _v, \u2026) attend strongly to the A: "
        "token that ends ISABELLA:. Layer-1 head 3 sends the line breaks after \u201clove.\u201d and "
        "\u201cISABELLA:\u201d back to the punctuation that ended the line.",
    ])
    s.append(figure("attention_layer2.png", 5.3,
                    "Figure 4. Layer 2, heads 1\u20134, selected checkpoint (learning rate 3e-3, step 4,300)."))
    s += bullets([
        "<b>Longer range in layer 2.</b> Layer-2 heads look further back on average (5.8\u20136.7 tokens) and often to an "
        "earlier piece of the same word: in head 2, S and A attend mostly to I, and _v, ir, t and ue attend back to "
        "_your; in heads 2 and 3, E, L and L attend to B. No head uses the first token as an attention \u201csink\u201d.",
    ])
    s.append(P(
        "These weights describe how this model routes information between positions. A bright cell does not by itself "
        "show that the key token caused the prediction, nor any human-like understanding [9]."
    ))
    s.append(figure("attention_before_after.png", 5.2,
                    "Figure 5. Layer 1, head 4 before training (step 0) and at the selected checkpoint; same sequence and color scale."))

    s.append(Heading("3.3 Positional encoding, runtime and memory (Step 4)", h2, "r3"))
    s.append(table_block(
        caption_text="Table 5. Validation loss of the selected checkpoint with and without its positional encodings (no retraining), "
        "against a context-free baseline that predicts every token from its add-one-smoothed training frequency.",
        tbl=table([
            ["Model", "Validation loss", "PPL"],
            ["Context-free (unigram) baseline", "5.5311", "252.42"],
            ["Selected checkpoint, positional encodings set to zero", "4.5038", "90.36"],
            ["Selected checkpoint (learning rate 3e-3, step 4,300)", "3.3632", "28.88"],
        ], [3.9 * inch, 1.2 * inch, 0.9 * inch]),
    ))
    s.append(P(
        "The trained model is 2.17 nats better than the context-free baseline. With its positional encodings removed it "
        "keeps only 47% of that improvement (validation loss 4.50), so it relies heavily on the explicit position "
        "signal; part of the drop also reflects inputs unlike those seen in training. On the T4, one training step on a "
        "fixed batch of 64 \u00d7 64 tokens took 8.2 ms (about 497,000 tokens per second); sampling a batch took 0.17 ms "
        "and a full validation pass 0.06 s, so validation every 100 steps added about 6% to the run time. Parameters, "
        "gradients and AdamW state take 8 MB. Among single activations, the output logits (B \u00d7 N \u00d7 V, 7.8 MB) "
        "exceed one layer's attention probabilities (B \u00d7 H \u00d7 N \u00d7 N, 4.0 MB) at N = 64; peak GPU memory "
        "allocated by the notebook during a training step was 185 MB of the T4's 14.6 GB."
    ))

    # ---------------------------------------------------------- 4. discussion
    s.append(Heading("4. Discussion", h1, "d"))
    s.append(P(
        "<b>Effect of the learning rate.</b> With everything else fixed, the learning rate decides how far the model gets "
        "in 5,000 steps. Raising it from 3e-4 to 1e-3 lowers the best validation loss by 0.102 (PPL 32.6 \u2192 29.4), "
        "but raising it again to 3e-3 gains only 0.018 (PPL 29.4 \u2192 28.9): returns diminish quickly. The faster "
        "learners also overfit more, with a final gap of 0.61 nats for 3e-3 against 0.34 for 3e-4, and their validation "
        "loss has flattened by step 3,000 while 3e-4 is still improving. Training was stable for all three: no run "
        "diverged, and validation loss rose by at most about 0.02 between evaluations. Because the budget is fixed and "
        "the learning rate constant, these results favor fast learners; neither configuration was required to win, and "
        "larger learning rates were not tried."
    ))
    s.append(P(
        "<b>What the attention maps revealed.</b> The first layer turned into mostly local machinery: three of four "
        "heads copy information from the previous token, which is what predicting the next piece of a word split into "
        "letters or short subwords needs. The remaining layer-1 head and the layer-2 heads attend further back, to the "
        "start of the current word or to structural tokens such as the colon ending a speaker name. The sample text "
        "generated from the selected checkpoint (in the notebook) reproduces exactly this structure, with speaker names "
        "in capitals followed by verse-like lines, but its phrases are ungrammatical and some words are invented: the "
        "model has learned local form, not meaning."
    ))
    s.append(P(
        "<b>What positional encoding and masking contribute.</b> The causal mask is what makes the model a valid "
        "next-token predictor: it removes every path from future tokens to earlier predictions, and both checks confirm "
        "this before and after training. Attention by itself is order-blind, so the sinusoidal encodings supply explicit "
        "absolute position; the mask adds only an implicit cue, because each position sees a different prefix [10]. The "
        "previous-token heads depend on knowing where position i \u2212 1 is, consistent with the large loss increase "
        "when the encodings are removed."
    ))
    s.append(P(
        "<b>Runtime and memory bottlenecks.</b> The experiment is cheap: each configuration trained in about 46 s on the "
        "T4, and the three runs took almost identical time because they perform identical work. The cost is the number "
        "of sequential optimizer steps; data sampling and validation are minor. Memory is far from a constraint at "
        "N = 64; attention memory grows with N\u00b2 (64 MB per layer at N = 256 for this batch), so it would become the "
        "main cost at longer contexts."
    ))
    s.append(P("<b>Limitations.</b>", body))
    s += bullets([
        "One seed per configuration: the 0.018 difference between 1e-3 and 3e-3 has not been checked against "
        "seed-to-seed variation.",
        "A fixed budget and constant learning rate favor faster learning rates; a longer budget or a schedule could "
        "change the ranking, especially for 3e-4.",
        "Validation results only, from one positional split of one small corpus; perplexity is per BPE token and not "
        "comparable with other tokenizations.",
        "Heatmaps come from one sequence, supported by statistics over all validation windows; attention weights are "
        "not explanations, and the positional-encoding probe ablates a trained model rather than training one without "
        "encodings.",
    ])

    # ---------------------------------------------------------- 5. AI disclosure (format aligned with Assignments 1 and 2)
    s.append(Heading("5. AI Tool Usage Disclosure", h1, "ai"))
    s.append(P("5.1 AI tools used", h2))
    s += bullets([
        "ChatGPT (OpenAI)",
        "Cursor",
        "CodeRabbit",
    ])
    s.append(P("5.2 What the AI tools contributed", h2))
    s += bullets([
        "Generated and refined starter and final Python code for:",
    ])
    s += sub_bullets([
        "Data loading and checksum verification, the positional split, BPE tokenizer and token windows",
        "The Transformer, causality checks, training loop, evaluation, plots, attention statistics and runtime measurements",
    ])
    s += bullets([
        "Assisted with implementing and debugging:",
    ])
    s += sub_bullets([
        "Causal masking, the reference-attention check and stride-N validation windows",
        "Controlled learning-rate comparison, checkpoint selection and timing",
    ])
    s += bullets([
        "Provided conceptual explanations of:",
    ])
    s += sub_bullets([
        "Shifted targets, causal masking, positional encodings and per-token perplexity",
        "Reading attention heatmaps and the limits of attention as explanation",
    ])
    s += bullets([
        "Assisted with debugging and consistency checks to identify potential implementation or interpretation issues.",
        "Assisted with drafting and refining portions of the report structure, tables, figure descriptions and written analysis.",
        "CodeRabbit was used for limited automated PR/code reviews to identify potential issues and inconsistencies during development.",
    ])
    s.append(P("5.3 Self contribution", h2))
    s += bullets([
        "Established the overall workflow according to the assignment requirements and reviewed each step before moving on.",
        "Defined the methodological constraints used throughout the analysis, including:",
    ])
    s += sub_bullets([
        "Splitting before fitting the tokenizer and keeping every window inside its split",
        "Changing only the learning rate under a fixed seed and step budget",
        "Following the requirements specified in the assignment",
    ])
    s += bullets([
        "Reviewed the proposed approaches and made/approved the final methodological decisions, including:",
    ])
    s += sub_bullets([
        "Character-level BPE with 500 entries, N = 64, and the model size",
        "The learning rate as the controlled change and the selected checkpoint",
    ])
    s += bullets([
        "Ran the notebook in Google Colab and inspected the resulting outputs, tables and visualizations.",
        "Verified that the implemented workflow and results were consistent with the actual data and written interpretations.",
        "Evaluated and validated the analysis, comparisons, visualizations and conclusions, and reviewed/refined the "
        "AI-assisted code and explanations throughout development.",
    ])

    # ---------------------------------------------------------- 6. references
    s.append(Heading("6. References", h1, "ref"))
    ref = ParagraphStyle("ref", parent=body, fontSize=9.6, leading=11.8, leftIndent=16, firstLineIndent=-16, spaceAfter=2,
                         alignment=0)
    for r in [
        "[1] A. Vaswani et al. Attention is all you need. <i>NeurIPS</i>, 2017.",
        "[2] A. Karpathy. char-rnn, Tiny Shakespeare data. https://github.com/karpathy/char-rnn",
        "[3] R. Sennrich, B. Haddow and A. Birch. Neural machine translation of rare words with subword units. <i>ACL</i>, 2016.",
        "[4] Hugging Face. Tokenizers library. https://github.com/huggingface/tokenizers",
        "[5] A. Paszke et al. PyTorch: An imperative style, high-performance deep learning library. <i>NeurIPS</i>, 2019.",
        "[6] B. Zhang and R. Sennrich. Root mean square layer normalization. <i>NeurIPS</i>, 2019.",
        "[7] R. Xiong et al. On layer normalization in the Transformer architecture. <i>ICML</i>, 2020.",
        "[8] I. Loshchilov and F. Hutter. Decoupled weight decay regularization. <i>ICLR</i>, 2019.",
        "[9] S. Jain and B. C. Wallace. Attention is not explanation. <i>NAACL</i>, 2019.",
        "[10] A. Haviv, O. Ram, O. Press, P. Izsak and O. Levy. Transformer language models without positional encodings "
        "still learn positional information. <i>Findings of EMNLP</i>, 2022.",
    ]:
        s.append(P(r, ref))

    # ---------------------------------------------------------- 7. additional resource (Assignment 1 format)
    s.append(Heading("7. Additional Resource", h1, "extra"))
    s.append(P(f"<b>Github Link:</b> {GITHUB_URL}", body))
    s.append(P(f"<b>Colab notebook:</b> {COLAB_URL}", body))
    return s


def main():
    global COLAB_URL
    parser = argparse.ArgumentParser()
    parser.add_argument("--colab", default="", help="Colab share link (LionMail Viewer access)")
    url = parser.parse_args().colab.strip()
    COLAB_URL = f'<link href="{url}" color="blue"><u>{url}</u></link>' if url else COLAB_PLACEHOLDER
    if not url:
        print("WARNING: no --colab link given; the PDF shows a red placeholder (-10 points if submitted).")
    pages = {}
    for _ in range(2):
        doc = ReportDoc(str(OUT), title="Assignment 3: Transformer is All You Need", author="Mit Sheth (ms7556)")
        doc.build(build_story(pages))
        pages = doc.pages_of
    print(f"Wrote {OUT} ({doc.page} pages); section pages: {pages}")


if __name__ == "__main__":
    main()

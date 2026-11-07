"""Build report/Assignment2_Report.pdf from the Colab-verified results.

Usage (from the repo root):
    python assignment2/report/build_report.py --colab "https://colab.research.google.com/drive/<id>"
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

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
OUT = HERE / "Assignment2_Report.pdf"

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
        canvas.drawString(MARGIN, 0.45 * inch, "COMS W4995 Applied Machine Learning \u2013 Assignment 2 \u2013 Mit Sheth (ms7556)")
        canvas.drawRightString(PAGE_W - MARGIN, 0.45 * inch, f"Page {doc.page}")
        canvas.restoreState()


def P(text, style=body):
    return Paragraph(text, style)


def bullets(items):
    return [Paragraph(t, bullet, bulletText="\u2022") for t in items]


def sub_bullets(items):
    """Nested list items, matching Assignment 1's en-dash sub-bullets."""
    return [Paragraph(t, sub_bullet, bulletText="\u2013") for t in items]


def table(rows, widths, highlight_rows=(), bold_first_col=False, align_right_from=None):
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
        P("Assignment 2: From Trees to Neural Networks", title),
        Spacer(1, 4),
        P("Gradient-boosted decision trees vs. a multi-layer perceptron on UCI Bank Marketing", subtitle),
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
            ["Step 1 \u2013 Data preparation (audit, cleaning, split, preprocessing)", "2.1, 2.2", pg("m1", "m2")],
            ["Step 2 \u2013 Gradient-boosted trees (XGBoost): setup, tuning, curves, importance", "2.3, 3.1", pg("m3", "r1")],
            ["Step 3 \u2013 Neural network (MLPClassifier): setup, tuning, loss curves", "2.3, 3.2", pg("m3", "r2")],
            ["Step 4 \u2013 Evaluation and comparison (test metrics, PR curves, confusion matrices, timing, discussion)", "2.4, 3.3, 4", pg("m5", "r3", "d")],
            ["Step 5 \u2013 Report: Introduction, Methods, Results, Discussion, AI disclosure, references", "1\u20136", f"1\u2013{pg('ref')}"],
        ], [4.45 * inch, 1.25 * inch, 0.8 * inch]),
    ))

    s.append(P("Summary", h2))
    s += bullets([
        "<b>Task.</b> Predict whether a client subscribes to a term deposit (<i>y</i> = yes, 11.27% of 41,188 calls) from "
        "information available <i>before</i> the call. The leaking <i>duration</i> column is removed.",
        "<b>Selected models</b> (by validation average precision, AP): XGBoost <b>G7</b> (learning rate 0.01, depth 4, "
        "subsample 0.8, 863 trees; validation AP 0.4923) and MLP <b>M6</b> (one hidden layer of 64 units, learning rate "
        "1e-4, L2 alpha 0.01, 135 epochs; validation AP 0.4825).",
        "<b>Test set</b> (6,179 rows, used once): AP 0.4819 (GBDT) vs. 0.4771 (MLP), against a no-skill baseline of 0.113. "
        "The two models are effectively tied; at the 0.5 threshold both are conservative (recall 0.24 vs. 0.25).",
        "<b>Cost and robustness.</b> GBDT fits about 2.8\u00d7 faster (10.0 s vs. 27.8 s median, same 2-core Colab CPU) and was "
        "stable across all eight configurations (validation AP 0.482\u20130.492). The MLP ranged from 0.318 to 0.483 and "
        "overfitted badly at default settings until the learning rate was reduced and L2 regularization added.",
    ])

    # ---------------------------------------------------------- 1. intro
    s.append(Heading("1. Introduction", h1, "intro"))
    s.append(P(
        "This report compares gradient-boosted decision trees (GBDT, XGBoost) and a multi-layer perceptron (MLP, "
        "scikit-learn <i>MLPClassifier</i>) on one tabular classification task. Both receive the same rows, split and "
        "features, so differences come from the model family and its tuning, not from the data pipeline."
    ))
    s.append(P(
        "<b>Dataset.</b> The UCI Bank Marketing dataset (<i>bank-additional-full.csv</i>) [1, 2] records 41,188 phone calls "
        "from a Portuguese bank's direct-marketing campaigns (May 2008 \u2013 November 2010), with 20 predictors and the "
        "binary target <i>y</i>. There are 10 numeric predictors (age, campaign, pdays, previous, duration and five "
        "macroeconomic indicators: emp.var.rate, cons.price.idx, cons.conf.idx, euribor3m, nr.employed) and 10 nominal "
        "ones (job, marital, education, default, housing, loan, contact, month, day_of_week, poutcome). The positive class "
        "is rare (4,640 calls, 11.27%), so the primary metric is average precision (AP, area under the precision\u2013recall "
        "curve), which reflects how well positives are ranked; accuracy alone would reward predicting \u201cno\u201d for "
        "everyone (88.7%)."
    ))

    # ---------------------------------------------------------- 2. methods
    s.append(Heading("2. Methods", h1, "methods"))
    s.append(Heading("2.1 Data audit and cleaning (Step 1a)", h2, "m1"))
    s.append(P(
        "The audit checked every column's type and cardinality, missing values, sentinel codes, duplicates, rare levels and "
        "the target's domain. All cleaning rules are deterministic row-wise transformations (no statistics are learned), so "
        "they are applied before the split without leaking information from validation or test rows."
    ))
    s += table_block(
        "Table 2. Data-quality findings and the decision taken for each.",
        table([
            ["Issue", "Finding", "Decision"],
            ["<i>duration</i>", "Call length in seconds; only known after the call ends.",
             "Dropped: target leakage for a pre-call prediction."],
            ["Missing values", "0 pandas nulls, but the literal category \u201cunknown\u201d appears in 6 columns: default 8,597 "
             "(20.9%), education 1,731, housing 990, loan 990, job 330, marital 80.",
             "Kept as its own category. On training rows it is informative: subscription is 5.3% when <i>default</i> is "
             "unknown vs. 12.9% when known."],
            ["<i>pdays</i> = 999", "Sentinel for \u201cno previous day count\u201d in 39,673 rows (96.3%); real values are 0\u201327. "
             "4,110 of these rows still have <i>previous</i> &gt; 0 (poutcome = failure).",
             "Added flag <i>pdays_recorded</i> (1 = a day count exists) and set the sentinel to \u22121 so it is not read as "
             "\u201c999 days\u201d; <i>previous</i> and <i>poutcome</i> are kept."],
            ["Duplicates", "12 exact duplicate rows; 1,784 after dropping <i>duration</i>.",
             "Kept: there is no client ID, so identical feature rows are plausibly different calls."],
            ["Rare levels", "<i>default</i> = yes occurs in only 3 rows.",
             "Kept; the encoder ignores categories unseen in training."],
            ["Target", "Only \u201cno\u201d/\u201cyes\u201d.", "Mapped to 0/1; any other value raises an error."],
        ], [1.0 * inch, 3.15 * inch, 2.95 * inch]),
        splittable=True,
    )

    s.append(Heading("2.2 Split and preprocessing (Steps 1b\u20131d)", h2, "m2"))
    s.append(P(
        "A two-stage stratified split (random_state = 42) produced <b>train 28,831 / validation 6,178 / test 6,179</b> rows "
        "(70/15/15), with 3,248 and 696 positives in train and validation (11.3% each); test labels stay unread until the "
        "final evaluation (Section 3.3). Preprocessing is a "
        "column transformer fitted on training rows only: a one-hot encoder (categories unseen in training are ignored) "
        "expands the 10 nominal columns to 53 indicators, and the 10 numeric columns (including <i>pdays_recorded</i>) pass through, giving "
        "<b>63 features for both models</b>. The only difference is that the MLP's numeric columns are standardized with a "
        "standard scaler fitted on training rows; trees split on value order and need no scaling. Validation and test "
        "rows are only transformed with the training-fitted preprocessors, and the test set was not scored until both final "
        "models were fixed."
    ))

    s.append(Heading("2.3 Model setup and tuning (Steps 2 and 3)", h2, "m3"))
    s += table_block(
        "Table 3. Fixed settings and controlled experiments for both model families (8 configurations each).",
        table([
            ["Aspect", "GBDT (XGBoost XGBClassifier) [3]", "MLP (scikit-learn MLPClassifier) [4]"],
            ["Input", "63 features; numeric columns unscaled", "Same 63 features; numeric columns standardized"],
            ["Fixed settings", "Histogram tree method (<i>tree_method</i> = hist); seed 42; other settings at defaults",
             "Adam [5] solver, ReLU activation, batch size 200; seed 42; other settings at defaults"],
            ["Training budget", "Up to 5,000 trees, a safety cap only: an earlier 3,000 cap was hit by the depth-2 run, "
             "so it was raised; no run reaches 5,000",
             "Up to 200 epochs (<i>max_iter</i>); a run ends earlier when training loss improves by less than 1e-4 for "
             "10 consecutive epochs"],
            ["Stopping and monitoring", "Binary log loss on training and validation sets, validation listed last; early "
             "stopping after 50 rounds without validation improvement; predictions use trees up to <i>best_iteration</i>",
             "Built-in early stopping off, so all training rows update the weights; <i>ConvergenceWarning</i>s are "
             "captured and recorded per run, not silenced"],
            ["Phase A", "Learning rate 0.01, 0.1, 0.3 (depth 4)", "Hidden layers (64), (128, 64), (128, 64, 32) "
             "(learning rate 1e-3, alpha 1e-4)"],
            ["Phase B", "Max depth 2, 4, 6, 8", "Initial learning rate 1e-4, 1e-3, 1e-2"],
            ["Phase C (regularization)", "Row subsample 1.0, 0.8, 0.6", "L2 penalty alpha 1e-4, 1e-2, 1e-1, 1.0"],
        ], [1.25 * inch, 2.9 * inch, 2.95 * inch], bold_first_col=True),
        splittable=True,
    )
    s.append(P(
        "Each phase changes one setting and carries forward the best value of the previous phase, so phases share a "
        "reference run. Within an XGBoost run, validation log loss decides when to stop adding trees; across runs, "
        "validation AP selects the configuration. For the MLP, <i>max_iter</i> is a fixed training budget, identical for "
        "every run, and the shared external validation set (not an internal holdout) is used only to compare configurations."
    ))

    s.append(Heading("2.4 Selection, evaluation and timing (Step 4)", h2, "m5"))
    s.append(P(
        "Each family's final configuration is the one with the highest validation AP (computed from predicted "
        "probabilities, unrounded). The test set is then scored once. AP is threshold-free; accuracy, precision, recall "
        "and F1 for the positive class use the default 0.5 probability threshold, which was deliberately not tuned. For "
        "timing, each selected configuration is refitted three times on the same Colab runtime (Linux x86_64, Intel Xeon 2.20 GHz, 2 CPU cores, "
        "no GPU; Python 3.13.18, pandas 2.2.3, NumPy 2.4.6, scikit-learn 1.6.1, XGBoost 3.4.1, matplotlib 3.10.0; "
        "seed 42) and the median is reported. Every refit is checked to reproduce the selected model, and preprocessing "
        "time (fit on train, then transform all splits) is measured separately."
    ))

    # ---------------------------------------------------------- 3. results
    s.append(Heading("3. Results", h1, "results"))
    s.append(Heading("3.1 GBDT results (Step 2)", h2, "r1"))
    s.append(P(
        "Table 4 lists all eight GBDT runs. <b>Learning rate</b> mainly changes speed, not the end point: 0.01 needs about 1,300 trees and 0.3 needs only 50, "
        "yet validation AP stays within 0.0024. Larger steps reach the validation minimum in fewer rounds and start "
        "overfitting sooner, so early stopping halts them earlier. <b>Depth</b> shows the bias\u2013variance trade-off "
        "directly: depth 2 has the highest validation loss and needs over 3,000 trees (underfitting), while depth 8 fits "
        "training data much better (train log loss 0.235) without improving validation, widening the gap from 0.007 to "
        "0.031. <b>Row subsampling</b> of 0.8 added slight regularization and gave the best validation AP (G7). Its training "
        "and validation curves (Figure 1) stay close together; early stopping keeps the first 863 trees (training ran to 913), "
        "at the validation minimum of 0.266."
    ))
    s.append(table_block(
        caption_text="Table 4. GBDT configurations. Trees = best_iteration + 1; gap = validation \u2212 train log loss. Selected row "
        "highlighted.",
        tbl=table([
            ["Config", "Phase", "Learning rate", "Depth", "Subsample", "Trees", "Train LL", "Valid LL", "Gap", "Valid AP"],
            ["G1", "A", "0.01", "4", "1.0", "1,293", "0.2596", "0.2665", "0.0069", "0.4906"],
            ["G2", "A", "0.10", "4", "1.0", "182", "0.2538", "0.2662", "0.0124", "0.4882"],
            ["G3", "A", "0.30", "4", "1.0", "50", "0.2550", "0.2667", "0.0117", "0.4894"],
            ["G4", "B", "0.01", "2", "1.0", "3,137", "0.2683", "0.2678", "\u22120.0005", "0.4822"],
            ["G5", "B", "0.01", "6", "1.0", "429", "0.2539", "0.2657", "0.0118", "0.4898"],
            ["G6", "B", "0.01", "8", "1.0", "412", "0.2352", "0.2665", "0.0313", "0.4828"],
            ["<b>G7</b>", "C", "0.01", "4", "0.8", "863", "0.2605", "0.2660", "0.0054", "<b>0.4923</b>"],
            ["G8", "C", "0.01", "4", "0.6", "898", "0.2596", "0.2656", "0.0060", "0.4917"],
        ], [0.55 * inch, 0.5 * inch, 1.0 * inch, 0.55 * inch, 0.85 * inch, 0.6 * inch, 0.75 * inch, 0.75 * inch,
            0.75 * inch, 0.75 * inch], highlight_rows=(7,)),
    ))
    s.append(figure("fig_gbdt_selected_logloss.png", 4.8,
                    "Figure 1. Training vs. validation log loss per boosting round for the selected GBDT (G7); the dotted "
                    "line marks the early-stopping best iteration (0-based index 862, i.e. 863 trees)."))
    fi_w = 4.45
    side = ParagraphStyle("side", parent=body, alignment=0)
    fi_text = [
        P("<b>Feature importance</b> (Figure 2) is measured as each feature's share of <b>total split gain</b> over the "
          "trees used for prediction (through <i>best_iteration</i>).", side),
        P("Macroeconomic context dominates: nr.employed alone accounts for about half of the gain, followed by euribor3m "
          "and cons.conf.idx. Among client and campaign features, the most important are pdays (recency of the last "
          "contact), age, the month, the number of calls this campaign, contact type and a previous success.", side),
        P("These scores describe association, not causation (Section 4.2).", side),
    ]
    fi_block = Table(
        [[figure("fig_gbdt_feature_importance.png", fi_w,
                 "Figure 2. Top 15 features of the selected GBDT by share of total gain.", keep=False), fi_text]],
        colWidths=[fi_w * inch + 8, TEXT_W - fi_w * inch - 8],
    )
    fi_block.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                  ("RIGHTPADDING", (0, 0), (0, 0), 8), ("RIGHTPADDING", (1, 0), (1, 0), 0)]))
    s.append(fi_block)

    s.append(table_block(
        lead=[Heading("3.2 MLP results (Step 3)", h2, "r2")],
        caption_text="Table 5. MLP configurations (\u201cConv.\u201d = finished before max_iter without a ConvergenceWarning). "
        "Selected row highlighted.",
        tbl=table([
            ["Config", "Phase", "Hidden layers", "LR", "Alpha", "Epochs", "Conv.", "Train LL", "Valid LL", "Gap", "Valid AP"],
            ["M1", "A", "(64)", "1e-3", "1e-4", "200", "No", "0.2159", "0.3065", "0.0907", "0.4099"],
            ["M2", "A", "(128, 64)", "1e-3", "1e-4", "200", "No", "0.0440", "0.9191", "0.8750", "0.3180"],
            ["M3", "A", "(128, 64, 32)", "1e-3", "1e-4", "150", "Yes", "0.0504", "1.1277", "1.0773", "0.3505"],
            ["M4", "B", "(64)", "1e-4", "1e-4", "200", "No", "0.2606", "0.2688", "0.0082", "0.4805"],
            ["M5", "B", "(64)", "1e-2", "1e-4", "200", "No", "0.1824", "0.4753", "0.2928", "0.3525"],
            ["<b>M6</b>", "C", "(64)", "1e-4", "1e-2", "135", "Yes", "0.2656", "0.2684", "0.0028", "<b>0.4825</b>"],
            ["M7", "C", "(64)", "1e-4", "1e-1", "135", "Yes", "0.2687", "0.2691", "0.0004", "0.4810"],
            ["M8", "C", "(64)", "1e-4", "1.0", "87", "Yes", "0.2780", "0.2745", "\u22120.0035", "0.4672"],
        ], [0.55 * inch, 0.5 * inch, 1.0 * inch, 0.45 * inch, 0.5 * inch, 0.62 * inch, 0.5 * inch, 0.7 * inch,
            0.7 * inch, 0.7 * inch, 0.75 * inch], highlight_rows=(6,)),
    ))
    s.append(figure("fig_mlp_selected_loss.png", 4.9,
                    "Figure 3. Training objective per epoch (loss_curve_, i.e. log loss plus L2 penalty) of the selected MLP (M6)."))
    s.append(P(
        "At the default learning rate, <b>larger networks memorize the training set</b>: the two-layer and three-layer models "
        "reach a training log loss of about 0.05 while validation loss rises above 0.9, and validation AP falls to "
        "0.32\u20130.35 (Table 5, rows M2\u2013M3). One layer of 64 units is the least overfit, so it was carried forward. Lowering the "
        "<b>learning rate</b> to 1e-4 nearly closed the gap (0.008) and raised AP to 0.48. At 1e-2 the training loss fell "
        "lowest of the three, but validation loss rose to 0.475: faster optimization only meant faster overfitting. "
        "<b>L2 regularization</b> then trades variance for bias: alpha = 0.01 (M6) gave the best validation AP and "
        "converged in 135 epochs, while alpha = 1.0 underfits slightly (validation loss below training loss, AP 0.467). "
        "The selected model's training objective (Figure 3, including the L2 penalty) falls steeply, then plateaus. "
        "Four runs used all 200 epochs and raised ConvergenceWarnings, which are recorded in Table 5. "
        "These warnings mean the optimizer had not finished, not that training failed, and the selected model did converge."
    ))

    s.append(table_block(
        lead=[Heading("3.3 Final comparison on the test set (Step 4)", h2, "r3")],
        caption_text="Table 6. Selected models on the held-out test set (6,179 rows, 696 positives, prevalence 0.1126). "
        "Threshold 0.5 for the threshold-based metrics; times are medians of three refits (range in parentheses).",
        tbl=table([
            ["Metric", "GBDT (XGBoost G7)", "MLP (M6)"],
            ["Validation AP (selection)", "0.4923", "0.4825"],
            ["<b>Test AP</b>", "<b>0.4819</b>", "<b>0.4771</b>"],
            ["Accuracy", "0.9022", "0.9003"],
            ["Precision (positive class)", "0.6917", "0.6460"],
            ["Recall (positive class)", "0.2385", "0.2543"],
            ["F1 (positive class)", "0.3547", "0.3649"],
            ["Predicted positives / true positives found", "240 / 166", "274 / 177"],
            ["Training time, median (range)", "9.994 s (7.278\u201310.046)", "27.818 s (27.631\u201327.993)"],
            ["Preprocessing time (median)", "0.141 s", "0.146 s"],
        ], [2.7 * inch, 1.9 * inch, 1.9 * inch], bold_first_col=True),
    ))
    s.append(P(
        "The two models are <b>practically tied</b> in ranking quality: test AP differs by 0.005, which is small "
        "compared with the sampling noise of a test set containing 696 positives. Both models are far above the no-skill AP "
        "of 0.113, and their PR curves nearly overlap across the whole recall range (Figure 4). At the 0.5 threshold both "
        "models are conservative, flagging only 240\u2013274 calls and finding about a quarter of subscribers (Figure 5). "
        "The MLP trades a little precision for a little recall, which gives it a marginally higher F1. Accuracy (about 0.90) "
        "is only 1.3\u20131.5 points above always predicting \u201cno\u201d (0.887), so it is not informative here. In cost, GBDT trains "
        "<b>about 2.8\u00d7 faster</b> on identical hardware, and preprocessing is negligible for both (about 0.14 s)."
    ))
    s.append(figure("fig_pr_curves.png", 4.2,
                    "Figure 4. Test-set precision\u2013recall curves with AP in the legend; dots mark the 0.5 threshold and "
                    "the dashed line is the test positive-class proportion (0.113), the no-skill reference."))
    s.append(figure("fig_confusion_matrices.png", 5.4,
                    "Figure 5. Test-set confusion matrices at threshold 0.5 (rows = true class, columns = predicted)."))

    # ---------------------------------------------------------- 4. discussion
    s.append(Heading("4. Discussion", h1, "d"))
    s.append(P("4.1 Bias and variance", h2))
    s.append(P(
        "For GBDT, early stopping limits variance automatically. Shallow trees (depth 2) show bias, with higher loss on both "
        "sets, and deep trees (depth 8) show variance, with a gap about four times larger and no validation gain. The MLP's main "
        "problem was <b>variance</b>: with nothing restraining it, extra capacity memorized the training rows (training loss "
        "0.04 vs. validation loss 0.92). A smaller step size and L2 regularization fixed this, and too much regularization "
        "(alpha 1.0) moved it back toward bias. Both selected models end with very small gaps (0.005 and 0.003), so their "
        "remaining error is mostly bias or irreducible noise. Without call duration, the pre-call features carry limited "
        "signal, and both families reach roughly the same ceiling."
    ))
    s.append(P("4.2 When to prefer each model; sensitivity to tuning and scaling", h2))
    s.append(P(
        "On medium-sized tabular data with mixed types, <b>GBDT is the better default</b>. It matched or beat the MLP, "
        "trained 2.8\u00d7 faster, needed no scaling, and its eight configurations all landed within about 0.01 AP of each other (0.482\u20130.492). "
        "That robustness means a reasonable model is obtained with little tuning. The MLP was <b>highly sensitive to "
        "hyperparameters</b> (validation AP ranged from 0.32 to 0.48) and depends on feature scaling: unscaled inputs such "
        "as nr.employed (\u2248 5,000) would dominate the gradients of binary indicators, whereas trees are invariant to "
        "monotone rescaling. An MLP becomes preferable for large or unstructured data (text, images, sequences), when "
        "learned embeddings or joint training with other neural components are needed, or when predictions must vary "
        "smoothly with the inputs."
    ))
    s.append(P(
        "<b>Categorical and missing values.</b> Here both models used identical one-hot features, and \u201cunknown\u201d was "
        "kept as an explicit category because it carries signal (for example, the lower subscription rate when "
        "<i>default</i> is unknown). In general, trees handle such data more naturally: XGBoost can route true missing "
        "values (NaN) down a learned default branch and also supports native categorical splits. An MLP needs every input "
        "to be numeric and complete, which requires explicit imputation, encoding and scaling, and sentinel values such as "
        "<i>pdays</i> = 999 must be recoded, as was done here."
    ))
    s.append(P(
        "<b>Interpretability.</b> GBDT provides built-in importance scores, but these describe <b>association, not "
        "causation</b>. The macroeconomic indicators are strongly correlated with each other and with calendar time, so the "
        "gain shared between them is partly arbitrary. The model mainly learned <i>when</i> campaigns succeeded, which "
        "does not show that employment levels cause subscriptions. The MLP has no comparable built-in measure; "
        "model-agnostic methods such as permutation importance or SHAP could be applied to either model, and would carry the "
        "same caveat."
    ))
    s.append(P("4.3 Limitations", h2))
    s += bullets([
        "<b>Single split and seed.</b> One stratified split with seed 42; differences of about 0.005 AP are within noise, so "
        "repeated or cross-validated splits would be needed to claim a winner.",
        "<b>Limited search.</b> Tuning was sequential and one factor at a time, with eight runs per model. The MLP "
        "architecture was chosen at the default learning rate and alpha, so a larger network might perform well once "
        "regularized.",
        "<b>Default threshold.</b> The 0.5 threshold gives low recall; a real campaign would choose a threshold from the "
        "precision\u2013recall curve to fit the cost of a call versus the value of a subscription.",
        "<b>Historical benchmark.</b> The data come from 2008\u20132010 campaigns. A random split mixes time periods, so it "
        "does not test performance on future campaigns. The dominance of macroeconomic features suggests that a "
        "time-ordered split would score lower.",
        "<b>Timing.</b> Times come from a shared 2-core Colab CPU and are indicative only; the ratio between the models is "
        "more reliable than the absolute seconds.",
    ])

    # ---------------------------------------------------------- 5. AI disclosure (format aligned with Assignment 1)
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
        "Data loading, cleaning, stratified splitting and leakage-safe preprocessing",
        "GBDT and MLP training, tuning, evaluation, plots and timing",
    ])
    s += bullets([
        "Assisted with implementing and debugging:",
    ])
    s += sub_bullets([
        "The leakage-safe train/validation/test split and preprocessing workflow",
        "XGBoost early stopping and MLP convergence / regularization",
        "Validation-AP selection, test metrics, PR curves, confusion matrices and timing",
    ])
    s += bullets([
        "Provided conceptual explanations of:",
    ])
    s += sub_bullets([
        "Target leakage (<i>duration</i>), sentinel values (<i>pdays</i> = 999) and average precision",
        "Bias\u2013variance under capacity/regularization, and total-gain importance as association not causation",
    ])
    s += bullets([
        "Assisted with debugging and consistency checks to identify potential implementation or interpretation issues.",
        "Assisted with drafting and refining portions of the report structure, tables, figure descriptions and written analysis.",
        "CodeRabbit was used for limited automated PR/code reviews to identify potential issues and inconsistencies during development.",
    ])
    s.append(P("5.3 Self contribution", h2))
    s += bullets([
        "Selected the UCI Bank Marketing dataset and established the overall workflow according to the assignment requirements.",
        "Defined the methodological constraints used throughout the analysis, including:",
    ])
    s += sub_bullets([
        "Avoiding data leakage and using a consistent train/validation/test split for both models",
        "Keeping the test set untouched until both configurations were fixed",
        "Following the requirements specified in the assignment",
    ])
    s += bullets([
        "Reviewed the proposed preprocessing and modeling approaches and made/approved the final methodological decisions, "
        "including:",
    ])
    s += sub_bullets([
        "Dropping <i>duration</i>, recoding <i>pdays</i> = 999, and keeping literal <i>unknown</i>",
        "MLP-only scaling and the selected configurations (G7, M6)",
    ])
    s += bullets([
        "Ran the notebook in Google Colab and inspected the resulting outputs, tables and visualizations.",
        "Verified that the implemented workflow and results were consistent with the actual dataset and written interpretations.",
        "Evaluated and validated the analysis, model comparisons, visualizations and conclusions, and reviewed/refined the "
        "AI-assisted code and explanations throughout development.",
    ])

    # ---------------------------------------------------------- 6. references
    s.append(Heading("6. References", h1, "ref"))
    ref = ParagraphStyle("ref", parent=body, fontSize=9.6, leading=11.8, leftIndent=16, firstLineIndent=-16, spaceAfter=2,
                         alignment=0)
    for r in [
        "[1] S. Moro, P. Cortez and P. Rita. A data-driven approach to predict the success of bank telemarketing. "
        "<i>Decision Support Systems</i>, 62:22\u201331, 2014.",
        "[2] UCI Machine Learning Repository: Bank Marketing. https://archive.ics.uci.edu/dataset/222/bank+marketing",
        "[3] T. Chen and C. Guestrin. XGBoost: A scalable tree boosting system. <i>KDD</i>, 2016; documentation at "
        "https://xgboost.readthedocs.io",
        "[4] F. Pedregosa et al. Scikit-learn: Machine learning in Python. <i>JMLR</i> 12:2825\u20132830, 2011; "
        "MLPClassifier and average_precision_score documentation at https://scikit-learn.org",
        "[5] D. P. Kingma and J. Ba. Adam: A method for stochastic optimization. <i>ICLR</i>, 2015.",
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
        doc = ReportDoc(str(OUT), title="Assignment 2: From Trees to Neural Networks", author="Mit Sheth (ms7556)")
        doc.build(build_story(pages))
        pages = doc.pages_of
    print(f"Wrote {OUT} ({doc.page} pages); section pages: {pages}")


if __name__ == "__main__":
    main()

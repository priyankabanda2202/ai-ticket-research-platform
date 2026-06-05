import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from datetime import datetime

# ── Colour palette ──────────────────────────────────────────
DARK_BG     = colors.HexColor("#0d1420")
ACCENT      = colors.HexColor("#38bdf8")
ACCENT2     = colors.HexColor("#818cf8")
ACCENT3     = colors.HexColor("#34d399")
WHITE       = colors.white
LIGHT_GRAY  = colors.HexColor("#e2e8f0")
MID_GRAY    = colors.HexColor("#94a3b8")
SURFACE     = colors.HexColor("#121a2a")
DANGER      = colors.HexColor("#f87171")
WARNING     = colors.HexColor("#fbbf24")

W, H = A4   # 595 x 842 pts

def rec_color(rec):
    r = (rec or "").upper()
    if r == "BUY":  return colors.HexColor("#34d399")
    if r == "SELL": return colors.HexColor("#f87171")
    return colors.HexColor("#fbbf24")

def draw_rounded_rect(c, x, y, w, h, r=6, fill_color=None, stroke_color=None):
    p = c.beginPath()
    p.moveTo(x + r, y)
    p.lineTo(x + w - r, y)
    p.arcTo(x + w - 2*r, y, x + w, y + 2*r, startAng=-90, extent=90)
    p.lineTo(x + w, y + h - r)
    p.arcTo(x + w - 2*r, y + h - 2*r, x + w, y + h, startAng=0, extent=90)
    p.lineTo(x + r, y + h)
    p.arcTo(x, y + h - 2*r, x + 2*r, y + h, startAng=90, extent=90)
    p.lineTo(x, y + r)
    p.arcTo(x, y, x + 2*r, y + 2*r, startAng=180, extent=90)
    p.close()
    if fill_color:
        c.setFillColor(fill_color)
    if stroke_color:
        c.setStrokeColor(stroke_color)
        c.setLineWidth(0.5)
    c.drawPath(p, fill=1 if fill_color else 0, stroke=1 if stroke_color else 0)

def draw_progress_bar(c, x, y, width, height, pct, bg_color, fill_color):
    # Background track
    draw_rounded_rect(c, x, y, width, height, r=3, fill_color=bg_color)
    # Fill
    fill_w = max(width * min(pct, 1.0), height)  # min = pill width
    draw_rounded_rect(c, x, y, fill_w, height, r=3, fill_color=fill_color)

def report_agent(state):
    ticker   = state["ticker"]
    decision = state["decision"]
    market   = state.get("market", {})
    sentiment= state.get("sentiment", {})

    os.makedirs("reports", exist_ok=True)
    file_path = f"reports/{ticker}_report.pdf"

    c = canvas.Canvas(file_path, pagesize=A4)

    # ── HEADER BANNER ───────────────────────────────────────
    c.setFillColor(DARK_BG)
    c.rect(0, H - 110, W, 110, fill=1, stroke=0)

    # Accent top line
    c.setFillColor(ACCENT)
    c.rect(0, H - 3, W, 3, fill=1, stroke=0)

    # Logo / title
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(30, H - 50, ticker)

    c.setFillColor(WHITE)
    c.setFont("Helvetica", 11)
    c.drawString(30, H - 70, "Market Analysis Report")

    c.setFillColor(MID_GRAY)
    c.setFont("Helvetica", 9)
    c.drawString(30, H - 88, f"Generated: {datetime.now().strftime('%B %d, %Y  %H:%M UTC')}")

    # Recommendation badge (top-right)
    rec   = (decision.get("recommendation") or "HOLD").upper()
    rc    = rec_color(rec)
    badge_x = W - 110
    draw_rounded_rect(c, badge_x, H - 72, 80, 28, r=14,
                      fill_color=colors.HexColor("#0d1420"),
                      stroke_color=rc)
    c.setFillColor(rc)
    c.setFont("Helvetica-Bold", 13)
    c.drawCentredString(badge_x + 40, H - 53, rec)

    # ── METRICS ROW ─────────────────────────────────────────
    y_metrics = H - 200
    metric_data = [
        ("Current Price",   f"${market.get('price', 0):.2f}",       "USD"),
        ("P/E Ratio",       f"{market.get('pe_ratio', 0):.2f}",      "Price to Earnings"),
        ("Volatility",      str(market.get('volatility','-')).title(),"Risk Level"),
        ("RSI",             f"{market.get('rsi', 0):.1f}",           "Momentum"),
    ]
    box_w = (W - 60) / 4
    for i, (label, value, sub) in enumerate(metric_data):
        bx = 30 + i * box_w
        draw_rounded_rect(c, bx + 2, y_metrics, box_w - 4, 70, r=6,
                          fill_color=SURFACE,
                          stroke_color=colors.HexColor("#1e2d45"))
        c.setFillColor(MID_GRAY)
        c.setFont("Helvetica", 8)
        c.drawString(bx + 12, y_metrics + 54, label.upper())

        c.setFillColor(LIGHT_GRAY)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(bx + 12, y_metrics + 34, value)

        c.setFillColor(MID_GRAY)
        c.setFont("Helvetica", 8)
        c.drawString(bx + 12, y_metrics + 18, sub)

    # ── DIVIDER ─────────────────────────────────────────────
    y_div = y_metrics - 20
    c.setStrokeColor(colors.HexColor("#1e2d45"))
    c.setLineWidth(0.5)
    c.line(30, y_div, W - 30, y_div)

    # ── SENTIMENT SECTION ───────────────────────────────────
    y_sent = y_div - 90
    draw_rounded_rect(c, 30, y_sent, (W - 70) / 2, 80, r=6,
                      fill_color=SURFACE,
                      stroke_color=colors.HexColor("#1e2d45"))

    c.setFillColor(MID_GRAY)
    c.setFont("Helvetica", 8)
    c.drawString(42, y_sent + 64, "SENTIMENT ANALYSIS")

    sent_label = str(sentiment.get("sentiment", "neutral")).title()
    sent_score = sentiment.get("score", 0)
    sent_color = ACCENT3 if sent_label.lower() == "positive" else (DANGER if sent_label.lower() == "negative" else WARNING)

    c.setFillColor(sent_color)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(42, y_sent + 46, sent_label)

    c.setFillColor(MID_GRAY)
    c.setFont("Helvetica", 9)
    score_str = f"{int(sent_score * 100)} / 100"
    c.drawRightString(30 + (W - 70) / 2 - 12, y_sent + 49, score_str)

    # Sentiment bar
    bar_x = 42
    bar_y = y_sent + 32
    bar_w = (W - 70) / 2 - 24
    draw_progress_bar(c, bar_x, bar_y, bar_w, 7, sent_score,
                      bg_color=colors.HexColor("#1e2d45"),
                      fill_color=sent_color)

    # Drivers chips
    drivers = sentiment.get("drivers", [])
    chip_x = 42
    chip_y = y_sent + 12
    for d in drivers:
        label_w = len(d) * 5.5 + 14
        draw_rounded_rect(c, chip_x, chip_y, label_w, 14, r=7,
                          fill_color=colors.HexColor("#1e2d45"),
                          stroke_color=colors.HexColor("#334155"))
        c.setFillColor(MID_GRAY)
        c.setFont("Helvetica", 7.5)
        c.drawString(chip_x + 7, chip_y + 3.5, d.title())
        chip_x += label_w + 6

    # ── DECISION SECTION ────────────────────────────────────
    dec_x = 30 + (W - 70) / 2 + 10
    dec_w = (W - 70) / 2
    draw_rounded_rect(c, dec_x, y_sent, dec_w, 80, r=6,
                      fill_color=SURFACE,
                      stroke_color=colors.HexColor("#1e2d45"))

    c.setFillColor(MID_GRAY)
    c.setFont("Helvetica", 8)
    c.drawString(dec_x + 12, y_sent + 64, "DECISION & CONFIDENCE")

    conf = decision.get("confidence", 0)
    c.setFillColor(MID_GRAY)
    c.setFont("Helvetica", 9)
    c.drawString(dec_x + 12, y_sent + 49, f"Confidence — {int(conf * 100)}%")

    # Confidence bar
    draw_progress_bar(c, dec_x + 12, y_sent + 36, dec_w - 24, 7, conf,
                      bg_color=colors.HexColor("#1e2d45"),
                      fill_color=ACCENT)

    # RSI gauge bar
    rsi_val = market.get("rsi", 50)
    c.setFillColor(MID_GRAY)
    c.setFont("Helvetica", 7.5)
    c.drawString(dec_x + 12, y_sent + 24, "RSI Gauge")
    rsi_bar_y = y_sent + 13
    # Gradient-like: draw red → yellow → green in 3 segments
    seg_w = (dec_w - 24) / 3
    for seg, col in enumerate([DANGER, WARNING, ACCENT3]):
        draw_rounded_rect(c, dec_x + 12 + seg * seg_w, rsi_bar_y,
                          seg_w - 1, 6, r=3, fill_color=col)
    # RSI dot
    rsi_pct = min(max(rsi_val, 0), 100) / 100
    dot_x = dec_x + 12 + rsi_pct * (dec_w - 24)
    c.setFillColor(WHITE)
    c.circle(dot_x, rsi_bar_y + 3, 4.5, fill=1, stroke=0)
    c.setFillColor(DARK_BG)
    c.circle(dot_x, rsi_bar_y + 3, 2.5, fill=1, stroke=0)

    # ── RATIONALE BOX ───────────────────────────────────────
    y_rat = y_sent - 90
    draw_rounded_rect(c, 30, y_rat, W - 60, 70, r=6,
                      fill_color=SURFACE,
                      stroke_color=colors.HexColor("#1e2d45"))

    # Left accent bar
    c.setFillColor(ACCENT2)
    c.rect(30, y_rat, 3, 70, fill=1, stroke=0)

    c.setFillColor(MID_GRAY)
    c.setFont("Helvetica", 8)
    c.drawString(44, y_rat + 54, "RATIONALE")

    c.setFillColor(LIGHT_GRAY)
    c.setFont("Helvetica", 10)
    rationale = decision.get("rationale", "")
    # Wrap long rationale text
    words = rationale.split()
    lines, line = [], []
    for word in words:
        test = " ".join(line + [word])
        if c.stringWidth(test, "Helvetica", 10) < W - 100:
            line.append(word)
        else:
            lines.append(" ".join(line))
            line = [word]
    if line:
        lines.append(" ".join(line))
    for li, text in enumerate(lines[:3]):
        c.drawString(44, y_rat + 36 - li * 14, text)

    # ── KEY METRICS TABLE ───────────────────────────────────
    y_table = y_rat - 30
    c.setFillColor(MID_GRAY)
    c.setFont("Helvetica", 8)
    c.drawString(30, y_table, "SUMMARY TABLE")

    y_table -= 8
    table_data = [
        ["Metric", "Value"],
        ["Ticker",          ticker],
        ["Recommendation",  rec],
        ["Confidence",      f"{int(conf * 100)}%"],
        ["Sentiment",       sent_label],
        ["Sentiment Score", f"{int(sent_score * 100)} / 100"],
        ["Price",           f"${market.get('price', 0):.2f}"],
        ["P/E Ratio",       f"{market.get('pe_ratio', 0):.2f}"],
        ["RSI",             f"{market.get('rsi', 0):.1f}"],
        ["Volatility",      str(market.get('volatility', '-')).title()],
    ]

    col_w = [(W - 60) * 0.45, (W - 60) * 0.55]
    tbl = Table(table_data, colWidths=col_w)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, 0),  SURFACE),
        ("TEXTCOLOR",   (0, 0), (-1, 0),  colors.HexColor("#94a3b8")),
        ("FONTNAME",    (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0),  8),
        ("BACKGROUND",  (0, 1), (-1, -1), colors.HexColor("#0d1420")),
        ("TEXTCOLOR",   (0, 1), (-1, -1), colors.HexColor("#e2e8f0")),
        ("FONTNAME",    (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",    (0, 1), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
            [colors.HexColor("#0d1420"), colors.HexColor("#121a2a")]),
        ("GRID",        (0, 0), (-1, -1), 0.3, colors.HexColor("#1e2d45")),
        ("TOPPADDING",  (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    tbl.wrapOn(c, W - 60, 300)
    tbl.drawOn(c, 30, y_table - tbl._height)

    # ── FOOTER ──────────────────────────────────────────────
    c.setFillColor(DARK_BG)
    c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.rect(0, 36, W, 0.5, fill=1, stroke=0)
    c.setFillColor(MID_GRAY)
    c.setFont("Helvetica", 8)
    c.drawString(30, 13, "Ticker Research Platform  ·  AI-powered analysis  ·  Not financial advice")
    c.drawRightString(W - 30, 13, f"Page 1 of 1  ·  {ticker}")

    c.save()
    return {"report_path": file_path}
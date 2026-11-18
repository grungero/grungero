"""Full-wrap KDP paperback cover for the 2027 Planner.

Usage: python3 kdp_cover.py <out.pdf> <page_count> [--theme sage]
Spec (KDP): white paper spine = pages x 0.002252 in; 0.125 in bleed on all outer edges;
height = trim + 0.25 in; keep text 0.125 in inside the trim (we use 0.375 in); barcode area
on back cover, bottom-right, kept clear.
"""
import sys

from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

FD = "/usr/share/fonts/truetype/crosextra/"
for n, f in (("Body", "Carlito-Regular"), ("BodyB", "Carlito-Bold"), ("Head", "Caladea-Regular"),
             ("HeadB", "Caladea-Bold"), ("HeadI", "Caladea-Italic")):
    pdfmetrics.registerFont(TTFont(n, FD + f + ".ttf"))

THEMES = {
    "sage": dict(bg="#E6EEE8", accent="#7D9A86", ink="#2F3A33"),
    "blush": dict(bg="#F5E7E5", accent="#C48B8B", ink="#3B2E2E"),
}
BOOKS = {
    "planner": dict(
        sub="Weekly & Monthly Planner", tag="GOALS  ·  BUDGET  ·  HABIT TRACKER  ·  WEEKLY PAGES",
        foot="8.5 x 11 in  ·  Dec 28, 2026 – Jan 2, 2028  ·  Monday start", spine="2027 PLANNER",
        head="Plan your best year yet.",
        blurb=["A clean, minimalist planner with everything you need",
               "to set goals, manage your money and build better habits."],
        items=["2027 year at a glance and yearly goals", "Yearly finance tracker",
               "12 monthly calendars (Monday start)", "12 monthly plan & budget pages",
               "12 habit trackers with mood & wins", "53 weekly planning pages", "Dot-grid notes pages"]),
    "budget": dict(
        sub="Budget Planner", tag="MONTHLY BUDGET  ·  EXPENSE TRACKER  ·  BILLS  ·  SAVINGS  ·  DEBT",
        foot="8.5 x 11 in  ·  100 pages  ·  January – December 2027", spine="2027 BUDGET PLANNER",
        head="Take control of your money.",
        blurb=["A simple, practical budget book to plan every month,",
               "track every expense and finally reach your money goals."],
        items=["Financial snapshot & money goals", "Yearly overview and bill tracker",
               "12 monthly budget pages", "48 expense tracker pages (4 per month)",
               "12 monthly reviews with no-spend challenge", "4 savings goal charts & sinking funds",
               "Debt payoff trackers and notes"]),
}
IN = 72
TRIM_W, TRIM_H, BLEED = 8.5 * IN, 11 * IN, 0.125 * IN


def build(out, pages, theme="sage", book="planner"):
    b = BOOKS[book]
    t = THEMES[theme]
    bg, acc, ink = HexColor(t["bg"]), HexColor(t["accent"]), HexColor(t["ink"])
    spine = pages * 0.002252 * IN
    W = 2 * BLEED + 2 * TRIM_W + spine
    H = 2 * BLEED + TRIM_H
    c = canvas.Canvas(out, pagesize=(W, H), initialFontName="Body")
    c.setTitle("2027 Planner cover")
    c.setFillColor(bg)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    back_x0 = BLEED
    spine_x0 = BLEED + TRIM_W
    front_x0 = spine_x0 + spine
    safe = 0.375 * IN

    # ---- front cover ----
    fx = front_x0 + TRIM_W / 2
    mid = BLEED + TRIM_H / 2
    c.setFillColor(acc)
    c.rect(front_x0, mid - 2, TRIM_W + BLEED, 4, stroke=0, fill=1)
    c.setFillColor(ink)
    c.setFont("Head", 120)
    c.drawCentredString(fx, mid + 40, "2027")
    c.setFont("HeadI", 30)
    c.drawCentredString(fx, mid - 55, b["sub"])
    c.setFont("Body", 13)
    c.setFillColor(acc)
    c.drawCentredString(fx, mid - 85, b["tag"])
    c.setFillColor(ink)
    c.setFont("Body", 12)
    c.drawCentredString(fx, BLEED + safe + 30, b["foot"])

    # ---- spine ----
    if pages >= 80:
        c.saveState()
        c.translate(spine_x0 + spine / 2, mid)
        c.rotate(-90)
        c.setFillColor(ink)
        size = min(8, spine - 0.125 * IN)  # 0.0625 in clearance each side
        c.setFont("BodyB", size)
        c.drawCentredString(0, -size / 3, b["spine"])
        c.restoreState()

    # ---- back cover ----
    bx = back_x0 + safe + 0.25 * IN
    y = BLEED + TRIM_H - safe - 60
    c.setFillColor(ink)
    c.setFont("HeadB", 24)
    c.drawString(bx, y, b["head"])
    y -= 36
    c.setFont("Body", 13)
    for line in b["blurb"]:
        c.drawString(bx, y, line)
        y -= 19
    y -= 16
    c.setFont("BodyB", 13)
    c.setFillColor(acc)
    c.drawString(bx, y, "INSIDE YOU'LL FIND")
    y -= 24
    c.setFillColor(ink)
    c.setFont("Body", 13)
    for item in b["items"]:
        c.setFillColor(acc)
        c.circle(bx + 4, y + 4, 3, stroke=0, fill=1)
        c.setFillColor(ink)
        c.drawString(bx + 16, y, item)
        y -= 22
    # barcode area (bottom-right of back cover, ~2 x 1.2 in) is left empty: KDP prints its barcode there
    c.showPage()
    c.save()
    return W / IN, H / IN, spine / IN


if __name__ == "__main__":
    out, pages = sys.argv[1], int(sys.argv[2])
    theme = sys.argv[sys.argv.index("--theme") + 1] if "--theme" in sys.argv else "sage"
    book = sys.argv[sys.argv.index("--book") + 1] if "--book" in sys.argv else "planner"
    w, h, s = build(out, pages, theme, book)
    print(f"{out}: {w:.4f} x {h:.4f} in, spine {s:.4f} in")

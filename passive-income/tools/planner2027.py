"""Generate a hyperlinked 2027 planner PDF (printable + digital for GoodNotes/Notability).

Usage: python3 planner2027.py <out.pdf> [--theme sage|blush|mono]
"""
import calendar
import datetime as dt
import sys

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

YEAR = 2027
FONT_DIR = "/usr/share/fonts/truetype/crosextra/"
pdfmetrics.registerFont(TTFont("Body", FONT_DIR + "Carlito-Regular.ttf"))
pdfmetrics.registerFont(TTFont("BodyB", FONT_DIR + "Carlito-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Head", FONT_DIR + "Caladea-Regular.ttf"))
pdfmetrics.registerFont(TTFont("HeadI", FONT_DIR + "Caladea-Italic.ttf"))

THEMES = {
    "sage": dict(accent="#7D9A86", light="#E6EEE8", ink="#2F3A33", line="#C9D3CC"),
    "blush": dict(accent="#C48B8B", light="#F5E7E5", ink="#3B2E2E", line="#E0CFCD"),
    "mono": dict(accent="#555555", light="#EEEEEE", ink="#222222", line="#CCCCCC"),
}

W, H = letter
M = 36            # outer margin
TAB_W = 26        # right navigation tab strip
CW = W - 2 * M - TAB_W  # content width
MONTHS = list(calendar.month_name)[1:]
MON_ABBR = [m[:3].upper() for m in MONTHS]
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
calendar.setfirstweekday(calendar.MONDAY)


def weeks_of_year():
    start = dt.date(YEAR, 1, 1)
    start -= dt.timedelta(days=start.weekday())
    weeks = []
    while start.year <= YEAR and not (start.year == YEAR and start > dt.date(YEAR, 12, 31)):
        weeks.append(start)
        start += dt.timedelta(days=7)
    return weeks


WEEKS = weeks_of_year()


def week_num(d):
    d = d - dt.timedelta(days=d.weekday())
    return WEEKS.index(d) + 1


def week_key(d):
    return "week_" + (d - dt.timedelta(days=d.weekday())).isoformat()


class Planner:
    def __init__(self, path, theme, print_mode=False):
        self.print_mode = print_mode
        t = THEMES[theme]
        self.A, self.L, self.INK, self.LN = (HexColor(t[k]) for k in ("accent", "light", "ink", "line"))
        self.c = canvas.Canvas(path, pagesize=letter, initialFontName="Body", initialFontSize=10)
        self.c.setTitle(f"{YEAR} Planner")
        self.c.setAuthor("Studio Planner Co.")
        self.page_no = 0
        if print_mode:
            # KDP paperback: no hyperlinks, no tabs, mirrored margins with a wider gutter
            self.c.linkRect = lambda *a, **k: None

    # ---------- helpers ----------
    def new_page(self, key=None, outline=None, level=0):
        if self.page_no:
            self.c.showPage()
        self.page_no += 1
        c = self.c
        c.setFillColor(white)
        c.rect(0, 0, W, H, stroke=0, fill=1)
        if key:
            c.bookmarkPage(key)
            if outline:
                c.addOutlineEntry(outline, key, level=level)
        if self.print_mode:
            # odd (right-hand) pages: gutter on the left = 0.75in; even pages: 0.61in left, gutter right
            c.translate(18 if self.page_no % 2 else 8, 0)
        else:
            self.tabs()

    def tabs(self, active=None):
        c = self.c
        x = W - M - TAB_W + 6
        labels = [("YEAR", "year")] + [(MON_ABBR[i], f"month_{i+1}") for i in range(12)] + [("NOTE", "notes")]
        h = (H - 2 * M) / len(labels)
        for i, (lab, key) in enumerate(labels):
            y = H - M - (i + 1) * h
            c.setFillColor(self.L if i % 2 else HexColor("#FFFFFF"))
            c.setStrokeColor(self.LN)
            c.setLineWidth(0.5)
            c.roundRect(x, y + 1, TAB_W - 6, h - 2, 4, stroke=1, fill=1)
            c.saveState()
            c.translate(x + (TAB_W - 6) / 2 + 3, y + h / 2)
            c.rotate(90)
            c.setFillColor(self.INK)
            c.setFont("BodyB", 7.5)
            c.drawCentredString(0, 0, lab)
            c.restoreState()
            c.linkRect("", key, (x, y + 1, x + TAB_W - 6, y + h - 1), relative=0, thickness=0)

    def title(self, text, sub=None):
        c = self.c
        c.setFillColor(self.INK)
        c.setFont("Head", 30)
        c.drawString(M, H - M - 28, text)
        if sub:
            c.setFont("HeadI", 13)
            c.setFillColor(self.A)
            c.drawString(M, H - M - 46, sub)
        c.setStrokeColor(self.A)
        c.setLineWidth(1.2)
        c.line(M, H - M - 56, M + CW, H - M - 56)
        return H - M - 70

    def label(self, x, y, text, size=9):
        c = self.c
        c.setFillColor(self.A)
        c.setFont("BodyB", size)
        c.drawString(x, y, text.upper())

    def lines(self, x, y_top, w, n, gap=20):
        c = self.c
        c.setStrokeColor(self.LN)
        c.setLineWidth(0.5)
        for i in range(n):
            y = y_top - (i + 1) * gap
            c.line(x, y, x + w, y)
        return y_top - n * gap

    def box(self, x, y, w, h, heading=None, fill=False, nlines=0, gap=20):
        c = self.c
        c.setStrokeColor(self.LN)
        c.setLineWidth(0.7)
        if fill:
            c.setFillColor(self.L)
            c.roundRect(x, y, w, h, 6, stroke=1, fill=1)
        else:
            c.roundRect(x, y, w, h, 6, stroke=1, fill=0)
        top = y + h
        if heading:
            self.label(x + 10, top - 16, heading)
            top -= 22
        if nlines:
            c.setStrokeColor(self.LN)
            c.setLineWidth(0.4)
            yy = top - gap
            while yy > y + 6:
                c.line(x + 10, yy, x + w - 10, yy)
                yy -= gap

    def checkbox_list(self, x, y_top, w, n, gap=20):
        c = self.c
        for i in range(n):
            y = y_top - (i + 1) * gap
            c.setStrokeColor(self.A)
            c.setLineWidth(0.7)
            c.rect(x, y + 2, 8, 8, stroke=1, fill=0)
            c.setStrokeColor(self.LN)
            c.setLineWidth(0.4)
            c.line(x + 14, y, x + w, y)

    def mini_month(self, x, y_top, w, month, link=True):
        c = self.c
        c.setFillColor(self.INK)
        c.setFont("BodyB", 10)
        c.drawString(x, y_top - 10, MONTHS[month - 1].upper())
        if link:
            c.linkRect("", f"month_{month}", (x, y_top - 14, x + w, y_top), relative=0, thickness=0)
        cw = w / 7
        c.setFont("BodyB", 6.5)
        c.setFillColor(self.A)
        for i, d in enumerate("MTWTFSS"):
            c.drawCentredString(x + cw * i + cw / 2, y_top - 24, d)
        c.setFont("Body", 7.5)
        c.setFillColor(self.INK)
        for r, week in enumerate(calendar.monthcalendar(YEAR, month)):
            for i, d in enumerate(week):
                if d:
                    cx, cy = x + cw * i + cw / 2, y_top - 36 - r * 11
                    c.drawCentredString(cx, cy, str(d))
                    if link:
                        k = week_key(dt.date(YEAR, month, d))
                        c.linkRect("", k, (cx - cw / 2, cy - 2, cx + cw / 2, cy + 8), relative=0, thickness=0)

    # ---------- pages ----------
    def cover(self):
        self.new_page("cover", "Cover")
        c = self.c
        if not self.print_mode:
            c.setFillColor(self.L)
            c.rect(M, M, CW, H - 2 * M, stroke=0, fill=1)
        c.setFillColor(self.A)
        c.rect(M, H / 2 - 2, CW, 4, stroke=0, fill=1)
        c.setFillColor(self.INK)
        c.setFont("Head", 110)
        c.drawCentredString(M + CW / 2, H / 2 + 40, str(YEAR))
        c.setFont("HeadI", 26)
        c.drawCentredString(M + CW / 2, H / 2 - 50, "Planner")
        c.setFont("Body", 11)
        c.setFillColor(self.A)
        c.drawCentredString(M + CW / 2, H / 2 - 75, "GOALS  ·  BUDGET  ·  HABITS  ·  WEEKLY PLANNING")
        c.setFillColor(self.INK)
        c.setFont("Body", 10)
        c.drawCentredString(M + CW / 2, M + 40, "This planner belongs to: ______________________________")

    def how_to(self):
        self.new_page("howto", "How to use")
        y = self.title("Welcome", "How to use your planner")
        tips = [
            "Start with the Year at a Glance and Yearly Goals pages to set your direction.",
            "Fill in the Yearly Finances page at the end of each month to watch your progress.",
            "Each month has 3 pages: a monthly calendar, a plan & budget page and a habit tracker.",
            "Weekly pages follow each month's habit tracker. Weeks start on Monday.",
            "Use the habit tracker to color in one square for every day you keep a habit.",
            "Review the 'What went well' and 'What I'll improve' boxes at the end of every month.",
            "Use the dot-grid Notes pages at the back for lists, ideas and brain dumps.",
        ] if self.print_mode else [
            "Printable: print any page at 100% (US Letter). A4 also works with 'fit to page'.",
            "Digital: import the PDF into GoodNotes, Notability, Noteshelf, Xodo or any PDF annotation app.",
            "Navigation: tap the tabs on the right edge to jump to the Year overview, any month, or Notes.",
            "Tap a month name on the Year page to open that month. Tap any day to open its week.",
            "On monthly calendars, tap the week number (W1, W2...) to open that weekly page.",
            "Every month includes: calendar, budget & goals page, and a 31-day habit tracker.",
            "Use the Notes section at the end for lists, ideas and brain dumps.",
        ]
        c = self.c
        c.setFont("Body", 12)
        c.setFillColor(self.INK)
        for t in tips:
            y -= 30
            c.setFillColor(self.A)
            c.circle(M + 6, y + 4, 3, stroke=0, fill=1)
            c.setFillColor(self.INK)
            c.drawString(M + 18, y, t)
        self.box(M, M, CW, 260, "My intention for " + str(YEAR), nlines=True, gap=22)

    def year(self):
        self.new_page("year", "Year at a glance")
        y = self.title(f"{YEAR} at a Glance")
        cols, gap = 3, 22
        w = (CW - gap * (cols - 1)) / cols
        for i in range(12):
            r, col = divmod(i, cols)
            self.mini_month(M + col * (w + gap), y - 10 - r * 150, w, i + 1)

    def goals(self):
        self.new_page("goals", "Yearly goals")
        y = self.title("Yearly Goals", "Dream it, plan it, do it")
        areas = ["Health & Fitness", "Money & Career", "Relationships", "Personal Growth", "Home & Lifestyle", "Fun & Travel"]
        gap = 14
        w = (CW - gap) / 2
        h = (y - M - 2 * gap) / 3
        for i, a in enumerate(areas):
            r, col = divmod(i, 2)
            self.box(M + col * (w + gap), y - (r + 1) * h - r * gap, w, h, a, nlines=True)

    def finance_year(self):
        self.new_page("finance", "Yearly finance overview")
        y = self.title("Yearly Finances", "Income · Expenses · Savings")
        c = self.c
        cols = ["MONTH", "INCOME", "EXPENSES", "SAVINGS", "DEBT PAID", "NOTES"]
        widths = [0.16, 0.15, 0.15, 0.15, 0.15, 0.24]
        rh = 28
        yy = y - 10
        c.setFillColor(self.L)
        c.rect(M, yy - rh, CW, rh, stroke=0, fill=1)
        x = M
        for col, wf in zip(cols, widths):
            self.label(x + 6, yy - 18, col, 8.5)
            x += CW * wf
        for i, m in enumerate(MONTHS + ["TOTAL"]):
            top = yy - rh * (i + 1)
            c.setStrokeColor(self.LN)
            c.setLineWidth(0.5)
            c.line(M, top - rh, M + CW, top - rh)
            c.setFillColor(self.INK)
            c.setFont("BodyB" if m == "TOTAL" else "Body", 10)
            c.drawString(M + 6, top - 18, m)
        x = M
        for wf in widths[:-1]:
            x += CW * wf
            c.line(x, yy, x, yy - rh * 14)
        self.box(M, M, CW, yy - rh * 14 - M - 16, "Savings goal tracker", nlines=True)

    def month_cal(self, m):
        self.new_page(f"month_{m}", MONTHS[m - 1], 0)
        y = self.title(MONTHS[m - 1], str(YEAR))
        c = self.c
        weeks = calendar.monthcalendar(YEAR, m)
        wk_w = 22
        cw = (CW - wk_w) / 7
        top = y - 8
        for i, d in enumerate(DAYS):
            self.label(M + wk_w + i * cw + 4, top - 12, d, 8)
        top -= 20
        notes_h = 110
        rh = (top - M - notes_h - 10) / len(weeks)
        for r, week in enumerate(weeks):
            ry = top - (r + 1) * rh
            first = next(d for d in week if d)
            wdate = dt.date(YEAR, m, first)
            wnum = week_num(wdate)
            c.setFillColor(self.L)
            c.roundRect(M, ry + 2, wk_w - 4, rh - 4, 4, stroke=0, fill=1)
            c.saveState()
            c.translate(M + (wk_w - 4) / 2 + 3, ry + rh / 2)
            c.rotate(90)
            c.setFillColor(self.A)
            c.setFont("BodyB", 8)
            c.drawCentredString(0, 0, f"W{wnum}")
            c.restoreState()
            c.linkRect("", week_key(wdate), (M, ry + 2, M + wk_w - 4, ry + rh - 2), relative=0, thickness=0)
            for i, d in enumerate(week):
                x = M + wk_w + i * cw
                c.setStrokeColor(self.LN)
                c.setLineWidth(0.6)
                if d:
                    c.setFillColor(self.L if i >= 5 else white)
                    c.rect(x, ry, cw, rh, stroke=1, fill=1)
                    c.setFillColor(self.INK)
                    c.setFont("BodyB", 10)
                    c.drawString(x + 4, ry + rh - 13, str(d))
                else:
                    c.rect(x, ry, cw, rh, stroke=1, fill=0)
        self.box(M, M, CW, notes_h, "Notes & priorities", nlines=True, gap=18)

    def month_plan(self, m):
        self.new_page(f"plan_{m}", f"{MONTHS[m-1]} plan & budget", 1)
        y = self.title(f"{MONTHS[m - 1]} Plan", "Goals · Budget · Reflection")
        gap = 14
        w = (CW - gap) / 2
        # left column: goals, to-do, important dates
        h1 = 190
        self.box(M, y - h1, w, h1, "Goals & to-do")
        self.checkbox_list(M + 10, y - 22, w - 20, 7, 22)
        self.box(M, y - 2 * h1 - gap, w, h1, "Important dates", nlines=True)
        # right column: budget
        c = self.c
        bx = M + w + gap
        bh = 2 * h1 + gap
        self.box(bx, y - bh, w, bh, "Monthly budget")
        rows = ["Income", "Rent / Mortgage", "Utilities", "Groceries", "Transport", "Insurance",
                "Debt payments", "Subscriptions", "Dining out", "Shopping", "Health", "Savings",
                "Other", "TOTAL EXPENSES", "LEFT OVER"]
        c.setFont("BodyB", 7.5)
        c.setFillColor(self.A)
        c.drawString(bx + w - 110, y - 30, "PLANNED")
        c.drawString(bx + w - 52, y - 30, "ACTUAL")
        ry = y - 36
        for r in rows:
            ry -= 23
            bold = r.isupper()
            c.setFont("BodyB" if bold else "Body", 9.5)
            c.setFillColor(self.INK)
            c.drawString(bx + 10, ry + 5, r)
            c.setStrokeColor(self.LN)
            c.setLineWidth(0.4)
            c.line(bx + w - 115, ry + 2, bx + w - 65, ry + 2)
            c.line(bx + w - 57, ry + 2, bx + w - 10, ry + 2)
        bottom = y - bh - gap
        self.box(M, M, w, bottom - M, "What went well", nlines=True)
        self.box(bx, M, w, bottom - M, "What I'll improve", nlines=True)

    def habits(self, m):
        self.new_page(f"habit_{m}", f"{MONTHS[m-1]} habit tracker", 1)
        y = self.title(f"{MONTHS[m - 1]} Habits", "Small steps, every day")
        c = self.c
        days = calendar.monthrange(YEAR, m)[1]
        name_w = 120
        cw = (CW - name_w) / 31
        top = y - 10
        c.setFont("BodyB", 7)
        for d in range(1, days + 1):
            wd = dt.date(YEAR, m, d).weekday()
            c.setFillColor(self.A if wd >= 5 else self.INK)
            c.drawCentredString(M + name_w + (d - 1) * cw + cw / 2, top - 10, str(d))
        nrows = 15
        rh = 26
        for r in range(nrows):
            ry = top - 16 - (r + 1) * rh
            c.setStrokeColor(self.LN)
            c.setLineWidth(0.4)
            c.line(M, ry, M + name_w - 6, ry)
            for d in range(days):
                x = M + name_w + d * cw
                c.setFillColor(self.L)
                c.rect(x + 1, ry + 2, cw - 2, rh - 4, stroke=0, fill=1)
        bottom = top - 16 - nrows * rh - 14
        gap = 14
        w = (CW - gap) / 2
        self.box(M, M, w, bottom - M, "Mood & energy", nlines=True)
        self.box(M + w + gap, M, w, bottom - M, "Wins this month", nlines=True)

    def week(self, start):
        end = start + dt.timedelta(days=6)
        wn = week_num(start)
        self.new_page(week_key(start), f"Week {wn}: {start:%b %d}", 1)
        rng = f"{start:%b %d} – {end:%b %d, %Y}"
        y = self.title(f"Week {wn}", rng)
        c = self.c
        gap = 10
        col_w = (CW - gap) / 2
        rh = (y - M - 3 * gap) / 4
        for i in range(8):
            r, col = divmod(i, 2)
            x = M + col * (col_w + gap)
            by = y - (r + 1) * rh - r * gap
            if i < 7:
                d = start + dt.timedelta(days=i)
                in_year = d.year == YEAR
                self.box(x, by, col_w, rh, None, fill=False, nlines=False)
                c.setFillColor(self.L)
                c.roundRect(x, by + rh - 22, col_w, 22, 6, stroke=0, fill=1)
                c.setFillColor(self.INK)
                c.setFont("BodyB", 10)
                c.drawString(x + 10, by + rh - 15, f"{DAYS[i]}  {d.day}")
                c.setFont("Body", 8.5)
                c.setFillColor(self.A)
                c.drawRightString(x + col_w - 10, by + rh - 15, d.strftime("%B"))
                if in_year:
                    c.linkRect("", f"month_{d.month}", (x, by + rh - 22, x + col_w, by + rh), relative=0, thickness=0)
                c.setStrokeColor(self.LN)
                c.setLineWidth(0.4)
                yy = by + rh - 22 - 18
                while yy > by + 6:
                    c.line(x + 10, yy, x + col_w - 10, yy)
                    yy -= 18
            else:
                self.box(x, by, col_w, rh, "Priorities & to-do")
                self.checkbox_list(x + 10, by + rh - 18, col_w - 20, int((rh - 24) // 18), 18)

    def notes(self, n=6):
        for i in range(n):
            key = "notes" if i == 0 else f"notes_{i}"
            self.new_page(key, "Notes" if i == 0 else None)
            y = self.title("Notes")
            c = self.c
            c.setFillColor(self.LN)
            yy = y - 10
            while yy > M:
                x = M
                while x < M + CW:
                    c.circle(x, yy, 0.8, stroke=0, fill=1)
                    x += 14
                yy -= 14

    def build(self):
        self.cover()
        self.how_to()
        self.year()
        self.goals()
        self.finance_year()
        for m in range(1, 13):
            self.month_cal(m)
            self.month_plan(m)
            self.habits(m)
            for w in WEEKS:
                # place each week after the month in which it starts (first week -> January)
                if (w.year == YEAR and w.month == m) or (w.year < YEAR and m == 1):
                    self.week(w)
        self.notes()
        self.c.save()
        return self.page_no


if __name__ == "__main__":
    out = sys.argv[1]
    theme = sys.argv[sys.argv.index("--theme") + 1] if "--theme" in sys.argv else "sage"
    n = Planner(out, theme, print_mode="--print" in sys.argv).build()
    print(f"{out}: {n} pages")

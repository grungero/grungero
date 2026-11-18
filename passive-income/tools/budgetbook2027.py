"""KDP paperback interior: 2027 Budget Planner & Expense Tracker (8.5x11, B&W).

Usage: python3 budgetbook2027.py <out.pdf>
"""
import calendar
import sys

import planner2027 as P
from planner2027 import CW, H, M, MONTHS, YEAR, Planner


class BudgetBook(Planner):
    def table(self, y_top, cols, widths, nrows, rh=22, head_h=24):
        """Ruled table with header. widths are fractions of CW."""
        c = self.c
        c.setFillColor(self.L)
        c.rect(M, y_top - head_h, CW, head_h, stroke=0, fill=1)
        x = M
        for col, wf in zip(cols, widths):
            self.label(x + 5, y_top - 16, col, 8)
            x += CW * wf
        c.setStrokeColor(self.LN)
        c.setLineWidth(0.5)
        bottom = y_top - head_h - nrows * rh
        for r in range(nrows + 1):
            y = y_top - head_h - r * rh
            c.line(M, y, M + CW, y)
        x = M
        for wf in widths[:-1]:
            x += CW * wf
            c.line(x, y_top, x, bottom)
        c.rect(M, bottom, CW, y_top - bottom, stroke=1, fill=0)
        return bottom

    def front(self):
        self.new_page("title", "Title")
        c = self.c
        c.setFillColor(self.INK)
        c.setFont("Head", 84)
        c.drawCentredString(M + CW / 2, H / 2 + 60, str(YEAR))
        c.setFont("HeadI", 28)
        c.drawCentredString(M + CW / 2, H / 2 + 10, "Budget Planner")
        c.setFont("Body", 12)
        c.setFillColor(self.A)
        c.drawCentredString(M + CW / 2, H / 2 - 20, "MONTHLY BUDGET  ·  EXPENSE TRACKER  ·  BILLS  ·  SAVINGS  ·  DEBT")
        c.setFillColor(self.INK)
        c.setFont("Body", 11)
        c.drawCentredString(M + CW / 2, M + 60, "This book belongs to: ______________________________")

        self.new_page("howto", "How to use")
        y = self.title("How to Use This Book", "Simple steps to take control of your money")
        steps = [
            "1. Fill in your Financial Snapshot and money goals for the year.",
            "2. List every recurring bill in the Bill Tracker and tick each month as you pay it.",
            "3. At the start of each month, plan your income and expenses on the Monthly Budget page.",
            "4. Log every purchase on the Expense Tracker pages (4 pages per month).",
            "5. At month end, total each category on the Monthly Review page and compare to your plan.",
            "6. Copy your monthly totals to the Yearly Overview to see your whole year.",
            "7. Use the Savings, Sinking Funds and Debt Payoff trackers at the back to watch progress.",
        ]
        c.setFont("Body", 12)
        for s in steps:
            y -= 28
            c.setFillColor(self.INK)
            c.drawString(M + 6, y, s)
        self.box(M, M, CW, y - M - 30, "My money motto for " + str(YEAR), nlines=True, gap=22)

    def snapshot(self):
        self.new_page("snapshot", "Financial snapshot")
        y = self.title("Financial Snapshot", "Where I'm starting on January 1")
        gap = 14
        w = (CW - gap) / 2
        h = 250
        for i, (head, rows) in enumerate((("What I own (assets)", 9), ("What I owe (debts)", 9))):
            x = M + i * (w + gap)
            self.box(x, y - h, w, h, head)
            self.lines(x + 10, y - 26, w - 20, rows, 22)
        y2 = y - h - gap
        self.box(M, y2 - 70, CW, 70, "Net worth = assets − debts")
        self.box(M, M, CW, y2 - 70 - gap - M, f"My money goals for {YEAR}")
        self.checkbox_list(M + 10, y2 - 70 - gap - 26, CW - 20, int((y2 - 70 - gap - M - 30) // 24), 24)

    def yearly(self):
        self.new_page("yearly", "Yearly overview")
        y = self.title("Yearly Overview", f"Copy your monthly totals here")
        bottom = self.table(y - 6, ["MONTH", "INCOME", "EXPENSES", "SAVED", "DEBT PAID", "NET"],
                            [0.2, 0.16, 0.16, 0.16, 0.16, 0.16], 13, rh=30)
        c = self.c
        c.setFillColor(self.INK)
        for i, m in enumerate(MONTHS + ["TOTAL"]):
            c.setFont("BodyB" if m == "TOTAL" else "Body", 10.5)
            c.drawString(M + 6, y - 6 - 24 - i * 30 - 19, m)
        self.box(M, M, CW, bottom - M - 16, "Notes on my year", nlines=True)

    def bills(self):
        for part in range(2):
            self.new_page(f"bills_{part}", "Bill tracker" if part == 0 else None)
            y = self.title("Bill Tracker", "Tick each bill when paid")
            cols = ["BILL", "DUE", "AMOUNT"] + [m[:1] for m in MONTHS]
            widths = [0.24, 0.08, 0.12] + [0.56 / 12] * 12
            c = self.c
            self.table(y - 6, cols, widths, 24, rh=25)

    def month(self, m):
        name = MONTHS[m - 1]
        # monthly budget
        self.new_page(f"budget_{m}", f"{name}", 0)
        y = self.title(f"{name} Budget", str(YEAR))
        gap = 14
        w = (CW - gap) / 2
        h_inc = 150
        self.box(M, y - h_inc, w, h_inc, "Income")
        self.lines(M + 10, y - 26, w - 20, 5, 22)
        self.box(M + w + gap, y - h_inc, w, h_inc, "Summary")
        c = self.c
        sy = y - 40
        for lab in ("Total income", "Total expenses", "Savings", "Debt payments", "Left over"):
            c.setFillColor(self.INK)
            c.setFont("Body", 10.5)
            c.drawString(M + w + gap + 12, sy, lab)
            c.setStrokeColor(self.LN)
            c.line(M + w + gap + 120, sy - 2, M + 2 * w + gap - 12, sy - 2)
            sy -= 22
        y2 = y - h_inc - gap
        cats = ["Housing", "Utilities", "Phone & internet", "Groceries", "Dining out", "Transport / fuel",
                "Insurance", "Health", "Debt payments", "Subscriptions", "Personal care", "Clothing",
                "Kids / family", "Pets", "Entertainment", "Gifts", "Savings", "Other", "Other"]
        bottom = self.table(y2, ["EXPENSE CATEGORY", "BUDGET", "ACTUAL", "DIFFERENCE"], [0.4, 0.2, 0.2, 0.2],
                            len(cats), rh=21)
        c.setFont("Body", 10)
        c.setFillColor(self.INK)
        for i, cat in enumerate(cats):
            c.drawString(M + 6, y2 - 24 - i * 21 - 15, cat)
        # expense log x4
        for k in range(4):
            self.new_page(f"log_{m}_{k}")
            yy = self.title(f"{name} Expenses", f"Page {k + 1} of 4")
            self.table(yy - 6, ["DATE", "DESCRIPTION", "CATEGORY", "PAYMENT", "AMOUNT"],
                       [0.11, 0.39, 0.2, 0.13, 0.17], 26, rh=24)
        # monthly review
        self.new_page(f"review_{m}")
        y = self.title(f"{name} Review", "How did this month go?")
        h1 = 210
        self.box(M, y - h1, w, h1, "Wins", nlines=True)
        self.box(M + w + gap, y - h1, w, h1, "Where I overspent", nlines=True)
        y3 = y - h1 - gap
        self.box(M, y3 - h1, w, h1, "Spending by week")
        cy = y3 - 40
        for wk in range(1, 6):
            c.setFillColor(self.INK)
            c.setFont("Body", 10.5)
            c.drawString(M + 12, cy, f"Week {wk}")
            c.setStrokeColor(self.LN)
            c.line(M + 70, cy - 2, M + w - 12, cy - 2)
            cy -= 30
        self.box(M + w + gap, y3 - h1, w, h1, "Changes for next month", nlines=True)
        self.box(M, M, CW, y3 - h1 - gap - M, "No-spend days (cross off)")
        days = calendar.monthrange(YEAR, m)[1]
        bx, by = M + 14, y3 - h1 - gap - 40
        cw = (CW - 28) / 16
        for d in range(1, days + 1):
            r, col = divmod(d - 1, 16)
            x = bx + col * cw
            yy = by - r * 34
            c.setStrokeColor(self.A)
            c.circle(x + cw / 2, yy, 11, stroke=1, fill=0)
            c.setFont("Body", 8.5)
            c.setFillColor(self.INK)
            c.drawCentredString(x + cw / 2, yy - 3, str(d))

    def back(self):
        for i in range(4):
            self.new_page(f"savings_{i}", "Savings goals" if i == 0 else None)
            y = self.title("Savings Goal", "Color in a box for every amount saved")
            c = self.c
            self.box(M, y - 60, CW, 60, "Goal:                                         Target amount:                     Target date:")
            # 100-box grid
            top = y - 80
            cols, rows = 10, 10
            cw = CW / cols
            rh = (top - M - 60) / rows
            for r in range(rows):
                for col in range(cols):
                    c.setStrokeColor(self.LN)
                    c.rect(M + col * cw + 3, top - (r + 1) * rh + 3, cw - 6, rh - 6, stroke=1, fill=0)
            self.box(M, M, CW, 48, "Each box = $")
        for i in range(3):
            self.new_page(f"sinking_{i}", "Sinking funds" if i == 0 else None)
            y = self.title("Sinking Funds", "Save a little each month for big expenses")
            gap = 14
            w = (CW - gap) / 2
            h = (y - M - gap) / 2
            for k in range(4):
                r, col = divmod(k, 2)
                x = M + col * (w + gap)
                by = y - (r + 1) * h - r * gap
                self.box(x, by, w, h, "Fund:                      Goal: $")
                self.lines(x + 10, by + h - 26, w - 20, int((h - 30) // 22), 22)
        for i in range(4):
            self.new_page(f"debt_{i}", "Debt payoff" if i == 0 else None)
            y = self.title("Debt Payoff Tracker", "Creditor:                          Starting balance:                 Rate:")
            self.table(y - 6, ["DATE", "PAYMENT", "INTEREST", "NEW BALANCE", "NOTES"],
                       [0.15, 0.17, 0.17, 0.2, 0.31], 26, rh=24)
        for i in range(10):
            self.new_page("notes" if i == 0 else f"notes_{i}", "Notes" if i == 0 else None)
            y = self.title("Notes")
            self.lines(M, y - 6, CW, int((y - 6 - M) // 24), 24)

    def build(self):
        self.front()
        self.snapshot()
        self.yearly()
        self.bills()
        for m in range(1, 13):
            self.month(m)
        self.back()
        if self.page_no % 2:
            self.new_page("blank")
        self.c.save()
        return self.page_no


if __name__ == "__main__":
    n = BudgetBook(sys.argv[1], "mono", print_mode=True).build()
    print(sys.argv[1], n, "pages")

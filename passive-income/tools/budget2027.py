"""Generate the 2027 Budget Planner spreadsheet (Excel + Google Sheets compatible).

Usage: python3 budget2027.py <out.xlsx>
"""
import sys

from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.formatting.rule import CellIsRule, DataBarRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

YEAR = 2027
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
ACC, LIGHT, INK, LINE = "7D9A86", "E6EEE8", "2F3A33", "C9D3CC"
F_TITLE = Font(name="Calibri", size=22, bold=True, color=INK)
F_SUB = Font(name="Calibri", size=11, italic=True, color=ACC)
F_HEAD = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
F_BOLD = Font(name="Calibri", size=11, bold=True, color=INK)
F_BODY = Font(name="Calibri", size=11, color=INK)
FILL_ACC = PatternFill("solid", fgColor=ACC)
FILL_LIGHT = PatternFill("solid", fgColor=LIGHT)
FILL_INPUT = PatternFill("solid", fgColor="FFFDF5")
THIN = Side(style="thin", color=LINE)
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
MONEY = '"$"#,##0.00;[Red]-"$"#,##0.00'
PCT = "0%"

INCOME_CATS = ["Salary", "Side Income", "Bonus", "Investments", "Other Income"]
EXPENSE_CATS = [
    ("Rent / Mortgage", 1200), ("Utilities", 180), ("Internet & Phone", 90), ("Groceries", 450),
    ("Dining Out", 150), ("Transportation", 200), ("Car Payment", 0), ("Insurance", 150),
    ("Health & Medical", 80), ("Debt Payments", 200), ("Subscriptions", 40), ("Personal Care", 50),
    ("Clothing", 60), ("Entertainment", 80), ("Gifts & Donations", 50), ("Kids & Family", 0),
    ("Pets", 0), ("Education", 0), ("Travel", 100), ("Savings & Investing", 300),
    ("Emergency Fund", 100), ("Miscellaneous", 50),
]
INCOME_DEFAULT = [4000, 0, 0, 0, 0]
TX_ROWS = 200


def hdr(ws, row, col, labels, widths=None):
    for i, lab in enumerate(labels):
        c = ws.cell(row=row, column=col + i, value=lab)
        c.font, c.fill, c.border = F_HEAD, FILL_ACC, BOX
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[row].height = 22


def title(ws, text, sub):
    ws["B2"] = text
    ws["B2"].font = F_TITLE
    ws["B3"] = sub
    ws["B3"].font = F_SUB
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 3


def cell(ws, ref, value=None, font=F_BODY, fmt=None, fill=None, border=True, align=None):
    c = ws[ref]
    if value is not None:
        c.value = value
    c.font = font
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if border:
        c.border = BOX
    if align:
        c.alignment = Alignment(horizontal=align)
    return c


def build(out):
    wb = Workbook()

    # ---------------- START HERE ----------------
    ws = wb.active
    ws.title = "Start Here"
    title(ws, f"{YEAR} Budget Planner", "Track income, expenses, savings & debt — all in one place")
    ws.column_dimensions["B"].width = 100
    steps = [
        "HOW TO USE",
        "1.  Go to the 'Categories' tab. Rename categories if you like and enter your MONTHLY BUDGET for each one (cream cells).",
        "2.  Each month tab (Jan–Dec) has a transaction log. Add every income and expense: date, description, category (drop-down) and amount.",
        "3.  The summary on the right of each month fills itself in: budget vs. actual, remaining, and % used per category.",
        "4.  The 'Dashboard' tab shows your whole year: income vs. expenses, savings rate and spending by category, with charts.",
        "5.  Use 'Savings Goals' and 'Debt Payoff' to watch your progress bars fill up.",
        "",
        "TIPS",
        "•  Only type in cream-colored cells. Everything else is calculated automatically.",
        "•  Google Sheets: File → Import → Upload this .xlsx (or open it from Google Drive) — all formulas keep working.",
        "•  Category names update everywhere when you rename them on the 'Categories' tab.",
        "•  Want a different currency? Select the cells and change the number format (Format → Number).",
        "",
        "Thank you for your purchase — here's to your best financial year yet!",
    ]
    for i, s in enumerate(steps):
        c = ws.cell(row=5 + i, column=2, value=s)
        c.font = F_BOLD if s.isupper() else F_BODY
        c.alignment = Alignment(wrap_text=True, vertical="top")

    # ---------------- CATEGORIES ----------------
    cat = wb.create_sheet("Categories")
    title(cat, "Categories & Monthly Budget", "Enter your planned monthly amount for each category")
    cat.column_dimensions["B"].width = 28
    cat.column_dimensions["C"].width = 18
    cat.column_dimensions["E"].width = 28
    cat.column_dimensions["F"].width = 18
    hdr(cat, 5, 2, ["Income Source", "Expected / Month"])
    for i, (name, val) in enumerate(zip(INCOME_CATS, INCOME_DEFAULT)):
        r = 6 + i
        cell(cat, f"B{r}", name, fill=FILL_INPUT)
        cell(cat, f"C{r}", val, fmt=MONEY, fill=FILL_INPUT)
    r_inc_tot = 6 + len(INCOME_CATS)
    cell(cat, f"B{r_inc_tot}", "TOTAL", F_BOLD, fill=FILL_LIGHT)
    cell(cat, f"C{r_inc_tot}", f"=SUM(C6:C{r_inc_tot-1})", F_BOLD, MONEY, FILL_LIGHT)

    hdr(cat, 5, 5, ["Expense Category", "Budget / Month"])
    for i, (name, val) in enumerate(EXPENSE_CATS):
        r = 6 + i
        cell(cat, f"E{r}", name, fill=FILL_INPUT)
        cell(cat, f"F{r}", val, fmt=MONEY, fill=FILL_INPUT)
    r_exp_last = 5 + len(EXPENSE_CATS)
    r_exp_tot = r_exp_last + 1
    cell(cat, f"E{r_exp_tot}", "TOTAL", F_BOLD, fill=FILL_LIGHT)
    cell(cat, f"F{r_exp_tot}", f"=SUM(F6:F{r_exp_last})", F_BOLD, MONEY, FILL_LIGHT)
    cell(cat, f"B{r_inc_tot+2}", "Planned left over / month", F_BOLD, fill=FILL_LIGHT)
    cell(cat, f"C{r_inc_tot+2}", f"=C{r_inc_tot}-F{r_exp_tot}", F_BOLD, MONEY, FILL_LIGHT)

    inc_range = f"Categories!$B$6:$B${5+len(INCOME_CATS)}"
    exp_range = f"Categories!$E$6:$E${r_exp_last}"
    # list of all categories for drop-down (hidden helper column H)
    cat.column_dimensions["H"].hidden = True
    all_cats = [f"=B{6+i}" for i in range(len(INCOME_CATS))] + [f"=E{6+i}" for i in range(len(EXPENSE_CATS))]
    for i, f in enumerate(all_cats):
        cat.cell(row=6 + i, column=8, value=f)
    dd_range = f"Categories!$H$6:$H${5+len(all_cats)}"

    # ---------------- MONTH SHEETS ----------------
    n_exp = len(EXPENSE_CATS)
    n_inc = len(INCOME_CATS)
    for m, mname in enumerate(MONTHS):
        ws = wb.create_sheet(mname[:3])
        title(ws, f"{mname} {YEAR}", "Log every transaction on the left — the summary updates automatically")
        for col, w in zip("BCDEFGHIJKLM", [12, 30, 22, 13, 3, 24, 14, 14, 14, 10, 3, 3]):
            ws.column_dimensions[col].width = w
        # transaction log
        hdr(ws, 5, 2, ["Date", "Description", "Category", "Amount"])
        dv = DataValidation(type="list", formula1=f"={dd_range}", allow_blank=True)
        ws.add_data_validation(dv)
        for r in range(6, 6 + TX_ROWS):
            cell(ws, f"B{r}", fmt="mmm d", fill=FILL_INPUT)
            cell(ws, f"C{r}", fill=FILL_INPUT)
            cell(ws, f"D{r}", fill=FILL_INPUT)
            cell(ws, f"E{r}", fmt=MONEY, fill=FILL_INPUT)
        dv.add(f"D6:D{5+TX_ROWS}")
        tx_cat = f"$D$6:$D${5+TX_ROWS}"
        tx_amt = f"$E$6:$E${5+TX_ROWS}"
        # summary
        hdr(ws, 5, 7, ["Income", "Expected", "Actual", "Difference", ""])
        for i in range(n_inc):
            r = 6 + i
            cell(ws, f"G{r}", f"=Categories!B{6+i}")
            cell(ws, f"H{r}", f"=Categories!C{6+i}", fmt=MONEY)
            cell(ws, f"I{r}", f"=SUMIF({tx_cat},G{r},{tx_amt})", fmt=MONEY)
            cell(ws, f"J{r}", f"=I{r}-H{r}", fmt=MONEY)
        ri = 6 + n_inc
        cell(ws, f"G{ri}", "TOTAL INCOME", F_BOLD, fill=FILL_LIGHT)
        for col in "HIJ":
            cell(ws, f"{col}{ri}", f"=SUM({col}6:{col}{ri-1})", F_BOLD, MONEY, FILL_LIGHT)

        e0 = ri + 2
        hdr(ws, e0, 7, ["Expenses", "Budget", "Actual", "Remaining", "% Used"])
        for i in range(n_exp):
            r = e0 + 1 + i
            cell(ws, f"G{r}", f"=Categories!E{6+i}")
            cell(ws, f"H{r}", f"=Categories!F{6+i}", fmt=MONEY)
            cell(ws, f"I{r}", f"=SUMIF({tx_cat},G{r},{tx_amt})", fmt=MONEY)
            cell(ws, f"J{r}", f"=H{r}-I{r}", fmt=MONEY)
            cell(ws, f"K{r}", f'=IF(H{r}=0,IF(I{r}>0,1,0),I{r}/H{r})', fmt=PCT)
        el = e0 + n_exp
        et = el + 1
        cell(ws, f"G{et}", "TOTAL EXPENSES", F_BOLD, fill=FILL_LIGHT)
        for col in "HIJ":
            cell(ws, f"{col}{et}", f"=SUM({col}{e0+1}:{col}{el})", F_BOLD, MONEY, FILL_LIGHT)
        cell(ws, f"K{et}", f"=IF(H{et}=0,0,I{et}/H{et})", F_BOLD, PCT, FILL_LIGHT)
        ws.conditional_formatting.add(f"K{e0+1}:K{el}",
                                      DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color=ACC))
        ws.conditional_formatting.add(f"J{e0+1}:J{el}",
                                      CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B", bold=True)))
        s0 = et + 2
        cell(ws, f"G{s0}", "NET (Income − Expenses)", F_BOLD, fill=FILL_LIGHT)
        cell(ws, f"I{s0}", f"=I{ri}-I{et}", F_BOLD, MONEY, FILL_LIGHT)
        cell(ws, f"G{s0+1}", "Savings rate", F_BOLD, fill=FILL_LIGHT)
        sav_rows = [e0 + 1 + i for i, (n, _) in enumerate(EXPENSE_CATS) if n in ("Savings & Investing", "Emergency Fund")]
        sav = "+".join(f"I{r}" for r in sav_rows)
        cell(ws, f"I{s0+1}", f"=IF(I{ri}=0,0,({sav}+MAX(I{s0},0))/I{ri})", F_BOLD, PCT, FILL_LIGHT)
        ws.freeze_panes = "B6"
        # remember layout for dashboard
        layout = dict(ri=ri, e0=e0, et=et, s0=s0)

    # ---------------- DASHBOARD ----------------
    db = wb.create_sheet("Dashboard", 1)
    title(db, f"{YEAR} Dashboard", "Your year at a glance — updates automatically")
    for col, w in zip("BCDEFG", [16, 16, 16, 16, 14, 3]):
        db.column_dimensions[col].width = w
    hdr(db, 5, 2, ["Month", "Income", "Expenses", "Net", "Savings Rate"])
    for i, mname in enumerate(MONTHS):
        r = 6 + i
        s = mname[:3]
        cell(db, f"B{r}", mname)
        cell(db, f"C{r}", f"='{s}'!I{layout['ri']}", fmt=MONEY)
        cell(db, f"D{r}", f"='{s}'!I{layout['et']}", fmt=MONEY)
        cell(db, f"E{r}", f"=C{r}-D{r}", fmt=MONEY)
        cell(db, f"F{r}", f"='{s}'!I{layout['s0']+1}", fmt=PCT)
    cell(db, "B18", "TOTAL", F_BOLD, fill=FILL_LIGHT)
    for col in "CDE":
        cell(db, f"{col}18", f"=SUM({col}6:{col}17)", F_BOLD, MONEY, FILL_LIGHT)
    cell(db, "F18", "=IF(C18=0,0,E18/C18)", F_BOLD, PCT, FILL_LIGHT)
    db.conditional_formatting.add("E6:E17", CellIsRule(operator="lessThan", formula=["0"], font=Font(color="C0392B", bold=True)))

    hdr(db, 21, 2, ["Expense Category", "Annual Budget", "Annual Actual", "Remaining", "% Used"])
    for i in range(n_exp):
        r = 22 + i
        row = layout["e0"] + 1 + i
        cell(db, f"B{r}", f"=Categories!E{6+i}")
        cell(db, f"C{r}", f"=Categories!F{6+i}*12", fmt=MONEY)
        cell(db, f"D{r}", "=" + "+".join(f"'{m[:3]}'!I{row}" for m in MONTHS), fmt=MONEY)
        cell(db, f"E{r}", f"=C{r}-D{r}", fmt=MONEY)
        cell(db, f"F{r}", f"=IF(C{r}=0,0,D{r}/C{r})", fmt=PCT)
    last = 21 + n_exp
    db.column_dimensions["B"].width = 24
    db.conditional_formatting.add(f"F22:F{last}",
                                  DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color=ACC))

    bar = BarChart()
    bar.type = "col"
    bar.title = "Income vs Expenses"
    bar.y_axis.numFmt = '"$"#,##0'
    bar.add_data(Reference(db, min_col=3, max_col=4, min_row=5, max_row=17), titles_from_data=True)
    bar.set_categories(Reference(db, min_col=2, min_row=6, max_row=17))
    bar.height, bar.width = 9, 18
    bar.series[0].graphicalProperties.solidFill = ACC
    bar.series[1].graphicalProperties.solidFill = "C48B8B"
    db.add_chart(bar, "H5")

    pie = PieChart()
    pie.title = "Spending by Category"
    pie.add_data(Reference(db, min_col=4, min_row=21, max_row=last), titles_from_data=True)
    pie.set_categories(Reference(db, min_col=2, min_row=22, max_row=last))
    pie.height, pie.width = 11, 18
    db.add_chart(pie, "H24")

    # ---------------- SAVINGS GOALS ----------------
    sg = wb.create_sheet("Savings Goals")
    title(sg, "Savings Goals", "Watch your progress bars fill up")
    for col, w in zip("BCDEFG", [30, 16, 16, 16, 14, 16]):
        sg.column_dimensions[col].width = w
    hdr(sg, 5, 2, ["Goal", "Target", "Saved So Far", "Still Needed", "Progress", "Target Date"])
    examples = [("Emergency fund (3 months)", 6000, 1500), ("Vacation", 2500, 400), ("New laptop", 1200, 0)]
    for i in range(12):
        r = 6 + i
        g = examples[i] if i < len(examples) else ("", None, None)
        cell(sg, f"B{r}", g[0] or None, fill=FILL_INPUT)
        cell(sg, f"C{r}", g[1], fmt=MONEY, fill=FILL_INPUT)
        cell(sg, f"D{r}", g[2], fmt=MONEY, fill=FILL_INPUT)
        cell(sg, f"E{r}", f'=IF(C{r}="","",MAX(C{r}-D{r},0))', fmt=MONEY)
        cell(sg, f"F{r}", f'=IF(OR(C{r}="",C{r}=0),"",MIN(D{r}/C{r},1))', fmt=PCT)
        cell(sg, f"G{r}", fmt="mmm d, yyyy", fill=FILL_INPUT)
    sg.conditional_formatting.add("F6:F17", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color=ACC))

    # ---------------- DEBT PAYOFF ----------------
    dp = wb.create_sheet("Debt Payoff")
    title(dp, "Debt Payoff Tracker", "List your debts — smallest balance first (snowball) or highest rate first (avalanche)")
    for col, w in zip("BCDEFGHI", [26, 16, 12, 16, 16, 16, 14, 18]):
        dp.column_dimensions[col].width = w
    hdr(dp, 5, 2, ["Debt", "Starting Balance", "Interest %", "Min. Payment", "Paid This Year", "Remaining", "Progress", "Est. Months Left"])
    dexamples = [("Credit card", 3200, 0.229, 95, 0), ("Car loan", 9800, 0.069, 310, 0), ("Student loan", 18000, 0.049, 210, 0)]
    for i in range(10):
        r = 6 + i
        d = dexamples[i] if i < len(dexamples) else (None, None, None, None, None)
        cell(dp, f"B{r}", d[0], fill=FILL_INPUT)
        cell(dp, f"C{r}", d[1], fmt=MONEY, fill=FILL_INPUT)
        cell(dp, f"D{r}", d[2], fmt="0.0%", fill=FILL_INPUT)
        cell(dp, f"E{r}", d[3], fmt=MONEY, fill=FILL_INPUT)
        cell(dp, f"F{r}", d[4], fmt=MONEY, fill=FILL_INPUT)
        cell(dp, f"G{r}", f'=IF(C{r}="","",MAX(C{r}-F{r},0))', fmt=MONEY)
        cell(dp, f"H{r}", f'=IF(OR(C{r}="",C{r}=0),"",MIN(F{r}/C{r},1))', fmt=PCT)
        cell(dp, f"I{r}",
             f'=IF(OR(G{r}="",G{r}=0,E{r}="",E{r}=0),"",IF(D{r}=0,ROUNDUP(G{r}/E{r},0),'
             f'IF(E{r}<=G{r}*D{r}/12,"Never - raise payment",ROUNDUP(NPER(D{r}/12,-E{r},G{r}),0))))')
    cell(dp, "B16", "TOTAL", F_BOLD, fill=FILL_LIGHT)
    for col in "CEFG":
        cell(dp, f"{col}16", f"=SUM({col}6:{col}15)", F_BOLD, MONEY, FILL_LIGHT)
    cell(dp, "H16", "=IF(C16=0,0,F16/C16)", F_BOLD, PCT, FILL_LIGHT)
    dp.conditional_formatting.add("H6:H15", DataBarRule(start_type="num", start_value=0, end_type="num", end_value=1, color=ACC))

    # tab colors
    for ws in wb.worksheets:
        ws.sheet_properties.tabColor = ACC if ws.title in ("Start Here", "Dashboard", "Categories") else LINE
    wb.save(out)


if __name__ == "__main__":
    build(sys.argv[1])
    print("saved", sys.argv[1])

"""Static site generator for the free-tools website (GitHub Pages, served from /docs).

Usage: python3 site.py   (writes ../../docs)
Edit SHOP links below once the stores exist; every page's product box updates on rebuild.
"""
import os

BASE = "https://grungero.github.io/grungero/"
SITE = "Sage & Sun Tools"
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "docs")

# Fill these in when the shops are live (empty = box shows "coming soon" text without link)
SHOP = {
    "planner_kdp": "",      # Amazon link of 2027 Weekly & Monthly Planner (paperback)
    "budget_kdp": "",       # Amazon link of 2027 Budget Planner (paperback)
    "planner_etsy": "",     # Etsy listing: digital 2027 planner
    "budget_etsy": "",      # Etsy listing: budget spreadsheet
}

CSS = """
:root{--bg:#FBF8F3;--card:#fff;--ink:#2F3A33;--muted:#5E6B62;--acc:#7D9A86;--acc2:#C9825F;--line:#E3DDD3}
@media (prefers-color-scheme:dark){:root{--bg:#1C211E;--card:#262C28;--ink:#EDEAE4;--muted:#B5BDB7;--acc:#9DB9A6;--acc2:#E09B78;--line:#3A423D}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
a{color:var(--acc2)}header,main,footer{max-width:860px;margin:0 auto;padding:0 16px}
header{display:flex;justify-content:space-between;align-items:center;padding-top:18px;flex-wrap:wrap;gap:8px}
header a.logo{font-weight:700;text-decoration:none;color:var(--ink);font-size:20px}
nav a{margin-left:14px;font-size:15px;text-decoration:none;color:var(--muted)}
h1{font-size:clamp(28px,5vw,40px);line-height:1.2;margin:28px 0 8px}h2{margin-top:36px}
.lead{color:var(--muted);font-size:19px;margin-top:0}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:20px;margin:20px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}
.grid a.card{display:block;text-decoration:none;color:var(--ink);margin:0}.grid a.card:hover{border-color:var(--acc)}
label{display:block;font-weight:600;margin:12px 0 4px;font-size:15px}
input,select{width:100%;padding:10px 12px;border:1px solid var(--line);border-radius:10px;font-size:16px;background:var(--bg);color:var(--ink)}
button,.btn{display:inline-block;background:var(--acc);color:#fff;border:0;border-radius:10px;padding:12px 20px;font-size:16px;font-weight:600;cursor:pointer;text-decoration:none;margin-top:14px}
.btn.alt{background:var(--acc2)}
.row{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}
table{width:100%;border-collapse:collapse;font-size:15px}th,td{text-align:left;padding:8px;border-bottom:1px solid var(--line)}
.result{font-size:20px;font-weight:700;color:var(--acc)}
.promo{border-left:5px solid var(--acc2)}
footer{color:var(--muted);font-size:14px;padding:40px 16px}
.debt-row{display:grid;grid-template-columns:2fr 1fr 1fr 1fr auto;gap:8px;align-items:end;margin-bottom:8px}
@media (max-width:600px){.debt-row{grid-template-columns:1fr 1fr}}
.x{background:none;color:var(--muted);border:1px solid var(--line);padding:8px 12px;margin:0}
"""


def promo(kind):
    if kind == "planner":
        title, text, k1, k2 = ("Want the full 2027 planner?",
                               "Our 100-page 2027 Weekly & Monthly Planner adds goals, monthly budgets, habit trackers and 53 weekly pages.",
                               "planner_kdp", "planner_etsy")
    else:
        title, text, k1, k2 = ("Track it all year long",
                               "The 2027 Budget Planner turns this into a habit: monthly budgets, expense logs, bill tracker, savings and debt payoff pages.",
                               "budget_kdp", "budget_etsy")
    links = []
    if SHOP[k1]:
        links.append(f'<a class="btn alt" href="{SHOP[k1]}" rel="noopener">Paperback on Amazon</a>')
    if SHOP[k2]:
        links.append(f'<a class="btn" href="{SHOP[k2]}" rel="noopener">Digital version</a> ')
    cta = " ".join(links) if links else "<em>Coming soon on Amazon &amp; Etsy.</em>"
    return f'<div class="card promo"><h3 style="margin-top:0">{title}</h3><p>{text}</p>{cta}</div>'


def page(slug, title, desc, body):
    canon = BASE + ("" if slug == "index" else slug + ".html")
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="website">
<link rel="stylesheet" href="style.css"></head><body>
<header><a class="logo" href="./">{SITE}</a><nav><a href="printable-calendar-2027.html">2027 Calendar</a><a href="budget-calculator.html">Budget</a><a href="debt-payoff-calculator.html">Debt</a><a href="savings-goal-calculator.html">Savings</a></nav></header>
<main>{body}</main>
<footer>© 2026 {SITE} · Free tools for planning your time and money. Calculators are for educational purposes and are not financial advice.</footer>
</body></html>"""
    with open(os.path.join(OUT, slug + ".html"), "w") as f:
        f.write(html)
    return canon


PAGES = []

PAGES.append(page("index", "Free 2027 Calendar & Budget Tools | " + SITE,
    "Free printable 2027 calendar and simple money calculators: 50/30/20 budget, debt payoff (snowball vs avalanche) and savings goals.",
    """<h1>Free tools to plan your 2027</h1><p class="lead">Printable calendars and simple money calculators. No sign-up, no email, nothing to install.</p>
<div class="grid">
<a class="card" href="printable-calendar-2027.html"><h3>📅 2027 Printable Calendar</h3><p>Free PDF: year at a glance + 12 monthly pages.</p></a>
<a class="card" href="budget-calculator.html"><h3>💵 50/30/20 Budget Calculator</h3><p>Split your income into needs, wants and savings.</p></a>
<a class="card" href="debt-payoff-calculator.html"><h3>📉 Debt Payoff Calculator</h3><p>Snowball vs avalanche: see your debt-free date.</p></a>
<a class="card" href="savings-goal-calculator.html"><h3>🎯 Savings Goal Calculator</h3><p>How much to save each month to hit your goal.</p></a>
</div>""" + promo("planner")))

PAGES.append(page("printable-calendar-2027", "Free Printable 2027 Calendar (PDF) – Monthly & Yearly | " + SITE,
    "Download a free printable 2027 calendar PDF: year at a glance plus 12 monthly calendars, Monday start, US Letter. Color or ink-saving black & white.",
    """<h1>Free Printable 2027 Calendar</h1><p class="lead">A clean, minimalist 2027 calendar you can print at home. 13 pages: one year-at-a-glance page plus a full page for every month.</p>
<div class="card"><h3 style="margin-top:0">Download (PDF, US Letter, prints on A4)</h3>
<a class="btn" href="downloads/2027-calendar-sage.pdf" download>Sage green version</a>
<a class="btn alt" href="downloads/2027-calendar-mono.pdf" download>Ink-saving black &amp; white</a>
<p style="font-size:14px;color:var(--muted)">Free for personal use. Weeks start on Monday. Weekends are shaded.</p></div>
<h2>What's inside</h2><ul><li>2027 year at a glance</li><li>12 monthly calendars with big writing boxes</li><li>Notes &amp; priorities space on every month</li></ul>
<h2>Single months</h2><p><a href="january-2027-calendar.html">January 2027</a> · <a href="february-2027-calendar.html">February 2027</a> · <a href="march-2027-calendar.html">March 2027</a> · <a href="april-2027-calendar.html">April 2027</a> · <a href="may-2027-calendar.html">May 2027</a> · <a href="june-2027-calendar.html">June 2027</a> · <a href="july-2027-calendar.html">July 2027</a> · <a href="august-2027-calendar.html">August 2027</a> · <a href="september-2027-calendar.html">September 2027</a> · <a href="october-2027-calendar.html">October 2027</a> · <a href="november-2027-calendar.html">November 2027</a> · <a href="december-2027-calendar.html">December 2027</a></p><h2>How to print</h2><p>Open the PDF, choose <strong>Actual size</strong> (or "Fit to page" for A4) and print. You can print only the months you need.</p>""" + promo("planner")))

PAGES.append(page("budget-calculator", "50/30/20 Budget Calculator (Free) | " + SITE,
    "Free 50/30/20 budget calculator: enter your monthly take-home pay and see how much to spend on needs, wants and savings.",
    """<h1>50/30/20 Budget Calculator</h1><p class="lead">The 50/30/20 rule splits your take-home pay: 50% for needs, 30% for wants and 20% for savings and debt payoff.</p>
<div class="card"><label for="inc">Monthly take-home income ($)</label><input id="inc" type="number" min="0" step="any" value="4000" inputmode="decimal">
<div class="row"><div><label for="pn">Needs %</label><input id="pn" type="number" value="50"></div><div><label for="pw">Wants %</label><input id="pw" type="number" value="30"></div><div><label for="ps">Savings %</label><input id="ps" type="number" value="20"></div></div>
<table style="margin-top:18px"><tr><th>Category</th><th>Per month</th><th>Per year</th></tr>
<tr><td>Needs (rent, food, bills)</td><td id="n" class="result"></td><td id="ny"></td></tr>
<tr><td>Wants (fun, dining, shopping)</td><td id="w" class="result"></td><td id="wy"></td></tr>
<tr><td>Savings &amp; debt payoff</td><td id="s" class="result"></td><td id="sy"></td></tr></table><p id="warn" style="color:var(--acc2)"></p></div>
<h2>How the 50/30/20 rule works</h2><p><strong>Needs</strong> are bills you must pay: housing, utilities, groceries, insurance, minimum debt payments. <strong>Wants</strong> are everything that makes life fun but isn't essential. <strong>Savings</strong> covers your emergency fund, retirement and extra debt payments. If your needs are higher than 50%, adjust the percentages above to fit your real life.</p>
<script>
const $=id=>document.getElementById(id),f=v=>v.toLocaleString(undefined,{style:'currency',currency:'USD'});
function calc(){const i=+$('inc').value||0,p=[+$('pn').value,+$('pw').value,+$('ps').value];
[['n',0],['w',1],['s',2]].forEach(([k,j])=>{$(k).textContent=f(i*p[j]/100);$(k+'y').textContent=f(i*p[j]/100*12)});
const t=p.reduce((a,b)=>a+b,0);$('warn').textContent=t!==100?`Your percentages add up to ${t}%, not 100%.`:''}
document.querySelectorAll('input').forEach(e=>e.addEventListener('input',calc));calc();
</script>""" + promo("budget")))

PAGES.append(page("debt-payoff-calculator", "Debt Payoff Calculator: Snowball vs Avalanche (Free) | " + SITE,
    "Free debt payoff calculator. Compare the debt snowball and debt avalanche methods, see your debt-free date and total interest saved.",
    """<h1>Debt Payoff Calculator</h1><p class="lead">Compare the <strong>snowball</strong> (smallest balance first) and <strong>avalanche</strong> (highest interest first) methods and see when you'll be debt-free.</p>
<div class="card"><div id="debts"></div><button class="x" id="add" type="button">+ Add debt</button>
<label for="extra">Extra payment per month on top of minimums ($)</label><input id="extra" type="number" min="0" value="200">
<button id="go" type="button">Calculate</button><div id="out" style="margin-top:16px"></div></div>
<h2>Snowball or avalanche?</h2><p>The <strong>avalanche</strong> method usually saves the most interest. The <strong>snowball</strong> method gives quick wins by clearing small debts first, which helps many people stay motivated. Either way, paying a fixed extra amount every month is what gets you out of debt.</p>
<script>
const D=document.getElementById('debts');
function row(n='',b='',r='',m=''){const d=document.createElement('div');d.className='debt-row';
d.innerHTML=`<div><label>Debt name</label><input value="${n}"></div><div><label>Balance $</label><input type="number" value="${b}"></div><div><label>Rate %</label><input type="number" step="any" value="${r}"></div><div><label>Min. payment $</label><input type="number" value="${m}"></div><button class="x" type="button" aria-label="Remove">✕</button>`;
d.querySelector('button').onclick=()=>d.remove();D.appendChild(d)}
row('Credit card',6500,22.9,160);row('Medical bill',1200,0,50);row('Car loan',9800,6.9,310);
document.getElementById('add').onclick=()=>row();
function sim(debts,extra,order){debts=debts.map(d=>({...d}));let month=0,interest=0;const budget=debts.reduce((a,d)=>a+d.min,0)+extra;
while(debts.some(d=>d.bal>0.005)&&month<600){month++;let pay=budget;
debts.forEach(d=>{if(d.bal>0){const i=d.bal*d.rate/1200;d.bal+=i;interest+=i}});
debts.filter(d=>d.bal>0).forEach(d=>{const p=Math.min(d.min,d.bal);d.bal-=p;pay-=p});
debts.filter(d=>d.bal>0).sort(order).forEach(d=>{const p=Math.min(pay,d.bal);d.bal-=p;pay-=p})}
return{month,interest}}
const f=v=>v.toLocaleString(undefined,{style:'currency',currency:'USD',maximumFractionDigits:0});
function when(m){const d=new Date();d.setMonth(d.getMonth()+m);return d.toLocaleDateString(undefined,{month:'long',year:'numeric'})}
document.getElementById('go').onclick=()=>{const debts=[...D.children].map(r=>{const v=[...r.querySelectorAll('input')].map(i=>i.value);return{name:v[0],bal:+v[1]||0,rate:+v[2]||0,min:+v[3]||0}}).filter(d=>d.bal>0);
const extra=+document.getElementById('extra').value||0;const out=document.getElementById('out');
if(!debts.length){out.textContent='Add at least one debt.';return}
const sn=sim(debts,extra,(a,b)=>a.bal-b.bal),av=sim(debts,extra,(a,b)=>b.rate-a.rate);
if(sn.month>=600){out.innerHTML='<p>With these payments the debt never gets paid off. Try a higher extra payment.</p>';return}
out.innerHTML=`<table><tr><th>Method</th><th>Debt-free in</th><th>Debt-free by</th><th>Total interest</th></tr>
<tr><td>Snowball</td><td>${sn.month} months</td><td>${when(sn.month)}</td><td>${f(sn.interest)}</td></tr>
<tr><td>Avalanche</td><td>${av.month} months</td><td>${when(av.month)}</td><td>${f(av.interest)}</td></tr></table>
<p class="result">Avalanche saves you ${f(Math.max(sn.interest-av.interest,0))} in interest.</p>`};
document.getElementById('go').click();
</script>""" + promo("budget")))

PAGES.append(page("savings-goal-calculator", "Savings Goal Calculator – How Much to Save per Month | " + SITE,
    "Free savings goal calculator: find out how much you need to save each month to reach your goal by a target date, with optional interest.",
    """<h1>Savings Goal Calculator</h1><p class="lead">Find out how much to put aside every month to reach your goal on time.</p>
<div class="card"><div class="row"><div><label for="g">Goal amount ($)</label><input id="g" type="number" value="6000"></div>
<div><label for="h">Already saved ($)</label><input id="h" type="number" value="500"></div>
<div><label for="m">Months to reach it</label><input id="m" type="number" min="1" value="12"></div>
<div><label for="r">Interest rate (APY %)</label><input id="r" type="number" step="any" value="4"></div></div>
<p>Save <span id="res" class="result"></span> per month <span id="wk" style="color:var(--muted)"></span></p></div>
<h2>Tips to reach your savings goal faster</h2><ul><li>Automate a transfer on payday so saving happens first.</li><li>Keep goal money in a separate high-yield savings account.</li><li>Use a sinking fund for each big expense (holidays, car repairs, travel).</li></ul>
<script>
const $=id=>document.getElementById(id),f=v=>v.toLocaleString(undefined,{style:'currency',currency:'USD'});
function calc(){const g=+$('g').value||0,h=+$('h').value||0,n=Math.max(1,+$('m').value||1),r=(+$('r').value||0)/1200;
const need=g-h*Math.pow(1+r,n);let p=r>0?need*r/(Math.pow(1+r,n)-1):need/n;p=Math.max(p,0);
$('res').textContent=f(p);$('wk').textContent=`(about ${f(p*12/52)} per week)`}
document.querySelectorAll('input').forEach(e=>e.addEventListener('input',calc));calc();
</script>""" + promo("budget")))


# ---------- monthly calendar pages (SEO: "<month> 2027 calendar") ----------
import calendar as _cal
import datetime as _dt

_cal.setfirstweekday(_cal.SUNDAY)  # US readers expect Sunday-first in HTML view


def _nth(year, month, weekday, n):
    d = _dt.date(year, month, 1)
    d += _dt.timedelta(days=(weekday - d.weekday()) % 7)
    if n > 0:
        return d + _dt.timedelta(weeks=n - 1)
    last = _dt.date(year, month, _cal.monthrange(year, month)[1])
    return last - _dt.timedelta(days=(last.weekday() - weekday) % 7)


def _easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    mo = (h + l - 7 * m + 114) // 31
    return _dt.date(y, mo, ((h + l - 7 * m + 114) % 31) + 1)


Y = 2027
HOLIDAYS = {
    _dt.date(Y, 1, 1): "New Year's Day", _nth(Y, 1, 0, 3): "Martin Luther King Jr. Day",
    _dt.date(Y, 2, 14): "Valentine's Day", _nth(Y, 2, 0, 3): "Presidents' Day",
    _dt.date(Y, 3, 17): "St. Patrick's Day", _easter(Y): "Easter Sunday",
    _nth(Y, 5, 6, 2): "Mother's Day", _nth(Y, 5, 0, -1): "Memorial Day",
    _dt.date(Y, 6, 19): "Juneteenth", _nth(Y, 6, 6, 3): "Father's Day",
    _dt.date(Y, 7, 4): "Independence Day", _nth(Y, 9, 0, 1): "Labor Day",
    _nth(Y, 10, 0, 2): "Columbus / Indigenous Peoples' Day", _dt.date(Y, 10, 31): "Halloween",
    _dt.date(Y, 11, 11): "Veterans Day", _nth(Y, 11, 3, 4): "Thanksgiving",
    _dt.date(Y, 12, 24): "Christmas Eve", _dt.date(Y, 12, 25): "Christmas Day", _dt.date(Y, 12, 31): "New Year's Eve",
}
MONTH_NAMES = list(_cal.month_name)[1:]
MONTH_CSS = """<style>.cal{table-layout:fixed}.cal th{text-align:center;color:var(--muted);font-size:13px}.cal td{height:64px;vertical-align:top;border:1px solid var(--line);font-weight:600;padding:6px}
.cal td.h{background:color-mix(in srgb,var(--acc2) 18%,transparent)}.cal small{display:block;overflow-wrap:anywhere;font-weight:400;font-size:11px;line-height:1.2;color:var(--acc2)}
.months{display:flex;flex-wrap:wrap;gap:8px}.months a{padding:6px 10px;border:1px solid var(--line);border-radius:8px;text-decoration:none;font-size:14px}</style>"""


def month_page(m):
    name = MONTH_NAMES[m - 1]
    slug = f"{name.lower()}-2027-calendar"
    rows = []
    for week in _cal.monthcalendar(Y, m):
        cells = []
        for d in week:
            if not d:
                cells.append("<td></td>")
                continue
            h = HOLIDAYS.get(_dt.date(Y, m, d))
            cells.append(f'<td class="h">{d}<small>{h}</small></td>' if h else f"<td>{d}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    hol = [f"<li><strong>{d:%A, %B %-d}</strong>: {n}</li>" for d, n in sorted(HOLIDAYS.items()) if d.month == m]
    hol_html = ("<h2>Holidays &amp; observances in " + name + " 2027 (US)</h2><ul>" + "".join(hol) + "</ul>") if hol else ""
    prev_m, next_m = MONTH_NAMES[(m - 2) % 12], MONTH_NAMES[m % 12]
    nav = '<div class="months">' + "".join(
        f'<a href="{n.lower()}-2027-calendar.html">{n[:3]}</a>' for n in MONTH_NAMES) + "</div>"
    body = f"""{MONTH_CSS}<h1>{name} 2027 Calendar</h1>
<p class="lead">Free printable {name} 2027 calendar with US holidays. Download the PDF or view it below.</p>
<div class="card"><a class="btn" href="downloads/{name.lower()}-2027-calendar.pdf" download>Download {name} 2027 PDF</a>
<a class="btn alt" href="printable-calendar-2027.html">Full 2027 calendar (all months)</a></div>
<table class="cal"><tr>{''.join(f'<th>{d}</th>' for d in ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'])}</tr>{''.join(rows)}</table>
<p style="font-size:14px;color:var(--muted)">{name} 2027 has {_cal.monthrange(Y, m)[1]} days and starts on a {_dt.date(Y, m, 1):%A}. The PDF version uses a Monday start with large writing boxes.</p>
{hol_html}<h2>Other months</h2>{nav}
<p><a href="{prev_m.lower()}-2027-calendar.html">← {prev_m} 2027</a> · <a href="{next_m.lower()}-2027-calendar.html">{next_m} 2027 →</a></p>""" + promo("planner")
    return page(slug, f"{name} 2027 Calendar – Free Printable PDF with Holidays | {SITE}",
                f"Free printable {name} 2027 calendar with US holidays. Download a clean PDF (US Letter, prints on A4) or view the {name} 2027 calendar online.",
                body)


for _m in range(1, 13):
    PAGES.append(month_page(_m))


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "style.css"), "w") as f:
        f.write(CSS)
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n")
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in PAGES:
            f.write(f"  <url><loc>{u}</loc></url>\n")
        f.write("</urlset>\n")
    print("site written to", os.path.abspath(OUT), len(PAGES), "pages")


if __name__ == "__main__":
    main()

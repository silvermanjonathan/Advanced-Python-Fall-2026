"""Session 1 worksheet: a printed page for tracing the two loops by hand."""

from build import code, esc, masthead, pager

WS_CSS = """
<style>
header.top .sub:empty{display:none}
.ws-name{display:flex; gap:24px; flex-wrap:wrap; font-size:17px; margin:0 0 6px}
.ws-name span{flex:1 1 220px; border-bottom:2px solid var(--ink); padding:0 0 4px}
.ws-name b{font-family:'JetBrains Mono',monospace; font-size:12.5px; letter-spacing:.1em;
  text-transform:uppercase; color:var(--ochre); margin-right:8px}
.lines p{border-bottom:2px solid var(--rule); min-height:34px; margin:0 0 10px; padding:0 0 2px}
.key{background:var(--green-tint); color:var(--green-ink)}
.lines p.key{min-height:0; padding:8px 10px; border-bottom:0; border-left:4px solid var(--green)}
table.trace tr.done td{}
table.trace{table-layout:fixed}
table.trace th{font-family:'JetBrains Mono',monospace; text-align:center; font-size:14.5px;
  padding:6px 3px; white-space:normal; overflow-wrap:normal}
table.trace td{height:36px; text-align:center; font-family:'JetBrains Mono',monospace; font-size:15px}
table.trace td.i{background:#EFE9DA; font-weight:700}
table.trace tr.start td{background:#FBF9F3; color:var(--ink-soft)}
table.trace tr.done td{background:#E8F1E9; color:var(--green-ink)}
table.trace tr.done td.i{background:#D9E7DC}
table.trace tr.done td.q{background:#E8F1E9}
table.trace th.q,table.trace td.q{background:#FBF2DC}
table.rename td{height:38px}
table.rename td.old{font-family:'JetBrains Mono',monospace; font-weight:700; width:130px; text-align:center;
  background:#EFE9DA; white-space:nowrap}
.two-up{display:grid; gap:18px; grid-template-columns:1fr}
@media(min-width:760px){.two-up{grid-template-columns:1fr 1fr}}
.two-up pre{margin:0; font-size:14px; line-height:1.5}
.nb{font-size:15px; color:var(--ink-soft)}
.checks p{display:flex; gap:12px; align-items:flex-start; margin:0 0 12px; max-width:none}
.checks .box{flex:0 0 auto; width:22px; height:22px; border:2px solid var(--ink); border-radius:3px;
  margin-top:3px}
@media print{
  @page{size:letter; margin:14mm 14mm 16mm}
  body{font-size:12pt; line-height:1.5} main{padding:0}
  header.top{padding:8px 0 6px; margin-bottom:10px}
  header.top .dates,header.top .sub{display:none}
  .ws-name{font-size:12pt; margin:0 0 10px}
  section{padding:14px 16px; margin:0 0 12px; border-width:1.5px}
  pre,tr,p,.lines p{break-inside:avoid} h2,h3,.chunk-no{break-after:avoid}
  pre{white-space:pre-wrap; overflow-wrap:anywhere}
  thead{display:table-header-group} .keep{break-inside:avoid} table.trace,table.rename{break-inside:avoid}
  .two-up{grid-template-columns:1fr; gap:12px}
  .chunk-no{margin:0 0 4px; font-size:9.5pt} h2{font-size:19pt; margin:0 0 8px} h3{font-size:14pt}
  main section:nth-of-type(4){break-before:page}
  table{font-size:12pt} table.trace th{font-size:10.5pt} table.trace td{height:34px; font-size:12pt}
  table.rename td{height:42px} .lines p{min-height:32px; margin:0 0 12px}
  .nb{font-size:11.5pt} code{font-size:.92em}
  .checks p{margin:0 0 10px} .checks .box{border-color:#111}
  .two-up pre{font-size:10.5pt; line-height:1.5; border:1px solid #999}
  .ws-name span{border-bottom-color:#111}
}
</style>
"""

FIRST_HALF = """readings = [41, 58, 33, 58, 12, 77, 58, 60, 29, 77]
limit = 55

t = 0
c = 0
b = 0
bi = 0

for i in range(10):
    r = readings[i]

    t = t + r

    if r > limit:
        c = c + 1

    if r > b:
        b = r
        bi = i

avg = t / 10

print(f"total {t}")
print(f"average {avg}")
print(f"over {limit}: {c}")
print(f"best {b} at index {bi}")"""

SECOND_HALF = """slot = 0
for i in range(10):
    slot = (slot + readings[i]) % 9
    print(f"i={i} reading={readings[i]} slot={slot}")"""

GATE_LOG = """door = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0]

x = 0
y = 0
z = 0
q = 0

for i in range(12):
    d = door[i]

    if d == 1:
        x = x + 1
        z = z + 1

    if d == 0:
        y = y + 1
        z = 0

    if z > q:
        q = z

print(f"x {x}")
print(f"y {y}")
print(f"z {z}")
print(f"q {q}")"""

READINGS = [41, 58, 33, 58, 12, 77, 58, 60, 29, 77]
DOORS = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0]
LIMIT = 55


def first_half_rows():
    """Return every row of the first-half trace, computed the way the program does."""
    rows = {}
    t = c = b = bi = 0
    for i in range(10):
        r = READINGS[i]
        t = t + r
        over = r > LIMIT
        if over:
            c = c + 1
        beats = r > b
        if beats:
            b = r
            bi = i
        rows[i] = [i, r, t, "yes" if over else "no", c, "yes" if beats else "no", b, bi]
    return rows


def gate_log_rows():
    """Return every row of the door trace, computed the way gate_log.py does."""
    rows = {}
    x = y = z = q = 0
    for i in range(12):
        d = DOORS[i]
        if d == 1:
            x = x + 1
            z = z + 1
        if d == 0:
            y = y + 1
            z = 0
        if z > q:
            q = z
        rows[i] = [i, d, x, y, z, q]
    return rows


def second_half_rows():
    """Return every row of the wrap-loop trace."""
    rows = {}
    slot = 0
    for i in range(10):
        before = slot + READINGS[i]
        slot = before % 9
        rows[i] = [i, READINGS[i], before, slot]
    return rows


KEY = {"on": False}


def lines(n, answer=None):
    """Return n ruled writing lines, or the answer in the key version."""
    if KEY["on"] and answer:
        return f'<div class="lines"><p class="key">{answer}</p></div>'
    return '<div class="lines">' + "<p></p>" * n + "</div>"


def trace_table(headers, start, rows, given, q_cols=(), done=None):
    """Return a hand-trace table.

    headers: column names. start: values for the row before the loop, or None.
    rows: list of index values. given: dict column -> function(i) for cells the
    worksheet fills in for the student. q_cols: columns tinted as yes/no questions.
    """
    out = '<table class="trace"><thead><tr>'
    for h in headers:
        cls = ' class="q"' if h in q_cols else ""
        out += f"<th{cls}>{esc(h)}</th>"
    out += "</tr></thead>"
    if start is not None:
        out += '<tr class="start">'
        for h, v in zip(headers, start):
            out += f"<td>{esc(str(v))}</td>"
        out += "</tr>"
    done = done or {}
    for i in rows:
        if i in done:
            out += '<tr class="done">'
            for h, v in zip(headers, done[i]):
                cls = ' class="i"' if h == "i" else (' class="q"' if h in q_cols else "")
                out += f"<td{cls}>{esc(str(v))}</td>"
            out += "</tr>"
            continue
        out += "<tr>"
        for h in headers:
            if h == "i":
                out += f'<td class="i">{i}</td>'
            elif h in given:
                out += f"<td>{esc(str(given[h](i)))}</td>"
            elif h in q_cols:
                out += '<td class="q"></td>'
            else:
                out += "<td></td>"
        out += "</tr>"
    return out + "</table>"


def rename_table(names, answers=None):
    """Return the three-column rename table, filled in for the key version."""
    out = ('<table class="rename"><tr><th>Old name</th><th>What the value is, in words</th>'
           "<th>Clearer new name</th></tr>")
    for n in names:
        if KEY["on"] and answers and n in answers:
            what, new = answers[n]
            out += (f'<tr><td class="old">{esc(n)}</td><td class="key">{esc(what)}</td>'
                    f'<td class="key"><code>{esc(new)}</code></td></tr>')
        else:
            out += f'<tr><td class="old">{esc(n)}</td><td></td><td></td></tr>'
    return out + "</table>"


def run_table(rows):
    """Return the predicted-against-printed table; the key shows what prints."""
    out = ('<table class="rename"><tr><th>Line</th><th>What I predicted</th>'
           "<th>What it printed</th><th>Right?</th></tr>")
    for label, printed in rows:
        cell = f'<td class="key"><code>{esc(printed)}</code></td>' if KEY["on"] else "<td></td>"
        out += f'<tr><td class="old">{esc(label)}</td><td></td>{cell}<td></td></tr>'
    return out + "</table>"


RENAMES_1 = {
    "t": ("the running total of all the readings", "total"),
    "c": ("how many readings were over the limit", "over_limit"),
    "b": ("the largest reading seen so far", "best"),
    "bi": ("the index of the first largest reading", "first_best_index"),
    "r": ("the reading being looked at on this pass", "reading"),
    "avg": ("the average reading", "average"),
    "i": ("the index of this pass, 0 to 9", "i"),
}
RENAMES_2 = {
    "x": ("how many doors were open", "open_count"),
    "y": ("how many doors were shut", "shut_count"),
    "z": ("how many open doors in a row, right now; goes back to 0 at a shut door", "open_run_so_far"),
    "q": ("the longest run of open doors seen anywhere", "longest_open_run"),
}


def worksheet01_key():
    """Return the teacher's answer key: the worksheet with every slot filled."""
    KEY["on"] = True
    try:
        return worksheet01()
    finally:
        KEY["on"] = False


def worksheet01():
    """Return the session 1 worksheet body."""
    b = masthead(
        "01",
        "Answer key: trace it before you run it" if KEY["on"] else "Worksheet: trace it before you run it",
        "Wednesday 16 September 2026",
        "",
    )
    b += (
        ('<div class="ws-name"><span><b>Teacher copy</b> every slot filled; worked rows the '
         'students get are the same values</span><span><b>Date</b> 16 September 2026</span></div>'
         if KEY["on"] else
         '<div class="ws-name"><span><b>Name</b></span><span><b>Date</b> 16 September 2026'
         "</span></div>")
    )

    b += (
        '<div class="toolbar"><a class="btn quiet" href="wed01_cold_read.html">Back to '
        'the session 1 page</a>'
        + ("" if KEY["on"] else '<a class="btn" href="wed01_worksheet.pdf" download>Download this worksheet (PDF)</a>')
        + "</div>"
    )
    b += '<h2><span class="num">1</span>Opener<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>One line each. What does the line do? If you are not sure, write that.</p>"
        '<p class="nb"><code>for i in range(10):</code></p>'
        + lines(1, "Runs the indented lines below it ten times, with i set to 0, then 1, and so on up to 9.")
        + '<p class="nb"><code>total = total + r</code></p>'
        + lines(1, "Adds r onto the running total and stores the new total back in total.")
        + '<p class="nb"><code>if r &gt; best:</code></p>'
        + lines(1, "A gate. The indented lines below it run only when r is strictly greater than best.")
        + '<p class="nb"><code>slot = (slot + 5) % 9</code></p>'
        + lines(1, "Adds 5 to slot, divides by 9, and keeps the remainder, so slot is always 0 to 8.")
    )

    b += '<h2><span class="num">2</span>The cold read<span class="mins">25 minutes</span></h2>'
    b += "<h3>The first half</h3>"
    b += (
        "<p>Read the program. Then fill the table one row per pass through the loop. "
        "The top row shows the values before the loop starts. In the two tinted columns "
        "write <b>yes</b> or <b>no</b>: did the gate open on this pass? Three rows are "
        "done for you, shaded, so you can check your working against them as you go. "
        "The rows in between are yours.</p>"
        '<div class="two-up">'
        + code(FIRST_HALF, "sweep_report.py, first half")
        + "<div>"
        + trace_table(
            ["i", "r", "t", "r > limit?", "c", "r > b?", "b", "bi"],
            ["start", "", 0, "", 0, "", 0, 0],
            range(10),
            {"r": lambda i: READINGS[i]},
            q_cols=("r > limit?", "r > b?"),
            done={i: v for i, v in first_half_rows().items() if KEY["on"] or i in (0, 3, 7)},
        )
        + "</div></div>"
        "<p>Now write the four lines the program will print.</p>"
        '<p class="nb"><code>total</code></p>' + lines(1, "total 503")
        + '<p class="nb"><code>average</code></p>' + lines(1, "average 50.3")
        + '<p class="nb"><code>over 55:</code></p>' + lines(1, "over 55: 6")
        + '<p class="nb"><code>best ... at index ...</code></p>' + lines(1, "best 77 at index 5")
        + '<div class="keep">' + "<p>The list holds 77 twice, at index 5 and at index 9, and the fourth line "
        "names only one of them. The gate <code>if r &gt; b:</code> decides which. "
        "Circle the one character in that gate that makes the comparison, then write one "
        "sentence: when the second 77 arrives, will the gate say yes or no, and why?</p>"
        + lines(2, "The character is the &gt; in <code>if r &gt; b:</code>. No. When the second 77 arrives, b is already 77, and 77 is not greater than 77, so the gate stays shut and bi stays 5. With &gt;= the gate would open and bi would become 9.")
        + "</div>"
    )

    b += "<h3>The second half</h3>"
    b += (
        "<p><code>%</code> gives the remainder after dividing. <code>41 % 9</code> is 5, "
        "because 41 is four nines with 5 left over. Work the middle column first, then "
        "take the remainder. Rows 3, 6, and 9 are done for you, shaded. The first three "
        "rows are required, and row 3 is there to check yourself against. Finish the rest "
        "if you have time.</p>"
        '<div class="two-up">'
        + code(SECOND_HALF, "sweep_report.py, second half")
        + "<div>"
        + trace_table(
            ["i", "reading", "slot + reading", "% 9 = slot"],
            ["start", "", "", 0],
            range(10),
            {"reading": lambda i: READINGS[i]},
            done={i: v for i, v in second_half_rows().items() if KEY["on"] or i in (3, 6, 9)},
        )
        + "</div></div>"
        "<p>Rows 1 and 3 both have a reading of 58. Do they land on the same slot? Say "
        "why or why not in one sentence.</p>"
        + lines(2, "No. Row 1 lands on slot 0: slot was 5 after row 0, and 5 + 58 = 63, which is seven nines exactly. Row 3 lands on slot 1: slot was 6 after row 2, and 6 + 58 = 64, remainder 1. The reading is the same but slot carries in what it was before, so the same reading can land in different slots.")
    )

    b += '<h2><span class="num">3</span>Run it<span class="mins">10 minutes</span></h2>'
    b += (
        "<p>Now run the program. Copy the real output next to your prediction. Mark "
        "each line right or wrong. Do not erase a wrong prediction.</p>"
        + run_table([
            ("total", "total 503"), ("average", "average 50.3"),
            ("over 55", "over 55: 6"), ("best", "best 77 at index 5"),
            ("slot, i=0 to 2", "5, 0, 6"),
        ])
    )

    b += '<h2><span class="num">4</span>The style pass<span class="mins">30 minutes</span></h2>'
    b += (
        "<p>The program works and it is hard to read. Rename every short name so the "
        "name says what the value is. Yours does not have to match anyone else's. It "
        "has to be a name the next reader understands without scrolling back up.</p>"
        + rename_table(["t", "c", "b", "bi", "r", "avg", "i"], RENAMES_1)
        + "<p>Then the docstring. A docstring is one sentence, inside triple quotes, on "
        "line 1 of the file, saying what the program is for. Python ignores it. The next "
        "reader does not. Here is one for this program:</p>"
        + code('''"""Summarize a run of tower readings and report where the strongest one sat."""''', "line 1 of sweep_report.py")
        + "<p>Copy it onto line 1 of your file. If you would rather say it your own way, "
        "write your sentence here first, then type it between the quotes:</p>"
        + lines(1, "Any one sentence that says what the program is for. The example on the page is fine to copy.")
    )
    b += "<h3>A second one, harder</h3>"
    b += (
        "<p>This program walks along a corridor of doors, where 1 means open and 0 "
        "means shut. Trace all four variables, then name them. A hint: every one of the "
        "four variables is counting something about the doors, so every new name should have the "
        "word door or open or shut in it. Watch the <code>z</code> column as you fill it "
        "in. It climbs and drops back to 0, and the name has to say why. Rows 1, 5, and 9 "
        "are done for you, shaded, to check against. One of the four variables is much "
        "harder to name than the others.</p>"
        '<div class="toolbar"><a class="btn quiet" href="wed01_doors_trace.html">Watch '
        "this table fill in, one gate at a time</a></div>"
        '<div class="two-up">'
        + code(GATE_LOG, "gate_log.py")
        + "<div>"
        + trace_table(
            ["i", "d", "x", "y", "z", "q"],
            ["start", "", 0, 0, 0, 0],
            range(12),
            {"d": lambda i: DOORS[i]},
            done={i: v for i, v in gate_log_rows().items() if KEY["on"] or i in (1, 5, 9)},
        )
        + "</div></div>"
        + rename_table(["x", "y", "z", "q"], RENAMES_2)
        + '<div class="keep"><p>Which of the four variables was hardest to name, and why?</p>'
        + lines(2, "z. It prints 0 at the end, which looks like a counter that never worked. It is right: z counts the current run of open doors and the last door was shut, so the run so far is 0. A name like open_run_so_far makes the 0 look right. q keeps the biggest value z ever reached, which is why q ends at 3.")
        + "</div>"
    )

    b += pager(
        ("wed01_cold_read.html", "Session 1: the page"),
        ("wed02_return_and_modules.html", "Session 2: functions that return a value"),
    )
    return b

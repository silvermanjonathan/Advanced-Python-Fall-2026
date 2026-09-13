"""Generate the Advanced Python GitHub Pages site.

Flat repo, inline CSS and JS, hub as homepage, no index.html.
"""

import html
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))
# Shipped layout: build/ sits inside the repo and pages go to the repo root.
# Dev layout: pages go to ./site next to this file.
OUT = os.path.join(_HERE, "site") if os.path.isdir(os.path.join(_HERE, "site")) \
    else os.path.dirname(_HERE)

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?'
    "family=Archivo:wght@400;500;600&"
    "family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&"
    "family=JetBrains+Mono:wght@400;700&display=swap\" rel=\"stylesheet\">"
)

CSS = """
:root{
  --paper:#F1F3F2; --ink:#15303C; --soft:#4A6472; --rule:#BFCBCE;
  --signal:#0E6B62; --predict:#8A5A00; --verified:#185E3B; --fault:#8C2B18;
  --code-bg:#0E2430; --code-fg:#DCE6E4; --panel:#E4E9E8;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:Archivo,system-ui,sans-serif; font-size:19px; line-height:1.6;
}
.wrap{max-width:1000px; margin:0 auto; padding:0 28px 90px}
p,li{max-width:68ch}
h1,h2,h3{font-family:"Bricolage Grotesque",Archivo,sans-serif; line-height:1.12; margin:0}
a{color:var(--signal)}
a:focus-visible,button:focus-visible{outline:3px solid var(--signal); outline-offset:3px}

/* masthead */
.top{border-bottom:2px solid var(--ink); padding:22px 0 14px; margin-bottom:34px}
.top .course{font-size:.8rem; letter-spacing:.06em; color:var(--soft); font-weight:600}
.top .bar{display:flex; gap:22px; align-items:baseline; flex-wrap:wrap; margin-top:6px}
.serial{font-family:"Bricolage Grotesque",sans-serif; font-weight:700; font-size:3.6rem;
  line-height:.85; color:var(--signal)}
.top h1{font-size:2.1rem; font-weight:700; flex:1 1 340px}
.when{font-family:"JetBrains Mono",monospace; font-size:.85rem; color:var(--soft);
  max-width:none}

/* blocks */
h2{font-size:1.5rem; font-weight:700; margin:48px 0 4px; padding-top:18px;
  border-top:1px solid var(--rule)}
.top + h2, .top + .flag + h2{border-top:0; padding-top:0; margin-top:30px}
h2 .num{color:var(--signal); font-weight:500; margin-right:.5em}
h3{font-size:1.12rem; font-weight:600; margin:28px 0 6px}
.lede{font-size:1.2rem; color:var(--soft); max-width:62ch; margin:10px 0 0}
.mins{font-family:"JetBrains Mono",monospace; font-size:.78rem; color:var(--soft);
  display:block; margin-top:2px}

pre{background:var(--code-bg); color:var(--code-fg); padding:18px 20px; overflow-x:auto;
  font-family:"JetBrains Mono",monospace; font-size:16px; line-height:1.5;
  border-radius:3px; margin:16px 0}
code{font-family:"JetBrains Mono",monospace; font-size:.92em;
  background:var(--panel); padding:1px 5px; border-radius:2px}
pre code{background:none; padding:0; font-size:inherit}
.fname{font-family:"JetBrains Mono",monospace; font-size:.78rem; color:var(--soft);
  margin:16px 0 -10px}

.predict{border-left:4px solid var(--predict); background:#F7F2E6; padding:14px 18px; margin:18px 0}
.predict b{color:var(--predict)}
.out{border-left:4px solid var(--verified); background:#EAF1EC; padding:6px 18px; margin:14px 0}
.out .tag{font-family:"JetBrains Mono",monospace; font-size:.72rem; color:var(--verified);
  font-weight:700; display:block; margin:10px 0 -6px}
.bug{border-left:4px solid var(--fault); background:#F7EBE8; padding:14px 18px; margin:18px 0}
.bug b{color:var(--fault)}

button.rev{font:600 .9rem Archivo,sans-serif; background:var(--signal); color:#fff;
  border:0; padding:9px 16px; border-radius:3px; cursor:pointer; margin:6px 0}
button.rev:hover{background:#0b544d}
.ans{display:none; border-left:4px solid var(--signal); background:#E6EFEE;
  padding:14px 18px; margin:6px 0 18px}
.ans.show{display:block}

table{border-collapse:collapse; width:100%; margin:18px 0; font-size:.92rem}
th,td{border-bottom:1px solid var(--rule); padding:8px 10px; text-align:left;
  vertical-align:top; overflow-wrap:anywhere}
th{font-weight:600; background:var(--panel)}
td code{font-size:.86em}

.exits{margin:22px 0}
.exit{border-top:1px solid var(--rule); padding:12px 0}
.exit .lab{font-family:"JetBrains Mono",monospace; font-size:.76rem; font-weight:700;
  color:var(--signal)}
.exit p{margin:3px 0 0}

.panel{background:var(--panel); border-top:3px solid var(--ink); padding:22px 24px; margin:52px 0 0}
.panel h2{border:0; margin:0 0 10px; padding:0; font-size:1.3rem}
.panel h3{margin:20px 0 4px; font-size:1rem}
.panel p,.panel li{max-width:74ch; font-size:.95rem}
.std{font-family:"JetBrains Mono",monospace; font-weight:700; color:var(--signal)}
.mapnote{font-size:.82rem; color:var(--soft); margin-top:14px}

nav.pager{display:flex; justify-content:space-between; gap:16px; flex-wrap:wrap;
  border-top:2px solid var(--ink); margin-top:46px; padding-top:16px; font-weight:600}
nav.pager a{text-decoration:none}
nav.pager .none{color:var(--rule)}

/* hub */
.grid{border-top:2px solid var(--ink); margin:30px 0 0}
.row{display:grid; grid-template-columns:48px 76px 1fr; gap:16px;
  border-bottom:1px solid var(--rule); padding:14px 0; align-items:baseline}
.row .n{font-family:"Bricolage Grotesque",sans-serif; font-weight:700; font-size:1.5rem;
  color:var(--signal)}
.row .d{font-family:"JetBrains Mono",monospace; font-size:.82rem; color:var(--soft)}
.row .t{font-weight:600; font-size:1.05rem}
.row .t a{text-decoration:none}
.row .s{display:block; font-weight:400; font-size:.92rem; color:var(--soft); max-width:62ch}
.row.off{opacity:.55}
.row.off .n{color:var(--soft)}
.flag{background:#F7F2E6; border-left:4px solid var(--predict); padding:14px 18px; margin:22px 0}
ul.tight{margin:8px 0; padding-left:22px}
ul.tight li{margin:3px 0}
.two{display:grid; grid-template-columns:1fr 1fr; gap:0 34px}
@media (max-width:760px){
  body{font-size:17px} .wrap{padding:0 18px 70px}
  .serial{font-size:2.6rem} .top h1{font-size:1.6rem}
  .row{grid-template-columns:38px 1fr; gap:6px 12px}
  .row .d{grid-column:2} .row .t{grid-column:2} .two{grid-template-columns:1fr}
  table{table-layout:fixed} th,td{padding:7px 8px}
}
@media print{
  body{background:#fff; font-size:11pt} button.rev{display:none}
  .ans{display:block} nav.pager{display:none} pre{border:1px solid #999}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important; animation:none!important}}
"""

JS = """
document.addEventListener('click', function(e){
  var b = e.target.closest('button.rev');
  if(!b) return;
  var box = document.getElementById(b.dataset.target);
  if(!box) return;
  var open = box.classList.toggle('show');
  b.textContent = open ? (b.dataset.hide || 'Hide') : (b.dataset.show || 'Show');
  b.setAttribute('aria-expanded', open ? 'true' : 'false');
});
"""


def esc(s):
    """Escape text for HTML."""
    return html.escape(s, quote=False)


def code(text, fname=None):
    """Return a code block with angle brackets escaped."""
    out = ""
    if fname:
        out += f'<p class="fname">{esc(fname)}</p>\n'
    out += "<pre><code>" + html.escape(text.rstrip("\n")) + "</code></pre>\n"
    return out


def output(text, label="verified output"):
    """Return a verified-output block."""
    return (
        f'<div class="out"><span class="tag">{esc(label)}</span>'
        "<pre><code>" + html.escape(text.rstrip("\n")) + "</code></pre></div>\n"
    )


_rev = [0]


def reveal(question, answer, show="Show the answer", hide="Hide the answer"):
    """Return a predict box plus a reveal button and hidden answer."""
    _rev[0] += 1
    rid = f"a{_rev[0]}"
    return (
        f'<div class="predict"><b>Predict first.</b> {question}</div>\n'
        f'<button class="rev" data-target="{rid}" data-show="{esc(show)}" '
        f'data-hide="{esc(hide)}" aria-expanded="false" aria-controls="{rid}">{esc(show)}</button>\n'
        f'<div class="ans" id="{rid}">{answer}</div>\n'
    )


def page(filename, title, body, head_extra=""):
    """Write one self-contained page."""
    doc = (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{esc(title)}</title>\n{FONTS}\n<style>{CSS}</style>\n{head_extra}"
        "</head>\n<body>\n<div class=\"wrap\">\n"
        f"{body}\n</div>\n<script>{JS}</script>\n</body>\n</html>\n"
    )
    path = os.path.join(OUT, filename)
    with open(path, "w") as f:
        f.write(doc)
    return path


def masthead(serial, title, when, lede):
    """Return the page masthead."""
    s = f'<div class="serial">{esc(serial)}</div>' if serial else ""
    return (
        '<header class="top"><div class="course">Advanced Python &middot; '
        "Wednesdays 4:00 to 5:30 &middot; Robofun, 110 West End Avenue</div>"
        f'<div class="bar">{s}<h1>{esc(title)}</h1></div>'
        f'<p class="when">{esc(when)}</p>'
        f'<p class="lede">{esc(lede)}</p></header>\n'
    )


def pager(prev, nxt):
    """Return the previous/next/hub navigation."""
    p = (
        f'<a href="{prev[0]}">&larr; {esc(prev[1])}</a>'
        if prev
        else '<span class="none">&larr; start of term</span>'
    )
    n = (
        f'<a href="{nxt[0]}">{esc(nxt[1])} &rarr;</a>'
        if nxt
        else '<span class="none">end of term &rarr;</span>'
    )
    return (
        f'<nav class="pager">{p}<a href="advanced_python_hub.html">Course hub</a>{n}</nav>\n'
    )


def validate(paths):
    """Check the generated pages for the usual breakages."""
    problems = []
    names = {os.path.basename(p) for p in paths}
    for p in paths:
        base = os.path.basename(p)
        with open(p) as f:
            doc = f.read()

        for tag in ["div", "pre", "code", "table", "header", "nav", "button", "p"]:
            o = len(re.findall(rf"<{tag}[\s>]", doc))
            c = len(re.findall(rf"</{tag}>", doc))
            if o != c:
                problems.append(f"{base}: <{tag}> {o} open vs {c} close")

        btns = re.findall(r'data-target="([^"]+)"', doc)
        ids = re.findall(r'class="ans" id="([^"]+)"', doc)
        if sorted(btns) != sorted(ids):
            problems.append(
                f"{base}: {len(btns)} reveal buttons vs {len(ids)} answer boxes"
            )
        if len(btns) != len(set(btns)):
            problems.append(f"{base}: duplicate reveal ids")

        for block in re.findall(r"<pre><code>(.*?)</code></pre>", doc, re.S):
            if "<" in block or ">" in block:
                problems.append(f"{base}: unescaped angle bracket in a code block")
                break

        for href in re.findall(r'href="([^"#h][^"]*)"', doc):
            if href.endswith(".html") and href not in names:
                problems.append(f"{base}: link to missing page {href}")

        if "\u2014" in doc or "\u2013" in doc:
            problems.append(f"{base}: contains an em or en dash")
        if "&mdash;" in doc or "&ndash;" in doc:
            problems.append(f"{base}: contains a dash entity")
        for cell in re.findall(r'<td class="std">.*?</td><td>(.*?)</td>', doc, re.S):
            txt = re.sub(r"<[^>]+>", "", cell).strip()
            if txt.endswith((":", ";", "such as", "such as by", "by")):
                problems.append(f"{base}: standard statement is a truncated stem: {txt[-40:]!r}")
        if "localStorage" in doc or "sessionStorage" in doc:
            problems.append(f"{base}: uses blocked browser storage")
        if "index.html" in doc:
            problems.append(f"{base}: references index.html")
    return problems

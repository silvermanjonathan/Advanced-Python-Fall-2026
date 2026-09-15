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
    "family=Bricolage+Grotesque:opsz,wght@12..96,400..800&"
    "family=DM+Sans:wght@400;500;700&"
    "family=JetBrains+Mono:wght@400;700&display=swap\" rel=\"stylesheet\">"
)

# Lecture Light, shared with the beginner course: built for a projector in a room
# with the lights on. Light ground, near-black text, few accents, no hairlines.
CSS = """
:root{
  --paper:#F4F0E6; --card:#FFFDF7; --ink:#17181B; --ink-soft:#4A4D53; --rule:#D3CBB8;
  --teal:#0E4D52; --teal-deep:#0A3A3E; --clay:#9C2B22;
  --ochre:#8A5A00; --ochre-line:#D99B12; --ochre-tint:#FBF2DC;
  --green:#1D5B39; --green-tint:#E8F1E9; --green-ink:#122B1C;
  --code-bg:#EDE7D9;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:'DM Sans',system-ui,sans-serif; font-size:18px; font-weight:500;
  line-height:1.65;
}
.wrap{max-width:900px; margin:0 auto}
a{color:var(--teal)}
a:focus-visible,button:focus-visible{outline:3px solid var(--ochre-line); outline-offset:3px}

/* masthead */
header.top{
  background:var(--teal); color:#FFFDF7;
  border-bottom:6px solid var(--ochre-line); padding:30px 22px 26px;
}
.eyebrow{
  font-family:'JetBrains Mono',monospace; font-size:13px; letter-spacing:.14em;
  text-transform:uppercase; color:#F2D89B; margin:0 0 10px; font-weight:700;
}
h1{
  font-family:'Bricolage Grotesque','DM Sans',sans-serif; font-weight:800;
  font-size:clamp(29px,4.8vw,44px); line-height:1.1; margin:0 0 10px;
}
h2{
  font-family:'Bricolage Grotesque','DM Sans',sans-serif; font-weight:700;
  font-size:25px; line-height:1.2; margin:0 0 12px; color:var(--teal-deep);
}
h3{
  font-family:'Bricolage Grotesque','DM Sans',sans-serif; font-weight:700;
  font-size:20px; margin:18px 0 8px; color:var(--teal-deep);
}
header.top h1,header.top h2{color:#FFFDF7}
.sub{color:#EAE3D2; margin:0 0 16px; font-size:19px; font-weight:400; max-width:70ch}
.dates{
  display:flex; flex-wrap:wrap; gap:10px; margin-top:16px;
  font-family:'JetBrains Mono',monospace; font-size:13.5px;
}
.pill{
  border:2px solid rgba(255,253,247,.4); border-radius:999px; padding:5px 13px;
  background:rgba(255,253,247,.08);
}
.pill b{color:#F2D89B; font-weight:700}

/* sections */
main{padding:28px 22px 12px}
section{
  background:var(--card); border:2px solid var(--rule); border-radius:6px;
  padding:22px 24px; margin:0 0 20px;
}
section.opener{border-left:8px solid var(--green)}
section.chunk{border-left:8px solid var(--ochre-line)}
section.brief{border-left:8px solid var(--teal)}
.chunk-no{
  font-family:'JetBrains Mono',monospace; font-size:13px; letter-spacing:.12em;
  text-transform:uppercase; color:var(--ochre); margin:0 0 8px; font-weight:700;
}
p{margin:0 0 14px; max-width:72ch}
ul,ol{margin:0 0 14px; padding-left:24px}
li{margin:0 0 8px; max-width:70ch}
ul.tight li{margin:0 0 5px}
.two{display:grid; gap:0 30px; grid-template-columns:1fr}
@media(min-width:760px){.two{grid-template-columns:1fr 1fr}}

/* code and output */
code,pre{
  /* JetBrains Mono ligatures turn != into a slashed equals and <= into a single
     glyph; students then type a character that does not exist. Keep every
     operator as the keys that produce it. */
  font-variant-ligatures:none; font-feature-settings:"liga" 0,"calt" 0,"dlig" 0;
}
code{
  font-family:'JetBrains Mono',monospace; font-size:.9em; font-weight:700;
  background:var(--code-bg); color:#1E2A2B; padding:2px 6px; border-radius:3px;
}
pre{
  font-family:'JetBrains Mono',monospace; font-size:15.5px; line-height:1.6;
  background:var(--code-bg); color:var(--ink); border:2px solid var(--rule);
  border-left:6px solid #B9AF96; border-radius:4px;
  padding:16px 18px; overflow-x:auto; margin:0 0 16px; font-weight:500;
}
pre code{background:none; padding:0; font-size:inherit; font-weight:inherit; color:inherit}
.fname{
  font-family:'JetBrains Mono',monospace; font-size:12.5px; letter-spacing:.1em;
  text-transform:uppercase; color:var(--ink-soft); margin:0 0 6px; font-weight:700;
}
.out{margin:0 0 16px}
.out .tag{
  font-family:'JetBrains Mono',monospace; font-size:12.5px; letter-spacing:.1em;
  text-transform:uppercase; color:var(--green); margin:0 0 7px; font-weight:700;
  display:block;
}
.out pre{background:var(--green-tint); border-color:#A9C6B2; border-left:6px solid var(--green); color:var(--green-ink)}

/* predict and reveal */
.predict{
  border:2px dashed var(--ochre); border-radius:5px;
  padding:16px 18px; margin:0 0 16px; background:var(--ochre-tint);
}
.predict b{color:var(--ochre)}
.predict > pre{background:var(--card)}
button.rev{
  font-family:'DM Sans',sans-serif; font-size:16px; font-weight:700;
  background:var(--teal); color:#FFFDF7; border:0; border-radius:4px;
  padding:10px 18px; cursor:pointer; margin:4px 0 0;
}
button.rev:hover{background:var(--teal-deep)}
.ans{display:none; margin-top:16px; padding-top:16px; border-top:2px solid var(--rule)}
.ans.show{display:block}
.ans > :last-child{margin-bottom:0}
.bug{
  background:#F7E4E1; border:2px solid var(--clay); border-left:8px solid var(--clay);
  border-radius:5px; padding:14px 16px; margin:0 0 18px; color:#3A1512;
}
.bug b{color:var(--clay)}
.flag{
  background:#F7E4E1; border:2px solid var(--clay); border-left:8px solid var(--clay);
  border-radius:5px; padding:14px 16px; margin:0 0 20px; font-size:16.5px; color:#3A1512;
}
.flag b{color:var(--clay)}

/* tables */
table{border-collapse:collapse; width:100%; margin:0 0 16px; font-size:16.5px}
th,td{border:2px solid var(--rule); padding:9px 11px; text-align:left; vertical-align:top;
  overflow-wrap:anywhere}
th{background:#EFE9DA; font-weight:700; font-size:15px; color:var(--teal-deep)}
td code{font-size:.86em}

/* exits */
.exits{display:grid; gap:14px; grid-template-columns:1fr}
@media(min-width:760px){.exits{grid-template-columns:repeat(3,1fr)}}
.exit{border:2px solid var(--rule); border-radius:5px; padding:16px; background:var(--card)}
.exit p{margin:0; font-size:16.5px}
.exit .lab{
  font-family:'JetBrains Mono',monospace; font-size:12.5px; letter-spacing:.1em;
  text-transform:uppercase; margin:0 0 8px; font-weight:700; display:block;
}
.exit:nth-child(1){border-top:6px solid var(--green)}
.exit:nth-child(1) .lab{color:var(--green)}
.exit:nth-child(2){border-top:6px solid var(--ochre-line)}
.exit:nth-child(2) .lab{color:var(--ochre)}
.exit:nth-child(3){border-top:6px solid var(--clay)}
.exit:nth-child(3) .lab{color:var(--clay)}

/* teacher panel and the capstone block */
section.panel{border-left:8px solid var(--clay)}
section.panel > h2{color:var(--clay)}
.panel p,.panel li{font-size:16.5px}
.std{font-family:'JetBrains Mono',monospace; font-weight:700; color:var(--teal)}
.mapnote{font-size:15px; color:var(--ink-soft); border-left:4px solid var(--rule); padding-left:14px}

/* pager and footer */
nav.pager{
  max-width:900px; margin:0 auto; padding:8px 22px 34px;
  display:flex; justify-content:space-between; gap:12px; flex-wrap:wrap;
  font-family:'JetBrains Mono',monospace; font-size:14px;
}
nav.pager a,nav.pager .none{
  text-decoration:none; font-weight:700; border:2px solid var(--rule);
  background:var(--card); border-radius:4px; padding:10px 14px;
}
nav.pager a{color:var(--teal)}
nav.pager a:hover{background:#EFE9DA}
nav.pager .none{color:var(--ink-soft); border-style:dashed}
footer{
  background:#EAE4D5; border-top:4px solid var(--teal); padding:22px 22px 36px;
  font-size:15px; color:var(--ink-soft);
}
footer p{margin:0}

/* hub */
.grid{margin:0}
.row{
  border:2px solid var(--rule); border-left:8px solid var(--teal); border-radius:5px;
  margin:0 0 12px; padding:14px 16px; background:var(--card);
  display:grid; grid-template-columns:44px 84px 1fr; gap:6px 14px; align-items:baseline;
}
.row .n{font-family:'JetBrains Mono',monospace; font-size:24px; font-weight:700; color:var(--teal)}
.row .d{font-family:'JetBrains Mono',monospace; font-size:13px; color:var(--ink-soft)}
.row .t{font-weight:700; font-size:19px}
.row .t a{text-decoration:none}
.row .s{display:block; font-weight:400; font-size:16px; color:var(--ink-soft); max-width:62ch}
.row.off{border-left-color:var(--clay); background:#FBF9F3}
.row.off .n{color:var(--clay)}

@media (max-width:760px){
  body{font-size:17px} main{padding:22px 16px 8px} header.top{padding:24px 16px 20px}
  section{padding:18px 16px} .row{grid-template-columns:38px 1fr}
  .row .d{grid-column:2} .row .t{grid-column:2}
  table{table-layout:fixed} th,td{padding:7px 8px}
}
@media print{
  body{background:#fff; font-size:11pt}
  header.top{background:#fff; color:#111; border-bottom:3px solid #111}
  header.top h1,header.top .sub,header.top .eyebrow,.pill b{color:#111}
  .pill{border-color:#666}
  button.rev{display:none} .ans{display:block}
  nav.pager,footer{display:none}
  section,.exit{background:#fff; break-inside:avoid} pre{border:1px solid #999}
  a{color:#111}
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
        f'<div class="predict"><b>Predict first.</b> {question}\n'
        f'<button class="rev" data-target="{rid}" data-show="{esc(show)}" '
        f'data-hide="{esc(hide)}" aria-expanded="false" aria-controls="{rid}">{esc(show)}</button>\n'
        f'<div class="ans" id="{rid}">{answer}</div></div>\n'
    )


FOOTER = (
    "<footer><div class=\"wrap\"><p>Advanced Python, Robofun Fall 2026. Second printing, "
    "13 September 2026. Built by a generator; the page, not the file, is the source of "
    "truth for output, because every quoted line came from a run.</p></div></footer>\n"
)


def _wrap_h2s(fragment):
    """Wrap each top-level h2 block of fragment in a card section."""
    pieces = re.split(r"(?=<h2)", fragment)
    out = pieces[0]
    for piece in pieces[1:]:
        m = re.match(
            r'<h2><span class="num">(\d+)</span>(.*?)<span class="mins">(.*?)</span></h2>',
            piece,
        )
        if m:
            num, title, mins = m.groups()
            cls = "opener" if num == "1" else "chunk"
            head = (
                f'<section class="{cls}"><p class="chunk-no">Section {num} &middot; '
                f"{mins}</p><h2>{title}</h2>"
            )
            out += head + piece[m.end():] + "</section>\n"
        else:
            out += "<section>" + piece + "</section>\n"
    return out


def sectionize(body):
    """Split a page body into header, sectioned main content, and pager."""
    header, rest = body.split("</header>", 1)
    header += "</header>"
    parts = re.split(
        r'(?=<section class="panel"|<div class="exits">|<nav class="pager">)', rest
    )
    main = ""
    nav = ""
    for part in parts:
        if part.startswith('<nav class="pager">'):
            nav = part
        elif part.startswith('<section class="panel"'):
            main += part
        elif part.startswith('<div class="exits">'):
            main += '<section class="brief"><h2>Exits</h2>' + part + "</section>\n"
        else:
            main += _wrap_h2s(part)
    return header, main, nav


def page(filename, title, body, head_extra=""):
    """Write one self-contained page."""
    header, main, nav = sectionize(body)
    doc = (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{esc(title)}</title>\n{FONTS}\n<style>{CSS}</style>\n{head_extra}"
        "</head>\n<body>\n"
        f'{header}\n<main><div class="wrap">\n{main}</div></main>\n{nav}{FOOTER}'
        f"<script>{JS}</script>\n</body>\n</html>\n"
    )
    path = os.path.join(OUT, filename)
    with open(path, "w") as f:
        f.write(doc)
    return path


def masthead(serial, title, when, lede):
    """Return the page masthead: the teal band with the eyebrow, title, and pills."""
    eyebrow = (
        f"Advanced Python &middot; Robofun &middot; Session {int(serial)} of 13"
        if serial
        else "Robofun &middot; Fall 2026 &middot; 110 West End Avenue"
    )
    return (
        '<header class="top"><div class="wrap">'
        f'<p class="eyebrow">{eyebrow}</p><h1>{esc(title)}</h1>'
        f'<p class="sub">{esc(lede)}</p>'
        f'<div class="dates"><span class="pill"><b>When</b> {esc(when)}</span>'
        '<span class="pill"><b>Time</b> 4:00 to 5:30</span>'
        '<span class="pill"><b>Length</b> 90 minutes</span></div>'
        "</div></header>\n"
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

        for tag in ["div", "pre", "code", "table", "header", "nav", "button", "p",
                    "section", "main", "footer", "h2"]:
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

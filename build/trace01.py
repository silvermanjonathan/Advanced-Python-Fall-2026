"""Session 1: an animated trace of gate_log.py filling the worksheet table."""

from build import masthead, pager

DOORS = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0]

TRACE_CSS = """
<style>
.doors{display:flex; gap:8px; flex-wrap:wrap; margin:0 0 16px}
.door{width:46px; height:58px; border:2px solid var(--rule); border-radius:4px;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  font-family:'JetBrains Mono',monospace; font-weight:700; background:var(--card)}
.door small{font-size:11px; color:var(--ink-soft); font-weight:400}
.door.open{background:var(--green-tint); border-color:var(--green); color:var(--green-ink)}
.door.shut{background:#F7E4E1; border-color:var(--clay); color:#3A1512}
.door.now{outline:4px solid var(--ochre-line); outline-offset:2px}
.controls{display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin:0 0 16px}
.controls button{font-family:'DM Sans',sans-serif; font-size:16px; font-weight:700;
  background:var(--teal); color:#FFFDF7; border:0; border-radius:4px; padding:10px 18px; cursor:pointer}
.controls button:hover{background:var(--teal-deep)}
.controls button.quiet{background:var(--card); color:var(--teal); border:2px solid var(--rule)}
.controls label{font-size:15px; color:var(--ink-soft); margin-left:8px}
.two-up{display:grid; gap:18px; grid-template-columns:1fr}
@media(min-width:820px){.two-up{grid-template-columns:1fr 1fr; align-items:start}}
pre.prog{margin:0; font-size:15px; line-height:1.55; counter-reset:ln}
pre.prog span.l{display:block; padding:0 6px; border-radius:3px; margin:0 -6px}
pre.prog span.l.hot{background:var(--ochre-tint); box-shadow:inset 4px 0 0 var(--ochre-line)}
pre.prog span.l.fired{background:var(--green-tint); box-shadow:inset 4px 0 0 var(--green)}
table.trace{table-layout:fixed; margin:0}
table.trace th,table.trace td{text-align:center; font-family:'JetBrains Mono',monospace; height:36px; padding:4px}
table.trace td.i{background:#EFE9DA; font-weight:700}
table.trace tr.start td{background:#FBF9F3; color:var(--ink-soft)}
table.trace td.new{background:var(--ochre-tint); font-weight:700; transition:background .6s}
table.trace td.set{background:var(--green-tint)}
table.trace tr.cur td.i{background:var(--ochre-line); color:#fff}
.say{border:2px dashed var(--ochre); border-radius:5px; background:var(--ochre-tint);
  padding:14px 18px; margin:0 0 16px; min-height:64px; font-size:17px}
.say b{color:var(--ochre)}
.vars{display:flex; gap:10px; flex-wrap:wrap; margin:0 0 16px}
.var{border:2px solid var(--rule); border-radius:5px; padding:8px 14px; background:var(--card);
  font-family:'JetBrains Mono',monospace; font-size:15px; min-width:78px; text-align:center}
.var b{display:block; font-size:22px}
.var.bump{border-color:var(--ochre-line); background:var(--ochre-tint)}
@media (prefers-reduced-motion:reduce){table.trace td.new{transition:none}}
</style>
"""

PROGRAM_LINES = [
    "door = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0]",
    "",
    "x = 0",
    "y = 0",
    "z = 0",
    "q = 0",
    "",
    "for i in range(12):",
    "    d = door[i]",
    "",
    "    if d == 1:",
    "        x = x + 1",
    "        z = z + 1",
    "",
    "    if d == 0:",
    "        y = y + 1",
    "        z = 0",
    "",
    "    if z > q:",
    "        q = z",
]


def program_block():
    """Return gate_log.py with one span per line so lines can light up."""
    out = '<pre class="prog">'
    for n, line in enumerate(PROGRAM_LINES):
        text = line.replace("<", "&lt;").replace(">", "&gt;")
        out += f'<span class="l" id="ln{n}">{text if text else " "}</span>'
    return out + "</pre>"


SCRIPT = """
<script>
(function(){
  var doors = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0];
  var steps = [];
  var x = 0, y = 0, z = 0, q = 0;
  steps.push({say: 'Before the loop. All four variables start at 0.', lines: [2,3,4,5], row: -1});
  for (var i = 0; i < 12; i++) {
    var d = doors[i];
    steps.push({say: 'Pass ' + i + '. Read the door: <b>d</b> is ' + d + (d === 1 ? ', open.' : ', shut.'),
      lines: [7, 8], row: i, set: {d: d}, fired: []});
    if (d === 1) {
      x = x + 1; z = z + 1;
      steps.push({say: 'First gate, <b>d == 1</b>: yes. <b>x</b> becomes ' + x + ' and <b>z</b> becomes ' + z + '.',
        lines: [10, 11, 12], row: i, set: {x: x, z: z}, fired: [10, 11, 12]});
    } else {
      steps.push({say: 'First gate, <b>d == 1</b>: no. Nothing inside it runs, so <b>x</b> stays ' + x + '.',
        lines: [10], row: i, set: {x: x}, fired: []});
    }
    if (d === 0) {
      y = y + 1; z = 0;
      steps.push({say: 'Second gate, <b>d == 0</b>: yes. <b>y</b> becomes ' + y + ' and <b>z</b> goes back to 0.',
        lines: [14, 15, 16], row: i, set: {y: y, z: z}, fired: [14, 15, 16]});
    } else {
      steps.push({say: 'Second gate, <b>d == 0</b>: no. <b>y</b> stays ' + y + '.',
        lines: [14], row: i, set: {y: y}, fired: []});
    }
    if (z > q) {
      var qBefore = q;
      q = z;
      steps.push({say: 'Third gate, <b>z &gt; q</b>: ' + z + ' is greater than ' + qBefore + ', yes. <b>q</b> becomes ' + q + '. That is a new longest run.',
        lines: [18, 19], row: i, set: {q: q}, fired: [18, 19], done: true});
    } else {
      steps.push({say: 'Third gate, <b>z &gt; q</b>: ' + z + ' is not greater than ' + q + ', no. <b>q</b> stays ' + q + '.',
        lines: [18], row: i, set: {q: q}, fired: [], done: true});
    }
  }
  steps.push({say: 'The loop is over. The four print lines show <b>x</b> 7, <b>y</b> 5, <b>z</b> 0, <b>q</b> 3. z is 0 only because the last door was shut.', lines: [], row: 12});

  var at = 0, timer = null;
  var cols = ['d', 'x', 'y', 'z', 'q'];
  function cell(row, col){ return document.getElementById('c' + row + col); }
  function render(){
    var s = steps[at];
    document.getElementById('say').innerHTML = s.say;
    document.getElementById('where').textContent = 'Step ' + at + ' of ' + (steps.length - 1);
    for (var n = 0; n < 20; n++) {
      var el = document.getElementById('ln' + n);
      el.className = 'l' + (s.lines.indexOf(n) >= 0 ? ((s.fired || []).indexOf(n) >= 0 ? ' fired' : ' hot') : '');
    }
    for (var i = 0; i < 12; i++) {
      var dv = document.getElementById('door' + i);
      dv.className = 'door ' + (doors[i] === 1 ? 'open' : 'shut') + (i === s.row ? ' now' : '');
      var tr = document.getElementById('row' + i);
      tr.className = (i === s.row ? 'cur' : '');
      cols.forEach(function(c){ var td = cell(i, c); td.textContent = ''; td.className = ''; });
    }
    // replay every step up to 'at' so the table shows what has been filled so far
    var vals = {};
    for (var k = 1; k <= at; k++) {
      var st = steps[k];
      if (st.row < 0 || st.row > 11) continue;
      if (!vals[st.row]) vals[st.row] = {};
      for (var key in (st.set || {})) vals[st.row][key] = st.set[key];
    }
    for (var r = 0; r < 12; r++) {
      if (!vals[r]) continue;
      cols.forEach(function(c){
        if (vals[r][c] !== undefined) { var td = cell(r, c); td.textContent = vals[r][c]; td.className = 'set'; }
      });
    }
    if (s.row >= 0 && s.row <= 11) {
      for (var key in (s.set || {})) { var td2 = cell(s.row, key); td2.className = 'new'; }
    }
    var live = {x: 0, y: 0, z: 0, q: 0};
    for (var m = 1; m <= at; m++) { var q2 = steps[m].set || {}; for (var kk in q2) if (kk !== 'd') live[kk] = q2[kk]; }
    ['x','y','z','q'].forEach(function(v){
      var box = document.getElementById('v' + v);
      box.querySelector('b').textContent = live[v];
      box.className = 'var' + ((s.set && s.set[v] !== undefined && s.fired && s.fired.length) ? ' bump' : '');
    });
  }
  function step(){ if (at < steps.length - 1) { at++; render(); } else { stop(); } }
  function back(){ if (at > 0) { at--; render(); } }
  function reset(){ stop(); at = 0; render(); }
  function play(){ if (timer) { stop(); return; } document.getElementById('play').textContent = 'Pause';
    timer = setInterval(step, parseInt(document.getElementById('speed').value, 10)); }
  function stop(){ if (timer) clearInterval(timer); timer = null; document.getElementById('play').textContent = 'Play'; }
  document.getElementById('step').addEventListener('click', function(){ stop(); step(); });
  document.getElementById('back').addEventListener('click', function(){ stop(); back(); });
  document.getElementById('reset').addEventListener('click', reset);
  document.getElementById('play').addEventListener('click', play);
  document.getElementById('speed').addEventListener('change', function(){ if (timer) { stop(); play(); } });
  document.addEventListener('keydown', function(e){
    if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); stop(); step(); }
    if (e.key === 'ArrowLeft') { e.preventDefault(); stop(); back(); }
  });
  render();
})();
</script>
"""


def trace01():
    """Return the animated door trace page body."""
    b = masthead(
        "01",
        "Watch the door trace fill in",
        "Wednesday 16 September 2026",
        "The worksheet table for gate_log.py, filled one gate at a time. Step through it "
        "on the projector, or play it and watch the three gates open and shut.",
    )
    b += (
        '<div class="toolbar"><a class="btn quiet" href="wed01_worksheet.html">Back to '
        'the worksheet</a><a class="btn quiet" href="wed01_cold_read.html">Session 1 '
        "page</a></div>"
    )
    b += '<h2><span class="num">1</span>The corridor<span class="mins">gate_log.py</span></h2>'
    b += "<p>Twelve doors. 1 is open, 0 is shut. The highlighted door is the one the loop is reading now.</p>"
    b += '<div class="doors">'
    for i, d in enumerate(DOORS):
        cls = "open" if d == 1 else "shut"
        b += f'<div class="door {cls}" id="door{i}">{d}<small>i={i}</small></div>'
    b += "</div>"
    b += (
        '<div class="controls">'
        '<button id="step">Step</button><button id="play">Play</button>'
        '<button id="back" class="quiet">Back</button><button id="reset" class="quiet">Reset</button>'
        '<label>Speed <select id="speed"><option value="1400">slow</option>'
        '<option value="800" selected>medium</option><option value="350">fast</option></select></label>'
        '<label id="where"></label>'
        "</div>"
        '<p class="nb">Keyboard: right arrow or space to step, left arrow to go back.</p>'
    )
    b += '<div class="say" id="say"></div>'
    b += '<div class="vars">'
    for v in "xyzq":
        b += f'<div class="var" id="v{v}">{v}<b>0</b></div>'
    b += "</div>"
    b += '<div class="two-up">' + program_block()
    b += '<div><table class="trace"><tr><th>i</th><th>d</th><th>x</th><th>y</th><th>z</th><th>q</th></tr>'
    b += '<tr class="start"><td>start</td><td></td><td>0</td><td>0</td><td>0</td><td>0</td></tr>'
    for i in range(12):
        b += f'<tr id="row{i}"><td class="i">{i}</td>'
        for c in "dxyzq":
            b += f'<td id="c{i}{c}"></td>'
        b += "</tr>"
    b += "</table></div></div>"
    b += (
        "<p>Each pass through the loop is four steps: read the door, then three gates in "
        "a row. A gate that opens is shaded green in the program. A gate that stays shut "
        "is shaded amber, and nothing inside it runs. Watch <code>z</code> climb while "
        "the doors are open and fall back to 0 the moment one is shut, and watch "
        "<code>q</code> catch only the highest value <code>z</code> ever reached.</p>"
    )
    b += pager(
        ("wed01_worksheet.html", "Session 1 worksheet"),
        ("wed01_cold_read.html", "Session 1: the page"),
    )
    b += SCRIPT
    return b

import re, pathlib
R = pathlib.Path('/Users/daviderichsen/Apps/Humanizer/yourwriting-ai')
SP = pathlib.Path('/private/tmp/claude-502/-Users-daviderichsen-Apps/c6bbc8e0-ea03-466a-9099-8b80b9762b2e/scratchpad')
tech = (R/'concepts/tech/index.html').read_text()
import subprocess
def git_head(path): return subprocess.run(['git','-C',str(R),'show','HEAD:'+path],capture_output=True,text=True,check=True).stdout
proof = git_head('index.html')          # the gate cut as committed

def between(s, a, b, incl=True):
    i = s.find(a); assert i >= 0, a[:60]
    j = s.find(b, i + len(a)); assert j >= 0, b[:60]
    return s[i:j+len(b)] if incl else s[i+len(a):j]
def rep1(s, old, new):
    assert s.count(old) == 1, (s.count(old), old[:70]); return s.replace(old, new)

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300..800&family=DM+Mono:wght@400;500&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">'
FAVICON_BLUE = "%2374a6ff"
NAV = '''<header class="nav" id="nav">
  <div class="container nav-inner">
    <a href="index.html" class="brand" aria-label="yourwriting.ai home"><span class="brand-name">yourwriting<span class="tld">.ai</span></span></a>
    <nav class="nav-links" aria-label="Primary"><a href="index.html#how" {how}>How it works</a><a href="gate.html" {gate}>The gate</a><a href="about.html" {about}>About</a><a href="faq.html" {faq}>FAQ</a></nav>
    <div class="nav-actions">
      <a href="contact.html" class="btn btn-fill nav-cta">Book a walkthrough</a>
    </div>
    <button class="menu-toggle" id="menuToggle" aria-label="Open menu" aria-expanded="false"><i></i><i></i><i></i></button>
  </div>
  <div class="scroll-progress" aria-hidden="true"><i id="scrollProgress"></i></div>
</header>
<div class="menu-overlay" id="menuOverlay">
  <button class="menu-close" id="menuClose">CLOSE ✕</button>
  <a href="index.html#how">How it works</a><a href="gate.html">The gate</a><a href="about.html">About</a><a href="faq.html">FAQ</a>
  <a href="contact.html">Book a walkthrough</a>
</div>'''
def nav_for(page):
    cur = {k: ('aria-current="page"' if k == page else '') for k in ['how','gate','about','faq']}
    return NAV.format(**cur)

# ---------------- CSS ----------------
base_css = (R/'concepts/tech/assets/site.css').read_text()
adds = (SP/'gate-additions.css').read_text()
tokens = '''
/* ================= yourwriting.ai: gate additions on the indigo base ================= */
:root{
  --ok: oklch(0.76 0.16 155); --ok-deep: oklch(0.48 0.13 155); --flag: oklch(0.70 0.19 35);
  --paper: var(--page-light); --paper-ink: oklch(0.21 0.012 262); --paper-muted: oklch(0.46 0.012 262);
  --serif: "Source Serif 4", Georgia, serif; --radius-lg: 16px;
}
'''
post = '''
.ok{ color:var(--accent); }
.page-head h1 .amber, .page-head h1 .ok{ color:var(--accent); }
.btn-fill, .btn-honey{ background:var(--ink); color:var(--bg); }
.btn-fill:hover, .btn-honey:hover{ background:var(--accent); color:#fff; transform:translateY(-1px); }
.cta .btn-honey{ background:var(--page-light-ink); color:var(--page-light); }
.cta .btn-honey:hover{ background:var(--accent-ink); color:#fff; }
.gate-cap b{ color:var(--accent); }
.cta h2 .amber, .cta h2 .ok{ color:var(--accent); }
.plan.lead{ border-color:oklch(from var(--accent) l c h / .45); background:oklch(from var(--accent) l c h / .07); }
.plan li::before{ color:var(--accent); }
.stats .stats-note{ margin-top:var(--s-6, 1.5rem); font-family:var(--mono); font-size:var(--t-micro); letter-spacing:.12em; text-transform:uppercase; color:var(--muted); }
'''
(R/'assets/site.css').write_text(base_css + tokens + adds + post)

# ---------------- INDEX ----------------
t = tech
# head
t = rep1(t, '<title>yourwriting.ai — An AI stack built around your writing</title>', '<title>Communication you can count on — yourwriting.ai</title>')
t = re.sub(r'<meta name="description" content="[^"]*">',
  '<meta name="description" content="yourwriting.ai tunes a model on the writing your firm already sends, then checks every claim against your own files before anyone reads it.">\n<link rel="canonical" href="https://yourwriting.ai/">\n<meta property="og:type" content="website">\n<meta property="og:site_name" content="yourwriting.ai">\n<meta property="og:title" content="Communication you can count on — yourwriting.ai">\n<meta property="og:description" content="yourwriting.ai tunes a model on the writing your firm already sends, then checks every claim against your own files before anyone reads it.">\n<meta property="og:url" content="https://yourwriting.ai/">\n<meta name="twitter:card" content="summary">', t, count=1)
t = re.sub(r'<link href="https://fonts.googleapis.com/css2\?family=Manrope[^"]*" rel="stylesheet">', FONTS, t, count=1)
palette = between(t, '<script>\n(function(){\n  var P = {', '})();\n</script>')
t = t.replace(palette, '')
# nav
old_nav = between(t, '<header class="nav" id="nav">', '</div>\n\n<main id="main">', incl=False)
t = t.replace('<header class="nav" id="nav">' + old_nav + '</div>', nav_for('how'))
# hero copy
t = rep1(t, '<div class="sc-step" id="st1" style="left:14%; top:76%; width:22%;"><b>01</b><strong>The screen</strong><p>Nothing changes for your team. Same monitor, same apps, one new address on the office network.</p></div>',
            '<div class="sc-step" id="st1" style="left:14%; top:76%; width:22%;"><b>01</b><strong>The draft</strong><p>Written in your voice, on the screen your team already uses. Every claim in it is marked before a person reads it.</p></div>')
t = rep1(t, '<strong>The box</strong><p>Under the desk: the model, your indexed documents, and our guard. One power cord, no subscription.</p>',
            '<strong>The box</strong><p>Under the desk: the tuned model, the gate, and an index of your own files. One power cord, no subscription.</p>')
t = rep1(t, '<strong>The cable</strong><p>It talks to your office network and nothing else. No internet round trip, no per-token bill.</p>',
            '<strong>The cable</strong><p>It talks to your office network and nothing else. No file leaves the building, no per-token bill.</p>')
t = rep1(t, '<h1 class="sh-h1"><span>An AI Stack That Was Built Around <span class="amber">Your Writing</span></span></h1>',
            '<h1 class="sh-h1"><span>Communication You Can <span class="amber">Count On</span></span></h1>')
A3_OLD = '<h2>One model in the building. Everyone connects to it.</h2><p>Your people at home, on the road and on site come in through your VPN. Frontier models only ever see what our guard lets out.</p>'
A3_NEW = '<h2>One model and one gate in the building. Everyone connects to it.</h2><p>Your people at home, on the road and on site come in through your VPN. Every draft passes the gate before a person sees it, and frontier models only ever see what the guard lets out.</p>'
assert t.count(A3_OLD) == 2; t = t.replace(A3_OLD, A3_NEW)
# anatomy
t = rep1(t, "<p class=\"sec-sub\">Rent the same model as your competitors and you'll ship the same answers. The layers underneath are where the difference is made.</p>",
            "<p class=\"sec-sub\">Rent the same model as your competitors and you'll ship the same answers. The layers underneath are where the difference is made — and the top one is a receipt.</p>")
layers_old = between(t, '<ol class="layer-list" id="layerList">', '</ol>')
layers_new = '''<ol class="layer-list" id="layerList">
        <li><span class="ll-name">The receipt</span><p class="ll-note">What your reviewer touches: every claim, the file and line it came from, what was repaired, what's held.</p></li>
        <li><span class="ll-name">The gate</span><p class="ll-note">Splits the draft into claims and checks each one against your files. Supported, repaired or held — no third answer.</p></li>
        <li><span class="ll-name">Evaluation</span><p class="ll-note">Planted errors, poisoned sources, a blind judge. Proof it works before your clients find out it doesn't.</p></li>
        <li><span class="ll-name">Human review</span><p class="ll-note">Your people grade the misses. Every one becomes a training example or a new gate rule.</p></li>
        <li><span class="ll-name">The tune</span><p class="ll-note">A thin adapter learned from the letters you already send, so drafts land in your voice.</p></li>
        <li><span class="ll-name">Your files</span><p class="ll-note">Invoices, contracts, policies, sent mail. The only truth the gate accepts — and the part money can't shortcut.</p></li>
      </ol>'''
t = t.replace(layers_old, layers_new)
for a, b in [('<span class="plate-tag">PRODUCT</span>', '<span class="plate-tag">RECEIPT</span>'), ('<span class="plate-tag">MODEL</span>', '<span class="plate-tag">GATE</span>'),
             ('<span class="plate-tag amber">TESTING</span>', '<span class="plate-tag amber">EVAL</span>'), ('<span class="plate-tag amber">LABELED</span>', '<span class="plate-tag amber">TUNE</span>'),
             ('<span class="plate-tag amber">RAW DATA</span>', '<span class="plate-tag amber">YOUR FILES</span>')]:
    t = rep1(t, a, b)
# models section -> gate section (from proof)
models = between(t, '<!-- models: the scorecard -->', '<!-- cases -->')
gate = between(proof, '<section class="gate" id="gate">', '</section>')
gate = gate.replace('class="ok"', 'class="amber"').replace('btn-ok', 'btn-fill')
t = t.replace(models, '<!-- the gate -->\n' + gate + '\n\n')
# forge (#how) after cinema
how = between(proof, '<section class="sec" id="how">', '</div></section>').replace('class="ok"', 'class="amber"').replace('LIVE IN 40 S', 'LIVE WITHIN THE HOUR')
writes = between(proof, '<section class="sec" id="writes">', '</div></section>').replace('class="ok"', 'class="amber"')
t = rep1(t, '<!-- night fold -->', '<!-- how it learns -->\n' + how + '\n\n<!-- what it writes -->\n' + writes + '\n\n<!-- night fold -->')
# night fold copy
t = rep1(t, '<h2>Agents work while <span class="amber">your company sleeps.</span></h2>', '<h2>Graded while <span class="amber">your office sleeps.</span></h2>')
t = rep1(t, "<p class=\"nf-sub\">Watched by people who don't. Every answer is graded overnight; every miss becomes tomorrow's training data.</p>",
            "<p class=\"nf-sub\">Every held claim and every edit your people made is read back overnight. Misses become the next adapter's training examples — and, where the miss was a claim, a new gate rule.</p>")
t = rep1(t, '<span class="nf-text">Your team logs off. The loop keeps working.</span>', "<span class=\"nf-text\">Your team logs off. The day's drafts and their receipts are queued.</span>")
t = rep1(t, "<span class=\"nf-text\">Graders on three continents review the day's answers.</span>", '<span class="nf-text">Held claims and edited drafts are graded against what actually went out.</span>')
t = rep1(t, "<span class=\"nf-text\">A scored report waits in your inbox — what slipped, what's fixed, what's next.</span>", '<span class="nf-text">A short report waits in your inbox — what was held, what was repaired, what changed.</span>')
# stats
stats_old = between(t, '<section class="stats" id="numbers">', '</section>')
stats_new = '''<section class="stats" id="numbers">
  <div class="container stats-grid">
    <div class="stat"><b><span class="count" data-to="99.8" data-dec="1">0</span><i>%</i></b><span>PLANTED ERRORS CAUGHT · 528 OF 529</span></div>
    <div class="stat"><b><span class="count" data-to="0" data-dec="0">0</span></b><span>SILENT MISSES ON POISONED SOURCES</span></div>
    <div class="stat"><b><span class="count" data-to="1.3" data-dec="1">0</span><i>%</i></b><span>FALSE FLAGS AT THE LIVE THRESHOLD</span></div>
    <div class="stat"><b><span class="count" data-to="160" data-dec="0">0</span></b><span>EVALUATION RUNS, JUDGED BLIND</span></div>
  </div>
  <p class="container stats-note">Gate v0.3 evaluation · October 2026 · planted and poisoned errors, a second model as blind judge. The full report is in every pilot's security pack.</p>
</section>'''
t = t.replace(stats_old, stats_new)
# quote -> limits + price
quote = between(t, '<!-- quote -->', '<!-- cta -->')
limits = between(proof, '<section class="sec" id="limits">', '</div></section>').replace('class="ok"', 'class="amber"')
price = between(proof, '<section class="sec" id="price">', '</div></section>').replace('class="ok"', 'class="amber"').replace('btn-ok', 'btn-fill')
t = t.replace(quote, '<!-- limits -->\n' + limits + '\n\n<!-- engagements -->\n' + price + '\n\n<!-- cta -->')
# cta
cta_old = between(t, '<section class="cta" id="demo">', '</section>')
cta_new = '''<section class="cta" id="demo">
  <div class="container">
    <h2 data-reveal>Bring one letter <span class="amber">you can't get wrong.</span></h2>
    <p data-reveal>We'll tune on the ones you've already sent, wire the gate to the files behind them, and show you the graded difference in four weeks.</p>
    <a href="contact.html" class="btn btn-honey" data-reveal>Book a walkthrough <span class="arr" aria-hidden="true">→</span></a>
  </div>
</section>'''
t = t.replace(cta_old, cta_new)
# footer
foot_old = between(t, '<footer id="company">', '</footer>')
foot_new = between(proof, '<footer id="company">', '</footer>')
t = t.replace(foot_old, foot_new)
# chat quick buttons
cq_old = between(t, '<div class="cw-quick">', '</div>'); cq_new = between(proof, '<div class="cw-quick">', '</div>')
t = t.replace(cq_old, cq_new)
# scripts
t = rep1(t, '<script src="assets/models.js"></script>\n', '')
main_js = between(t, '<script>\n(function(){\n  "use strict";', '})();\n</script>')
models_js = between(main_js, '  /* models: pick one local + one frontier', '  })();\n')
main_js_new = main_js.replace(models_js, '')
t = t.replace(main_js, main_js_new)
gate_js = '  /* the gate: claims lift out' + between(proof, '  /* ---------------- the gate: claims lift out', '  /* ---------------- counters ----------------', incl=False)
extra = '''<script>
(function(){
  if (typeof window.gsap === "undefined" || typeof window.ScrollTrigger === "undefined") return;
  gsap.registerPlugin(ScrollTrigger);
  var RM = matchMedia("(prefers-reduced-motion: reduce)").matches;
''' + gate_js + '''
  ScrollTrigger.sort(); ScrollTrigger.refresh();
})();
</script>'''
t = rep1(t, '<button class="cw-btn" id="cwBtn"', extra + '\n<button class="cw-btn" id="cwBtn"')
# refresh order must follow document order: hero > gate > anatomy > cinema > forge > overnight
for old, new in [
  ('trigger: ".sh", start: "top top", end: "+=7600",', 'trigger: ".sh", start: "top top", end: "+=7600", refreshPriority: 10,'),
  ('trigger: "#gatePin", start: mobile ? "top 70%" : "top top",', 'trigger: "#gatePin", refreshPriority: 9, start: mobile ? "top 70%" : "top top",'),
  ('trigger: ".anatomy", start: "top top", end: "+=2600",', 'trigger: ".anatomy", start: "top top", end: "+=2600", refreshPriority: 8,'),
  ('trigger: section, start: "top top", end: "+=3000",', 'trigger: section, start: "top top", end: "+=3000", refreshPriority: 7,'),
  ('ScrollTrigger.create({ trigger: s, start: "top 62%", end: "bottom 62%", onToggle:', 'ScrollTrigger.create({ trigger: s, refreshPriority: 6, start: "top 62%", end: "bottom 62%", onToggle:'),
  ('ScrollTrigger.create({ trigger: "#forgeSteps", start: "top 62%", end: "bottom 62%", scrub:', 'ScrollTrigger.create({ trigger: "#forgeSteps", refreshPriority: 6, start: "top 62%", end: "bottom 62%", scrub:'),
  ('trigger: ".night-fold", start: "top top", end: "+=2600",', 'trigger: ".night-fold", start: "top top", end: "+=2600", refreshPriority: 5,'),
  ('  ScrollTrigger.sort(); ScrollTrigger.refresh();', '  ScrollTrigger.refresh(); window.addEventListener("load", function(){ ScrollTrigger.refresh(); });'),
]:
    t = rep1(t, old, new)
assert 'A FICTIONAL' not in t and 'models.html' not in t and 'Amara' not in t and 'solutions.html' not in t
(R/'index.html').write_text(t)

# ---------------- SUBPAGES ----------------
for p, key in [('gate.html','gate'), ('about.html','about'), ('contact.html',''), ('faq.html','faq')]:
    s = git_head(p)
    s = re.sub(r'<link href="https://fonts.googleapis.com/css2\?family=Inter\+Tight[^"]*" rel="stylesheet">', FONTS, s, count=1)
    s = rep1(s, '<link rel="stylesheet" href="assets/proof.css">', '<link rel="stylesheet" href="assets/site.css">')
    s = s.replace('%2334c98a', FAVICON_BLUE)
    old = between(s, '<header class="nav" id="nav">', '<main id="main">', incl=False)
    s = s.replace('<header class="nav" id="nav">' + old, nav_for(key) + '\n')
    s = s.replace('class="ok"', 'class="amber"').replace('btn-ok', 'btn-fill')
    if p == 'gate.html': s = s.replace('.gf-branch .hold{', '.gf-branch .held{').replace('<div class="hold"><b>', '<div class="held"><b>')
    (R/p).write_text(s)
if (R/'assets/proof.css').exists(): (R/'assets/proof.css').unlink()
print('built; index', len(t), 'css', (R/'assets/site.css').stat().st_size)

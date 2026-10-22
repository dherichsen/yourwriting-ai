
/* Crucible site: nav, reveals, chat widget (scripted — wire CHAT_ENDPOINT to a real assistant) */
(function(){
  var nav = document.getElementById("nav"), sub = document.body.classList.contains("sub");
  if (sub && nav) { nav.classList.add("nav-dark", "scrolled"); }
  var t = document.getElementById("menuToggle"), ov = document.getElementById("menuOverlay"), cl = document.getElementById("menuClose");
  function openMenu(o){ if (!ov) return; ov.classList.toggle("open", o); t && t.setAttribute("aria-expanded", String(o)); document.documentElement.style.overflow = o ? "hidden" : ""; }
  if (sub) { /* the home page binds its own menu; binding twice would toggle it straight back shut */
    t && t.addEventListener("click", function(){ openMenu(!ov.classList.contains("open")); });
    cl && cl.addEventListener("click", function(){ openMenu(false); });
    ov && ov.querySelectorAll("a").forEach(function(a){ a.addEventListener("click", function(){ openMenu(false); }); });
  }
  if (sub) { document.documentElement.classList.add("motion-ok"); var io = new IntersectionObserver(function(es){ es.forEach(function(e){ if (e.isIntersecting) { e.target.classList.add("revealed"); io.unobserve(e.target); } }); }, { rootMargin: "0px 0px -8% 0px" }); document.querySelectorAll("[data-reveal]").forEach(function(el){ io.observe(el); }); }

  /* chat */
  var CHAT_ENDPOINT = ""; /* POST {messages:[...]} → {reply:"..."}; empty = scripted answers below */
  var FAQ = [
    { k: /fine.?tun|custom|train|adapter|lora|teach|solution/i, a: "Fine-tuning teaches the local model your documents, vocabulary and rules. A thin adapter trains on the box in a few hours; the base model stays untouched. Four weeks per task, scored before and after. Details on the <a href='solutions.html'>Custom Solutions</a> page." },
    { k: /who are you|about|team|founded|company|where.*based|hiring|career|job/i, a: "Keep is nine people in Tucson who put a private AI box in small businesses: practices, shops, firms. Sam started it in 2025 after running IT for a dental group; 1,240 businesses have a box today. The story and open roles are on the <a href='about.html'>About</a> page." },
    { k: /local|on.?prem|building|office|box|workstation/i, a: "Local means an open model (Qwen 3.8 is our pick) running on a small box we set up in your office, usually under a desk. Your files never leave the building and there is no per-message bill. Almost everyone starts here." },
    { k: /api|frontier|claude|fable|astra|openai|grok|gemini|cloud/i, a: "Frontier models (Fable 5.1, Astra, Grok 4.6 and others) run behind our guard: every request is screened for prompt injection and a small local model hashes names and account numbers before anything leaves, then restores them on the way back. Typical round trip is about 380 ms." },
    { k: /price|pricing|cost|how much|\$|budget/i, a: "A flat monthly price per box, no per-seat and no per-message fees; the pilot month is free. Keep One is $390 a month after the 30-day pilot; the tiers are on the <a href='index.html#pilot'>home page</a>, or <a href='contact.html'>talk to Sam</a>." },
    { k: /secur|privacy|pii|hash|inject|safe|leak|gdpr|hipaa/i, a: "Two layers. Locally, nothing leaves your network. For API calls, our guard screens for prompt injection and hashes personal details locally before the request goes out, so the provider only sees an anonymised request. See the <a href='faq.html'>FAQ</a> for the audit details." },
    { k: /speed|latency|fast|slow|ms/i, a: "Local answers come back in about 40 ms; guarded frontier calls in about 380 ms. Chat takes the fast path, deep analysis the thorough one." },
    { k: /model|which|best|recommend|test|compare|score/i, a: "We run the whole field against your real tasks before your data touches anything, then recommend one. The current scorecard is on the <a href='models.html'>models page</a>; Qwen 3.8 is our default local pick." },
    { k: /demo|call|talk|human|person|sales|contact|book/i, a: "Happy to. Leave your details on the <a href='contact.html'>contact page</a> and Sam replies within one business day, usually the same afternoon." },
    { k: /install|setup|how long|deploy|when|tuesday/i, a: "One afternoon. We bring the box, plug it into power and your network, index your files and leave when your first answer comes back. The 30-day pilot starts that day." },
    { k: /remote|home|vpn|travel|field/i, a: "People working from home, traveling or on site reach the local model through your existing VPN. Nothing changes for them except the address." },
  ];
  var btn = document.getElementById("cwBtn"), panel = document.getElementById("cw"), log = document.getElementById("cwLog"), form = document.getElementById("cwForm"), input = document.getElementById("cwInput");
  if (!btn || !panel) return;
  function add(text, who){ var m = document.createElement("div"); m.className = "msg " + who; if (who === "bot") m.innerHTML = text; else m.textContent = text; log.appendChild(m); log.scrollTop = log.scrollHeight; return m; }
  function reply(q){
    var hit = FAQ.find(function(f){ return f.k.test(q); });
    var a = hit ? hit.a : "I can answer questions about the box, the pilot, pricing, security, speed and setup. For anything else, <a href='contact.html'>leave Sam a note</a>; he replies within one business day.";
    var typing = add("…", "bot");
    setTimeout(function(){ typing.innerHTML = a; log.scrollTop = log.scrollHeight; }, 500);
  }
  function ask(q){ add(q, "me"); if (CHAT_ENDPOINT) { fetch(CHAT_ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ messages: [{ role: "user", content: q }] }) }).then(function(r){ return r.json(); }).then(function(j){ add(j.reply || "…", "bot"); }).catch(function(){ reply(q); }); } else reply(q); }
  var opened = false;
  function open(o){ panel.classList.toggle("open", o); btn.setAttribute("aria-expanded", String(o)); if (o && !opened) { opened = true; add("Hi. Ask about the box, the pilot, pricing, security or setup. I'm scripted; Sam picks up on the contact page.", "bot"); } if (o) input.focus(); }
  btn.addEventListener("click", function(){ open(!panel.classList.contains("open")); });
  document.getElementById("cwClose").addEventListener("click", function(){ open(false); });
  document.querySelectorAll(".cw-quick button").forEach(function(b){ b.addEventListener("click", function(){ ask(b.textContent); }); });
  form.addEventListener("submit", function(e){ e.preventDefault(); var q = input.value.trim(); if (!q) return; input.value = ""; ask(q); });
  document.addEventListener("keydown", function(e){ if (e.key === "Escape") open(false); });
})();

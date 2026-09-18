# yourwriting.ai

Concept sites for a fictional product: an open model fine-tuned on the writing your business already sends, running on a box in your own building, with a hallucination gate in front of it.

- **`tech/` — yourwriting.ai, the techy cut.** Scale-style proportions, indigo black, a three-act pinned scroll story (screen → desk → office floor plan), a paired model scorecard, and a fine-tuning deep dive.
- **`proof/` — yourwriting.ai, the fine-tuning cut.** Built entirely around fine-tuning and the **hallucination gate**: the draft is split into claims, each claim is looked up in your own files, repaired or held, and a receipt travels with it. Charcoal and paper, green for checked, red-orange for flagged.
- **`keep/` — Keep.** The same idea aimed at small businesses: light, blue/orange/yellow, a founder named Sam, a thirty-day pilot and three hardware tiers.

Each site has a home page, a models list, a model detail page (with an inlined sample evaluation report), a fine-tuning page, about, FAQ, contact, and a scripted chat widget. Plain static HTML (GSAP + ScrollTrigger + Lenis, Three.js for the night-shift globe) — open from disk or any static host. Form and chat endpoints are empty constants (`INQUIRY_ENDPOINT`, `CHAT_ENDPOINT`).

Everything here is fictional: the companies, people, prices, scores and quotes are invented. Not affiliated with Scale AI, onpremises.ai or anyone else.

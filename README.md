# yourwriting.ai

The live site for yourwriting.ai: an open model fine-tuned on the writing your firm already sends, with a hallucination gate in front of it that traces every claim to a line in your own files.

- **Root (`index.html`, `gate.html`, `about.html`, `contact.html`, `faq.html`)** — the site. The indigo-black "on-premises" design (pinned three-act hero, layer stack, cinema, night globe) carrying the gate cut's content and its two scenes (the receipt animation and "how it learns your voice"). Stylesheet: `assets/site.css` = the on-prem base plus a gate-additions block.
- **`concepts/`** — the five earlier concept cuts (tech, proof, keep, creators, everyday), kept for reference, `noindex`, disallowed in `robots.txt`. Everything in there is fictional.

Plain static HTML (GSAP + ScrollTrigger + Lenis, Three.js for the globe). Contact form posts to FormSubmit (`hello@yourwriting.ai`) with a mailto fallback. Hosted on GitHub Pages; canonical domain https://yourwriting.ai/.

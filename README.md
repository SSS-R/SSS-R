<h1 align="center">Sultan Rafi</h1>

<p align="center"><strong>Harness engineer</strong></p>

<p align="center">
  I build the scaffolding autonomous coding agents run inside: the specs,<br>
  the permission layers, the validators. And I'm the one who checks what comes out.
</p>

<p align="center">
  <sub>CS undergrad · BRAC University · Dhaka, Bangladesh</sub>
</p>

---

## What I'm building

**[PDF Splitter](https://github.com/SSS-R/pdf-splitter)** · [use it →](https://sss-r.github.io/pdf-splitter/)
A PDF toolkit that runs entirely in your browser. Split, merge, compress, reorder, images to PDF.
Open devtools, watch the Network tab, process a file. You'll see zero requests. That isn't a
feature bullet, it's the whole product.
<sub>`Vanilla JS` `Vite` `Playwright`</sub>

**[Master Sentinal](https://github.com/SSS-R/Master-Sentinal)**
Windows diagnostics hub for the moment something feels *off* with a PC. Live dashboard, guided
health scan with real repair tools, shareable reports, all in plain language instead of jargon.
No telemetry, no upsell, MIT forever.
<sub>`Python 3.11` `CI-tested`</sub>

**[Zenfa AI](https://github.com/SSS-R/Zenfa-AI)** · [platform](https://github.com/SSS-R/project-zenfa)
A PC build optimizer for the Bangladesh market, where parts pricing is volatile and nobody's
catalogue is trustworthy. A knapsack solver handles the hard constraints; the LLM handles the
judgment calls a solver can't encode.
<sub>`FastAPI` `Gemini Flash` `Docker`</sub>

**[UPI: The FIFA Paradox](https://github.com/SSS-R/UPI)**
Football rates players on goals and assists, which ignores most of what happens in a match.
UPI builds a Unified Performance Index over StatsBomb open data that rewards every deliberate
action on the pitch.
<sub>`Jupyter` `pandas` `state-value models`</sub>

---

## How I work

I build with AI coding agents. The agent isn't the skill, though. Anyone can ask one to write
code. What decides whether you get something real is everything you put around it.

**I write the spec first.**
Before any code: a short document saying what this does, what it deliberately does not do, and
what finished looks like. Give an agent a vague goal and it will build the wrong thing with
total confidence, and the code will look fine while it does it.

**I put a gate in front of anything that executes.**
In [mobile-agent-pc](https://github.com/SSS-R/mobile-agent-pc), no command reaches the machine
until it clears a validator and a permissions file. If software can act on its own, something
predictable should sit between it and your system.

**I check the output before I believe it.**
The failure that hurts isn't a crash, it's a confident wrong answer: a command flag that doesn't
exist, a number labelled with the wrong unit, a security assumption that doesn't hold. I've
caught all three. Run it, read it, check the number.

---

## Free help, if you need it

I'm a student building a track record, not an agency. If you're stuck on something in web
development or AI, I'll work on it for free.

Worth asking me about:

- **Web apps** in Next.js, React or FastAPI. Building one, or fixing one that broke.
- **Getting an LLM into your product**: agents, MCP servers, retrieval, automation pipelines.
- **Reviewing code an AI wrote for you** before it goes live. This is the one people skip.
- **Small Python tools** and scripts you keep doing by hand.

No invoice, no catch. Open an issue on any repo here and describe the problem.

I'm one person and still in university, so I'll tell you straight if I'm out of depth or out of
time, instead of wasting yours.

---

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/SSS-R/SSS-R/main/assets/stats-dark.svg">
  <img src="https://raw.githubusercontent.com/SSS-R/SSS-R/main/assets/stats-light.svg" alt="Contribution and language stats" width="840">
</picture>

<sub>Generated daily by <a href="scripts/generate_stats.py">a script in this repo</a> rather than a third-party
card service, so it still renders when those are rate-limited.</sub>

</div>

---

<p align="center">
  <a href="https://github.com/SSS-R"><img src="https://img.shields.io/badge/GitHub-SSS--R-181717?style=flat-square&logo=github" alt="GitHub"></a>
  <!-- add your own: LinkedIn · email · portfolio -->
</p>

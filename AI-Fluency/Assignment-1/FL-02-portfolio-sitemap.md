# FL-02: Portfolio Sitemap + AI Workspace

**Week 1 — Decide What You're Proving**

---

## Proof Statement

> I build production-ready, secure APIs that pass compliance reviews — input validation, auth, rate limiting, CORS — on first pass. I'm proving this to a tech lead at a compliance-heavy company, so they will download my CV.
>
> **Why this needs to exist:** A CV lists titles but can't prove production-readiness. A portfolio shows the actual secure patterns, the before/after of a compliance gap closed, and the reasoning behind every security decision.

## Portfolio Sitemap

```
Landing ──► Home (Hero)
               │
               ├──► Work (Case Studies)
               │       ├── API Security Audit — before/after
               │       └── Production-Ready API Build
               │
               ├──► About
               │       └── Why security, my process, the tools I use
               │
               └──► Contact / CV
                       └── Download CV + Let's talk
```

### Page-by-page rationale

| Page | Purpose against claim | Leads to the one action? |
|------|-----------------------|--------------------------|
| **Home** | Hero states the claim in one sentence. CTA button: "Download CV". Tech lead knows in 5 seconds who I am and what I prove. | Yes — primary CTA is the one action. |
| **Work** | Proves the claim. Two case studies showing secure API patterns, decision reasoning, and compliance impact. | Prepares them — they need proof before they'll download. |
| **About** | Explains why I focus on security, my background, my thinking process. Humanizes the claim. | Supports — a tech lead wants to know *who* built this. |
| **Contact / CV** | The one action: download CV and send me a message. No friction. | Yes — this is the destination. |

### What I deliberately left out
- **Blog** — doesn't prove the claim. Tech lead doesn't need my opinions, they need to see secure code.
- **Skills bars / badges** — visual noise. The case studies prove competence better than percentages.
- **Testimonials** — don't have them yet. Adding an empty section weakens trust.

## Claude Project Setup

I created a Claude Project called **"Backend Security Portfolio — AI Fluency"** with these custom instructions:

```
You are a tutor helping me build a portfolio that proves ONE thing: that I build production-ready, secure APIs that pass compliance reviews.

My proof statement (our north star):
"I build production-ready, secure APIs that pass compliance reviews — input validation, auth, rate limiting, CORS — on first pass. I'm proving this to a tech lead at a compliance-heavy company, so they will download my CV."

Your role:
- Tutor, not author. Explain your reasoning. Show trade-offs. Ask sharp questions.
- When I share work or ideas, pressure-test them against the proof statement.
- If something doesn't serve the claim or the one action (download CV), call it out.
- Keep answers concise. No fluff. No fake enthusiasm.

Reference: I'm a backend AI engineering intern. My stack is Python, FastAPI, PostgreSQL, Docker. I value minimal dependencies, type hints, and testing.
```

## Pressure-Test Prompt

I ran this prompt inside my Claude Project:

```
This is my proof statement: "I build production-ready, secure APIs that pass compliance reviews — input validation, auth, rate limiting, CORS — on first pass. I'm proving this to a tech lead at a compliance-heavy company, so they will download my CV."

This is my sitemap:
- Home (hero + CTA to download CV)
- Work (two case studies: API security audit, production API build)
- About (why security, my thinking process)
- Contact / CV (download + message)

Pressure-test this sitemap against my claim and my one action. Specifically:
1. Which pages earn their place?
2. Which pages are wasted or redundant?
3. What's missing?
4. Does this actually walk a tech lead from landing → believing → downloading my CV?
5. Where is the weakest link?

Be specific, not encouraging. I want to know what to change.
```

## Changes I Made After Pressure-Testing

Structurally the sitemap is right — four pages, one action, no wasted nav items. The gap isn't architecture, it's evidence: the claim makes four specific, checkable promises and the sitemap doesn't yet say where the checking happens.

**1. Which pages earn their place?**
- **Work** — unconditionally. It's the only page that's evidence instead of assertion. Every other page exists to route people into it or catch them after it.
- **Home** — earns its place structurally as the entry point, but as scoped ("hero + CTA") it does zero persuading. If Home is just a headline and a button, one of two things happens: the visitor bounces before reaching your actual proof, or they download the CV cold, unconvinced. A skeptical tech lead reading an unconvincing CV with no primed context is a worse outcome than no download at all.
- **Contact/CV** — earns its place as the terminal action page, but it's doing two jobs. See #2.
- **About** — conditional. Only earns its place if "my thinking process" means a reusable method — a checklist you'd apply to any endpoint — not a backstory. "Why security" is the tell. That phrasing points toward origin-story content, which is fluff against this specific claim.

**2. Which pages are wasted or redundant?**
No full page is dead weight — but there's wasted space inside two of them.
- Contact/CV bundles two different intents: download (transactional, matches your one action) and message (relational, a different action for a different visitor). A tech lead evaluating you for compliance rigor doesn't want to chat first, they want the artifact. Competing CTAs drag down conversion on both. Shrink the message form to visibly secondary, or cut it — your CV already has your email.
- If About just restates what Work already shows ("I care about security, here's my process") without generalizing it, it's redundant. It only earns its keep if Work is the applied instance and About is the reusable method behind it.

**3. What's missing?**
- **A named framework.** "Passes compliance reviews" is empty until you say reviewed against *what* — OWASP ASVS, OWASP API Security Top 10, whatever you're actually using. Name it, consistently, everywhere the claim appears.
- **Externally verifiable artifacts**, not just narrative: repo links, CI badges (tests, lint, dependency/security scanning), coverage %, ideally a live endpoint with OpenAPI docs the tech lead can poke themselves — hit the rate-limited route and watch it 429, send a bad payload and watch it 422. Letting them verify beats telling them.
- **A dated artifact for "on first pass" specifically** — a scan report or checklist, timestamped, showing state at the *first* review, not after fixes. No date or version attached, and "on first pass" is unfalsifiable marketing copy — this audience will clock that immediately.
- **A persistent CV-download path.** Right now it only lives on Home and Contact. Someone convinced halfway through a Work case study shouldn't have to hunt for it — put it in the nav, on every page.

I'm not suggesting new top-level pages for any of this. A "Proof" or "Demo" page adds friction to a funnel built around one action. This is content that belongs inside Work and Home, plus one persistent nav element.

**4. Does it walk a tech lead from landing → believing → downloading?**
The shape is right: land, prove, optionally deepen, convert. Two joints will actually break:
- Home gives no reason to believe before asking for a click into Work — right now that click is unearned.
- Work is carrying 100% of the persuasion weight for a specific, checkable claim (4 named pillars + "on first pass"), and nothing in the sitemap says yet where that specific evidence lives.

About being skippable is fine — not everything needs to be mandatory reading in a lean funnel. It's only a problem if you're quietly relying on About to deliver proof that Work should already be carrying on its own.

**5. Weakest link**
The evidence gap behind "on first pass." That's the boldest, most specific, most checkable phrase in the whole statement — it implies an actual review event with a documented outcome, not "I'm confident this is secure." Nothing in the sitemap shows where that lives.

Two questions to resolve before you build anything further:
- Are the audit case study and the build case study the same project? If yes, that's your strongest possible structure — the audit *is* your pass artifact for the build. If no, "on first pass" has no receipt for whichever project doesn't have an audit attached, and the claim reads as confidence, not proof.
- Who ran the "pass" — you, against a checklist? If so, is that checklist itself visible, so the tech lead can judge your bar instead of taking your word that you cleared it?

One more precise inconsistency: your claim says "APIs," plural. Your sitemap shows one build case study. Either the second case study also needs to demonstrate a build, not just an audit, or the claim should read "an API" — a plural claim resting on singular evidence is exactly the kind of gap a compliance reviewer is trained to catch.

```
Pictures:
```
<img width="959" height="539" alt="image" src="https://github.com/user-attachments/assets/49d987dc-435a-4bc3-be9e-e7cde486aa57" />
<img width="959" height="539" alt="Screenshot 2026-07-13 173325" src="https://github.com/user-attachments/assets/05deed2e-9a88-445a-a7a3-c31509262adc" />
<img width="959" height="539" alt="Screenshot 2026-07-13 174546" src="https://github.com/user-attachments/assets/f6197fef-6f97-48a0-8614-cbc4f5c06290" />
<img width="959" height="539" alt="Screenshot 2026-07-13 174604" src="https://github.com/user-attachments/assets/3a9a9bcf-e94f-4a2c-af2d-6645ef70eb94" />





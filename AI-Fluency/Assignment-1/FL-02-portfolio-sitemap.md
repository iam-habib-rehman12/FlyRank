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

*(To fill in after I get Claude's response.)*

1. ...
2. ...
```


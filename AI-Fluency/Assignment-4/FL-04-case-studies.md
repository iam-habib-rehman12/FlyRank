# FL-04: Framed Case Studies

**Week 2 · Frame Your Work**

---

## Voice Card

> Direct, plain, no buzzwords, warm.

Added to my Claude Project as a standing instruction so every draft stays in my voice.

---

## Case 1: MindTrial — Multi-LLM Benchmarking Framework

### The problem

Teams building LLM-powered apps have no standard way to compare models across the things that actually matter — reasoning, vision, structured output. Benchmarks exist but they're scattered, inconsistent, and don't let you test the same task across multiple models side by side.

### What I did

I built a modular benchmarking framework that evaluates multiple LLMs across reasoning, vision, and structured output tasks. Key decisions:

- Configurable evaluation tasks so you're not locked into one test set
- Structured metrics and dashboards for comparing model strengths and weaknesses side by side
- Modular design so adding a new model or task doesn't require rewriting the whole pipeline

I decided against a monolithic evaluation script early on. A modular approach meant each model and task lived in its own component, making the system testable and extensible from the start.

### What came of it

The framework enables systematic testing of model behavior across dimensions that actually matter in production. Teams can compare models on the same tasks, see where each one falls short, and make informed decisions instead of guessing.

Next: expand to cover more model providers and add automated regression testing so a new model version doesn't silently break existing evaluations.

---

## Case 2: CineAI — AI-Powered Movie Discovery

### The problem

Streaming platforms recommend based on what you watched, not why you liked it. The result: the same five suggestions on loop. Users who want to discover something genuinely new have no way to find it.

### What I did

I built a Netflix-inspired movie discovery system using content-based filtering. Core decisions:

- Content-based over collaborative filtering — no "people who liked X also liked Y" echo chamber
- Explainable recommendations — the UI shows *why* a movie was suggested, not just the suggestion itself
- Built with Python and Streamlit for a fast, interactive frontend

The explainability piece was a deliberate choice. I wanted users to trust the suggestions, not wonder why a random title appeared.

### What came of it

A working recommendation engine that surfaces movies based on actual content similarity, not just popularity. The explainable UI means users can see the reasoning behind each pick and refine their search accordingly.

Next: add user feedback loops so the model improves from real interactions, not just initial similarity scores.

---

## Case 3: Conversation Intelligence Platform — NLP Behavioral Analytics

### The problem

WhatsApp group chats and community conversations contain rich behavioral data — who talks to whom, when, and how — but extracting those insights requires manual effort. No one is reading through thousands of messages to find patterns.

### What I did

I built an NLP pipeline that analyzes large-scale conversational datasets from WhatsApp exports. The system:

- Processes message history and extracts behavioral signals — response patterns, emoji usage, temporal activity
- Models social interaction patterns through network analysis
- Visualises everything in interactive dashboards

Key decision: build the pipeline modularly so it can ingest data from other platforms (Telegram, Slack) without a full rewrite. The analytics layer stays the same; only the parser changes.

### What came of it

The platform turns raw chat exports into actionable behavioral insights — who's most engaged, when conversations peak, how communication styles differ. The interactive dashboards make the patterns visible at a glance instead of buried in spreadsheets.

Next: add sentiment analysis over time so you can see not just what people did, but how the tone of a conversation shifted across weeks.

---

## Bio & Contact

### Bio

I build AI systems that actually work on real problems — LLM evaluation, recommendation engines, conversational analytics. I'm an AI Systems Engineer focused on making machine learning useful, not just interesting.

### Contact / CTA

Want to see the code or talk about a project? [Download my CV](mailto:janmuhammadjanwari@gmail.com) or send a message. Happy to chat about LLMs, NLP, or what I'm building next.

---

## Before / After: Generic AI vs Edited

### Before (generic AI line)

> "I'm a passionate and results-driven AI engineer dedicated to leveraging cutting-edge machine learning technologies to deliver innovative solutions that drive measurable impact and exceed stakeholder expectations."

### After (my version, post-edit)

> I build AI systems that actually work on real problems — LLM evaluation, recommendation engines, conversational analytics. I'm an AI Systems Engineer focused on making machine learning useful, not just interesting.

**What I cut:** "passionate," "results-driven," "cutting-edge," "leveraging," "innovative solutions," "measurable impact," "stakeholder expectations" — seven buzzwords that say nothing specific.

**What stayed:** a concrete claim (I build AI systems), specific examples (LLM evaluation, recommendations, analytics), and a clear stance (useful, not just interesting). A real person could say this out loud.

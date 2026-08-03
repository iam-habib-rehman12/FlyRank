# Build the Systems That Build Software

## Assignment Information

- **Track:** Backend AI Engineering
- **Phase:** Build
- **Type:** Video assignment
- **Session:** Build the Systems That Build Software
- **Instructor:** Mirza Asceric
- **Video:** https://www.youtube.com/watch?v=rraHPF4ZgCw

## Overview

AI-assisted software development changes the engineer's job. The primary challenge is no longer typing every line of code; it is designing the environment in which an AI coding agent can work reliably. That environment—the plans, context, documentation, tools, tests, constraints, and feedback loops around the model—is the **agent harness**.

A capable model without a strong harness may produce code quickly but inconsistently. A strong harness turns that raw capability into a repeatable engineering process. It gives the agent enough context to make good decisions, breaks work into verifiable tasks, detects mistakes, and prevents an automated loop from declaring success when the software is not actually complete.

## Key Lessons

### 1. The engineer's role is shifting

Traditional development puts most effort into manually implementing code. AI-native development moves more effort toward:

- defining the problem precisely;
- designing system boundaries and architecture;
- writing executable specifications;
- providing useful repository context;
- building automated checks;
- reviewing behavior and outcomes;
- deciding priorities and trade-offs.

AI can accelerate implementation, but it does not remove engineering judgment. Human responsibility moves upward—from writing syntax to designing and supervising the system that produces the syntax.

### 2. Context is the agent's memory

An agent starts each new conversation with limited knowledge. Important decisions that exist only in chat history or in a developer's head will eventually be lost.

Persistent repository files should therefore contain the information needed to continue the work:

- project purpose and architecture;
- setup and run commands;
- coding conventions;
- important constraints;
- domain terminology;
- design decisions;
- testing and deployment instructions;
- links to deeper documentation.

The repository becomes shared memory for both humans and agents.

### 3. The README should be a map

A useful README does not try to contain every detail. It helps a new contributor—or an agent—quickly discover:

1. what the project does;
2. how the repository is organized;
3. how to install and run it;
4. how to verify changes;
5. where detailed documentation lives.

Documentation should be concise, current, discoverable, and close to the code it describes. Stale or ambiguous documentation is dangerous because an agent may follow it confidently.

### 4. Specifications must be executable

A weak task such as “build authentication” leaves too many decisions implicit. A strong specification is detailed enough that a capable stranger could implement it without repeatedly asking what was intended.

A good specification includes:

- the problem and desired user outcome;
- scope and explicit non-goals;
- affected components;
- data models and API contracts;
- security and failure cases;
- implementation steps;
- acceptance criteria;
- validation commands;
- a visible definition of done.

“Done” must be observable. Examples include a passing test, a successful API response, a migration that runs cleanly, or a UI state that can be demonstrated.

### 5. Build a controlled implementation loop

A productive agent loop repeatedly:

1. reads the specification;
2. selects one incomplete task;
3. implements the smallest coherent change;
4. runs validation;
5. records progress;
6. continues only when the checks pass.

Small tasks reduce uncertainty and make failures easier to diagnose. The loop should operate on explicit state rather than relying on the agent to remember what happened earlier.

### 6. Trust comes from verification

Generated code should not be trusted merely because it looks reasonable or the agent says the task is finished. Trust must come from independent evidence:

- unit and integration tests;
- type checking;
- formatting and linting;
- database migration checks;
- security rules;
- API contract tests;
- build verification;
- end-to-end acceptance tests;
- human review for high-risk decisions.

A completion claim is meaningful only when the required gates pass.

### 7. Add circuit breakers

Autonomous loops can repeat the same mistake, consume resources, or make increasingly broad changes. A reliable harness needs limits such as:

- maximum attempts or iterations;
- time and cost budgets;
- restricted tool permissions;
- narrow file or service scope;
- stop conditions after repeated failures;
- escalation to a human when assumptions are unclear;
- rollback or recovery procedures.

The safest agent is not the one that never fails; it is the one that fails visibly, stops safely, and leaves useful evidence.

### 8. The codebase is an interface

Agents perform better in codebases that are easy to understand. Clear naming, small modules, explicit types, consistent structure, and enforced boundaries reduce the number of guesses the agent must make.

Good codebase design includes:

- descriptive domain language;
- typed inputs and outputs;
- stable interfaces;
- predictable directory structure;
- focused functions and modules;
- automated architectural rules;
- clear ownership of data and side effects.

Code quality is therefore part of prompt quality: the repository itself communicates intent to the agent.

### 9. Parallel agents require coordination

Multiple agents can increase throughput only when their work is isolated and their responsibilities are clear. Useful controls include:

- separate branches or worktrees;
- non-overlapping task ownership;
- shared specifications and conventions;
- dependency-aware task ordering;
- automated merge gates;
- one source of truth for progress;
- human review at integration points.

Without coordination, parallelism creates merge conflicts, duplicated work, and inconsistent architecture.

### 10. Human judgment remains essential

Humans remain responsible for deciding:

- what should be built;
- which trade-offs are acceptable;
- whether requirements reflect real user needs;
- how much risk is tolerable;
- whether the evidence actually proves correctness;
- when the AI is confidently wrong.

The engineer's highest-value skill is not producing more code. It is recognizing what matters, designing a trustworthy process, and catching errors before they reach users.

## Backend AI Engineering Application

For a backend service, I would apply these lessons by creating a harness with:

- a repository map and architecture documentation;
- versioned API and database specifications;
- small implementation tasks with acceptance criteria;
- unit, integration, and contract tests;
- typed schemas for requests, responses, and events;
- automated lint, type-check, migration, and test gates;
- limited credentials for agent tools;
- retry, timeout, and cost limits for background jobs;
- structured logs and observable failure states;
- human approval before production deployment or destructive data changes.

This approach lets an AI agent help implement endpoints, database operations, authentication, and background jobs while keeping correctness and control in the engineering system.

## Personal Takeaways

My main takeaway is that AI coding quality depends heavily on the system surrounding the model. Better prompts can help, but persistent context, precise specifications, strong tests, and safe feedback loops provide much more durable improvement.

The practical goal is to make the correct path easy and the incorrect path visible. When documentation explains the system, tasks define measurable outcomes, tests verify behavior, and circuit breakers limit failures, AI becomes a dependable engineering collaborator rather than an uncontrolled code generator.

## Completion Evidence

The assigned video was used as the learning resource for this write-up:

https://www.youtube.com/watch?v=rraHPF4ZgCw

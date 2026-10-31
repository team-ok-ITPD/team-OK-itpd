# Product vision

Debug GYM

## Goal

A learner can practice investigating and fixing bugs in a prepared, realistic
environment from inside VS Code, with optional agent help that leaves the
investigation and the fix to them.

**Supports:** [VP-01](research/value-proposition.md#vp-01),
[VP-02](research/value-proposition.md#vp-02),
[VP-03](research/value-proposition.md#vp-03).

**Threshold:** [the threshold of success](threshold-of-success.md).

## Stakeholders

- **Learner**: practices debugging with the product, the primary user.
- **Customer**: decides the scope, and most likely provides the agent's API
  keys.
- **Exercise authors**: the team, who write the bug categories, broken code,
  reproduction commands, and tests.
- **Whoever pays for the agent's API usage**: unresolved at kickoff, to be named
  once it is settled.

## Constraints

### CON-01

The first prototype uses Python.

- **Status:** Active
- **Source:** Customer-given
- **What it costs:** no Go or Java exercises in the first prototype.
- **Decision:** [`DEC-001`](decisions.md#dec-001)

### CON-02

Learners reach the prepared environment through VS Code, either on a website the
product provides or on their own machine over remote SSH.

- **Status:** Active
- **Source:** Customer-given
- **What it costs:** no support for other IDEs, and the product depends on SSH
  access to the environment.
- **Decision:** [`DEC-002`](decisions.md#dec-002)

### CON-03

Built and maintained by 4 people.

- **Status:** Active
- **Source:** Team-given
- **What it costs:** at most four people can work in parallel, so the first
  exercise set and the agent integration have to stay small enough for four
  people to build and maintain.

### CON-04

Nine course weeks remain (Weeks 3 to 11), ending with the final presentation on
December 4.

- **Status:** Active
- **Source:** Environmental
- **What it costs:** the first working slice is due in Week 3, the MVP in Week
  5, and the code freeze falls in Week 9, so the scope has to be a few exercises
  with minimal agent assistance rather than a full exercise gallery.

### CON-05

The first teaching service targets university students and teachers rather than an unrestricted public service.

- **Status:** Active
- **Source:** Customer-given
- **What it costs:** public acquisition and general-purpose commercial use are outside the first rollout; onboarding and access must serve the university audience.
- **Decision:** [`DEC-026`](decisions.md#dec-026)

### CON-06

Exercise access requires university-email authorization; a shared link is not anonymous access.

- **Status:** Active
- **Source:** Customer-given
- **What it costs:** the team must implement verified identity and access checks before broad sharing; the domain and verification mechanism still need agreement.
- **Decision:** [`DEC-019`](decisions.md#dec-019)

### CON-07

The product has administrator, teacher and student roles; only teachers publish exercises publicly, and only the administrator creates or changes teacher accounts.

- **Status:** Active
- **Source:** Customer-given
- **What it costs:** publication and teacher-account administration require separate authorization paths; generic staff access cannot stand in for the product permission model.
- **Decision:** [`DEC-017`](decisions.md#dec-017)

### CON-08

The administrator-supplied generation API key is usable by teachers only; the administrator does not generate exercises.

- **Status:** Active
- **Source:** Customer-given
- **What it costs:** generation must distinguish personal keys from the shared teacher key and authorize their use independently; one shared key is not available to every registered account.
- **Decision:** [`DEC-018`](decisions.md#dec-018)

### CON-09

Each named teaching group has exactly one teacher.

- **Status:** Active
- **Source:** Customer-given
- **What it costs:** the first group model cannot assume co-teaching; ownership transfer and teacher removal need explicit lifecycle policy.
- **Decision:** [`DEC-021`](decisions.md#dec-021)

## Boundary

### BND-01

Fix the bug for the learner.

- **Status:** Active
- **Handled by:** The user, by hand
- **Why:** [`DEC-004`](decisions.md#dec-004): the agent assists inside VS Code
  while the learner investigates and performs the fix.

### BND-02

Support IDEs other than VS Code.

- **Status:** Active
- **Handled by:** Nobody
- **Why:** [`DEC-002`](decisions.md#dec-002): VS Code is the first access path,
  and support for other IDEs was not confirmed.

### BND-03

Offer exercises in languages other than Python.

- **Status:** Active
- **Handled by:** Nobody
- **Why:** [`DEC-001`](decisions.md#dec-001): the customer asked to start with
  Python, such as Go and Java come later.

## Context

![System context diagram](architecture/context.svg)

The learner is the actor. The external systems are VS Code on the learner's own
machine and the AI agent service (API) that provides assistance. The prepared
environment, with its broken code and tests, is part of the product, per
[`DEC-003`](decisions.md#dec-003). VS Code is on the diagram because the learner
connects to the environment through it (`CON-02`), and the agent does not apply
the fix because `BND-01` leaves that to the learner.

## Where The Detail Lives

- [Roles, capabilities and access constraints](roles-and-access.md)

- [Architecture](architecture/README.md)

- [User stories](https://github.com/team-ok-ITPD/team-OK-itpd/issues?q=label%3Auser-story)
- [Week 2 report](../reports/week-02/README.md)

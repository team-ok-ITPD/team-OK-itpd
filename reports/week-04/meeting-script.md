# Meeting script

## Context

Our problem-space sentence: a developer who wants to practise debugging needs
one place where a realistic, multi-file exercise is generated, run with real
debugging tools, and checked against the intended bug, and no product carries
all three in one flow.

The current MUP demonstrates parts of five candidate stories, but they are not
finished or Customer-accepted. Known gaps include false-positive exercise
matching in FR-001, per-learner preparation and cleanup in FR-002, and the SSH
and invalid-access behavior in FR-005. US-03 and US-04 have automated technical
evidence, but still need a Customer verdict against their story criteria.

The five quality requirements contain proposed pilot measures. The three ADRs
are team-accepted records of current choices, but they are not proof that every
addressed requirement passes and have not been ratified by the Customer. The
deployment and access model remains unsettled.

Target: record a separate Customer verdict for US-01 through US-05, settle the
quality and architecture choices needed for the pilot, and choose the next
story without presenting unmet requirements as completed work.

## Agenda

1. Permission questions (2 min). Questions 1–3.
   Show: the recording and publication choices in the note taker's document.
2. The current software against its acceptance criteria (13 min).
   Show: the running product, and the stories
   [US-01](https://github.com/team-ok-ITPD/team-OK-itpd/issues/28),
   [US-02](https://github.com/team-ok-ITPD/team-OK-itpd/issues/29),
   [US-03](https://github.com/team-ok-ITPD/team-OK-itpd/issues/30),
   [US-04](https://github.com/team-ok-ITPD/team-OK-itpd/issues/31) and
   [US-05](https://github.com/team-ok-ITPD/team-OK-itpd/issues/32), one `AC-nn`
   at a time. Questions 4–12.
3. The quality requirements (6 min).
   Show: [the quality requirements](../../docs/quality-requirements/README.md).
   Questions 13–14.
4. The architecture against what drives it (5 min).
   Show: [the architecture](../../docs/architecture/README.md), its container
   view and its decisions. Questions 15–19.
5. What we build next (2 min).
   Show:
   [US-06](https://github.com/team-ok-ITPD/team-OK-itpd/issues/33) and
   [US-07](https://github.com/team-ok-ITPD/team-OK-itpd/issues/34). Question 20.
6. Read back the decisions and action points (2 min).  
   Show: the note taker's list. Question 21.

## Questions

1. _(closed)_ May we record this meeting?
2. _(closed)_ If recorded, may we publish a sanitized transcript in the public
   repository?
3. _(closed)_ May we share the recording or transcript with the course
   instructors? We will record each permission separately.
4. _(open)_ While each story runs, what did you expect to happen at this step
   that did not?
5. _(closed)_ Do you accept or reject US-01 against AC-01 and AC-02? Please name
   any failed criterion.
6. _(closed)_ Do you accept or reject US-02 against AC-01 and AC-02? Please name
   any failed criterion.
7. _(closed)_ Do you accept or reject US-03 against AC-01 and AC-02? Please name
   any failed criterion.
8. _(closed)_ Do you accept or reject US-04 against AC-01 and AC-02? Please name
   any failed criterion.
9. _(closed)_ Do you accept or reject the current US-05 against its unchanged
   remote SSH and invalid-access criteria? Please name any failed criterion.
10. _(closed)_ Separately from that verdict, is browser-based VS Code acceptable
    instead of remote SSH for the first pilot?
11. _(open)_ What authentication and access-control behavior does the first
    pilot require, regardless of whether access is through a browser or SSH?
12. _(closed)_ When a learner runs the tests, should every test be visible, or
   only a selected subset?
13. _(closed)_ For each QR-01 through QR-05, do you accept its scenario and
    measure, want it changed, or want to defer it? Please give one answer per QR.
14. _(open)_ When you check exercise correctness, isolation, testability,
    response time and reset behavior, what evidence would make each result
    credible for the pilot?
15. _(closed)_ Do you ratify the team's accepted ADR-001, ask us to reconsider
    it, or defer a Customer position on its split between the exercise catalog,
    debug workspace and workspace store?
16. _(closed)_ Do you ratify the team's accepted ADR-002, ask us to reconsider
    it, or defer a Customer position on buggy code, reference code and pytest
    tests for each exercise?
17. _(closed)_ Do you ratify the team's accepted ADR-003, ask us to reconsider
    it, or defer a Customer position on the learner-local persistent workspace
    boundary?
18. _(closed)_ For the pilot, may learner code run on a shared server we deploy,
    or must it run on each learner's own computer until isolation is proven?
19. _(open)_ Looking at the container view and decisions, what is missing or
    surprising to you?
20. _(open)_ Which should come next: assistance inside VS Code that does not edit
    learner files, or category browsing with examples and category-correct
    selection? What outcome makes that choice valuable?
21. _(closed)_ Does this read-back accurately record every decision, rejected or
    deferred item, and action point with its owner and Week 5 due date?

## Roles

Meeting date: 2026-10-26.

Expected participants: `Customer`, `@adelazzi`, `@Danashi11` and `@qwxiae`.
`@adelazzi` asks, `@Danashi11` takes notes, and `@qwxiae` observes and records
what we did not ask.

## Key improvements

### "Is the output of the tests clear enough?" -> "While each story runs, what did you expect to happen at this step that did not?"

The original asks for a judgement of something we already built, and a polite
customer answers yes. The rewrite asks what the customer expected, so a gap
between our result and their expectation shows up as a rejected criterion
instead of a compliment.

### "Would you like us to check the bug with a script?" -> "When you check whether an exercise has the bug it claims, what do you look at?"

The original offers our solution and asks for approval. The rewrite asks about
what the customer does today, so the answer tells us what the quality
requirement for exercise correctness has to measure.

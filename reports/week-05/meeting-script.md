# Meeting script

## Context

Our problem-space sentence: a developer who wants to practise debugging needs
one place where a realistic, multi-file exercise is generated, run with real
debugging tools, and checked against the intended bug, and no product carries
all three in one flow.

Last week's meeting showed the web prototype of the learner flow, so
`US-01` through `US-05` have no Customer verdict, and five open questions are
still open. We believe the locally running flow does what the five stories say,
except for the remote SSH and invalid-access behavior of `US-05`, which are
still unimplemented. The university VM is not available, so there is no
production instance and no deployed test result to show; we show the local
product and the architecture the deployment will follow, and the report will
declare the deviation.

Target: settle whether the locally running learner flow meets the acceptance
criteria of `US-01` through `US-05`, and which route and execution model the
next sprint builds.

## Agenda

1. Permission questions (2 min). Questions 1–3.
   Show: the recording and publication choices in the note taker's document.
2. The Week 4 action points and open questions (5 min). Questions 4–7.
   Show: [the Week 4 action points](../week-04/meeting-report.md#action-points)
   and [open questions](../week-04/meeting-report.md#open-questions).
3. The working software against its acceptance criteria (12 min).
   Questions 8–14.
   Show: the product running locally, one complete scenario from login to
   submitting from VS Code, and the stories
   [US-01](https://github.com/team-ok-ITPD/team-OK-itpd/issues/28),
   [US-02](https://github.com/team-ok-ITPD/team-OK-itpd/issues/29),
   [US-03](https://github.com/team-ok-ITPD/team-OK-itpd/issues/30),
   [US-04](https://github.com/team-ok-ITPD/team-OK-itpd/issues/31) and
   [US-05](https://github.com/team-ok-ITPD/team-OK-itpd/issues/32), one `AC-nn`
   at a time.
4. The quality requirements and the deployment plan (6 min). Questions 15–16.
   Show: [the quality requirements](../../docs/quality-requirements/README.md),
   [the container view](../../docs/architecture/README.md#container-view) and
   [ADR-003](../../docs/architecture/adr/ADR-003.md). No production instance is
   shown, because the university VM is not available.
5. What we build next (3 min). Question 17.
   Show:
   [US-06](https://github.com/team-ok-ITPD/team-OK-itpd/issues/33) and
   [US-07](https://github.com/team-ok-ITPD/team-OK-itpd/issues/34).
6. Read back the decisions and action points (2 min). Question 18.
   Show: the note taker's list.

## Questions

1. _(closed)_ May we record this meeting?
2. _(closed)_ If recorded, may we publish a sanitized transcript in the public
   repository?
3. _(closed)_ May we share the recording or transcript with the course
   instructors if you refuse publication? We will record each permission
   separately.
4. _(open)_ Of the two routes to VS Code we compared, desktop VS Code over SSH
   and VS Code in the browser, which would you ship to pilot learners, and what
   would make you pick the other one?
5. _(closed)_ Should learner code run on a shared server we deploy, or on each
   learner's own computer until isolation is proven?
6. _(closed)_ Should learners see every default test, or only a selected subset?
7. _(open)_ When you check whether an exercise has the bug it claims, what do
   you look at?
8. _(open)_ While each story runs, what did you expect to happen at this step
   that did not?
9. _(closed)_ Do you accept or reject `US-01` against its acceptance criteria,
   one `AC-nn` at a time? Please name any failed criterion.
10. _(closed)_ Do you accept or reject `US-02` against its acceptance criteria,
    one `AC-nn` at a time? Please name any failed criterion.
11. _(closed)_ Do you accept or reject `US-03` against its acceptance criteria,
    one `AC-nn` at a time? Please name any failed criterion.
12. _(closed)_ Do you accept or reject `US-04` against its acceptance criteria,
    one `AC-nn` at a time? Please name any failed criterion.
13. _(closed)_ Do you accept or reject the current `US-05` against its remote
    SSH and invalid-access criteria? Please name any failed criterion.
14. _(open)_ In the complete scenario you just saw, which step would stop a
    pilot learner first?
15. _(closed)_ For each of `QR-01` through `QR-05`, do you accept its scenario
    and measure, want it changed, or want to defer it? Please give one answer
    per requirement.
16. _(open)_ What evidence would make you trust exercise correctness, isolation
    and testability when we test them on the university VM?
17. _(open)_ After what you saw today, what should the next sprint deliver
    first, and what outcome makes that choice valuable?
18. _(closed)_ Does this read-back accurately record every decision, rejected or
    deferred item, and action point with its owner and Week 6 due date?

## Roles

Meeting date: 2026-10-31.

Expected participants: `Customer`, `@UTKANOS-RIBA`, `@Danashi11`, `@qwxiae` and
`@adelazzi`.
`@UTKANOS-RIBA` asks, `@Danashi11` takes notes, and `@qwxiae` observes and
records what we did not ask.
`@adelazzi` runs the product on the screen while it is shown.

## Key improvements

### "Is the workspace good enough to pilot?" -> "While each story runs, what did you expect to happen at this step that did not?"

The original asks the Customer to judge something we built, and a polite
Customer answers yes. The rewrite asks what the Customer expected, so a gap
between our result and their expectation shows up as a rejected criterion
instead of a compliment.

### "Are our quality tests good?" -> "What evidence would make you trust exercise correctness, isolation and testability when we test them on the university VM?"

The original asks for approval of tests that do not exist yet. The rewrite asks
what the Customer would accept as proof, so the answer sets the pass criterion
each test has to meet.

# Meeting script

## Context

Our problem-space sentence: a developer who wants to practise debugging needs
one place where a realistic, multi-file exercise is generated, run with real
debugging tools, and checked against the intended bug, and no product carries
all three in one flow.

We believe the first working slice does what the five stories ask, except that
US-05 asks for SSH and access control while the workspace is browser-based and
has no login. We also believe the five quality requirements and the container
view answer what drives the product: the threshold of success, the constraints,
and the risks. We have not checked the numbers in the requirements with the
customer, and we do not know where learner code may run.

Target: settle whether the customer accepts each of the five finished stories,
whether the quality requirements and the architecture answer what the product
has to achieve, and which story we build next.

## Agenda

1. Permission questions (2 min).  
   Show: nothing.
2. The working software against its acceptance criteria (10 min).  
   Show: the running product, and the stories
   [US-01](https://github.com/team-ok-ITPD/team-OK-itpd/issues/28),
   [US-02](https://github.com/team-ok-ITPD/team-OK-itpd/issues/29),
   [US-03](https://github.com/team-ok-ITPD/team-OK-itpd/issues/30),
   [US-04](https://github.com/team-ok-ITPD/team-OK-itpd/issues/31) and
   [US-05](https://github.com/team-ok-ITPD/team-OK-itpd/issues/32), one `AC-nn`
   at a time. Questions 1–4.
3. The quality requirements (7 min).  
   Show: [the quality requirements](../../docs/quality-requirements/README.md).
   Questions 5–7.
4. The architecture against what drives it (6 min).  
   Show: [the architecture](../../docs/architecture/README.md), its container
   view and its decisions. Questions 8–9.
5. What we build next (3 min).  
   Show:
   [US-06](https://github.com/team-ok-ITPD/team-OK-itpd/issues/33) and
   [US-07](https://github.com/team-ok-ITPD/team-OK-itpd/issues/34). Question 10.
6. Read back the decisions and action points (2 min).  
   Show: the note taker's list.

## Questions

1. _(open)_ While each story runs, what did you expect to happen at this step
   that did not?
2. _(closed)_ Do you accept US-01, US-02, US-03 and US-04 as shown, each against
   its own criteria? Please give one answer per story, and name any criterion it
   failed.
3. _(closed)_ US-05 asks for SSH and access control, and our workspace opens in
   the browser with no login. Is the browser workspace acceptable for the first
   pilot, or must learners connect from their own VS Code?
4. _(closed)_ When a learner runs the tests, should every test be visible, or
   only a selected subset?
5. _(open)_ Of these five requirements, which one would you miss first if it
   were not met?
6. _(open)_ When you check whether an exercise has the bug it claims, what do
   you look at?
7. _(closed)_ Are the numbers in the requirements, such as two seconds for the
   catalog, 30 seconds for the workspace, and five learners at once, the right
   ones for the pilot?
8. _(closed)_ For the pilot, may learner code run on a server we deploy, or must
   it run on each learner's own computer?
9. _(open)_ Looking at what each part of the product does, what is missing or
   surprising to you?
10. _(open)_ Of the stories we have not built, one for help from an agent and one
    for browsing bug categories, which would you miss first if it were not
    built?

## Roles

`@adelazzi` asks, `@Danashi11` takes notes, `@qwxiae` observes and records what
we did not ask.

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

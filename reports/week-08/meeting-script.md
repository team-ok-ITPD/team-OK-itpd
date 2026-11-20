# Week 8 UT-01 Design And Execution Review Script

## Context

Our problem-space sentence: a professor who wants to teach debugging needs one
place where exercises can be created or selected, assigned to groups, solved by
students in a real VS Code environment, and evaluated through automated tests
and submission review.

`UT-01` is designed but no counted session, staging verification or usability
result is claimed yet. Target: settle whether the Customer accepts the planned
test as a way to evaluate the core learner debugging workflow, and agree the
execution plan before sessions begin.

## Agenda

1. Permission questions (3 min). Show: nothing. Questions 1-3.
2. Product status and core learner workflow (5 min). Show: the deployed product
   when it is available from the university network, otherwise the local product
   and [the deployment plan](../../docs/deployment.md). Question 4.
3. UT-01 design and participant plan (12 min). Show: [the UT-01 record](../../docs/usability-tests/ut-01/README.md), its tasks and participant profile. Questions 5-7.
4. Instruments, consent and private evidence (8 min). Show: [the surveys](../../docs/usability-tests/ut-01/surveys.md), [consent](../../docs/usability-tests/ut-01/consent.md), the private-repository arrangement and recordings-folder access record. Questions 8-9.
5. Staging, instrumentation and QR-07 (7 min). Show: [the instrumentation plan](../../docs/usability-tests/ut-01/README.md#instrumentation) and [QR-07 QRT-01](../../docs/quality-requirements/qr/QR-07.md#qrt-01). Questions 10-11.
6. Carried Week 7 action points and product questions (15 min). Show: [the Week 7 report](../week-07/meeting-report.md#action-points) and its [open questions](../week-07/meeting-report.md#open-questions). Questions 12-22.
7. Week 8 execution plan (5 min). Show: [the UT-01 schedule](../../docs/usability-tests/ut-01/README.md#schedule). Question 23.
8. Read back decisions and action points (5 min). Show: the note taker's list. Question 24.

## Questions

1. _(open)_ May we record this meeting?
2. _(open)_ May we publish a sanitized transcript in the repository?
3. _(open)_ If publication is refused, may we share the transcript privately
   with instructors?
4. _(open)_ Does the prepared debugging-exercise workflow shown here still
   represent the learner workflow whose usability you want us to evaluate?
5. _(open)_ Does Task 1's scenario, in which a learner finds, investigates,
   fixes and verifies a prepared Python exercise, answer the most important
   usability question for this workflow?
6. _(open)_ Is the planned participant profile and target of five eligible
   learners, with at least three counted sessions, appropriate for this review?
7. _(open)_ Does the proposed Week 8 arrangement plan give the team enough time
   to recruit, run sessions, analyze results and bring back the outcome?
8. _(open)_ Do the pre-test, task SEQ questions, SUS and post-test capture the
   evidence you need to judge the learner experience?
9. _(open)_ Does the consent and private-evidence plan give participants the
   right recording, withdrawal and deletion protections?
10. _(open)_ Is staging-only verification with a synthetic reset seed and
    `source=usability-test` telemetry the right boundary for the sessions?
11. _(open)_ Is QR-07's median main-task SEQ bar of 5 out of 7 a useful
    usability decision bar for this release?
12. _(open)_ Which fields and drill-downs must the professor see in the
    group-results view for the core workflow to be useful?
13. _(open)_ What is the final exercise-creation flow between the website and
    VS Code, including save, publication and assignment?
14. _(open)_ How should AI assistance be delivered inside the VS Code
    container, and which API-key and quota model is acceptable?
15. _(open)_ How should a professor configure the tools that students can use
    in an exercise environment?
16. _(open)_ Which malicious-code checks are required separately from
    suspicious-solution analysis?
17. _(open)_ What trigger, resource limits and false-positive workflow should
    apply to post-deadline suspicious-solution analysis?
18. _(open)_ Which CSV columns and Moodle grading workflow must the first
    results export support?
19. _(open)_ What should happen to a submission after an assignment deadline?
20. _(open)_ How should students see group-membership changes, assignments and
    notifications?
21. _(open)_ Can one group have multiple professors, and how are university
    accounts verified?
22. _(open)_ If UT-01 exposes a major obstacle, should the team prioritize a
    focused usability fix before further advanced AI integration work?
23. _(open)_ Does the proposed Week 8 execution sequence give the team enough
    time to verify staging, run at least three counted sessions, analyze the
    results and bring the outcome back to you?
24. _(open)_ Does this read-back accurately capture the agreed test direction,
    execution plan, decisions, open questions and action owners?

## Roles

- **Scheduled date:** 2026-11-20.
- **Moderator:** @adelazzi.
- **Note taker:** @Danashi11.
- **Observer:** @qwxiae.
- **Technical presenter:** @UTKANOS-RIBA.
- **Customer:** Customer.
- **All team members:** attend and confirm the read-back.

## Key improvements

### "Is the usability test good?" -> "Does Task 1's scenario answer the most important usability question for this workflow?"

The original asks for a general opinion. The rewrite names the task and asks
whether it answers a decision-relevant question, so the answer can change the
test design before sessions run.

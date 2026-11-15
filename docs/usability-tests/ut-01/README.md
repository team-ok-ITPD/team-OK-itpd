# UT-01: Complete a debugging exercise

- **Status:** Planned
- **Design sprint:** [SPRINT-07](../../project-plan.md#sprint-07)
- **Run sprint:** [SPRINT-08](../../project-plan.md#sprint-08)

## Goal

Evaluate whether representative learners can complete the Debug GYM debugging-practice workflow and identify where they encounter difficulty or need assistance.

## Research Questions

1. Can a representative learner find and open a prepared debugging exercise and reach the point of verifying a fix without assistance?
2. At which points in the workflow do learners hesitate, make errors, or request assistance?
3. How do learners rate the ease of completing the main task and the overall usability of Debug GYM?

## Quality Requirement

This test will serve [QR-07](../../quality-requirements/qr/QR-07.md), the Interaction Capability usability requirement. Its sub-characteristic, measure, and pass criterion are to be defined in Part 5 before the first counted session.

## Participant Profile

To be completed in Part 6. The intended participant is an adult (18 or older) representative of a learner who practises debugging tasks. The profile must specify their role and relevant task, familiarity with similar products, device, and relation to the target user before recruitment.

## The Tasks

To be completed in Part 3. The test will use one main usability test task followed by two secondary usability test tasks. Their scenarios, start points, end states, success criteria, time limits, help rule, and fixed order must be finalized before the first counted session.

## Protocol

To be completed in Part 3. Every counted session will follow the same written protocol, including consent, pre-test, think-aloud observation, task execution, SEQ after each task, SUS, open-ended post-test, and debrief.

## Measures

To be completed in Part 3. Planned measures include task completion and assistance, time on task, SEQ after each task, SUS after all tasks, and qualitative observations.

## Instrumentation

To be completed in Part 3. The design must identify the Week 6 analytics events reused, any added events or test-only records, the session-linking method, the data store, and the verification before the first counted session. Test telemetry must use `source=usability-test` and must not reach production.

## Analysis Plan

To be completed in Part 7 before the first counted session. It will define the per-participant table, aggregate task measures, SEQ and SUS summaries, thematic analysis, severity ratings, instrumentation comparison, and limitations.

## Schedule

- Design: [SPRINT-07](../../project-plan.md#sprint-07).
- Planned run: [SPRINT-08](../../project-plan.md#sprint-08).
- Arrange at least three completed sessions with representative adults aged 18 or older; five is the design target.
- Exact session dates are not yet recorded. The team will arrange sessions and record their sprint allocation here.
- Results are due with Submission 8. Week 7 makes no usability-results claim.

## Roles

To be completed with the responsible team members' GitHub usernames before sessions:

- **Facilitator:** TBD
- **Observer:** TBD
- **Recording and raw-notes custodian:** TBD

## Environment

The required environment is the staging deployment on the university network, using seeded synthetic data reset before each session. No real payment is made. The exact staging URL, seed/reset procedure, and readiness evidence must be recorded before the first counted session.

## Consent And Data

Obtain durable consent before every counted session, including consent to recording and sanitized public results. The public repository will contain only sanitized records and aggregate findings. Consent records, identity mapping, raw notes, recordings, and the test's filtered telemetry export belong in the private usability-data repository and team-owned cloud recordings folder. Their locations and access instructions must not be published here. The private repository and recordings are to be deleted after the course is graded; the sanitized public record remains.

## Evidence Map

| Evidence | Location | Visibility |
| --- | --- | --- |
| Test design, surveys, public consent template, sanitized session notes, results and sanitized images | This `docs/usability-tests/ut-01/` directory | Public, sanitized |
| Signed consent, participant identity mapping, raw notes, working analysis and filtered test telemetry export | Team's private `<organization>/<repo>-usability-data` repository (to be created) | Private; team and instructors |
| Session recordings | Team-owned cloud folder (to be created) | Private; team and instructors |
| Moodle submission wrapper and any required private access instructions | Moodle | Course submission |
| Results, findings and triage handoff | Week 8 report and this test's `results.md` | Public, sanitized |

No participant identity, raw participant data, private repository URL, or recording-folder URL belongs in this product repository.

## Results

See [results.md](results.md). It is intentionally a stub until the Week 8 results submission.

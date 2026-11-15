# UT-01: Debugging-Practice Workflow

- **Status:** Planned
- **Design sprint:** [SPRINT-07](../../project-plan.md#sprint-07)
- **Run sprint:** [SPRINT-08](../../project-plan.md#sprint-08)

## Goal

Assess whether representative learners can independently complete Debug GYM's prepared debugging-exercise workflow.

## Research Questions

1. Can a representative learner locate, open, debug and verify the prepared exercise without help?
2. Where do learners hesitate, make errors or need help in that workflow?
3. How easy do learners rate each task and the product overall?

## Quality Requirement

This test serves [QR-07](../../quality-requirements/qr/QR-07.md). Its manual test reads the main task's median SEQ from [results.md](results.md).

## Participant Profile

Recruit five, with at least three completed and countable sessions, of adults aged 18 or older who are not team members, the Customer, instructors or course staff. Each participant must be a learner who has used Python coursework or comparable programming exercises, may have limited debugging-tool experience, and uses a university-network laptop browser. A classmate is eligible only when they meet this profile. Assign `P-01`, `P-02` and onward in arrangement order; a withdrawn, unrecorded or broken session is not counted and its replacement receives the next free code.

The team will recruit through eligible classmates and university programming-study contacts, screen against this profile, then arrange in-person university-network sessions in SPRINT-08. Exact identities, contact details and dates stay private.

## The Tasks

Tasks are administered in this fixed order. The facilitator reads only the scenario and start point; no task names a screen, control or step.

### Task 1: Complete A Prepared Debugging Exercise (main)

- **Scenario:** You need to practise fixing a Python problem before a class exercise. Find a suitable prepared task, investigate why it fails, make a correction and check whether your correction works.
- **Start point:** Signed-in staging home with the synthetic test account and reset seed.
- **End state:** The participant has requested verification after saving a correction.
- **Success criterion:** `Unaided` when verification reports all tests passing without facilitator help; `Assisted` when it does after help; `Failed` when it does not happen within 20 minutes or the participant stops.
- **Time limit:** 20 minutes.

### Task 2: Reproduce The Problem

- **Scenario:** Before changing a proposed solution, establish what is wrong and gather enough evidence to explain it to a classmate.
- **Start point:** The same reset exercise in the prepared workspace.
- **End state:** The participant can describe an observed failing result from their own run.
- **Success criterion:** `Unaided` when this is achieved without facilitator help; `Assisted` when it is achieved after help; `Failed` after 8 minutes or on stop.
- **Time limit:** 8 minutes.

### Task 3: Return To The Exercise

- **Scenario:** After checking your work, return to the exercise information and identify what you would do next if the correction did not work.
- **Start point:** The state left by Task 2.
- **End state:** The participant reaches the exercise information and states a plausible next debugging action.
- **Success criterion:** `Unaided` when this is achieved without facilitator help; `Assisted` when it is achieved after help; `Failed` after 5 minutes or on stop.
- **Time limit:** 5 minutes.

Help means the facilitator supplies a navigation, interpretation or technical hint beyond repeating the scenario. The facilitator records the request and gives one neutral, minimum hint; a second hint ends that task as `Assisted`.

## Protocol

Follow [the session template](sessions/README.md). Order: welcome; consent and recording check; pre-test; think-aloud instruction; Tasks 1-3 with observation and SEQ after each; SUS; open post-test; debrief. The facilitator does not teach, correct, or demonstrate a task. Stop immediately if the participant withdraws, declines recording, requests to stop or a material technical failure prevents the task; do not count that session.

## Measures

Record each task's outcome, help, time from scenario reading to end state, and the seven-point SEQ. After all tasks record the ten SUS responses and calculate the score in [surveys.md](surveys.md). The observer also records observable friction and think-aloud statements in private raw notes. Main-task completion/assistance, median time, median SEQ, SUS mean/median and thematic findings are analysis outputs; QR-07 reads only median main-task SEQ.

## Instrumentation

The staging session reuses `exercise_searched`, `exercise_opened`, `workspace_opened` and `solution_verified` from [the event table](../../analytics.md#the-events). Set `DEBUG_GYM_ANALYTICS_SOURCE=usability-test` only on staging for the recorded UTC session window, then restore `web`; never use this setting in production. Link events to a session through that UTC window plus the staging test account's opaque `learner_id`; keep the account-to-`P-nn` mapping and filtered export private. The events go to the staging analytics store and must carry `source=usability-test`.

The observer sheet and surveys are test-only private records. Instrumentation can corroborate search, exercise open, workspace open and server verification; it cannot measure think-aloud, facilitator help, SEQ, SUS, or why a participant struggled. Before the first counted session, a teammate runs Task 1 on staging, confirms the records reach the named store and confirms the UTC window and opaque identifier isolate that run. This verification is planned, not completed.

## Analysis Plan

Before sessions, create a private per-participant table with participant code, profile screen, each task's outcome/help/time/SEQ, SUS, notable observations, event-window match and technical failures. Report aggregate main-task completion and assistance, median main-task time, median SEQ for each task, QR-07's median main-task SEQ against its bar, and SUS mean and median. The team will code observations into themes, rate each finding as low, medium or high severity by impact and persistence, compare observed task flow against the telemetry window, and state limitations including sample size, staging-only conditions and instrumentation gaps.

Every finding is triaged. A significant finding produces a SPRINT-08 task issue that cites [Finding 1](results.md#finding-1), names the affected `FR-nnn` or `ADR-nnn`, and links the relevant story and acceptance criterion.

## Schedule

- **SPRINT-07:** complete design, obtain private-data access, dry run and schedule instrumentation verification.
- **SPRINT-08:** arrange and run the five-target/three-minimum counted sessions, sanitize notes, analyse results, triage findings and settle QR-07.

No counted session, dry run or instrumentation verification is claimed yet.

## Roles

Before the first counted session, the team records the GitHub usernames of one facilitator for every session, one observer, and one recordings/raw-notes custodian in the private data repository. They are intentionally unassigned here because no team allocation has been recorded.

## Environment

Use the staging deployment on the university network with a synthetic seeded exercise reset before every session and no real payment. Confirm staging availability, the reset procedure, the opaque participant link and `source=usability-test` telemetry before the first counted session. Staging availability and this verification are pending.

## Consent And Data

Use [the public consent template](consent.md) before every counted session. The private [usability-data repository](https://github.com/team-ok-ITPD/team-OK-itpd-usability-data) exists but must receive instructor access and its team-owned recordings folder before any counted session; authenticated access instructions remain private. That repository holds signed consents, identity mapping, raw notes, working analysis, filtered telemetry export and the recordings-folder access record. Delete it, its history and recordings after course grading; retain only sanitized public records.

## Evidence Map

| Evidence | Location | Visibility |
| --- | --- | --- |
| Design, instruments, sanitized results and images | This `ut-01/` directory | Public, sanitized |
| Consent, identity mapping, raw notes, analysis and telemetry export | Private usability-data repository | Private |
| Recordings and folder access | Team-owned cloud folder | Private |
| Private access instructions | Moodle wrapper | Course-only |
| Results, findings and triage | [results.md](results.md) and Week 8 report | Public, sanitized |

## Results

See [results.md](results.md). It remains a stub until SPRINT-08 analysis.

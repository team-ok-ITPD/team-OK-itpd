# Week 07 report

## Project

- **Project:** Debug GYM
- **Team:** Team 02
- **Week:** Week 7, Usability Test Design And The Week 7 Release
- **Release:** `REL-07`, the tag [`v0.4.0`](https://github.com/team-ok-ITPD/team-OK-itpd/releases/tag/v0.4.0), is a cumulative release because `REL-06` was not cut.

## Summary

The `UT-01` usability test is designed and its recruitment is planned; no usability result is claimed. [The `UT-01` record](../../docs/usability-tests/ut-01/README.md) holds the goal, the research questions, the participant profile, one main and two secondary tasks, the measures, the instrumentation, the analysis plan, the [session plan](../../docs/usability-tests/ut-01/README.md#schedule), the roles and the evidence map. [The surveys](../../docs/usability-tests/ut-01/surveys.md) hold the pre-test, the SEQ after each task, the full ten SUS items and the open-ended post-test, and [the consent template](../../docs/usability-tests/ut-01/consent.md) is ready to collect. The test serves [QR-07](../../docs/quality-requirements/qr/QR-07.md), whose manual [QRT-01](../../docs/quality-requirements/qr/QR-07.md#qrt-01) reads the main task's median SEQ against a bar of 5 of 7. The recruitment target is five participants with at least three counted sessions; the participant profile is an adult learner outside the team who has used Python coursework or comparable exercises.

The test's instrumentation reuses four Week 6 events and marks them with `source=usability-test` on staging. The marking is implemented and covered by automated tests. It was **not verified** on a staging deployment, because the university VM was unavailable; the verification and a dry run are scheduled in `SPRINT-08` before the first counted session. The private [usability-data repository](https://github.com/team-ok-ITPD/team-OK-itpd-usability-data) exists and will hold the consent records, identity mapping, raw notes, analysis and the filtered telemetry export. The recordings folder is the team's cloud folder, and its link and access are in the Moodle submission. Instructor access to both is not confirmed in this report.

The focus metric, [solved exercises per active learner per week](../../docs/analytics.md), has no value yet: it needs a deployed analytics backend and learners outside the team using the product. No metric is computed here, and no test or smoke traffic is presented as a value. The [analytics plan](../../docs/analytics.md) and the [observability plan](../../docs/observability.md) hold the queries and signals.

The Week 7 Customer meeting did not review the `UT-01` design, so the design and the Week 8 plan are not yet agreed with the Customer; see [Deviations](#deviations). The meeting's transcript is not published, and its sanitized notes are in [meeting-notes.md](meeting-notes.md). The testing-plan rows that are not `Passes` are in [the testing plan](../../docs/project-plan.md#quality-requirement-testing-plan).

## Customer Meeting Outcome

The meeting held on 2026-11-13 settled the role model and the group-first teaching workflow, and produced [DEC-039](../../docs/decisions.md#dec-039) through [DEC-043](../../docs/decisions.md#dec-043). It showed no `UT-01` design, accepted or rejected no story, and moved no candidate story out. Its outcome, the Week 6 action points and open questions, and the new action points are in [the meeting report](meeting-report.md).

## Minimum Usable Product Candidate

The latest tagged candidate is [`v0.4.0`](https://github.com/team-ok-ITPD/team-OK-itpd/releases/tag/v0.4.0), which includes the Week 5 learner flow and the Week 6 sharing and verification changes. It has CI and local-container evidence but no staging or production deployment evidence.

## Usability Test

**Design.** One main task, completing a prepared debugging exercise, and two secondary tasks, reproducing the problem and returning to the exercise information, are the same for every participant in a fixed order, each with an `Unaided`, `Assisted` or `Failed` criterion, a time limit and a help rule. See [the tasks](../../docs/usability-tests/ut-01/README.md#the-tasks) and [the session template](../../docs/usability-tests/ut-01/sessions/README.md).

**Recruitment target and participant profile.** Five participants, at least three counted sessions, adults aged 18 or older who are not team members, the Customer, instructors or course staff. Codes `P-01` onward are assigned in the order the sessions are arranged. See [the profile](../../docs/usability-tests/ut-01/README.md#participant-profile).

**Surveys.** [The surveys](../../docs/usability-tests/ut-01/surveys.md) hold the pre-test, the SEQ after each task, the SUS with its formula, and the open-ended post-test.

**Instrumentation and verification.** The test reuses `exercise_searched`, `exercise_opened`, `workspace_opened` and `solution_verified`, linked to a session by its UTC window and an opaque learner identifier. It cannot cover think-aloud, help, SEQ, SUS or why a participant struggled. See [the instrumentation](../../docs/usability-tests/ut-01/README.md#instrumentation). No verification has been run; it is scheduled in `SPRINT-08` before the first counted session.

**Consent and private repository.** [The consent template](../../docs/usability-tests/ut-01/consent.md) carries the age declaration, the recording, the sanitized public results, the optional quote, the private access, the tools used, the withdrawal and the deletion after grading. The private [usability-data repository](https://github.com/team-ok-ITPD/team-OK-itpd-usability-data) and the recordings folder are deleted after the course is graded; the sanitized public record stays. The repository link is excluded from the link check in `.lycheeignore` because opening it needs authenticated course access.

**Recordings folder.** The team's cloud folder; its link and access instructions are in the Moodle submission only.

**Session plan.** The team contacts eligible classmates from 2026-11-16, aims to confirm three participants by 2026-11-17 and to run the sessions between 2026-11-18 and 2026-11-20, in person on the university network against staging. See [the schedule](../../docs/usability-tests/ut-01/README.md#schedule).

**Quality requirement and test.** [QR-07](../../docs/quality-requirements/qr/QR-07.md) is an `Interaction Capability` requirement with the `Operability` sub-characteristic, and its manual [QRT-01](../../docs/quality-requirements/qr/QR-07.md#qrt-01) is `Not verified`, planned for `SPRINT-08`.

**Week 8 handoff.** The recruitment target, the participant profile and the session plan are set. The [`results.md`](../../docs/usability-tests/ut-01/results.md) stub, the findings template and the triage plan are in place. Still to do before the first counted session: confirm that the instructors can open the private repository and the recordings folder, verify the instrumentation on staging, run the dry run, and present the design to the Customer and agree the results date. The results, findings, verdict and triage are due with Submission 8, and no result is claimed here.

## Coverage

| Deliverable | Artifact |
| --- | --- |
| Sprint plan | [docs/project-plan.md#sprint-07](../../docs/project-plan.md#sprint-07) |
| `UT-01` test record | [docs/usability-tests/ut-01/README.md](../../docs/usability-tests/ut-01/README.md) |
| Surveys and post-test | [docs/usability-tests/ut-01/surveys.md](../../docs/usability-tests/ut-01/surveys.md) |
| Tasks and protocol | [docs/usability-tests/ut-01/README.md#the-tasks](../../docs/usability-tests/ut-01/README.md#the-tasks) and [docs/usability-tests/ut-01/sessions/README.md](../../docs/usability-tests/ut-01/sessions/README.md) |
| Test instrumentation | [docs/usability-tests/ut-01/README.md#instrumentation](../../docs/usability-tests/ut-01/README.md#instrumentation) and [docs/analytics.md#the-events](../../docs/analytics.md#the-events) |
| Consent template | [docs/usability-tests/ut-01/consent.md](../../docs/usability-tests/ut-01/consent.md) |
| Private usability-data repository | The private usability-data repository, linked from the record and this report and excluded from the link check |
| Recordings folder | The team's cloud folder, linked in the Moodle submission only |
| `QR-nn` and its test | [docs/quality-requirements/qr/QR-07.md](../../docs/quality-requirements/qr/QR-07.md) and its [QRT-01](../../docs/quality-requirements/qr/QR-07.md#qrt-01) |
| Recruitment target and session plan | [docs/usability-tests/ut-01/README.md#participant-profile](../../docs/usability-tests/ut-01/README.md#participant-profile) and [docs/usability-tests/ut-01/README.md#schedule](../../docs/usability-tests/ut-01/README.md#schedule) |
| Week 8 handoff | [reports/week-07/README.md#usability-test](#usability-test) |
| Glossary | [docs/glossary.md](../../docs/glossary.md) |
| Risk register | [docs/risks.md](../../docs/risks.md) |
| Week 6 action points | [## Previous action points](meeting-report.md#previous-action-points) in `reports/week-07/meeting-report.md` |
| Week 6 open questions | [## Previous open questions](meeting-report.md#previous-open-questions) in the same report |
| Sprint Review | [reports/week-07/meeting-report.md](meeting-report.md); it did not review the `UT-01` design |
| Meeting script | [reports/week-07/meeting-script.md](meeting-script.md) |
| Meeting transcript | Not published: only the sanitized notes in [reports/week-07/meeting-notes.md](meeting-notes.md) are committed |
| `REL-07` | [v0.4.0](https://github.com/team-ok-ITPD/team-OK-itpd/releases/tag/v0.4.0), [CHANGELOG.md](../../CHANGELOG.md#040---2026-11-15) and [docs/project-plan.md#rel-07](../../docs/project-plan.md#rel-07) |
| Sprint retrospective | [reports/week-07/sprint-retrospective.md](sprint-retrospective.md) |
| AI usage | [reports/week-07/ai-usage.md](ai-usage.md) |

## Contribution

| Member | Evidence |
| --- | --- |
| [@adelazzi](https://github.com/adelazzi) | Named facilitator of the `UT-01` sessions in [the record](../../docs/usability-tests/ut-01/README.md#roles); owner of the Week 8 design-presentation action in [the meeting report](meeting-report.md#action-points). |
| [@Danashi11](https://github.com/Danashi11) | Named observer in [the record](../../docs/usability-tests/ut-01/README.md#roles); owner of the CSV-export schema action in [the meeting report](meeting-report.md#action-points). |
| [@qwxiae](https://github.com/qwxiae) | Named instrumentation verifier in [the record](../../docs/usability-tests/ut-01/README.md#roles); owner of the tool-configuration action in [the meeting report](meeting-report.md#action-points). |
| [@UTKANOS-RIBA](https://github.com/UTKANOS-RIBA) | Named recordings and raw-notes custodian in [the record](../../docs/usability-tests/ut-01/README.md#roles); owner of the suspicious-submission review action in [the meeting report](meeting-report.md#action-points). |

TODO(before submit): add each member's merged pull requests and reviews for this week.

## Repository Evidence

TODO(before submit): link the merged pull request that closed a `SPRINT-07` task issue, and the latest green link-check, Markdown-check, `actionlint` and product-code runs on `main`.

The link check excludes only the private usability-data repository, because opening it needs authenticated course access; the exclusion and its reason are in `.lycheeignore`.

## Deviations

- The Week 7 Customer meeting on 2026-11-13 did not review the `UT-01` design. Its agenda covered roles, the teaching workflow, VS Code, AI and architecture, so no `DEC-nnn` records feedback on the test, and the Week 8 plan and the results date are not agreed with the Customer. The team action in [the meeting report](meeting-report.md#action-points) presents the design at the Week 8 meeting.
- The instrumentation verification and the dry run are not run, because the university VM and staging were unavailable. Both are scheduled in `SPRINT-08` before the first counted session.
- The recordings folder and the instructors' access to the private repository and the folder are not confirmed in this report.
- `QR-02 QRT-01` and `QR-06 QRT-01`, planned for `SPRINT-07`, moved to `SPRINT-08` because no deployed environment was available to run them.
- `REL-06` was never cut, so `REL-07` is a cumulative release and not a docs-only one.
- No transcript of the Week 7 meeting is published; its sanitized notes are committed.
- Two of the four Week 6 action points and most Week 6 open questions were not addressed at the Week 7 meeting and remain open, as [the meeting report](meeting-report.md#previous-action-points) records.

## Privacy

No private-only material was committed to this repository, and no participant identity was committed to it.

# Sprint 9 retrospective — preparation draft

**Status:** The team's actual retrospective discussion, participants and agreed
actions have not been supplied. This file is a preparation scaffold, not a
claim that the ceremony took place or that the team agreed the observations.

## Evidence To Discuss

- The [Customer review](meeting-report.md#user-acceptance-tests) includes an
  explicit student-UAT passing statement and a successful professor-account
  sign-in, but the fresh professor-assignment journey was blocked.
- Advance UAT definitions, reviewed builds and permissions were not found in
  the supplied repository record. These evidence gaps remain visible rather
  than being backfilled as completed preparation.
- The recording contains changing requirements and explicitly deferred
  features; distinguish fixes from additions before Sprint 10 scheduling.

## Team Discussion Pending

| Topic | Question for the team |
| --- | --- |
| What worked | Which preparation and collaboration practices helped demonstrate the working account/student flows? |
| What did not | Why did the assignment blocker reach the review, and which checks would have exposed it earlier? |
| Evidence | How will the next review capture its build, original tests, actual runners and three permission answers? |
| Scope | How will the team separate required fixes, UI polish and explicitly deferred features before handoff? |

## Proposed Conclusions For Team Review

### Keep

- Demonstrate complete user journeys instead of isolated screenshots: the
  student correction/submission and account sign-in exposed observable results.
- Read back requested changes and separate fixes from future features.
- Retain failed observations: the assignment blocker was not hidden by showing
  an export from pre-existing data.

These are evidence-based proposals, not quotations of team sentiment.

### Change

- Run a fresh professor → student → professor-results rehearsal before the
  Customer review. Existing demo data should not substitute for the new run.
- Capture the exact deployed tag/commit, environment and actual runner once
  at the start; keep local and university-VM evidence separate.
- Prepare the three UATs, start states and script before the next review.
- Classify hidden-test/security/quality claims separately from a working UI demo.
- Reserve time for fixes, independent review, release and submission after
  the Customer meeting.

## Proposed Improvement Experiments

Owners and deadlines are unassigned until the team agrees them. Each experiment
has a concrete completion check rather than a claim of an already-held ceremony.

| Proposal | Completion check | Proposed deadline | Owner |
| --- | --- | --- | --- |
| Fresh multi-role rehearsal | A new exercise is assigned, a member submits as a student, and the professor exports that new result. | Before Sprint 10 review. | Team to assign. |
| Build/evidence header | Review notes start with full commit, tag if any, deployment identity and runner; no secret URL is published. | Before Sprint 10 review. | Team to assign. |
| Freeze the test script | Exactly three retained UAT definitions and start states are linked before the review; later amendments are explicit. | Before Sprint 10 review. | Team to assign. |
| Review readiness gate | Outstanding blockers and quality tests without evidence are read back before scheduling handoff acceptance. | Before handoff. | Team to assign. |

## Team Confirmation Still Required

- Actual discussion date and whether this retrospective was held.
- Which observations and experiments the team agrees to keep.
- Owner usernames and agreed deadlines; links to scheduled tasks where needed.
- Any real disagreement or additional lessons, in the team's own words.

Until confirmed, this document is an AI-assisted proposal, not the completed
Sprint 9 retrospective. No team vote, attendance, agreement or sentiment is
invented, and no past date should be added to imply advance preparation.

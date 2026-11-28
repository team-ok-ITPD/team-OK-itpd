# UT-01 Results

## Late Supplement And Shortfall

**Documented:** 2026-11-27, after the Assignment 8 deadline of 2026-11-21.

The team reports three real sessions: P-01 and P-02 on 2026-11-26,
and P-03 on 2026-11-27. Consent to participation was obtained.
On 2026-11-28, the team reconfirmed that all three sessions involved real
people.
The team reports that the instructor personally approved an exception to the
recording requirement for these sessions. This is a team-reported clarification,
not a change to the published course rule. UT-01 remains `Planned` because
the staging and prior instrumentation-verification conditions remain unmet.
This is a qualitative record of the supplied notes, not a completed study
or a passing quality-requirement test.

The team supplied notes and survey responses. No telemetry export or
pre-session instrumentation-verification record is available.
The following summaries omit demographic combinations, raw responses,
participant quotations, local addresses and private operational details.

## Results Table

Outcomes below describe observed actions, not protocol-compliant success
classifications. Missing timing and different verification paths prevent
retrospective classification against the fixed criteria.

| Session | Task 1 and assistance | Task 2 | Task 3 | Timing coverage |
| --- | --- | --- | --- | --- |
| [UT-01 P-01](sessions/P-01.md) | Own example confirmed correction; technical help and terminal editing; no passing test suite | Reproduced shared-list behaviour; reset retained diagnostic calls | Returned after retry; proposed further checks | Not measured |
| [UT-01 P-02](sessions/P-02.md) | Own example confirmed correction on a separate file; no passing test suite; submission not attempted | Reproduced shared-list behaviour | Returned with browser Back; proposed breakpoint | Not measured |
| [UT-01 P-03](sessions/P-03.md) | Three tests passed after technical help; optional submission rejected | Fresh failing test supported explanation after organizer reset | Opened exercise separately after Back did not complete | Partial intervals only; see session |

### SEQ And SUS Coverage

Individual SEQ and calculated SUS scores are preserved in the linked sanitized
notes as descriptive observations only. Acceptance of these local sessions
against the remaining protocol conditions has not been established.
No completion rate, median task time, median SEQ, SUS mean or SUS median
is claimed for the planned staging test. The three exploratory records
are not evidence of population usability or QR-07 compliance.

## Thematic Analysis

- **Unclear verification:** P-01 and P-02 could run their own examples but
  found the available Test control inconsistent with an exercise without tests.
- **Completion uncertainty:** P-01 and P-03 encountered rejected submissions
  and an ambiguous saved-status indicator after editing.
- **Environment readiness:** P-01 and P-03 required organizer intervention
  before the editor could open in the local environment.
- **Navigation friction:** P-01 and P-03 encountered a browser dialog on
  return; P-03 used a separate tab. P-02 returned directly.

Selecting practice was understandable in all three notes. P-03 could interpret
the failing boundary test and recognize passing tests after correction.

## Findings

These are provisional findings from local sessions, not confirmed
defects on staging. Severity describes observed impact, not frequency.

### Finding 1

- **Severity:** Major — the Test control did not provide a usable verification
  result for an exercise without tests, leaving the main task's criterion unmet.
- **Tasks:** UT-01 Task 1 with UT-01 P-01 and UT-01 P-02.
- **Evidence:** [P-01](sessions/P-01.md#observations) and
  [P-02](sessions/P-02.md#observations).
- **Recommendation:** Explain when tests are unavailable and provide an explicit
  expected-output example or a usable verification path.
- **Task issue:** None.

### Finding 2

- **Severity:** Major — submission rejection prevented confirmation of delivery,
  although submission is additional to Task 1's verification end state.
- **Tasks:** UT-01 Task 1 with UT-01 P-01 and UT-01 P-03.
- **Evidence:** [P-01](sessions/P-01.md#observations) and
  [P-03](sessions/P-03.md#observations).
- **Recommendation:** Reproduce in the supported practice environment and provide
  a specific recovery action; distinguish file saving from submission status.
- **Task issue:** None.

### Finding 3

- **Severity:** Major — editor launch was blocked until technical intervention.
  This concerns local environment preparation; a deployed defect is not established.
- **Tasks:** UT-01 Task 1 with UT-01 P-01 and UT-01 P-03.
- **Evidence:** [P-01](sessions/P-01.md) and [P-03](sessions/P-03.md).
- **Recommendation:** Verify editor connectivity before sessions and distinguish
  unavailable connection from a stopped runtime in diagnostics.
- **Task issue:** None.

### Finding 4

- **Severity:** Minor — returning to the exercise required retries or a workaround,
  but the information was eventually accessible.
- **Tasks:** UT-01 Task 3 with UT-01 P-01 and UT-01 P-03.
- **Evidence:** [P-01](sessions/P-01.md#observations) and
  [P-03](sessions/P-03.md#observations); [P-02](sessions/P-02.md) returned normally.
- **Recommendation:** Provide an explicit return-to-exercise link and clarify
  the meaning of saved status.
- **Task issue:** None.

## Triage

| Finding | Disposition | Issue and scheduling |
| --- | --- | --- |
| [Finding 1](#finding-1) | Candidate: verify no-tests behaviour and expected output | None; not scheduled |
| [Finding 2](#finding-2) | Candidate: reproduce practice submission rejection and status ambiguity | None; not scheduled |
| [Finding 3](#finding-3) | Candidate: environment preflight before rerun; no deployed defect claimed | None; not scheduled |
| [Finding 4](#finding-4) | Candidate: check ordinary browser exit and explicit return link | None; not scheduled |

No issue or product fix was created by this documentation update. Significant
findings still require team triage into task issues with story/AC and FR/ADR
traceability. The assignment's issue/scheduling requirement is not yet met.
These late observations cannot be backdated into SPRINT-08 or claimed as
fixes delivered in REL-08. No Customer decision or implementation commitment
is inferred from participant suggestions.

## Instrumentation Comparison

| Planned evidence | Available evidence | Comparison |
| --- | --- | --- |
| `exercise_searched`, `exercise_opened` | Navigation described in notes | No event export; cannot match participant windows |
| `workspace_opened` | Editor opening and technical intervention described | No event export or prior verification evidence |
| `solution_verified` | Own examples for P-01/P-02; IDE test result for P-03 | Neither establishes the planned server event |
| Task 2 explanation and Task 3 return | Observer summaries | Planned events do not cover explanation or return |
| Help, SEQ and SUS | Supplied notes and surveys | These require observation/survey, not inferred telemetry |

The reported local submission rejection in P-03 is an observation from the
supplied note, not an independently inspected log export. No funnel conversion,
timing comparison, analytics isolation or production metric is claimed.

## Limitations

- Three local sessions; their acceptance against the remaining protocol
  conditions has not been established.
- Local macOS/Chromium environments rather than university staging; network,
  same-facilitator and two-team-member conditions are not established.
- Notes describe adult Python learners familiar with VS Code, but complete
  exclusion screening and durable consent scope were not supplied for review.
  Consent to participation is team-confirmed; no quotations are published.
- Two exercises differ: P-01/P-02 used Mutable default argument; P-03 used
  Adult check is off by one. Verification methods and assistance differ.
- P-01/P-02 lack measured time; P-03 has partial intervals, not comparable
  whole-task timings. P-01's Task 2 reset was incomplete.
- Repeated tasks introduce learning effects. Stepwise debugging was not tested.
- Notes were sanitized retrospectively, not published on each session day.
  Private storage/access, instrumentation verification and telemetry are unverified.

## Conclusion

1. **Independent completion:** not established. P-01/P-02 checked an example
   rather than a passing suite; P-03 passed tests after technical help.
2. **Friction and help:** local editor startup, unclear verification,
   submission recovery and returning to the exercise are the candidate
   improvements in Findings 1–4.
3. **Perceived ease:** individual ratings are documented in session notes,
   but this shortfall record supports no aggregate usability conclusion.

[QR-07 QRT-01 remains Not verified](../../project-plan.md#quality-requirement-testing-plan).
The threshold goals are not settled by these observations: TOS-01 requires
timely debugger evidence and TOS-03 requires five usefulness responses and
Customer acceptance, neither supplied here.

The documentation response is this late, sanitized qualitative supplement.
Product recommendations remain candidates, not approved changes. No product
change is committed to or declined on the strength of these notes alone:
supported-environment reproduction and team prioritization are still needed.
Completing UT-01 requires consented, profile-screened sessions on the verified
staging path, or instructor approval of the remaining protocol deviations.
The team-reported recording exception does not establish either of those.

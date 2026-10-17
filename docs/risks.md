# Risks

| ID | Status | Impact | Likelihood | Risk |
| --- | --- | --- | --- | --- |
| [RISK-01](#risk-01) | Open | High | High | The Week 3 build started after most of the sprint elapsed, so the working slice may miss the deadline, which would leave `MLS-03` undelivered. |
| [RISK-02](#risk-02) | Open | High | Medium | The browser IDE depends on Docker images and extension downloads, so an unavailable dependency may prevent the environment from starting, which would block the core task. |
| [RISK-03](#risk-03) | Open | High | Medium | Learner code runs in a shared service without a settled isolation architecture, so unsafe code may affect other users or infrastructure, which would prevent a public pilot. |
| [RISK-04](#risk-04) | Open | Medium | High | The draft threshold has not been reviewed by the Customer, so its measures may not reflect Customer priorities, which would make progress evidence irrelevant. |

## RISK-01

The Week 3 build started after most of the sprint elapsed, so the working slice may miss the deadline, which would leave `MLS-03` undelivered.

- **Status:** Open
- **Impact:** High
  - The first planned increment and release depend on an end-to-end working
    slice, so documentation alone cannot satisfy the sprint goal.
- **Likelihood:** High
  - Product implementation began on the hard-deadline day and still requires a
    reviewed pull request.
- **Trigger:** the clean-checkout rehearsal has not passed before the release
  task is ready for review.
- **Window:** [SPRINT-03](project-plan.md#sprint-03).
- **Mitigation:** keep the slice to one curated exercise and reuse the proven
  Docker and code-server prototype direction.
- **Contingency:** publish the tested one-exercise harness as the release and
  reschedule unmerged enhancements into `SPRINT-04`.

## RISK-02

The browser IDE depends on Docker images and extension downloads, so an unavailable dependency may prevent the environment from starting, which would block the core task.

- **Status:** Open
- **Impact:** High
  - A learner cannot reproduce, debug, or verify the exercise if code-server
    does not start.
- **Likelihood:** Medium
  - The Week 2 spike ran successfully, but a clean machine still has to download
    external images and extensions.
- **Trigger:** the image build or a clean start fails while fetching a pinned
  dependency.
- **Window:** `MLS-03` and each later deployment.
- **Mitigation:** pin the base image and Python dependencies and rehearse the
  documented clean-checkout path.
- **Contingency:** distribute the same exercise as a Dev Container configuration
  that opens in the learner's installed VS Code.

## RISK-03

Learner code runs in a shared service without a settled isolation architecture, so unsafe code may affect other users or infrastructure, which would prevent a public pilot.

- **Status:** Open
- **Impact:** High
  - A security incident would stop learner trials and threaten the delivery
    plan and repository's public standing.
- **Likelihood:** Medium
  - Docker provides a boundary, but resource limits and hostile-code controls
    have not yet been validated.
- **Trigger:** a test program accesses host resources, another learner's files,
  or exceeds its configured resource allowance.
- **Window:** [SPRINT-04](project-plan.md#sprint-04) through the first public
  pilot.
- **Mitigation:** test container boundaries and define CPU, memory, process, and
  filesystem limits before accepting untrusted code.
- **Contingency:** run exercises only on each learner's own computer until the
  server-side isolation design passes its safety checks.

## RISK-04

The draft threshold has not been reviewed by the Customer, so its measures may not reflect Customer priorities, which would make progress evidence irrelevant.

- **Status:** Open
- **Impact:** Medium
  - The product could meet internally useful numbers without meeting the bar the
    Customer considers successful.
- **Likelihood:** High
  - The team drafted the measures after the Week 3 meeting rather than agreeing
    them during it.
- **Trigger:** the Customer rejects or materially changes any proposed `TOS-nn`
  measure.
- **Window:** before the Week 4 customer meeting.
- **Mitigation:** send the three measures to the Customer before Week 4 and ask
  for an explicit decision on each.
- **Contingency:** replace the rejected measure with the Customer's measurable
  wording and record the change in a new `DEC-nnn`.

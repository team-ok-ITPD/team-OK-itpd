# Risks

| ID | Status | Impact | Likelihood | Risk |
| --- | --- | --- | --- | --- |
| [RISK-01](#risk-01) | Open | High | High | The Week 3 build started after most of the sprint elapsed, so the working slice may miss the deadline, which would leave `MLS-03` undelivered. |
| [RISK-02](#risk-02) | Open | High | Medium | The browser IDE depends on Docker images and extension downloads, so an unavailable dependency may prevent the environment from starting, which would block the core task. |
| [RISK-03](#risk-03) | Open | High | Medium | Learner code runs in a shared service without a settled isolation architecture, so unsafe code may affect other users or infrastructure, which would prevent a public pilot. |
| [RISK-05](#risk-05) | Open | High | Medium | The team may not recruit three representative adults in time for UT-01. |
| [RISK-06](#risk-06) | Open | High | Medium | A participant may withdraw or refuse recording, leaving a session unusable. |
| [RISK-07](#risk-07) | Open | High | Medium | Instructors may not be able to access private usability evidence. |
| [RISK-08](#risk-08) | Open | High | Medium | Staging or session scheduling may prevent UT-01 from finishing in SPRINT-08. |
| [RISK-09](#risk-09) | Open | High | Medium | A secret may enter a public configuration artifact, which would expose a service or account and require incident response. |
| [RISK-11](#risk-11) | Open | High | Medium | A pinned dependency may become unupdatable, which could leave a vulnerable or unbuildable delivery path. |
| [RISK-12](#risk-12) | Open | High | Medium | A manual environment change may drift from the runbook, which could make the checked revision differ from the deployed product. |
| [RISK-04](#risk-04) | Open | Medium | High | The draft threshold has not been reviewed by the Customer, so its measures may not reflect Customer priorities, which would make progress evidence irrelevant. |
| [RISK-10](#risk-10) | Open | Medium | High | A configuration change may leave the inventory stale, which could make a contributor follow an incorrect build, check or deployment path. |

## RISK-05

The team may not recruit three representative adults in time for UT-01.

- **Status:** Open
- **Impact:** High
- **Likelihood:** Medium
- **Trigger:** fewer than three eligible, consented sessions are arranged.
- **Window:** [SPRINT-07](project-plan.md#sprint-07) to [SPRINT-08](project-plan.md#sprint-08).
- **Mitigation:** recruit five eligible adults through the documented profile and arrange replacements early.
- **Contingency:** recruit replacements; if three remain unavailable, keep QR-07 `Not verified` or move it to SPRINT-09, declare the shortfall and claim no result.

## RISK-06

A participant may withdraw or refuse recording, leaving a session unusable.

- **Status:** Open
- **Impact:** High
- **Likelihood:** Medium
- **Trigger:** consent, recording permission or continued participation is withdrawn.
- **Window:** every UT-01 session.
- **Mitigation:** explain consent and withdrawal before recording and confirm it at session start.
- **Contingency:** do not count the session, remove its raw text and recording, retire the code and recruit a replacement under the next code.

## RISK-07

Instructors may not be able to access private usability evidence.

- **Status:** Open
- **Impact:** High
- **Likelihood:** Medium
- **Trigger:** an instructor cannot open the private repository or recordings folder.
- **Window:** before the first counted session through grading.
- **Mitigation:** grant team and instructor reader access before collecting data and check it before sessions.
- **Contingency:** recreate access with the team and instructors; if GitHub access is unavailable, provide private text through a Moodle-only archive and declare the deviation.

## RISK-08

Staging or session scheduling may prevent UT-01 from finishing in SPRINT-08.

- **Status:** Open
- **Impact:** High
- **Likelihood:** Medium
- **Trigger:** staging is unavailable, instrumentation is unverified or sessions cannot finish by the sprint end.
- **Window:** SPRINT-07 through SPRINT-08.
- **Mitigation:** verify staging and instrumentation before the first counted session and schedule sessions early.
- **Contingency:** move the QR-07 row to SPRINT-09 with a reason, declare it in the report and claim no result.

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

## RISK-09

A secret may enter a public configuration artifact, which would expose a service
or account and require incident response.

- **Status:** Open
- **Impact:** High
  - A leaked credential can allow unauthorized use of a service and requires
    rotation, history cleanup and instructor notification.
- **Likelihood:** Medium
  - The repository documents environment shape and deployment work, so a
    contributor can mistake a real value for an example value.
- **Trigger:** a credential, token, private address or other secret appears in
  a tracked file, pull request or public artifact.
- **Window:** every configuration and deployment change through course grading.
- **Mitigation:** keep values in private environment settings, use placeholders
  in `.env.example`, and review changed artifacts and generated output before
  merge.
- **Contingency:** revoke or rotate the secret, notify the instructor, remove it
  from files and history, and record the affected account privately.

## RISK-10

A configuration change may leave the inventory stale, which could make a
contributor follow an incorrect build, check or deployment path.

- **Status:** Open
- **Impact:** Medium
  - A stale plan delays a change and can cause a failed check or deployment,
    but the repository and its source configuration remain recoverable.
- **Likelihood:** High
  - Build, documentation and release records changed across several sprints,
    while the inventory itself is new in Week 8.
- **Trigger:** a pull request changes a configuration item named in
  `docs/configuration-plan.md` without updating the plan when its description
  becomes inaccurate.
- **Window:** every pull request after the Week 8 review.
- **Mitigation:** review the configuration plan whenever a change affects its
  build, check, environment, release or agent-context records.
- **Contingency:** update the plan in the pull request that reveals the drift
  and treat the stale inventory as a documentation defect until corrected.

## RISK-11

A pinned dependency may become unupdatable, which could leave a vulnerable or
unbuildable delivery path.

- **Status:** Open
- **Impact:** High
  - The product or CI pipeline can become unable to build safely, blocking a
    checked release.
- **Likelihood:** Medium
  - The project depends on container images, Python packages and third-party
    GitHub Actions whose versions can change or be withdrawn.
- **Trigger:** a dependency update fails, a pinned version is unavailable, or a
  security advisory requires a version that cannot be adopted.
- **Window:** every dependency update and release through the final delivery.
- **Mitigation:** keep versions explicit, review Dependabot updates and run the
  documented product and container checks before release.
- **Contingency:** pin the last known working version, record why it cannot be
  updated, and open the task that removes the blocked dependency.

## RISK-12

A manual environment change may drift from the runbook, which could make the
checked revision differ from the deployed product.

- **Status:** Open
- **Impact:** High
  - Staging or production could behave differently from the commit whose checks
    and usability evidence the team presents.
- **Likelihood:** Medium
  - The university environment is operated outside the repository and may need
    manual deployment actions.
- **Trigger:** staging or production configuration differs from the documented
  deployment procedure or a deploy cannot be repeated from the recorded commit.
- **Window:** every staging verification, usability session and release.
- **Mitigation:** deploy the checked commit through the runbook and record
  configuration shape rather than making unrecorded server-side patches.
- **Contingency:** redeploy the commit that staging passed, update the runbook
  when the documented procedure changed, and do not patch the VM by hand.

# Sprint 9 handoff preparation

Prepared after the 28 November review, not a pre-review script or accepted
handoff. Source: [meeting notes](meeting-notes.md#handoff), 01:26:29–01:29:12.
No private access details, recording or credentials belong in this document.

## Customer Expectations

- Fix the professor assignment blocker and polish the product before handoff.
- Make the root README useful to prospective users: purpose, audience,
  capabilities and clear links to deployment instructions.
- Move course-specific material below product information.
- Meet again before demo day; no exact appointment is established.
- Demonstrate the fresh professor → student → professor results journey,
  rather than rely on seeded/exportable older data.

## Readiness And Remaining Work

| Area | Evidence now | Before handoff |
| --- | --- | --- |
| Administrator | [PR #220](https://github.com/team-ok-ITPD/team-OK-itpd/pull/220) implements the owner's follow-up corrections. | Independent review, merge and deployment verification; this is not the reviewed November 28 build. |
| Student | [Meeting evidence](meeting-report.md#user-acceptance-tests) includes a passing statement for the demonstrated student journey. | Confirm original UAT identity/build and re-run on the tagged handoff deployment. |
| Professor | Assignment failed in the recording. | Diagnose/fix, then run a fresh exercise, group assignment, student submission and professor export. Verify professor generation separately if the original test requires it. |
| Instructions | [Setup](../../docs/setup.md), [deployment](../../docs/deployment.md), [teaching](../../docs/teaching-workflow.md) and [administrator workflows](../../docs/admin-workflows.md) exist. | Walk through the README as a new user; verify role-specific instructions against the release. |
| Local VS Code | Demonstrated during the meeting. | Verify copy-code, connection guidance and safe return navigation; do not claim these fixes from the administrator PR. |
| Hidden tests and containers | Configuration was discussed, not fully validated. | Explain visible/hidden file configuration and supply isolation/resource-limit evidence. |
| Results and policy | Existing export was discussed. | Confirm CSV columns, grade semantics, pre-close access, late work and unassignment rules. |
| Ownership and access | No transfer is established. | Identify receiving operator, permitted private access, deployment/backup/recovery guidance and remaining limitations. |

## Provisional Sprint 10 Refinement

The [Sprint 10 milestone](https://github.com/team-ok-ITPD/team-OK-itpd/milestone/8)
exists, but the team has not supplied agreed owners, story points or capacity.
Use the [meeting action points](meeting-report.md#action-points) to refine scope;
do not silently convert every suggestion into a release commitment.

Full historical multi-file submission viewing and private forks of public
exercises were explicitly discussed as future work. Preserve those deferrals.
Group deactivation and inactive-student membership were clarified later by
the owner and are included in #220, not claimed as delivery at the meeting.

## Next Review Preparation

1. Confirm appointment, actual moderator/operator and Customer access privately.
2. Record the deployed tag and full commit before starting.
3. Recover the original three UAT definitions; do not rewrite them to fit a demo.
4. Use synthetic administrator/professor/student accounts and a fresh exercise.
5. Verify account invitation, student work/submission and the complete teaching
   journey. Preserve any failed or unexecuted steps with their reason.
6. Present the current quality-test evidence and each threshold's unchanged
   measure; distinguish failed tests from absent evidence.
7. Walk through user/deployment instructions and read back remaining limitations.
8. Ask explicitly for the handoff decision and permitted evidence handling.

This is an agenda for a future review, not proof that any of these steps ran.

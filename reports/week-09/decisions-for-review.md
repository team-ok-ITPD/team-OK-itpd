# Sprint 9 candidate decision wording

Prepared retrospectively from the [meeting notes](meeting-notes.md) and later
owner clarifications. This is a member-review aid, not `docs/decisions.md`.
No DEC identifiers are reserved or assigned. A member must verify wording,
source and scope before recording a real Customer decision.

## Three UAT Outcomes

| Candidate wording | Source | Member check before recording |
| --- | --- | --- |
| The demonstrated administrator professor-account creation/sign-in journey succeeded. | 01:22:59–01:24:42. | Verify this maps to the original administrator UAT; do not claim every provisioning or role-denial check passed. |
| The demonstrated student generation, correction and submission journey passes. | Explicit passing statement at 01:22:37–01:22:58; demonstration at 01:10:27–01:19:38. | Retain the reported return-button authentication defect; identify the original UAT. |
| The attempted professor group-assignment journey fails and must be fixed/re-run before handoff. | 01:02:32–01:05:28 and 01:24:44–01:26:25. | Distinguish the failed assignment from any professor-generation step that was not run. Existing-data export is not a fresh end-to-end Pass. |

Use runner `Team` for the team-controlled live demonstrations. The
[candidate reviewed baseline](../../docs/user-acceptance-tests.md#review-baseline)
comes from the owner's `main` at 13:30 statement, with timezone still qualified.
Each verified UAT judgment needs its own actual DEC entry and backlinks.

## Product And Handoff Wording

| Candidate wording | Source and boundary |
| --- | --- |
| Any valid email domain is permitted under administrator responsibility. | 00:02:15–00:02:37. |
| Remove the separate group-number input; retain group name and course context. | 00:11:07–00:13:49. |
| Prefer account invitations allowing owners to choose passwords; do not expose stored passwords or send administrator-assigned initial passwords. | 00:14:10–00:20:11; check supersession of earlier policy explicitly. |
| Clear hidden student selections after filtering and provide individual multi-group membership editing. | 00:21:59–00:25:45. |
| Default student assignments to To do, compact the dashboard and remove the cross-course grade average. | 00:27:18–00:38:52; no implementation claim. |
| Keep full historical multi-file submission viewing and student forks as future work. | 00:40:43–00:43:13 and 01:20:03–01:21:29. |
| Fix the assignment blocker, provide a user-oriented README with linked deployment guidance and arrange review before demo day. | 01:26:29–01:29:12; no fixed appointment or completed handoff acceptance. |

## Later Owner Clarifications — Separate Provenance

After the meeting, the owner explicitly requested reversible group deactivation
with student visibility/material access retained, inactive groups last for
administrators, and membership changes for inactive students without activating
their accounts. Implementation is in
[PR #220](https://github.com/team-ok-ITPD/team-OK-itpd/pull/220).

These are owner instructions from development chat, not verbatim Customer
statements from the recording. A member must not backdate or misattribute them.

## Recording Procedure

1. Compare the exact passage and original expected result.
2. Confirm Customer attribution and whether the statement is a decision or suggestion.
3. Use the next available identifier in the maintained decision record.
4. Record the actual date, source, rationale and any superseded policy.
5. Link the entry from the meeting report and corresponding UAT run.

No general story acceptance, changed threshold measure or final product
acceptance should be inferred from positive closing remarks.

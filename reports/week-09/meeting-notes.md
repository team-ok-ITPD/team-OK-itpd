# Sprint 9 review evidence notes

**Status:** Retrospective, sanitized working notes for team verification, not a
verbatim or speaker-verified transcript.

The user supplied a private recording of approximately 01:29:34.
The team confirmed the meeting date as 2026-11-28 and permission to record;
the recording remains private. Reviewed builds still need confirmation.
Automatic transcription was performed locally.
The Russian opening and a separate English-forced transcription of the remainder
were used for this summary. Raw recognition artifacts, recording, credentials
and private operational details are not included.

These notes paraphrase the dialogue. They do not establish permission to publish
a full transcript. Timecodes refer to the original recording held by the team.

## Administrator

| Timecode | Evidence and qualification |
| --- | --- |
| 00:00:04–00:03:34 | Four administrator areas are shown: Teachers, Students, Administrators and Groups. Teacher-account creation, editing and email delivery are demonstrated/discussed. The presenter says the application is running locally at 00:03:13–00:03:18. |
| 00:02:15–00:02:37 | Arbitrary email addresses are permitted under administrator responsibility; a university domain is not required. |
| 00:03:34–00:06:59 | A CSV imports four students without groups. An attempted bulk enrollment is blocked by an inactive selected account. This does not establish a general import failure. |
| 00:07:21–00:11:07 | Destructive group deletion is undesirable. Deactivation/archival is discussed, initially deferred and later described as useful, provided students retain access to historical assignments and solutions. Exact next-sprint scope needs confirmation. |
| 00:11:07–00:13:49 | Separate group name, course and group number are questioned. Removing the separate group-number input is read back; retain group name and course context. |
| 00:14:10–00:20:11 | Stored passwords must not be displayed or retained as plaintext. After discussing email risks, creating an account without an administrator-chosen password and sending an owner password-setup link is preferred. This differs from the creation-time password email previously implemented. |
| 00:21:28–00:23:18 | Searchable group filtering is positively received. Persistent hidden selections are challenged: filtering should clear hidden selections, which must not return when the filter is removed; the counter should reflect intended checked rows. |
| 00:23:24–00:23:45 | Adding active students to a group succeeds. |
| 00:24:19–00:25:45 | Multiple group membership is supported. Individual membership editing on the student edit page is requested in addition to bulk operations. |

## Student

| Timecode | Evidence and qualification |
| --- | --- |
| 00:27:18–00:29:30 | Make the dashboard more compact, remove duplicate group/student counters, and prioritize pending assignments. |
| 00:32:05–00:33:47 | Make To do the default assignment tab rather than All. |
| 00:35:03–00:36:58 | Clarify search matches and provide All/My/Public exercise filtering rather than only an Only my bugs checkbox. |
| 00:37:44–00:38:52 | Remove the average grade across different courses/assignments because their weights and numbers of bugs differ. |
| 00:39:39–00:40:41 | Browser VS Code submission is demonstrated; assignment status changes from To do to Submitted and a result appears. |
| 00:40:43–00:43:13 | The limited/latest source preview is discussed. Full historical multi-file submission viewing is useful but explicitly future work. Git-based storage is a suggestion, not an agreed architecture. |
| 00:43:21–00:49:39 | Local VS Code pairing, testing and submission are demonstrated. A submission with zero tests passing is described. The reviewer welcomes local-editor support, requests clearer instructions and a copy-code button. Latest-submission details should sit near status/deadline. Exact test counts require video verification. |
| 00:53:38–00:54:58 | Student generation is initially postponed while provider credentials are obtained. It is subsequently attempted later in the same meeting, so it must not be reported as never run. |
| 01:10:27–01:16:56 | OpenRouter configuration is followed by generation of a matrix-mean task, diagnosis, correction, passing tests and submission. Exact provider model, counts and build are not independently verified. No credential is reproduced here. |
| 01:17:01–01:18:03 | Clear congratulatory completion feedback is requested. The extension return button is reported to fail with an authentication/403 problem; later website navigation does not prove this button was fixed. |
| 01:20:03–01:21:29 | Forking a public exercise into a student's editable private copy is proposed, then deferred as a new feature. |

## Professor

| Timecode | Evidence and qualification |
| --- | --- |
| 00:55:11–00:56:47 | Owned groups and catalog filters are shown. Similar ownership/availability filtering is requested for students. |
| 00:57:15–00:59:57 | ZIP/Dockerfile and entry-file configuration are discussed. A single entry-file path is not enough to specify which tests/files are hidden. This conversation does not prove actual hidden-test isolation. |
| 01:01:05–01:01:32 | Professor endpoint/provider settings need completion and verification. |
| 01:02:32–01:05:28 | Group assignment is attempted and explicitly described as not working. No root cause is established from the recording. |
| 01:06:09–01:07:19 | Complete professor settings, clarify visible/hidden test configuration and retry the assignment/generation flow. Student generation success does not establish professor generation. |

## Acceptance Tests And Deployment

| Timecode | Evidence and qualification |
| --- | --- |
| 01:07:43–01:08:02 | A university-VM deployment is reported. No commit/tag or deployment identity is given, and earlier administrator demonstration is explicitly local. |
| 01:08:03–01:09:43 | The participants discuss three journeys: administrator provisioning, student work/submission, and professor exercise generation/assignment. They acknowledge one journey is blocked and propose rechecking it at handoff. |
| 01:22:37–01:22:58 | After the student demonstration, the reviewer explicitly says this user acceptance test passes. Original UAT numbering, exact runner and build still need confirmation. |
| 01:22:59–01:24:42 | A professor account is created and used to sign in. The reviewer checks that the same initial credentials were used and confirms that it works. This is not proof that every possible administrator operation passed. |
| 01:24:44–01:26:25 | The remaining journey should cover professor creation/assignment, student submission and professor results download. Assignment remains problematic. Export/closure of pre-existing demo data does not complete a fresh end-to-end run. |

## Handoff

| Timecode | Evidence and qualification |
| --- | --- |
| 01:26:29–01:28:28 | Fix the blocker and polish the root README for users: audience, capabilities and deployment guidance. Course-oriented material can move down; detailed deployment instructions can remain in docs when linked clearly. |
| 01:28:44–01:29:12 | Arrange the next review/handoff before demo day. No exact appointment is fixed. |
| 01:29:21–01:29:30 | Positive closing feedback about progress does not erase the stated blocker or establish full product/handoff acceptance. |

## Candidate Decisions Requiring Member Verification

No `DEC-nnn` is assigned by these notes. A team member must verify the source,
identify any reversal of earlier policy, and record each real decision in
`docs/decisions.md`, including a separate entry per actual UAT outcome.
In particular, verify the preferred password invitation flow, group identity,
filtered-selection behavior, deferred features and the original three UAT
identities. No general story acceptance is inferred without its `US-nn` and
acceptance-criteria mapping.

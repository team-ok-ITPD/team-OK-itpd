# Week 9 AI Usage

- OpenCode fixed invitation-only CSV provisioning: legacy password cells are
  ignored for both new and existing accounts; new accounts have unusable
  passwords until owner setup. Import regression tests were adapted to that
  requirement, including disabled-email and repeat-import behavior.

- At the owner's request, the administrator student list now shows each group's
  course between its name and teacher, with an explicit No course fallback.

- OpenCode (GPT-6.1 Sol) is implementing the owner's November 28 administrator
  corrections in task #219: invitation-only account creation, group identity,
  filtering selection, individual/inactive-student membership editing and
  reversible group deactivation. Existing group identifiers and memberships
  are retained. Regression checks use synthetic accounts and local-memory email;
  no real-email delivery or completed browser acceptance is claimed here.
- Following owner UI feedback, OpenCode removed password editing, restyled group
  status and added a searchable membership picker with separate selected groups.
  Browser inspection checked password absence and an empty search while selected
  memberships remained visible; it did not send mail or save account changes.
- The owner requested a simpler membership editor: current groups with explicit
  Remove actions and a collapsed Add group search with Add actions, rather than
  displaying a catalog of checkboxes in the student card.
- Follow-up UI correction hides legacy group numbers in all shared group labels
  and removes the student-total badge from the administrator section heading.

- Codex implemented the project owner's clarified meeting feedback locally:
  catalog filters and owner names, administrator-managed course text,
  independent group assignments, confirmation and archival withdrawal,
  ZIP-only uploads, optional metadata and removal of reference solution storage.
- Codex adapted student and professor generation, demo fixtures, migrations
  and regression tests. Provider responses remain mocked in automated checks.
- Codex added creation tabs, provider-aware personal credentials, live catalog
  filters and a group/deadline assignment dialog. Automated UI behavior checks
  cover keyboard tabs, stale filter responses, assignment errors and redirects.
- Codex moved assignment to the opened exercise page and replaced Compose
  upload with a validated optional Dockerfile, retaining legacy configuration.
  Uploaded Dockerfiles are stored only; no image build is claimed.
- No Customer approval, visual acceptance or live provider result is claimed.
  The owner will inspect the local application before publication.

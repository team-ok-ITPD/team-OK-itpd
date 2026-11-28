# Administrator Workflows

## Scope And Source

This implementation follows the administrator feedback in the
[20 November meeting transcript](../reports/week-08/meeting-transcript.md),
01:32:32–02:07:38, and task
[#193](https://github.com/team-ok-ITPD/team-OK-itpd/issues/193).
It is not a record of new Customer decisions or production acceptance.

The administrator panel contains Teachers, Students, Administrators and Groups.
Assignments remain a teacher workflow; the former administrator assignment
pages and group-membership pages are removed.

## Accounts And Access

- Create accounts with name, email and active status; the owner chooses a
  password through an emailed setup link. Editing has no password field either;
  a submitted password value is ignored and the existing hash is preserved.
  Use Send access link for the owner to reset their password.
- Only administrators can use these routes. Roles are fixed server-side;
  an edit cannot promote a student or teacher to administrator.
- Self-deactivation and self-deletion are refused. Changing one's own password
  preserves the current session; other old sessions become invalid.
- Deactivation removes database-backed web sessions and both IDE-token types.
  Even an idle old session cannot resume after reactivation. The already rendered
  browser page is not remotely erased; its next request requires sign-in.
- Delete requires a separate GET confirmation page and CSRF-protected POST.
  Accounts with teaching groups, exercises, assignments or submissions are
  protected against deletion; deactivate them to retain history. Other deletion
  removes the account, memberships and tokens, not learner workspace files.
  This conservative retention rule needs team/Customer confirmation; it is not
  an inferred authorization to erase historical learning data.

## Students And Groups

Students is the single membership-management entry point. A compact shared
toolbar contains search, the group filter and bulk actions. Search by name/email,
filter by group and see the filtered count and each student's groups/teachers.
The student list is paginated at 30 accounts per page. Select students, choose an action
and, for membership changes only, a target group:

- Add to group (including inactive students); repeating it does not duplicate membership.
- Remove from group; assignments and submission history remain unchanged.
- Activate/deactivate the selected students.

Only visible rows can remain selected. Applying search clears selections;
navigation discards selections outside the visible page, and removing a filter
does not restore discarded selections. The counter and confirmation reflect
the selected visible rows. Successful bulk actions clear the selection.
Individual student editing also supports multiple group memberships, including
inactive accounts and inactive groups; this does not reactivate an account.
The student card initially shows current memberships with a Remove action.
Add group expands a search for existing groups by name, course or teacher;
each result has an Add action. Adding closes the search and puts the group in
the current list. At most 20 matching results appear at once; refine search
to find more. Filtering never removes a current membership. Changes apply only
on Save. Without JavaScript all native checkboxes remain available.
Activation/deactivation ignores the target group, which is hidden for these
actions. All supplied IDs must identify students; any invalid selection rejects
the entire action. Search remains explicit via Search or Enter.

Groups provides clickable rows for editing (also accessible by keyboard),
and an active-teacher selector with search inside its dropdown. Without
JavaScript, the group-name link and native select remain available.
Each group still has exactly one teacher. Changing it does not transfer exercise
or assignment ownership. Membership is managed in Students, not in Groups.

Following the November 28 review and owner's clarification in task #219, group
forms use **Group name**, optional **Course**, description, teacher and active
status. There is no separate group-number input for new groups. Legacy numbers
remain stored for CSV compatibility but are not shown in interface group labels.
Group names created through the form must be unique ignoring case.

Deactivation is reversible and sorts groups after active groups in the
administrator list. It does not remove memberships, assignments, submissions or
student access to group materials. An inactive account still cannot sign in.

This is the current implementation direction from the user, not a rewrite of
the historical course-description rule in [DEC-044](decisions.md#dec-044).
There is still no separate course-management model.

## Student CSV Import

Use **Students → Import CSV**. UTF-8 (optional BOM), comma-separated, at most
1 MB and 5000 data rows. Headers are unique; unknown headers are rejected.

| Column | Required | Meaning |
| --- | --- | --- |
| `name` | Yes | Up to 100 characters |
| `email` | Yes | Valid email, up to 150 characters; case-insensitive account matching |
| `is_active` | No | `true`/`false` or `1`/`0`; blank preserves existing state, defaults to active for a new account |
| `password` | No, legacy only | Accepted but ignored; import never assigns or resets passwords |
| `course` | For enrollment | Legacy CSV group-name lookup in `name`; the separate course text is managed in the group form |
| `group_number` | When a legacy name is ambiguous | Optional compatibility identifier; up to 50 characters |
| `teacher_email` | For a new group | Must identify one existing active teacher |

Repeat identical account data on several rows to enroll one student into several
groups. Conflicting repeated account data is rejected. Course and group number
identify the group. Without a number, an existing course must match exactly
one group. New groups require a teacher, not a number. Imports never reassign
existing teachers or change course data.
Imports may record inactive students' memberships, but inactive users have no
access; manual batch enrollment also permits inactive accounts without activation.

Existing students are updated, never promoted from another role. A new group is
created only when its name and teacher are supplied. Omitted memberships are
not removed. Repeating unchanged data creates no duplicate users, groups or
memberships and never changes existing passwords.

For backward compatibility, old CSVs with the `group` column can still refer to
an unambiguous existing group by its former name. When a nonempty legacy `group` value is supplied, it
supplies the existing `name` field and the old `course` column retains its legacy
description meaning. Add `group_number` when a legacy name is ambiguous;
new files should use `course,group_number,teacher_email` without legacy `group`.

Confirmation applies the entire file in one transaction. Any malformed or
invalid row rolls back all database changes, including access revocation.
The CSV is processed in memory, not stored or logged. Error messages do not
echo passwords or row contents. Email is attempted only after a successful import.

## Optional Account Email

When creating an active account, the email includes its login email, a sign-in
URL and an expiring password-setup link. No initial password is emailed, including
for CSV imports. Interactive creation ignores submitted password fields and
stores an unusable password until the owner completes setup.

New accounts receive a welcome message with their role and password-setup
instructions. Manual resend uses an access-link message rather than a new-account
invitation. CSV updates never change passwords or resend invitations.
Both templates include link-expiry and unexpected-message guidance;
normal service emails contain no test-preview banners.

The November 28 owner clarification supersedes the previous initial-password
email behavior. Existing passwords/hashes are never included in a message.
New CSV accounts also start with unusable passwords and use owner setup links.
Legacy password cells are ignored, including on repeated imports.

Delivery is disabled by default; without it new accounts remain without usable
passwords. Configure email and use Send access link to complete onboarding.

The deployment owner configures these environment variables privately:

| Variable | Default | Purpose |
| --- | --- | --- |
| `DJANGO_ACCOUNT_EMAIL_ENABLED` | `0` | Set to `1` to enable delivery |
| `DJANGO_ACCOUNT_PUBLIC_URL` | Empty | Trusted public application origin; never taken from an incoming Host header |
| `DJANGO_EMAIL_BACKEND` | Django SMTP backend | Transport; console/file/dummy delivery is refused for access tokens |
| `DJANGO_EMAIL_HOST` | `localhost` | SMTP host |
| `DJANGO_EMAIL_PORT` | `587` | SMTP port |
| `DJANGO_EMAIL_USE_TLS` | `1` | Enable STARTTLS |
| `DJANGO_EMAIL_HOST_USER` | Empty | SMTP user |
| `DJANGO_EMAIL_HOST_PASSWORD` | Empty | SMTP credential; never commit it |
| `DJANGO_DEFAULT_FROM_EMAIL` | `noreply@example.com` | Sender address |

Unchanged imports do not resend
mail. **Send access link** sends a link-only email from an account's edit page:
it cannot recover or resend an initial password, because the application does
not retain its original text. Delivery errors show a generic warning, never provider
exception contents or credentials. Accounts are not rolled back if mail fails;
the administrator must fix delivery and retry Send access link. Inactive accounts do
not receive links and cannot use the password-setup endpoint.

Actual SMTP delivery requires operator configuration and is not established by
tests against Django's in-memory email backend.

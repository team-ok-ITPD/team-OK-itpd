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

- Create/edit accounts with name, email, active status and one password field.
  Newly entered passwords are visible by default, with Hide/Show controls.
  A saved password or hash is never displayed; validation errors do not
  redisplay submitted passwords. Blank password on edit preserves the existing hash.
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

- Add to group (only active students); repeating it does not duplicate membership.
- Remove from group; assignments and submission history remain unchanged.
- Activate/deactivate the selected students.

With JavaScript and browser session storage available, explicit selections persist
within the same tab/account across search, filters and pages. A counter shows the
total selection, including students outside the current page. Select-all affects only
the visible page; Clear selection clears the entire selection. Confirmation
includes the total count, including off-page students. Successful bulk actions
clear the selection; failed actions retain it. Without JavaScript or storage,
selection persistence across navigation is unavailable.
Activation/deactivation ignores the target group, which is hidden for these
actions. All supplied IDs must identify students; any invalid selection rejects
the entire action. Search remains explicit via Search or Enter.

Groups provides clickable rows for editing (also accessible by keyboard),
and an active-teacher selector with search inside its dropdown. Without
JavaScript, the group-name link and native select remain available.
Each group still has exactly one teacher. Changing it does not transfer exercise
or assignment ownership. Membership is managed in Students, not in Groups.

Following the user's updated clarification on 2026-11-27, groups have separate
**Group name** (`name`), **Course** (`course`) and **Group number**
(`group_number`) fields. Course is optional free text editable by administrators
and read-only for professors. Existing course text is initialized from the old
name so no existing name is lost. Group numbers preserve leading zeroes and
identifiers such as `BS-23`; name/number pairs remain unique ignoring case.
Description is optional free-form notes.

Existing records retain their names and descriptions; their new group number
starts blank rather than being guessed. Administrators must supply a number
when creating or editing a group. Display labels include both group name and
number across administrator, professor and student pages.

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
| `password` | Conditional | At least eight characters; required for a new account when access email is disabled; blank preserves existing password |
| `course` | For enrollment | Legacy CSV group-name lookup in `name`; the separate course text is managed in the group form |
| `group_number` | For a new group; when course is ambiguous | One group per row; up to 50 characters |
| `teacher_email` | For a new group | Must identify one existing active teacher |

Repeat identical account data on several rows to enroll one student into several
groups. Conflicting repeated account data is rejected. Course and group number
identify the group. Without a number, an existing course must match exactly
one group. New groups require a number and teacher. Imports never reassign
existing teachers or change course data.
Imports may record inactive students' memberships, but inactive users have no
access; manual batch enrollment requires activation first.

Existing students are updated, never promoted from another role. A new group is
created only when its course, group number and teacher are supplied. Omitted memberships are
not removed. Repeating unchanged data creates no duplicate users, groups or
memberships and does not rehash an unchanged password.

For backward compatibility, old CSVs with the `group` column can still refer to
an unambiguous existing group by its former name. When a nonempty legacy `group` value is supplied, it
supplies the existing `name` field and the old `course` column retains its legacy
description meaning. Add `group_number` when ambiguous or creating a new group;
new files should use `course,group_number,teacher_email` without legacy `group`.

Confirmation applies the entire file in one transaction. Any malformed or
invalid row rolls back all database changes, including access revocation.
The CSV is processed in memory, not stored or logged. Error messages do not
echo passwords or row contents. Email is attempted only after a successful import.

## Optional Account Email

When creating an active account, the email includes its login email, the
initial password entered by the administrator, a sign-in URL and an expiring
password-setup link. This applies to teachers, students and administrators,
including new students created by CSV import. If no initial password was
provided, only the setup link is sent.

The initial password is taken from the creation request, never recovered from
the database. Only its hash is stored by the application. The recipient's mailbox
will contain the initial password; anyone with access to that message can use
it until the password changes. This delivery behavior follows the user's
explicit follow-up request, not a new recorded Customer decision.

Delivery is disabled by default; without it the administrator supplies and
communicates the initial password through their existing private process.

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

Password changes still send link-only emails. Unchanged imports do not resend
mail. **Send access link** sends a link-only email from an account's edit page:
it cannot recover or resend an initial password, because the application does
not retain its original text. Delivery errors show a generic warning, never provider
exception contents or credentials. Accounts are not rolled back if mail fails;
the administrator must retry or set an initial password. Inactive accounts do
not receive links and cannot use the password-setup endpoint.

Actual SMTP delivery requires operator configuration and is not established by
tests against Django's in-memory email backend.

# Teaching Workflow

This page records the requested v2 professor workflow and its local review
status on 2026-11-20. The source is the project owner's instructions in the
development chat. Customer decision records retain their own sources.

## Current Iteration

| Capability | Local implementation |
| --- | --- |
| Groups and students | The professor sees only administrator-assigned groups and their members. A separate free-text course field is editable only by administrators. |
| Assigning an exercise | Assigning another author's public exercise creates an independent private copy owned by the professor, including code, tests and project configuration. Its description links to the original. Owned exercises are assigned directly. Each new assignment belongs to one group. |
| Deadline | Optional, entered in UTC and stored independently for each exercise/group assignment. Reassigning an active, unreviewed owned exercise updates that group's assignment. Legacy multi-group records are split with submission history retained. |
| Result availability | After the deadline or manual closure. Without a deadline, manual closure is required. |
| Result table | Student full name, email and best verified test counts. Missing counts show Awaiting verification. |
| CSV export | The same availability and access checks apply to the downloadable result table. |
| Exercise catalog | Live title search with independent availability (all/public/private) and owner (all/my/others) filters. Cards show owners and link to exercise details. Only the opened exercise page has Assign to a group, with an owned-group/optional-deadline dialog. Filtering remains scoped on the server. Owners can publish and unpublish; other authors' public exercises remain read-only. |
| Project import | ZIP only, limited to 5 MB compressed, 5 MB expanded and 100 text files, checked on the server. Title, language and project are required; description and difficulty are optional. The entry file is detected when unambiguous. |
| Creation from a group | Upload and generation use separate keyboard-accessible tabs. Saves a private exercise and its assignment together, then returns to that group. Validation errors keep the relevant tab open. |
| Environment configuration | An optional UTF-8 Dockerfile up to 50 KB is stored with the exercise. It must contain FROM. Dockerfile upload replaces Compose upload; legacy stored Compose text is retained separately. Uploaded Dockerfiles are not built or executed yet. |
| Generation | A prompt, Python or JavaScript, and a test count. Generated projects must run the requested number of tests and fail at least one on the buggy source. Reference solutions are neither requested nor stored; this check does not establish that the tests accept every correct implementation. |
| Personal API key | Professor settings stores an encrypted personal key and provider choice (OpenAI, OpenRouter or the platform provider). An empty personal key uses both the internal platform key and its configured provider. |
| Suspicion analysis | A worker reviews every submitted attempt once after the deadline, or after manual closure for an assignment without a deadline. Advisory findings appear beside the student and in CSV. |
| Browser VS Code | Reuses code-server and the Debug GYM extension from the original app. Professors save project snapshots; students submit source for server verification. |
| Verified results | Python uses pytest and JavaScript uses Node's test runner in fresh, network-isolated temporary containers. Open student pages poll their own result every three seconds. |

Closing requires explicit confirmation. Withdrawing an assignment removes
student access and retains submissions/results in the professor's archive;
it does not delete the exercise or change another group's assignment.

The November 27 migration splits existing multi-group assignments and preserves
attempts for each group's students. Completed review records are copied to avoid
repeating a provider request for historical work. Historical migration files keep
the removed field's definition so existing databases can be upgraded.

## Local Setup

Install `app/v2/debug_gym/requirements.txt`, run the v2 migrations and build the
repository's Dockerfile with tag `debug-gym-ide`. Run the v2 Django server on
`127.0.0.1:8002`.

Run this separate worker from `app/v2/debug_gym` alongside the web server.

```sh
python manage.py review_due_assignments
```

It checks due assignments every 30 seconds. `--once` performs one sweep.
A unique database record claims each assignment before its single provider
request. Missing credentials leave the assignment pending. Provider errors
record a failed attempt without an automatic repeat. An interrupted running
attempt requires operator inspection because the remote request may have
completed. Deadlines cannot be changed after a review is claimed.

Use `python manage.py seed_teaching_demo --teacher teacher@debuggym.local` to
add named demonstration data. Existing accounts and exercises are retained.
The command verifies demo submissions with Docker, then writes the new demo
logins to the ignored `app/v2/debug_gym/DEMO_ACCOUNTS.md`.

## Agent Configuration

| Environment variable | Purpose |
| --- | --- |
| `DEBUG_GYM_AGENT_KEY` | Internal fallback key, available to both web process and review worker. |
| `DEBUG_GYM_AGENT_URL` | Server-controlled Chat Completions endpoint, defaulting to OpenAI. |
| `DEBUG_GYM_AGENT_MODEL` | Provider model name, defaulting to `gpt-4.1-mini`. |
| `DEBUG_GYM_IDE_IMAGE` | Common workspace and test image, defaulting to `debug-gym-ide`. |
| `DEBUG_GYM_SITE_URL` | Browser-facing platform URL. |
| `DEBUG_GYM_IDE_SERVER_URL` | Platform address reachable from the VS Code container. |

Personal API keys use Fernet encryption. Preserve the ignored
`app/v2/debug_gym/.agent-encryption-key` alongside database backups. Without that
key file, stored personal keys need to be entered again. Provider failures are
reported without echoing tokens or the provider response body.

The same [Chat Completions API contract](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)
is used for generation and review. A configured compatible provider must support
JSON object responses. Generated files are validated as untrusted projects.

Personal OpenAI keys route to OpenAI. OpenRouter uses its documented
[Chat Completions endpoint](https://openrouter.ai/docs/api/api-reference/chat/send-chat-completion-request).
For OpenRouter, a model without a provider prefix receives `openai/`.
The platform-provider option preserves the server-configured endpoint and model.
Selecting a personal provider never routes the internal platform key to it.

## Verification And Limits

Automated tests cover credentials, access, deadlines, retries, generation
validation, one-time scheduled reviews, result export and project imports.
A disposable runtime rehearsal used the updated extension's snapshot helper
inside actual code-server containers, saved an author project, submitted a
student fix, observed a server-computed 2/2 result and exported it after closure.
Separate real-container checks observed 0/1 before and 1/1 after a fix in both
Python and JavaScript.

The provider integration is tested with controlled responses. No live provider
request has been verified because no key is configured. Visual browser QA was
unavailable; page rendering and normal HTTP entry points were checked.

Per-exercise dependency installation and building uploaded Dockerfiles remain
outside this iteration. Both language runners use the common prebuilt image.

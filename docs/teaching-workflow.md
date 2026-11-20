# Teaching Workflow

This page records the requested v2 professor workflow and its local review
status on 2026-11-20. The source is the project owner's instructions in the
development chat. Customer decision records retain their own sources.

## Current Iteration

| Capability | Local implementation |
| --- | --- |
| Groups and students | The professor sees only administrator-assigned groups and their members. |
| Assigning an exercise | Assigning another author's public exercise creates an independent private copy owned by the professor, including code, tests and project configuration. Its description links to the original. Owned exercises are assigned directly. Each new assignment belongs to one group. |
| Deadline | Optional, entered in UTC and stored independently for each group assignment. |
| Result availability | After the deadline or manual closure. Without a deadline, manual closure is required. |
| Result table | Student full name, email and best verified test counts. Missing counts show Awaiting verification. |
| CSV export | The same availability and access checks apply to the downloadable result table. |
| Exercise catalog | Own exercises and public exercises, title search, publication and unpublication of owned exercises. Another author's public exercise is read-only, including browser VS Code access. Unpublication retains existing assignments and copies. |
| Project import | A ZIP containing UTF-8 source and test files, with a chosen source entry file. |
| Creation from a group | Saves a private exercise and its assignment together, then returns to that group. |
| Environment configuration | An optional Compose YAML is stored with the exercise for the runtime integration. |
| Generation | A prompt, Python or JavaScript, and a test count. The reference solution must pass every generated test and the buggy source must fail at least one before the exercise is saved. |
| Personal API key | Professor settings stores an encrypted personal key. An empty personal key uses the internal platform key. |
| Suspicion analysis | A worker reviews every submitted attempt once after the deadline, or after manual closure for an assignment without a deadline. Advisory findings appear beside the student and in CSV. |
| Browser VS Code | Reuses code-server and the Debug GYM extension from the original app. Professors save project snapshots; students submit source for server verification. |
| Verified results | Python uses pytest and JavaScript uses Node's test runner in fresh, network-isolated temporary containers. Open student pages poll their own result every three seconds. |

Existing multi-group assignments retain their shared deadline. The professor UI
declines deadline changes and closure for those records, avoiding changes to
another group's work. Newly created assignments use one group per record.

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

Per-exercise dependency installation and running uploaded Compose files remain
outside this iteration. Both language runners use the common prebuilt image.

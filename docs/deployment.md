# Deployment

This runbook deploys one reviewed commit to staging and then production on the
university VM. The VM is reachable only from the university network. Its real
IPv4 address, credentials and environment values belong in the private Moodle
submission or on the VM, never in this repository.

Use [Setup and run](setup.md) for prerequisites, configuration variables, the
image build, startup and health checks. This runbook adds only the environment
mapping and release procedure.

## Environments

| Environment | Location | Purpose | Configuration |
| --- | --- | --- | --- |
| Development | A contributor's machine | Implement and run scripted checks | A local `.env` copied from `.env.example` |
| Integration | GitHub Actions | Build the image and run automated checks on pull requests and `main` | Workflow values and no deployment secrets |
| Staging | University VM, staging ports | Rehearse the exact release candidate and run deployed tests | `/opt/debug-gym/staging/.env`, readable only by the deployment account |
| Production | University VM, production ports | Serve the Customer and verify the core learner task | `/opt/debug-gym/production/.env`, readable only by the deployment account |

Staging and production use different Compose project names, ports, data volumes
and environment files. They may run on the same VM, but neither environment
reuses the other's secrets or mutable data.

## VM Access

1. In the university portal, recreate the team's VM when required and set the
   deployment account password through the portal.
2. Connect from a campus machine or another machine already on the university
   network: `ssh <deployment-user>@<university-vm-ipv4>`.
3. Confirm the checked-out repository contains no `.env` file or private key
   tracked by Git.
4. Keep the real staging and production addresses in the private Moodle
   submission. Use `<university-vm-ipv4>` in shared instructions and evidence.

## Configuration

Create the two environment files outside the checkout. Use `.env.example` as
the public description of their shape, choose different host ports for each
deployment, and set each workspace URL to the corresponding campus-reachable
address. Restrict both files to the deployment account.

Set `DEBUG_GYM_METRICS_TOKEN`, `DEBUG_GYM_ANALYTICS_URL` and
`DEBUG_GYM_ANALYTICS_KEY` in each file with values that are different for
staging and production. Their meaning is in [Setup](setup.md), the events are
in the [analytics plan](analytics.md) and the metric in
[Observability](observability.md). With the URL empty the product still works
and collects nothing.

Do not put passwords, tokens, API keys, the VM address or environment-file
contents in Git, command history, screenshots or CI logs.

## Telemetry Pipelines

The product sends analytics events and operating signals to two backends that the team self-hosts and does not build. The product works with both absent. Keep both backends' addresses and credentials out of Git, as described under [Configuration](#configuration). The plans are the [analytics plan](analytics.md) and the [observability plan](observability.md).

### Analytics Backend

1. Deploy an analytics backend on the university VM. OpenPanel is the course default; if another backend is used, name it here.
2. Create one environment scope for staging and one for production, each with its own credential.
3. Set `DEBUG_GYM_ANALYTICS_URL` and `DEBUG_GYM_ANALYTICS_KEY` in each environment's file to that scope's address and credential. The address must start with `https://`.
4. Build a dashboard in each scope with a chart for the focus metric or its first input, running the query in [the metric's section](analytics.md#the-metric-tree).
5. Send the smoke events to staging with `python scripts/send_smoke_event.py --url <staging address>`. The staging event list shows them, the metric chart excludes them, and production receives none.

### Observability Backend

1. Deploy an observability backend on the university VM. OpenObserve is the course default.
2. Create one organization for staging and one for production.
3. Set `DEBUG_GYM_METRICS_TOKEN` in each environment's file. Configure that environment's scraper with the same token, and remote-write its metrics to that environment's organization.
4. Collect the catalog's JSON request lines into the `debug_gym_requests` stream of the same organization, and record the log exporter's batch interval and the metric exporter's interval here once chosen.
5. Build a dashboard in each organization with a chart named after [SLI-01](observability.md#sli-01), running the query recorded there.
6. Check staging with `python scripts/check_sli.py` ([QR-06 QRT-01](quality-requirements/qr/QR-06.md#qrt-01)). Leave production configured with the same query and send it no test traffic.

## Manual Deployment

1. Choose the release commit from a green `main` run and record its full hash.
2. On the VM, fetch the repository and check out that exact commit in the
   staging checkout.
3. With the staging environment file and Compose project name selected, follow
   the build, startup and readiness procedure in
   [Setup and run](setup.md#start-and-check-readiness).
4. Run every `deployed` QRT against staging from a campus machine, using an
   environment variable such as `$STAGING_URL` rather than writing the address
   into evidence.
5. If staging passes, check out the same commit in the production checkout and
   follow the same linked startup and readiness procedure with the production
   environment file and project name.
6. Do not rebuild from a different commit between staging and production.

The product CI contains no deployment job because GitHub-hosted runners cannot
reach the university network. A team member performs every deployment manually.

## Verification

After production starts, perform the core learner task from a campus machine:

1. Open the production catalog and confirm its health endpoint succeeds.
2. Request the prepared Python list-mutation exercise.
3. Open its browser-based VS Code workspace and confirm its health endpoint
   succeeds.
4. Reproduce the intended failure, apply the known fix and confirm all exercise
   tests pass.
5. Record the release commit, date and checks without recording the real
   address.

A release is deployable only when both health endpoints and the complete core
task succeed.

## Rollback

1. Stop the failed deployment without deleting its volumes.
2. Check out the previous production release tag in the production checkout.
3. Start that tag with the unchanged production environment file by following
   the linked setup procedure.
4. Repeat the production verification above.
5. Record the failed commit, observed failure and restored release in the
   weekly report. Do not retry production until a corrected commit has passed
   staging.

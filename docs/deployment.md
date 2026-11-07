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

Do not put passwords, tokens, API keys, the VM address or environment-file
contents in Git, command history, screenshots or CI logs.

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

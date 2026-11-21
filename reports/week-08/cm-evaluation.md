# CM Evaluation

- **Baseline:** [`v0.4.0`](https://github.com/team-ok-ITPD/team-OK-itpd/releases/tag/v0.4.0), the `REL-07` release state.
- **Reviewed:** 2026-11-21.

## Method

Team 02 reviewed the repository on 2026-11-21 against the `v0.4.0` baseline,
in four passes: source control and checks, environments and builds,
documentation and reports, then agent context. Each pass read the files named
in [the configuration plan](../../docs/configuration-plan.md) rather than the
plan's own description of them, and the review judged each set of artifacts by
the purpose it serves instead of asking whether a required artifact may be
removed. Private VM settings, credentials, participant data, the GitHub
settings pages and Customer decisions were out of scope.

## Catching A Regression Before A Release

- **Today:** [CFG-01](../../docs/configuration-plan.md#cfg-01), [CFG-02](../../docs/configuration-plan.md#cfg-02) and [CFG-03](../../docs/configuration-plan.md#cfg-03) review changes, run the checks and build the documentation.
- **A more convenient way:** `Keep` the separate product, Markdown, link,
  documentation and workflow checks, and `Add` one job to the product
  workflow that installs the v2 dependencies and runs the v2 Django tests.
- **Why:** The separate checks report different failures, so a reader can tell
  a documentation error from a product regression. The goal is not met for the
  application that carries this sprint's changes: `app/v2/debug_gym` has test
  modules for its accounts, administrator, core, professor and student parts,
  and no workflow runs them, so a green product check says nothing about it.
  The new job replaces the by-hand v2 test run that the v2 setup guide asks
  for.
- **Tradeoffs:** The product workflow gets slower and needs the v2 packages
  installed in CI. That cost is worth paying because without it the main
  application can regress behind a green check. The repeated checkout setup in
  every workflow stays, since merging the workflows would hide which check
  failed.

## Reproducing The Product Safely

- **Today:** [CFG-04](../../docs/configuration-plan.md#cfg-04) and [CFG-05](../../docs/configuration-plan.md#cfg-05) hold the deployment runbook, the public environment shape, the container build and the dependency inputs.
- **A more convenient way:** `Merge` `requirements.lock` into the root
  `requirements.txt` as one exactly pinned file that the container and the
  workflow install, `Replace` the version ranges and the doubled `docker` line
  in the v2 requirements with exact pins, and `Add` the v2 directory to
  Dependabot. `Keep` the public `.env.example` and the runbook, with real
  values in the private submission material.
- **Why:** The root has two inputs that disagree: `requirements.txt` pins a
  newer `pytest` than `requirements.lock`, the container and the workflow read
  only the lock, and Dependabot watches only the root, so it edits the file
  nothing installs. The v2 requirements float on version ranges that neither
  the workflow nor the container installs. One pinned file per application
  removes that split, and the checked build is then the build that ships.
- **Tradeoffs:** Dependabot opens more pull requests, including ones for
  transitive packages, and the rename touches the Dockerfile, the workflow and
  the setup guides. Separately, a reader cannot reproduce the university
  deployment from the public repository alone; that loss is necessary because
  publishing its values would turn configuration documentation into a secret
  leak.

## Keeping Project Context Findable

- **Today:** [CFG-06](../../docs/configuration-plan.md#cfg-06), [CFG-07](../../docs/configuration-plan.md#cfg-07) and [CFG-08](../../docs/configuration-plan.md#cfg-08) provide the agent instructions, the indexes, the report locations and the course rule router.
- **A more convenient way:** `Keep` the nested v2 instructions and the
  `CLAUDE.md` that imports them, and `Replace` the root `AGENTS.md` layout and
  checks lines so they describe `app/v2/debug_gym` and its test command. The
  root file already links the configuration plan, so no link is added.
- **Why:** A repository-wide agent starts at the root file. That file calls
  `app/` the catalog server and lists only the root test command, so an agent
  working on v2 is sent to the wrong application and the wrong check. The
  change removes that stale description and leaves the style rules where they
  govern.
- **Tradeoffs:** The root file grows by a few lines that must stay true as v2
  changes. The upkeep is small next to an agent following a layout that no
  longer matches the repository.

## What We Could Not Judge

The university VM's backup and snapshot policy was not available. The risk is
that recovery depends on redeploying from the repository rather than restoring
an environment, so the plan records the runbook and the public configuration
shape and no infrastructure guarantee. The branch-protection and tag-protection
settings were read only as described in `CONTRIBUTING.md`, because the GitHub
settings pages were out of reach for this review; the risk is that a described
rule is not enforced, so [CFG-01](../../docs/configuration-plan.md#cfg-01)
should be checked on the settings page before it is trusted. The team also has
no `CODEOWNERS` file and no workflow that scans for secrets, so a secret leak
would be caught only by review, which [RISK-09](../../docs/risks.md#risk-09)
records.

## The First Change

The team would first merge the root `requirements.lock` into one exactly pinned
`requirements.txt`, pin the v2 requirements and add the v2 directory to
Dependabot. It keeps the pinned container build, the separate workflows and the
public `.env.example`. It removes the second root dependency file and the open
version ranges, which let Dependabot edit a file that nothing installs. Its
main tradeoff is more Dependabot pull requests and a rename that touches the
Dockerfile, the workflow and the setup guides.

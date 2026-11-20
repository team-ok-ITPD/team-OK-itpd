# CM Evaluation

- **Baseline:** [`v0.4.0`](https://github.com/team-ok-ITPD/team-OK-itpd/releases/tag/v0.4.0), the `REL-07` release state.
- **Reviewed:** 2026-11-19.

## Method

Team 02 reviewed the repository on 2026-11-19 against the `v0.4.0` baseline in
four passes: source control and checks, environments and builds, documentation
and reports, then agent context. The review grouped artifacts by the local goal
convenience of the current set rather than whether a required artifact may be
removed. Private VM settings, credentials, participant data and Customer
decisions were out of scope.

## Keeping A Reviewed Release Deliverable

- **Today:** [CFG-01](../../docs/configuration-plan.md#cfg-01), [CFG-02](../../docs/configuration-plan.md#cfg-02) and [CFG-03](../../docs/configuration-plan.md#cfg-03) link review, CI checks, documentation build and release evidence.
- **A more convenient way:** `Keep` the separate product, Markdown, link,
  documentation and workflow checks.
- **Why:** The checks report different failures and the release process needs
  each signal independently; combining their names or evidence would make it
  harder to identify whether a product regression or documentation error blocks
  delivery.
- **Tradeoffs:** Several workflows repeat checkout setup and action pins. That
  duplication costs maintenance, but separate reported checks preserve a clear
  review and release surface, so the team keeps them.

## Reproducing The Product Safely

- **Today:** [CFG-04](../../docs/configuration-plan.md#cfg-04) and [CFG-05](../../docs/configuration-plan.md#cfg-05) describe the environment shape, deployment instructions, images and dependency inputs.
- **A more convenient way:** `Keep` the public `.env.example` and runbook, and
  keep real values in the private submission material.
- **Why:** This separates the configuration shape needed by a new contributor
  from credentials and private deployment addresses, while the container and
  lockfiles make the checked build reproducible.
- **Tradeoffs:** A reader cannot reproduce the university deployment from the
  public repository alone. That loss is necessary because publishing its values
  would turn configuration documentation into a secret leak.

## Keeping Project Context Findable

- **Today:** [CFG-06](../../docs/configuration-plan.md#cfg-06), [CFG-07](../../docs/configuration-plan.md#cfg-07) and [CFG-08](../../docs/configuration-plan.md#cfg-08) provide agent instructions, indexes, report locations and the course rule router.
- **A more convenient way:** `Add` one direct link from the root `AGENTS.md` to
  the configuration plan; keep the v2-specific instructions limited to v2
  implementation conventions.
- **Why:** A repository-wide agent starts at the root instructions, while the
  configuration plan is the inventory it needs to understand builds, checks and
  maintained artifacts. The nested v2 file solves styling consistency but does
  not explain the whole repository.
- **Tradeoffs:** The root instructions gain one more maintained link. The small
  upkeep cost is worthwhile because it removes a discovery step and keeps the
  configuration inventory authoritative.

## What We Could Not Judge

The university VM's backup and snapshot policy was not available for this
review. The risk is that recovery could depend on redeploying from the
repository rather than restoring an environment snapshot; the configuration
plan therefore records the deployment runbook and public configuration shape,
not an unverified infrastructure guarantee.

## The First Change

The team would first add the configuration-plan link to the root `AGENTS.md`.
It keeps the existing course-skill router and v2 style instructions, removes
the need for an agent to discover the configuration inventory by searching, and
has the tradeoff that the root instructions gain one link that must stay valid.

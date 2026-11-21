# Configuration Plan

**Reviewed:** 2026-11-21

This is the maintained inventory of the configuration that builds, checks,
delivers and explains Debug GYM. Each connection records the edge and the
concrete consequence of breaking it.

## Source Control And Release

### CFG-01

The reviewed `main` branch, pull-request flow and release records.

- **Status:** Active
- **Type:** process
- **Purpose:** Changes are reviewed before they reach `main`, and a release can
  be traced from its GitHub release to its changelog and plan record. Without
  this process, a reader cannot tell which revision was released or reviewed.
- **Owner:** Team release owner.
- **Where:** GitHub branch protection for `main`, `CONTRIBUTING.md`,
  `CHANGELOG.md` and `docs/project-plan.md`.
- **Connections:**
  - `enforces` [CFG-02](#cfg-02): a changed workflow or failed check could be
    merged without independent review.
  - `produces` GitHub releases and tags: cutting a release before its
    changelog and plan records agree leaves deployment guidance contradictory.
- **What good looks like:** Changes reach `main` through reviewed pull
  requests, and each release has a matching tag, release body and dated
  changelog section, per [the branch-protection rule](https://github.com/inno-itpd/itpd/blob/main/requirements/repository-requirements.md#branch-protection)
  and [the release rule](https://github.com/inno-itpd/itpd/blob/main/requirements/releases-requirements.md#cutting-a-release).

## Checks

### CFG-02

The GitHub Actions checks that validate product code, documentation, links and
workflow syntax.

- **Status:** Active
- **Type:** CI pipeline
- **Purpose:** Product regressions, malformed Markdown, broken links and invalid
  workflow files are detected before delivery. Without these workflows, a green
  local check can hide a failed container or a broken public report link.
- **Owner:** Team CI owner.
- **Where:** `.github/workflows/product.yml`, `markdown.yml`, `lychee.yml`,
  `pages.yml` and `actionlint.yml`. The product workflow runs the root tests and
  the catalog application's tests; the v2 Django tests under `app/v2/debug_gym`
  are run by hand and no workflow runs them.
- **Connections:**
  - `reads` [CFG-05](#cfg-05): product checks build the dependency and
    container configuration; a changed lockfile or image without CI coverage
    can break the delivered application.
  - `enforces` [CFG-01](#cfg-01): required checks must keep their reported
    names, or `main` can wait for a check that no workflow produces.
  - `reads` `.lycheeignore`: an unexplained exclusion can hide a broken link.
- **What good looks like:** Required checks run on pull requests and `main`,
  third-party actions are pinned, and the latest `main` runs are green before
  submission, per [continuous integration](https://github.com/inno-itpd/itpd/blob/main/requirements/repository-requirements.md#continuous-integration).

### CFG-03

The documentation site build and its navigation.

- **Status:** Active
- **Type:** build configuration
- **Purpose:** Maintained documentation is rendered and its internal links are
  checked as a reader will use them. Without it, an index can point at a file
  that is not reachable from the published documentation site.
- **Owner:** Team documentation owner.
- **Where:** `mkdocs.yml`, `requirements-docs.txt`, `scripts/docs_links.py` and
  `docs/index.md`.
- **Connections:**
  - `reads` the maintained documents named in [CFG-07](#cfg-07): an omitted
    navigation entry makes a valid record hard to discover.
  - `produces` the documentation-site check in [CFG-02](#cfg-02): a build
    configuration error prevents that CI signal from being emitted.
- **What good looks like:** The strict documentation build succeeds and the
  navigation points to maintained documentation, per [continuous integration](https://github.com/inno-itpd/itpd/blob/main/requirements/repository-requirements.md#continuous-integration).

## Environments And Secrets

### CFG-04

The deployment runbook and public configuration shape.

- **Status:** Active
- **Type:** document and setting
- **Purpose:** A team member can prepare a local, staging or production
  deployment without committing secret values. Without it, configuration is
  recovered from a previous operator's shell or a private VM.
- **Owner:** Team deployment owner.
- **Where:** `docs/deployment.md`, `docs/setup.md`, `.env.example` and the
  private environment settings described in the Moodle wrapper.
- **Connections:**
  - `reads` [CFG-05](#cfg-05): the runbook deploys the Compose services and
    dependency versions; a service-name or variable mismatch makes deployment
    fail or drift.
  - `cites` [CFG-06](#cfg-06): agents and contributors must not put private
    values in the repository; a missing rule risks a credential leak.
- **What good looks like:** The four environments, deployment and rollback are
  documented, while real addresses and secrets stay private, per [environments and deployment](https://github.com/inno-itpd/itpd/blob/main/requirements/repository-requirements.md#environments-and-deployment).

## Dependencies And Builds

### CFG-05

The container build, Python dependency locks and dependency-update settings.

- **Status:** Active
- **Type:** dependency and build configuration
- **Purpose:** The applications and their checks use reproducible versions of
  Python packages, images and GitHub Actions. Without it, a clean checkout can
  fetch a different dependency set from the one CI exercised.
- **Owner:** Team dependency owner.
- **Where:** `Dockerfile`, `compose.yaml`, `requirements.lock`,
  `requirements.txt`, `app/adel_b/requirements.txt`,
  `app/v2/debug_gym/requirements.txt` and `.github/dependabot.yml`. The root
  `requirements.txt` pins a different `pytest` version from the one in
  `requirements.lock`, the container and the workflow install only the lock, the
  v2 requirements use version ranges that no workflow installs, and Dependabot
  watches only the repository root.
- **Connections:**
  - `produces` [CFG-02](#cfg-02): product and container checks build these
    inputs; an unpinned or incompatible update can fail the pipeline.
  - `reads` [CFG-04](#cfg-04): the deployment runbook names the services and
    configuration that this build provides; stale instructions cannot start the
    built product.
- **What good looks like:** Dependencies and third-party actions are pinned or
  updated through reviewed pull requests, and a clean documented build works,
  per [pinning third-party actions](https://github.com/inno-itpd/itpd/blob/main/requirements/repository-requirements.md#pinning-third-party-actions).

## Agent Context And Artifacts

### CFG-06

The root `AGENTS.md` and the v2-specific `app/v2/debug_gym/AGENTS.md`.

- **Status:** Active
- **Type:** agent instruction
- **Purpose:** A new agent learns repository-wide constraints before changing a
  course deliverable and receives v2 styling conventions only in the subtree
  they govern. Without them, agents can duplicate styles, edit private files or
  treat planned evidence as completed.
- **Owner:** All team members.
- **Where:** `AGENTS.md`, `app/v2/debug_gym/AGENTS.md` and the `app/v2/debug_gym/CLAUDE.md`
  that imports it. The root `AGENTS.md` does not yet describe `app/v2/` or its checks.
- **Connections:**
  - `cites` [CFG-08](#cfg-08): the root instructions route an agent to the
    course skill; a missing route leaves course requirements undiscovered.
  - `reads` this configuration plan: without the link, an agent cannot locate
    the inventory that explains the repository's configuration.
  - `cites` [CFG-07](#cfg-07): the instructions identify the locations and
    boundaries of maintained artifacts; a stale map sends changes to the wrong
    place.
- **What good looks like:** Instructions state the layout, checks, conventions
  and off-limits files, and direct agents to the course rules, per [agent instructions](https://github.com/inno-itpd/itpd/blob/main/requirements/agent-instructions-requirements.md#what-it-states).

### CFG-07

The maintained-document indexes and weekly-report process.

- **Status:** Active
- **Type:** documentation process
- **Purpose:** A reader can discover enduring documentation in `docs/` and each
  week's evidence in `reports/week-NN/`. Without the indexes and report process,
  a grader or later team member must infer which files are current evidence.
- **Owner:** Team documentation owner.
- **Where:** `docs/index.md`, the indexes under `docs/`, `reports/week-NN/` and
  `mkdocs.yml`.
- **Connections:**
  - `produces` [CFG-03](#cfg-03): indexes and navigation are rendered by the
    documentation build; a missing entry makes the artifact unreachable.
  - `cites` [CFG-01](#cfg-01): a release report links the merged release state;
    a report on an unmerged branch is not submission evidence.
- **What good looks like:** Durable material lives in `docs/`, weekly evidence
  lives in its report directory, and each report indexes its supporting
  artifacts, per [weekly public report](https://github.com/inno-itpd/itpd/blob/main/requirements/weekly-report-requirements.md#weekly-public-report).

### CFG-08

The course `SKILL.md` router and its installed course materials.

- **Status:** Active
- **Type:** skill
- **Purpose:** The team uses the course's current rule router before editing a
  deliverable. Without it, a contributor can satisfy a remembered example while
  missing the applicable requirement.
- **Owner:** All team members.
- **Where:** the course `SKILL.md` linked from `AGENTS.md` and the course
  materials available to repository tools.
- **Connections:**
  - `produces` the rules read by [CFG-06](#cfg-06): a changed course rule that
    is not consulted makes an agent's output non-compliant.
  - `cites` [CFG-07](#cfg-07): the router explains whether an artifact belongs
    in maintained documentation or weekly evidence.
- **What good looks like:** The team installs and follows the course skill but
  does not edit it, per [the course-materials skill rule](https://github.com/inno-itpd/itpd/blob/main/requirements/repository-requirements.md#the-course-materials-as-an-agent-skill).

### CFG-09

The former top-level `docs/README.md` documentation entry point.

- **Status:** Dropped
- **Type:** document
- **Purpose:** It was the earlier documentation entry point before the current
  `docs/index.md` navigation was adopted.
- **Owner:** Team documentation owner.
- **Where:** removed `docs/README.md`; replaced by `docs/index.md`.
- **Connections:**
  - `produces` the earlier documentation entry point; retaining both names
    would leave readers following an obsolete path.
- **What good looks like:** The active documentation entry point is
  `docs/index.md` and navigation uses it, per [where artifacts live](https://github.com/inno-itpd/itpd/blob/main/requirements/general-requirements.md#where-artifacts-live-in-the-repository).
- **Dropped:** 2026-10-02: the entry point was removed when `docs/index.md`
  became the maintained documentation index.

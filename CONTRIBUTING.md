# Contributing

## Issues and planning

All work starts in an issue. A story describes a user outcome; implementation
is split into task issues, and one pull request closes exactly one task. Assign
the issue to its sprint milestone and to the same two members named by its
`Responsible` and `Accountable` fields.

The team uses the public
[GitHub Projects sprint table](https://github.com/orgs/team-ok-ITPD/projects/1)
to see ownership and status across the repository. The table is grouped by
milestone so sprint scope and unscheduled work are visible together. Sprint
backlogs remain visible in the repository's
[milestones](https://github.com/team-ok-ITPD/team-OK-itpd/milestones).

## Week 4 issue conversion

The issue forms use native `User Story` and `Task` types. Stories link their
specifications under `Specified by`; open tasks link the FRs or ADRs they serve
under `Requirements`, or explain `None` for repository upkeep. Links point to
files already available on `main`.

Preview the existing-card conversion from the repository root:

```sh
python scripts/migrate_week4_issues.py --output-dir ../w4-preview
```

Use Git credential manager or a token in `GH_TOKEN` with repository issue access.
Inspect `issue-conversion.json`: it saves each original card and proposed patch.
After the specifications merge into `main`, run the same command with `--apply`
and a new output directory. Review the fresh snapshot too; each run reads current
cards rather than applying an older preview. Keep backups outside this repository.

The tool preserves story criteria and historical verification ticks, does not
close issues or post comments, and leaves milestones and priority fields intact.
It refuses missing specification links or unmapped stories, converts old type
labels to issue types, and retires MoSCoW labels only after checking that each
story has its MoSCoW field. It aligns assignees only where two distinct ownership
fields already exist. An interrupted application can be previewed and rerun; it
is not a transaction, so inspect the saved originals before undoing a change.
The preview is preparation, not evidence of a completed live conversion.

## Branches and commits

Name a branch `<issue-number>-<short-lowercase-description>`, for example
`52-week-03-planning`.

Use Conventional Commits in the form `type: short imperative description`.
Common types are `feat`, `fix`, `docs`, `test`, `ci`, and `chore`. Keep each
commit focused on one coherent change.

## Pull requests

A pull request must target `main`, link exactly one task with `Closes #nn`,
explain what changed and why, state how it was checked, and direct the reviewer
to the risky or requirement-sensitive parts. It also states whether the change
is user-visible and updates `[Unreleased]` when it is.

The accountable reviewer checks the task criteria, scope, tests, documentation,
privacy, and repository checks. They tick every task criterion before approving.
A member other than the author must approve, and the branch merges only through
its pull request after all checks are green.

The complete standard for stories, tasks, and pull requests is the
[Definition of Done](docs/definition-of-done.md).

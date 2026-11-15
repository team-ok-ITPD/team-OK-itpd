# Definition of done

## Story

- Every acceptance criterion passes on `main`.
- Every task issue that works on the story has closed with its pull request
  merged, so each also met the Task and Pull Request lists below.
- The story issue links the evidence for each criterion.
- The accountable member has checked that each criterion is runnable and that
  every link on the issue resolves.
- The story closes only after the Customer accepts it against its acceptance
  criteria.

## Task

- Every acceptance criterion the task carries is satisfied.
- The task closes as completed when the pull request that closes it merges into
  `main`.

## Pull Request

- A pull request closes exactly one task issue and links it.
- The accountable reviewer ticks every task acceptance criterion before
  approving.
- The approval comes from a member other than the author.
- The repository link, Markdown and `actionlint` checks are green.
- Product CI is green for the applicable build and automated-test checks; its
  linting, formatting and type-checking steps record why they are not
  applicable to the current stack.
- A user-visible change updates the `[Unreleased]` section of
  [`CHANGELOG.md`](../CHANGELOG.md).
- The acceptance criteria claimed by the pull request pass on its branch and on
  `main` after it merges.
- No secret, recording without publication permission, or private-only material
  is committed.
- The pull request description records implementation decisions and how the
  change was checked.

# Agent Instructions

Read the applicable rule through [the course SKILL.md](https://github.com/inno-itpd/itpd/blob/main/SKILL.md) before changing a course deliverable.

## Repository Layout

- `app/` is the Python catalog server and its `static/` HTML, CSS and JavaScript.
- `exercise/` is learner-facing buggy code, tests and debugger configuration; `exercise_author/` holds the reference implementation outside the workspace.
- `product_tests/` checks the product and the buggy/reference contract.
- `docs/` holds maintained requirements, architecture, plans and terminology.
- `reports/week-NN/` holds that week's evidence and AI disclosure.
- `scripts/` holds startup and documentation helpers; `.github/` holds CI and issue forms. `site/` is generated and ignored.

## Checks

- Install `requirements.lock` and run `python -m pytest -q` from the repository root. The intentionally buggy exercise fails its own tests; the product suite must pass.
- Run `docker compose config --quiet` and `docker compose build` for container changes. Product checks CI builds the image and smoke-tests both applications.
- Install `requirements-docs.txt` and run `python -m mkdocs build --strict`; Documentation site CI repeats it.
- Run `npx --yes markdownlint-cli2@0.20.0 "**/*.md"`; Markdown check CI repeats it.
- Check Links CI uses Lychee over the repository; external checks need network.
- Run `git diff --check`. Green pytest alone does not establish browser UI, SSH, authentication, Customer acceptance or quality-target compliance.

## Conventions

- Follow `CONTRIBUTING.md`: Conventional Commits, a `<task-number>-<slug>` branch, one task closed per PR and review by someone other than the author.
- Python uses four spaces and snake_case; frontend code is plain HTML/CSS/JavaScript. Preserve LF in shell scripts.
- Keep identifiers and anchors stable; distinguish required behavior from observed evidence.
- Preserve Customer criteria unless a genuine decision authorizes a change. Never invent approval or a completed test.
- Do not overwrite a learner's volume or reset it without a named disposable test project or the user's instruction.
- Disclose AI assistance in the current week's report.

## Files An Agent Must Not Edit

- `.env` and local credentials: the owner configures them; use `.env.example` for non-secret examples.
- `.git/` and `site/`: Git and the documentation builder own these outputs; change source and regenerate instead.
- `reports/week-01/`, `reports/week-02/`, `reports/week-03/`: preserve historical evidence; a team-authorized factual correction retains its date and never invents earlier approval or verification.
- `docs/decisions.md`: a member recording a real Customer decision verifies its source; agents must not invent verdicts or rewrite old decisions.
- Released changelog sections and release tags: the release owner handles corrections; ordinary changes go in `[Unreleased]`.

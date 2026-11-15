# Changelog

All notable user-visible changes to this project are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- The product records an analytics event for each core-task step, with a random
  learner identifier and no personal data, when an analytics backend is
  configured.
- The catalog search exposes a request-duration metric and a structured request
  log, so an operator can find a failed request and read its latency.

- A sourced administrator, teacher and student capability model, access constraints,
  proposed enforcement rules and unresolved policy questions.

### Changed

- Prepared exercise search matches titles and sits above the exercise list.
- Prepared exercises enforce private, signed-in public and assigned-group access,
  with server-filtered My, Public, Group and All catalog views.
- Teachers assign exercises to administrator-managed groups with an independent
  deadline per group, replacing direct student assignments and estimated duration.
- Submitted solutions are verified in a fresh, resource-limited container instead
  of trusting test counts reported by the browser or VS Code extension; concurrent
  verification and its waiting queue are bounded to protect the service.
- Open exercise pages detect new VS Code submissions, rerun their displayed tests
  and refresh results, reproduction and history without a page reload.

- Exercise pages use VS Code for source editing and retain reproduction, actions,
  tests and read-only output; manual actions read the latest saved solution.

### Fixed

- Successful registration and sign-in now open the learner or professor workspace
  instead of reporting a false server-reachability error.
- The teacher's student progress table fits its card and scrolls horizontally
  within the card on narrow screens.

## 0.3.0 - 2026-10-31

### Added

- A signed-in Django learner flow with separate persistent drafts and attempts.
- Browser-based VS Code launch, test-result display and solution submission.
- Prepared-exercise title search and automated Django and extension checks.

### Changed

- Product documentation now describes the implemented features, four
  environments, manual deployment and rollback procedure.

## [0.2.0](https://github.com/team-ok-ITPD/team-OK-itpd/releases/tag/v0.2.0) - 2026-10-25

### Added

- A linked functional-requirements index, architecture decision records and
  glossary, with documentation navigation and contribution guidance.

### Changed

- Setup and repository guidance now describe the optional launchers, tracked
  debugger configuration, workspace readiness and current MUP limitations.

### Fixed

- Exercise lookup rejects known unsupported bug categories instead of returning
  the list-mutation exercise because another keyword overlaps.

- The terminal in the browser workspace finds Python and pytest, so
  `python -m pytest -q` runs the exercise's tests.

## [0.1.0](https://github.com/team-ok-ITPD/team-OK-itpd/releases/tag/v0.1.0) - 2026-10-18

### Added

- Setup and reset instructions and a published documentation site for the
  prepared Python debugging exercise.

- A prepared Python list-mutation exercise that learners can find in plain
  language, open in browser-based VS Code, reproduce, debug, and verify with
  pytest.

# Changelog

All notable user-visible changes to this project are documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
the project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Open exercise pages detect new VS Code submissions, rerun their displayed tests
  and refresh results, reproduction and history without a page reload.

- Exercise pages use VS Code for source editing and retain reproduction, actions,
  tests and read-only output; manual actions read the latest saved solution.

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

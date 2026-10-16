# Decisions

## DEC-001

Start the prototype with Python.

- **Status:** Active
- **Date:** 2026-10-02
- **Made by:** Customer
- **Source:** [the Week 1 kickoff meeting](../reports/week-01/meeting-report.md#4-decisions)
- **Why:** Python is the first prototype language; Go and Java remain later possibilities.

## DEC-002

Keep VS Code access central to the first product direction.

- **Status:** Active
- **Date:** 2026-10-02
- **Made by:** Customer
- **Source:** [the Week 1 kickoff meeting](../reports/week-01/meeting-report.md#4-decisions)
- **Why:** learners need debugging tools, and VS Code connects them to the
  prepared environment through remote SSH.

## DEC-003

Treat the system as a prepared debugging harness, not only an exercise gallery.

- **Status:** Active
- **Date:** 2026-10-02
- **Made by:** Customer
- **Source:** [the Week 1 kickoff meeting](../reports/week-01/meeting-report.md#4-decisions)
- **Why:** the experience includes dependencies, language tooling, an isolated
  environment, broken code, reproduction commands, and tests that verify the
  fix.

## DEC-004

Preserve learner agency while using an agent for help.

- **Status:** Active
- **Date:** 2026-10-02
- **Made by:** Customer
- **Source:** [the Week 1 kickoff meeting](../reports/week-01/meeting-report.md#4-decisions)
- **Why:** the agent assists inside VS Code while the learner investigates and
  performs the fix; the exact assistance levels remain open.


## DEC-006

Generate each exercise as a correct program, a buggy program, and pytest tests.

- **Status:** Active
- **Date:** 2026-10-16
- **Made by:** Customer
- **Source:** [the Week 3 validation meeting](../reports/week-03/meeting-report.md#4-decisions)
- **Why:** The exercise author needs to see the intended bug and verify that the tests pass on the correct program and reproduce the bug on the buggy program. Pytest provides executable tests rather than relying only on AI-generated JSON input/output comparisons.

## DEC-007

Debug and submit in VS Code with a real debugger, not in a web editor.

- **Status:** Active
- **Date:** 2026-10-16
- **Made by:** Customer
- **Source:** [the Week 3 validation meeting](../reports/week-03/meeting-report.md#4-decisions)
- **Why:** Learners need real debugging tools, including breakpoints, and exercises may contain multiple files or modules. They should work on and submit their solutions through a VS Code workflow rather than a single web editor. Whether this is delivered as a standalone application, a browser-based environment, or a custom extension remains open.

## DEC-008

Show only a problem statement in the exercise preview.

- **Status:** Active
- **Date:** 2026-10-16
- **Made by:** Customer
- **Source:** [the Week 3 validation meeting](../reports/week-03/meeting-report.md#4-decisions)
- **Why:** Displaying source code and output in a small preview is unsuitable for large or multi-file exercises. A problem statement is sufficient for the learner to understand the exercise and decide whether to start it.

## DEC-009

Put the language choice in the centre of the request form.

- **Status:** Active
- **Date:** 2026-10-16
- **Made by:** Customer
- **Source:** [the Week 3 validation meeting](../reports/week-03/meeting-report.md#4-decisions)
- **Why:** The language selector was not immediately discoverable in the prototype. Placing it prominently in the central form area makes the language choice easier to find.

## DEC-010

Show the full output of the tests, not one row.

- **Status:** Active
- **Date:** 2026-10-16
- **Made by:** Customer
- **Source:** [the Week 3 validation meeting](../reports/week-03/meeting-report.md#4-decisions)
- **Why:** Test output can contain much more than a single value, potentially including thousands of values. Learners need access to the full test output to understand failures and investigate bugs.

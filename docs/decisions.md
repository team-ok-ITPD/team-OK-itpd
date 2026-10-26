# Decisions

## DEC-001

Start the prototype with Python.

- **Status:** Active
- **Date:** 2026-10-02
- **Made by:** Customer
- **Source:**
  [the Week 1 kickoff meeting](../reports/week-01/meeting-report.md#4-decisions)
- **Why:** Python is the first prototype language; Go and Java remain later
  possibilities.

## DEC-002

Keep VS Code access central to the first product direction.

- **Status:** Active
- **Date:** 2026-10-02
- **Made by:** Customer
- **Source:**
  [the Week 1 kickoff meeting](../reports/week-01/meeting-report.md#4-decisions)
- **Why:** learners need debugging tools, and VS Code connects them to the
  prepared environment through remote SSH.

## DEC-003

Treat the system as a prepared debugging harness, not only an exercise gallery.

- **Status:** Active
- **Date:** 2026-10-02
- **Made by:** Customer
- **Source:**
  [the Week 1 kickoff meeting](../reports/week-01/meeting-report.md#4-decisions)
- **Why:** the experience includes dependencies, language tooling, an isolated
  environment, broken code, reproduction commands, and tests that verify the
  fix.

## DEC-004

Preserve learner agency while using an agent for help.

- **Status:** Active
- **Date:** 2026-10-02
- **Made by:** Customer
- **Source:**
  [the Week 1 kickoff meeting](../reports/week-01/meeting-report.md#4-decisions)
- **Why:** the agent assists inside VS Code while the learner investigates and
  performs the fix; the exact assistance levels remain open.

## DEC-005

Build the minimum usable product with Docker, code-server, Python, and pytest.

- **Status:** Active
- **Date:** 2026-10-17
- **Made by:** Team
- **Source:** [the Week 3 planning task](https://github.com/team-ok-ITPD/team-OK-itpd/issues/52)
- **Why:** the Week 2 spike already demonstrated a browser-accessible VS Code
  environment with Python tooling and breakpoint debugging, while pytest gives
  each exercise executable reproduction and verification checks.
  
## DEC-006

Generate each exercise as a correct program, a buggy program, and pytest tests.

- **Status:** Active
- **Date:** 2026-10-16
- **Made by:** Customer
- **Source:**
  [the Week 3 validation meeting](../reports/week-03/meeting-report.md#4-decisions)
- **Why:** The exercise author needs to see the intended bug and verify that the
  tests pass on the correct program and reproduce the bug on the buggy program.
  Pytest provides executable tests rather than relying only on AI-generated JSON
  input/output comparisons.

## DEC-007

Debug and submit in VS Code with a real debugger, not in a web editor.

- **Status:** Active
- **Date:** 2026-10-16
- **Made by:** Customer
- **Source:**
  [the Week 3 validation meeting](../reports/week-03/meeting-report.md#4-decisions)
- **Why:** Learners need real debugging tools, including breakpoints, and
  exercises may contain multiple files or modules. They should work on and
  submit their solutions through a VS Code workflow rather than a single web
  editor. Whether this is delivered as a standalone application, a browser-based
  environment, or a custom extension remains open.

## DEC-008

Show only a problem statement in the exercise preview.

- **Status:** Active
- **Date:** 2026-10-16
- **Made by:** Customer
- **Source:**
  [the Week 3 validation meeting](../reports/week-03/meeting-report.md#4-decisions)
- **Why:** Displaying source code and output in a small preview is unsuitable
  for large or multi-file exercises. A problem statement is sufficient for the
  learner to understand the exercise and decide whether to start it.

## DEC-009

Put the language choice in the centre of the request form.

- **Status:** Active
- **Date:** 2026-10-16
- **Made by:** Customer
- **Source:**
  [the Week 3 validation meeting](../reports/week-03/meeting-report.md#4-decisions)
- **Why:** The language selector was not immediately discoverable in the
  prototype. Placing it prominently in the central form area makes the language
  choice easier to find.

## DEC-010

Show the full output of the tests, not one row.

- **Status:** Active
- **Date:** 2026-10-16
- **Made by:** Customer
- **Source:**
  [the Week 3 validation meeting](../reports/week-03/meeting-report.md#4-decisions)
- **Why:** Test output can contain much more than a single value, potentially
  including thousands of values. Learners need access to the full test output to
  understand failures and investigate bugs.

## DEC-011

Keep the default tests read-only and let learners add tests of their own.

- **Status:** Active
- **Date:** 2026-10-26
- **Made by:** Customer
- **Source:**
  [the Week 4 customer meeting](../reports/week-04/meeting-report.md#decisions)
- **Why:** The default tests are the source of truth: they fail when the program
  is buggy and pass when it is correct. Letting a learner edit them would remove
  that guarantee, while new tests of their own leave it intact.

## DEC-012

Design for desktop users and do not build for mobile.

- **Status:** Active
- **Date:** 2026-10-26
- **Made by:** Customer
- **Source:**
  [the Week 4 customer meeting](../reports/week-04/meeting-report.md#decisions)
- **Why:** The target learners are students who use their own computers in
  university labs and work with real code editors, so mobile support would cost
  effort for users the product does not serve.

## DEC-013

Make opening an exercise in VS Code a Must Have.

- **Status:** Active
- **Date:** 2026-10-26
- **Made by:** Customer
- **Source:**
  [the Week 4 customer meeting](../reports/week-04/meeting-report.md#decisions)
- **Why:** Desktop users who work with real tools need to open and solve an
  exercise in VS Code, so it is a must-have and not the delighter the team had
  proposed. This confirmed [DEC-007](#dec-007) and raised its priority.

## DEC-014

Submit the solution from VS Code, not from a button on the site.

- **Status:** Active
- **Date:** 2026-10-26
- **Made by:** Customer
- **Source:**
  [the Week 4 customer meeting](../reports/week-04/meeting-report.md#decisions)
- **Why:** If VS Code fills the screen, a learner should not have to switch back
  to the site to run tests or submit, so the command lives in VS Code and not on
  the site.

## DEC-015

Search only the prepared exercises and list every match below the filters.

- **Status:** Active
- **Date:** 2026-10-26
- **Made by:** Customer
- **Source:**
  [the Week 4 customer meeting](../reports/week-04/meeting-report.md#decisions)
- **Why:** A learner who does not remember an exercise's exact title needs to
  see several matches, and an AI-generated exercise is created fresh, so there
  is nothing to search. The first match is selected and nothing is previewed
  when there are no results.
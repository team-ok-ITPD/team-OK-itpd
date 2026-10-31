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

## DEC-016

Remove the code preview and the debug control from the workspace, show only the
tests, and update them dynamically.

- **Status:** Active
- **Date:** 2026-10-31
- **Made by:** Customer
- **Source:**
  [the Week 5 customer meeting](../reports/week-05/meeting-report.md#decisions)
- **Why:** Multi-file exercises with about 300 lines per file cannot be read in
  a small browser preview, and VS Code already shows the code. The test panel
  stays and must refresh after each run without a reload.

## DEC-017

Use three roles, admin, teacher and student, and let only teachers publish to
the public gallery.

- **Status:** Active
- **Date:** 2026-10-31
- **Made by:** Customer
- **Source:**
  [the Week 5 customer meeting](../reports/week-05/meeting-report.md#decisions)
- **Why:** A student could upload malicious code that others then run in the
  gallery or on the server. Exercises that teachers publish are assumed safe,
  because teachers have already checked that they work. The admin account is
  fixed in the system, and only the admin creates or changes teacher accounts.

## DEC-018

Let everyone except the admin generate exercises and use their own API key, and
let the admin's key serve teachers.

- **Status:** Active
- **Date:** 2026-10-31
- **Made by:** Customer
- **Source:**
  [the Week 5 customer meeting](../reports/week-05/meeting-report.md#decisions)
- **Why:** A teacher may want a stronger model than the admin's key provides,
  and one key with a limit cannot serve a cohort of 250 students. A student may
  also use an exercise that someone else generated, and then needs no key.

## DEC-019

Require authorization with a university email, with no public access for now.

- **Status:** Active
- **Date:** 2026-10-31
- **Made by:** Customer
- **Source:**
  [the Week 5 customer meeting](../reports/week-05/meeting-report.md#decisions)
- **Why:** The service is not expected to be public yet, and a shared link to
  an exercise opens only after sign-in. Student accounts are created from the
  university email, and sending the verification code is left to the team.

## DEC-020

Put all exercises in Prepared exercises with the access levels private, public
and group, and filters My, Public, Group and All.

- **Status:** Active
- **Date:** 2026-10-31
- **Made by:** Team
- **Source:**
  [the Week 5 customer meeting](../reports/week-05/meeting-report.md#decisions)
- **Why:** One list replaces a separate section for generated exercises. A
  student's own generated exercises stay private, a teacher can share an
  exercise with a group or publish it, and each exercise records its author and
  group.

## DEC-021

Let teachers form named groups, with one teacher per group, and download each
group's results as a CSV without grades.

- **Status:** Active
- **Date:** 2026-10-31
- **Made by:** Customer
- **Source:**
  [the Week 5 customer meeting](../reports/week-05/meeting-report.md#decisions)
- **Why:** Named groups let a teacher assign an exercise to a lab or exam
  group and collect analytics per group. The CSV shows who solved what and how
  many tests passed, with no overall statistics and no grades.

## DEC-022

Set a deadline per group and exercise, and count the best submission.

- **Status:** Active
- **Date:** 2026-10-31
- **Made by:** Customer
- **Source:**
  [the Week 5 customer meeting](../reports/week-05/meeting-report.md#decisions)
- **Why:** Different groups have labs at different times, so a deadline belongs
  to the pair of group and exercise and cannot spill over to another group. If
  the last edit were submitted automatically, a small change before the
  deadline could turn a passing result into a failing one.

## DEC-023

Keep the title search in Prepared exercises and rename its label so that it no
longer reads as a bug description.

- **Status:** Active
- **Date:** 2026-10-31
- **Made by:** Customer
- **Source:**
  [the Week 5 customer meeting](../reports/week-05/meeting-report.md#decisions)
- **Why:** The box labelled "Describe the bug you want to practice" only
  searches titles, so the label misleads a learner. This builds on
  [DEC-015](#dec-015).

## DEC-024

Keep Custom instructions, difficulty and language in the request form, drop
topic, and give Custom instructions priority on conflict.

- **Status:** Active
- **Date:** 2026-10-31
- **Made by:** Team
- **Source:**
  [the Week 5 customer meeting](../reports/week-05/meeting-report.md#decisions)
- **Why:** The language model knows several languages while a learner may think
  only of Python, so language and difficulty must be stated. Custom
  instructions can replace a fixed topic list, which cannot cover every topic.
  How usable free text is for a learner who has not met the bug is still to be
  analysed.

## DEC-025

Keep the left panel for started, unfinished exercises with tests passed and a
delete option, and remove the New Challenge button and the Back to practice
button.

- **Status:** Active
- **Date:** 2026-10-31
- **Made by:** Team
- **Source:**
  [the Week 5 customer meeting](../reports/week-05/meeting-report.md#decisions)
- **Why:** A learner may leave an exercise unfinished and return to it later.
  Deleting an exercise from the panel resets it as if it had never been started
  and cleans up its container.

## DEC-026

Build for the university first, with no paid features and no Moodle
integration.

- **Status:** Active
- **Date:** 2026-10-31
- **Made by:** Customer
- **Source:**
  [the Week 5 customer meeting](../reports/week-05/meeting-report.md#decisions)
- **Why:** The first aim is to test whether learning on bugs works for students
  and teachers of programming courses. The interface stresses structure, so
  that a student does not miss an exercise because of poor design. Integration
  with Moodle costs too much, and paid functions can wait.

## DEC-027

Accept `US-01`, requesting a prepared exercise.

- **Status:** Active
- **Date:** 2026-10-31
- **Made by:** Customer
- **Source:**
  [the Week 5 customer meeting](../reports/week-05/meeting-report.md#decisions)
- **Why:** The demonstrated prepared-exercise request satisfies the completed
  core learner increment; later generation and access requirements extend it.

## DEC-028

Accept `US-02`, opening a ready exercise environment.

- **Status:** Active
- **Date:** 2026-10-31
- **Made by:** Customer
- **Source:**
  [the Week 5 customer meeting](../reports/week-05/meeting-report.md#decisions)
- **Why:** The learner can open the prepared browser-based VS Code environment
  from the current application without setting up its Python tooling.

## DEC-029

Accept `US-03`, reproducing the intended bug.

- **Status:** Active
- **Date:** 2026-10-31
- **Made by:** Customer
- **Source:**
  [the Week 5 customer meeting](../reports/week-05/meeting-report.md#decisions)
- **Why:** The demonstrated exercise repeatedly exposes its intended failure
  through the supplied tests.

## DEC-030

Accept `US-04`, checking whether the fix works.

- **Status:** Active
- **Date:** 2026-10-31
- **Made by:** Customer
- **Source:**
  [the Week 5 customer meeting](../reports/week-05/meeting-report.md#decisions)
- **Why:** The learner can run the tests, inspect their result and submit the
  current solution through the implemented workflow.

## DEC-031

Accept `US-05`, using VS Code debugging tools.

- **Status:** Active
- **Date:** 2026-10-31
- **Made by:** Customer
- **Source:**
  [the Week 5 customer meeting](../reports/week-05/meeting-report.md#decisions)
- **Why:** Browser-based VS Code provides the real debugging environment used
  by the accepted core workflow; later access controls extend this capability.

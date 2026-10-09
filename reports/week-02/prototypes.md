# Week 02 prototypes

## Prepared debug environment in the browser

- **What it is:** a code spike: one Docker image with VS Code (code-server),
  Python, pytest, and the Python and debugger extensions preinstalled, started
  as one container per learner with the learner's files in a volume. The learner
  opens one URL and debugs a failing test, with nothing installed locally. It
  ran on a laptop, and it was not tested with many learners at once.
- **View:**
  [the debugger paused at a breakpoint in the exercise](images/debug-env.png).
- **Tested:** [`US-02`](https://github.com/team-ok-ITPD/team-OK-itpd/issues/29),
  exercising `AC-01` without the local VS Code install it assumes, and
  [`US-05`](https://github.com/team-ok-ITPD/team-OK-itpd/issues/32), exercising
  the breakpoint part of `AC-01` through a browser instead of remote SSH. Also
  [`ASM-07`](../../docs/assumptions.md#asm-07), because the setup effort was the
  risk.
- **Question:** can a learner get a debug-ready environment, with the debugger
  and extensions already installed, from a browser alone?

<!-- - **What the customer said:**
- **What changed:** -->

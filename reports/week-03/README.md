# Week 3 report

## Project

- **Project:** Debug GYM
- **Team:** Team 02
- **Week:** Week 3, Customer Validation and Initial Implementation
- **Scope:** Validate the Figma prototype with the customer, record product
  decisions, and prepare a runnable Python debugging exercise.

## Summary

The customer reviewed the New Challenge and Practice screens and clarified
several requirements. Learners need to debug and submit through VS Code with a
real debugger; an exercise should include a correct program, a buggy program,
and pytest tests; and the interface should make language selection easy to
find, preview only the problem statement, and show complete test output.

The repository also contains an initial runnable exercise flow: a catalog
service, a prepared Python exercise in a browser-based VS Code workspace, and
tests that confirm the exercise reproduces its bug and that the reference
solution passes. The delivery approach for VS Code and the environment for
running learner code are still open technical questions.

## Customer validation outcomes

The meeting recorded five decisions:

- [DEC-006: Include a correct program, a buggy program, and pytest tests](../../docs/decisions.md#dec-006)
- [DEC-007: Debug and submit in VS Code with a real debugger](../../docs/decisions.md#dec-007)
- [DEC-008: Show only the problem statement in the exercise preview](../../docs/decisions.md#dec-008)
- [DEC-009: Make language selection prominent in the request form](../../docs/decisions.md#dec-009)
- [DEC-010: Show the full test output](../../docs/decisions.md#dec-010)

The customer did not settle how VS Code will be delivered, where learner code
will execute, whether learners can see and edit all tests, or how to verify
that a generated exercise contains the intended bug. Follow-up actions and
meeting details are in the [customer validation meeting report](meeting-report.md).

## Runnable prototype

The prepared exercise, **The surviving negative**, demonstrates a Python list
mutation bug. The exercise instructions explain how to reproduce the failure,
debug it, and verify a fix in the VS Code workspace.

From the repository root, run:

```sh
docker compose up --build
```

The catalog is available at `http://localhost:3000`, and the browser-based
VS Code workspace is at `http://localhost:8080`. Docker Engine must be running.

## Coverage

| Deliverable | Artifact |
| --- | --- |
| Customer validation | [Meeting report](meeting-report.md), [script](meeting-script.md), and [transcript](meeting-transcript.md) |
| Product decisions | [DEC-006 through DEC-010](../../docs/decisions.md#dec-006) |
| Project milestone and sprint goals | [Project plan](../../docs/project-plan.md) |
| Exercise instructions | [The surviving negative](../../exercise/README.md) |
| Buggy exercise and reproduction tests | [Exercise source](../../exercise/remove_negatives.py) and [exercise tests](../../exercise/tests/test_remove_negatives.py) |
| Catalog and web interface | [Catalog service](../../app/server.py) and [static assets](../../app/static/) |
| Container setup | [Dockerfile](../../Dockerfile), [Compose configuration](../../compose.yaml), and [startup script](../../scripts/start.sh) |
| Product contract tests | [Catalog tests](../../product_tests/test_catalog.py) and [exercise contract tests](../../product_tests/test_exercise_contract.py) |

## Remaining questions

- Should learner code run in a sandboxed server-side container or on the
  learner's computer?
- Will learners see and edit all tests, or only selected tests?
- Will VS Code be standalone, browser-based, or supported through a custom
  extension?
- How can the team verify that an exercise contains the specific intended bug,
  beyond confirming that tests fail?

These questions and proposed follow-up actions are recorded in the
[meeting report](meeting-report.md). The decisions above do not resolve these
implementation choices.

## Privacy

The meeting report records that recording was permitted. No private-only
material is identified as a repository deliverable.

# Glossary

The words this project uses in one way only.

## Debugging Practice

### Exercise

A debugging task containing a problem statement, intentionally buggy code and tests with which the learner reproduces a defect and checks a fix.

**Defined by:** [`DEC-003`](decisions.md#dec-003), [`FR-003`](functional-requirements/fr/FR-003.md).

### Reference implementation

The author's known-correct program that must pass the same tests that expose the exercise's intended defect.

**Defined by:** [`DEC-006`](decisions.md#dec-006), [`ADR-002`](architecture/adr/ADR-002.md).

### Verification

Running the exercise tests against current learner code and inspecting complete pass-or-fail output, without recording a submission or trusted grade.

**Defined by:** [`FR-004`](functional-requirements/fr/FR-004.md), [`ADR-002`](architecture/adr/ADR-002.md).

### Assistance

A response requested by the learner in VS Code that leaves source files unchanged until the learner edits them.

**Defined by:** [`FR-006`](functional-requirements/fr/FR-006.md).

## Execution Environment

### Workspace

The prepared VS Code environment containing exercise files, Python tooling, a terminal and a debugger for the learner's investigation.

**Defined by:** [`FR-002`](functional-requirements/fr/FR-002.md).

### Container

A C4 application or data-store responsibility, which need not correspond one-to-one with a Docker container or Compose service.

**Defined by:** [`ADR-001`](architecture/adr/ADR-001.md).

### Reset

Deliberately deleting a selected local project's exercise volume and recreating the original buggy exercise, discarding learner edits.

**Defined by:** [`ADR-003`](architecture/adr/ADR-003.md).

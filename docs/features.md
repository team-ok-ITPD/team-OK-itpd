# Features

This page introduces Debug GYM's implemented capabilities in the order a
learner meets them. Project-specific words use the definitions in the
[glossary](glossary.md).

## Find A Prepared Exercise

A learner can search for a prepared [exercise](glossary.md#exercise) and open
one that matches the kind of Python bug they want to practise. My, Public,
Group and All views remain limited to exercises the signed-in learner may open.

- **Stories:** [US-01](https://github.com/team-ok-ITPD/team-OK-itpd/issues/28), [US-08](https://github.com/team-ok-ITPD/team-OK-itpd/issues/110)
- **Behavior:** [FR-001](functional-requirements/fr/FR-001.md)
- **Decisions:** [ADR-001](architecture/adr/ADR-001.md)

Teachers can keep their exercises private, publish them to signed-in users or
share them with members of assigned teaching groups. A copied link does not
grant access.

- **Story:** [US-09](https://github.com/team-ok-ITPD/team-OK-itpd/issues/111)
- **Access model:** [Roles and access](roles-and-access.md#exercise-audience)
- **Decisions:** [DEC-017](decisions.md#dec-017), [DEC-019](decisions.md#dec-019), [DEC-020](decisions.md#dec-020)

## Open A Ready Workspace

A learner can open a prepared [workspace](glossary.md#workspace) in
browser-based VS Code without installing the exercise's Python tooling.

- **Stories:** [US-02](https://github.com/team-ok-ITPD/team-OK-itpd/issues/29), [US-05](https://github.com/team-ok-ITPD/team-OK-itpd/issues/32)
- **Behavior:** [FR-002](functional-requirements/fr/FR-002.md), [FR-005](functional-requirements/fr/FR-005.md)
- **Decisions:** [ADR-001](architecture/adr/ADR-001.md), [ADR-003](architecture/adr/ADR-003.md)

## Reproduce The Bug

A learner can run an [exercise](glossary.md#exercise) repeatedly and observe
the intended failure before investigating it with VS Code's debugging tools.

- **Stories:** [US-03](https://github.com/team-ok-ITPD/team-OK-itpd/issues/30), [US-05](https://github.com/team-ok-ITPD/team-OK-itpd/issues/32)
- **Behavior:** [FR-003](functional-requirements/fr/FR-003.md), [FR-005](functional-requirements/fr/FR-005.md)
- **Decisions:** [ADR-001](architecture/adr/ADR-001.md), [ADR-002](architecture/adr/ADR-002.md)

## Verify And Submit A Fix

A learner can run [verification](glossary.md#verification), inspect the complete
test result and submit the current solution from VS Code.

- **Stories:** [US-04](https://github.com/team-ok-ITPD/team-OK-itpd/issues/31), [US-05](https://github.com/team-ok-ITPD/team-OK-itpd/issues/32)
- **Behavior:** [FR-004](functional-requirements/fr/FR-004.md), [FR-005](functional-requirements/fr/FR-005.md)
- **Decisions:** [ADR-001](architecture/adr/ADR-001.md), [ADR-002](architecture/adr/ADR-002.md)

## Assign Exercises To Groups

An administrator maintains each named teaching group's student membership. A
teacher can assign their own exercise to one of their groups, set an independent
deadline for that group/exercise pair and inspect each member's progress.

- **Story:** [US-09](https://github.com/team-ok-ITPD/team-OK-itpd/issues/111)
- **Access model:** [Roles and access](roles-and-access.md#groups-and-assignments)
- **Decisions:** [DEC-033](decisions.md#dec-033), [DEC-035](decisions.md#dec-035)

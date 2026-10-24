# Architecture

This document records the architecture serving the scope in the [product vision](../product-vision.md).

## Drivers

- **Business goals:** [the threshold of success](../threshold-of-success.md).
- **Constraints:** [the product vision's constraints](../product-vision.md#constraints).
- **Functional requirements:** [the functional requirements index](../functional-requirements/README.md).
- **Quality requirements:** [the quality requirements priority matrix](../quality-requirements/README.md).

## Container View

The product runs as two applications and one store in a learner-local Docker deployment, as decided in [ADR-001](adr/ADR-001.md).

![Container view](container.svg)

### Container Responsibilities

| Container | Responsibilities |
| --- | --- |
| `exercise catalog` | Serves the request UI and API; matches requests to prepared exercises; checks workspace readiness; owns in-memory catalog metadata. |
| `debug workspace` | Serves browser VS Code; runs Python, pytest and the debugger; reads and changes the exercise; owns the editor and debugger session. |
| `workspace store` | Stores exercise files and editor configuration; preserves edits across restarts; owns persistent learner state, discarded only by an explicit reset. |

The volume is passive storage; the operator's Compose reset recreates it, rather than the store executing a reset itself. The existing volume is not automatically migrated when an image changes.

The current deployment provides one local workspace, not a multi-user service. SSH and invalid-access refusal remain required but unimplemented. Assistance and category browsing are specified future behavior, not capabilities supplied by the boxes in this diagram. [ADR-003](adr/ADR-003.md) records the local-operation boundary.

## Diagrams And Legends

The container diagram's solid blue boxes are applications, the green cylinder is a data store, the dashed grey box is an external browser, and each arrow names the protocol and exchanged data. C4 containers are not Docker container count.

The image is [container.svg](container.svg) and its Mermaid source is [container.mmd](container.mmd). Regenerate the image from its source when changing the diagram. The broader vision's context diagram includes intended SSH and AI interactions; it is not a deployment inventory of implemented integrations.

## Architectural Decisions

The [unfilled template](adr/TEMPLATE.md) defines the record shape. Accepted records below document decisions already in force, not successful implementation of every addressed requirement.

| ADR | Status | Addresses | Decision |
| --- | --- | --- | --- |
| [ADR-001](adr/ADR-001.md) | Accepted | [`FR-001`](../functional-requirements/fr/FR-001.md), [`FR-002`](../functional-requirements/fr/FR-002.md), [`FR-003`](../functional-requirements/fr/FR-003.md), [`FR-004`](../functional-requirements/fr/FR-004.md), [`FR-005`](../functional-requirements/fr/FR-005.md), [`FR-006`](../functional-requirements/fr/FR-006.md), [`FR-007`](../functional-requirements/fr/FR-007.md), [`QR-03`](../quality-requirements/qr/QR-03.md), [`QR-04`](../quality-requirements/qr/QR-04.md) | Package The Catalog And VS Code Workspace Locally |
| [ADR-002](adr/ADR-002.md) | Accepted | [`FR-003`](../functional-requirements/fr/FR-003.md), [`FR-004`](../functional-requirements/fr/FR-004.md), [`QR-01`](../quality-requirements/qr/QR-01.md), [`QR-03`](../quality-requirements/qr/QR-03.md) | Validate Exercises With A Buggy Program And An Oracle |
| [ADR-003](adr/ADR-003.md) | Accepted | [`FR-002`](../functional-requirements/fr/FR-002.md), [`FR-005`](../functional-requirements/fr/FR-005.md), [`QR-02`](../quality-requirements/qr/QR-02.md), [`QR-05`](../quality-requirements/qr/QR-05.md) | Keep The Prototype Learner-Local With Persistent State |

# Architecture

The [product vision](../product-vision.md) defines the product scope and boundaries that this architecture supports.

## Architecture Drivers

### Functional Requirements

- [FR-001](../functional-requirements/fr/FR-001.md) requires the `exercise catalog` to match a prepared exercise.
- [FR-002](../functional-requirements/fr/FR-002.md) requires the catalog and workspace to provide a ready environment.
- [FR-003](../functional-requirements/fr/FR-003.md) requires repeatable reproduction of the intended bug.
- [FR-004](../functional-requirements/fr/FR-004.md) requires complete pass-or-fail verification output.
- [FR-005](../functional-requirements/fr/FR-005.md) requires access to VS Code debugging tools and refusal of invalid access.

### Quality Requirements

- [QR-01](../quality-requirements/qr/QR-01.md) makes exercise correctness a high-importance, high-risk driver.
- [QR-02](../quality-requirements/qr/QR-02.md) makes learner and host isolation a high-importance, high-risk driver.
- [QR-03](../quality-requirements/qr/QR-03.md) requires testability from a clean checkout.
- [QR-04](../quality-requirements/qr/QR-04.md) sets response-time targets for the catalog and workspace.
- [QR-05](../quality-requirements/qr/QR-05.md) requires recoverable exercise state.

The [quality-requirement priority matrix](../quality-requirements/README.md) records the business importance and technical risk of each driver.

### Constraints

- [CON-01](../product-vision.md#con-01) makes Python the first prototype language.
- [CON-02](../product-vision.md#con-02) keeps VS Code as the learner's access path.
- [CON-03](../product-vision.md#con-03) limits delivery and maintenance capacity to four people.
- [CON-04](../product-vision.md#con-04) limits the first release by the course schedule.

### Risks

- [RISK-02](../risks.md#risk-02) may prevent startup when images or extensions are unavailable.
- [RISK-03](../risks.md#risk-03) prevents a public pilot until learner-code isolation is validated.

## Container View

The current product runs as two applications and one data store in one learner-local Docker deployment.
The stack and separation of their responsibilities follow [ADR-001](adr/ADR-001.md).

![Container view](container.svg)

### Container Responsibilities

| Container          | Responsibilities                                                                                                                                                                                           |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `exercise catalog` | Serves the exercise request interface and API; matches requests to prepared exercises; checks workspace readiness before returning a link; owns the in-memory catalog metadata                            |
| `debug workspace`  | Serves the browser-based VS Code application; runs Python, pytest, and the debugger; reads and changes the learner's current exercise; owns the running editor and debugger session state                  |
| `workspace store`  | Stores the learner's current exercise files and editor configuration; preserves those files when the applications restart; replaces that state with the prepared buggy exercise when the learner resets it |

## Diagrams And Legends

Solid blue boxes are applications the team deploys, the green cylinder is a data store the team deploys, and the dashed grey box is an external system. Each solid arrow is labelled with the protocol and data that crosses it.

The image is [`container.svg`](container.svg), and its Mermaid source is [`container.mmd`](container.mmd). The image is generated with Mermaid.

## Architecture Decision Records

New records use the [ADR template](adr/TEMPLATE.md).

| ADR | Decision | Status | Drivers |
| --- | --- | --- | --- |
| [ADR-001](adr/ADR-001.md) | Adopt the Docker, code-server, Python, and pytest stack and split responsibilities | Accepted | [FR-001](../functional-requirements/fr/FR-001.md), [FR-002](../functional-requirements/fr/FR-002.md), [FR-003](../functional-requirements/fr/FR-003.md), [FR-004](../functional-requirements/fr/FR-004.md), [FR-005](../functional-requirements/fr/FR-005.md), [QR-03](../quality-requirements/qr/QR-03.md), [QR-04](../quality-requirements/qr/QR-04.md), [QR-05](../quality-requirements/qr/QR-05.md) |
| [ADR-002](adr/ADR-002.md) | Represent each exercise with buggy code, reference code, and pytest tests | Accepted | [FR-003](../functional-requirements/fr/FR-003.md), [FR-004](../functional-requirements/fr/FR-004.md), [QR-01](../quality-requirements/qr/QR-01.md), [QR-03](../quality-requirements/qr/QR-03.md), [QR-05](../quality-requirements/qr/QR-05.md) |
| [ADR-003](adr/ADR-003.md) | Isolate each learner workspace and bound learner-code execution | Accepted | [FR-002](../functional-requirements/fr/FR-002.md), [FR-005](../functional-requirements/fr/FR-005.md), [QR-02](../quality-requirements/qr/QR-02.md), [QR-04](../quality-requirements/qr/QR-04.md) |

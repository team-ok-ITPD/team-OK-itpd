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

## Teaching

### Teaching group

A named set of students with exactly one teacher. An administrator maintains
membership independently from account roles and exercise assignments.

**Defined by:** [`DEC-033`](decisions.md#dec-033).

### Group assignment

The relationship that makes one exercise available to one teaching group and
stores that group's independent deadline for the exercise.

**Defined by:** [`DEC-033`](decisions.md#dec-033), [`DEC-035`](decisions.md#dec-035).

### Exercise audience

The access level of an exercise: private to its author, public to signed-in
users or available to current members of its assigned teaching groups.

**Defined by:** [`DEC-019`](decisions.md#dec-019), [`DEC-020`](decisions.md#dec-020).

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

## Observability

| Term | Meaning in Debug GYM |
| --- | --- |
| Observability | Using emitted data to investigate the application's behavior. |
| Telemetry | The data the application emits about its operation. |
| Signal | A telemetry type, such as a metric, log or trace. |
| Service level indicator (SLI) | A measured aspect of service behavior, such as catalog request duration. |
| Observability backend | The self-hosted system that stores the product's metrics and logs and serves their dashboards. The team deploys it and does not build it. |

See the [observability plan](observability.md) for the signals and their queries.

## Analytics

| Term | Meaning in Debug GYM |
| --- | --- |
| Focus metric | The one number the product's value is read from: [solved exercises per active learner per week](analytics.md#solved-exercises-per-active-learner-per-week). |
| Input metric | A metric one level under another in the metric tree that explains movement in it. |
| Counter-metric | A metric that guards the focus metric rather than feeding it, such as [attempts per solved exercise](analytics.md#attempts-per-solved-exercise). |
| Metric tree | The nested list of the focus metric, its counter-metric and its input metrics in the [analytics plan](analytics.md#the-metric-tree). |
| Event | One action the product records, such as `exercise_opened`, with the fields in the [event table](analytics.md#the-events). |
| Instrumentation | The product code that emits an event or a signal. |
| Analytics backend | The self-hosted system that receives the product's events and serves their dashboards. The team deploys it and does not build it. |
| Dashboard | A page of charts in a telemetry backend, each running the query recorded in the plan. |

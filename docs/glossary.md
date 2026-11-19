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

## Usability Testing

| Term | Meaning in Debug GYM |
| --- | --- |
| Usability test | A planned study in which representative people attempt realistic product tasks while the team records predefined measures. |
| Participant | An eligible adult who consents to a counted usability session; their identity is private and represented publicly only by a `P-nn` code. |
| Usability session | One consented, recorded execution of the UT-01 protocol by one participant. |
| Consent | A participant's durable agreement to the session's recording, private handling and sanitized public results, with a withdrawal path. |
| Recording | Private screen/audio evidence of a consented session, deleted after course grading. |
| Measure | A directly recorded observation, such as a task's SEQ answer or time on task. |
| Metric | A defined quantitative value derived from measures, such as median main-task SEQ. |
| Statistic | A numerical summary calculated from the collected sample, such as a median or mean. |
| SUS | System Usability Scale: the prescribed ten-item, five-point post-test questionnaire and score. |
| SEQ | Single Ease Question: the seven-point ease rating asked after each task. |

## Configuration Management

### Configuration

The maintained files, settings and processes Debug GYM depends on to build,
check, deliver and explain the repository.

**Defined by:** [the configuration plan](configuration-plan.md).

### Configuration management

The team's practice of maintaining the configuration inventory and keeping it
accurate when a recorded configuration changes.

**Defined by:** [the configuration plan](configuration-plan.md).

### Configuration review

A goal-based judgement of whether Debug GYM's configuration artifacts are the
most convenient set for the purposes they serve.

**Defined by:** [the CM evaluation](../reports/week-08/cm-evaluation.md).

### Configuration plan

The maintained public inventory of Debug GYM's configuration items, owners,
locations and connections.

**Defined by:** [the configuration plan](configuration-plan.md).

### Configuration item

One maintained file, setting, process, dependency or skill that Debug GYM
depends on to be built, checked, delivered or understood.

**Defined by:** [the configuration plan](configuration-plan.md).

### Configuration evaluation

The Week 8 evidence that records a goal-based review of the configuration at a
frozen baseline.

**Defined by:** [the CM evaluation](../reports/week-08/cm-evaluation.md).

### Baseline

An identified frozen repository state against which a configuration evaluation
is made.

**Defined by:** [the CM evaluation](../reports/week-08/cm-evaluation.md).

### Upkeep

The work of keeping a maintained configuration record accurate when the
repository changes what that record describes.

**Defined by:** [the configuration plan](configuration-plan.md).

### Reproducible build

A Debug GYM build whose documented container and dependency inputs can be
checked again without silently selecting different versions.

**Defined by:** [CFG-05](configuration-plan.md#cfg-05).

### Dependency pinning

Recording a specific dependency or action revision so a Debug GYM build or CI
run uses the version the team reviewed.

**Defined by:** [CFG-05](configuration-plan.md#cfg-05).

### Secret

A private configuration value, credential or address that Debug GYM keeps out
of the public repository and public documentation.

**Defined by:** [CFG-04](configuration-plan.md#cfg-04).

### Context window

The limited repository context an agent can read in one session, which Debug
GYM's indexes and instructions must make sufficient for a correct change.

**Defined by:** [CFG-06](configuration-plan.md#cfg-06).

### Agent instruction

A repository or subtree `AGENTS.md` rule that directs an AI assistant's work
within its stated scope.

**Defined by:** [CFG-06](configuration-plan.md#cfg-06).

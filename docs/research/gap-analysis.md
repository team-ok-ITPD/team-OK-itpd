# Gap Analysis

These gaps are hypotheses derived from the three alternatives in [`comparison.md`](comparison.md). They describe opportunities to investigate, not validated user needs.

## GAP-01

Realistic tasks with a learner-facing experience.

- **Status:** Active
- **Who needs it and what they cannot do:** learners who want realistic
  debugging practice cannot work with repository-level tasks without taking on
  the setup burden of a research environment.
- **Evidence:** the `Debugging realism`, `Onboarding`, and
  `Extensibility / deployment` rows in [the comparison](comparison.md) show
  compact browser challenges in [ALT-01](alternatives.md#alt-01), a broad kata
  platform in [ALT-02](alternatives.md#alt-02), and repository-level tasks in a
  research framework with substantial setup in
  [ALT-03](alternatives.md#alt-03).
- **What closing it looks like:** a learner-facing product provides realistic,
  repository-level debugging without the setup burden of a research
  environment.
- **Buildable by us in this course:** yes, if the first version uses a small set
  of prepared exercises rather than a broad exercise library.
- **Confidence:** Medium. The alternatives establish the product gap, but the
  scale of codebase learners consider authentic and the setup they tolerate
  still require validation.

## GAP-02

Teach the investigation process, not only the final fix.

- **Status:** Active
- **Who needs it and what they cannot do:** learners who want to improve their
  debugging method cannot tell from final test results alone whether their
  investigation process is becoming repeatable.
- **Evidence:** the `Feedback & guidance` and `Investigation support` rows in
  [the comparison](comparison.md) show progressive hints in
  [ALT-01](alternatives.md#alt-01), test and solution feedback in
  [ALT-02](alternatives.md#alt-02), and rich observations intended primarily
  for agents in [ALT-03](alternatives.md#alt-03).
- **What closing it looks like:** feedback helps learners reason about their
  investigation steps as well as whether their final fix passes.
- **Buildable by us in this course:** yes, if process feedback is limited to the
  investigation signals and explanations used by the first exercise set.
- **Confidence:** Medium. The alternatives provide little learner-focused
  process feedback, but which signals learners find useful without revealing
  the answer still requires validation.

## GAP-03

Balance guidance and learner agency.

- **Status:** Active
- **Who needs it and what they cannot do:** learners who become stuck need help
  without having the investigation or fix completed for them.
- **Evidence:** the `Feedback & guidance` and `AI assistance` rows in
  [the comparison](comparison.md) show structured hints in
  [ALT-01](alternatives.md#alt-01), mostly result-oriented feedback in
  [ALT-02](alternatives.md#alt-02), and tools designed for agent interaction in
  [ALT-03](alternatives.md#alt-03).
- **What closing it looks like:** learners can request adjustable, timely
  guidance while retaining responsibility for the investigation and fix.
- **Buildable by us in this course:** yes, if guidance is optional and its
  initial levels are limited to the first exercise set.
- **Confidence:** Medium. The evidence shows different guidance models, but the
  timing and amount of help learners prefer still require validation.

## GAP-04

Lower setup friction while retaining useful investigation tools.

- **Status:** Active
- **Who needs it and what they cannot do:** learners who want to begin a
  debugging task quickly cannot get both low-friction onboarding and useful
  investigation tools from the evaluated alternatives.
- **Evidence:** the `Onboarding` and `Investigation support` rows in
  [the comparison](comparison.md) show low-friction browser access in
  [ALT-01](alternatives.md#alt-01) and [ALT-02](alternatives.md#alt-02), while
  the richer tools in [ALT-03](alternatives.md#alt-03) require Python, package,
  environment, and often Docker setup.
- **What closing it looks like:** learners start with little setup while still
  receiving enough tools for meaningful debugging.
- **Buildable by us in this course:** yes, if the product prepares one
  constrained environment and toolchain for the initial exercises.
- **Confidence:** Medium. The setup contrast is clear, but first-task
  observation is still needed to identify which steps block learners.

## Rejected from detailed comparison

These candidates were identified in the search but not selected for the three-product comparison. This is a scope decision, not a claim that they lack value.

| Candidate | Reason not selected |
| --- | --- |
| SWE-bench | Benchmark/task dataset rather than a learner-facing product. |
| BuLyst | Overlaps with the direct debugging-practice angle represented by BugHunt. |
| SadhanAI | AI-personalization angle is narrower than the selected comparison set. |
| Moss | Broader software-engineering task focus. |
| Before You Ask for Help | Process guidance rather than an interactive task platform. |
| Recticode | Overlaps with practice platforms; less contrast than the selected set. |
| Codritium | Broader software-engineering scope. |

See [`candidate-list.md`](../../reports/week-01/candidate_list.md) for the full searched list and screening notes.

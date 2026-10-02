# Gap Analysis

These gaps are hypotheses derived from the three alternatives in [`comparison.md`](comparison.md). They describe opportunities to investigate, not validated user needs.

## GAP-01: Realistic tasks with a learner-facing experience

**Evidence:** BugHunt uses compact bug challenges (ALT-01), while debug-gym supports repository-level tasks but is primarily an agent research framework (ALT-03). Codewars is a broad kata platform with debugging as one category (ALT-02).

**Gap:** Explore whether a learner-facing product can provide realistic, repository-level debugging without the setup burden of a research environment.

**Validation needed:** Ask learners what scale of codebase feels authentic and what setup they will tolerate.

## GAP-02: Teach the investigation process, not only the final fix

**Evidence:** BugHunt provides progressive hints and bug-pattern explanations (ALT-01). Codewars emphasizes tests and solution access (ALT-02). Debug-gym exposes debugging tools and observations for agent interaction (ALT-03).

**Gap:** Explore feedback that helps learners reason about investigation steps as well as whether their final fix passes.

**Validation needed:** Determine which process signals or explanations learners find useful without giving away the answer.

## GAP-03: Balance guidance and learner agency

**Evidence:** BugHunt's hints offer structured guidance (ALT-01); Codewars' feedback is mainly test output and solutions (ALT-02); debug-gym's tools are rich but designed for agent interaction (ALT-03).

**Gap:** Explore adjustable, timely guidance that supports a learner while leaving the investigation to them.

**Validation needed:** Test when learners want hints, how much detail they want, and whether guidance should be optional.

## GAP-04: Lower setup friction while retaining useful investigation tools

**Evidence:** BugHunt and Codewars are browser-based (ALT-01, ALT-02); debug-gym requires Python, package and environment setup, and often Docker (ALT-03).

**Gap:** Explore an onboarding path that makes it easy to start while still exposing enough tools for meaningful debugging.

**Validation needed:** Observe first-task completion and identify setup steps that block learners.

## Rejected from detailed comparison

These candidates were identified in the search but not selected for the three-product comparison. This is a scope decision, not a claim that they lack value.

| Candidate | Reason not selected |
|---|---|
| SWE-bench | Benchmark/task dataset rather than a learner-facing product. |
| BuLyst | Overlaps with the direct debugging-practice angle represented by BugHunt. |
| SadhanAI | AI-personalization angle is narrower than the selected comparison set. |
| Moss | Broader software-engineering task focus. |
| Before You Ask for Help | Process guidance rather than an interactive task platform. |
| Recticode | Overlaps with practice platforms; less contrast than the selected set. |
| Codritium | Broader software-engineering scope. |

See [`candidate-list.md`](../../reports/week-01/candidate-list.md) for the full searched list and screening notes.

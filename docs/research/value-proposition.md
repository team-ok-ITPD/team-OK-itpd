# Value Proposition

These are draft propositions to validate, not confirmed product commitments. They are informed by the gaps in [`gap-analysis.md`](gap-analysis.md).

## VP-01

Practice debugging in realistic code.

- **Status:** Active
- **User:** learners who want to improve their debugging skills.
- **Problem:** isolated snippets do not provide realistic practice in
  investigating and fixing bugs in existing code.
- **What we do that the alternatives do not:** provide learner-facing debugging
  tasks that can grow beyond isolated snippets into realistic code.
- **Closes:** [GAP-01](gap-analysis.md#gap-01).
- **Rests on:** [ASM-01](../assumptions.md#asm-01),
  [ASM-02](../assumptions.md#asm-02), and
  [ASM-03](../assumptions.md#asm-03).
- **What it costs:** realistic tasks require more exercise authoring and
  environment preparation than isolated snippets, so the initial exercise set
  has to remain small.
- **How a competitor would respond:** a browser challenge platform could add
  multi-file exercises, while a repository-level research framework could add
  a learner-facing workflow.

**Validation:** Ask learners to compare a snippet-based task with a small
multi-file task and describe which better supports their goals.

## VP-02

Learn a repeatable investigation process.

- **Status:** Active
- **User:** learners who want to build repeatable debugging habits.
- **Problem:** feedback focused on the final fix does not help learners improve
  how they investigate a bug.
- **What we do that the alternatives do not:** offer optional, staged guidance
  and feedback about the investigation as well as the final fix.
- **Closes:** [GAP-02](gap-analysis.md#gap-02) and
  [GAP-03](gap-analysis.md#gap-03).
- **Rests on:** [ASM-04](../assumptions.md#asm-04),
  [ASM-05](../assumptions.md#asm-05), and
  [ASM-06](../assumptions.md#asm-06).
- **What it costs:** staged guidance must be designed for each exercise and can
  reduce learner agency if it reveals too much.
- **How a competitor would respond:** an existing practice platform could add
  progressive hints or process feedback; the distinction depends on keeping
  that guidance tied to the learner's investigation.

**Validation:** Test optional hint levels and ask learners whether the guidance
changed their reasoning or merely revealed the answer.

## VP-03

Start quickly, then access useful tools.

- **Status:** Active
- **User:** learners who want to begin debugging without configuring a research
  environment first.
- **Problem:** low-setup alternatives provide limited investigation tools,
  while richer repository-level tools require substantial setup.
- **What we do that the alternatives do not:** make it straightforward to begin
  a debugging task while providing investigation tools as task complexity
  increases.
- **Closes:** [GAP-04](gap-analysis.md#gap-04).
- **Rests on:** [ASM-07](../assumptions.md#asm-07) and
  [ASM-08](../assumptions.md#asm-08).
- **What it costs:** the team must prepare and maintain the environment and
  limit the first version to a narrow toolchain and exercise set.
- **How a competitor would respond:** a browser practice platform could add
  richer debugging tools, or a self-hosted framework could simplify its
  learner onboarding.

**Validation:** Observe learners starting a first task and record where they
need help or abandon the flow.

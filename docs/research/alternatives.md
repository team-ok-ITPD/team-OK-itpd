# Alternative Research

## Problem space

Developers need to improve their ability to investigate and fix bugs in existing code, rather than only practice writing code from scratch.

## Properties

The following properties were selected before evaluating the alternatives:

1. **Debugging realism** — how closely the tasks resemble real debugging work rather than greenfield coding or algorithmic exercises.
2. **Investigation support** — tools available to investigate the root cause, such as tests, debuggers, tracing, visualizers, or logs.
3. **Feedback & guidance** — hints, explanations, reference solutions, or other feedback provided during or after a task.
4. **AI assistance** — whether AI is involved and what role it plays in the debugging process.
5. **Task variety & difficulty** — variety of bug types and ability to practice at different difficulty levels.
6. **Onboarding** — effort required to start and complete the first real debugging task.
7. **Extensibility / deployment** — ability to add custom tasks/tools and run or modify the system independently.

---

## ALT-01

BugHunt

- **Status:** Active
- **Kind:** Direct competitor, hosted
- **Link:** <https://www.trybughunt.com/>
- **Version looked at:** Website and challenge library, 2026-10-01
- **Depth of evaluation:** Tested the public challenge flow and reviewed the
  challenge library, bug-pattern pages, visualizer, and product description.
- **Problem it solves:** Helps developers practice finding and fixing bugs in
  existing code instead of only writing code from scratch.

**Observations by property**

| Property                       | Observation                                                                                                                                                                          |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Debugging realism**          | Challenges provide working code containing a specific bug and describe the symptom rather than directly identifying the cause. The user must investigate and fix the code.           |
| **Investigation support**      | Users can edit code, run it against tests, and use a step-through visualizer that shows execution and variable values.                                                               |
| **Feedback & guidance**        | Challenges provide three progressive hints and an explanation of the bug pattern after a successful fix.                                                                             |
| **AI assistance**              | No AI-based debugging assistant was observed in the public challenge flow.                                                                                                           |
| **Task variety & difficulty**  | Challenges cover Python and JavaScript and include patterns such as off-by-one errors, infinite loops, scope errors, null/undefined errors, logic errors, and async/race conditions. |
| **Onboarding**                 | A challenge can be started directly in the browser without an account or installation.                                                                                               |
| **Extensibility / deployment** | The public product is a hosted browser experience. No public mechanism for users to create or self-host their own challenge environment was observed during this evaluation.         |

**Strengths**

- The task structure closely matches the core debugging activity: the user receives existing code and a symptom, then has to locate and fix the bug.
- Progressive hints and explanations turn the result of a debugging attempt into a learning experience rather than simply marking the answer as correct.

**Weaknesses**

- The public experience does not appear to use AI to adapt the debugging process or provide conversational assistance.
- The challenges are relatively small and self-contained; the evaluated flow does not reproduce the complexity of debugging a multi-file repository or production-like codebase.
- The public product does not expose an obvious self-hosting or custom-environment workflow.

**Evidence:**

- Product flow and learning model: <https://www.trybughunt.com/>
- Challenge library: <https://www.trybughunt.com/challenges>
- Bug patterns: <https://www.trybughunt.com/bugs>
- Visualizer: <https://www.trybughunt.com/visualize>

---

## ALT-02

Codewars

- **Status:** Active
- **Kind:** Adjacent substitute, hosted
- **Link:** <https://www.codewars.com/kata?tags=Debugging>
- **Version looked at:** Website and official documentation, 2026-10-01
- **Depth of evaluation:** Reviewed the Debugging kata collection, kata trainer
  documentation, testing documentation, and kata authoring documentation.
- **Problem it solves:** Provides repeated coding practice through short
  challenges, including a dedicated Bug Fixes / Debugging category.

**Observations by property**

| Property                       | Observation                                                                                                                                                                                               |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Debugging realism**          | Codewars includes dedicated Bug Fixes kata where users analyze existing code, identify the issue, and fix it, but the overall platform also contains many greenfield algorithm and programming exercises. |
| **Investigation support**      | The trainer provides a code editor, sample tests, test output, and hidden full tests. Users can also add their own sample tests.                                                                          |
| **Feedback & guidance**        | Failed tests provide output; after completing or forfeiting a kata, users can access other users' solutions.                                                                                              |
| **AI assistance**              | No AI debugging assistant was observed in the evaluated trainer/documentation.                                                                                                                            |
| **Task variety & difficulty**  | The platform has many kata across languages and difficulty levels, with Debugging currently represented by a large collection of kata.                                                                    |
| **Onboarding**                 | The user can select a kata and enter the trainer directly; the trainer provides the task description, editor, tests, and output in one environment.                                                       |
| **Extensibility / deployment** | Users can author their own kata, including initial code, solutions, sample tests, submission tests, and language-specific configurations, but creating kata requires the appropriate authoring privilege. |

**Strengths**

- Large and varied practice ecosystem with explicit difficulty/ranking and many programming languages.
- Strong automated verification: sample tests can be run during development and a full hidden test suite is required for completion.

**Weaknesses**

- The platform is primarily a general coding-practice system; debugging is only one category among many rather than the central learning workflow.
- The trainer focuses heavily on whether the final solution passes tests; it does not explicitly evaluate or teach the user's investigation process.
- No AI debugging assistance was observed in the evaluated experience.

**Evidence:**

- Debugging kata: <https://www.codewars.com/kata?tags=Debugging>
- Kata trainer: <https://docs.codewars.com/references/kata-trainer/>
- Tests: <https://docs.codewars.com/concepts/kata/tests/>
- Bug-fixing kata authoring: <https://docs.codewars.com/authoring/tutorials/create-first-kata/>

---

## ALT-03

Microsoft debug-gym

- **Status:** Active
- **Kind:** Open-source, self-hosted
- **Link:** <https://github.com/microsoft/debug-gym>
- **Version looked at:** GitHub repository, main branch, 2026-10-01
- **Depth of evaluation:** Reviewed the repository README, system design,
  debugging tools, agent architecture, benchmark support, terminal backends,
  and human mode.
- **Problem it solves:** Provides an interactive environment for developing and
  evaluating AI debugging agents on repository-level Python debugging tasks.

**Observations by property**

| Property                       | Observation                                                                                                                                                                                              |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Debugging realism**          | The environment works with code repositories and supports repository-level debugging tasks, including a customized SWE-bench setup where tests fail before the debugging process and pass after the fix. |
| **Investigation support**      | Provides interactive tools including `bash`, `view`, `eval`, `pdb`, `grep`, `listdir`, `edit`, and `submit`.                                                                                             |
| **Feedback & guidance**        | The environment returns observations such as error messages, debugger output, and state changes after tool calls; evaluation can run tests after submission.                                             |
| **AI assistance**              | AI is central to the system: LLM-based agents interact with the debugging environment and use its tools to investigate and fix bugs.                                                                     |
| **Task variety & difficulty**  | Supports multiple benchmarks including SWE-bench, SWE-smith, R2E-Gym, Aider, and custom buggy snippets.                                                                                                  |
| **Onboarding**                 | Requires Python 3.12, package installation, LLM configuration, and environment setup. Docker is recommended for the terminal environment.                                                                |
| **Extensibility / deployment** | Highly extensible: users can add custom tools and configure agents, environments, benchmarks, LLM backends, and terminal implementations. It can run locally with Docker or at scale using Kubernetes.   |

**Strengths**

- Provides a rich interactive debugging environment rather than reducing debugging to repeated code generation and test execution.
- Highly extensible and self-hostable, allowing researchers to add custom tools, agents, benchmarks, and environments.
- Supports both LLM-based agents and a human mode for manually interacting with the debugging environment.

**Weaknesses**

- The system is designed primarily as a research framework for AI debugging agents rather than as a polished learning product for human developers.
- Setup is significantly more complex than browser-based alternatives: it requires Python, package installation, LLM configuration, and usually Docker.
- Current support is focused on Python repositories and Linux environments; the project explicitly describes limitations for other languages/platforms.

**Evidence:**

- Repository and installation: <https://github.com/microsoft/debug-gym>
- System design and tools: <https://github.com/microsoft/debug-gym#system-design>
- Human mode: <https://github.com/microsoft/debug-gym#32-human-mode>
- Responsible AI / intended use: <https://raw.githubusercontent.com/microsoft/debug-gym/main/RESPONSIBLE_AI.md>

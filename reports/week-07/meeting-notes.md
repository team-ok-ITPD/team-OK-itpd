# Week 7 customer meeting notes

## 1. Roles and permissions

### Administrator

The administrator has system-wide management responsibilities:

- Manage users.
- Create and edit groups and manage group membership.
- Add and remove students from groups.
- Assign students and professors to groups.
- View public and private bugs.
- View assignment information where needed for administration.

The discussion rejected giving administrators the professor's teaching
workflow for creating, editing or assigning exercises. The administrator may
need visibility of assignments, but assignment management belongs to the
professor.

### Professor

The professor's teaching workflow includes:

- View groups and their members.
- Browse public bugs and the professor's own private bugs.
- Create or select bugs and exercises.
- Assign exercises to groups.
- Set assignment deadlines.
- Edit or close assignments.
- Review group submissions, student code, grades and test results.

The discussion reaffirmed group-based assignment rather than assigning an
exercise directly to an individual student.

### Student

The student dashboard should expose:

- All groups the student belongs to; membership in multiple groups is
  supported.
- Pending assignments and deadlines.
- Grades and assignment details.
- A personal bug/practice workspace.
- Practice results and bug history.

Students should be able to solve assigned exercises and also practice
independently.

## 2. Core teacher-to-student workflow

The participants converged on the following central scenario:

1. The professor creates a bug or selects an existing one.
2. The professor assigns the exercise to a group.
3. Students in that group open and solve the exercise in the VS Code
   environment.
4. Students submit their solutions.
5. The system runs the exercise tests and reports the results.
6. The professor reviews group results, test outcomes and submitted source
   code.

The teacher-facing result view should expose test outcomes, including how many
tests passed. The exact dashboard layout and result fields still need
refinement.

## 3. Bug sources and exercise creation

Three possible sources were discussed:

- **Gallery:** public bugs/exercises published by others.
- **My bugs:** the professor's own private bugs.
- **AI:** newly generated bugs/exercises.

The proposed workflow is to select or generate an exercise on the website,
open it in VS Code, edit it there, and submit it back to the platform. A saved
new exercise should be private by default, with publication or group assignment
as a later action.

The participants discussed removing the embedded code editor from the
website's exercise-creation page and using a button to open the VS Code
container instead. The precise page layout and save/publish interaction were
not finalized.

## 4. VS Code and AI assistance

VS Code in the container-based environment was identified as the editing and
debugging environment for both professors and students. The discussion
considered manual editing and AI-assisted editing of generated or existing
bugs.

The team did not settle how an AI agent would be made available inside the
container, how it would be configured, or how API keys and quotas would work.
Possible approaches included a system-provided key and a professor-provided
key. These remain architecture and operating-cost questions.

The customer emphasized defining the required user scenarios and architecture
before reducing the work to a sequence of UI-only increments. The team
emphasized delivering the basic functioning pages first and introducing
advanced integrations incrementally. The implementation sequence therefore
needs further agreement, while the required scenarios must remain visible in
the architecture and backlog.

## 5. Tools available to students

The professor should be able to determine which development tools are available
to students while solving an exercise. Examples raised included linters,
debuggers and type checkers.

Container or Dockerfile configuration was discussed as one possible way to
provide those tools. The teacher-facing configuration mechanism, allowed-tool
model and container implementation remain open.

## 6. Submission review and suspicious solutions

The discussion distinguished ordinary test results from detecting unfair or
hacked solutions. A solution may pass known tests while exploiting leaked test
cases rather than implementing the intended behavior.

The participants discussed an AI-assisted review of all submissions after the
assignment deadline. The direction discussed was:

- The professor initiates the review rather than running an agent on every
  individual submission as it arrives.
- The system analyzes the collected submissions and identifies potentially
  suspicious solutions.
- The system presents flagged submissions to the professor.
- The professor reviews the code and can confirm or reject a suspicious flag.

Generated tests were considered as a possible additional signal, but they
cannot be trusted automatically because generated tests may be incorrect or
produce false positives. The review design, model, trigger, cost limits,
concurrency and false-positive handling still need specification. The
participants discussed using a system-provided API key for this capability;
quota and funding arrangements were not settled.

Malicious-code scanning was also mentioned, but no concrete scanner or
complete security design was selected.

## 7. Results and export

The professor needs to inspect submissions and test results at group level.
CSV export was discussed to support downstream grading and possible Moodle
workflows. The exact CSV columns, grading semantics and import process were
not decided.

## 8. Prioritization and delivery approach

The discussion identified the need to:

1. Define the main teacher and student scenarios.
2. Establish a coherent architecture and UI structure around those scenarios.
3. Prioritize the core teacher-to-student workflow.
4. Deliver the basic pages and a working end-to-end example incrementally.
5. Add advanced AI and submission-analysis capabilities in planned increments.

There was disagreement about whether AI-agent functionality could simply be
deferred as non-core. The customer stressed that the required scenarios and
architecture must account for it; the team stressed that implementation should
be staged to control complexity. No final detailed release sequence was
recorded.

## 9. Decisions and accepted direction

The report records the outcomes that were clear enough to treat as decisions.
The detailed reasoning and unresolved boundaries are in
[the meeting report](meeting-report.md) and
[the decision register](../../docs/decisions.md).

- Assignment creation and editing belong to professors; administrators may
  have assignment visibility but do not perform the professor's assignment
  workflow.
- The central workflow is professor selects/creates and assigns an exercise
to a group, students solve and submit, and the professor reviews submissions
  and test results.
- Professors need a way to specify which development tools students can use
  for an exercise; the configuration mechanism is not yet selected.
- A professor-initiated, system-supported review of all submissions for
  potentially suspicious solutions is the direction to design; operational
  details remain open.
- The professor needs an export of assignment results; the CSV schema remains
  open.

## 10. Unresolved questions

- What exact fields and drill-downs should the professor's group-results view
  show?
- What is the final exercise-creation interface and save/publish workflow?
- How are AI agents delivered into the VS Code container, and which API-key
  and quota model applies?
- How does a professor specify the tools available in the student container?
- What security checks are required for malicious code, separately from
  suspicious-solution analysis?
- What model, execution trigger, resource limits and false-positive workflow
  apply to post-deadline submission analysis?
- What is the CSV schema and how will it support Moodle or other grading
  workflows?
- What happens to submissions after the deadline?
- How are student group membership changes and assignment notifications
  presented?
- Can a group have multiple professors, and how are university accounts
  verified?

## Outcome

The meeting clarified the roles and the core group-assignment workflow, and
identified requirements for configurable student tools, post-deadline
submission review and result export. The exact UI, architecture, cost model,
security controls and detailed execution plan remain to be specified. See the
[meeting report](meeting-report.md) for the recorded decisions, follow-up work
and open questions.

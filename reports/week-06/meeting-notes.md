# Week 6 decision-focused meeting notes

## Editorial Note

This is a decision-focused set of notes made from two automatic transcripts.
It is not a verbatim transcript. The transcription service's
speaker labels are unreliable, so the entries below use neutral `Participant`
labels and record only enough dialogue to preserve the rationale and outcome.
The source recordings were provided to the team in two parts. Their filenames
and audio are not published in the repository.

## Part 1

### Product Roles And Student Flows

**[00:00:17-00:01:27] Participant:** The team reports three changes: removal of
the browser editor, dynamic result updates after submission, and a draft split
between administrator, teacher and student. Groups, assignments and deadlines
are the next increment if the direction is confirmed.

**[00:01:30-00:04:25] Participants:** The group clarifies three student flows:
solve an exercise assigned by a teacher, choose an exercise from the public
university gallery, or generate a private exercise for personal practice.
Student-created exercises do not enter the public gallery. Teacher assignments
go to groups rather than directly to individual students.

### Tests And Submission Safety

**[00:04:34-00:06:48] Participants:** The discussion identifies oversized or
malicious submissions as a risk. Client-side size checks alone are not trusted;
server-side limits are necessary. No numeric limit is selected.

**[00:07:18-00:08:45] Participants:** The group rejects both extremes of
showing no tests and exposing all verification tests. Students need selected
tests to reproduce the bug, while additional tests remain hidden. Container
isolation, not test secrecy alone, is responsible for execution safety.

**[00:09:00-00:12:29] Participants:** AI or external scanning is explored.
Token cost, arbitrary input size, false positives and preserving the exact
rejected artifact remain unresolved. No scanner or manual-review process is
selected.

**[00:12:29-00:14:36] Participants:** External security services and additional
network protection are discussed as future investigation. They are not made an
MVP commitment.

## Part 2

### Isolation And Exercise Boundaries

**[00:00:00-00:06:29] Participants:** The group confirms that the service must
run untrusted code safely. Existing container execution is acknowledged, while
a custom scanning platform is rejected as non-core work without further
research.

**[00:06:35-00:09:12] Participants:** File count, total size and supplementary
formats are discussed. Suggestions include five files, 1,000 lines per file,
one megabyte, CSV and text-like data. None is adopted; the team will measure
representative exercises and propose an MVP boundary.

### Teacher Workflow

**[00:09:17-00:12:50] Participants:** A teacher starts from groups, opens one
group and inspects assigned exercises and learner results. Pass/fail, passed
test counts, failed-test details and learner source are considered, but the
exact dashboard and CSV schema remain open.

**[00:13:05-00:15:05] Participants:** Exercises are created independently and
then assigned to one or more groups. The group chooses to validate the exact
teacher dashboard through a prototype instead of fixing the layout verbally.

**[00:16:25-00:17:49] Participants:** Estimated duration is removed. A deadline
belongs to an exercise assignment for a group. Assignment controls select
groups rather than individual students, and group membership is managed in a
separate administrator flow.

### Learner Page And Scope

**[00:18:05-00:19:34] Participants:** The demonstrated branch still contains
browser-editor elements because of an incorrect merge. Their removal remains
the decision. The learner page keeps reproduction and test information, even
though VS Code also displays tests.

**[00:20:45-00:23:23] Participants:** A group-first teacher flow is refined.
The suggestion to model legal excuses or per-student exceptions in Debug GYM is
withdrawn; Moodle remains responsible for legal-excuse handling.

### Submission Containers And Queue

**[00:23:55-00:26:10] Participants:** Hidden tests must not be readable by
submitted code. Each submission creates a fresh temporary container, runs the
verification there, returns the result and destroys the container.

**[00:24:53-00:26:33] Participants:** Concurrent submission containers are
bounded. Excess work enters a bounded queue and the learner sees a waiting
message. The numeric limits remain open.

## Outcome

The maintained outcomes are in the [meeting report](meeting-report.md). That
report intentionally excludes proposals that did not reach agreement.

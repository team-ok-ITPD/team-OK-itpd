# Week 6 AI Usage

## Tools

- An online transcription service converted the two meeting recordings to text.
- OpenCode compared the transcript with the previous meeting records and
  Assignment 6, then helped structure the report, notes and decision records.
- OpenCode reviewed the merged teaching workflow and helped implement and test
  isolated server-side submission verification.
- OpenCode helped migrate individual exercise assignments to administrator-managed
  groups, update the teaching interface and verify access and deadline behavior.
- OpenCode helped implement and test private, signed-in public and group exercise
  audiences, catalog filters and consistent server-side access checks.
- Claude drafted the analytics plan, FR-014 and ADR-006, the analytics event
  emitter, its call sites, the smoke-event script and their tests, and the
  observability requirement, decision record, quality requirement, test script
  and container view update.
- Claude drafted the issue and pull request texts and the Week 6 report
  structure.

## Review And Use

The team did not trust the automatic speaker labels. The retained notes use
neutral participant labels, preserve timestamps and classify an outcome as a
decision only where the discussion reached a clear agreement. Exploratory
security products, numeric limits, dashboard layouts and export fields remain
open rather than being promoted to requirements.

The public repository receives sanitized, decision-focused notes, not the
recordings or a verbatim transcript. A team member must review the decisions,
owners and due dates before merge.

Claude could not run Django, Docker, the university VM or either telemetry
backend. A team member ran the Django tests and sent real events to a temporary
HTTPS request catcher, and must review every drafted record, status and claim
before merge. The observability test script has not been run against an
observability backend.

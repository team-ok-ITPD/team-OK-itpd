# Week 02 report

## Project

- **Project:** Debug GYM
- **Team:** Team 02
- **Week:** Week 2, Requirements and Prototyping
- **Scope:** issue-based requirements, maintained decisions and assumptions,
  product vision and system context, a minimum usable product candidate, a
  technical prototype record, and documentation CI.

## Summary

The team moved the Week 1 decisions and assumptions into maintained logs,
defined the product vision and boundary, opened seven prioritized user stories,
proposed a minimum usable product candidate, and recorded a browser-based
debugging environment spike. We also normalized the research identifiers and
added green link and Markdown checks on `main`.

The technical spike challenged the expectation that useful debugging tools
necessarily require local environment setup: on one laptop, code-server
provided a prepared browser environment with breakpoint debugging. This does
not yet establish customer acceptance or multi-user capacity.

Still open are the eighth required story, the customer's verdict on the MUP
candidate, customer feedback on the prototype, the resulting artifact change,
and the kickoff questions that require customer input.

## Minimum Usable Product Candidate

Core task: a learner asks for a Python debugging exercise, reproduces the bug
in a prepared environment, uses the VS Code debugger to find it, fixes it, and
sees the verification tests pass.

- [`US-01`: Get an exercise for a bug type I want to practice](https://github.com/team-ok-ITPD/team-OK-itpd/issues/28)
- [`US-02`: Start debugging without setting up tooling](https://github.com/team-ok-ITPD/team-OK-itpd/issues/29)
- [`US-03`: Reproduce the bug on demand](https://github.com/team-ok-ITPD/team-OK-itpd/issues/30)
- [`US-04`: Find out whether my fix works](https://github.com/team-ok-ITPD/team-OK-itpd/issues/31)
- [`US-05`: Use VS Code debugging tools on the exercise](https://github.com/team-ok-ITPD/team-OK-itpd/issues/32)

Customer's verdict is pending. No `DEC-nnn` is claimed until the customer
responds.

Prototype-driven change: pending customer feedback; no resulting change is
claimed yet.

## Coverage

| Deliverable | Artifact |
| --- | --- |
| Kickoff action points | Not yet recorded in the required `Previous action points` section; see the current [reports/week-02/meeting-report.md](meeting-report.md). |
| Kickoff open questions | Not yet recorded in the required `Previous open questions` section; see the current [reports/week-02/meeting-report.md](meeting-report.md). |
| Product vision | [docs/product-vision.md](../../docs/product-vision.md) |
| System context diagram | [docs/architecture/context.svg](../../docs/architecture/context.svg) and [docs/architecture/context.mmd](../../docs/architecture/context.mmd), embedded in the product vision. |
| Assumptions | [docs/assumptions.md](../../docs/assumptions.md) |
| Decisions | [docs/decisions.md](../../docs/decisions.md) |
| Story issues | [Issues filtered by the `user-story` label](https://github.com/team-ok-ITPD/team-OK-itpd/issues?q=label%3Auser-story) |
| Issue forms | [.github/ISSUE_TEMPLATE/user-story.yml](../../.github/ISSUE_TEMPLATE/user-story.yml), [.github/ISSUE_TEMPLATE/task.yml](../../.github/ISSUE_TEMPLATE/task.yml), and [.github/ISSUE_TEMPLATE/config.yml](../../.github/ISSUE_TEMPLATE/config.yml) |
| Labels | [Repository labels](https://github.com/team-ok-ITPD/team-OK-itpd/labels) |
| Pull request template | [.github/pull_request_template.md](../../.github/pull_request_template.md) |
| Prototypes | [reports/week-02/prototypes.md](prototypes.md) |
| Meeting script | [reports/week-02/meeting-script.md](meeting-script.md) |
| Customer validation | Customer feedback is pending; the current internal record is [reports/week-02/meeting-report.md](meeting-report.md), and no customer transcript exists yet. |
| AI usage | [reports/week-02/ai-usage.md](ai-usage.md) |

## Contribution

| Member | Work |
| --- | --- |
| [@Danashi11](https://github.com/Danashi11) | Issue workflow and maintained logs ([PR #17](https://github.com/team-ok-ITPD/team-OK-itpd/pull/17), [PR #21](https://github.com/team-ok-ITPD/team-OK-itpd/pull/21), [PR #23](https://github.com/team-ok-ITPD/team-OK-itpd/pull/23)); Markdown cleanup, research migration, and CI ([PR #27](https://github.com/team-ok-ITPD/team-OK-itpd/pull/27), [PR #46](https://github.com/team-ok-ITPD/team-OK-itpd/pull/46), [PR #47](https://github.com/team-ok-ITPD/team-OK-itpd/pull/47)). |
| [@qwxiae](https://github.com/qwxiae) | [User stories](https://github.com/team-ok-ITPD/team-OK-itpd/issues?q=author%3Aqwxiae+label%3Auser-story), product vision ([PR #26](https://github.com/team-ok-ITPD/team-OK-itpd/pull/26)), MUP candidate ([PR #36](https://github.com/team-ok-ITPD/team-OK-itpd/pull/36)), and prototype record ([PR #39](https://github.com/team-ok-ITPD/team-OK-itpd/pull/39)). |
| [@adelazzi](https://github.com/adelazzi) | Week 2 planning, AI usage, and supporting design artifacts ([PR #42](https://github.com/team-ok-ITPD/team-OK-itpd/pull/42)); reviews of the MUP, prototype, issue workflow, and Markdown CI pull requests. |
| [@UTKANOS-RIBA](https://github.com/UTKANOS-RIBA) | Participated in the Week 2 internal planning ([meeting notes](meeting-notes.md)) and was assigned the reference-platform presentation role in the [meeting script](meeting-script.md#roles). |

## Repository Evidence

- [PR #47](https://github.com/team-ok-ITPD/team-OK-itpd/pull/47) was reviewed,
  approved, merged, and closed task issue `#44`.
- [Latest green link check on `main`](https://github.com/team-ok-ITPD/team-OK-itpd/actions/runs/38044716086).
- [Latest green Markdown check on `main`](https://github.com/team-ok-ITPD/team-OK-itpd/actions/runs/38044716090).
- No links are excluded from automated checking.

## Deviations

- Customer validation is being handled asynchronously after the current
  reporting point. The customer verdict, prototype reaction, and resulting
  artifact change remain pending and are not presented as completed work.
- Seven user stories are currently open; the required eighth story remains to
  be defined without inventing an unsupported product requirement.

## Privacy

No private-only material was committed to this repository. No customer
transcript has been produced because customer feedback is still pending.

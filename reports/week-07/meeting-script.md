# Meeting script

## Context

Our problem-space sentence: a professor who wants to teach debugging needs one place where exercises can be created or selected, assigned to groups, solved by students in a real VS Code environment, and evaluated through automated tests and submission review.

The previous discussion established three distinct roles: administrator, professor and student. The administrator manages users and groups, the professor manages exercises and assignments, and students solve assigned exercises and practise independently.

The central workflow is agreed at a high level: the professor creates or selects an exercise, assigns it to a group, students solve and submit it through VS Code, the system runs tests, and the professor reviews the results and submitted code.

However, several important decisions remain open. These include the precise role permissions, exercise creation and publication flow, AI integration in VS Code, available development tools, suspicious-submission analysis, and CSV export. The architecture must account for these scenarios even if some capabilities are implemented incrementally.

Target: validate the proposed role-based workflows, agree on the architecture and behavior of the core teacher-to-student scenario, resolve the most important open questions, and establish implementation priorities.

## Agenda

1. Role responsibilities and permissions (5 min). Questions 1–5.
   Show: the administrator, professor and student dashboards or proposed wireframes, and the role-permission matrix.

2. The core teacher-to-student workflow (8 min). Questions 6–10.
   Show: one complete scenario from selecting an exercise to assigning it to a group, student submission through VS Code, automated test execution and professor review.

3. Exercise creation and bug sources (5 min). Questions 11–14.
   Show: the proposed Gallery, My bugs and AI exercise sources, and the exercise creation page with the proposed VS Code integration.

4. VS Code, AI assistance and development tools (7 min). Questions 15–19.
   Show: the proposed container architecture, VS Code environment and configuration options for student development tools.

5. Submission review, suspicious solutions and export (7 min). Questions 20–24.
   Show: the proposed professor results dashboard, test results, suspicious-submission review flow and CSV export example.

6. Architecture, prioritization and delivery plan (5 min). Questions 25–28.
   Show: the proposed architecture, main user scenarios and prioritized backlog.

7. Read back the decisions and action points (3 min). Question 29.
   Show: the note taker's list of decisions, unresolved questions, action owners and deadlines.

## Questions

1. _(closed)_ Do you agree with the proposed three-role model: administrator, professor and student?

2. _(closed)_ Should administrators have system-wide user and group management permissions without having the professor's exercise creation and assignment workflow?

3. _(closed)_ Should administrators be able to view public and private bugs and assignment information for administrative purposes?

4. _(closed)_ Should professors be responsible for creating or selecting exercises, assigning them to groups, setting deadlines and reviewing submissions?

5. _(closed)_ Should students be allowed to belong to multiple groups and have both assigned exercises and an independent personal practice workspace?

6. _(closed)_ Do you agree that assignments should always be made to groups rather than directly to individual students?

7. _(open)_ Is any important step missing from the proposed workflow: exercise selection, group assignment, student solving, submission, automated testing or professor review?

8. _(closed)_ Should students solve exercises and submit their solutions through VS Code in a container-based environment?

9. _(closed)_ Should the system automatically run exercise tests after a student submits a solution and make the results available to the professor?

10. _(open)_ What information should the professor see when reviewing submissions? Consider passed and failed tests, source code, grades, individual student results and group-level summaries.

11. _(closed)_ Are Gallery, My bugs and AI sufficient as the three initial sources of exercises?

12. _(closed)_ Should newly created exercises be private by default, with publication to the Gallery or assignment to a group as separate actions?

13. _(open)_ Do you agree with removing the embedded code editor from the exercise creation page and using a button to open the exercise in VS Code instead? What functionality must remain on the website?

14. _(open)_ What should the exercise save, publish and assignment workflow look like when a professor finishes editing an exercise in VS Code?

15. _(closed)_ Should VS Code in the container environment be the common development and debugging environment for both professors and students?

16. _(open)_ How should AI assistance be provided inside the VS Code container? Should we use a system-provided API key, a professor-provided key, or support both?

17. _(open)_ Who should be responsible for API costs, quotas and usage limits for AI-assisted editing and submission analysis?

18. _(open)_ Which development tools should professors be able to enable or disable for students? Consider linters, debuggers and type checkers.

19. _(open)_ Should development tools be configured through a teacher-facing interface, predefined container profiles or Dockerfile configuration? What level of control does the professor need?

20. _(closed)_ Should suspicious-submission analysis be initiated by the professor after the assignment deadline rather than automatically for every submission?

21. _(open)_ What evidence should the AI-assisted review use to identify potentially suspicious solutions? Should it compare submitted source code, test results, similarities between submissions and additional generated tests?

22. _(closed)_ Should AI-generated suspicious-submission flags be treated only as recommendations that the professor must review and confirm or reject?

23. _(open)_ What false-positive rate and explanation would be acceptable before the professor can trust suspicious-submission detection? How should the system handle incorrect generated tests?

24. _(open)_ What information should be included in CSV exports to support grading and possible Moodle integration? Consider student identifiers, group, grades, test results and assignment information.

25. _(open)_ What architecture must be established now to support the complete teacher and student scenarios, including AI integration and submission analysis, even if those features are implemented later?

26. _(open)_ Which parts of the system should be delivered first to demonstrate a functioning end-to-end teacher-to-student workflow?

27. _(open)_ Which capabilities can be deferred to later increments without requiring major architectural changes? Please consider AI-assisted editing, suspicious-submission analysis, generated tests and advanced tool configuration.

28. _(closed)_ Do you agree with prioritizing the basic role-based pages and one complete working assignment scenario before implementing advanced integrations?

29. _(closed)_ Does this read-back accurately record every decision, rejected or deferred item, unresolved question and action point with its owner and deadline?

## Roles

Meeting date: 2026-11-13.

Expected participants: `Customer` and `Project team`.

Suggested responsibilities:

- `Project team`: presents the proposed workflows, architecture and working software.
- `Customer`: validates requirements, clarifies expected behavior and makes product decisions.
- `Meeting facilitator`: asks questions and keeps the discussion focused.
- `Note taker`: records decisions, open questions, rejected proposals and action points.
- `Technical representative`: explains architecture, VS Code integration, containers and AI-related constraints.

## Key improvements

### "Should we give administrators all the same features as professors?" -> "Should administrators have system-wide user and group management permissions without having the professor's exercise creation and assignment workflow?"

The original question combines two different responsibilities. The rewrite separates administrative management from teaching responsibilities, helping prevent unnecessary permission overlap and unclear ownership.

### "Should we implement AI?" -> "How should AI assistance be provided inside the VS Code container? Should we use a system-provided API key, a professor-provided key, or support both?"

The original question is too broad to produce an architectural decision. The rewrite identifies concrete alternatives and encourages discussion of API costs, quotas and responsibility.

### "Should AI detect cheating?" -> "What evidence should the AI-assisted review use to identify potentially suspicious solutions?"

Passing automated tests does not necessarily mean that a solution correctly implements the intended behavior. The rewrite focuses on the evidence and limitations of detection instead of assuming that AI can reliably determine whether a student cheated.

### "Should we implement everything incrementally?" -> "Which capabilities can be deferred to later increments without requiring major architectural changes?"

The original question risks treating advanced features as unnecessary. The rewrite distinguishes between implementing a feature now and accounting for it in the architecture from the beginning.

### "Is the professor dashboard good?" -> "What information should the professor see when reviewing submissions?"

The original question invites a general opinion without establishing requirements. The rewrite identifies concrete information needed for grading and feedback, making the dashboard requirements more actionable.

## Expected meeting outcomes

By the end of the meeting, we should have:

1. An agreed role and permission model for administrators, professors and students.
2. A validated end-to-end teacher-to-student workflow.
3. An agreed approach to exercise creation, selection, editing and publication.
4. Clear architectural direction for VS Code containers and development tools.
5. A decision or documented alternatives for AI integration and API costs.
6. An agreed direction for submission review and suspicious-solution detection.
7. Defined requirements for professor results views and CSV export.
8. A prioritized implementation plan with owners and deadlines for unresolved decisions.

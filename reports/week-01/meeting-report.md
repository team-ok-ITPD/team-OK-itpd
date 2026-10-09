# Kickoff Meeting Report

## 1. Meeting details

- **Date:** 02.10.2026
- **Meeting:** Week 1 kickoff with Customer
- **Location or call link:** 303 room
- **Recording:** No recording. Just the notes.
- **Evidence:** [`meeting-notes.md`](meeting-notes.md)

## 2. Attendance and roles

- **Attendees:** @adelazzi, @UTKANOS-RIBA, @Danashi11, @qwxiae, Customer. The whole team attended.
- **Interviewer:** @adelazzi and @UTKANOS-RIBA
- **Note-taker:** @qwxiae
- **Observer:** @Danashi11

## 3. Discussion summary

- **Learners and problem:** The product is for people who want hands-on debugging practice for a specific kind of problem. One example was a learner asking for a Go concurrency debugging exercise in plain language. We also need to provide bug categories with examples, which keeps the product focused on recognizable debugging problem types.
- **Task realism:** The product should work as a harness that prepares the dependencies, language tooling, a working environment, broken code, commands that reproduce the issue, and tests that verify whether the bug was fixed. This supports the direction of realistic debugging tasks rather than isolated puzzles.
- **Investigation tools and feedback:** VS Code integration is important because learners need access to debugging tools. There are two expected access paths: a website that provides VS Code, and the user's own VS Code connected to the environment. The agent should help inside VS Code, but the user should still perform the fix.
- **AI and learner agency:** The service will most likely provide API keys for the agent instead of asking users to bring their own. The notes leave open what the agent is allowed to do: give hints, show a fix, or only explain. This is a core unresolved product constraint because too much help could remove the debugging practice.
- **Scope, onboarding, and success:** The prototype starts with Python. Go concurrency was an example of the full idea, not the first implementation target. Surrounding features include scoring, a leaderboard, a gallery, attempt tracking, and problem categories, but they were not ranked for the first version.

## 4. Decisions

| Decision | Rationale | Trace |
|---|---|---|
| Start the prototype with Python. | Python is the first prototype language; Go and Java remain later possibilities. | GAP-01, VP-01 |
| Keep VS Code access central to the first product direction. | Access to debugging tools is important, and VS Code integration with remote SSH is the connection path to the prepared environment. | GAP-04, VP-03 |
| Treat the system as a prepared debugging harness, not only an exercise gallery. | Dependencies, language tooling, container or VM access, reproduction commands, and verification tests are part of the experience. | GAP-01, GAP-04, VP-01, VP-03 |
| Preserve learner agency while using an agent for help. | The agent is connected to VS Code, but the user performs the fix; exact agent permissions remain open. | GAP-02, GAP-03, VP-02 |

## 5. Action points

| Action | Owner | Due |
|---|---|---|
| Define the initial Python bug categories and wrМite at least one example for each category. | @adelazzi | Week 2: 2026-10-06 |
| Clarify the first-version priority of scoring, leaderboard, attempt tracking, gallery, and categories in follow-up. | @qwxiae | Week 2: 2026-10-07 |
| Specify the allowed agent behavior levels: explain only, hint, or reveal fix. | @UTKANOS-RIBA | Week 2: 2026-10-08 |
| Check the infrastructure assumption for one 16 GB VPS versus several configured servers, including concurrent users and per-user environments. | @Danashi11 | Week 2: 2026-10-08 |

## 6. Disagreements

| Topic | What changed or remains unresolved | Resolution |
|---|---|---|
| First prototype language | The project description and meeting example included Go, but the prototype should start with Python. | Resolved: prototype starts with Python; Go and Java are later possibilities. |
| First-version feature set | Scoring, leaderboard, gallery, attempt tracking, and categories were listed but not ranked. | Unresolved: clarify first-version priorities in Week 2. |
| Agent autonomy | The product needs an agent inside VS Code, but the notes do not define whether it may give hints, show fixes, or only explain. | Unresolved: define allowed assistance levels in Week 2. |
| IDE support | VS Code is required for debugging-tool access; support for other IDEs was not confirmed. | Unresolved: assume VS Code first until additional IDE support is requested. |

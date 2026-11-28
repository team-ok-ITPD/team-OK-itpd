# Separate Technical Rehearsal And AI Disclosure

## Human Sessions And Separate Technical Rehearsal

The team confirmed on 2026-11-28 that P-01, P-02 and P-03 were conducted
with real people. The separate agent-driven technical rehearsal below is
not one of those sessions. Its simulated questionnaire scores must not be
attributed to any participant or used in the human usability results.
AI assistance in preparing documentation does not mean AI conducted the
human sessions.

## 2026-11-27: Separate Agent-Driven Technical Rehearsal

OpenCode with GPT-6 Astra followed the user-provided participant worksheet
against a disposable local copy of Debug GYM v2 at commit
`53ee0487cec87b1229bf1c4f45853474d3ee16e6`.
It created demo data, used the browser to navigate the student practice flow,
edited the exercise and ran its tests, then restored the disposable exercise
for the second task and returned to its description for the third task.

The initial IDE launch required an explicit Docker Desktop socket setting.
The exercise tests changed from one failure and two passes to three passes;
the subsequent submission returned HTTP 403. The reset restored the expected
test failure. Browser back navigation was interrupted by a dialog, so the
exercise description was reopened at its previously visited address.

The requested standalone report was saved to the user's Downloads folder.
It explicitly labels the run and questionnaire scores as an AI simulation.
Setup included reading seed code containing solutions, so independent
discovery of the bug is not claimed. This is not a counted human usability
session, a quality-requirement verdict or Customer acceptance.

The product source was not changed. Follow-up recommendations in the report
require team review; no acceptance or implementation decision was made.

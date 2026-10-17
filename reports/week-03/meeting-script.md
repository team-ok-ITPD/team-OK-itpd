# Meeting script

## Context

Our problem-space sentence: a developer who wants to practise debugging needs
one place where a realistic, multi-file exercise is generated, run with real
debugging tools, and checked against the intended bug, and no product carries
all three in one flow.

We believe this is the gap our product targets, and that it is worth building.
We have not checked whether the customer needs real debugging (breakpoints,
several files) or whether failing tests and an output console are enough, and we
do not know whether the customer will accept a web page rather than VS Code.

Target: find out whether one flow that generates a debugging exercise, runs it,
and verifies the fix is the problem the customer wants solved, and in which
form.

## Agenda

1. Permission questions (2 min).  
   Show: nothing.
2. Our reading of the problem and our direction (5 min).  
   Show: [value-proposition.md](../../docs/research/value-proposition.md).
   Questions 1–2.
3. Who creates and solves exercises, and how it works today (10 min).  
   Show: nothing, so the answers describe their routine rather than our idea.
   Questions 3–6.
4. What went wrong and what cannot change (6 min). Show: nothing. Questions 7–8.
5. Scope (5 min).  
   Show: [gap-analysis.md](../../docs/research/gap-analysis.md). Questions 9–10.
6. Read back the decisions and action points (2 min).  
   Show: the note taker's list.

## Questions

### Business goals

1. _(open)_ Why practise debugging with generated exercises rather than
   hand-written ones or real codebases?
2. _(open)_ When this works, what changes for the people who practise, and for
   you?

### End users

3. _(open)_ Who creates an exercise, who solves it, and who decides whether it
   is good?
4. _(closed)_ Are the person who creates an exercise and the person who solves
   it the same?

### Current workflow

5. _(open)_ Walk me through the last debugging exercise you wrote or solved,
   step by step. What happened at each step?
6. _(open)_ Where do the code, the tests, and the debugger live today when you
   practise?

### Pain points and constraints

7. _(open)_ What was the most annoying part of the last exercise that went
   wrong? For example, a bug that was not the one intended, or tests that passed
   or failed for the wrong reason.
8. _(closed)_ Can you run participants' code on your own servers today?

### Scope

9. _(open)_ If only one of generating the exercise, running the tests, or
   debugging with breakpoints could ship, which one survives?
10. _(closed)_ Is working in VS Code acceptable, or does it have to be a web
    page?

## Roles

`@adelazzi` asks, `@Danashi11` takes notes, `@UTKANOS-RIBA` observes and records
what we did not ask.

## Key improvements

### "Would you like a console under the editor?" -> "When the last test failed, what did you look at to find out why?"

We were offering a solution. The rewrite asks for the past, so the answer
describes what the customer really looks at (one row of output, or a thousand
values) instead of a preference for our idea.

### "Is pasting the solution from VS Code a good idea?" -> "Last time you fixed a bug in a project with several files, where did you edit the code and how did you check it?"

The original asks the customer to judge a design we already chose. The rewrite
anchors it to an event the customer will remember, so the answer shows whether
multi-file work and a VS Code workflow are real needs or a guess.

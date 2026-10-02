# Kickoff meeting script

## Context

Our problem-space sentence: a software developer or programming language learner who wants to get better at debugging one particular kind of problem has almost no hands-on exercises for it, so they practice on generic puzzles or wait for a real bug to teach them.

We believe an LLM can generate realistic, solvable debugging exercises for a chosen kind of problem, and that users will want to debug them in their own VS Code.

We have not checked how good generated exercises are, or whether the customer cares more about generation, the VS Code connection, or the public gallery.

This meeting tests both.

## Questions


**Business goals**

1. _(open)_  What made you decide to build this rather than point people to the debugging exercises that already exist?
2. _(open)_ When this works, what is different about how people learn to debug?

**End users**

3. _(open)_ Think of the last person you saw learn to debug a new kind of problem. Who were they, and what were they trying to learn?
4. _(closed)_ Is the person who asks for an exercise the same person who solves it?

**Current workflow**

5. _(open)_  What did you do the last time an exercise you were given turned out to be broken, too easy, or impossible to solve?
6. _(open)_ Walk me through the last time you practiced, or taught, debugging a specific kind of problem.
   What happened at each step?

**Pain points and constraints**

7. _(open)_ What was the most annoying part of the last time you tried to practice debugging?
8. _(closed)_ Does a user have to be able to start an exercise with nothing installed beyond VS Code?

**Scope**

9. _(open)_  If we could only ship one of these, which one would you keep: generating exercises, connecting from VS Code, or the public gallery?
10. _(open)_ What is clearly out of scope for you?

## Roles

@interviewer-username asks, @notetaker-username takes notes, @observer-username observes and records what we did not ask and what was not said.

## Key improvements

**"Would you use a site that generates debugging exercises?" -> "Walk me through the last time you practiced, or taught, debugging a specific kind of problem." (Question 5)**

The original asks for an opinion about our idea, and almost anyone says yes.
The rewrite asks about a past event, so the answer is a real routine and shows whether the pain exists.

**"Is the quality of generated exercises important to you?" -> "What did you do the last time an exercise you were given turned out to be broken, too easy, or impossible to solve?" (Question 6)**

Everyone says quality is important, so the original tells us nothing.
The rewrite anchors it to a specific past failure, so the answer shows what a bad exercise costs and what the customer did about it.

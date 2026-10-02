# Meeting notes

**Meeting:** Week 1 kickoff with the customer

**Date:** 02.10.2026

**Attendees:** @adelazzi, @UTKANOS-RIBA, @Danashi11, @qwxiae, customer

## Notes

The customer began by describing the system as a harness that prepares everything a debugging exercise needs: the dependencies, the language compiler for the exercise (Go was the example), a container for the user to work in, and a connection to VS Code.

The customer then walked through how a user would start.
A user logs in, receives notifications, and creates an account.
The user asks for an exercise in plain language, and the customer gave the example of a user saying they want to practice debugging concurrency in Go.
The system sets up the whole environment and gives the user a link to click, which connects their VS Code to it.
The user does not have to find or install the Go tooling themselves.

The customer described what happens behind that link.
A virtual machine is created and linked to the user, and the user gets access to the broken code.
The terminal runs inside the virtual machine, so the user can run commands there and try to fix the code.
The system also provides commands that reproduce the problem.
An agent is connected to VS Code and helps the user while they debug, and the user does the fix themselves.
When the user finishes, the harness tests the code with the bug and decides whether the problem is fixed.
The customer said the harness should show that the problem is reproducible.

The customer said the user can reach the environment in two ways: through a website that provides VS Code, or through VS Code on their own machine.
Access to debugging tools is important to the customer, and this is the reason for the VS Code integration.
The customer was not sure whether other IDEs would also be acceptable.

On the infrastructure side, the customer said the service has a configured setup for each language, running on several servers and that the service will most likely provide the API keys for the agent, so users do not bring their own.
The customer named remote SSH as the way VS Code connects to the environment and mentioned a VPS with 16 GB.
An attempt is stored for about a week.

The customer then described the surrounding features: scoring, a leaderboard, a gallery of problems, tracking of a user's attempts, and categories of problems.
The system should support a set of programming languages, with Python, Go and Java named.

The customer asked the team to start with Python for the prototype.
The Go concurrency case was an example of the full idea and not the first target.

Finally, the customer asked for bug categories with examples.

## Decided

- The prototype starts with Python.

## Left open

- Which of scoring, the leaderboard, attempt tracking and the gallery belong in the first version. The customer listed them but did not rank them.
- When Go and Java are added after Python.
- What the agent is allowed to do while helping, for example whether it can give hints, show a fix, or only explain.
- Whether the infrastructure is one 16 GB VPS or several configured servers, and whether it is enough for several users at once, each with their own virtual machine or container.
- Whether IDEs other than VS Code need to be supported.
- Who pays for the agent's API usage if the service provides the keys, and whether there is a limit per user.
- What "about a week" of storage means for attempts: whether it applies to solutions, progress and leaderboard entries, and what happens after.
- Which bug categories to start with, and who writes the examples.

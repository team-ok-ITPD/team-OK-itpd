# Internal Project Planning Script

## Context

This week’s meeting was internal. The team focused on dividing the project into workstreams, defining the prototype architecture, and finalizing the user experience direction. The team discussed the client’s acceptance of the ChatGPT-style workflow, where users describe what they want to practice and proceed directly to a prepared debugging environment.

The **Figma design has been completed**, providing the visual direction for the prototype: [View the Figma design](https://www.figma.com/design/29kS3KyEPkdidEwrBsmNwO/ITPD?node-id=1-2&t=3J8dqgqCYNouOkZA-1).

The first prototype will focus on **Python and browser-based coding and debugging**. VS Code integration through SSH may be considered in a later phase. The immediate objective is to validate a complete, simple workflow before expanding the feature set.

## Questions

**Project Split**

1. Which project components can be developed independently?
2. Which tasks depend on one another, and which can proceed in parallel?

**Architecture and Examples**

3. Which existing platforms provide useful examples for our debugging environment?
4. Which architecture best supports the initial prototype and future extensions?

**UX and Figma Design**

5. How can the completed Figma design support a simple prompt-to-practice workflow?
6. What is the minimum information users need to provide before starting?
7. How can we minimize clicks and unnecessary screens?

**Prototype Scope**

8. What is the minimum end-to-end workflow required for the Python debugging prototype?
9. How can users inspect code, investigate bugs, and test fixes directly in the browser?
10. What should be validated before considering VS Code integration through SSH?

**Client Validation**

11. Does the proposed architecture meet the client's expectations?
12. Which decisions require confirmation before implementation proceeds?

## Roles

- **@adelazzi:** Leads discussion on UX, the user journey, and architecture.
- **@UTKANOS-RIBA:** Presents reference examples and relevant platform patterns.
- **@Danashi11:** Focuses on task decomposition and prototype scope.
- **@qwxiae:** Documents decisions and tracks open questions.

## Key Improvements

- **Project architecture:** Focus on separating workstreams and defining a modular architecture.
- **User experience:** Use the completed Figma design to guide a minimal prompt-to-practice workflow.
- **Prototype scope:** Start with Python and browser-based debugging before introducing additional languages or VS Code integration.
- **Validation:** Prioritize testing the core workflow and confirming the architecture with the client before expanding the project.
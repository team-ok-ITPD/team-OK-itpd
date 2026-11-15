# Debug Gym Style Guide

[Shared] One look for every page. Every team member, and every LLM they use,
follows this guide. If you use an AI assistant, paste this file into the chat
or point the tool at it before asking for any page or style.

## Where the Styles Live

| File | What it holds | Who edits it |
|---|---|---|
| `static/css/tokens.css` | Every colour, text size, spacing, radius and shadow as a CSS variable | Agree in the team first |
| `static/css/main.css` | Base styles and shared components (buttons, badges, cards, forms, tables, alerts, code) | Add new shared pieces; never change a token value here |
| `static/style-preview.html` | A page showing every component | Update when you add a component |

`main.css` imports `tokens.css`, so a page only links `main.css`.

## The Rules

1. **Never write a raw colour.** No `#hex`, `rgb()` or colour names outside
   `tokens.css`. Use `var(--color-...)`.
2. **Never write a raw font size.** Use `var(--text-...)`.
3. **Use the spacing scale** for margins, padding and gaps: `var(--space-1)`
   to `var(--space-10)`.
4. **Use the shared classes first** (`.button`, `.badge`, `.card`, `.field`,
   `.table`, `.alert`, ...). Write new CSS only when no shared class fits.
5. **No inline `style="..."`** and no CSS frameworks (no Bootstrap, no Tailwind).
6. **Page-only CSS** goes at the end of `main.css` under a comment
   `/* Page: <app>/<template> */`, and still uses tokens only.
7. **Need a new colour or size?** Add a token to `tokens.css` and mention it in
   your pull request. Do not invent near-duplicates.
8. Keep the dark theme: text on `--color-bg` or `--color-surface`, the indigo
   accent for actions, status colours only for status.

## Tokens

### Colours

| Token | Value | Use for |
|---|---|---|
| `--color-bg` | `#0b0f17` | Page background, inputs |
| `--color-surface` | `#111827` | Cards, panels, navbar |
| `--color-surface-2` | `#1f2937` | Hover rows, secondary buttons, badges |
| `--color-surface-3` | `#273244` | Avatars, deepest raised layer |
| `--color-border` | `#374151` | Inputs, buttons, dashed empty states |
| `--color-border-soft` | `#263041` | Card borders, table lines |
| `--color-text` | `#f9fafb` | Main text |
| `--color-text-muted` | `#9ca3af` | Secondary text |
| `--color-text-subtle` | `#6b7280` | Hints, timestamps, table headers |
| `--color-accent` | `#6366f1` | Primary actions, focus ring, eyebrows |
| `--color-accent-strong` | `#4f46e5` | Primary button hover |
| `--color-accent-2` | `#8b5cf6` | Second colour of the brand gradient |
| `--color-accent-soft` / `-border` / `-text` | indigo tints | Highlighted badges and info alerts |
| `--color-link` | `#a5b4fc` | Links |
| `--gradient-brand` | indigo → violet | Logo and the one main call to action |
| `--color-success`, `-soft`, `-border`, `-text` | green | Solved, graded, saved |
| `--color-danger`, `-soft`, `-border`, `-text` | red | Errors, failed, overdue, delete |
| `--color-warning`, `-soft`, `-border`, `-text` | amber | Pending, in progress, due soon |
| `--code-keyword` … `--code-comment` | | Python syntax colours in code blocks |

On dark backgrounds, use the `-text` variant for coloured text and the `-soft`
variant for backgrounds.

Difficulty (LeetCode-style): `--color-easy` (green), `--color-medium` (amber),
`--color-hard` (red). Use the classes `.difficulty-easy`, `.difficulty-medium`
and `.difficulty-hard` on text or badges.

Atmosphere (hero and sign-in pages only): `--glow-accent` and `--glow-accent-2`
(soft background glows), `--color-grid-line` with `--grid-size` (faint grid),
`--color-surface-glass` (see-through card with blur), `--gradient-text` (use the
`.text-gradient` class on one or two words of a headline).

### Text Sizes

The root size is 15px (`--font-size-root`). Body text is `--text-md`.

| Token | Size | Use for |
|---|---|---|
| `--text-2xs` | 0.7rem | Small badges |
| `--text-xs` | 0.78rem | Badges, eyebrows, table headers, field hints and errors |
| `--text-sm` | 0.85rem | Secondary text, form labels, small buttons, tables |
| `--text-md` | 1rem | Body text, inputs |
| `--text-lg` | 1.1rem | Card and section titles (`h2`) |
| `--text-xl` | 1.5rem | Stat numbers on dashboards |
| `--text-2xl` | 1.6–2.1rem | Page title (`h1`), one per page |
| `--text-display` | 2.2–3.4rem | Hero headline on login and landing pages only |

Weights: `--weight-regular` (400), `--weight-semibold` (600, labels and
buttons), `--weight-bold` (700, eyebrows and stats), `--weight-black` (800, hero
headline only). Fonts: `--font-sans`
(Inter) for text, `--font-mono` (JetBrains Mono) for code.

### Spacing, Shape and Layout

- Spacing: `--space-1` 0.25rem, `--space-2` 0.5rem, `--space-3` 0.75rem,
  `--space-4` 1rem, `--space-5` 1.25rem, `--space-6` 1.5rem, `--space-8` 2rem,
  `--space-10` 2.5rem.
- Radius: `--radius-sm` (0.5rem) for buttons, inputs and alerts; `--radius`
  (0.75rem) for cards; `--radius-pill` for badges.
- Shadows: `--shadow-accent` only under the brand button; `--shadow-overlay`
  for menus and dialogs.
- Layout: `--content-max` (76rem) page width, `--content-narrow` (42rem) for
  reading text, `--sidebar-width` (17rem), `--control-height` (2.5rem) for
  buttons and inputs.

## Components

Copy these snippets. See them rendered at `/static/style-preview.html`.

### Page Header

```html
<header class="page-header">
  <div>
    <p class="eyebrow">Professor / Assignments</p>
    <h1>My assignments</h1>
  </div>
  <a class="button primary" href="...">New assignment</a>
</header>
<p class="lede">One sentence that explains the page.</p>
```

### Buttons

```html
<button class="button primary">Save</button>          <!-- main action, one per area -->
<button class="button secondary">Run tests</button>   <!-- other actions -->
<a class="button ghost" href="...">Cancel</a>          <!-- low emphasis -->
<button class="button danger">Delete</button>          <!-- destructive -->
<a class="button brand" href="...">Start practice</a>  <!-- one hero action per page -->
<button class="button primary small">Assign</button>  <!-- inside tables and cards -->
```

### Badges

```html
<span class="badge">Easy</span>
<span class="badge success">Graded</span>
<span class="badge warning">Submitted</span>
<span class="badge danger">Overdue</span>
<span class="badge accent">Public</span>
<span class="badge small">Python</span>
```

Status mapping for the whole site: todo → plain badge, submitted → `warning`,
graded or solved → `success`, overdue or failed → `danger`, public/private →
`accent` / plain.

### Cards, Stats and Empty States

```html
<section class="card">
  <h2 class="card-title">Recent grades</h2>
  <p class="text-muted">...</p>
</section>

<div class="grid-cards">
  <div class="card stat"><span class="stat-value">24</span><span class="stat-label">Students</span></div>
</div>

<div class="empty"><strong>No assignments yet.</strong><span>Create one from a bug.</span></div>
```

### Forms

```html
<form class="form" method="post">
  <label class="field">
    Email
    <input type="email" name="email" required>
    <small class="field-hint">Use your university email.</small>
    <small class="field-error">Enter a valid email address.</small>
  </label>
  <button class="button primary" type="submit">Log in</button>
</form>
```

Mark an invalid input with `aria-invalid="true"` or the wrapper with `.has-error`.

### Alerts and Messages

```html
<p class="alert success">Assignment created.</p>
<p class="alert error">The deadline has passed.</p>
<p class="alert warning">Due tomorrow.</p>
<p class="alert info">Practice bugs are not graded.</p>
```

Map Django message tags to these classes: `success`, `error`, `warning`,
`info`.

### Tables

```html
<table class="table">
  <thead><tr><th>Student</th><th>Status</th><th>Grade</th></tr></thead>
  <tbody><tr><td>Ali</td><td><span class="badge success">Graded</span></td><td>9.5</td></tr></tbody>
</table>
```

### Sign-in Pages (Login, Register, Password Reset)

Reuse the login page layout from `accounts/templates/accounts/login.html`: put
`auth-page` on `<body>` (grid + glow background), wrap the page in
`.auth-shell`, the story side in `.auth-story` and the form in `.auth-card`.
Keep one `.button.brand` as the submit button.

```html
{% extends "base.html" %}
{% block body_class %}auth-page{% endblock %}
{% block body %}
<div class="auth-shell">
  <section class="auth-story">...</section>
  <section class="auth-card">
    <p class="eyebrow">Join Debug Gym</p>
    <h2>Create your account</h2>
    <form class="form" method="post">...<button class="button brand">Create account</button></form>
  </section>
</div>
{% endblock %}
```

### Code

```html
<pre class="code"><span class="tok-keyword">def</span> <span class="tok-function">count</span>(items):
    <span class="tok-keyword">return</span> <span class="tok-builtin">len</span>(items)  <span class="tok-comment"># comment</span></pre>
```

## Prompt for AI Assistants

Paste this before asking an LLM for a Debug Gym page:

> Use the Debug Gym style guide (docs/style-guide.md). Link only
> `static/css/main.css`. Use its classes (`page-header`, `eyebrow`, `button
> primary/secondary/ghost/danger/brand`, `badge`, `card`, `field`, `table`,
> `alert`, `code`). Do not add colours, font sizes or inline styles; use the CSS
> variables from tokens.css if new CSS is unavoidable. No CSS frameworks.

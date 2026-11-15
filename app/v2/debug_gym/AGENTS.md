# Debug Gym v2: Instructions for AI Assistants

[Shared] Read this before changing anything in `app/v2/debug_gym/`.

## Styling

Follow [docs/style-guide.md](docs/style-guide.md) for every page and style.

- Link only `static/css/main.css` (it imports `static/css/tokens.css`).
- Use the shared classes: `page-header`, `eyebrow`, `lede`, `button` with
  `primary`, `secondary`, `ghost`, `danger` or `brand`, `badge`, `card`,
  `stat`, `empty`, `field`, `table`, `alert`, `code`.
- Never write raw colours (`#hex`, `rgb()`) or font sizes outside
  `tokens.css`; use `var(--color-...)`, `var(--text-...)`, `var(--space-...)`.
- No inline `style` attributes and no CSS frameworks.
- Page-only CSS goes at the end of `main.css` under `/* Page: <app>/<template> */`.

## Project Conventions

- Keep the one-line owner header at the top of each file, such as
  `<!-- [Student Dev] ... -->` or `# [Professor Dev] ...`.
- Templates extend `templates/base.html`.
- Shared models live in `core/models.py`; follow the team database schema.

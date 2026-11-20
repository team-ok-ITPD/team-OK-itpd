# [Shared] Debug Gym v2 setup and run

Debug Gym v2 is a Django application with three roles: admin, professor and
student. It runs on your own computer with SQLite and needs no Docker. The
older prepared-exercise catalog described in the repository's
[`docs/setup.md`](../../../../docs/setup.md) is a separate application under
`app/`.

## Prerequisites

- Git.
- Python 3.10 or newer (Django 5.2 requires it). Check `python --version`; on
  Windows `py --version` also works, and on macOS or Linux use `python3`.
- A modern browser, free host port 8000, and an internet connection for the
  first dependency install.

Nothing else is installed globally. The launcher keeps Django in a `.venv`
folder next to `run.py`, which Git ignores.

This is a local development setup: `DEBUG` is on and the secret key is a
placeholder. Keep it on your own machine and never use these settings in
production.

## Install and run

Clone a fresh copy and enter the project folder:

```sh
git clone https://github.com/team-ok-ITPD/team-OK-itpd.git
cd team-OK-itpd/app/v2/debug_gym
```

Then run the launcher. It works the same way on every system.

On Windows, in PowerShell or Command Prompt:

```powershell
py run.py --demo
```

On macOS or Linux:

```sh
python3 run.py --demo
```

The launcher creates `.venv`, installs `requirements.txt` (again only when that
file changes), applies the database migrations, creates the demo data, starts
the server and opens `http://127.0.0.1:8000/`. Press `Ctrl+C` in the terminal to
stop it.

| Option | Meaning |
| --- | --- |
| `--demo` | Create the demo accounts and sample data below. Safe to repeat. Refused unless `DJANGO_DEBUG=1`. |
| `--port 8001` | Use another port when 8000 is busy. |
| `--no-browser` | Do not open the browser. |
| `--test` | Run the Django test suite instead of the server. |

Without `--demo` the launcher starts with an empty database and tells you if no
account exists yet.

## Demo accounts

`--demo` creates these accounts, all with the password `debug-gym-pass`:

| Email | Role |
| --- | --- |
| `admin@example.com` | Admin |
| `prof@example.com` | Professor |
| `ali@example.com` | Student |
| `omar@example.com` | Student |

It also creates the group **Demo Group** (taught by the professor, with both
students), one private bug assigned to that group with a deadline a week away,
and one public bug for practice. These passwords are for local development only.

To use your own admin account instead, activate the environment and run
`createsuperuser`:

```sh
# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS or Linux
source .venv/bin/activate

python manage.py createsuperuser
```

If activation is unavailable, call the environment's Python directly, for
example `.venv\Scripts\python.exe manage.py createsuperuser`.

## Configuration

The settings read these environment variables. The defaults suit a local run.

| Variable | Default | Meaning |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | `dev-only-insecure-key-change-me` | Signing key. Set a real one for anything but local use. |
| `DJANGO_DEBUG` | `1` | Debug mode. `--demo` refuses to run when this is not `1`. |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | Comma-separated host names the server answers to. |

The database is `db.sqlite3` in the project folder. Git ignores it.

## What to try

Sign in at `http://127.0.0.1:8000/`. Each role lands on its own dashboard.

1. **Student** (`ali@example.com`): the dashboard lists your groups, pending
    assignments and recent grades. Open **Assignments**, choose the demo
    assignment and select **Solve this bug**. Change the code, because the
    original buggy code is rejected, and submit. The assignment now shows
    **Submitted**, and you can resubmit until the deadline. **Practice** lists
    public bugs; practice attempts are saved but never graded. **Results** shows
    your graded work and history.
2. **Admin** (`admin@example.com`): open `/admin-panel/` to create teacher,
    student and administrator accounts. Teachers can also be edited or
    deactivated. Use **Groups** to create a group, select its active teacher,
    change its teacher, and add or remove students. Each group has one teacher.
    Changing the group's teacher does not transfer existing assignments or
    exercises. Assignment pages are read-only in the administrator panel.
3. **Professor** (`prof@example.com`): `/professor/` currently shows only a
    placeholder dashboard. Groups, assignments and grading pages are not
    implemented yet.
4. **Django admin** (`/django-admin/`, admin account only): create bugs,
    assignments, groups and submissions, and set a grade and feedback on a
    submission, which students then see. This is a development tool, not the
    product's professor workflow.

## Stop and reset

Stop the server with `Ctrl+C`. Your data stays in `db.sqlite3`.

To start again from an empty database, stop the server, delete `db.sqlite3` and
run the launcher again. This removes every local account and submission, so
copy out anything you need first.

To rebuild the environment, delete the `.venv` folder and run the launcher again.

## Checks

From the project folder:

```sh
python run.py --test
```

Or, inside the activated environment, run everything or one app:

```sh
python manage.py test
python manage.py test student
```

After you change a model, create and apply its migration, and confirm nothing
is left over:

```sh
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations --check --dry-run
```

Before opening a pull request, follow the repository's
[CONTRIBUTING.md](../../../../CONTRIBUTING.md) and the style rules in
[style-guide.md](style-guide.md).

## Troubleshooting

| Symptom | Action |
| --- | --- |
| `python` is not found on Windows | Use `py run.py`, or install Python from python.org and tick **Add python.exe to PATH**. |
| Python is too old | Install Python 3.10 or newer; the launcher stops with the version it found. |
| pip cannot install the dependencies | Check your network and run the launcher again. It retries because the install is only recorded after it succeeds. |
| Port 8000 is already in use | Stop the other program or run with `--port 8001`. |
| The browser does not open | Open `http://127.0.0.1:8000/` yourself, or run with `--no-browser` on a machine without a browser. |
| `403 Forbidden` on `/admin-panel/` or `/professor/` for an admin or professor | Your branch lacks the `RoleRequiredMixin` fix: the mixin must honour each view's `required_role`. Student pages are not affected. |
| `no such table` or a migration error | Run `python manage.py migrate` in the activated environment. If the database is only demo data, delete `db.sqlite3` and rerun the launcher. |
| Sign-in fails for a demo account | Run `python run.py --demo` again. It creates missing accounts but never changes an existing password. |
| `--demo` refuses to run | `DJANGO_DEBUG` is set to something other than `1` in your shell. Unset it for local use. |
| Broken environment after a Python upgrade | Delete `.venv` and run the launcher again. |

## Verification record

No platform run is recorded yet. When a member runs `run.py --demo` on a clean
checkout, add the date, operating system, Python version and what they
confirmed here. Do not record a check that was not performed.

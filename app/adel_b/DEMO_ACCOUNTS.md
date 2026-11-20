# Debug GYM Demo Accounts

Created 2026-11-06 16:11 by `manage.py seed_demo`. Running the
command again deletes these accounts and their data and creates new passwords.

Keep this file private. It is listed in `.gitignore` and must not be committed.

- Website: http://localhost:8001
- Django admin: http://localhost:8001/admin/
- Log in with the username or the email.

## Accounts

| Role | Username | Email | Password | What it shows |
|---|---|---|---|---|
| Admin | `demo_admin` | `demo_admin@debuggym.demo` | `quartz-velvet-40` | Django admin: change any user's role (student or professor). |
| Professor | `prof_lina` | `prof_lina@debuggym.demo` | `canyon-meadow-68` | Teaching pages: her 2 exercises, assignments and student progress. |
| Student | `student_ali` | `student_ali@debuggym.demo` | `orbit-velvet-28` | A student who solved both assignments and has a streak. |
| Student | `student_maria` | `student_maria@debuggym.demo` | `falcon-canyon-35` | A student in the middle: one in progress, one submitted but not solved (overdue). |
| Student | `student_omar` | `student_omar@debuggym.demo` | `meadow-quartz-96` | A student who has not started: two open assignments, one overdue. |

## Demo Data

Prof. Lina wrote 2 exercises and assigned both to all 3 students:

| Exercise | Due | Ali | Maria | Omar |
|---|---|---|---|---|
| The forgotten zero | in 7 days | Solved (2 submissions) | In progress | Not started |
| The shrinking word | 2 days ago (overdue) | Solved | Not solved (1 / 3) | Not started, overdue |

## Suggested Tour

1. Log in as `prof_lina`: the **Teaching** page lists both exercises with assigned and solved counts.
2. Open **Assign & results** on "The shrinking word" to see each student's status, best score and the overdue mark.
3. Open **Edit** and press **Check with Python** to show that the tests catch the bug.
4. Log in as `student_omar`: **My assignments** shows two open exercises, one overdue.
5. Open one, press **Run Tests**, fix the code, then **Submit**; back as `prof_lina`, the result appears.
6. Log in as `demo_admin` at the Django admin to show how a student is made a professor.

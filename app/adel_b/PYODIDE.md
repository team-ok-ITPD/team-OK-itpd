# Browser Python (Pyodide): When We Need A Container

The `adel_b` site runs learner code in the browser with
[Pyodide 0.26.4](https://pyodide.org/en/0.26.4/) (Python 3.12 compiled to
WebAssembly). This note says which challenges can stay in the browser and which
would need a container. It reflects the Pyodide 0.26.4 documentation, checked
on 2026-10-26; check the links again before relying on it for a new version.

## Works In The Browser (No Container)

- **Plain Python and most of the standard library:** `csv`, `json`, `re`,
  `collections`, `itertools`, `datetime`, `dataclasses`, `math`, `random`,
  `pathlib`, `io` and similar.
- **Several files in one challenge:** Pyodide has an in-memory file system, so a
  challenge can ship `main.py`, helper modules and data files such as
  `data.csv`, then import and read them normally. Each run can start from a
  fresh copy.
- **Packages built into Pyodide** (loaded on demand, larger first download):

  | Area | Packages |
  |---|---|
  | Data | `numpy`, `pandas`, `scipy`, `statsmodels`, `xarray`, `duckdb`, `fastparquet`, `xlrd` |
  | Machine learning | `scikit-learn`, `xgboost`, `lightgbm` |
  | Charts and images | `matplotlib`, `bokeh`, `altair`, `Pillow`, `opencv-python`, `scikit-image` |
  | Text and web data | `beautifulsoup4`, `lxml`, `html5lib`, `regex`, `nltk`, `pyyaml` |
  | Maths and graphs | `sympy`, `networkx`, `mpmath`, `igraph` |
  | Models and tools | `pydantic`, `sqlalchemy`, `peewee`, `rich`, `pytest` |

  Full list: [packages in Pyodide 0.26.4](https://pyodide.org/en/0.26.4/usage/packages-in-pyodide.html).
- **Pure-Python packages from PyPI** through `micropip`, when they have no
  compiled parts and do not need the features listed below.
- **Needs an extra load step:** `sqlite3`, `ssl` and `lzma` are not loaded by
  default. Our worker would have to load them before a challenge can use them.

## Does Not Work In The Browser (Needs A Container)

| Need | Why the browser cannot do it |
|---|---|
| Threads, processes, `multiprocessing` | They import but do not work in Pyodide. |
| Running other programs (`subprocess`, shell, `git`) | There is no operating system to start them. |
| Raw sockets or running a server | Sockets do not work; code cannot listen on a port. |
| Real database servers (PostgreSQL, MySQL, Redis) | Needs sockets and a separate server; `psycopg2` is not available. |
| Missing compiled packages | For example `torch`, `tensorflow`, `polars`, `pyarrow`, `openpyxl` (see the full list). |
| Terminal and GUI modules | `tkinter`, `curses`, `termios`, `pty`, `tty` and `turtle` are removed or cannot be imported. |
| Unix system modules | `fcntl`, `pwd`, `grp`, `resource`, `syslog` and `dbm` are removed. |
| Very large data | Every file must be downloaded and held in browser memory. |
| A real step-through debugger | The browser gives run, print and pass/fail, not VS Code breakpoints. |
| Grading the server can trust | The browser reports its own results, which a learner could fake. |

## Works With Limits

- **HTTP with `requests` or `urllib3`:** requests go through the browser, so
  the target site must allow it (CORS), and certificates and timeouts are not
  under our control. Treat challenges that call real web APIs as container
  cases.
- **`hashlib`:** algorithms that need OpenSSL need an extra load step.
- **`zoneinfo`:** needs the `tzdata` package.
- **First run:** Pyodide downloads about 10 MB, plus each package used, and
  needs internet unless we host the files ourselves.

## Quick Rule

Use the browser when the challenge is Python code plus data files, using the
standard library or the packages above. Use a container when it needs another
program, a network service, threads or processes, a missing package, large
data, a real debugger, or grading the learner cannot fake.

Sources: [Pyodide packages](https://pyodide.org/en/0.26.4/usage/packages-in-pyodide.html)
and [Pyodide Python constraints](https://pyodide.org/en/0.26.4/usage/wasm-constraints.html).

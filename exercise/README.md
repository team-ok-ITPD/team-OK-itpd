# The surviving negative

A filter should remove every negative number from a list, but some negative
values survive. The function runs without raising an exception.

## Reproduce

Run this command in the VS Code terminal:

```bash
python -m pytest -q
```

The unchanged exercise reports named failing tests. Running it again produces
the same failures.

## Investigate

Open the Run and Debug view and select **Debug reproduction tests**. Set a
breakpoint in `remove_negatives.py`, start the debugger, and inspect how the
list and loop position change.

## Verify

Edit `remove_negatives.py`, then run `python -m pytest -q` again. The exercise
is complete when all tests pass.

## Reset

From the repository root, run:

```bash
docker compose down --volumes
docker compose up --build
```

Removing the Compose volume restores the original exercise, but permanently
deletes any changes saved in the workspace.

# Week 6 - AI Code Review and Testing

## Guardrails

I ran these commands from the Week 6 starter directory:

| Command | What it checks |
| --- | --- |
| `python -m black --check main.py test_main.py` | Fails if either file needs formatting. |
| `python -m ruff check main.py test_main.py` | Checks for lint issues such as unused imports and undefined names. |
| `python -m pytest -q` | Runs the tests and returns a nonzero exit code if a test fails. |

### Failure demonstration

I created a temporary test outside the repository with `assert 1 == 2`.
Running it alongside the starter tests produced `1 failed, 3 passed, 1 warning`
and exit code `1`. Running only the starter tests produced
`3 passed, 1 warning` and exit code `0`.

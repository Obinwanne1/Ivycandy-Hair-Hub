# Testing

Reference material for planning test work on `C:\Users\rigwe\Desktop\TicToc\BuildWeb`.

---

## Current State: No Tests

There are no tests in this codebase. No test files, no test directories, no test framework configuration, and no CI/CD pipeline exist.

---

## Confirmed Absence

The following were checked and are not present:

- No `tests/` or `test/` directory
- No files matching `test_*.py` or `*_test.py`
- No `pytest.ini`, `setup.cfg`, `pyproject.toml`, or `tox.ini`
- No `conftest.py`
- No `.github/workflows/` directory (no GitHub Actions)
- No `Makefile` with test targets
- `requirements.txt` contains only three runtime dependencies: `streamlit`, `anthropic`, `python-dotenv` — no test framework listed

---

## Test Framework Recommendations (for future planning)

Given the project's structure, the most practical test targets and approaches would be:

### Unit-testable surface

`db.py` is the most isolated and testable module. It has no Streamlit dependency and exposes pure Python functions that take and return simple values. All functions use a hardcoded `DB_PATH` derived from `__file__`, which would need to be patched or parameterised for testing.

`ai_reply.py` contains two functions (`generate_reply`, `generate_sales_script`) that call the Anthropic API. These would require mocking `anthropic.Anthropic` to test without live API calls.

`app.py` is a single-file Streamlit application with no unit-testable logic extracted — it mixes UI rendering, data fetching, and business logic inline. Testing it would require either Streamlit's `AppTest` utility (introduced in Streamlit 1.28) or end-to-end browser automation.

### Suggested setup if tests are added

- **Framework:** `pytest` (standard choice; compatible with all targets here)
- **DB tests:** Use `tmp_path` fixture to create a temporary SQLite file; patch `db.DB_PATH` at test time
- **AI tests:** Mock `anthropic.Anthropic` with `unittest.mock.patch` or `pytest-mock`
- **Streamlit UI tests:** `streamlit.testing.v1.AppTest` for smoke-testing page rendering without a browser
- **Coverage:** `pytest-cov` with `--cov=.` for line coverage reporting

### Example structure if introduced

```
tests/
    conftest.py          # shared fixtures (tmp db path, mock anthropic client)
    test_db.py           # unit tests for all db.py CRUD functions
    test_ai_reply.py     # tests for generate_reply / generate_sales_script (mocked API)
    test_app.py          # Streamlit AppTest smoke tests for each page
```

---

## CI/CD

No CI/CD configuration exists. The project deploys manually to Streamlit Cloud by connecting the GitHub repo at `share.streamlit.io`. There are no pre-commit hooks, no branch protection rules, and no automated test gates in the current workflow.

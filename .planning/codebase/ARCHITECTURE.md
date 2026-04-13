# Architecture — Ivycandy Hair Hub

## Architectural Pattern

**Single-file monolith with a two-module backend.**

The app is a Streamlit single-page application. All UI logic lives in one file (`app.py`). Backend concerns are split into two purpose-built modules (`db.py`, `ai_reply.py`) that `app.py` imports directly. There is no HTTP routing layer, no controller abstraction, and no service class hierarchy — Streamlit's page-selection idiom (`st.sidebar.radio` + `if page == ...` branches) acts as the router.

---

## Layers and Their Responsibilities

### 1. Presentation Layer — `app.py`
- Owns all Streamlit widget calls, layout, CSS injection, and HTML markdown.
- Implements page routing via a `st.sidebar.radio` value matched against named string constants (`NAV_PAGES`).
- Calls `db.*` functions directly for data reads/writes; calls `ai_reply.*` functions for AI generation.
- Manages ephemeral UI state through `st.session_state` (e.g., `"last_reply"`, `"last_script"`, `"dash_reply"`).
- Contains inline CSS (~330 lines) injected via `st.markdown(..., unsafe_allow_html=True)` to theme the app with the Ivycandy brand.

### 2. Data Access Layer — `db.py`
- Owns all SQLite interactions. Provides a thin function-per-operation API (no ORM).
- `DB_PATH` is resolved relative to the module's own directory (`data/business.db`).
- `get_conn()` is a factory that returns a `sqlite3.Row`-aware connection.
- `init_db()` is called once on startup (from `app.py` line 14) to create all four tables if they don't exist.
- All write operations call `conn.commit()` explicitly; reads return lists of `sqlite3.Row` objects.

### 3. AI Integration Layer — `ai_reply.py`
- Wraps the Anthropic Claude API (`claude-sonnet-4-6` model).
- Defines one static `SYSTEM_PROMPT` that encodes the brand voice and output format.
- Exposes two public functions:
  - `generate_reply(customer_message, context)` — for ad-hoc reply drafting.
  - `generate_sales_script(script_type)` — for three canned script types (`cold_lead`, `returning_customer`, `pricing_inquiry`).
- Reads `ANTHROPIC_API_KEY` from environment via `python-dotenv` at import time.
- Instantiates a new `anthropic.Anthropic` client per function call (no singleton).

### 4. Configuration / Environment
- `.env` — holds `ANTHROPIC_API_KEY`; loaded by `ai_reply.py` at module import.
- `.streamlit/config.toml` — sets `headless = true` (cloud deploy) and `theme.base = "dark"`.
- `requirements.txt` — pins three packages: `streamlit`, `anthropic`, `python-dotenv`.

---

## Data Flow

### User triggers an AI reply (most common path)
```
User types message in st.text_area (app.py)
  → st.button click triggers generate_reply() call (app.py)
    → ai_reply.generate_reply(msg, context) (ai_reply.py)
      → anthropic.Anthropic.messages.create() — HTTPS to Anthropic API
        → response.content[0].text returned
    → result stored in st.session_state["last_reply"]
  → Streamlit rerenders; text_area displays the reply
```

### User adds a client (typical CRUD path)
```
User fills st.form fields (app.py — Client Registry page)
  → st.form_submit_button click
    → db.add_client(...) (db.py)
      → sqlite3 INSERT into data/business.db
    → st.success() message shown
    → next interaction triggers st.rerun() / re-read from db
```

### Dashboard load (aggregate read path)
```
app.py startup: db.init_db() — ensures tables exist
Page == "Dashboard":
  → db.get_all_clients()  ─┐
  → db.get_leads()         ├─ three SQLite SELECT calls
  → db.get_posts(today)   ─┘
  → Python list comprehensions compute overdue/new_leads counts
  → st.markdown() renders stat widgets with computed values
```

---

## Key Abstractions

| Abstraction | Location | Role |
|---|---|---|
| `NAV_PAGES` list | `app.py` line 338 | Defines navigation order; each string maps to an `if/elif` page block |
| `page_header(icon, title, caption)` | `app.py` line 354 | Reusable UI helper — renders branded page title |
| `platform_badge(platform)` | `app.py` line 363 | Maps platform string → HTML badge span |
| `init_db()` | `db.py` line 15 | Idempotent schema migration (CREATE IF NOT EXISTS) |
| `get_conn()` | `db.py` line 9 | Connection factory; centralises row_factory config |
| `SYSTEM_PROMPT` | `ai_reply.py` line 7 | Static prompt that encodes brand voice for all AI calls |
| `generate_reply()` | `ai_reply.py` line 31 | Single-turn AI reply generation with optional context |
| `generate_sales_script()` | `ai_reply.py` line 51 | Lookup-table approach: maps script_type key → hardcoded prompt |

---

## Entry Points

| Entry Point | How invoked |
|---|---|
| `streamlit run app.py` | Normal startup — `db.init_db()` runs, Streamlit serves on port 8501 |
| `app.py` top-level | `st.set_page_config()` and CSS injection happen unconditionally on every request cycle |
| `db.init_db()` (line 14, `app.py`) | Called once per Python process start; safe to call repeatedly |

There is no `if __name__ == "__main__"` guard; `app.py` is intended only for `streamlit run`.

---

## Module Boundaries

```
app.py
  imports db          (data access — SQLite)
  imports ai_reply    (AI generation — Anthropic API)
  imports streamlit   (UI framework)
  imports datetime, base64, os  (stdlib)

db.py
  imports sqlite3, os  (stdlib only — no app.py dependency)

ai_reply.py
  imports anthropic, python-dotenv, os  (no db.py or app.py dependency)
```

`db.py` and `ai_reply.py` have no cross-dependency. Either can be imported and tested independently. `app.py` is the only integration point.

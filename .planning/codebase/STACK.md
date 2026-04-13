# Tech Stack

## Language

- **Python 3.9+** (pycache shows `cpython-314`, meaning Python 3.14 is in active use locally)
- No TypeScript, JavaScript, or other languages — pure Python backend + Streamlit-rendered HTML/CSS

## Runtime / Platform

- **Local:** Windows 10, run via `python -m streamlit run app.py`
- **Cloud:** Streamlit Community Cloud (`share.streamlit.io`), targeting `main` branch, entry point `app.py`
- Default port: `8501`

## Frameworks and Libraries

Pinned in `requirements.txt`:

| Package | Version Constraint | Role |
|---|---|---|
| `streamlit` | `>=1.35.0` | Full-stack web UI framework — pages, widgets, layout, session state |
| `anthropic` | `>=0.25.0` | Official Anthropic Python SDK — Claude API calls |
| `python-dotenv` | `>=1.0.0` | Loads `.env` file into `os.environ` for local dev |

Standard library only (no additional installs):

| Module | Role |
|---|---|
| `sqlite3` | Database access — all read/write in `db.py` |
| `os` | Path construction, env var access |
| `base64` | Encodes `assets/logo.png` for inline HTML embedding |
| `datetime` | Date arithmetic for dashboard greetings and lead overdue logic |

## Configuration Approach

### `.env` (local development)
- Path: `.env` at project root
- Single key: `ANTHROPIC_API_KEY`
- Loaded via `python-dotenv` (`load_dotenv()`) in `ai_reply.py`
- Gitignored — never committed

### Streamlit Cloud secrets (production)
- Configured via Streamlit Cloud UI under **Advanced settings → Secrets**
- TOML format: `ANTHROPIC_API_KEY = "sk-ant-..."`
- Accessed identically through `os.getenv("ANTHROPIC_API_KEY")`

### `.streamlit/config.toml`
- Path: `.streamlit/config.toml`
- Sets `[server] headless = true` (required for cloud/headless deploy)
- Sets `[theme] base = "dark"` (dark mode baseline)

### `.gitignore`
Ignores: `.env`, `data/`, `__pycache__/`, `*.pyc`, `.claude/`, `.streamlit/secrets.toml`

## Key Dependencies — What They Do

### `streamlit`
The entire UI layer. Handles routing (via `st.sidebar.radio`), all input widgets (`st.text_area`, `st.button`, `st.columns`), session state (`st.session_state`), and HTML rendering (`st.markdown(..., unsafe_allow_html=True)`). No separate frontend build step — Python IS the UI.

### `anthropic`
Wraps Claude API calls in `ai_reply.py`. Two functions use it:
- `generate_reply()` — single-turn message generation (`claude-sonnet-4-6`, `max_tokens=600`)
- `generate_sales_script()` — one-click script generation for 3 preset scenarios (`max_tokens=500`)
Both use `client.messages.create()` (non-streaming).

### `python-dotenv`
Called once at module load in `ai_reply.py` (`load_dotenv()`). Enables local dev without setting system env vars manually.

### `sqlite3` (stdlib)
All DB operations live in `db.py`. Uses `sqlite3.Row` for dict-like row access. No ORM — raw SQL with parameterized queries throughout.

## UI / Styling Approach

- All CSS injected via `st.markdown(..., unsafe_allow_html=True)` at the top of `app.py`
- Google Fonts loaded via `@import` in CSS: **Poppins** (headings/UI) and **Lora** (body)
- Google Material Icons loaded via `@import` for sidebar nav and toggle icons
- Brand palette defined as CSS custom properties (`--pink`, `--purple`, `--teal`, etc.)
- No CSS framework (no Tailwind, Bootstrap, etc.)

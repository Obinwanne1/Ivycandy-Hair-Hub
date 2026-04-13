# Structure — Ivycandy Hair Hub

## Directory Layout

```
BuildWeb/
├── app.py                    # Main application — all UI, routing, and page logic
├── db.py                     # SQLite data access layer
├── ai_reply.py               # Anthropic API wrapper (AI reply + sales scripts)
├── requirements.txt          # Python dependencies (3 packages)
├── .env                      # Environment secrets (ANTHROPIC_API_KEY) — gitignored
├── .gitignore
├── README.md                 # Project documentation
├── SKILL.md                  # AI feature guide
│
├── assets/
│   └── logo.png              # Brand logo — embedded as base64 in sidebar and tab icon
│
├── data/
│   └── business.db           # SQLite database file — auto-created on first run
│
├── .streamlit/
│   └── config.toml           # Streamlit server config (headless, dark theme)
│
├── __pycache__/              # Python bytecode cache — gitignored
│   ├── ai_reply.cpython-314.pyc
│   └── db.cpython-314.pyc
│
└── .planning/                # Planning documents (this directory)
    └── codebase/
        ├── ARCHITECTURE.md
        └── STRUCTURE.md
```

---

## Key File Locations and Purposes

### Source files

| File | Purpose |
|---|---|
| `app.py` | Single entry point. Contains: CSS theming, sidebar nav, Dashboard page, AI Reply Assistant page, Client Registry page, Lead Tracker page, Content Calendar page, Sales Scripts page. ~703 lines. |
| `db.py` | All SQLite logic. Defines `DB_PATH`, `get_conn()`, `init_db()`, and CRUD functions for four tables. ~169 lines. |
| `ai_reply.py` | Anthropic API calls. Defines `SYSTEM_PROMPT` (brand voice), `generate_reply()`, `generate_sales_script()`. ~71 lines. |

### Configuration files

| File | Purpose |
|---|---|
| `.env` | `ANTHROPIC_API_KEY=...` — loaded by `ai_reply.py` via `python-dotenv` |
| `.streamlit/config.toml` | `headless = true` for cloud deploy; `theme.base = "dark"` |
| `requirements.txt` | `streamlit>=1.35.0`, `anthropic>=0.25.0`, `python-dotenv>=1.0.0` |

### Data files

| File | Purpose |
|---|---|
| `data/business.db` | SQLite database. Contains tables: `clients`, `orders`, `leads`, `content_calendar`. Created by `db.init_db()` on first run. |

### Assets

| File | Purpose |
|---|---|
| `assets/logo.png` | Brand logo. Loaded at startup in `app.py`, base64-encoded, embedded in sidebar HTML and used as `page_icon`. |

---

## Naming Conventions

- **Python files**: snake_case (`ai_reply.py`, `db.py`, `app.py`).
- **DB functions**: verb + noun, snake_case. Prefixed by entity: `add_client`, `get_all_clients`, `update_client`, `delete_client`, `add_lead`, `get_leads`, `update_lead_status`, `add_post`, `get_posts`, `update_post_status`, `add_order`, `get_orders_for_client`.
- **Session state keys**: lowercase string literals with underscores, stored directly on `st.session_state`: `"last_reply"`, `"last_script"`, `"dash_reply"`.
- **Streamlit widget keys**: prefixed by context to avoid collisions: `dash_reply_btn`, `dash_clear`, `del_{id}`, `lead_status_{id}`, `save_lead_{id}`, `post_{id}`, `post_status_{id}`, `update_post_{id}`.
- **CSS classes**: kebab-case (`stat-widget`, `card-label`, `lead-row`, `page-header`, `sidebar-brand`).
- **CSS variables**: `--pink`, `--purple`, `--teal`, `--light`, `--midgray`, `--border`.
- **Page names**: Title Case strings in `NAV_PAGES` list (`"Dashboard"`, `"AI Reply Assistant"`, `"Client Registry"`, `"Lead Tracker"`, `"Content Calendar"`, `"Sales Scripts"`).
- **AI script types**: snake_case string keys used as lookup dictionary keys: `"cold_lead"`, `"returning_customer"`, `"pricing_inquiry"`.

---

## Where to Find Things

### Routes / Pages
All page logic is in `app.py`. Navigation is driven by:
```python
NAV_PAGES = [...]           # line 338 — defines page order
page = st.sidebar.radio(...)  # line 347 — captures selection
if page == "Dashboard": ...   # line 376 — page blocks separated by ═══ banners
elif page == "AI Reply Assistant": ...  # line 502
elif page == "Client Registry": ...     # line 536
elif page == "Lead Tracker": ...        # line 608
elif page == "Content Calendar": ...    # line 648
elif page == "Sales Scripts": ...       # line 683
```

### Database Models (table schemas)
All four table schemas are defined in `db.py` inside `init_db()`, lines 17–58:
- `clients` — id, name, platform, contact, style_pref, notes, last_contact, created_at
- `orders` — id, client_id (FK → clients), item, amount, order_date, notes
- `leads` — id, name, platform, inquiry, status, follow_up_on, created_at
- `content_calendar` — id, post_date, platform, caption, status

### DB CRUD functions
All in `db.py`:
- Clients: lines 63–99
- Orders: lines 103–116
- Leads: lines 120–140
- Content Calendar: lines 145–169

### AI Prompt / Brand Voice
`SYSTEM_PROMPT` constant in `ai_reply.py`, lines 7–28. Edit this to change AI tone, output format, or sales principles.

### Styling / Theming
Inline CSS is in `app.py`, lines 25–326, injected via `st.markdown(..., unsafe_allow_html=True)`. Imports Google Fonts (Poppins, Lora) and Material Icons from CDN.

### Utilities / Helpers
Two small helpers at the top of the routing section in `app.py`:
- `page_header(icon, title, caption)` — line 354
- `platform_badge(platform)` — line 363
- `_img_b64(path)` — line 16, used only for logo loading at startup

### Environment / Secrets
`ANTHROPIC_API_KEY` read from `.env` by `ai_reply.py` line 5 (`load_dotenv()`), then accessed as `os.getenv("ANTHROPIC_API_KEY")` inside each API-calling function.

### Assets
`assets/logo.png` — loaded once at startup (`app.py` line 20), stored as `LOGO_B64` global, injected into sidebar HTML at line 331.

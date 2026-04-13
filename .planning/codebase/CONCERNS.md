# Codebase Concerns

> Reference material for planning. Last updated: 2026-04-13.

---

## 1. Security Concerns

### 1.1 Live API Key Committed to `.env` (CRITICAL)
- **File:** `.env` line 2
- The Anthropic API key (`sk-ant-api03-jU53J…`) is stored in plaintext in `.env`, which is tracked by git (no `.gitignore` entry blocks it).
- Any push to a public repo (or even a private one with shared access) exposes the key.
- **Action:** Rotate the key immediately. Add `.env` to `.gitignore`. Use environment variables injected at the hosting layer (e.g., Streamlit Cloud Secrets).

### 1.2 No Authentication Layer
- **File:** `app.py` — entire file
- The dashboard has zero authentication. Anyone who can reach the URL can view, add, edit, and delete all client data, orders, and leads.
- This is a significant concern for cloud deployment (README references cloud deploy).
- **Action:** Add Streamlit's built-in `st.secrets`-based auth or a simple password gate via `st.text_input` + session state before any page renders.

### 1.3 XSS via `unsafe_allow_html`
- **File:** `app.py` — used extensively (lines 331, 356, 395, 451, 462, 470, 487, etc.)
- User-supplied data (client names, lead names, notes, captions, inquiry text) is interpolated directly into HTML strings passed to `st.markdown(..., unsafe_allow_html=True)`.
- Example: `{c['name']}` in the Recent Clients card (line 453), `{l['name']}` in lead rows (line 473), `{l['inquiry']}` in lead expander (line 638).
- A client name containing `<script>` or HTML tags will execute in the browser.
- **Action:** HTML-escape all database-sourced values before interpolating into `st.markdown` HTML blocks (use `html.escape()`).

### 1.4 No Input Validation on Amounts
- **File:** `app.py` line 588 — `amount = oc2.number_input("Amount (€)", min_value=0.0, step=5.0)`
- There is no maximum cap and no server-side validation. Streamlit's `number_input` enforces `min_value` client-side only; a crafted request could bypass it.
- Minor concern for a local tool, but relevant if exposed to internet.

---

## 2. Technical Debt

### 2.1 Massive Single-File Application
- **File:** `app.py` (~703 lines)
- All pages (Dashboard, AI Reply, Client Registry, Lead Tracker, Content Calendar, Sales Scripts), all CSS, and all UI logic are in one file.
- Adding a new page or modifying a page requires navigating the full file. Will become increasingly hard to maintain.
- **Action:** Split into a `pages/` structure (Streamlit multi-page) or at minimum extract each page section into its own module.

### 2.2 ~300 Lines of Inline CSS
- **File:** `app.py` lines 25–326
- The entire design system is a string literal injected via `st.markdown`. It relies heavily on Streamlit internal `data-testid` and `data-baseweb` attributes that are not part of any public API and break silently on Streamlit upgrades.
- **Action:** Extract to a separate `styles.py` or `assets/style.css` file, loaded once; add a note pinning the Streamlit version.

### 2.3 CSS Selector Fragility (nth-of-type Nav Icons)
- **File:** `app.py` lines 315–321
- Sidebar nav icons are injected using `label:nth-of-type(2)` through `nth-of-type(7)` with hardcoded `::before` content strings. This breaks immediately if a nav item is added, reordered, or removed.
- **Action:** Use a custom HTML component or icon-prefixed label text instead of positional CSS.

### 2.4 `__import__("datetime")` Inline Hack
- **File:** `app.py` line 379
- `__import__("datetime").datetime.now().hour` is used instead of a proper import. `datetime` is already available via `from datetime import date, timedelta` at the top; `datetime.datetime` was simply forgotten.
- **Action:** Change line 2 import to `from datetime import date, timedelta, datetime` and replace the inline `__import__` call with `datetime.now().hour`.

### 2.5 Hardcoded Follow-up Default of 3 Days
- **File:** `app.py` line 619 — `value=date.today() + timedelta(days=3)`
- The default follow-up window is baked into the UI. Should be a configurable setting (e.g., stored in a `settings` table or `.streamlit/secrets.toml`).

### 2.6 Hardcoded Currency Symbol (€)
- **File:** `app.py` lines 588, 599, 601
- Currency is hardcoded as euros (€). If the business operates in GBP, NGN, or another currency, every reference must be manually updated.
- **Action:** Move to a config constant or `st.secrets`.

### 2.7 Hardcoded Business Name and Brand Text
- **File:** `app.py` lines 7, 333–335, 384
- "Ivycandy Hair Hub", "Ivycandy Hair", "Business Dashboard" are scattered as literals throughout the file.
- **Action:** Centralize into a `config.py` or top-of-file constants.

---

## 3. Known Bugs / Fragile Areas

### 3.1 `recent_clients` Ordering Relies on DB Insert Order
- **File:** `app.py` line 443 — `list(reversed(all_clients))[:6]`
- `get_all_clients()` returns rows `ORDER BY name` alphabetically. `reversed()` on an alphabetically sorted list does not give "most recently added" — it gives reverse-alphabetical order.
- **Action:** Either add `ORDER BY created_at DESC` to the query or use a dedicated `get_recent_clients(n)` function.

### 3.2 Lead Overdue Logic Duplicated in Two Places
- **File:** `app.py` lines 391 (Dashboard) and 629 (Lead Tracker)
- The overdue filter `l['follow_up_on'] <= str(today) and l['status'] == 'new'` is copy-pasted in both page sections. If the definition of "overdue" changes, both must be updated.
- **Action:** Extract to a helper function in `db.py` or a shared utilities module.

### 3.3 `display_leads` Deduplication is Broken
- **File:** `app.py` line 463 — `overdue + [l for l in new_leads if l not in overdue]`
- `sqlite3.Row` objects do not support equality comparison by value — `l not in overdue` uses object identity. Overdue leads will appear twice.
- **Action:** Use `id`-based deduplication: `{l['id']: l for l in overdue + new_leads}.values()`.

### 3.4 Content Calendar `View Schedule` Only Filters by Exact Date
- **File:** `app.py` lines 666–678, `db.py` `get_posts()`
- There is no way to view a week or month at a glance. Users must select each day individually. This will frustrate planning workflows.
- **Action:** Add a date-range query option.

### 3.5 No Edit Functionality for Leads or Posts
- **File:** `app.py` Lead Tracker and Content Calendar sections
- Users can update lead status and post status but cannot edit the lead inquiry text, name, platform, or post caption/date after creation. Corrections require deleting and re-adding records.

### 3.6 Order Amount Currency Label Inconsistency
- **File:** `app.py` line 599 renders `€{total:.2f}` but `db.py` stores `amount` as `REAL` with no currency metadata. If orders were entered with amounts in a different unit, the display is silently wrong.

---

## 4. Performance Bottlenecks

### 4.1 Full Table Scans on Every Page Load
- **File:** `db.py` — `get_all_clients()`, `get_leads()`, `get_posts()`
- Every page re-render (which Streamlit triggers on any interaction) re-queries all rows from all tables. No pagination, no `LIMIT`.
- Acceptable for small data (<200 rows), but will slow noticeably at scale.
- **Action:** Add `@st.cache_data(ttl=30)` decorators on read functions, or implement pagination. Add indexes on frequently filtered columns (`leads.status`, `leads.follow_up_on`, `content_calendar.post_date`).

### 4.2 Logo Loaded and Base64-Encoded on Every Cold Start
- **File:** `app.py` lines 16–20 — `_img_b64()` is called at module level
- Executed once per Streamlit worker process restart, which is fine. However, there is no error handling: if `assets/logo.png` is missing (e.g., on a fresh clone without the binary), the app crashes on startup with an unhandled `FileNotFoundError`.
- **Action:** Wrap in a try/except and fall back to a placeholder.

### 4.3 New Anthropic Client Instantiated on Every AI Call
- **File:** `ai_reply.py` lines 36, 63 — `client = anthropic.Anthropic(...)` inside the function body
- A new SDK client object is created for every call. While lightweight, it is wasteful and inconsistent.
- **Action:** Instantiate once at module level.

---

## 5. Missing Error Handling

### 5.1 No API Key Validation at Startup
- **File:** `ai_reply.py` line 36 — `api_key=os.getenv("ANTHROPIC_API_KEY")`
- If `ANTHROPIC_API_KEY` is not set, `os.getenv()` returns `None` and the Anthropic client will raise an unhelpful error only when the first AI call is made, deep in the UI flow.
- **Action:** Check for the key at app startup (`app.py`) and display a clear `st.error` banner if missing.

### 5.2 `generate_sales_script` Will `KeyError` on Unknown Script Type
- **File:** `ai_reply.py` line 65 — `prompts[script_type]`
- If an unrecognised `script_type` string is passed, Python raises an unhandled `KeyError`. The calling UI in `app.py` only passes values from a fixed dict, so this is safe today, but fragile.
- **Action:** Use `prompts.get(script_type)` with a fallback or raise a descriptive `ValueError`.

### 5.3 Database Errors Are Not Caught in UI
- **File:** `app.py` — all `db.*` calls (add_client, add_lead, add_post, etc.)
- None of the form submission handlers wrap `db.*` calls in try/except. A SQLite lock, disk-full error, or schema mismatch will produce an unhandled exception and crash the page.
- **Action:** Wrap DB calls in try/except and surface errors with `st.error()`.

### 5.4 Schema Migrations Are Not Handled
- **File:** `db.py` `init_db()`
- `CREATE TABLE IF NOT EXISTS` only creates tables that don't exist. If the schema changes (e.g., a new column is added), existing deployments will silently keep the old schema. There is no migration mechanism.
- **Action:** Add a lightweight migration layer (check column existence with `PRAGMA table_info()` and `ALTER TABLE ADD COLUMN` as needed).

---

## 6. Hard-coded Values That Should Be Configurable

| Value | File / Line | Should become |
|---|---|---|
| `"claude-sonnet-4-6"` model ID | `ai_reply.py` lines 43, 65 | Config constant or secret |
| `max_tokens=600` / `500` | `ai_reply.py` lines 44, 65 | Config constant |
| Follow-up default `+3 days` | `app.py` line 619 | Settings/config |
| Currency `€` | `app.py` lines 588, 599, 601 | Config constant |
| Business name "Ivycandy Hair Hub" | `app.py` lines 7, 333–335 | Config constant |
| DB path `data/business.db` | `db.py` line 4 | Env var / config |
| 5-year business history in system prompt | `ai_reply.py` line 7 | Configurable prompt template |

---

## 7. Dependencies — Outdated or Risky

- **`requirements.txt`** pins only minimum versions (`>=`) with no upper bounds or lock file.
- `streamlit>=1.35.0` — major UI-breaking changes are common between minor versions; the CSS hacks in `app.py` are particularly fragile across versions.
- `anthropic>=0.25.0` — the SDK has had breaking changes between minor versions (e.g., messages API shape). No lock ensures reproducible installs.
- There is no `requirements-lock.txt` or `pip freeze` snapshot committed.
- **Action:** Add a `requirements-lock.txt` (or use `pip-compile`) and pin a specific Streamlit version that has been tested with the current CSS selectors.

---

## 8. Areas Needing Refactoring Before Scaling

### 8.1 No Multi-user Support
The entire app assumes a single user. All session state is global to the Streamlit session. If the app were ever shared with a team (e.g., multiple staff members), session state conflicts and shared-write races on SQLite would occur immediately.

### 8.2 SQLite Is the Entire Data Layer
`data/business.db` is a local file. This means:
- No concurrent writes from multiple users
- No cloud-native backup
- Data is lost if the hosting container is ephemeral (Streamlit Cloud restarts wipe the filesystem)
- **Action:** Migrate to a hosted database (PostgreSQL via Supabase, PlanetScale, etc.) before any cloud-production deployment.

### 8.3 No Logging or Audit Trail
No logging of AI calls, errors, or user actions exists. If an AI reply is generated and something goes wrong, there is no record. At scale, API cost visibility and error debugging require structured logging.

### 8.4 `app.py` God-File Pattern
All routing, UI rendering, CSS, and business logic live in one 703-line file. This is the single largest refactoring need: split into Streamlit multi-page app (`pages/`) with shared utilities in `utils/` or `components/`.

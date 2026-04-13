# Codebase Conventions

Reference material for planning work on `C:\Users\rigwe\Desktop\TicToc\BuildWeb`.

---

## Code Style

### Formatting and Indentation

- **4-space indentation** throughout all Python files (`app.py`, `db.py`, `ai_reply.py`).
- Line lengths are generally kept reasonable but not strictly enforced — long `st.markdown()` calls with inline HTML can run 150–200+ characters (accepted as-is for template strings).
- Blank lines are used liberally to separate logical sections within a page block.
- Inline HTML within `st.markdown()` calls uses single-line formatting for short snippets and multi-line strings for longer blocks.

### Imports

- Standard library imports first, then third-party, then local modules.
- `app.py` uses a single-line multi-import: `import base64, os` — the only case of comma-combined imports.
- Local modules (`db`, `ai_reply`) are imported without aliasing.

---

## Naming Conventions

### Variables

- `snake_case` for all variables: `all_clients`, `new_leads`, `filter_status`, `post_platform`.
- Short, descriptive names preferred over long ones: `c` for a client row in a loop, `l` for a lead row, `p` for a post row.
- Temporary form field variables use the object type as prefix: `l_name`, `l_platform`, `lc1`, `lc2` (lead columns), `pc1`, `pc2` (post columns).
- Session state keys are string literals in `snake_case`: `"dash_reply"`, `"last_reply"`, `"last_script"`.

### Functions

- `snake_case` for all functions.
- `db.py` functions follow a consistent CRUD verb pattern:
  - `add_*` — inserts a new record (e.g. `add_client`, `add_lead`, `add_order`, `add_post`)
  - `get_*` — retrieves records (e.g. `get_all_clients`, `get_leads`, `get_posts`)
  - `update_*` — updates a specific field (e.g. `update_client`, `update_lead_status`, `update_post_status`)
  - `delete_*` — removes a record (e.g. `delete_client`)
  - `search_*` — filtered retrieval (e.g. `search_clients`)
- Helper functions in `app.py` are prefixed with `_` for private/internal use: `_img_b64`.
- Page-level helpers are short and action-named: `page_header`, `platform_badge`.

### Constants

- `UPPER_SNAKE_CASE` for module-level constants: `DB_PATH`, `SYSTEM_PROMPT`, `LOGO_B64`, `NAV_PAGES`.

### Files

- All lowercase, no separators except underscores: `app.py`, `db.py`, `ai_reply.py`.
- The three source files map 1:1 to their responsibilities: UI, database, AI.

### CSS Classes

- `kebab-case` for all custom CSS class names: `stat-grid`, `stat-widget`, `lead-row`, `lead-dot`, `page-header`, `card-label`, `badge-ig`, `sidebar-brand`.
- Modifier variants use a second segment: `badge-ig`, `badge-tt`, `badge-wa`, `badge-fb`, `badge-def`.

---

## Common Patterns

### Page Routing

Navigation is handled by a single `st.sidebar.radio()` call. Each page is a top-level `if/elif` block in `app.py` keyed on the string value of `page`:

```python
if page == "Dashboard":
    ...
elif page == "AI Reply Assistant":
    ...
```

No page modules or routing abstraction — all pages live inline in `app.py`.

### HTML Injection via `st.markdown`

Custom HTML is injected via `st.markdown(..., unsafe_allow_html=True)`. Paired open/close div tags are common:

```python
st.markdown('<div class="card"><div class="card-label">...</div>', unsafe_allow_html=True)
# ... Streamlit widgets ...
st.markdown('</div>', unsafe_allow_html=True)
```

This pattern wraps Streamlit native widgets inside custom HTML containers. The open tag is injected as one `st.markdown` call; the close tag as another.

### Streamlit Forms

`st.form()` is used for all data-entry operations (add client, add lead, add order, plan post). The pattern is:

```python
with st.form("form_key", clear_on_submit=True):
    # field widgets
    submitted = st.form_submit_button("Label", type="primary")
if submitted:
    # validation then db write
```

Validation (e.g. `if not name.strip()`) happens outside the `with` block, after form submission.

### Session State for AI Outputs

AI-generated content is stored in `st.session_state` under a string key. The UI renders conditionally based on whether the key exists:

```python
if generate_btn:
    reply = ai_reply.generate_reply(...)
    st.session_state["last_reply"] = reply
if "last_reply" in st.session_state:
    st.text_area(...)
    st.button("Clear", on_click=lambda: st.session_state.pop("last_reply", None))
```

### Database Connections

Every `db.py` function opens and closes its own connection via `with get_conn() as conn:`. There is no persistent connection or connection pool. `conn.row_factory = sqlite3.Row` is set on every connection so rows behave like dicts.

### Column Layouts

`st.columns()` is used heavily throughout pages. Column variables are typically named `col1, col2` (or `c1, c2`, `lc1, lc2`, etc.) and immediately unpacked in assignment.

---

## Error Handling

- AI API calls are wrapped in `try/except Exception as e` blocks, with the error surfaced via `st.error(str(e))` or `st.error(f"API error: {e}")`.
- Database operations have no explicit error handling — exceptions would propagate to Streamlit's built-in error display.
- Form validation is manual and minimal: required fields are checked with `.strip()`, and `st.error()` is shown for failures; `st.success()` for success.
- No logging framework is used anywhere in the codebase.

---

## State Management

State is managed at three levels:

1. **Ephemeral UI state** — Streamlit re-renders on every interaction; form values and widget states are held by Streamlit's internal state between reruns.
2. **`st.session_state`** — Used exclusively for AI output caching (`"dash_reply"`, `"last_reply"`, `"last_script"`). Keys are popped on "Clear" button clicks.
3. **SQLite persistence** — All business data (clients, leads, orders, content calendar) is persisted to `data/business.db` via `db.py`. Reads happen on every page render; writes are committed immediately after each mutation.

`st.rerun()` is called explicitly after destructive or mutating DB operations (delete, status update) to force a full page refresh.

---

## Comment and Docstring Practices

### Section Dividers

Heavy use of box-drawing comment banners to separate major sections in `app.py`:

```python
# ═══════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ═══════════════════════════════════════════════════════════
```

Lighter dividers separate sub-sections within a page or within `db.py`:

```python
# ── Clients ──────────────────────────────────────────────
# ── Sidebar ────────────────────────────────────────────────
```

### Docstrings

`ai_reply.py` is the only file with function docstrings. They are single-paragraph plain English, describing the function's purpose and noting parameter meanings:

```python
def generate_reply(customer_message: str, context: str = "") -> str:
    """
    Generate a sales-focused WhatsApp reply for a customer message.
    context: optional extra info e.g. customer name, purchase history
    """
```

`db.py` and `app.py` have no docstrings on functions.

### Inline Comments

Inline comments in `app.py` are used sparingly for UI layout intent (`# ── Greeting ──`, `# Hero — Quick Reply`, `# Overdue leads widget`). CSS blocks include brief comment labels for each component group.

### Type Hints

Used in `ai_reply.py` function signatures (`customer_message: str`, `context: str = ""`, `-> str`). Absent in `db.py` and `app.py`.

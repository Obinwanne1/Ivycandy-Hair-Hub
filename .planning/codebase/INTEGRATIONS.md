# Integrations

## External APIs

### Anthropic Claude API
- **SDK:** `anthropic` Python package (`>=0.25.0`)
- **Model used:** `claude-sonnet-4-6`
- **Purpose:** AI-generated customer reply messages and sales scripts
- **Where called:** `ai_reply.py` — `generate_reply()` and `generate_sales_script()`
- **Auth:** `ANTHROPIC_API_KEY` environment variable (`.env` locally, Streamlit secrets in production)
- **Call pattern:** Non-streaming `client.messages.create()`, single-turn only (no conversation history)
- **Token limits:** `max_tokens=600` for replies, `max_tokens=500` for scripts
- **Data sent:** Raw customer message text + optional context string. Customer messages leave the app and go to Anthropic's API servers — noted in README under Data & Privacy.

### Google Fonts / Material Icons (CDN)
- **Type:** CDN asset load (no API key required)
- **Fonts loaded:** Poppins, Lora (via `fonts.googleapis.com/css2`)
- **Icons loaded:** Material Icons (via `fonts.googleapis.com/icon`)
- **How:** `@import` rules in injected CSS in `app.py`
- **Dependency risk:** Requires outbound internet access at runtime; no offline fallback defined

---

## Database

### SQLite
- **Type:** Embedded relational database (file-based, no server)
- **ORM:** None — raw `sqlite3` stdlib with parameterized queries
- **File path:** `data/business.db` (relative to project root, created automatically)
- **Access module:** `db.py`
- **Connection pattern:** `sqlite3.connect()` per operation, `conn.row_factory = sqlite3.Row` for dict-style access

### Schema (4 tables, defined in `db.init_db()`)

**`clients`**
| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER PK | autoincrement |
| `name` | TEXT NOT NULL | |
| `platform` | TEXT | Instagram / TikTok / WhatsApp / Facebook |
| `contact` | TEXT | phone or handle |
| `style_pref` | TEXT | hair style preference |
| `notes` | TEXT | free-form notes |
| `last_contact` | TEXT | date string |
| `created_at` | TEXT | `datetime('now')` default |

**`orders`**
| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER PK | autoincrement |
| `client_id` | INTEGER | FK → `clients(id)` ON DELETE CASCADE |
| `item` | TEXT | product name |
| `amount` | REAL | sale value |
| `order_date` | TEXT | `date('now')` default |
| `notes` | TEXT | |

**`leads`**
| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER PK | autoincrement |
| `name` | TEXT | |
| `platform` | TEXT | social platform source |
| `inquiry` | TEXT | what they asked about |
| `status` | TEXT | `'new'` default; also `'contacted'`, `'converted'`, `'lost'` |
| `follow_up_on` | TEXT | date string for reminder |
| `created_at` | TEXT | `datetime('now')` default |

**`content_calendar`**
| Column | Type | Notes |
|---|---|---|
| `id` | INTEGER PK | autoincrement |
| `post_date` | TEXT | planned publish date |
| `platform` | TEXT | Instagram / TikTok / Facebook / LinkedIn |
| `caption` | TEXT | post copy |
| `status` | TEXT | `'draft'` default |

### Persistence Notes
- **Local:** database persists between runs in `data/business.db` (gitignored)
- **Streamlit Cloud:** ephemeral — resets on each redeploy; README recommends replacing `db.py` with Supabase or PlanetScale for persistent cloud storage

---

## Auth Providers

None. No user authentication is implemented. The app is single-user by design — intended for the business owner only. Access control relies entirely on deployment access (private Streamlit Cloud URL or local-only).

---

## Cloud Services

### Streamlit Community Cloud
- **URL:** `share.streamlit.io`
- **Deploy target:** `main` branch, entry `app.py`
- **Secrets management:** Streamlit Cloud secrets UI (TOML format)
- **Limitations documented:** SQLite is ephemeral (resets on redeploy)

---

## Webhooks / Event Systems

None. The app is entirely request/response — no webhooks, no background jobs, no queues, no pub/sub. All AI calls are synchronous, blocking on user button click.

---

## Social Platform References (Non-API)

The app tracks activity on Instagram, TikTok, WhatsApp, and Facebook as data fields only. There is no programmatic integration with any of these platforms — no OAuth, no API calls, no posting automation. The content calendar and lead tracker store platform names as text; replies are copy-pasted manually by the business owner.

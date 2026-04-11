# Ivycandy Hair Hub

A business intelligence dashboard for **Ivycandy Hair** — a premium online hair business operating through WhatsApp, Instagram, TikTok, and Facebook.

Live on Streamlit Cloud · runs locally on Windows · no external database required.

---

## Pages

| Page | Icon | Description |
|---|---|---|
| **Dashboard** | `dashboard` | Live stat widgets (clients, leads, overdue follow-ups, posts) + quick AI reply + recent activity |
| **AI Reply Assistant** | `auto_awesome` | Paste a customer message → get a professional, ready-to-send WhatsApp reply instantly |
| **Client Registry** | `people` | Store customer details, style preferences, contact info, and full order history |
| **Lead Tracker** | `flag` | Log social media leads with auto 3-day follow-up reminders and overdue alerts |
| **Content Calendar** | `calendar_month` | Plan and draft posts for Instagram, TikTok, Facebook, and LinkedIn |
| **Sales Scripts** | `description` | One-click scripts for cold leads, returning customers, and pricing inquiries |

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | [Streamlit](https://streamlit.io) |
| AI | [Anthropic Claude API](https://anthropic.com) (`claude-sonnet-4-6`) |
| Database | SQLite (local) / ephemeral on Streamlit Cloud |
| Language | Python 3.9+ |
| Icons | [Google Material Icons](https://fonts.google.com/icons) via CSS |

---

## Deployment

### Streamlit Cloud (live URL)

1. Fork or connect the repo at [share.streamlit.io](https://share.streamlit.io)
2. Set **Branch:** `main` · **Main file:** `app.py`
3. Under **Advanced settings → Secrets**, add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
4. Click **Deploy**

> The SQLite database is ephemeral on Streamlit Cloud — data resets on redeploy. For persistent cloud storage, replace `db.py` with a hosted database (e.g. Supabase, PlanetScale).

### Local (Windows)

```bash
git clone https://github.com/Obinwanne1/Ivycandy-Hair-Hub.git
cd Ivycandy-Hair-Hub
pip install -r requirements.txt
```

Create a `.env` file:
```env
ANTHROPIC_API_KEY=your_api_key_here
```

Run the app:
```bash
python -m streamlit run app.py
```

Open `http://localhost:8501` in your browser.

#### Windows quick-launch (.bat)

```bat
@echo off
cd /d "C:\path\to\Ivycandy-Hair-Hub"
start "" http://localhost:8501
python -m streamlit run app.py --server.headless true --browser.gatherUsageStats false
```

---

## Project Structure

```
Ivycandy-Hair-Hub/
├── app.py                  # Main Streamlit app — all pages + CSS
├── db.py                   # SQLite — all read/write operations
├── ai_reply.py             # Claude API — reply generation + sales scripts
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── config.toml         # Streamlit server config
├── assets/
│   └── logo.png            # Brand logo (committed)
├── .env                    # API key — local only, never committed
└── data/                   # SQLite database file — never committed
```

---

## Data & Privacy

- All customer data is stored in `data/business.db` (SQLite, local)
- AI replies are generated via the Anthropic API — customer messages are sent to Anthropic's servers
- `.env` and `data/` are gitignored — credentials and data never enter version control
- On Streamlit Cloud, data is stored on Streamlit's infrastructure and resets on redeploy

---

## AI Features

See [SKILL.md](SKILL.md) for a guide to the AI Reply Assistant and Sales Scripts.

---

## Customising for Another Business

1. Replace `assets/logo.png` with the client's logo
2. Update brand colors in the `:root` CSS block in `app.py`
3. Update the AI system prompt in `ai_reply.py` to match the client's brand voice
4. Replace the currency symbol (`€`) throughout `app.py`
5. Update `page_title` and `page_icon` in `st.set_page_config()`
6. Update sidebar nav labels in the `NAV_PAGES` list in `app.py`

---

## Built With

- [Streamlit](https://streamlit.io)
- [Anthropic Claude API](https://docs.anthropic.com)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html)

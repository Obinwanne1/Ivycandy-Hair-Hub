# Ivycandy Hair Hub

A local business intelligence dashboard built for **Ivycandy Hair** — a premium online hair business operating through WhatsApp, Instagram, TikTok, and Facebook.

No website required. Runs entirely on your computer.

---

## What It Does

| Page | Icon | Description |
|---|---|---|
| **Dashboard** | `dashboard` | Live stat widgets (clients, leads, overdue, posts) + quick AI reply + recent activity grid |
| **AI Reply Assistant** | `auto_awesome` | Paste a customer's WhatsApp/DM message → get a professional, sales-focused reply in seconds |
| **Client Registry** | `people` | Store customer details, style preferences, and full order history |
| **Lead Tracker** | `flag` | Log social media leads with auto 3-day follow-up reminders and overdue alerts |
| **Content Calendar** | `calendar_month` | Plan and draft posts for Instagram, TikTok, Facebook, and LinkedIn |
| **Sales Scripts** | `description` | One-click scripts for cold leads, returning customers, and pricing inquiries |

Nav icons are rendered via [Google Material Icons](https://fonts.google.com/icons) — no emoji, no image files.

---

## Tech Stack

- **UI** — [Streamlit](https://streamlit.io) (runs in your browser, no server needed)
- **Database** — SQLite (all data stored locally on your machine)
- **AI** — [Anthropic Claude API](https://anthropic.com) (`claude-sonnet-4-6`)
- **Language** — Python 3.9+

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/Obinwanne1/Ivycandy-Hair-Hub.git
cd Ivycandy-Hair-Hub
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your API key

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

Get your key at [console.anthropic.com](https://console.anthropic.com)

### 4. Add your logo

Place your logo image at:
```
assets/logo.png
```

### 5. Run the app

```bash
python -m streamlit run app.py --server.headless true --browser.gatherUsageStats false
```

Then open your browser to `http://localhost:8501`

---

## Windows Quick Launch

Create a `.bat` file on your Desktop for one double-click startup:

```bat
@echo off
cd /d "C:\path\to\Ivycandy-Hair-Hub"
start "" http://localhost:8501
python -m streamlit run app.py --server.headless true --browser.gatherUsageStats false --server.port 8501
```

---

## Project Structure

```
Ivycandy-Hair-Hub/
├── app.py              # Main Streamlit app (all pages + CSS)
├── db.py               # SQLite database — all read/write operations
├── ai_reply.py         # Claude API — reply generation + sales scripts
├── requirements.txt    # Python dependencies
├── .env                # Your API key (not committed to git)
├── assets/             # Logo image (not committed to git)
└── data/               # SQLite database file (not committed to git)
```

---

## Data & Privacy

All customer data is stored **locally** in `data/business.db` (SQLite).  
Nothing is sent to any cloud service except AI-generated replies (via the Anthropic API).  
Your `.env` and `data/` folder are excluded from git — your data stays on your machine.

---

## Customising for Another Client

1. Replace `assets/logo.png` with the client's logo
2. Update brand colors in the `:root` CSS block inside `app.py`
3. Update the AI system prompt in `ai_reply.py` to match the client's brand voice
4. Change currency symbol (search/replace `€` in `app.py`)
5. Update `page_title` and `page_icon` in `st.set_page_config()`
6. Update sidebar nav labels in the `NAV_PAGES` list in `app.py`

---

## Built With

- [Streamlit](https://streamlit.io)
- [Anthropic Claude API](https://docs.anthropic.com)
- [Python `sqlite3`](https://docs.python.org/3/library/sqlite3.html)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

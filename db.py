import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "business.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                platform    TEXT,
                contact     TEXT,
                style_pref  TEXT,
                notes       TEXT,
                last_contact TEXT,
                created_at  TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id  INTEGER REFERENCES clients(id) ON DELETE CASCADE,
                item       TEXT,
                amount     REAL,
                order_date TEXT DEFAULT (date('now')),
                notes      TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                name         TEXT,
                platform     TEXT,
                inquiry      TEXT,
                status       TEXT DEFAULT 'new',
                follow_up_on TEXT,
                created_at   TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS content_calendar (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                post_date   TEXT,
                platform    TEXT,
                caption     TEXT,
                status      TEXT DEFAULT 'draft'
            )
        """)
        conn.commit()


# ── Clients ──────────────────────────────────────────────
def add_client(name, platform, contact, style_pref, notes, last_contact):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO clients (name, platform, contact, style_pref, notes, last_contact) VALUES (?,?,?,?,?,?)",
            (name, platform, contact, style_pref, notes, last_contact),
        )
        conn.commit()


def get_all_clients():
    with get_conn() as conn:
        return conn.execute("SELECT * FROM clients ORDER BY name").fetchall()


def search_clients(query):
    with get_conn() as conn:
        like = f"%{query}%"
        return conn.execute(
            "SELECT * FROM clients WHERE name LIKE ? OR contact LIKE ? OR platform LIKE ?",
            (like, like, like),
        ).fetchall()


def update_client(client_id, name, platform, contact, style_pref, notes, last_contact):
    with get_conn() as conn:
        conn.execute(
            """UPDATE clients SET name=?, platform=?, contact=?, style_pref=?, notes=?, last_contact=?
               WHERE id=?""",
            (name, platform, contact, style_pref, notes, last_contact, client_id),
        )
        conn.commit()


def delete_client(client_id):
    with get_conn() as conn:
        conn.execute("DELETE FROM clients WHERE id=?", (client_id,))
        conn.commit()


# ── Orders ────────────────────────────────────────────────
def add_order(client_id, item, amount, order_date, notes):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO orders (client_id, item, amount, order_date, notes) VALUES (?,?,?,?,?)",
            (client_id, item, amount, order_date, notes),
        )
        conn.commit()


def get_orders_for_client(client_id):
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM orders WHERE client_id=? ORDER BY order_date DESC", (client_id,)
        ).fetchall()


# ── Leads ────────────────────────────────────────────────
def add_lead(name, platform, inquiry, follow_up_on):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO leads (name, platform, inquiry, follow_up_on) VALUES (?,?,?,?)",
            (name, platform, inquiry, follow_up_on),
        )
        conn.commit()


def get_leads(status=None):
    with get_conn() as conn:
        if status:
            return conn.execute(
                "SELECT * FROM leads WHERE status=? ORDER BY follow_up_on", (status,)
            ).fetchall()
        return conn.execute("SELECT * FROM leads ORDER BY follow_up_on").fetchall()


def update_lead_status(lead_id, status):
    with get_conn() as conn:
        conn.execute("UPDATE leads SET status=? WHERE id=?", (status, lead_id))
        conn.commit()


# ── Content Calendar ──────────────────────────────────────
def add_post(post_date, platform, caption):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO content_calendar (post_date, platform, caption) VALUES (?,?,?)",
            (post_date, platform, caption),
        )
        conn.commit()


def get_posts(post_date=None):
    with get_conn() as conn:
        if post_date:
            return conn.execute(
                "SELECT * FROM content_calendar WHERE post_date=? ORDER BY platform", (post_date,)
            ).fetchall()
        return conn.execute(
            "SELECT * FROM content_calendar ORDER BY post_date DESC"
        ).fetchall()


def update_post_status(post_id, status):
    with get_conn() as conn:
        conn.execute("UPDATE content_calendar SET status=? WHERE id=?", (status, post_id))
        conn.commit()

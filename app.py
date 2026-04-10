import streamlit as st
from datetime import date, timedelta
import base64, os
import db
import ai_reply

st.set_page_config(
    page_title="Ivycandy Hair Hub",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

db.init_db()

def _img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

LOGO_B64 = _img_b64(os.path.join(os.path.dirname(__file__), "assets", "logo.png"))

# ═══════════════════════════════════════════════════════════
# BRAND CSS
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Lora:ital,wght@0,400;0,500;1,400&display=swap');
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

:root {
    --pink:    #d94797;
    --purple:  #966acc;
    --teal:    #4e6b86;
    --light:   #f5f0f0;
    --midgray: #b7a7a7;
    --border:  #3d3030;
}

html, body, [class*="css"] { font-family: 'Lora', Georgia, serif; }
h1, h2, h3 { font-family: 'Poppins', Arial, sans-serif !important; font-weight: 700 !important; }


/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2a1f1f 0%, #1a1414 100%) !important;
    border-right: 1px solid var(--border);
    padding-top: 0 !important;
}
section[data-testid="stSidebar"] .block-container { padding-top: 3rem; }
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] label p,
section[data-testid="stSidebar"] label span,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] p {
    color: #ffffff !important;
    font-family: 'Poppins', Arial, sans-serif !important;
    font-size: 0.88rem !important;
}

/* ── Sidebar brand ── */
.sidebar-brand {
    display: flex; flex-direction: column; align-items: center;
    padding: 1.5rem 1rem 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}
.sidebar-brand img {
    width: 100px; border-radius: 50%;
    border: 2px solid var(--pink);
    margin-bottom: 0.6rem; object-fit: cover;
}
.sidebar-brand h1 {
    font-family: 'Poppins', Arial, sans-serif;
    font-size: 1rem; font-weight: 700;
    color: #fff; margin: 0;
    letter-spacing: 0.02em; text-align: center;
}
.sidebar-brand span {
    font-size: 0.68rem; color: var(--pink);
    letter-spacing: 0.12em; text-transform: uppercase; margin-top: 3px;
}

/* ── Page header ── */
.page-header {
    padding-bottom: 0.75rem;
    border-bottom: 2px solid var(--pink);
    margin-bottom: 1.5rem;
}
.page-header h1 {
    font-family: 'Poppins', Arial, sans-serif !important;
    font-size: 1.75rem !important; font-weight: 700 !important;
    margin: 0 !important; padding: 0 !important;
    display: flex; align-items: center; gap: 0.5rem;
}
.page-caption { font-size: 0.85rem; opacity: 0.6; margin-top: -1rem; margin-bottom: 1.5rem; }

/* ── MSN-style stat widgets ── */
.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-bottom: 1.75rem; }
.stat-widget {
    background: rgba(128,128,128,0.06);
    border: 1px solid rgba(128,128,128,0.18);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    transition: box-shadow 0.2s;
    position: relative; overflow: hidden;
}
.stat-widget:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
.stat-widget::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: var(--accent, var(--pink));
}
.stat-widget .stat-label {
    font-family: 'Poppins', Arial, sans-serif;
    font-size: 0.68rem; letter-spacing: 0.1em;
    text-transform: uppercase; opacity: 0.6; margin-bottom: 0.4rem;
}
.stat-widget .stat-value {
    font-family: 'Poppins', Arial, sans-serif;
    font-size: 2rem; font-weight: 700; line-height: 1;
    margin-bottom: 0.25rem;
}
.stat-widget .stat-sub { font-size: 0.78rem; opacity: 0.55; }

/* ── MSN-style content grid ── */
.content-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 1.25rem; margin-bottom: 1.5rem; }
.content-grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem; }

/* ── Cards ── */
.card {
    background: rgba(128,128,128,0.06) !important;
    border: 1px solid rgba(128,128,128,0.18) !important;
    border-radius: 14px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.1); }

/* Section header — MSN style */
.section-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 0.85rem; padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(128,128,128,0.2);
}
.section-header h3 {
    font-family: 'Poppins', Arial, sans-serif !important;
    font-size: 0.85rem !important; font-weight: 600 !important;
    text-transform: uppercase; letter-spacing: 0.06em;
    margin: 0 !important;
}
.section-header .see-more {
    font-family: 'Poppins', Arial, sans-serif;
    font-size: 0.75rem; color: var(--pink); cursor: pointer;
    text-decoration: none;
}

/* Card label */
.card-label {
    font-family: 'Poppins', Arial, sans-serif;
    font-size: 0.68rem; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--pink) !important;
    margin-bottom: 0.5rem;
}

/* Lead row card */
.lead-row {
    display: flex; align-items: center; gap: 0.75rem;
    padding: 0.65rem 0;
    border-bottom: 1px solid rgba(128,128,128,0.12);
}
.lead-row:last-child { border-bottom: none; }
.lead-dot {
    width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0;
}
.lead-dot.overdue { background: #e74c3c; }
.lead-dot.new     { background: var(--pink); }
.lead-dot.contacted { background: var(--teal); }
.lead-dot.converted { background: #27ae60; }
.lead-dot.lost    { background: #999; }
.lead-name { font-family: 'Poppins', Arial, sans-serif; font-size: 0.83rem; font-weight: 500; flex: 1; }
.lead-meta { font-size: 0.73rem; opacity: 0.55; }

/* Platform badge */
.badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 20px;
    font-family: 'Poppins', Arial, sans-serif;
    font-size: 0.68rem; font-weight: 600;
    letter-spacing: 0.04em;
}
.badge-ig  { background: rgba(217,71,151,0.15); color: var(--pink); }
.badge-tt  { background: rgba(0,0,0,0.08); color: #555; }
.badge-wa  { background: rgba(37,211,102,0.12); color: #1a8a45; }
.badge-fb  { background: rgba(66,103,178,0.12); color: #4267b2; }
.badge-def { background: rgba(128,128,128,0.12); color: #666; }

/* ── Inputs ── */
input:focus, textarea:focus,
div[data-baseweb="input"]:focus-within,
div[data-baseweb="textarea"]:focus-within {
    border-color: var(--pink) !important;
    box-shadow: 0 0 0 2px rgba(217,71,151,0.18) !important;
}
input, textarea,
div[data-baseweb="input"] input,
div[data-baseweb="textarea"] textarea {
    border-radius: 8px !important;
    font-family: 'Lora', Georgia, serif !important;
}

/* ── Primary button ── */
button[kind="primary"] {
    background: linear-gradient(135deg, var(--pink), var(--purple)) !important;
    border: none !important; border-radius: 8px !important;
    color: #fff !important;
    font-family: 'Poppins', Arial, sans-serif !important;
    font-weight: 600 !important; font-size: 0.85rem !important;
    box-shadow: 0 3px 10px rgba(217,71,151,0.3) !important;
}
button[kind="primary"]:hover { opacity: 0.88 !important; }

/* ── Tabs ── */
div[data-baseweb="tab-list"] { background: transparent !important; }
div[data-baseweb="tab"] {
    font-family: 'Poppins', Arial, sans-serif !important;
    font-size: 0.84rem !important; font-weight: 500 !important;
    border-radius: 8px 8px 0 0 !important;
    padding: 0.5rem 1.1rem !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
}
div[aria-selected="true"][data-baseweb="tab"] {
    color: var(--pink) !important;
    border-bottom-color: var(--pink) !important;
}

/* ── Expanders ── */
div[data-testid="stExpander"] {
    background: rgba(128,128,128,0.05) !important;
    border: 1px solid rgba(128,128,128,0.18) !important;
    border-radius: 12px !important;
    margin-bottom: 0.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
div[data-testid="stExpander"] summary {
    font-family: 'Poppins', Arial, sans-serif !important;
    font-size: 0.87rem !important;
}

/* ── Alerts ── */
div[data-testid="stAlert"] { border-radius: 10px !important; font-family: 'Lora', Georgia, serif !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: rgba(128,128,128,0.3); border-radius: 4px; }

/* Push content down so page title isn't clipped */
.block-container { padding-top: 3.5rem !important; }

/* ── Replace sidebar toggle » with Material Icon ── */
[data-testid="stSidebarCollapseButton"] button,
[data-testid="collapsedControl"] button {
    position: relative !important;
    color: transparent !important;
    font-size: 0 !important;
}
[data-testid="stSidebarCollapseButton"] button > *,
[data-testid="collapsedControl"] button > * { display: none !important; }
[data-testid="stSidebarCollapseButton"] button::after {
    font-family: 'Material Icons' !important;
    content: "keyboard_double_arrow_left" !important;
    font-size: 1.3rem !important;
    color: var(--midgray) !important;
    position: absolute !important;
    top: 50% !important; left: 50% !important;
    transform: translate(-50%, -50%) !important;
}
[data-testid="collapsedControl"] button::after {
    font-family: 'Material Icons' !important;
    content: "keyboard_double_arrow_right" !important;
    font-size: 1.3rem !important;
    color: var(--midgray) !important;
    position: absolute !important;
    top: 50% !important; left: 50% !important;
    transform: translate(-50%, -50%) !important;
}

/* ── Sidebar nav icons via Material Icons ── */
section[data-testid="stSidebar"] [data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    padding: 0.55rem 0.9rem !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: background 0.15s, color 0.15s !important;
    color: rgba(255,255,255,0.65) !important;
    margin: 1px 0 !important;
}
section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,0.07) !important;
    color: #fff !important;
}
section[data-testid="stSidebar"] [data-testid="stRadio"] label::before {
    font-family: 'Material Icons' !important;
    font-size: 1.15rem !important;
    line-height: 1 !important;
    margin-right: 0.25rem !important;
    flex-shrink: 0 !important;
}
/* Hide the empty radio group label (nth-of-type 1 = collapsed group title) */
section[data-testid="stSidebar"] [data-testid="stRadio"] label:nth-of-type(1) { display: none !important; }
section[data-testid="stSidebar"] [data-testid="stRadio"] label:nth-of-type(2)::before { content: "dashboard"; }
section[data-testid="stSidebar"] [data-testid="stRadio"] label:nth-of-type(3)::before { content: "auto_awesome"; }
section[data-testid="stSidebar"] [data-testid="stRadio"] label:nth-of-type(4)::before { content: "people"; }
section[data-testid="stSidebar"] [data-testid="stRadio"] label:nth-of-type(5)::before { content: "flag"; }
section[data-testid="stSidebar"] [data-testid="stRadio"] label:nth-of-type(6)::before { content: "calendar_month"; }
section[data-testid="stSidebar"] [data-testid="stRadio"] label:nth-of-type(7)::before { content: "description"; }
/* Hide radio dot */
section[data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────
st.sidebar.markdown(f"""
<div class="sidebar-brand">
    <img src="data:image/png;base64,{LOGO_B64}" alt="Ivycandy Hair">
    <h1>Ivycandy Hair Hub</h1>
    <span>Business Dashboard</span>
</div>
""", unsafe_allow_html=True)

NAV_PAGES = [
    "Dashboard",
    "AI Reply Assistant",
    "Client Registry",
    "Lead Tracker",
    "Content Calendar",
    "Sales Scripts",
]

page = st.sidebar.radio(
    "",
    NAV_PAGES,
    label_visibility="collapsed",
)

# ── Helpers ────────────────────────────────────────────────
def page_header(icon, title, caption=""):
    st.markdown(f"""
    <div class="page-header">
        <h1>{icon} {title}</h1>
    </div>
    """, unsafe_allow_html=True)
    if caption:
        st.markdown(f'<p class="page-caption">{caption}</p>', unsafe_allow_html=True)

def platform_badge(platform):
    mapping = {
        "Instagram": ("IG", "badge-ig"),
        "TikTok": ("TT", "badge-tt"),
        "WhatsApp": ("WA", "badge-wa"),
        "Facebook": ("FB", "badge-fb"),
    }
    label, cls = mapping.get(platform, (platform[:2].upper(), "badge-def"))
    return f'<span class="badge {cls}">{label}</span>'

# ═══════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ═══════════════════════════════════════════════════════════
if page == "Dashboard":
    # ── Greeting ──
    today = date.today()
    hour = __import__("datetime").datetime.now().hour
    greeting = "Good morning" if hour < 12 else ("Good afternoon" if hour < 17 else "Good evening")
    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
        <h1 style="font-family:Poppins,Arial,sans-serif;font-weight:700;font-size:1.6rem;margin:0;">{greeting} 👋</h1>
        <p style="opacity:0.5;font-size:0.85rem;margin-top:0.25rem;">{today.strftime("%A, %d %B %Y")} &nbsp;·&nbsp; Ivycandy Hair Hub</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Stat widgets ──
    all_clients = db.get_all_clients()
    all_leads   = db.get_leads()
    overdue     = [l for l in all_leads if l['follow_up_on'] and l['follow_up_on'] <= str(today) and l['status'] == 'new']
    new_leads   = [l for l in all_leads if l['status'] == 'new']
    posts_today = db.get_posts(str(today))

    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-widget" style="--accent:#d94797;">
            <div class="stat-label">Total Clients</div>
            <div class="stat-value">{len(all_clients)}</div>
            <div class="stat-sub">in your registry</div>
        </div>
        <div class="stat-widget" style="--accent:#966acc;">
            <div class="stat-label">Active Leads</div>
            <div class="stat-value">{len(new_leads)}</div>
            <div class="stat-sub">awaiting follow-up</div>
        </div>
        <div class="stat-widget" style="--accent:{'#e74c3c' if overdue else '#27ae60'};">
            <div class="stat-label">Overdue Follow-ups</div>
            <div class="stat-value">{len(overdue)}</div>
            <div class="stat-sub">{'action needed' if overdue else 'all clear'}</div>
        </div>
        <div class="stat-widget" style="--accent:#4e6b86;">
            <div class="stat-label">Posts Today</div>
            <div class="stat-value">{len(posts_today)}</div>
            <div class="stat-sub">planned for {today.strftime("%d %b")}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Main grid: Hero (AI Reply) + Leads panel ──
    col_main, col_side = st.columns([2, 1], gap="large")

    with col_main:
        # Hero — Quick Reply
        st.markdown('<div class="section-header"><h3>Quick AI Reply</h3><span class="see-more">✨ Most used feature</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><div class="card-label">Paste customer message → copy reply into WhatsApp</div>', unsafe_allow_html=True)
        dash_msg = st.text_area("dash_msg", placeholder='e.g. "Do you have 26" body wave in stock?"', height=100, label_visibility="collapsed")
        if st.button("Generate Reply", type="primary", use_container_width=True, key="dash_reply_btn"):
            if dash_msg.strip():
                with st.spinner("Writing..."):
                    try:
                        r = ai_reply.generate_reply(dash_msg)
                        st.session_state["dash_reply"] = r
                    except Exception as e:
                        st.error(str(e))
        if "dash_reply" in st.session_state:
            st.text_area("", value=st.session_state["dash_reply"], height=140, key="dash_reply_out")
            st.button("Clear", key="dash_clear", on_click=lambda: st.session_state.pop("dash_reply", None))
        st.markdown('</div>', unsafe_allow_html=True)

        # Recent clients grid
        st.markdown('<div class="section-header" style="margin-top:1rem;"><h3>Recent Clients</h3></div>', unsafe_allow_html=True)
        recent_clients = list(reversed(all_clients))[:6]
        if not recent_clients:
            st.info("No clients yet — add your first in Client Registry.")
        else:
            g1, g2, g3 = st.columns(3)
            cols = [g1, g2, g3]
            for i, c in enumerate(recent_clients):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="card" style="padding:0.9rem 1rem;margin-bottom:0.6rem;">
                        <div style="font-family:Poppins,Arial,sans-serif;font-size:0.85rem;font-weight:600;margin-bottom:0.25rem;">{c['name']}</div>
                        <div style="font-size:0.75rem;opacity:0.55;">{c['platform'] or '—'} &nbsp;·&nbsp; {c['style_pref'] or 'No pref'}</div>
                        <div style="font-size:0.72rem;opacity:0.4;margin-top:0.2rem;">Last: {c['last_contact'] or 'never'}</div>
                    </div>
                    """, unsafe_allow_html=True)

    with col_side:
        # Overdue leads widget
        st.markdown('<div class="section-header"><h3>Leads to Follow Up</h3></div>', unsafe_allow_html=True)
        st.markdown('<div class="card" style="padding:0.9rem 1.1rem;">', unsafe_allow_html=True)
        display_leads = (overdue + [l for l in new_leads if l not in overdue])[:8]
        if not display_leads:
            st.markdown('<p style="font-size:0.82rem;opacity:0.5;margin:0;">No active leads — add some in Lead Tracker.</p>', unsafe_allow_html=True)
        else:
            for l in display_leads:
                is_overdue = l in overdue
                dot_cls = "overdue" if is_overdue else l['status']
                st.markdown(f"""
                <div class="lead-row">
                    <div class="lead-dot {dot_cls}"></div>
                    <div class="lead-name">{l['name']}<br>
                        <span class="lead-meta">{l['follow_up_on'] or '—'}</span>
                    </div>
                    {platform_badge(l['platform'])}
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Today's content widget
        st.markdown('<div class="section-header" style="margin-top:1rem;"><h3>Today\'s Posts</h3></div>', unsafe_allow_html=True)
        st.markdown('<div class="card" style="padding:0.9rem 1.1rem;">', unsafe_allow_html=True)
        if not posts_today:
            st.markdown('<p style="font-size:0.82rem;opacity:0.5;margin:0;">Nothing planned for today.</p>', unsafe_allow_html=True)
        else:
            for p in posts_today:
                status_color = {"draft": "#e67e22", "scheduled": "#3498db", "posted": "#27ae60"}.get(p['status'], "#999")
                st.markdown(f"""
                <div class="lead-row">
                    <div class="lead-dot" style="background:{status_color};"></div>
                    <div class="lead-name">{p['platform']}<br>
                        <span class="lead-meta">{p['status'].upper()}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE: AI REPLY ASSISTANT
# ═══════════════════════════════════════════════════════════
elif page == "AI Reply Assistant":
    page_header("✨", "AI Reply Assistant", "Paste a customer's message — get a ready-to-send WhatsApp reply instantly.")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="card"><div class="card-label">Customer Message</div>', unsafe_allow_html=True)
        customer_msg = st.text_area("customer_msg_input", placeholder='e.g. Do you have straight human hair bundles in 24 inches? How much?', height=160, label_visibility="collapsed")
        context = st.text_input("Extra context (optional)", placeholder='e.g. Returning customer, bought 22" bundles before')
        generate_btn = st.button("Generate Reply", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><div class="card-label">Generated Reply — Copy & Paste into WhatsApp</div>', unsafe_allow_html=True)
        if generate_btn:
            if not customer_msg.strip():
                st.warning("Paste the customer's message first.")
            else:
                with st.spinner("Writing reply..."):
                    try:
                        reply = ai_reply.generate_reply(customer_msg, context)
                        st.session_state["last_reply"] = reply
                    except Exception as e:
                        st.error(f"API error: {e}")
        if "last_reply" in st.session_state:
            st.text_area("", value=st.session_state["last_reply"], height=240, key="reply_output")
            st.button("Clear", on_click=lambda: st.session_state.pop("last_reply", None))
        else:
            st.markdown('<p style="font-size:0.85rem;opacity:0.45;margin-top:0.5rem;">Your reply will appear here...</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE: CLIENT REGISTRY
# ═══════════════════════════════════════════════════════════
elif page == "Client Registry":
    page_header("👥", "Client Registry")

    tab_list, tab_add, tab_orders = st.tabs(["All Clients", "Add Client", "Order History"])

    with tab_list:
        search = st.text_input("Search by name, contact, or platform", "")
        clients = db.search_clients(search) if search else db.get_all_clients()
        if not clients:
            st.info("No clients yet. Add your first one in the 'Add Client' tab.")
        else:
            for c in clients:
                with st.expander(f"**{c['name']}** — {c['platform'] or '—'}  |  Last contact: {c['last_contact'] or 'never'}"):
                    col1, col2, col3 = st.columns(3)
                    col1.markdown(f"**Contact:** {c['contact'] or '—'}")
                    col2.markdown(f"**Platform:** {c['platform'] or '—'}")
                    col3.markdown(f"**Style pref:** {c['style_pref'] or '—'}")
                    if c['notes']:
                        st.markdown(f"**Notes:** {c['notes']}")
                    if st.button("Delete", key=f"del_{c['id']}"):
                        db.delete_client(c['id'])
                        st.rerun()

    with tab_add:
        with st.form("add_client_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            name = c1.text_input("Full name *")
            platform = c2.selectbox("Platform", ["WhatsApp", "Instagram", "TikTok", "Facebook", "Other"])
            contact = c1.text_input("Contact (phone / @handle)")
            style_pref = c2.text_input("Style preference", placeholder='e.g. 24" straight, dark brown')
            last_contact = st.date_input("Last contact date", value=date.today())
            notes = st.text_area("Notes", placeholder="Anything else useful...")
            submitted = st.form_submit_button("Save Client", type="primary")
        if submitted:
            if not name.strip():
                st.error("Name is required.")
            else:
                db.add_client(name, platform, contact, style_pref, notes, str(last_contact))
                st.success(f"'{name}' added to registry.")

    with tab_orders:
        clients_all = db.get_all_clients()
        if not clients_all:
            st.info("Add clients first.")
        else:
            names = {c['id']: c['name'] for c in clients_all}
            selected_id = st.selectbox("Select client", options=list(names.keys()), format_func=lambda x: names[x])
            orders = db.get_orders_for_client(selected_id)
            with st.form("add_order_form", clear_on_submit=True):
                st.markdown('<div class="card-label">Log a new order</div>', unsafe_allow_html=True)
                oc1, oc2 = st.columns(2)
                item = oc1.text_input("Item", placeholder='e.g. 24" straight bundle x2')
                amount = oc2.number_input("Amount (€)", min_value=0.0, step=5.0)
                order_date = st.date_input("Order date", value=date.today())
                o_notes = st.text_input("Notes (optional)")
                o_submitted = st.form_submit_button("Add Order", type="primary")
            if o_submitted and item:
                db.add_order(selected_id, item, amount, str(order_date), o_notes)
                st.success("Order logged.")
                st.rerun()
            if orders:
                st.markdown("---")
                total = sum(o['amount'] or 0 for o in orders)
                st.markdown(f'<div class="card-label">Order history — <strong>Total: €{total:.2f}</strong></div>', unsafe_allow_html=True)
                for o in orders:
                    st.markdown(f"- `{o['order_date']}` — {o['item']}  **€{o['amount']:.2f}**  {o['notes'] or ''}")
            else:
                st.info("No orders logged yet.")

# ═══════════════════════════════════════════════════════════
# PAGE: LEAD TRACKER
# ═══════════════════════════════════════════════════════════
elif page == "Lead Tracker":
    page_header("🎯", "Lead Tracker", "Log social media leads — auto follow-up reminder in 3 days.")

    tab_new, tab_all = st.tabs(["Add Lead", "All Leads"])

    with tab_new:
        with st.form("add_lead_form", clear_on_submit=True):
            lc1, lc2 = st.columns(2)
            l_name = lc1.text_input("Name / handle")
            l_platform = lc2.selectbox("Platform", ["Instagram", "TikTok", "WhatsApp", "Facebook", "Other"])
            l_inquiry = st.text_area("What did they ask / express interest in?")
            l_followup = st.date_input("Follow-up reminder date", value=date.today() + timedelta(days=3))
            l_submit = st.form_submit_button("Save Lead", type="primary")
        if l_submit and l_name:
            db.add_lead(l_name, l_platform, l_inquiry, str(l_followup))
            st.success("Lead saved. Reminder set.")

    with tab_all:
        filter_status = st.selectbox("Filter by status", ["all", "new", "contacted", "converted", "lost"])
        leads = db.get_leads(None if filter_status == "all" else filter_status)
        today_str = str(date.today())
        overdue = [l for l in leads if l['follow_up_on'] and l['follow_up_on'] <= today_str and l['status'] == 'new']
        if overdue:
            st.error(f"⚠️ {len(overdue)} lead(s) need follow-up today or are overdue!")
        if not leads:
            st.info("No leads yet.")
        else:
            for l in leads:
                flag = "🔴 " if l['follow_up_on'] and l['follow_up_on'] <= today_str and l['status'] == 'new' else ""
                with st.expander(f"{flag}**{l['name']}** ({l['platform']}) — Follow up: {l['follow_up_on']} | {l['status'].upper()}"):
                    st.markdown(f"**Inquiry:** {l['inquiry'] or '—'}")
                    new_status = st.selectbox("Update status", ["new", "contacted", "converted", "lost"],
                        index=["new", "contacted", "converted", "lost"].index(l['status']), key=f"lead_status_{l['id']}")
                    if st.button("Save status", key=f"save_lead_{l['id']}"):
                        db.update_lead_status(l['id'], new_status)
                        st.rerun()

# ═══════════════════════════════════════════════════════════
# PAGE: CONTENT CALENDAR
# ═══════════════════════════════════════════════════════════
elif page == "Content Calendar":
    page_header("📅", "Content Calendar")

    tab_add_post, tab_view = st.tabs(["Plan a Post", "View Schedule"])

    with tab_add_post:
        with st.form("add_post_form", clear_on_submit=True):
            pc1, pc2 = st.columns(2)
            post_date = pc1.date_input("Post date", value=date.today())
            post_platform = pc2.selectbox("Platform", ["Instagram", "TikTok", "Facebook", "LinkedIn", "All"])
            caption = st.text_area("Caption / script", height=200, placeholder="Write your caption here...")
            p_submit = st.form_submit_button("Add to Calendar", type="primary")
        if p_submit and caption:
            db.add_post(str(post_date), post_platform, caption)
            st.success("Post added to calendar.")
        st.markdown('<div class="card" style="margin-top:1rem"><div class="card-label">Pro Tip</div>Need a caption? Go to AI Reply Assistant and paste a prompt like: <em>"Write me a TikTok caption for a 24\" straight wig reveal"</em></div>', unsafe_allow_html=True)

    with tab_view:
        filter_date = st.date_input("View posts for date", value=date.today())
        posts = db.get_posts(str(filter_date))
        if not posts:
            st.info(f"No posts planned for {filter_date}.")
        else:
            for p in posts:
                with st.expander(f"**{p['platform']}** — {p['status'].upper()}"):
                    st.text_area("Caption", value=p['caption'], height=150, key=f"post_{p['id']}")
                    new_status = st.selectbox("Status", ["draft", "scheduled", "posted"],
                        index=["draft", "scheduled", "posted"].index(p['status']), key=f"post_status_{p['id']}")
                    if st.button("Update", key=f"update_post_{p['id']}"):
                        db.update_post_status(p['id'], new_status)
                        st.rerun()

# ═══════════════════════════════════════════════════════════
# PAGE: SALES SCRIPTS
# ═══════════════════════════════════════════════════════════
elif page == "Sales Scripts":
    page_header("💬", "Sales Scripts", "Generate ready-to-use scripts for common sales situations.")

    script_options = {
        "Cold lead — new follower, hasn't messaged": "cold_lead",
        "Returning customer — 6+ months inactive": "returning_customer",
        "Pricing inquiry": "pricing_inquiry",
    }
    selected_label = st.selectbox("Choose a script type", list(script_options.keys()))
    if st.button("Generate Script", type="primary"):
        with st.spinner("Writing script..."):
            try:
                script = ai_reply.generate_sales_script(script_options[selected_label])
                st.session_state["last_script"] = script
            except Exception as e:
                st.error(f"API error: {e}")
    if "last_script" in st.session_state:
        st.markdown('<div class="card"><div class="card-label">Your Script</div>', unsafe_allow_html=True)
        st.text_area("", value=st.session_state["last_script"], height=300, key="script_out")
        st.markdown('</div>', unsafe_allow_html=True)

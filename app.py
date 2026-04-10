import streamlit as st
from datetime import date, timedelta
import base64, os
import db
import ai_reply

# ── Page config ───────────────────────────────────────────
st.set_page_config(
    page_title="Ivycandy Hair Hub",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

db.init_db()

# ── Load logo as base64 ───────────────────────────────────
def _img_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

LOGO_B64 = _img_b64(os.path.join(os.path.dirname(__file__), "assets", "logo.png"))

# ── Brand CSS ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Lora:ital,wght@0,400;0,500;1,400&display=swap');

/* ── Brand tokens ── */
:root {
    --pink:    #d94797;
    --purple:  #966acc;
    --light:   #f5f0f0;
    --midgray: #b7a7a7;
    --border:  #3d3030;
}

/* ── Fonts only — no color overrides on global elements ── */
html, body, [class*="css"] { font-family: 'Lora', Georgia, serif; }
h1, h2, h3 { font-family: 'Poppins', Arial, sans-serif !important; font-weight: 700 !important; }

/* ── Sidebar — always dark ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2a1f1f 0%, #1a1414 100%) !important;
    border-right: 1px solid var(--border);
    padding-top: 0 !important;
}
section[data-testid="stSidebar"] .block-container { padding-top: 1rem; }
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

/* Sidebar brand block */
.sidebar-brand {
    display: flex; flex-direction: column; align-items: center;
    padding: 1.5rem 1rem 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1rem;
}
.sidebar-brand img {
    width: 110px; border-radius: 50%;
    border: 2px solid var(--pink);
    margin-bottom: 0.6rem; object-fit: cover;
}
.sidebar-brand h1 {
    font-family: 'Poppins', Arial, sans-serif;
    font-size: 1.05rem; font-weight: 700;
    color: var(--light); margin: 0;
    letter-spacing: 0.03em; text-align: center;
}
.sidebar-brand span {
    font-size: 0.7rem; color: var(--pink);
    letter-spacing: 0.12em; text-transform: uppercase; margin-top: 2px;
}

/* ── Page header ── */
.page-header {
    display: flex; align-items: center; gap: 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(128,128,128,0.25);
    margin-bottom: 1.5rem;
}
.page-header .icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, var(--pink), var(--purple));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
}
.page-header h1 { margin: 0 !important; padding: 0 !important; font-size: 1.9rem !important; }
.page-caption {
    font-size: 0.85rem; opacity: 0.6;
    margin-top: -1rem; margin-bottom: 1.5rem;
}

/* ── Cards — transparent so they adapt to either theme ── */
.card {
    background: rgba(128,128,128,0.07) !important;
    border: 1px solid rgba(128,128,128,0.2) !important;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.card-label {
    font-family: 'Poppins', Arial, sans-serif;
    font-size: 0.7rem; letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--pink) !important;
    margin-bottom: 0.5rem;
}

/* ── Inputs — only border + focus, no background/color override ── */
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

/* ── Primary button — gradient ── */
button[kind="primary"] {
    background: linear-gradient(135deg, var(--pink), var(--purple)) !important;
    border: none !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-family: 'Poppins', Arial, sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}
button[kind="primary"]:hover { opacity: 0.88 !important; }

/* ── Tabs — active accent only ── */
div[data-baseweb="tab-list"] { background: transparent !important; gap: 0.25rem; }
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
    background: transparent !important;
}

/* ── Expanders — transparent so theme shows through ── */
div[data-testid="stExpander"] {
    background: rgba(128,128,128,0.06) !important;
    border: 1px solid rgba(128,128,128,0.2) !important;
    border-radius: 10px !important;
    margin-bottom: 0.5rem;
}
div[data-testid="stExpander"] summary {
    font-family: 'Poppins', Arial, sans-serif !important;
    font-size: 0.88rem !important;
}

/* ── Alerts ── */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: 'Lora', Georgia, serif !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: rgba(128,128,128,0.3); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar brand block ────────────────────────────────────
st.sidebar.markdown(f"""
<div class="sidebar-brand">
    <img src="data:image/png;base64,{LOGO_B64}" alt="Ivycandy Hair">
    <h1>Ivycandy Hair Hub</h1>
    <span>Business Dashboard</span>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "",
    ["AI Reply Assistant", "Client Registry", "Lead Tracker", "Content Calendar", "Sales Scripts"],
    label_visibility="collapsed",
)

# ── Helper: page header ───────────────────────────────────
def page_header(icon, title, caption=""):
    st.markdown(f"""
    <div class="page-header">
        <div class="icon">{icon}</div>
        <h1 style="font-family:Poppins,Arial,sans-serif;font-weight:700;font-size:1.9rem;margin:0;">{title}</h1>
    </div>
    """, unsafe_allow_html=True)
    if caption:
        st.markdown(f'<p class="page-caption">{caption}</p>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# PAGE: AI REPLY ASSISTANT
# ═══════════════════════════════════════════════════════════
if page == "AI Reply Assistant":
    page_header("✨", "AI Reply Assistant", "Paste a customer's message — get a ready-to-send WhatsApp reply instantly.")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="card"><div class="card-label">Customer Message</div>', unsafe_allow_html=True)
        customer_msg = st.text_area(
            "customer_msg_input",
            placeholder="e.g. Do you have straight human hair bundles in 24 inches? How much?",
            height=150,
            label_visibility="collapsed",
        )
        context = st.text_input(
            "Extra context (optional)",
            placeholder="e.g. Returning customer, bought 22\" bundles before",
        )
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
            st.text_area("", value=st.session_state["last_reply"], height=220, key="reply_output")
            st.button("Clear", on_click=lambda: st.session_state.pop("last_reply", None))
        else:
            st.markdown('<p style="color:var(--midgray);font-size:0.85rem;margin-top:0.5rem;">Your reply will appear here...</p>', unsafe_allow_html=True)
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
                st.markdown(f'<div class="card-label">Order history — <span style="color:var(--light);font-size:1rem;font-family:Poppins,Arial,sans-serif;">Total: €{total:.2f}</span></div>', unsafe_allow_html=True)
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

        today = str(date.today())
        overdue = [l for l in leads if l['follow_up_on'] and l['follow_up_on'] <= today and l['status'] == 'new']
        if overdue:
            st.error(f"⚠️ {len(overdue)} lead(s) need follow-up today or are overdue!")

        if not leads:
            st.info("No leads yet.")
        else:
            for l in leads:
                flag = "🔴 " if l['follow_up_on'] and l['follow_up_on'] <= today and l['status'] == 'new' else ""
                with st.expander(f"{flag}**{l['name']}** ({l['platform']}) — Follow up: {l['follow_up_on']} | {l['status'].upper()}"):
                    st.markdown(f"**Inquiry:** {l['inquiry'] or '—'}")
                    new_status = st.selectbox(
                        "Update status",
                        ["new", "contacted", "converted", "lost"],
                        index=["new", "contacted", "converted", "lost"].index(l['status']),
                        key=f"lead_status_{l['id']}",
                    )
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

        st.markdown('<div class="card" style="margin-top:1rem"><div class="card-label">Pro Tip</div>Need a caption? Use the AI Reply Assistant — paste a prompt like: <em>"Write me a TikTok caption for a 24\" straight wig reveal"</em></div>', unsafe_allow_html=True)

    with tab_view:
        filter_date = st.date_input("View posts for date", value=date.today())
        posts = db.get_posts(str(filter_date))

        if not posts:
            st.info(f"No posts planned for {filter_date}.")
        else:
            for p in posts:
                with st.expander(f"**{p['platform']}** — {p['status'].upper()}"):
                    st.text_area("Caption", value=p['caption'], height=150, key=f"post_{p['id']}")
                    new_status = st.selectbox(
                        "Status",
                        ["draft", "scheduled", "posted"],
                        index=["draft", "scheduled", "posted"].index(p['status']),
                        key=f"post_status_{p['id']}",
                    )
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
    script_key = script_options[selected_label]

    if st.button("Generate Script", type="primary"):
        with st.spinner("Writing script..."):
            try:
                script = ai_reply.generate_sales_script(script_key)
                st.session_state["last_script"] = script
            except Exception as e:
                st.error(f"API error: {e}")

    if "last_script" in st.session_state:
        st.markdown('<div class="card"><div class="card-label">Your Script</div>', unsafe_allow_html=True)
        st.text_area("", value=st.session_state["last_script"], height=300, key="script_out")
        st.markdown('</div>', unsafe_allow_html=True)

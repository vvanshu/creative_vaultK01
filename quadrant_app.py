import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

# -----------------------------------------------------------------------------
# CONSTANTS & CONFIG
# -----------------------------------------------------------------------------
DATA_FILE = "quadrant_data.json"

QUADRANT_INFO = {
    "Q1": {
        "title": "Q1: Do First",
        "subtitle": "Urgent & Important",
        "color": "#991b1b",
        "badge_bg": "#ffc4b3",
        "bg_class": "q1-bg",
        "desc": "Crises, tight college deadlines, urgent issues."
    },
    "Q2": {
        "title": "Q2: Schedule",
        "subtitle": "Important, Not Urgent",
        "color": "#1e40af",
        "badge_bg": "#b6d5ff",
        "bg_class": "q2-bg",
        "desc": "Vibecoding, Portfolio, Content, Networking, Exercise."
    },
    "Q3": {
        "title": "Q3: Delegate / Limit",
        "subtitle": "Urgent, Not Important",
        "color": "#854d0e",
        "badge_bg": "#ffe894",
        "bg_class": "q3-bg",
        "desc": "Interruptions, minor requests, low-impact tasks."
    },
    "Q4": {
        "title": "Q4: Eliminate",
        "subtitle": "Not Urgent & Not Important",
        "color": "#5b21b6",
        "badge_bg": "#d8c7ff",
        "bg_class": "q4-bg",
        "desc": "Mindless scrolling, busywork, time sinks."
    }
}

PRIORITY_BADGES = {
    "Critical": {"bg": "#ffcdd2", "text": "#900c3f"},
    "High": {"bg": "#ffe0b2", "text": "#7a2700"},
    "Medium": {"bg": "#fff9c4", "text": "#5d4037"},
    "Low": {"bg": "#c8e6c9", "text": "#1b5e20"}
}

ENERGY_ICONS = {
    "High Energy": "⚡ High Energy",
    "Medium Energy": "🔋 Medium Energy",
    "Low Energy": "🍃 Low Energy"
}

st.set_page_config(
    page_title="Quadrants - Neobrutalist Eisenhower Matrix",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# PERSISTENCE HELPERS
# -----------------------------------------------------------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                if "tasks" not in data: data["tasks"] = []
                if "weekly_audits" not in data: data["weekly_audits"] = []
                if "monthly_audits" not in data: data["monthly_audits"] = []
                if "vibecoding_streak" not in data: data["vibecoding_streak"] = 0
                return data
        except Exception:
            pass
    return {
        "tasks": [],
        "weekly_audits": [],
        "monthly_audits": [],
        "vibecoding_streak": 0
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

if "db" not in st.session_state:
    st.session_state.db = load_data()

# -----------------------------------------------------------------------------
# ULTRA HIGH-CONTRAST NEOBRUTALIST & SOFT PASTEL STYLING
# -----------------------------------------------------------------------------
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">

<style>
    /* Global Canvas Styling */
    .stApp {
        background-color: #f7f5ef;
        background-image: radial-gradient(#d3cbbe 1.5px, transparent 1.5px);
        background-size: 24px 24px;
        color: #000000 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2rem;
    }

    /* GLOBAL HIGH CONTRAST TYPOGRAPHY */
    h1, h2, h3, h4, h5, h6, p, label, span, div, small, caption, strong, summary {
        color: #000000 !important;
    }

    /* App Header Banner */
    .app-header-box {
        background: #ffffff;
        border: 3px solid #000000;
        box-shadow: 5px 5px 0px #000000;
        border-radius: 20px;
        padding: 1.2rem 1.8rem;
        margin-bottom: 1.8rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .app-title-text {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.3rem;
        font-weight: 700;
        color: #000000 !important;
        margin: 0;
        letter-spacing: -0.02em;
    }

    .app-sub-text {
        font-size: 1rem;
        color: #1a1a1a !important;
        font-weight: 700;
        margin-top: 0.2rem;
    }

    /* Neobrutalist Stat Cards */
    .stat-card-neo {
        border: 2.5px solid #000000;
        box-shadow: 4px 4px 0px #000000;
        border-radius: 18px;
        padding: 1.1rem 1rem;
        text-align: center;
        transition: transform 0.15s ease;
    }
    .stat-card-neo:hover {
        transform: translate(-2px, -2px);
        box-shadow: 6px 6px 0px #000000;
    }
    .stat-val-neo {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #000000 !important;
        line-height: 1;
    }
    .stat-lbl-neo {
        font-size: 0.82rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
        color: #000000 !important;
    }

    /* Quadrant Container Headers */
    .q-box-neo {
        border: 2.5px solid #000000;
        box-shadow: 4px 4px 0px #000000;
        border-radius: 20px 20px 0 0;
        padding: 1.1rem 1.3rem;
        margin-bottom: 0px;
    }

    .q1-bg { background-color: #ffdcd3; }
    .q2-bg { background-color: #d6e8ff; }
    .q3-bg { background-color: #fff2b2; }
    .q4-bg { background-color: #e8dfff; }

    .q-title-neo {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.3rem;
        color: #000000 !important;
        margin: 0;
    }
    .q-desc-neo {
        font-size: 0.88rem;
        font-weight: 700;
        color: #1a1a1a !important;
        margin-top: 0.25rem;
    }

    /* Checkbox Label Contrast Override */
    div[data-testid="stCheckbox"] label p {
        color: #000000 !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
    }

    /* Bubbly Badges */
    .badge-neo {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 50px;
        font-size: 0.78rem;
        font-weight: 800;
        border: 1.8px solid #000000;
        margin-right: 0.35rem;
        margin-top: 0.25rem;
        box-shadow: 1px 1px 0px #000000;
        color: #000000 !important;
    }

    /* High Contrast Input Overrides */
    input, textarea, select, div[data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border: 2px solid #000000 !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] * {
        color: #000000 !important;
        font-weight: 700 !important;
    }

    /* Streamlit Native Buttons */
    .stButton > button {
        border: 2.5px solid #000000 !important;
        box-shadow: 3.5px 3.5px 0px #000000 !important;
        border-radius: 14px !important;
        font-weight: 800 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        transition: all 0.15s ease !important;
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    .stButton > button:hover {
        transform: translate(-2px, -2px) !important;
        box-shadow: 5px 5px 0px #000000 !important;
        background-color: #fff9e6 !important;
        color: #000000 !important;
    }

    button[kind="primary"] {
        background-color: #b2f2bb !important;
        color: #000000 !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #eee9dc !important;
        border-right: 3px solid #000000 !important;
    }
    section[data-testid="stSidebar"] * {
        color: #000000 !important;
    }

    div[data-testid="stForm"] {
        background: #ffffff !important;
        border: 3px solid #000000 !important;
        box-shadow: 4px 4px 0px #000000 !important;
        border-radius: 20px !important;
        padding: 1.25rem !important;
    }

    /* Popover High Contrast */
    div[data-testid="stPopoverBody"] {
        background-color: #ffffff !important;
        border: 3px solid #000000 !important;
        box-shadow: 5px 5px 0px #000000 !important;
        border-radius: 16px !important;
    }
    div[data-testid="stPopoverBody"] * {
        color: #000000 !important;
        font-weight: 700 !important;
    }

    /* Expander Contrast */
    div[data-testid="stExpander"] summary {
        background-color: #ffffff !important;
        border: 2px solid #000000 !important;
        border-radius: 12px !important;
    }
    div[data-testid="stExpander"] summary * {
        color: #000000 !important;
        font-weight: 800 !important;
    }

    /* Tabs Override */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #dfd8c8;
        padding: 8px;
        border-radius: 18px;
        border: 2.5px solid #000000;
        box-shadow: 3px 3px 0px #000000;
    }

    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 12px;
        color: #000000 !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 800;
        font-size: 0.95rem;
        padding: 0 20px;
        border: 2px solid transparent;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2.5px solid #000000 !important;
        box-shadow: 3px 3px 0px #000000 !important;
    }

    .streak-card-neo {
        background: #ffd8a8;
        border: 2.5px solid #000000;
        box-shadow: 4px 4px 0px #000000;
        border-radius: 18px;
        padding: 1.25rem;
        text-align: center;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# APP HEADER
# -----------------------------------------------------------------------------
st.markdown("""
<div class="app-header-box">
    <div>
        <h1 class="app-title-text">🎯 Quadrants App</h1>
        <div class="app-sub-text">Neobrutalist Eisenhower Matrix & Goal System</div>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR: QUICK TASK CREATION & STREAK TRACKER
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ Quick Task Entry")
    with st.form(key="add_task_form", clear_on_submit=True):
        task_title = st.text_input("Task Title", placeholder="e.g. Finish Framer Portfolio")
        quadrant = st.selectbox(
            "Quadrant", 
            ["Q2: Important, Not Urgent", "Q1: Urgent & Important", "Q3: Urgent, Not Important", "Q4: Neither"]
        )
        q_code = quadrant.split(":")[0]
        
        category = st.selectbox("Category", ["Vibecoding", "Portfolio", "Content/Insta", "College", "Career/Networking", "General"])
        est_time = st.number_input("Estimated Time (mins)", min_value=15, max_value=480, value=60, step=15)
        priority = st.select_slider("Priority Level", options=["Low", "Medium", "High", "Critical"], value="Medium")
        energy = st.radio("Required Energy", ["High Energy", "Medium Energy", "Low Energy"], index=1, horizontal=True)
        
        submit = st.form_submit_button("➕ Add Task to System", use_container_width=True, type="primary")
        
        if submit:
            if not task_title.strip():
                st.error("Please enter a valid task title.")
            else:
                new_task = {
                    "id": str(datetime.now().timestamp()),
                    "title": task_title.strip(),
                    "quadrant": q_code,
                    "category": category,
                    "est_time": int(est_time),
                    "priority": priority,
                    "energy": energy,
                    "completed": False,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.db["tasks"].append(new_task)
                save_data(st.session_state.db)
                st.toast(f"✅ Added task to {q_code}!", icon="🎯")
                st.rerun()

    st.markdown("---")
    
    # Vibecoding Streak Box
    streak = st.session_state.db.get("vibecoding_streak", 0)
    st.markdown("### 🔥 30-Day Vibecoding Streak")
    
    st.markdown(f"""
    <div class="streak-card-neo">
        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 2.6rem; font-weight: 800; color: #000000; line-height: 1;">🔥 {streak}</div>
        <div style="font-size: 0.85rem; color: #000000; font-weight: 800; margin-top: 0.3rem; text-transform: uppercase;">Consecutive Days</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    col_s1, col_s2 = st.columns([1, 1])
    with col_s1:
        if st.button("+1 Day 🔥", use_container_width=True):
            st.session_state.db["vibecoding_streak"] = streak + 1
            save_data(st.session_state.db)
            st.toast("🔥 Streak updated!", icon="🎉")
            st.rerun()
    with col_s2:
        if st.button("Reset", use_container_width=True):
            st.session_state.db["vibecoding_streak"] = 0
            save_data(st.session_state.db)
            st.toast("Streak reset to 0.", icon="ℹ️")
            st.rerun()
            
    # Streak Milestone badges
    if streak >= 30:
        st.success("🏆 30-Day Vibecoding Master!")
    elif streak >= 14:
        st.info("🚀 14-Day Consistency Beast!")
    elif streak >= 7:
        st.warning("🌟 7-Day Momentum Builder!")

# -----------------------------------------------------------------------------
# MAIN NAVIGATION TABS
# -----------------------------------------------------------------------------
tab_matrix, tab_list, tab_audit = st.tabs(["🧩 4-Quadrant Matrix", "📋 Task List & Filters", "📊 Weekly & Monthly Audits"])

# -----------------------------------------------------------------------------
# TAB 1: 4-QUADRANT MATRIX
# -----------------------------------------------------------------------------
with tab_matrix:
    tasks = st.session_state.db.get("tasks", [])
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t.get("completed")])
    q2_tasks = [t for t in tasks if t.get("quadrant") == "Q2"]
    q2_ratio = int((len(q2_tasks) / total_tasks * 100)) if total_tasks > 0 else 0
    total_est_hours = round(sum(t.get("est_time", 0) for t in tasks if not t.get("completed")) / 60, 1)

    # Neobrutalist Stat Cards Grid
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f"""
        <div class="stat-card-neo" style="background-color: #d6e8ff;">
            <div class="stat-val-neo">{total_tasks}</div>
            <div class="stat-lbl-neo">Total Tasks</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="stat-card-neo" style="background-color: #b2f2bb;">
            <div class="stat-val-neo">{completed_tasks}</div>
            <div class="stat-lbl-neo">Completed</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
        <div class="stat-card-neo" style="background-color: #e8dfff;">
            <div class="stat-val-neo">{q2_ratio}%</div>
            <div class="stat-lbl-neo">Q2 Focus Ratio</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m4:
        st.markdown(f"""
        <div class="stat-card-neo" style="background-color: #fff2b2;">
            <div class="stat-val-neo">{total_est_hours}h</div>
            <div class="stat-lbl-neo">Pending Time</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_top1, col_top2 = st.columns(2)
    col_bot1, col_bot2 = st.columns(2)

    grid_mapping = [
        ("Q1", col_top1),
        ("Q2", col_top2),
        ("Q3", col_bot1),
        ("Q4", col_bot2)
    ]

    for q_code, col in grid_mapping:
        info = QUADRANT_INFO[q_code]
        q_tasks = [t for t in tasks if t.get("quadrant") == q_code]
        q_completed = len([t for t in q_tasks if t.get("completed")])
        q_total = len(q_tasks)

        with col:
            st.markdown(f"""
            <div class="q-box-neo {info['bg_class']}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 class="q-title-neo">{info['title']} <span style="font-size: 0.9rem; opacity: 0.85; color: #000000;">({info['subtitle']})</span></h4>
                    <span style="font-size: 0.88rem; font-weight: 800; color: #000000; background: #ffffff; border: 2px solid #000000; padding: 3px 12px; border-radius: 20px; box-shadow: 1px 1px 0px #000000;">{q_completed}/{q_total}</span>
                </div>
                <div class="q-desc-neo">{info['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if not q_tasks:
                st.caption("✨ No tasks in this quadrant.")
                st.markdown("<br>", unsafe_allow_html=True)
            else:
                for task in q_tasks:
                    is_done = task.get("completed", False)
                    p_badge = PRIORITY_BADGES.get(task.get("priority", "Medium"), {"bg": "#fff3bf", "text": "#5d4037"})
                    e_icon = ENERGY_ICONS.get(task.get("energy", "Medium Energy"), "🔋 Medium Energy")
                    
                    with st.container():
                        t_col1, t_col2 = st.columns([0.78, 0.22])
                        with t_col1:
                            cb_label = f"~~{task['title']}~~" if is_done else f"**{task['title']}**"
                            checked = st.checkbox(
                                f"{cb_label}", 
                                value=is_done, 
                                key=f"cb_{task['id']}"
                            )
                            if checked != is_done:
                                task["completed"] = checked
                                save_data(st.session_state.db)
                                st.rerun()
                                
                            st.markdown(f"""
                            <div style="margin-left: 28px; margin-top: -4px; margin-bottom: 8px;">
                                <span class="badge-neo" style="background-color: #ffffff; color: #000000;">{task.get('category')}</span>
                                <span class="badge-neo" style="background-color: #e2e8f0; color: #000000;">⏱️ {task.get('est_time')}m</span>
                                <span class="badge-neo" style="background-color: {p_badge['bg']}; color: {p_badge['text']};">{task.get('priority')}</span>
                                <span class="badge-neo" style="background-color: #ffffff; color: #000000;">{e_icon}</span>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        with t_col2:
                            pop_col1, pop_col2 = st.columns(2)
                            with pop_col1:
                                with st.popover("↔️"):
                                    st.markdown(f"**Move '{task['title']}'**")
                                    target_q = st.radio(
                                        "Select Quadrant:",
                                        ["Q1", "Q2", "Q3", "Q4"],
                                        index=["Q1", "Q2", "Q3", "Q4"].index(q_code),
                                        key=f"mov_rad_{task['id']}"
                                    )
                                    if st.button("Confirm Move", key=f"mov_btn_{task['id']}"):
                                        task["quadrant"] = target_q
                                        save_data(st.session_state.db)
                                        st.toast(f"Moved task to {target_q}")
                                        st.rerun()
                            with pop_col2:
                                if st.button("🗑️", key=f"del_{task['id']}"):
                                    st.session_state.db["tasks"] = [t for t in st.session_state.db["tasks"] if t["id"] != task["id"]]
                                    save_data(st.session_state.db)
                                    st.toast("Task deleted!")
                                    st.rerun()
                        st.markdown("<hr style='margin: 4px 0 10px 0; border-color: #000000; opacity: 0.2;'>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 2: TASK LIST & FILTERS
# -----------------------------------------------------------------------------
with tab_list:
    st.subheader("📋 Task Management & Advanced Filters")
    
    tasks = st.session_state.db.get("tasks", [])
    
    if not tasks:
        st.info("No tasks recorded yet. Add one from the sidebar quick task entry!")
    else:
        df = pd.DataFrame(tasks)
        
        # Search & Filter Controls
        f_col1, f_col2, f_col3, f_col4 = st.columns([2, 1, 1, 1])
        with f_col1:
            search_query = st.text_input("🔍 Search Tasks", placeholder="Search by title...")
        with f_col2:
            filter_q = st.multiselect("Quadrant", options=["Q1", "Q2", "Q3", "Q4"], default=["Q1", "Q2", "Q3", "Q4"])
        with f_col3:
            categories = list(df["category"].unique()) if "category" in df.columns else []
            filter_cat = st.multiselect("Category", options=categories, default=categories)
        with f_col4:
            status_filter = st.selectbox("Status", options=["All", "Active Only", "Completed Only"])

        # Filter Application
        filtered_df = df.copy()
        if search_query.strip():
            filtered_df = filtered_df[filtered_df["title"].str.contains(search_query, case=False, na=False)]
        if filter_q:
            filtered_df = filtered_df[filtered_df["quadrant"].isin(filter_q)]
        if filter_cat:
            filtered_df = filtered_df[filtered_df["category"].isin(filter_cat)]
        if status_filter == "Active Only":
            filtered_df = filtered_df[filtered_df["completed"] == False]
        elif status_filter == "Completed Only":
            filtered_df = filtered_df[filtered_df["completed"] == True]

        st.markdown(f"**Showing {len(filtered_df)} of {len(df)} Tasks**")

        # Interactive Data Table
        display_df = filtered_df[["completed", "quadrant", "title", "category", "est_time", "priority", "energy", "created_at"]].copy()
        display_df.columns = ["Completed", "Quadrant", "Title", "Category", "Est Mins", "Priority", "Energy", "Created At"]
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("<br>", unsafe_allow_html=True)
        btn_col1, btn_col2, btn_col3 = st.columns([1.5, 1.5, 3])
        with btn_col1:
            if st.button("🧹 Clear Completed Tasks", use_container_width=True):
                st.session_state.db["tasks"] = [t for t in tasks if not t.get("completed")]
                save_data(st.session_state.db)
                st.toast("Cleaned up completed tasks!")
                st.rerun()
        with btn_col2:
            json_str = json.dumps(st.session_state.db, indent=4)
            st.download_button(
                label="📥 Export System JSON",
                data=json_str,
                file_name=f"quadrants_backup_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )

# -----------------------------------------------------------------------------
# TAB 3: WEEKLY & MONTHLY AUDITS
# -----------------------------------------------------------------------------
with tab_audit:
    st.subheader("📊 Systems & Macro Audit")
    
    audit_type = st.radio("Audit Horizon", ["Weekly System Review", "Monthly Macro Goals Audit"], horizontal=True)
    
    if audit_type == "Weekly System Review":
        st.markdown("### 🗓️ Weekly System Check-In")
        with st.form("weekly_audit_form"):
            week_str = st.text_input("Week Horizon", value=datetime.now().strftime("Week %W, %Y"))
            q2_focus = st.text_area(
                "What Quadrant 2 goals did you move forward this week?", 
                placeholder="e.g. Completed portfolio layout, 7-day Vibecoding streak, 3 workouts..."
            )
            avoidance_check = st.text_area(
                "Did you complete your Saturday Avoidance Block (Research & Content Batching)?", 
                placeholder="e.g. Yes, batched 3 IG reels and researched Framer animations..."
            )
            energy_reflection = st.text_area(
                "Where did your system leak energy or time?", 
                placeholder="e.g. Late night scrolling on Tuesday, unnecessary Q3 context switches..."
            )
            
            submit_audit = st.form_submit_button("💾 Save Weekly Audit", type="primary")
            if submit_audit:
                st.session_state.db["weekly_audits"].append({
                    "id": str(datetime.now().timestamp()),
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "week": week_str,
                    "q2_focus": q2_focus,
                    "avoidance_check": avoidance_check,
                    "energy_reflection": energy_reflection
                })
                save_data(st.session_state.db)
                st.toast("Weekly Audit Saved Successfully!", icon="🎉")
                st.rerun()
                
        audits = st.session_state.db.get("weekly_audits", [])
        if audits:
            st.markdown("---")
            st.subheader("Past Weekly Audits")
            for wa in reversed(audits):
                with st.expander(f"📌 Audit: {wa.get('week')} ({wa.get('date')})"):
                    st.markdown(f"**🎯 Q2 Focus & Wins:**\n{wa.get('q2_focus') or 'None entered'}")
                    st.markdown(f"**🛡️ Avoidance Block:**\n{wa.get('avoidance_check') or 'None entered'}")
                    st.markdown(f"**⚡ Energy Leaks & Fixes:**\n{wa.get('energy_reflection') or 'None entered'}")

    else:
        st.markdown("### 🏆 Monthly Macro Goals Audit")
        
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            st.markdown("""
            <div class="stat-card-neo" style="background-color: #d6e8ff;">
                <div class="stat-val-neo">12 Posts</div>
                <div class="stat-lbl-neo">Instagram Goal (3/wk)</div>
            </div>
            """, unsafe_allow_html=True)
        with col_g2:
            st.markdown("""
            <div class="stat-card-neo" style="background-color: #b2f2bb;">
                <div class="stat-val-neo">1 Project</div>
                <div class="stat-lbl-neo">Portfolio Goal</div>
            </div>
            """, unsafe_allow_html=True)
        with col_g3:
            streak = st.session_state.db.get('vibecoding_streak', 0)
            st.markdown(f"""
            <div class="stat-card-neo" style="background-color: #ffd8a8;">
                <div class="stat-val-neo">{streak} / 30</div>
                <div class="stat-lbl-neo">Vibecoding Streak</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.form("monthly_audit_form"):
            month_str = st.text_input("Month Horizon", value=datetime.now().strftime("%B %Y"))
            goal_outcomes = st.text_area(
                "Monthly Outcomes Summary", 
                placeholder="e.g. Published 12 IG posts, finished Framer portfolio, hit 30-day streak..."
            )
            self_trust_score = st.slider("Self-Trust & Discipline Score (1-10)", 1, 10, 8)
            
            submit_m_audit = st.form_submit_button("💾 Save Monthly Audit", type="primary")
            if submit_m_audit:
                st.session_state.db["monthly_audits"].append({
                    "id": str(datetime.now().timestamp()),
                    "month": month_str,
                    "outcomes": goal_outcomes,
                    "self_trust_score": self_trust_score,
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
                save_data(st.session_state.db)
                st.toast("Monthly Audit Saved Successfully!", icon="🏆")
                st.rerun()

        m_audits = st.session_state.db.get("monthly_audits", [])
        if m_audits:
            st.markdown("---")
            st.subheader("Past Monthly Audits")
            for ma in reversed(m_audits):
                with st.expander(f"🌟 Monthly Review: {ma.get('month')} (Self-Trust: {ma.get('self_trust_score')}/10)"):
                    st.markdown(f"**📅 Date Logged:** {ma.get('date')}")
                    st.markdown(f"**📈 Key Outcomes:**\n{ma.get('outcomes') or 'None entered'}")
                    st.progress(ma.get('self_trust_score', 5) / 10.0, text=f"Self-Trust Score: {ma.get('self_trust_score')}/10")

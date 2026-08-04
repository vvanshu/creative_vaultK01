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
        "title": "Q1: Do First (Urgent & Important)",
        "color": "#ff4d4d",
        "glow": "rgba(255, 77, 77, 0.25)",
        "bg_color": "rgba(255, 77, 77, 0.06)",
        "border_color": "rgba(255, 77, 77, 0.4)",
        "desc": "Crises, tight college deadlines, urgent issues."
    },
    "Q2": {
        "title": "Q2: Schedule (Important, Not Urgent)",
        "color": "#3b82f6",
        "glow": "rgba(59, 130, 246, 0.25)",
        "bg_color": "rgba(59, 130, 246, 0.06)",
        "border_color": "rgba(59, 130, 246, 0.4)",
        "desc": "Vibecoding, Portfolio, Content, Networking, Exercise."
    },
    "Q3": {
        "title": "Q3: Delegate / Limit (Urgent, Not Important)",
        "color": "#eab308",
        "glow": "rgba(234, 179, 8, 0.25)",
        "bg_color": "rgba(234, 179, 8, 0.06)",
        "border_color": "rgba(234, 179, 8, 0.4)",
        "desc": "Interruptions, minor requests, low-impact tasks."
    },
    "Q4": {
        "title": "Q4: Eliminate (Not Urgent & Not Important)",
        "color": "#9ca3af",
        "glow": "rgba(156, 163, 175, 0.25)",
        "bg_color": "rgba(156, 163, 175, 0.06)",
        "border_color": "rgba(156, 163, 175, 0.4)",
        "desc": "Mindless scrolling, busywork, time sinks."
    }
}

PRIORITY_COLORS = {
    "Critical": "#ef4444",
    "High": "#f97316",
    "Medium": "#eab308",
    "Low": "#10b981"
}

ENERGY_ICONS = {
    "High Energy": "⚡ High",
    "Medium Energy": "🔋 Medium",
    "Low Energy": "🍃 Low"
}

st.set_page_config(
    page_title="Quadrants - Eisenhower Matrix System",
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
# STUNNING GLASSMORPHIC DARK UI CSS
# -----------------------------------------------------------------------------
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">

<style>
    /* Root Design Tokens */
    :root {
        --bg-main: #0b0f19;
        --card-bg: rgba(18, 24, 38, 0.75);
        --card-border: rgba(255, 255, 255, 0.08);
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --accent-glow: rgba(59, 130, 246, 0.15);
    }

    .stApp {
        background-color: var(--bg-main);
        background-image: 
            radial-gradient(at 0% 0%, rgba(30, 58, 138, 0.2) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(17, 24, 39, 0.8) 0px, transparent 50%),
            radial-gradient(at 50% 50%, rgba(15, 23, 42, 0.5) 0px, transparent 100%);
        color: var(--text-primary);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Top App Header Banner */
    .app-title-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.5rem 0 1.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        margin-bottom: 1.5rem;
    }

    .app-title {
        font-family: 'Outfit', sans-serif;
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 30%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
        margin: 0;
    }

    .app-subtitle {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-top: 0.2rem;
    }

    /* Metric Glass Cards */
    .stat-card {
        background: var(--card-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 1.1rem 1.2rem;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }
    .stat-val {
        font-family: 'Outfit', sans-serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.1;
    }
    .stat-lbl {
        font-size: 0.75rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 0.4rem;
        font-weight: 600;
    }

    /* Quadrant Container Styling */
    .q-header-box {
        padding: 1rem 1.2rem;
        border-radius: 14px 14px 0 0;
        border: 1px solid var(--card-border);
        margin-bottom: 0px;
        backdrop-filter: blur(10px);
    }

    .q1-style { background: rgba(255, 77, 77, 0.08); border-color: rgba(255, 77, 77, 0.3); }
    .q2-style { background: rgba(59, 130, 246, 0.08); border-color: rgba(59, 130, 246, 0.3); }
    .q3-style { background: rgba(234, 179, 8, 0.08); border-color: rgba(234, 179, 8, 0.3); }
    .q4-style { background: rgba(156, 163, 175, 0.08); border-color: rgba(156, 163, 175, 0.3); }

    .q-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 1.15rem;
        margin: 0;
    }
    .q-desc {
        font-size: 0.8rem;
        color: var(--text-secondary);
        margin-top: 0.2rem;
    }

    /* Task Item Card */
    .task-card {
        background: rgba(24, 32, 49, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: 0.9rem 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.2s ease-in-out;
    }
    .task-card:hover {
        border-color: rgba(255, 255, 255, 0.15);
        background: rgba(30, 41, 59, 0.7);
        transform: translateY(-1px);
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.18rem 0.55rem;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        margin-right: 0.3rem;
    }
    .badge-cat {
        background: rgba(255, 255, 255, 0.06);
        color: #cbd5e1;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .badge-time {
        background: rgba(59, 130, 246, 0.12);
        color: #93c5fd;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }

    /* Customizing Streamlit Tabs & Inputs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.6);
        padding: 6px;
        border-radius: 14px;
        border: 1px solid var(--card-border);
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 10px;
        color: var(--text-secondary);
        font-weight: 600;
        font-size: 0.9rem;
        padding: 0 18px;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(59, 130, 246, 0.2) !important;
        color: #ffffff !important;
        border: 1px solid rgba(59, 130, 246, 0.4) !important;
    }

    /* Sidebar form styling */
    div[data-testid="stSidebarNav"] {
        display: none;
    }

    .sidebar-streak-box {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(249, 115, 22, 0.15) 100%);
        border: 1px solid rgba(249, 115, 22, 0.3);
        border-radius: 14px;
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
<div class="app-title-container">
    <div>
        <h1 class="app-title">🎯 Quadrants System</h1>
        <div class="app-subtitle">Eisenhower Matrix & Systemic Goal Auditor for High-Performers</div>
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
        
        submit = st.form_submit_button("➕ Add Task to System", use_container_width=True)
        
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
    <div class="sidebar-streak-box">
        <div style="font-size: 2.2rem; font-weight: 800; color: #f97316; line-height: 1;">🔥 {streak}</div>
        <div style="font-size: 0.8rem; color: #cbd5e1; font-weight: 600; margin-top: 0.3rem;">CONSECUTIVE DAYS</div>
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
        if st.button("Reset", use_container_width=True, type="secondary"):
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

    # Statistics Bar
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-val">{total_tasks}</div>
            <div class="stat-lbl">Total Tasks</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-val" style="color: #10b981;">{completed_tasks}</div>
            <div class="stat-lbl">Completed</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-val" style="color: #3b82f6;">{q2_ratio}%</div>
            <div class="stat-lbl">Q2 Focus Ratio</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-val" style="color: #f59e0b;">{total_est_hours}h</div>
            <div class="stat-lbl">Pending Time</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_top1, col_top2 = st.columns(2)
    col_bot1, col_bot2 = st.columns(2)

    grid_mapping = [
        ("Q1", col_top1, "q1-style"),
        ("Q2", col_top2, "q2-style"),
        ("Q3", col_bot1, "q3-style"),
        ("Q4", col_bot2, "q4-style")
    ]

    for q_code, col, css_class in grid_mapping:
        info = QUADRANT_INFO[q_code]
        q_tasks = [t for t in tasks if t.get("quadrant") == q_code]
        q_completed = len([t for t in q_tasks if t.get("completed")])
        q_total = len(q_tasks)

        with col:
            st.markdown(f"""
            <div class="q-header-box {css_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 class="q-title" style="color:{info['color']};">{info['title']}</h4>
                    <span style="font-size: 0.8rem; font-weight: 700; color: {info['color']}; background: rgba(255,255,255,0.06); padding: 2px 8px; border-radius: 10px;">{q_completed}/{q_total}</span>
                </div>
                <div class="q-desc">{info['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if not q_tasks:
                st.caption("✨ No tasks in this quadrant.")
                st.markdown("<br>", unsafe_allow_html=True)
            else:
                for task in q_tasks:
                    is_done = task.get("completed", False)
                    p_color = PRIORITY_COLORS.get(task.get("priority", "Medium"), "#eab308")
                    e_icon = ENERGY_ICONS.get(task.get("energy", "Medium Energy"), "🔋 Medium")
                    
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
                            <div style="margin-left: 28px; margin-top: -6px; margin-bottom: 8px;">
                                <span class="badge badge-cat">{task.get('category')}</span>
                                <span class="badge badge-time">⏱️ {task.get('est_time')}m</span>
                                <span class="badge" style="background: {p_color}22; color: {p_color}; border: 1px solid {p_color}44;">{task.get('priority')}</span>
                                <span class="badge" style="background: rgba(255,255,255,0.04); color: #94a3b8; border: 1px solid rgba(255,255,255,0.08);">{e_icon}</span>
                            </div>
                            """, unsafe_allow_html=True)
                            
                        with t_col2:
                            pop_col1, pop_col2 = st.columns(2)
                            with pop_col1:
                                # Quick move menu
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
                        st.markdown("<hr style='margin: 4px 0 10px 0; border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

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
            if st.button("🧹 Clear Completed Tasks", use_container_width=True, type="secondary"):
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
            <div class="stat-card">
                <div class="stat-val" style="color: #60a5fa;">12 Posts</div>
                <div class="stat-lbl">Instagram Goal (3/wk)</div>
            </div>
            """, unsafe_allow_html=True)
        with col_g2:
            st.markdown("""
            <div class="stat-card">
                <div class="stat-val" style="color: #34d399;">1 Project</div>
                <div class="stat-lbl">Portfolio Goal</div>
            </div>
            """, unsafe_allow_html=True)
        with col_g3:
            streak = st.session_state.db.get('vibecoding_streak', 0)
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-val" style="color: #f97316;">{streak} / 30</div>
                <div class="stat-lbl">Vibecoding Streak</div>
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

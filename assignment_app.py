import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta

# Page configuration - mobile-first centered viewport
st.set_page_config(
    page_title="Assignment Tracker",
    page_icon="📜",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 1. Custom CSS/HTML Injection for Modern Dark Theme Aesthetics
st.markdown("""
<style>
    /* Import modern Sans font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Hide standard Streamlit header, footer, decoration top bar, and default menu */
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    div[data-testid="stDecoration"] { display: none !important; }
    #MainMenu { visibility: hidden !important; }

    /* Set the viewport dark canvas and base typography */
    .stApp {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    /* Style the main container (the dark panel card) */
    .block-container {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.4) !important;
        padding: 30px 24px !important;
        margin: 25px auto !important;
        max-width: 520px !important;
        border-radius: 16px !important;
        position: relative !important;
    }

    /* Modern Headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #F8FAFC !important;
        font-weight: 700 !important;
        margin-top: 15px !important;
        margin-bottom: 10px !important;
        letter-spacing: -0.5px !important;
    }

    /* Input textboxes and numbers matching dark theme */
    input, textarea {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        font-family: inherit !important;
        padding: 8px 12px !important;
    }
    input:focus, textarea:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25) !important;
        outline: none !important;
    }

    /* Custom labels styles for streamlit input components */
    label {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: #94A3B8 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.2px;
        margin-bottom: 4px !important;
    }

    /* Streamlit form box custom dark styling */
    div[data-testid="stForm"] {
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        background-color: #0F172A !important;
        padding: 20px !important;
        box-shadow: none !important;
    }

    /* Streamlit expander component overhaul */
    .streamlit-expanderHeader {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        color: #F8FAFC !important;
        font-family: inherit !important;
        font-weight: 600 !important;
        margin-bottom: 4px !important;
        transition: background-color 0.15s ease, border-color 0.15s ease;
    }
    .streamlit-expanderHeader:hover {
        background-color: #243049 !important;
        border-color: #475569 !important;
    }
    .streamlit-expanderContent {
        background-color: #1E293B !important;
        border-left: 1px solid #334155 !important;
        border-right: 1px solid #334155 !important;
        border-bottom: 1px solid #334155 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        padding: 15px !important;
    }

    /* Streamlit default buttons overrides */
    .stButton > button {
        border: 1px solid #475569 !important;
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border-radius: 8px !important;
        font-family: inherit !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        box-shadow: none !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
        padding: 6px 12px !important;
    }
    .stButton > button:hover {
        background-color: #0F172A !important;
        color: #3B82F6 !important;
        border-color: #3B82F6 !important;
    }
    .stButton > button:active {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
        border-color: #3B82F6 !important;
    }

    /* Highlight class for primary submit buttons */
    div[data-testid="stFormSubmitButton"] .stButton > button {
        background-color: #3B82F6 !important;
        border-color: #2563EB !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stFormSubmitButton"] .stButton > button:hover {
        background-color: #2563EB !important;
        border-color: #1D4ED8 !important;
        color: #FFFFFF !important;
    }

    /* Styling for selectboxes, date input, calendar widgets in dark theme */
    div[data-baseweb="select"] > div {
        background-color: #0F172A !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    
    /* Calendar popover element styling */
    div[data-baseweb="calendar"] {
        background-color: #1E293B !important;
        border: 1px solid #475569 !important;
        font-family: inherit !important;
        border-radius: 8px !important;
        color: #F8FAFC !important;
    }
    div[data-baseweb="calendar"] button {
        border-radius: 8px !important;
        color: #F8FAFC !important;
    }
    div[data-baseweb="calendar"] button:hover {
        background-color: #334155 !important;
        color: #FFFFFF !important;
    }
    div[data-baseweb="calendar"] [aria-selected="true"] {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
    }

    /* Selectbox list/dropdown items contrast */
    div[data-baseweb="menu"] {
        background-color: #1E293B !important;
        border: 1px solid #475569 !important;
    }
    div[data-baseweb="menu"] li {
        color: #F8FAFC !important;
    }
    div[data-baseweb="menu"] li:hover, div[data-baseweb="menu"] li[aria-selected="true"] {
        background-color: #334155 !important;
        color: #FFFFFF !important;
    }

    /* Modern clean card structure */
    .ledger-card {
        border: 1px solid #334155;
        background-color: #0F172A;
        padding: 16px;
        margin-top: 15px;
        margin-bottom: 5px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .ledger-subject {
        font-family: inherit;
        font-size: 0.75rem;
        color: #94A3B8;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .ledger-title {
        font-family: inherit;
        font-size: 1.15rem;
        font-weight: 600;
        color: #F8FAFC;
        margin: 6px 0;
    }
    .ledger-tag {
        background-color: #1E293B;
        border: 1px solid #334155;
        color: #94A3B8;
        padding: 2px 8px;
        font-size: 0.7rem;
        font-family: inherit;
        border-radius: 6px;
        margin-right: 5px;
        display: inline-block;
        font-weight: 500;
    }
    
    /* Clean rounded priority badges */
    .badge-high {
        background-color: rgba(239, 68, 68, 0.15) !important;
        border: 1px solid #EF4444 !important;
        color: #F87171 !important;
        padding: 2px 8px !important;
        border-radius: 9999px !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        display: inline-block !important;
    }
    .badge-medium {
        background-color: rgba(59, 130, 246, 0.15) !important;
        border: 1px solid #3B82F6 !important;
        color: #60A5FA !important;
        padding: 2px 8px !important;
        border-radius: 9999px !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        display: inline-block !important;
    }
    .badge-low {
        background-color: rgba(16, 185, 129, 0.15) !important;
        border: 1px solid #10B981 !important;
        color: #34D399 !important;
        padding: 2px 8px !important;
        border-radius: 9999px !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        display: inline-block !important;
    }

    /* Scrollbars matching modern slate paneling */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #1E293B;
    }
    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# 2. Local State Storage Initialization
if "assignments" not in st.session_state:
    st.session_state.assignments = [
        {
            "id": 1,
            "title": "Draft blueprints for steam engine",
            "subject": "Thermodynamics",
            "tags": ["BLUEPRINT", "LAB", "DRAFTING"],
            "due_date": date.today() + timedelta(days=3),
            "estimated_hours": 8.5,
            "completed": False
        },
        {
            "id": 2,
            "title": "Calibrate mechanical sextant",
            "subject": "Navigation",
            "tags": ["PRACTICAL", "FIELDWORK"],
            "due_date": date.today() + timedelta(days=1),
            "estimated_hours": 4.0,
            "completed": False
        },
        {
            "id": 3,
            "title": "Translate ancient paper scroll",
            "subject": "Archaeology",
            "tags": ["TRANSLATION", "LIBRARY"],
            "due_date": date.today() + timedelta(days=7),
            "estimated_hours": 12.0,
            "completed": False
        }
    ]

# Display reactive state messages if present (shows success/deletion feedback post-rerun)
if "just_added" in st.session_state:
    st.markdown(f"""
    <div style="border: 1px solid #10B981; background-color: rgba(16, 185, 129, 0.1); color: #34D399; padding: 12px; margin-bottom: 15px; border-radius: 8px; font-size: 0.9rem;">
        <strong>Success:</strong> {st.session_state["just_added"]}
    </div>
    """, unsafe_allow_html=True)
    del st.session_state["just_added"]

if "status_msg" in st.session_state:
    st.markdown(f"""
    <div style="border: 1px solid #3B82F6; background-color: rgba(59, 130, 246, 0.1); color: #60A5FA; padding: 12px; margin-bottom: 15px; border-radius: 8px; font-size: 0.9rem;">
        <strong>Status:</strong> {st.session_state["status_msg"]}
    </div>
    """, unsafe_allow_html=True)
    del st.session_state["status_msg"]

# 3. Main Header Section
st.markdown("""
<div style="text-align: center; border-bottom: 1px solid #334155; padding-bottom: 15px; margin-bottom: 20px;">
    <h1 style="margin: 0; font-size: 2.1rem; letter-spacing: -1px; line-height: 1.1;">Assignment Tracker</h1>
    <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 4px;">
        Prioritized Task Management in Modern Dark Theme
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Urgency priority sorting engine (Strict 11:59:59 PM calculation)
active_tasks = []
now = datetime.now()

for task in st.session_state.assignments:
    if task["completed"]:
        continue
    
    # Calculate target time: 11:59:59 PM of the target due date
    due_datetime = datetime.combine(task["due_date"], time(23, 59, 59))
    time_remaining = due_datetime - now
    days_left = time_remaining.total_seconds() / 86400.0
    
    # Clamping overdue/urgent conditions to avoid infinity/division error
    days_left_clamped = max(days_left, 0.0001)
    score = task["estimated_hours"] / days_left_clamped
    
    task_copy = task.copy()
    task_copy["days_left"] = days_left
    task_copy["score"] = score
    task_copy["overdue"] = due_datetime < now
    active_tasks.append(task_copy)

# Sort strictly by priority score descending
active_tasks = sorted(active_tasks, key=lambda x: x["score"], reverse=True)

# 5. Top Stats Manifest Card
pending_count = len(active_tasks)
total_hours = sum([t["estimated_hours"] for t in active_tasks])
critical_count = sum([1 for t in active_tasks if (t["score"] >= 8.0 or t["days_left"] <= 1.5)])

st.markdown(f"""
<div style="border: 1px solid #334155; padding: 12px 15px; margin-bottom: 20px; background-color: #0F172A; border-radius: 8px;">
    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; line-height: 1.4;">
        <div>Active Assignments: <span style="font-weight: bold; color: #3B82F6;">{pending_count}</span></div>
        <div>Total Workload: <span style="font-weight: bold; color: #3B82F6;">{total_hours:.1f} hrs</span></div>
    </div>
    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-top: 4px; line-height: 1.4;">
        <div>Critical Items: <span style="font-weight: bold; color: #EF4444;">{critical_count}</span></div>
        <div>Sort Mode: <span style="font-weight: bold; color: #94A3B8;">Urgency Score</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. Expanding Data Entry Form
with st.expander("[+] Create Assignment", expanded=False):
    with st.form("new_record_form", clear_on_submit=True):
        title = st.text_input("Title", placeholder="e.g. Draft blueprints for steam engine")
        subject = st.text_input("Subject / Course", placeholder="e.g. Thermodynamics")
        
        col_date, col_hrs = st.columns(2)
        with col_date:
            due_date = st.date_input("Due Date", value=date.today())
        with col_hrs:
            est_hours = st.number_input("Estimated Hours", min_value=0.1, max_value=120.0, value=1.0, step=0.5)
            
        tags_input = st.text_input("Tags (comma-separated)", placeholder="e.g. BLUEPRINT, LAB")
        
        submitted = st.form_submit_button("Add Assignment")
        if submitted:
            if not title.strip():
                st.markdown("""
                <div style="border: 1px solid #EF4444; background-color: rgba(239, 68, 68, 0.1); color: #F87171; padding: 12px; margin-top: 10px; border-radius: 8px; font-size: 0.85rem;">
                    <strong>Error:</strong> Assignment title cannot be blank!
                </div>
                """, unsafe_allow_html=True)
            else:
                subj_final = subject.strip() if subject.strip() else "GENERAL"
                tags_list = [t.strip().upper() for t in tags_input.split(",") if t.strip()]
                if not tags_list:
                    tags_list = ["ASSIGNMENT"]
                    
                new_id = max([t["id"] for t in st.session_state.assignments] + [0]) + 1
                
                new_task = {
                    "id": new_id,
                    "title": title.strip(),
                    "subject": subj_final,
                    "tags": tags_list,
                    "due_date": due_date,
                    "estimated_hours": float(est_hours),
                    "completed": False
                }
                
                st.session_state.assignments.append(new_task)
                st.session_state["just_added"] = f"Assignment #{new_id} added successfully!"
                st.rerun()

# 7. Active Tasks Render Loop
st.markdown("<h3 style='margin-top: 20px; font-size: 1.15rem; border-bottom: 1px solid #334155; padding-bottom: 5px;'>Pending Assignments</h3>", unsafe_allow_html=True)

if not active_tasks:
    st.markdown("""
    <div style="text-align: center; padding: 30px; font-style: italic; color: #94A3B8; border: 1px dashed #334155; background-color: #0F172A; margin-top: 15px; border-radius: 8px;">
        -- No active assignments --
    </div>
    """, unsafe_allow_html=True)
else:
    for idx, item in enumerate(active_tasks):
        days_left = item["days_left"]
        score = item["score"]
        
        # Decide stamping labels
        if score >= 8.0 or days_left <= 1.5:
            stamp_class = "badge-high"
            stamp_text = "High Priority"
            urgency_color = "#F87171"
        elif score >= 3.0:
            stamp_class = "badge-medium"
            stamp_text = "Medium Priority"
            urgency_color = "#60A5FA"
        else:
            stamp_class = "badge-low"
            stamp_text = "Low Priority"
            urgency_color = "#34D399"
            
        # Parse time-remaining labels nicely
        if item["overdue"]:
            days_left_str = "<span style='color: #EF4444; font-weight: bold;'>OVERDUE</span>"
        elif days_left < 1.0:
            hours_left = days_left * 24.0
            if hours_left < 1.0:
                mins_left = hours_left * 60.0
                days_left_str = f"<strong>{int(mins_left)} mins left</strong>"
            else:
                days_left_str = f"<strong>{hours_left:.1f} hrs left</strong>"
        else:
            days_left_str = f"<strong>{days_left:.1f} days left</strong>"
            
        tags_html = " ".join([f"<span class='ledger-tag'>#{t}</span>" for t in item["tags"]])
        
        # Card container printout
        card_html = f"""
        <div class="ledger-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span class="ledger-subject">Course: {item['subject'].upper()}</span>
                <span class="{stamp_class}">{stamp_text}</span>
            </div>
            <div class="ledger-title">* {item['title']}</div>
            <div style="font-size: 0.85rem; color: #94A3B8; line-height: 1.4; margin: 8px 0;">
                Due: {item['due_date'].strftime('%Y-%m-%d')} ({days_left_str})<br>
                Est. Hours: {item['estimated_hours']:.1f} | 
                Urgency Score: <span style="font-weight: bold; color: {urgency_color};">{score:.2f}</span>
            </div>
            <div>{tags_html}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Buttons for immediate completion or scrap action
        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            if st.button("✓ Complete", key=f"comp_{item['id']}", use_container_width=True):
                for o_idx, orig in enumerate(st.session_state.assignments):
                    if orig["id"] == item["id"]:
                        st.session_state.assignments[o_idx]["completed"] = True
                st.session_state["status_msg"] = f"Assignment #{item['id']} marked complete"
                st.rerun()
        with btn_col2:
            if st.button("✗ Delete", key=f"scrap_{item['id']}", use_container_width=True):
                for o_idx, orig in enumerate(st.session_state.assignments):
                    if orig["id"] == item["id"]:
                        st.session_state.assignments.pop(o_idx)
                        break
                st.session_state["status_msg"] = f"Assignment #{item['id']} deleted"
                st.rerun()

# 8. Archive Section (Completed Tasks Repositorium)
archived_tasks = [t for t in st.session_state.assignments if t["completed"]]

st.write("")
with st.expander(f"[#] Completed Archive ({len(archived_tasks)})", expanded=False):
    if not archived_tasks:
        st.markdown("""
        <div style="text-align: center; padding: 15px; font-style: italic; color: #94A3B8; font-size: 0.85rem;">
            -- Archive empty --
        </div>
        """, unsafe_allow_html=True)
    else:
        for idx, item in enumerate(archived_tasks):
            tags_html = " ".join([f"<span class='ledger-tag'>#{t}</span>" for t in item["tags"]])
            card_html = f"""
            <div class="ledger-card" style="opacity: 0.65; border-style: dashed; box-shadow: none;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <span class="ledger-subject" style="text-decoration: line-through;">Course: {item['subject'].upper()}</span>
                    <span style="border: 1px dashed #94A3B8; color: #94A3B8; padding: 2px 8px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600;">Completed</span>
                </div>
                <div class="ledger-title" style="text-decoration: line-through; color: #94A3B8;">* {item['title']}</div>
                <div style="font-size: 0.8rem; color: #64748B; margin: 5px 0;">
                    Completed | Workload: {item['estimated_hours']:.1f} hrs
                </div>
                <div>{tags_html}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Action controls for individual archived tasks
            btn_col1, btn_col2 = st.columns([1, 1])
            with btn_col1:
                if st.button("↺ Restore", key=f"rest_{item['id']}", use_container_width=True):
                    for o_idx, orig in enumerate(st.session_state.assignments):
                        if orig["id"] == item["id"]:
                            st.session_state.assignments[o_idx]["completed"] = False
                    st.session_state["status_msg"] = f"Assignment #{item['id']} restored"
                    st.rerun()
            with btn_col2:
                if st.button("☠ Delete", key=f"purge_{item['id']}", use_container_width=True):
                    for o_idx, orig in enumerate(st.session_state.assignments):
                        if orig["id"] == item["id"]:
                            st.session_state.assignments.pop(o_idx)
                            break
                    st.session_state["status_msg"] = f"Assignment #{item['id']} deleted forever"
                    st.rerun()

# 9. System Control Panel & Plaintext Export
st.markdown("<h4 style='font-size: 0.95rem; text-align: center; margin-top: 25px; margin-bottom: 12px; border-top: 1px solid #334155; padding-top: 20px;'>Settings & Tools</h4>", unsafe_allow_html=True)

col_ctrl1, col_ctrl2 = st.columns([1, 1])

with col_ctrl1:
    if st.button("Load Demo Data", help="Load reference retro data"):
        st.session_state.assignments = [
            {
                "id": 1,
                "title": "Draft blueprints for steam engine",
                "subject": "Thermodynamics",
                "tags": ["BLUEPRINT", "LAB", "DRAFTING"],
                "due_date": date.today() + timedelta(days=3),
                "estimated_hours": 8.5,
                "completed": False
            },
            {
                "id": 2,
                "title": "Calibrate mechanical sextant",
                "subject": "Navigation",
                "tags": ["PRACTICAL", "FIELDWORK"],
                "due_date": date.today() + timedelta(days=1),
                "estimated_hours": 4.0,
                "completed": False
            },
            {
                "id": 3,
                "title": "Translate ancient paper scroll",
                "subject": "Archaeology",
                "tags": ["TRANSLATION", "LIBRARY"],
                "due_date": date.today() + timedelta(days=7),
                "estimated_hours": 12.0,
                "completed": False
            }
        ]
        st.session_state["status_msg"] = "Demo data loaded"
        st.rerun()

with col_ctrl2:
    if st.button("Delete All Tasks", help="Wipe all active log entries"):
        st.session_state.assignments = []
        st.session_state["status_msg"] = "All assignments deleted"
        st.rerun()

# Compile the plaintext document matching paper ledger exports
report_lines = []
report_lines.append("==================================================")
report_lines.append("             ASSIGNMENT STATUS REPORT")
report_lines.append(f"        GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report_lines.append("==================================================")
report_lines.append("")
report_lines.append("[ ACTIVE ASSIGNMENTS ]")
report_lines.append("-" * 50)

if not active_tasks:
    report_lines.append("-- NO ACTIVE ASSIGNMENTS DETECTED --")
else:
    for item in active_tasks:
        stamp_label = "Low"
        if item["score"] >= 8.0 or item["days_left"] <= 1.5:
            stamp_label = "High"
        elif item["score"] >= 3.0:
            stamp_label = "Medium"
        
        report_lines.append(f"ID: #{item['id']} | Course: {item['subject'].upper()}")
        report_lines.append(f"TASK: {item['title']}")
        report_lines.append(f"DUE : {item['due_date'].strftime('%Y-%m-%d')} | REMAINING: {item['days_left']:.2f} DAYS")
        report_lines.append(f"EST : {item['estimated_hours']:.1f} HRS | URGENCY: {item['score']:.2f} [{stamp_label}]")
        report_lines.append(f"TAGS: {', '.join(item['tags'])}")
        report_lines.append("-" * 50)

report_lines.append("")
report_lines.append("[ COMPLETED ASSIGNMENTS ]")
report_lines.append("-" * 50)
if not archived_tasks:
    report_lines.append("-- NO COMPLETED ASSIGNMENTS DETECTED --")
else:
    for item in archived_tasks:
        report_lines.append(f"ID: #{item['id']} | Course: {item['subject'].upper()}")
        report_lines.append(f"TASK: {item['title']}")
        report_lines.append(f"TAGS: {', '.join(item['tags'])}")
        report_lines.append("-" * 50)

report_lines.append("")
report_lines.append("==================================================")
report_lines.append("              END OF REPORT")
report_lines.append("==================================================")

report_text = "\n".join(report_lines)

st.write("")
st.download_button(
    label="💾 Download Text Export",
    data=report_text,
    file_name=f"assignment_manifest_{date.today().strftime('%Y%m%d')}.txt",
    mime="text/plain",
    use_container_width=True
)

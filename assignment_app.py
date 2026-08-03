import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta

# Page configuration - mobile-first centered viewport
st.set_page_config(
    page_title="Vintage Retro Assignment Tracker",
    page_icon="📜",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 1. Custom CSS/HTML Injection for Retro Paper Aesthetics
st.markdown("""
<style>
    /* Import vintage typewriter fonts from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Courier+Prime:ital,wght@0,400;0,700;1,400;1,700&family=Special+Elite&display=swap');

    /* Hide standard Streamlit header, footer, decoration top bar, and default menu */
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    div[data-testid="stDecoration"] { display: none !important; }
    #MainMenu { visibility: hidden !important; }

    /* Set the viewport desk canvas and base typography */
    .stApp {
        background-color: #EFEAD8 !important;
        background-image: radial-gradient(#d3c5ab 1.2px, transparent 1.2px) !important;
        background-size: 24px 24px !important;
        color: #2E251E !important;
        font-family: 'Courier Prime', 'Courier New', monospace !important;
    }

    /* Style the main ledger sheet block (the notebook page) */
    .block-container {
        background-color: #FAF6ED !important;
        border: 3px solid #2E251E !important;
        box-shadow: 10px 10px 0px #2E251E !important;
        padding: 30px 25px 30px 45px !important;
        margin: 25px auto !important;
        max-width: 540px !important;
        position: relative !important;
    }

    /* Ledger vertical margin line (red double line style) */
    .block-container::before {
        content: "";
        position: absolute;
        top: 0;
        left: 32px;
        width: 3px;
        height: 100%;
        border-left: 1px solid #C25953;
        border-right: 1px solid #C25953;
        opacity: 0.75;
        z-index: 10;
        pointer-events: none;
    }

    /* Custom headers matching typed documents */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Special Elite', cursive, monospace !important;
        color: #2E251E !important;
        font-weight: bold !important;
        margin-top: 15px !important;
        margin-bottom: 10px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Input textboxes and numbers matching typewriter sheets */
    input, textarea {
        background-color: #FCFAF6 !important;
        color: #2E251E !important;
        border: 2px solid #2E251E !important;
        border-radius: 0px !important;
        font-family: 'Courier Prime', monospace !important;
        padding: 8px 12px !important;
    }
    input:focus, textarea:focus {
        border-color: #C25953 !important;
        box-shadow: none !important;
    }

    /* Custom labels styles for streamlit input components */
    label {
        font-family: 'Special Elite', monospace !important;
        color: #2E251E !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.5px;
    }

    /* Streamlit form box custom retro styling */
    div[data-testid="stForm"] {
        border: 2px solid #2E251E !important;
        border-radius: 0px !important;
        background-color: transparent !important;
        padding: 15px !important;
        box-shadow: none !important;
    }

    /* Streamlit expander component overhaul */
    .streamlit-expanderHeader {
        background-color: #FAF6ED !important;
        border: 2px solid #2E251E !important;
        border-radius: 0px !important;
        color: #2E251E !important;
        font-family: 'Special Elite', monospace !important;
        margin-bottom: 2px !important;
        transition: background-color 0.15s ease;
    }
    .streamlit-expanderHeader:hover {
        background-color: #F1EAD8 !important;
    }
    .streamlit-expanderContent {
        background-color: #FAF6ED !important;
        border-left: 2px solid #2E251E !important;
        border-right: 2px solid #2E251E !important;
        border-bottom: 2px solid #2E251E !important;
        border-top: none !important;
        border-radius: 0px !important;
        padding: 15px !important;
    }

    /* Flat block buttons with zero-radius and solid drop shadows */
    .stButton > button {
        border: 2px solid #2E251E !important;
        background-color: #FCFAF6 !important;
        color: #2E251E !important;
        border-radius: 0px !important;
        font-family: 'Special Elite', monospace !important;
        font-weight: bold !important;
        font-size: 0.85rem !important;
        box-shadow: 4px 4px 0px #2E251E !important;
        transition: all 0.1s ease-in-out !important;
        width: 100% !important;
        padding: 6px 12px !important;
    }
    .stButton > button:hover {
        background-color: #F1EAD8 !important;
        color: #2E251E !important;
        transform: translate(1px, 1px) !important;
        box-shadow: 3px 3px 0px #2E251E !important;
        border-color: #2E251E !important;
    }
    .stButton > button:active {
        background-color: #2E251E !important;
        color: #FAF6ED !important;
        transform: translate(3px, 3px) !important;
        box-shadow: 1px 1px 0px #2E251E !important;
    }

    /* Styling for typewriter selectboxes and date input fields */
    div[data-baseweb="select"] > div {
        background-color: #FCFAF6 !important;
        color: #2E251E !important;
        border: 2px solid #2E251E !important;
        border-radius: 0px !important;
    }
    
    /* Calendar portal adjustments */
    div[data-baseweb="calendar"] {
        background-color: #FAF6ED !important;
        border: 2px solid #2E251E !important;
        font-family: 'Courier Prime', monospace !important;
        border-radius: 0px !important;
    }
    div[data-baseweb="calendar"] button {
        border-radius: 0px !important;
        color: #2E251E !important;
    }
    div[data-baseweb="calendar"] button:hover {
        background-color: #F1EAD8 !important;
    }

    /* Official paper record card elements */
    .ledger-card {
        border: 2px solid #2E251E;
        background-color: #FCFAF6;
        padding: 15px;
        margin-top: 15px;
        margin-bottom: 5px;
        box-shadow: 4px 4px 0px #2E251E;
        position: relative;
    }
    .ledger-subject {
        font-family: 'Special Elite', monospace;
        font-size: 0.85rem;
        color: #7A6B58;
        font-weight: bold;
        letter-spacing: 1px;
    }
    .ledger-title {
        font-family: 'Courier Prime', monospace;
        font-size: 1.2rem;
        font-weight: 700;
        color: #1E1815;
        margin: 6px 0;
    }
    .ledger-tag {
        background-color: #F1EAD8;
        border: 1px solid #2E251E;
        padding: 2px 6px;
        font-size: 0.75rem;
        font-family: 'Courier Prime', monospace;
        margin-right: 5px;
        display: inline-block;
        font-weight: bold;
    }
    
    /* Stamp style ink overlays */
    .stamp-critical {
        border: 3px double #B23B25;
        color: #B23B25;
        padding: 2px 8px;
        font-family: 'Special Elite', monospace;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
        transform: rotate(-3deg);
        text-shadow: 1px 1px 0px rgba(178, 59, 37, 0.08);
    }
    .stamp-pending {
        border: 2px solid #2E251E;
        color: #2E251E;
        padding: 2px 8px;
        font-family: 'Special Elite', monospace;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
        transform: rotate(2deg);
    }
    .stamp-steady {
        border: 2px dashed #7A7268;
        color: #7A7268;
        padding: 2px 8px;
        font-family: 'Special Elite', monospace;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
    }
    
    /* Scrollbars matching analog iron frames */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #FAF6ED;
    }
    ::-webkit-scrollbar-thumb {
        background: #2E251E;
        border-radius: 0px;
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
    <div style="border: 2px solid #2E251E; background-color: #E8F5E9; color: #1B5E20; padding: 10px; margin-bottom: 15px; font-family: 'Courier Prime', monospace; font-size: 0.85rem;">
        [✓ COMMIT SUCCESS] {st.session_state["just_added"]}
    </div>
    """, unsafe_allow_html=True)
    del st.session_state["just_added"]

if "status_msg" in st.session_state:
    st.markdown(f"""
    <div style="border: 2px solid #2E251E; background-color: #FAF2E6; color: #7A5B35; padding: 10px; margin-bottom: 15px; font-family: 'Courier Prime', monospace; font-size: 0.85rem;">
        [⚙ LEDGER STATE UPDATE] {st.session_state["status_msg"]}
    </div>
    """, unsafe_allow_html=True)
    del st.session_state["status_msg"]

# 3. Main Header Section
st.markdown("""
<div style="text-align: center; border-bottom: 2px dashed #2E251E; padding-bottom: 12px; margin-bottom: 15px;">
    <h1 style="margin: 0; font-size: 2.1rem; letter-spacing: -1px; line-height: 1.1;">ASSIGNMENT LEDGER</h1>
    <div style="font-family: 'Special Elite', monospace; font-size: 0.85rem; color: #7A6B58; margin-top: 4px;">
        ANALOG LOGBOOK & PRIORITY MANIFEST // V1.0
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
<div style="border: 2px dashed #2E251E; padding: 12px 15px; margin-bottom: 20px; background-color: #FCFAF6;">
    <div style="display: flex; justify-content: space-between; font-family: 'Special Elite', monospace; font-size: 0.8rem; line-height: 1.4;">
        <div>ACTIVE RECORDS: <span style="font-weight: bold;">{pending_count}</span></div>
        <div>PENDING WORKLOAD: <span style="font-weight: bold;">{total_hours:.1f} HRS</span></div>
    </div>
    <div style="display: flex; justify-content: space-between; font-family: 'Special Elite', monospace; font-size: 0.8rem; margin-top: 4px; line-height: 1.4;">
        <div>CRITICAL URGENT: <span style="font-weight: bold; color: #B23B25;">{critical_count}</span></div>
        <div>LEDGER FEED: <span style="font-weight: bold;">PRIORITIZED DESC</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: #7A6B58; margin: 10px 0 15px 0;'>==================================================</div>", unsafe_allow_html=True)

# 6. Expanding Data Entry Form
with st.expander("[+] FILE NEW RECORD", expanded=False):
    with st.form("new_record_form", clear_on_submit=True):
        title = st.text_input("TASK TITLE", placeholder="e.g. Draft blueprints for steam engine")
        subject = st.text_input("LOG DEPT / SUBJECT", placeholder="e.g. Thermodynamics")
        
        col_date, col_hrs = st.columns(2)
        with col_date:
            due_date = st.date_input("DEADLINE DATE", value=date.today())
        with col_hrs:
            est_hours = st.number_input("EST. WORKLOAD (HRS)", min_value=0.1, max_value=120.0, value=1.0, step=0.5)
            
        tags_input = st.text_input("METADATA TAGS (comma-separated)", placeholder="e.g. BLUEPRINT, LAB")
        
        submitted = st.form_submit_button("COMMIT TO LEDGER")
        if submitted:
            if not title.strip():
                st.markdown("""
                <div style="border: 2px solid #B23B25; background-color: #FFEBEE; color: #B23B25; padding: 8px 12px; margin-top: 10px; font-family: 'Courier Prime', monospace; font-size: 0.85rem;">
                    [!] VALIDATION ERROR: RECORD TITLE CANNOT BE VOID!
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
                st.session_state["just_added"] = f"RECORD #{new_id} ('{title.strip()}') COMMITTED"
                st.rerun()

# 7. Active Ledger Render Loop
st.markdown("<h3 style='margin-top: 15px; font-size: 1.15rem; text-decoration: underline;'>[ PENDING LEDGER QUEUE ]</h3>", unsafe_allow_html=True)

if not active_tasks:
    st.markdown("""
    <div style="text-align: center; padding: 30px; font-style: italic; color: #7A6B58; border: 2px dashed #2E251E; background-color: #FCFAF6; margin-top: 15px; font-family: 'Courier Prime', monospace;">
        -- NO ACTIVE RECORDS DETECTED IN LEDGER --
    </div>
    """, unsafe_allow_html=True)
else:
    for idx, item in enumerate(active_tasks):
        days_left = item["days_left"]
        score = item["score"]
        
        # Decide stamping labels
        if score >= 8.0 or days_left <= 1.5:
            stamp_class = "stamp-critical"
            stamp_text = "[ CRITICAL ]"
            urgency_color = "#B23B25"
        elif score >= 3.0:
            stamp_class = "stamp-pending"
            stamp_text = "[ PENDING ]"
            urgency_color = "#2E251E"
        else:
            stamp_class = "stamp-steady"
            stamp_text = "[ STEADY ]"
            urgency_color = "#7A7268"
            
        # Parse time-remaining labels nicely
        if item["overdue"]:
            days_left_str = "<span style='color: #B23B25; font-weight: bold;'>OVERDUE</span>"
        elif days_left < 1.0:
            hours_left = days_left * 24.0
            if hours_left < 1.0:
                mins_left = hours_left * 60.0
                days_left_str = f"<strong>{int(mins_left)} MINS LEFT</strong>"
            else:
                days_left_str = f"<strong>{hours_left:.1f} HRS LEFT</strong>"
        else:
            days_left_str = f"<strong>{days_left:.1f} DAYS LEFT</strong>"
            
        tags_html = " ".join([f"<span class='ledger-tag'>#{t}</span>" for t in item["tags"]])
        
        # Card container printout
        card_html = f"""
        <div class="ledger-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span class="ledger-subject">DEPT: {item['subject'].upper()}</span>
                <span class="{stamp_class}">{stamp_text}</span>
            </div>
            <div class="ledger-title">* {item['title']}</div>
            <div style="font-family: 'Courier Prime', monospace; font-size: 0.85rem; color: #544B40; line-height: 1.4; margin: 8px 0;">
                DEADLINE: {item['due_date'].strftime('%Y-%m-%d')} ({days_left_str})<br>
                WORKLOAD: {item['estimated_hours']:.1f} HOURS | 
                URGENCY INDEX: <span style="font-weight: bold; color: {urgency_color};">{score:.2f}</span>
            </div>
            <div>{tags_html}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Buttons for immediate completion or scrap action
        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            if st.button("✓ STAMP COMPLETED", key=f"comp_{item['id']}", use_container_width=True):
                for o_idx, orig in enumerate(st.session_state.assignments):
                    if orig["id"] == item["id"]:
                        st.session_state.assignments[o_idx]["completed"] = True
                st.session_state["status_msg"] = f"RECORD #{item['id']} ARCHIVED"
                st.rerun()
        with btn_col2:
            if st.button("✗ SCRAP RECORD", key=f"scrap_{item['id']}", use_container_width=True):
                for o_idx, orig in enumerate(st.session_state.assignments):
                    if orig["id"] == item["id"]:
                        st.session_state.assignments.pop(o_idx)
                        break
                st.session_state["status_msg"] = f"RECORD #{item['id']} SCRAPPED PERMANENTLY"
                st.rerun()

st.markdown("<div style='text-align: center; color: #7A6B58; margin: 15px 0 10px 0;'>==================================================</div>", unsafe_allow_html=True)

# 8. Archive Section (Completed Tasks Repositorium)
archived_tasks = [t for t in st.session_state.assignments if t["completed"]]

with st.expander(f"[#] ARCHIVE REPOSITORIUM ({len(archived_tasks)})", expanded=False):
    if not archived_tasks:
        st.markdown("""
        <div style="text-align: center; padding: 15px; font-style: italic; color: #7A6B58; font-family: 'Courier Prime', monospace; font-size: 0.85rem;">
            -- ARCHIVE VOID --
        </div>
        """, unsafe_allow_html=True)
    else:
        for idx, item in enumerate(archived_tasks):
            tags_html = " ".join([f"<span class='ledger-tag'>#{t}</span>" for t in item["tags"]])
            card_html = f"""
            <div class="ledger-card" style="opacity: 0.65; background-color: #F1EAD8; border-style: dashed; box-shadow: none;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <span class="ledger-subject" style="text-decoration: line-through;">DEPT: {item['subject'].upper()}</span>
                    <span style="border: 2px dashed #7A6B58; color: #7A6B58; padding: 2px 6px; font-family: 'Special Elite', monospace; font-size: 0.75rem; font-weight: bold;">[ ARCHIVED ]</span>
                </div>
                <div class="ledger-title" style="text-decoration: line-through; color: #544B40;">* {item['title']}</div>
                <div style="font-family: 'Courier Prime', monospace; font-size: 0.8rem; color: #7A6B58; margin: 5px 0;">
                    RESOLVED RECORD | WORKLOAD: {item['estimated_hours']:.1f} HRS
                </div>
                <div>{tags_html}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Action controls for individual archived tasks
            btn_col1, btn_col2 = st.columns([1, 1])
            with btn_col1:
                if st.button("↺ RESTORE RECORD", key=f"rest_{item['id']}", use_container_width=True):
                    for o_idx, orig in enumerate(st.session_state.assignments):
                        if orig["id"] == item["id"]:
                            st.session_state.assignments[o_idx]["completed"] = False
                    st.session_state["status_msg"] = f"RECORD #{item['id']} RESTORED"
                    st.rerun()
            with btn_col2:
                if st.button("☠ PURGE RECORD", key=f"purge_{item['id']}", use_container_width=True):
                    for o_idx, orig in enumerate(st.session_state.assignments):
                        if orig["id"] == item["id"]:
                            st.session_state.assignments.pop(o_idx)
                            break
                    st.session_state["status_msg"] = f"RECORD #{item['id']} PURGED"
                    st.rerun()

st.markdown("<div style='text-align: center; color: #7A6B58; margin: 15px 0 10px 0;'>==================================================</div>", unsafe_allow_html=True)

# 9. System Control Panel & Plaintext Export
st.markdown("<h4 style='font-size: 0.95rem; text-align: center; margin-bottom: 12px; letter-spacing: 0.5px;'>[ LEDGER SYSTEM CONTROL PANEL ]</h4>", unsafe_allow_html=True)

col_ctrl1, col_ctrl2 = st.columns([1, 1])

with col_ctrl1:
    if st.button("SEED INITIAL RECORDS", help="Load reference retro data"):
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
        st.session_state["status_msg"] = "TEST RECORDS INSTALLED"
        st.rerun()

with col_ctrl2:
    if st.button("PURGE ACTIVE LEDGER", help="Wipe all active log entries"):
        st.session_state.assignments = []
        st.session_state["status_msg"] = "ALL LEDGER ENTRIES SCRAPPED"
        st.rerun()

# Compile the plaintext document matching paper ledger exports
report_lines = []
report_lines.append("==================================================")
report_lines.append("              OFFICIAL LEDGER REPORT")
report_lines.append(f"        GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report_lines.append("==================================================")
report_lines.append("")
report_lines.append("[ ACTIVE PENDING RECORDS ]")
report_lines.append("-" * 50)

if not active_tasks:
    report_lines.append("-- NO ACTIVE RECORDS DETECTED --")
else:
    for item in active_tasks:
        stamp_label = "STEADY"
        if item["score"] >= 8.0 or item["days_left"] <= 1.5:
            stamp_label = "CRITICAL"
        elif item["score"] >= 3.0:
            stamp_label = "PENDING"
        
        report_lines.append(f"ID: #{item['id']} | DEPT: {item['subject'].upper()}")
        report_lines.append(f"TASK: {item['title']}")
        report_lines.append(f"DUE : {item['due_date'].strftime('%Y-%m-%d')} | REMAINING: {item['days_left']:.2f} DAYS")
        report_lines.append(f"EST : {item['estimated_hours']:.1f} HRS | URGENCY INDEX: {item['score']:.2f} [{stamp_label}]")
        report_lines.append(f"TAGS: {', '.join(item['tags'])}")
        report_lines.append("-" * 50)

report_lines.append("")
report_lines.append("[ ARCHIVED RESOLVED RECORDS ]")
report_lines.append("-" * 50)
if not archived_tasks:
    report_lines.append("-- NO ARCHIVED RECORDS DETECTED --")
else:
    for item in archived_tasks:
        report_lines.append(f"ID: #{item['id']} | DEPT: {item['subject'].upper()}")
        report_lines.append(f"TASK: {item['title']}")
        report_lines.append(f"TAGS: {', '.join(item['tags'])}")
        report_lines.append("-" * 50)

report_lines.append("")
report_lines.append("==================================================")
report_lines.append("              END OF LEDGER SHEET")
report_lines.append("==================================================")

report_text = "\n".join(report_lines)

st.write("")
st.download_button(
    label="💾 DOWNLOAD ASCII MANIFEST",
    data=report_text,
    file_name=f"ledger_manifest_{date.today().strftime('%Y%m%d')}.txt",
    mime="text/plain",
    use_container_width=True
)

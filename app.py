import streamlit as st
import json

# Page Configuration
st.set_page_config(
    page_title="Minimalist Challenge Tracker",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Glassmorphic Dark styling injection
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    
    <style>
        /* Global variables */
        :root {
            --bg-color: #090d16;
            --accent-green: #10b981;
            --accent-green-glow: rgba(16, 185, 129, 0.35);
            --card-bg: rgba(17, 24, 39, 0.7);
            --card-border: rgba(255, 255, 255, 0.08);
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
        }

        /* Streamlit background overrides */
        .stApp {
            background-color: var(--bg-color);
            background-image: radial-gradient(circle at 50% 50%, #111827 0%, #090d16 100%);
            color: var(--text-primary);
            font-family: 'Outfit', sans-serif;
        }

        /* Center container adjustments */
        .block-container {
            padding-top: 3rem;
            padding-bottom: 3rem;
            max-width: 580px !important;
        }

        /* Remove default headers/footers */
        header, footer, div[data-testid="stToolbar"] {
            visibility: hidden !important;
            display: none !important;
        }

        /* App Banner Header */
        .app-header {
            text-align: center;
            margin-bottom: 2rem;
        }

        .glow-title {
            font-size: 2.25rem;
            font-weight: 800;
            letter-spacing: 0.1em;
            background: linear-gradient(135deg, #ffffff 40%, #a5b4fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 4px 20px rgba(165, 180, 252, 0.15);
            margin-bottom: 0.25rem;
            text-transform: uppercase;
        }

        .subtitle {
            font-size: 0.875rem;
            color: var(--text-secondary);
            font-family: 'Plus Jakarta Sans', sans-serif;
            letter-spacing: 0.05em;
        }

        /* Glassmorphic card styling */
        .glass-card {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 1.75rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            margin-bottom: 1.5rem;
        }

        /* Progress Card & Metrics styling */
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-top: 1rem;
            text-align: center;
        }

        .metric-box {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 12px;
            padding: 0.75rem 0.5rem;
        }

        .metric-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: #ffffff;
            line-height: 1.2;
        }

        .metric-label {
            font-size: 0.75rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-top: 0.25rem;
        }

        /* Visual Progress Bar */
        .progress-bar-container {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            height: 10px;
            width: 100%;
            overflow: hidden;
            margin-top: 1.25rem;
            border: 1px solid rgba(255, 255, 255, 0.02);
        }

        .progress-bar-fill {
            background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
            height: 100%;
            border-radius: 8px;
            box-shadow: 0 0 10px var(--accent-green-glow);
            transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Days Grid layout */
        .circle-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 12px;
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
            justify-content: center;
        }

        @media (max-width: 480px) {
            .circle-grid {
                grid-template-columns: repeat(5, 1fr);
                gap: 8px;
            }
            .glow-title {
                font-size: 1.85rem;
            }
        }

        /* Grid Day Circle Link Styling */
        .circle-day {
            display: flex;
            align-items: center;
            justify-content: center;
            aspect-ratio: 1 / 1;
            border-radius: 50%;
            text-decoration: none !important;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            user-select: none;
        }

        .circle-day.incomplete {
            background: rgba(255, 255, 255, 0.03);
            color: var(--text-secondary);
        }

        .circle-day.incomplete:hover {
            background: rgba(255, 255, 255, 0.08);
            color: #ffffff;
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
        }

        .circle-day.completed {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: #ffffff;
            border-color: #10b981;
            box-shadow: 0 0 12px var(--accent-green-glow);
        }

        .circle-day.completed:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 18px rgba(16, 185, 129, 0.6);
        }

        /* Streamlit native widget customization */
        div[data-testid="stForm"] {
            border: 1px solid var(--card-border) !important;
            background: var(--card-bg) !important;
            border-radius: 20px !important;
            padding: 1.5rem !important;
        }
        
        button[kind="primary"] {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
            border: none !important;
            color: white !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 12px var(--accent-green-glow) !important;
        }
        
        button[kind="secondary"] {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid var(--card-border) !important;
            color: var(--text-secondary) !important;
        }
        
        button[kind="secondary"]:hover {
            background: rgba(255, 255, 255, 0.08) !important;
            color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

# Helper to load existing challenge from local storage/session state
def init_state():
    if "challenge_created" not in st.session_state:
        # Check if we have backup file in project root for simple persistence
        try:
            with open("challenge_data.json", "r") as f:
                data = json.load(f)
                st.session_state.challenge_name = data.get("name", "Daily Habit")
                st.session_state.challenge_days = data.get("days", 30)
                st.session_state.completed = set(data.get("completed", []))
                st.session_state.challenge_created = True
        except FileNotFoundError:
            st.session_state.challenge_created = False

# Save state helper for simple persistence
def save_state():
    if st.session_state.challenge_created:
        data = {
            "name": st.session_state.challenge_name,
            "days": st.session_state.challenge_days,
            "completed": list(st.session_state.completed)
        }
        with open("challenge_data.json", "w") as f:
            json.dump(data, f)
    else:
        try:
            import os
            if os.path.exists("challenge_data.json"):
                os.remove("challenge_data.json")
        except OSError:
            pass

# Initialize session state variables
init_state()

# 1. Intercept grid clicks using Query Parameters
if "toggle" in st.query_params:
    try:
        day_to_toggle = int(st.query_params["toggle"])
        if st.session_state.challenge_created:
            if day_to_toggle in st.session_state.completed:
                st.session_state.completed.remove(day_to_toggle)
            else:
                st.session_state.completed.add(day_to_toggle)
            save_state()
    except ValueError:
        pass
    st.query_params.clear()
    st.rerun()

# --- HEADER ---
st.markdown("""
    <div class="app-header">
        <h1 class="glow-title">🎯 DayTrack</h1>
        <p class="subtitle">Minimalist Challenge Tracker</p>
    </div>
""", unsafe_allow_html=True)

# --- CREATION MODE ---
if not st.session_state.challenge_created:
    with st.form("create_challenge_form"):
        st.subheader("Start a New Challenge")
        challenge_name = st.text_input("What is your challenge?", placeholder="e.g. 100 Days of Code, Daily Gym, Meditate")
        
        duration_option = st.radio("Duration", ["7 Days", "30 Days", "60 Days", "Custom Days"], horizontal=True, index=1)
        
        custom_days = 30
        if duration_option == "Custom Days":
            custom_days = st.number_input("Number of Days", min_value=1, max_value=365, value=30, step=1)
        
        submit_btn = st.form_submit_button("Launch Challenge", type="primary")
        
        if submit_btn:
            if not challenge_name.strip():
                st.error("Please provide a name for your challenge!")
            else:
                days = 30
                if duration_option == "7 Days":
                    days = 7
                elif duration_option == "30 Days":
                    days = 30
                elif duration_option == "60 Days":
                    days = 60
                else:
                    days = int(custom_days)
                
                st.session_state.challenge_name = challenge_name
                st.session_state.challenge_days = days
                st.session_state.completed = set()
                st.session_state.challenge_created = True
                save_state()
                st.rerun()

# --- CHALLENGE ACTIVE MODE ---
else:
    name = st.session_state.challenge_name
    total_days = st.session_state.challenge_days
    completed_set = st.session_state.completed
    
    completed_count = len(completed_set)
    remaining_count = max(0, total_days - completed_count)
    percentage = int((completed_count / total_days) * 100) if total_days > 0 else 0

    # 1. Challenge Info & Progress Banner
    progress_bar_html = f"""
        <div class="glass-card">
            <h3 style="margin-top: 0; font-size: 1.35rem; font-weight: 700; margin-bottom: 0.5rem; text-align: center;">{name}</h3>
            <div class="metrics-grid">
                <div class="metric-box">
                    <div class="metric-value">{completed_count}</div>
                    <div class="metric-label">Completed</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{remaining_count}</div>
                    <div class="metric-label">Remaining</div>
                </div>
                <div class="metric-box">
                    <div class="metric-value">{percentage}%</div>
                    <div class="metric-label">Progress</div>
                </div>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar-fill" style="width: {percentage}%;"></div>
            </div>
        </div>
    """
    st.markdown(progress_bar_html, unsafe_allow_html=True)

    # 2. Interactive Circle Grid
    grid_html = '<div class="circle-grid">'
    for i in range(1, total_days + 1):
        is_completed = i in completed_set
        class_name = "completed" if is_completed else "incomplete"
        grid_html += f'<a href="?toggle={i}" target="_self" class="circle-day {class_name}">{i}</a>'
    grid_html += '</div>'
    
    st.markdown(grid_html, unsafe_allow_html=True)

    # 3. Control Panel (Reset and New Challenge)
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Reset Progress", use_container_width=True, type="secondary"):
            st.session_state.completed = set()
            save_state()
            st.rerun()
            
    with col2:
        if st.button("New Challenge", use_container_width=True, type="secondary"):
            st.session_state.challenge_created = False
            save_state()
            st.rerun()

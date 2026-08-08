import streamlit as st
import database

AVATAR_PRESETS = [
    "🚀", "⚔️", "🧙‍♂️", "⚡", "🎯", "🧬", "👑", "💻", 
    "🎨", "📚", "🏋️‍♂️", "🦅", "💡", "🛡️", "🔥", "✨"
]

IDENTITY_PRESETS = [
    ("Student", "Pro Creator"),
    ("Junior Dev", "AI Systems Architect"),
    ("Freelancer", "Agency Founder"),
    ("Novice Writer", "Best-selling Author"),
    ("Fitness Beginner", "Elite Athlete"),
    ("Dreamer", "Relentless Builder")
]

def render_onboarding():
    st.markdown("""
    <div style="text-align: center; padding: 30px 0 10px 0;">
        <div style="font-size: 3rem; margin-bottom: 8px;">⚡</div>
        <h1 style="font-size: 2.2rem; font-weight: 800; letter-spacing: -1px; margin-bottom: 8px; color: #1C1C1E;">
            Welcome to LifeOS
        </h1>
        <p style="color: #8E8E93; font-size: 1.05rem; max-width: 520px; margin: 0 auto 20px auto;">
            Transform your life goals into an RPG quest system. Earn XP, level up, unlock real-world rewards, and visualize your evolution.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.subheader("👤 Create Your Character Profile")
        
        with st.form("onboarding_form"):
            col1, col2 = st.columns([2, 1])
            with col1:
                name = st.text_input("Character / Hero Name", placeholder="e.g. Alex Vance", value="Alex Vance")
            with col2:
                avatar = st.selectbox("Choose Avatar", AVATAR_PRESETS, index=0)

            st.markdown("---")
            st.markdown("#### 🔮 Identity Transformation Path")
            
            preset_choice = st.selectbox(
                "Quick Select Transformation Blueprint (or enter custom below)",
                ["Custom"] + [f"{c} ➔ {f}" for c, f in IDENTITY_PRESETS],
                index=0
            )

            if preset_choice != "Custom":
                default_curr, default_fut = preset_choice.split(" ➔ ")
            else:
                default_curr, default_fut = "Student / Novice", "Master Builder & Leader"

            c1, c2 = st.columns(2)
            with c1:
                current_identity = st.text_input("Current Identity", value=default_curr, help="Where you are starting right now")
            with c2:
                future_identity = st.text_input("Future Vision Identity", value=default_fut, help="Who you are transforming into")

            st.markdown("---")
            goal_duration = st.select_slider(
                "Primary Goal Duration Campaign",
                options=["30 Days", "60 Days", "90 Days", "180 Days", "1 Year"],
                value="90 Days"
            )

            submit_button = st.form_submit_button("⚡ Start Your Quest Journey")

            if submit_button:
                if not name.strip():
                    st.error("Please enter your character name.")
                else:
                    database.create_profile(name, avatar, current_identity, future_identity, goal_duration)
                    # Seed default goals & rewards
                    database.seed_default_data_if_empty()
                    st.success("Character Profile Created!")
                    st.rerun()

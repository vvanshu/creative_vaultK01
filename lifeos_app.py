import streamlit as st
import database
import styles

from components import onboarding, dashboard, goals, journey, rewards, review, profile_view

# Page Config
st.set_page_config(
    page_title="LifeOS - RPG Productivity",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Database
database.init_db()

# Inject Minimalist Light iOS Styling
styles.inject_styles()

def main():
    profile = database.get_profile()

    # If no profile exists, show onboarding
    if not profile:
        onboarding.render_onboarding()
        return

    level_info = database.calculate_level_info(profile["total_xp"])
    available_xp = profile["total_xp"] - profile["spent_xp"]

    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 10px 0 20px 0;">
            <div style="font-size: 2.4rem; line-height: 1;">{profile['avatar']}</div>
            <h2 style="font-size: 1.2rem; font-weight: 700; margin: 8px 0 2px 0;">{profile['name']}</h2>
            <div class="badge-blue" style="font-size: 0.8rem;">Lvl {level_info['level']} • {level_info['title']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='margin: 10px 0; border: none; border-top: 1px solid rgba(0,0,0,0.06);'>", unsafe_allow_html=True)

        page = st.radio(
            "Navigation",
            [
                "⚡ Quest Dashboard",
                "🎯 Goal Center",
                "🗺️ Journey Map",
                "🎁 Reward Store",
                "📝 Weekly Review",
                "👤 Character Profile"
            ],
            label_visibility="collapsed"
        )

        st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid rgba(0,0,0,0.06);'>", unsafe_allow_html=True)

        # Sidebar Stats Mini Card
        st.markdown(f"""
        <div class="ios-card-subtle">
            <div style="font-size: 0.8rem; color: #8E8E93; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px;">Character Stats</div>
            <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 0.9rem;">
                <span>Available XP:</span>
                <span style="font-weight: 700; color: #007AFF;">⚡ {available_xp}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 4px; font-size: 0.9rem;">
                <span>Total XP:</span>
                <span style="font-weight: 700; color: #34C759;">{profile['total_xp']}</span>
            </div>
            <div style="margin-top: 8px;">
                <div class="ios-progress-bg">
                    <div class="ios-progress-fill" style="width: {level_info['progress_pct'] * 100}%;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Render selected view
    if page == "⚡ Quest Dashboard":
        dashboard.render_dashboard()
    elif page == "🎯 Goal Center":
        goals.render_goals()
    elif page == "🗺️ Journey Map":
        journey.render_journey()
    elif page == "🎁 Reward Store":
        rewards.render_rewards()
    elif page == "📝 Weekly Review":
        review.render_review()
    elif page == "👤 Character Profile":
        profile_view.render_profile()

if __name__ == "__main__":
    main()

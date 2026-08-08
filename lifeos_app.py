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
            <div style="font-size: 2.6rem; line-height: 1;">{profile['avatar']}</div>
            <h2 style="font-size: 1.25rem; font-weight: 800; margin: 8px 0 2px 0; color: #0F172A;">{profile['name']}</h2>
            <div class="badge-blue" style="font-size: 0.85rem;">Lvl {level_info['level']} • {level_info['title']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='margin: 10px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

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

        st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

        # Sidebar Stats Mini Card
        st.markdown(f"""
        <div class="ios-sub-box">
            <div style="font-size: 0.8rem; color: #475569; text-transform: uppercase; font-weight: 800; letter-spacing: 0.5px;">Character Stats</div>
            <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 0.9rem;">
                <span style="color: #334155; font-weight: 600;">Available XP:</span>
                <span style="font-weight: 800; color: #0284C7;">⚡ {available_xp}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-top: 4px; font-size: 0.9rem;">
                <span style="color: #334155; font-weight: 600;">Total XP:</span>
                <span style="font-weight: 800; color: #16A34A;">{profile['total_xp']}</span>
            </div>
            <div style="margin-top: 8px;">
                <div class="ios-progress-bg">
                    <div class="ios-progress-fill" style="width: {level_info['progress_pct'] * 100}%;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Top Brand Header Bar
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between; padding: 14px 22px; background: #FFFFFF; border-radius: 16px; border: 1px solid #CBD5E1; box-shadow: 0 2px 10px rgba(0,0,0,0.03); margin-bottom: 24px;">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="width: 42px; height: 42px; border-radius: 12px; background: linear-gradient(135deg, #0284C7 0%, #6B21A8 100%); color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; box-shadow: 0 4px 10px rgba(2,132,199,0.25);">
                ⚡
            </div>
            <div>
                <h1 style="font-size: 1.4rem; font-weight: 800; margin: 0; color: #0F172A; letter-spacing: -0.5px; line-height: 1.2;">LifeOS</h1>
                <p style="font-size: 0.82rem; color: #475569; margin: 0; font-weight: 600;">Personal RPG Productivity & Identity Transformation Suite</p>
            </div>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
            <span class="badge-blue">⚡ RPG Engine</span>
            <span class="badge-green">iOS Minimalist</span>
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

import streamlit as st
import database

def render_profile():
    st.title("👤 Character & Settings")
    profile = database.get_profile()
    if not profile:
        return

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""
        <div class="ios-card" style="text-align: center;">
            <div class="avatar-container" style="margin: 0 auto 14px auto; width: 88px; height: 88px; font-size: 2.8rem;">
                {profile['avatar']}
            </div>
            <h2 style="margin: 0;">{profile['name']}</h2>
            <p style="color: #8E8E93; margin: 4px 0 14px 0;">{profile['goal_duration']} Horizon</p>
            <div class="badge-purple" style="font-size: 0.9rem;">Total XP: {profile['total_xp']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("Edit Transformation Blueprint")
        with st.form("edit_profile_form"):
            curr = st.text_input("Current Identity", value=profile["current_identity"])
            fut = st.text_input("Future Vision Identity", value=profile["future_identity"])
            av = st.text_input("Avatar Emoji", value=profile["avatar"])

            submitted = st.form_submit_button("Update Identity")
            if submitted:
                database.update_profile_identity(curr, fut, av)
                st.success("Identity profile updated!")
                st.rerun()

    st.markdown("---")
    st.subheader("📊 Audit Log & XP History")
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM xp_logs ORDER BY id DESC LIMIT 15")
    logs = [dict(r) for r in cursor.fetchall()]
    conn.close()

    if logs:
        for l in logs:
            badge = "badge-green" if l["action_type"] == "earn" else "badge-orange"
            prefix = "+" if l["action_type"] == "earn" else "-"
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 8px 14px; background: #FFFFFF; border-radius: 10px; margin-bottom: 6px; border: 1px solid rgba(0,0,0,0.04);">
                <span>{l['description']}</span>
                <span class="{badge}">{prefix}{l['xp_amount']} XP</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No XP activity logged yet.")

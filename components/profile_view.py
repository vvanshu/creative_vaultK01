import streamlit as st
import database

def render_profile():
    st.title("👤 Character Profile & Settings")
    profile = database.get_profile()
    if not profile:
        return

    col1, col2 = st.columns([1, 2])

    with col1:
        with st.container(border=True):
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="margin: 0 auto 12px auto; width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #0284C7 0%, #6B21A8 100%); color: white; display: flex; align-items: center; justify-content: center; font-size: 2.6rem;">
                    {profile['avatar']}
                </div>
                <h2 style="margin: 0; color: #0F172A;">{profile['name']}</h2>
                <p style="color: #64748B; margin: 4px 0 12px 0;">{profile['goal_duration']} Horizon</p>
                <div class="badge-purple" style="font-size: 0.9rem;">Total Earned: {profile['total_xp']} XP</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        with st.container(border=True):
            st.subheader("Edit Identity Blueprint")
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
    
    col_reset, col_logs = st.columns([1, 1.5])

    with col_reset:
        st.subheader("⚠️ Reset Options")
        with st.container(border=True):
            st.markdown("<h4 style='margin-top: 0; color: #C2410C;'>Soft Reset (Restart XP Progress)</h4>", unsafe_allow_html=True)
            st.write("Resets your total/available XP to 0 and unchecks completed quests back to active.")
            if st.button("🔄 Soft Reset Progress"):
                database.reset_progress(full_reset=False)
                st.toast("Progress reset to 0 XP!", icon="🔄")
                st.rerun()

            st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

            st.markdown("<h4 style='margin-top: 0; color: #DC2626;'>Full Reset (Wipe All Character Data)</h4>", unsafe_allow_html=True)
            st.write("Completely deletes character profile, goals, quests, and rewards to run onboarding fresh.")
            if st.button("🚨 Full Account Reset", help="Permanently deletes all data"):
                database.reset_progress(full_reset=True)
                st.toast("All account data reset. Starting onboarding...", icon="🧹")
                st.rerun()

    with col_logs:
        st.subheader("📊 Audit Log & XP History")
        with st.container(border=True):
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
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 12px; background: #F8FAFC; border-radius: 8px; margin-bottom: 6px; border: 1px solid #E2E8F0;">
                        <span style="font-weight: 500; font-size: 0.9rem; color: #0F172A;">{l['description']}</span>
                        <span class="{badge}">{prefix}{l['xp_amount']} XP</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No XP activity logged yet.")

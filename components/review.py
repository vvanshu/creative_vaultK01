import streamlit as st
import datetime
import database

def render_review():
    st.title("📝 Weekly Review & Reflection")
    st.write("Reflect on your performance, log obstacles, and set the upcoming week's focus.")

    # Auto generate week date string (e.g. Week of Aug 08, 2026)
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    week_str = f"Week of {start_of_week.strftime('%b %d, %Y')}"

    tab_current, tab_history = st.tabs(["✍️ Perform Review", "📜 Review Logs"])

    with tab_current:
        # Fetch auto summary of completed tasks
        completed_tasks = database.get_tasks(is_completed=True)
        auto_completed_text = "\n".join([f"• {t['title']} (+{t['xp_value']} XP)" for t in completed_tasks[:10]]) if completed_tasks else "No completed tasks logged this week yet."

        with st.form("weekly_review_form"):
            st.markdown(f"### 🗓️ Review for `{week_str}`")

            st.markdown("#### 1. What did I complete this week?")
            completed_summary = st.text_area(
                "Completed Achievements",
                value=f"Automated Task Highlights:\n{auto_completed_text}\n\nAdditional Wins:",
                height=130
            )

            st.markdown("#### 2. What failed or caused friction?")
            what_failed = st.text_area(
                "Obstacles, Bottlenecks & Distractions",
                placeholder="e.g. Got distracted on Tuesday, underestimated difficulty of module 2.",
                height=100
            )

            st.markdown("#### 3. What is next week's mission?")
            next_week_mission = st.text_area(
                "Primary Focus & Strategy",
                placeholder="e.g. Focus 100% on shipping MVP & running 3 user test sessions.",
                height=100
            )

            submitted = st.form_submit_button("📝 Submit Weekly Review")

            if submitted:
                database.create_weekly_review(
                    week_str, completed_summary.strip(),
                    what_failed.strip(), next_week_mission.strip()
                )
                # Award bonus XP for completing weekly review!
                database.update_xp(50, "earn", "Completed Weekly Review Bonus")
                st.toast("🎉 Weekly Review Saved! +50 Bonus XP Awarded!", icon="📝")
                st.success("Review logged successfully.")
                st.rerun()

    with tab_history:
        reviews = database.get_weekly_reviews()
        if not reviews:
            st.info("No past weekly reviews found. Perform your first review above!")
        else:
            for rev in reviews:
                st.markdown(f"""
                <div class="ios-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="badge-blue">{rev['week_start']}</span>
                        <span style="font-size: 0.8rem; color: #8E8E93;">Logged at {rev['created_at'][:10]}</span>
                    </div>
                    <div style="margin-top: 14px;">
                        <h4 style="color: #34C759; margin-bottom: 4px;">✅ Achievements & Completed Quests</h4>
                        <p style="white-space: pre-line; font-size: 0.95rem; margin: 0 0 14px 0;">{rev['completed_summary']}</p>
                        
                        <h4 style="color: #FF9500; margin-bottom: 4px;">⚠️ Obstacles & Failures</h4>
                        <p style="white-space: pre-line; font-size: 0.95rem; margin: 0 0 14px 0;">{rev['what_failed'] or 'None logged.'}</p>
                        
                        <h4 style="color: #007AFF; margin-bottom: 4px;">🎯 Next Week's Mission</h4>
                        <p style="white-space: pre-line; font-size: 0.95rem; margin: 0;">{rev['next_week_mission']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

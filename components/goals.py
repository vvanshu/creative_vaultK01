import streamlit as st
import database

def render_goals():
    st.title("🎯 Life Goals & Quest Breakdown")

    tab_view, tab_create = st.tabs(["📋 Active Goals", "➕ Create New Goal"])

    with tab_view:
        goals = database.get_goals()
        if not goals:
            st.info("No life goals created yet. Switch to 'Create New Goal' to craft your first mission!")
        else:
            for g in goals:
                st.markdown(f"""
                <div class="ios-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <span class="badge-purple">{g['category']}</span>
                            <span class="badge-blue" style="margin-left: 6px;">⏱️ {g['duration']}</span>
                            <h2 style="margin: 8px 0 4px 0;">{g['name']}</h2>
                            <p style="color: #8E8E93; font-size: 0.95rem; margin: 0;">
                                🏆 <b>Final Target:</b> {g['final_target']}
                            </p>
                        </div>
                        <div style="text-align: right;">
                            <span style="font-weight: 700; color: #007AFF; font-size: 1.1rem;">{g['hours_allocated']} hrs/week</span>
                        </div>
                    </div>
                    <hr style="margin: 16px 0; border: none; border-top: 1px solid rgba(0,0,0,0.06);">
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px;">
                        <div>
                            <h4 style="margin: 0 0 6px 0; font-size: 0.9rem; color: #8E8E93;">🗓️ Monthly Target</h4>
                            <p style="font-size: 0.95rem; font-weight: 500; margin: 0;">{g['monthly_target'] or 'Not set'}</p>
                        </div>
                        <div>
                            <h4 style="margin: 0 0 6px 0; font-size: 0.9rem; color: #8E8E93;">⚡ Weekly Actions</h4>
                            <p style="font-size: 0.95rem; font-weight: 500; margin: 0; white-space: pre-line;">{g['weekly_actions'] or 'Not set'}</p>
                        </div>
                        <div>
                            <h4 style="margin: 0 0 6px 0; font-size: 0.9rem; color: #8E8E93;">☀️ Daily Tasks</h4>
                            <p style="font-size: 0.95rem; font-weight: 500; margin: 0; white-space: pre-line;">{g['daily_tasks'] or 'Not set'}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Delete option
                if st.button(f"🗑️ Delete Goal '{g['name']}'", key=f"del_g_{g['id']}"):
                    database.delete_goal(g["id"])
                    st.rerun()

    with tab_create:
        st.subheader("Craft a New Life Goal")
        with st.form("create_goal_form"):
            c1, c2 = st.columns([2, 1])
            with c1:
                name = st.text_input("Goal Name", placeholder="e.g. Master Full-Stack AI Development")
            with c2:
                category = st.selectbox("Category", ["Career & Coding", "Health & Fitness", "Finance & Freedom", "Creative & Craft", "Mindset & Growth"])

            c_dur, c_hrs = st.columns(2)
            with c_dur:
                duration = st.selectbox("Duration Horizon", ["30 Days", "60 Days", "90 Days", "180 Days", "1 Year"])
            with c_hrs:
                hours_allocated = st.number_input("Weekly Hours Allocated", min_value=1.0, max_value=100.0, value=15.0, step=1.0)

            st.markdown("---")
            final_target = st.text_input("Final Target (Destination)", placeholder="e.g. Launch 3 AI apps with 500 monthly active users")
            monthly_target = st.text_input("Monthly Target (Milestone)", placeholder="e.g. Ship v1.0 MVP and set up analytics")

            col_w, col_d = st.columns(2)
            with col_w:
                weekly_actions = st.text_area("Weekly Actions (1 item per line)", placeholder="Ship 1 new core feature\nRun 2 user interview sessions")
            with col_d:
                daily_tasks = st.text_area("Daily Quests (1 item per line)", placeholder="Code for 2 focused hours\n1 Git commit\nRead 15 mins of documentation")

            submitted = st.form_submit_button("🎯 Create Goal & Seed Quests")

            if submitted:
                if not name.strip() or not final_target.strip():
                    st.error("Goal Name and Final Target are required.")
                else:
                    database.create_goal(
                        name.strip(), duration, final_target.strip(),
                        monthly_target.strip(), weekly_actions.strip(),
                        daily_tasks.strip(), hours_allocated, category
                    )
                    st.success("Goal successfully initialized with transformation journey stages!")
                    st.rerun()

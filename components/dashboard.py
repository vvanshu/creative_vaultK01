import streamlit as st
import database

def render_dashboard():
    profile = database.get_profile()
    if not profile:
        return

    level_info = database.calculate_level_info(profile["total_xp"])
    available_xp = profile["total_xp"] - profile["spent_xp"]

    # Profile & Character Banner Card
    st.markdown(f"""
    <div class="profile-banner">
        <div style="display: flex; align-items: center; gap: 18px; flex-wrap: wrap;">
            <div style="width: 68px; height: 68px; border-radius: 50%; background: linear-gradient(135deg, #007AFF 0%, #5856D6 100%); color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-size: 2rem; box-shadow: 0 4px 14px rgba(0,122,255,0.3);">
                {profile['avatar']}
            </div>
            <div style="flex-grow: 1;">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <span class="badge-blue">Level {level_info['level']} {level_info['title']}</span>
                        <h2 style="margin: 6px 0 2px 0;">{profile['name']}</h2>
                        <p style="color: #8E8E93; font-size: 0.95rem; margin: 0;">
                            Identity Evolution: <b>{profile['current_identity']}</b> ➔ <span style="color: #007AFF; font-weight: 600;">{profile['future_identity']}</span>
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.6rem; font-weight: 800; color: #007AFF;">⚡ {available_xp} <span style="font-size: 0.85rem; font-weight: 500; color: #8E8E93;">Available XP</span></div>
                        <div style="font-size: 0.85rem; color: #8E8E93;">Total Earned: <b>{profile['total_xp']} XP</b></div>
                    </div>
                </div>
                <div style="margin-top: 12px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #8E8E93; font-weight: 500;">
                        <span>Level Progress: {level_info['current_level_xp']} / {level_info['next_level_xp']} XP</span>
                        <span>{int(level_info['progress_pct'] * 100)}%</span>
                    </div>
                    <div class="ios-progress-bg">
                        <div class="ios-progress-fill" style="width: {level_info['progress_pct'] * 100}%;"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Core Dashboard Grid: Quests & Quick Add
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("⚔️ Active Quests & Daily Tasks")

        # Filter tabs
        filter_tab = st.radio(
            "Filter Quests",
            ["All Daily Tasks", "Weekly Actions", "Completed Tasks"],
            horizontal=True,
            label_visibility="collapsed"
        )

        is_comp_filter = True if filter_tab == "Completed Tasks" else False
        task_type_filter = "weekly" if filter_tab == "Weekly Actions" else ("daily" if filter_tab == "All Daily Tasks" else None)

        tasks = database.get_tasks(task_type=task_type_filter, is_completed=is_comp_filter)

        if not tasks:
            st.info("No active quests found. Add a new quest using the Quick Add form!")
        else:
            for task in tasks:
                task_id = task["id"]
                difficulty = task["difficulty"]
                xp_val = task["xp_value"]

                badge_class = "badge-blue" if difficulty == "Small" else ("badge-orange" if difficulty == "Medium" else "badge-purple")
                
                with st.container(border=True):
                    c_check, c_desc, c_meta, c_del = st.columns([0.5, 3.5, 1.2, 0.5])

                    with c_check:
                        checked = st.checkbox("", value=bool(task["is_completed"]), key=f"chk_{task_id}")
                        if checked != bool(task["is_completed"]):
                            database.toggle_task(task_id)
                            if checked:
                                st.toast(f"🎉 Quest Completed! Earned +{xp_val} XP!", icon="⚡")
                            st.rerun()

                    with c_desc:
                        st_style = "text-decoration: line-through; color: #8E8E93;" if task["is_completed"] else "font-weight: 600; color: #1C1C1E;"
                        goal_label = f" <span style='font-size: 0.8rem; color: #8E8E93;'>({task['goal_name']})</span>" if task.get("goal_name") else ""
                        st.markdown(f"<span style='{st_style}'>{task['title']}</span>{goal_label}", unsafe_allow_html=True)

                    with c_meta:
                        st.markdown(f"<span class='{badge_class}'>+{xp_val} XP</span>", unsafe_allow_html=True)

                    with c_del:
                        if st.button("✕", key=f"del_{task_id}", help="Delete quest"):
                            database.delete_task(task_id)
                            st.rerun()

    with col_right:
        st.subheader("➕ Quick Add Quest")
        with st.container(border=True):
            with st.form("quick_add_task_form"):
                task_title = st.text_input("Quest Description", placeholder="e.g. Code 45 mins")
                
                c_diff, c_type = st.columns(2)
                with c_diff:
                    difficulty = st.selectbox("Difficulty", ["Small (10 XP)", "Medium (30 XP)", "Large (100 XP)"], index=1)
                    diff_val = difficulty.split(" ")[0]
                with c_type:
                    task_type = st.selectbox("Type", ["daily", "weekly"], format_func=lambda x: x.capitalize())

                goals = database.get_goals()
                goal_options = {g["id"]: g["name"] for g in goals}
                selected_goal_id = None
                if goal_options:
                    selected_goal_id = st.selectbox("Link to Goal", options=list(goal_options.keys()), format_func=lambda x: goal_options[x])

                submitted = st.form_submit_button("⚡ Create Quest")

                if submitted:
                    if not task_title.strip():
                        st.warning("Please enter a quest description.")
                    else:
                        database.create_task(task_title.strip(), difficulty=diff_val, task_type=task_type, goal_id=selected_goal_id)
                        st.success("Quest created!")
                        st.rerun()

        # XP Difficulty Guide Card
        st.markdown("""
        <div class="ios-sub-box" style="margin-top: 16px;">
            <h4 style="margin-top: 0; font-size: 0.95rem;">⚡ XP Rules</h4>
            <div style="display: flex; flex-direction: column; gap: 6px; font-size: 0.85rem; color: #3A3A3C;">
                <div><span class="badge-blue">Small</span> Quick task (15-30m) = <b>10 XP</b></div>
                <div><span class="badge-orange">Medium</span> Focused effort (1-2h) = <b>30 XP</b></div>
                <div><span class="badge-purple">Large</span> Major milestone/deep work = <b>100 XP</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

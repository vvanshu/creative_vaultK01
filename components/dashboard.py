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
            <div style="width: 68px; height: 68px; border-radius: 50%; background: linear-gradient(135deg, #0284C7 0%, #6B21A8 100%); color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-size: 2rem; box-shadow: 0 4px 14px rgba(2,132,199,0.3);">
                {profile['avatar']}
            </div>
            <div style="flex-grow: 1;">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <span class="badge-blue">Level {level_info['level']} {level_info['title']}</span>
                        <h2 style="margin: 6px 0 2px 0;">{profile['name']}</h2>
                        <p style="color: #475569; font-size: 0.95rem; margin: 0;">
                            Identity Evolution: <b style="color: #0F172A;">{profile['current_identity']}</b> ➔ <span style="color: #0284C7; font-weight: 700;">{profile['future_identity']}</span>
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1.6rem; font-weight: 800; color: #0284C7;">⚡ {available_xp} <span style="font-size: 0.85rem; font-weight: 500; color: #475569;">Available XP</span></div>
                        <div style="font-size: 0.85rem; color: #475569;">Total Earned: <b>{profile['total_xp']} XP</b></div>
                    </div>
                </div>
                <div style="margin-top: 12px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.85rem; color: #475569; font-weight: 600;">
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
    col_left, col_right = st.columns([2.2, 1.2])

    with col_left:
        st.subheader("⚔️ Quest Dashboard")

        # Tabs for Active Quests vs Archive
        tab_active, tab_weekly, tab_archive = st.tabs(["⚡ Active Quests", "📅 Weekly Actions", "📦 Archive (Completed)"])

        with tab_active:
            tasks = database.get_tasks(task_type="daily", is_completed=False)
            if not tasks:
                st.info("No active daily quests! Create a new quest using the Quick Add form.")
            else:
                for task in tasks:
                    render_task_item(task, is_archive=False)

        with tab_weekly:
            tasks = database.get_tasks(task_type="weekly", is_completed=False)
            if not tasks:
                st.info("No active weekly actions.")
            else:
                for task in tasks:
                    render_task_item(task, is_archive=False)

        with tab_archive:
            completed_tasks = database.get_tasks(is_completed=True)
            if not completed_tasks:
                st.info("Archive is empty. Completed quests will appear here.")
            else:
                st.markdown("<p style='font-size: 0.85rem; color: #64748B;'>Uncheck any task below to restore it to active quests and update XP.</p>", unsafe_allow_html=True)
                for task in completed_tasks:
                    render_task_item(task, is_archive=True)

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
            <h4 style="margin-top: 0; font-size: 0.95rem; color: #0F172A;">⚡ XP Rules</h4>
            <div style="display: flex; flex-direction: column; gap: 8px; font-size: 0.85rem; color: #334155;">
                <div><span class="badge-blue">Small</span> Quick task (15-30m) = <b>10 XP</b></div>
                <div><span class="badge-orange">Medium</span> Focused effort (1-2h) = <b>30 XP</b></div>
                <div><span class="badge-purple">Large</span> Major milestone/deep work = <b>100 XP</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_task_item(task, is_archive=False):
    task_id = task["id"]
    difficulty = task["difficulty"]
    xp_val = task["xp_value"]

    badge_class = "badge-blue" if difficulty == "Small" else ("badge-orange" if difficulty == "Medium" else "badge-purple")

    with st.container(border=True):
        c_check, c_desc, c_meta, c_del = st.columns([0.5, 3.5, 1.2, 0.5])

        with c_check:
            checked = st.checkbox("", value=bool(task["is_completed"]), key=f"chk_{'arch_' if is_archive else ''}{task_id}")
            if checked != bool(task["is_completed"]):
                database.toggle_task(task_id)
                if checked:
                    st.toast(f"🎉 Quest Completed! Earned +{xp_val} XP!", icon="⚡")
                else:
                    st.toast(f"↩️ Quest Restored to Active! (-{xp_val} XP)", icon="↩️")
                st.rerun()

        with c_desc:
            st_style = "text-decoration: line-through; color: #64748B;" if task["is_completed"] else "font-weight: 700; color: #0F172A;"
            goal_label = f" <span style='font-size: 0.8rem; color: #64748B;'>({task['goal_name']})</span>" if task.get("goal_name") else ""
            date_label = f"<br/><span style='font-size: 0.75rem; color: #94A3B8;'>Completed: {task['completed_at'][:16]}</span>" if task.get("completed_at") else ""
            st.markdown(f"<span style='{st_style}'>{task['title']}</span>{goal_label}{date_label}", unsafe_allow_html=True)

        with c_meta:
            st.markdown(f"<span class='{badge_class}'>+{xp_val} XP</span>", unsafe_allow_html=True)

        with c_del:
            if st.button("✕", key=f"del_{'arch_' if is_archive else ''}{task_id}", help="Delete quest"):
                database.delete_task(task_id)
                st.rerun()

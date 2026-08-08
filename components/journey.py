import streamlit as st
import database

def render_journey():
    st.title("🗺️ Transformation Journey Map")
    st.write("Visualize your multi-stage identity evolution from novice to master.")

    profile = database.get_profile()
    goals = database.get_goals()

    if not goals:
        st.info("No active goals found. Create a goal to automatically construct your transformation pipeline!")
        return

    # Select goal
    goal_options = {g["id"]: g["name"] for g in goals}
    selected_goal_id = st.selectbox(
        "Select Goal Campaign Map",
        options=list(goal_options.keys()),
        format_func=lambda x: goal_options[x]
    )

    selected_goal = next(g for g in goals if g["id"] == selected_goal_id)
    stages = database.get_journey_stages(selected_goal_id)

    st.markdown(f"""
    <div class="ios-card" style="background: linear-gradient(135deg, #FFFFFF 0%, #F0F4FF 100%);">
        <span class="badge-blue">Identity Roadmap</span>
        <h2 style="margin: 8px 0;">{selected_goal['name']}</h2>
        <p style="color: #8E8E93; margin: 0;">
            Target Horizon: <b>{profile['current_identity']}</b> ➔ <b style="color: #007AFF;">{profile['future_identity']}</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📍 Journey Nodes")

    for idx, stage in enumerate(stages):
        is_completed = bool(stage["is_completed"])
        node_class = "completed" if is_completed else ("active" if idx == 0 or stages[idx-1]["is_completed"] else "")
        status_icon = "✅" if is_completed else ("🚀" if node_class == "active" else "🔒")
        status_label = "Completed Stage" if is_completed else ("Current Active Focus" if node_class == "active" else f"Locked ({stage['required_xp']} XP required)")

        col_icon, col_content, col_action = st.columns([0.6, 3.5, 1.2])

        with col_icon:
            st.markdown(f"""
            <div style="font-size: 2rem; text-align: center; margin-top: 10px;">
                {status_icon}
            </div>
            """, unsafe_allow_html=True)

        with col_content:
            st.markdown(f"""
            <div class="journey-node {node_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; color: #8E8E93;">
                        Stage {stage['stage_order']} • {status_label}
                    </span>
                </div>
                <h3 style="margin: 4px 0 2px 0;">{stage['title']}</h3>
                <p style="margin: 0; color: #3A3A3C; font-size: 0.95rem;">{stage['description']}</p>
            </div>
            """, unsafe_allow_html=True)

        with col_action:
            if not is_completed and node_class == "active":
                if st.button("Mark Complete 🎯", key=f"stage_btn_{stage['id']}"):
                    database.complete_journey_stage(stage["id"])
                    st.toast("🎉 Stage Cleared! Milestone Reached!", icon="🏆")
                    st.rerun()
            elif is_completed:
                st.markdown("<div style='margin-top: 25px; text-align: center;'><span class='badge-green'>Cleared</span></div>", unsafe_allow_html=True)

        if idx < len(stages) - 1:
            st.markdown("""
            <div style="text-align: center; color: #C7C7CC; font-size: 1.4rem; margin: -10px 0 10px 0;">
                ↓
            </div>
            """, unsafe_allow_html=True)

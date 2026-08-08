import streamlit as st
import database

def render_rewards():
    st.title("🎁 Reward Store & Perks")
    st.write("Exchange your earned XP for real-world rewards and perks.")

    profile = database.get_profile()
    if not profile:
        return

    available_xp = profile["total_xp"] - profile["spent_xp"]

    # Header Card with Available XP
    st.markdown(f"""
    <div class="ios-card" style="display: flex; justify-content: space-between; align-items: center; background: linear-gradient(135deg, #FFFFFF 0%, #FFF9F0 100%); border: 1px solid rgba(255, 149, 0, 0.2);">
        <div>
            <span class="badge-orange">Perk Vault</span>
            <h2 style="margin: 6px 0 0 0;">Unlock Rewards</h2>
            <p style="color: #8E8E93; margin: 4px 0 0 0; font-size: 0.95rem;">Treat yourself for consistent effort and completed quests.</p>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 2.2rem; font-weight: 800; color: #FF9500;">⚡ {available_xp}</div>
            <div style="font-size: 0.85rem; color: #8E8E93;">Available XP</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_shop, tab_create = st.tabs(["🛒 Available Rewards", "➕ Add Custom Reward"])

    with tab_shop:
        tier_filter = st.radio("Filter Tier", ["All", "Small", "Medium", "Big"], horizontal=True)
        tier_param = None if tier_filter == "All" else tier_filter

        rewards = database.get_rewards(tier=tier_param)

        if not rewards:
            st.info("No rewards in this tier. Create one under 'Add Custom Reward'!")
        else:
            cols = st.columns(2)
            for idx, reward in enumerate(rewards):
                with cols[idx % 2]:
                    r_id = reward["id"]
                    is_claimed = bool(reward["is_claimed"])
                    xp_cost = reward["xp_cost"]
                    tier = reward["tier"]

                    badge_class = "badge-blue" if tier == "Small" else ("badge-orange" if tier == "Medium" else "badge-purple")
                    can_afford = available_xp >= xp_cost and not is_claimed

                    st.markdown(f"""
                    <div class="ios-card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between; position: relative;">
                        <div>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span class="{badge_class}">{tier} Reward</span>
                                <span style="font-weight: 800; color: #FF9500; font-size: 1.1rem;">⚡ {xp_cost} XP</span>
                            </div>
                            <h3 style="margin: 12px 0 6px 0;">{reward['name']}</h3>
                            <p style="font-size: 0.85rem; color: #8E8E93; margin: 0;">
                                ⌛ Expiry / Availability: <b>{reward['expiry_date'] or 'Permanent'}</b>
                            </p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if is_claimed:
                        st.success(f"Claimed on {reward['claimed_at'][:10] if reward.get('claimed_at') else 'Recently'}")
                    else:
                        if st.button(f"Unlock for ⚡ {xp_cost} XP", key=f"claim_{r_id}", disabled=not can_afford):
                            success, msg = database.claim_reward(r_id)
                            if success:
                                st.balloons()
                                st.toast(f"🎉 Reward Unlocked: {reward['name']}!", icon="🎁")
                                st.rerun()
                            else:
                                st.error(msg)
                    
                    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    with tab_create:
        st.subheader("Create a Custom Reward")
        with st.form("create_reward_form"):
            r_name = st.text_input("Reward Name", placeholder="e.g. 15-min Espresso Break, Buy New Book, Cheat Meal")
            
            c_tier, c_cost = st.columns(2)
            with c_tier:
                tier = st.selectbox("Reward Tier", ["Small", "Medium", "Big"])
            with c_cost:
                default_cost = 50 if tier == "Small" else (250 if tier == "Medium" else 1000)
                xp_cost = st.number_input("XP Cost", min_value=10, max_value=10000, value=default_cost, step=10)

            expiry_date = st.text_input("Expiry Date / Condition", placeholder="e.g. Any Weekend, End of Month, Immediate")

            submitted = st.form_submit_button("🎁 Add Reward to Vault")

            if submitted:
                if not r_name.strip():
                    st.error("Reward Name is required.")
                else:
                    database.create_reward(r_name.strip(), tier, xp_cost, expiry_date.strip())
                    st.success("Custom Reward Added!")
                    st.rerun()

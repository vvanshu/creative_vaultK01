import streamlit as st
import random
import time
from datetime import datetime

# ==============================================================================
# PAGE CONFIGURATION & FELT TABLE STYLES
# ==============================================================================
st.set_page_config(
    page_title="Startup Sprint: Solitaire Card Table",
    page_icon="🦄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the Casino Felt / Solitaire Card Table
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Casino Green Felt Table Background */
    .stApp {
        background: radial-gradient(ellipse at center, #14462a 0%, #0a2918 70%, #05160c 100%);
        color: #f8fafc;
    }

    /* Top Bar Title */
    .table-title {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fef08a 0%, #fbbf24 50%, #f59e0b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
    }
    
    .table-subtitle {
        color: #86efac;
        font-size: 0.88rem;
        margin-bottom: 0.8rem;
        font-weight: 500;
    }

    /* Player Table Area */
    .player-board-container {
        background: rgba(10, 35, 20, 0.75);
        border: 2px solid rgba(251, 191, 36, 0.25);
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 12px;
        box-shadow: inset 0 0 15px rgba(0,0,0,0.5), 0 4px 12px rgba(0,0,0,0.4);
    }
    
    .player-board-active {
        border: 2px solid #fbbf24 !important;
        box-shadow: 0 0 18px rgba(251, 191, 36, 0.4), inset 0 0 15px rgba(0,0,0,0.5) !important;
        background: rgba(14, 50, 28, 0.9) !important;
    }

    /* Solitaire Card Slots */
    .slot-row {
        display: flex;
        gap: 8px;
        margin: 6px 0;
        justify-content: space-between;
    }

    .card-slot {
        flex: 1;
        min-height: 80px;
        border-radius: 8px;
        padding: 6px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        box-sizing: border-box;
        transition: all 0.2s ease;
    }

    /* Empty Dashed Slot */
    .slot-empty {
        border: 2px dashed rgba(134, 239, 172, 0.3);
        background: rgba(0, 0, 0, 0.25);
        color: #86efac;
        font-size: 0.72rem;
        font-weight: 600;
    }

    /* Physical Filled Solitaire Card */
    .slot-filled {
        background: #ffffff;
        color: #0f172a;
        border: 2px solid #cbd5e1;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255,255,255,0.9);
    }

    .slot-filled-locked {
        background: #faf5ff;
        color: #581c87;
        border: 2px solid #a855f7;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(168, 85, 247, 0.25);
    }

    .slot-filled-scale {
        background: #fffbeb;
        color: #78350f;
        border: 2px solid #f59e0b;
        border-radius: 8px;
    }

    .card-slot-title {
        font-weight: 800;
        font-size: 0.8rem;
        line-height: 1.1;
    }

    .card-slot-badge {
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        padding: 2px 4px;
        border-radius: 4px;
        margin-bottom: 2px;
        display: inline-block;
    }

    /* Physical Playing Card in Hand */
    .hand-card-box {
        background: #ffffff;
        color: #0f172a;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 10px;
        min-height: 125px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 6px 16px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,1);
        margin-bottom: 8px;
    }

    .hand-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 4px;
        margin-bottom: 4px;
    }

    .hand-card-type {
        font-size: 0.68rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    .hand-card-title {
        font-size: 0.92rem;
        font-weight: 800;
        color: #0f172a;
        margin: 2px 0;
    }

    .hand-card-desc {
        font-size: 0.72rem;
        color: #475569;
        line-height: 1.2;
    }

    /* Face-Down Deck Box */
    .deck-facedown {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e1b4b 100%);
        border: 2px solid #fbbf24;
        border-radius: 10px;
        padding: 14px;
        text-align: center;
        color: #fef08a;
        box-shadow: 0 8px 18px rgba(0,0,0,0.5), inset 0 0 10px rgba(0,0,0,0.6);
        min-height: 95px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    /* Face-Up Discard Box */
    .deck-faceup {
        background: #ffffff;
        border: 2px solid #cbd5e1;
        border-radius: 10px;
        padding: 14px;
        text-align: center;
        color: #0f172a;
        box-shadow: 0 8px 18px rgba(0,0,0,0.4);
        min-height: 95px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    /* Activity Feed Box */
    .felt-log-box {
        background: rgba(5, 22, 12, 0.9);
        border: 1px solid rgba(134, 239, 172, 0.3);
        border-radius: 10px;
        padding: 10px;
        max-height: 220px;
        overflow-y: auto;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
    }
    
    .felt-log-line {
        padding: 3px 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# DECK DEFINITION (54 Cards Total)
# ==============================================================================
CARD_SPECS = {
    # Phase 1: MVP (16 cards)
    "Idea": {
        "phase": 1,
        "type": "Phase 1: MVP",
        "type_color": "#0284c7",
        "icon": "💡",
        "title": "Idea",
        "desc": "Foundational spark. Pairs with Build for MVP.",
        "count": 8
    },
    "Build": {
        "phase": 1,
        "type": "Phase 1: MVP",
        "type_color": "#0284c7",
        "icon": "🛠️",
        "title": "Build",
        "desc": "Core prototype. Pairs with Idea for MVP.",
        "count": 8
    },
    # Phase 2: PMF (14 cards)
    "User": {
        "phase": 2,
        "type": "Phase 2: PMF",
        "type_color": "#9333ea",
        "icon": "👥",
        "title": "User",
        "desc": "Active customer base. Pairs with Traction.",
        "count": 7
    },
    "Traction": {
        "phase": 2,
        "type": "Phase 2: PMF",
        "type_color": "#9333ea",
        "icon": "🚀",
        "title": "Traction 🔒",
        "desc": "Locks Stage! Secures Phase 1 & 2 permanently.",
        "count": 7
    },
    # Phase 3: Scale (12 cards)
    "Investment": {
        "phase": 3,
        "type": "Phase 3: Scale",
        "type_color": "#d97706",
        "icon": "💰",
        "title": "Investment",
        "desc": "+1 Scale. Dilutes Founder Equity by -10%.",
        "count": 6
    },
    "Revenue": {
        "phase": 3,
        "type": "Phase 3: Scale",
        "type_color": "#16a34a",
        "icon": "📈",
        "title": "Revenue",
        "desc": "+1 Scale. Recovers +10% Equity (max 100%).",
        "count": 6
    },
    # Actions & Victory (12 cards)
    "Grand Exit": {
        "phase": 4,
        "type": "Victory Trigger",
        "type_color": "#10b981",
        "icon": "🦄",
        "title": "Grand Exit",
        "desc": "WIN! Needs Phase 1, 2, 3 (≥1 Inv & ≥1 Rev) + ≥80% Equity.",
        "count": 4
    },
    "Competitor Steal": {
        "phase": 0,
        "type": "Espionage Action",
        "type_color": "#e11d48",
        "icon": "🥷",
        "title": "Comp Steal",
        "desc": "Steals 1 card from an unlocked opponent's MVP board.",
        "count": 3
    },
    "Shield / Block": {
        "phase": 0,
        "type": "Defense Asset",
        "type_color": "#2563eb",
        "icon": "🛡️",
        "title": "Shield / Block",
        "desc": "Held in hand or activated. Automatically blocks Steals!",
        "count": 3
    },
    "Pivot": {
        "phase": 0,
        "type": "Strategy Action",
        "type_color": "#475569",
        "icon": "🔄",
        "title": "Pivot",
        "desc": "Swaps 1 card on your board with the top draw card.",
        "count": 2
    }
}

def generate_deck():
    deck = []
    for card_name, spec in CARD_SPECS.items():
        deck.extend([card_name] * spec["count"])
    random.shuffle(deck)
    return deck

# ==============================================================================
# GAME STATE INITIALIZATION
# ==============================================================================
def init_game(player_count=4, human_name="Founder", local_multi=False):
    deck = generate_deck()
    players = []
    
    bot_roster = ["Byte Capital (AI)", "Nexus Ventures (AI)", "Apex Syndicate (AI)"]
    
    for i in range(player_count):
        if i == 0 or local_multi:
            name = human_name if i == 0 else f"Founder {i+1}"
            is_bot = False
        else:
            name = bot_roster[i-1] if (i-1) < len(bot_roster) else f"AI Bot {i+1}"
            is_bot = True
            
        hand = [deck.pop() for _ in range(4)] if len(deck) >= 4 else []
        
        players.append({
            "id": i,
            "name": name,
            "is_bot": is_bot,
            "hand": hand,
            "phase1": {"idea": False, "build": False},
            "phase2": {"user": False, "traction": False},
            "phase3": {"investment_count": 0, "revenue_count": 0},
            "equity": 100,
            "is_locked": False,
            "has_shield": False,
            "actions_left": 2
        })
        
    st.session_state.game_started = True
    st.session_state.round_num = 1
    st.session_state.current_idx = 0
    st.session_state.deck = deck
    st.session_state.discard_pile = []
    st.session_state.players = players
    st.session_state.logs = []
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.pending_action = None
    
    add_game_log("🏁 Table opened! 54-card deck shuffled and dealt.", "gold")
    # Draw initial turn cards
    draw_cards(st.session_state.players[0], 2)

def add_game_log(msg, color="white"):
    t_str = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.insert(0, {"time": t_str, "msg": msg, "color": color})

def recycle_deck():
    if len(st.session_state.deck) == 0:
        if len(st.session_state.discard_pile) > 0:
            st.session_state.deck = st.session_state.discard_pile.copy()
            random.shuffle(st.session_state.deck)
            st.session_state.discard_pile = []
            add_game_log("♻️ Draw deck was empty! Discard pile shuffled back into deck.", "#a855f7")

def draw_cards(player, count=2):
    drawn = []
    for _ in range(count):
        recycle_deck()
        if st.session_state.deck:
            c = st.session_state.deck.pop()
            player["hand"].append(c)
            drawn.append(c)
    if drawn:
        if player["is_bot"]:
            add_game_log(f"📥 {player['name']} drew {len(drawn)} cards from deck.", "#94a3b8")
        else:
            add_game_log(f"📥 {player['name']} drew: {', '.join(drawn)}", "#67e8f9")

# ==============================================================================
# GAME ENGINE & VALIDATION RULES
# ==============================================================================
def check_p1_done(p):
    return p["phase1"]["idea"] and p["phase1"]["build"]

def check_p2_done(p):
    return p["phase2"]["user"] and p["phase2"]["traction"]

def check_p3_done(p):
    return p["phase3"]["investment_count"] >= 1 and p["phase3"]["revenue_count"] >= 1

def can_exit(p):
    return check_p1_done(p) and check_p2_done(p) and check_p3_done(p) and (p["equity"] >= 80)

def play_card_action(player_idx, card_name, target_data=None):
    p = st.session_state.players[player_idx]
    if card_name not in p["hand"]:
        return False, "Card is not in your hand."
    if p["actions_left"] <= 0:
        return False, "No actions remaining this turn."
        
    success = False
    log_msg = ""
    log_col = "white"

    # Phase 1
    if card_name == "Idea":
        if p["phase1"]["idea"]:
            return False, "You already have an Idea card placed in Slot 1."
        p["phase1"]["idea"] = True
        p["hand"].remove(card_name)
        success = True
        log_msg = f"💡 {p['name']} placed [Idea] in Phase 1 MVP."
        log_col = "#38bdf8"
        if check_p1_done(p):
            log_msg += " 🎯 Phase 1 MVP complete!"

    elif card_name == "Build":
        if p["phase1"]["build"]:
            return False, "You already have a Build card placed in Slot 2."
        p["phase1"]["build"] = True
        p["hand"].remove(card_name)
        success = True
        log_msg = f"🛠️ {p['name']} placed [Build] in Phase 1 MVP."
        log_col = "#38bdf8"
        if check_p1_done(p):
            log_msg += " 🎯 Phase 1 MVP complete!"

    # Phase 2
    elif card_name == "User":
        if not check_p1_done(p):
            return False, "Must complete Phase 1 (Idea + Build) before placing Phase 2 cards!"
        if p["phase2"]["user"]:
            return False, "You already have a User card placed in Slot 3."
        p["phase2"]["user"] = True
        p["hand"].remove(card_name)
        success = True
        log_msg = f"👥 {p['name']} placed [User] in Phase 2 PMF."
        log_col = "#c084fc"
        if check_p2_done(p):
            p["is_locked"] = True
            log_msg += " 🔒 PMF STAGE LOCKED! Phase 1 & 2 immune to steals."
            log_col = "#a855f7"

    elif card_name == "Traction":
        if not check_p1_done(p):
            return False, "Must complete Phase 1 (Idea + Build) before placing Phase 2 cards!"
        if p["phase2"]["traction"]:
            return False, "You already have Traction placed in Slot 4."
        p["phase2"]["traction"] = True
        p["hand"].remove(card_name)
        success = True
        log_msg = f"🚀 {p['name']} placed [Traction] in Phase 2 PMF."
        log_col = "#c084fc"
        if check_p2_done(p):
            p["is_locked"] = True
            log_msg += " 🔒 PMF STAGE LOCKED! Phase 1 & 2 immune to steals."
            log_col = "#a855f7"

    # Phase 3
    elif card_name == "Investment":
        if not check_p2_done(p):
            return False, "Must complete Phase 2 (User + Traction) before scaling Phase 3!"
        p["phase3"]["investment_count"] += 1
        p["equity"] = max(0, p["equity"] - 10)
        p["hand"].remove(card_name)
        success = True
        log_msg = f"💰 {p['name']} added [Investment] to Slot 5 (-10% Equity -> {p['equity']}%)."
        log_col = "#fbbf24"

    elif card_name == "Revenue":
        if not check_p2_done(p):
            return False, "Must complete Phase 2 (User + Traction) before scaling Phase 3!"
        p["phase3"]["revenue_count"] += 1
        p["equity"] = min(100, p["equity"] + 10)
        p["hand"].remove(card_name)
        success = True
        log_msg = f"📈 {p['name']} added [Revenue] to Slot 6 (+10% Equity recovered -> {p['equity']}%)."
        log_col = "#4ade80"

    # Actions
    elif card_name == "Shield / Block":
        p["has_shield"] = True
        p["hand"].remove(card_name)
        success = True
        log_msg = f"🛡️ {p['name']} activated [Shield] defense against espionage!"
        log_col = "#60a5fa"

    elif card_name == "Competitor Steal":
        if not target_data:
            return False, "Steal target data missing."
        target_pid = target_data.get("target_pid")
        target_slot = target_data.get("target_slot")
        
        target_p = st.session_state.players[target_pid]
        if target_p["is_locked"]:
            return False, f"{target_p['name']} is PMF Locked! Protected from steals."
        if not target_p["phase1"].get(target_slot, False):
            return False, f"{target_p['name']} does not have that card in Phase 1."
            
        p["hand"].remove(card_name)
        st.session_state.discard_pile.append(card_name)
        
        # Check shield defense
        if target_p["has_shield"]:
            target_p["has_shield"] = False
            add_game_log(f"🛡️ {target_p['name']}'s Active Shield deflected {p['name']}'s Steal!", "#60a5fa")
            p["actions_left"] -= 1
            return True, "Steal blocked by Active Shield!"
        elif "Shield / Block" in target_p["hand"]:
            target_p["hand"].remove("Shield / Block")
            st.session_state.discard_pile.append("Shield / Block")
            add_game_log(f"🛡️ {target_p['name']} countered {p['name']}'s Steal with a Shield from hand!", "#60a5fa")
            p["actions_left"] -= 1
            return True, "Steal countered by Shield card in hand!"
        else:
            target_p["phase1"][target_slot] = False
            stolen_c = "Idea" if target_slot == "idea" else "Build"
            p["hand"].append(stolen_c)
            success = True
            log_msg = f"🥷 {p['name']} stole [{stolen_c}] from {target_p['name']}'s board!"
            log_col = "#f43f5e"

    elif card_name == "Pivot":
        if not target_data or "slot" not in target_data:
            return False, "Need slot selection to pivot."
        slot_key = target_data["slot"]
        
        recycle_deck()
        if not st.session_state.deck:
            return False, "Draw deck is empty."
            
        new_card = st.session_state.deck.pop()
        p["hand"].remove(card_name)
        st.session_state.discard_pile.append(card_name)
        
        if slot_key == "idea" and p["phase1"]["idea"] and not p["is_locked"]:
            p["phase1"]["idea"] = False
            st.session_state.discard_pile.append("Idea")
        elif slot_key == "build" and p["phase1"]["build"] and not p["is_locked"]:
            p["phase1"]["build"] = False
            st.session_state.discard_pile.append("Build")
        elif slot_key == "investment" and p["phase3"]["investment_count"] > 0:
            p["phase3"]["investment_count"] -= 1
            p["equity"] = min(100, p["equity"] + 10)
            st.session_state.discard_pile.append("Investment")
        elif slot_key == "revenue" and p["phase3"]["revenue_count"] > 0:
            p["phase3"]["revenue_count"] -= 1
            p["equity"] = max(0, p["equity"] - 10)
            st.session_state.discard_pile.append("Revenue")
            
        p["hand"].append(new_card)
        success = True
        log_msg = f"🔄 {p['name']} pivoted [{slot_key}] slot and drew [{new_card}] from the deck!"
        log_col = "#cbd5e1"

    # Victory Exit
    elif card_name == "Grand Exit":
        if not can_exit(p):
            if p["equity"] < 80:
                return False, f"Founder Equity is at {p['equity']}%. Need ≥ 80% to claim Grand Exit!"
            return False, "Need all 3 Phases completed (MVP + PMF + Scale ≥1 Inv & ≥1 Rev)!"
            
        p["hand"].remove(card_name)
        st.session_state.game_over = True
        st.session_state.winner = p["name"]
        success = True
        log_msg = f"🏆🦄 {p['name']} PLAYED GRAND EXIT! UNICORN RACE WON AT {p['equity']}% EQUITY!"
        log_col = "#facc15"

    if success:
        p["actions_left"] -= 1
        add_game_log(log_msg, log_col)
        return True, log_msg
        
    return False, "Could not execute action."

def discard_card_action(player_idx, card_name):
    p = st.session_state.players[player_idx]
    if card_name in p["hand"]:
        p["hand"].remove(card_name)
        st.session_state.discard_pile.append(card_name)
        p["actions_left"] -= 1
        add_game_log(f"🗑️ {p['name']} discarded [{card_name}].", "#94a3b8")
        return True
    return False

def end_player_turn():
    num_p = len(st.session_state.players)
    curr_idx = st.session_state.current_idx
    
    st.session_state.players[curr_idx]["actions_left"] = 2
    next_idx = (curr_idx + 1) % num_p
    
    if next_idx == 0:
        st.session_state.round_num += 1
        add_game_log(f"=== 🏁 Round {st.session_state.round_num} Started ===", "#e2e8f0")
        
    st.session_state.current_idx = next_idx
    next_p = st.session_state.players[next_idx]
    next_p["actions_left"] = 2
    
    draw_cards(next_p, 2)
    st.session_state.pending_action = None

# ==============================================================================
# RULE-BASED BOT DECISION ENGINE
# ==============================================================================
def execute_bot_turn(bot_idx):
    bot = st.session_state.players[bot_idx]
    if st.session_state.game_over:
        return
        
    while bot["actions_left"] > 0 and not st.session_state.game_over:
        hand = bot["hand"]
        
        # 1. Grand Exit
        if "Grand Exit" in hand and can_exit(bot):
            play_card_action(bot_idx, "Grand Exit")
            return
            
        # 2. Fix Equity if < 80% with Revenue
        if bot["equity"] < 80 and "Revenue" in hand and check_p2_done(bot):
            ok, _ = play_card_action(bot_idx, "Revenue")
            if ok: continue
            
        # 3. Build Phase 1
        if not bot["phase1"]["idea"] and "Idea" in hand:
            ok, _ = play_card_action(bot_idx, "Idea")
            if ok: continue
        if not bot["phase1"]["build"] and "Build" in hand:
            ok, _ = play_card_action(bot_idx, "Build")
            if ok: continue
            
        # 4. Build Phase 2 (if Phase 1 is done)
        if check_p1_done(bot):
            if not bot["phase2"]["user"] and "User" in hand:
                ok, _ = play_card_action(bot_idx, "User")
                if ok: continue
            if not bot["phase2"]["traction"] and "Traction" in hand:
                ok, _ = play_card_action(bot_idx, "Traction")
                if ok: continue
                
        # 5. Build Phase 3 (if Phase 2 is done)
        if check_p2_done(bot):
            if bot["phase3"]["revenue_count"] == 0 and "Revenue" in hand:
                ok, _ = play_card_action(bot_idx, "Revenue")
                if ok: continue
            if bot["phase3"]["investment_count"] == 0 and "Investment" in hand and bot["equity"] >= 80:
                ok, _ = play_card_action(bot_idx, "Investment")
                if ok: continue
            if "Revenue" in hand and bot["equity"] < 100:
                ok, _ = play_card_action(bot_idx, "Revenue")
                if ok: continue
                
        # 6. Activate Shield
        if "Shield / Block" in hand and not bot["has_shield"]:
            ok, _ = play_card_action(bot_idx, "Shield / Block")
            if ok: continue
            
        # 7. Steal from leading unlocked opponent
        if "Competitor Steal" in hand:
            targets = []
            for op in st.session_state.players:
                if op["id"] != bot["id"] and not op["is_locked"]:
                    if op["phase1"]["idea"]:
                        targets.append((op["id"], "idea"))
                    elif op["phase1"]["build"]:
                        targets.append((op["id"], "build"))
            if targets:
                ok, _ = play_card_action(bot_idx, "Competitor Steal", {"target_pid": targets[0][0], "target_slot": targets[0][1]})
                if ok: continue
                
        # 8. Investment if safe
        if "Investment" in hand and check_p2_done(bot) and bot["equity"] > 80:
            ok, _ = play_card_action(bot_idx, "Investment")
            if ok: continue
            
        # 9. Discard duplicate / excess card
        if hand:
            discard_card_action(bot_idx, hand[0])
        else:
            bot["actions_left"] = 0
            break
            
    end_player_turn()

# ==============================================================================
# HELPER: RENDER SOLITAIRE SLOT HTML
# ==============================================================================
def render_slot_html(filled, title, icon, badge_text, slot_type="mvp", extra_info=""):
    if not filled:
        return f'<div class="card-slot slot-empty"><div>{icon}</div><div>+ {title}</div></div>'
    
    if slot_type == "locked":
        cls = "slot-filled-locked"
        bg_col = "#f3e8ff"
        tx_col = "#6b21a8"
    elif slot_type == "scale":
        cls = "slot-filled-scale"
        bg_col = "#fef3c7"
        tx_col = "#92400e"
    else:
        cls = "slot-filled"
        bg_col = "#e0f2fe"
        tx_col = "#0369a1"

    extra_markup = f'<div style="font-size:0.65rem; color:#475569; margin-top:2px;">{extra_info}</div>' if extra_info else ''
    return f'<div class="card-slot {cls}"><span class="card-slot-badge" style="background:{bg_col}; color:{tx_col};">{badge_text}</span><div class="card-slot-title">{icon} {title}</div>{extra_markup}</div>'

# ==============================================================================
# SIDEBAR CONTROLS & RULES
# ==============================================================================
with st.sidebar:
    st.markdown("### 🎲 Table Options")
    
    if not st.session_state.get("game_started", False):
        p_count = st.radio("Total Players (1 Human + AI Bots)", [2, 3, 4], index=2, horizontal=True)
        f_name = st.text_input("Your Founder Name", value="VentureLead", max_chars=18)
        local_mode = st.checkbox("Local Pass & Play (All Human)", value=False)
        
        if st.button("🚀 Deal Cards & Start Game", type="primary", use_container_width=True):
            init_game(player_count=p_count, human_name=f_name, local_multi=local_mode)
            st.rerun()
    else:
        active_p = st.session_state.players[st.session_state.current_idx]
        st.info(f"**Turn:** Round {st.session_state.round_num}\n\n**Active:** {active_p['name']} ({active_p['actions_left']} actions left)")
        
        if st.button("🔄 Reset / New Table", use_container_width=True):
            st.session_state.game_started = False
            st.session_state.game_over = False
            st.rerun()

    st.markdown("---")
    st.markdown("### 📖 Solitaire Stage Rules")
    with st.expander("🔍 Rule Cheat Sheet", expanded=False):
        st.markdown("""
        **1. Phase 1 (MVP Slots 1 & 2):**
        - Needs **💡 Idea** + **🛠️ Build**.
        - *Vulnerable* to rival Competitor Steals!
        
        **2. Phase 2 (PMF Slots 3 & 4):**
        - Needs **👥 User** + **🚀 Traction**.
        - **🔒 Stage Lock:** Once placed, Phase 1 & 2 are permanently immune to theft!
        
        **3. Phase 3 (Scale Slots 5 & 6):**
        - **💰 Investment:** +1 Scale, -10% Equity.
        - **📈 Revenue:** +1 Scale, +10% Equity recovery.
        
        **4. Grand Exit 🦄 (Victory Condition):**
        - All 6 slots completed + **Grand Exit** card played + **≥ 80% Founder Equity**!
        """)

# ==============================================================================
# MAIN VIEW ROUTING
# ==============================================================================
if not st.session_state.get("game_started", False):
    # Welcome Lobby Screen
    st.markdown('<div class="table-title">🦄 Startup Sprint: Solitaire Card Table</div>', unsafe_allow_html=True)
    st.markdown('<div class="table-subtitle">Digital Card Table Game: Outbuild rivals, lock in PMF, balance equity, and exit!</div>', unsafe_allow_html=True)
    
    col_l1, col_l2 = st.columns([3, 2])
    with col_l1:
        st.markdown("""
        ### Welcome to the Card Table, Founder! 🃏
        Experience startup building reimagined as a digital Solitaire card race:
        
        - 💡 **Fill MVP Slots:** Pair *Idea* and *Build* cards.
        - 🔒 **Lock PMF Slots:** Deploy *User* and *Traction* to permanently lock your board against rival steals.
        - 📈 **Balance Scale Slots:** Manage *Investments* and *Revenue* to stay **≥ 80% Founder Equity**.
        - 🦄 **Grand Exit:** Trigger victory when all foundations are met!
        
        👉 **Select your player count in the sidebar and click 'Deal Cards & Start Game'!**
        """)
    with col_l2:
        st.markdown("""
        <div style="background: rgba(10,35,20,0.85); border: 2px solid #fbbf24; border-radius: 12px; padding: 20px; text-align: center;">
            <div style="font-size: 3rem;">🦄</div>
            <h3 style="color: #fef08a; margin: 4px 0;">54-Card Stateful Deck</h3>
            <p style="color: #86efac; font-size: 0.85rem;">16 MVP Cards • 14 PMF Cards • 12 Scale Cards • 12 Action/Win Cards</p>
        </div>
        """, unsafe_allow_html=True)
else:
    # ==============================================================================
    # ACTIVE SOLITAIRE CARD TABLE VIEW
    # ==============================================================================
    st.markdown('<div class="table-title">🦄 Startup Sprint: Solitaire Card Table</div>', unsafe_allow_html=True)

    # Top Bar Game Status
    active_player = st.session_state.players[st.session_state.current_idx]
    bar_c1, bar_c2, bar_c3 = st.columns([3, 2, 2])

    with bar_c1:
        turn_txt = f"🔥 **Active Turn:** `{active_player['name']}`"
        if active_player["is_bot"]:
            turn_txt += " *(AI Thinking...)*"
        st.markdown(turn_txt)
    with bar_c2:
        st.markdown(f"⚡ **Actions Remaining:** `{active_player['actions_left']} / 2`")
    with bar_c3:
        st.markdown(f"🏁 **Round:** `{st.session_state.round_num}`")

    st.markdown("---")

    # Winner Modal / Celebration
    if st.session_state.game_over:
        st.balloons()
        st.success(f"🎉🏆 **VICTORY!** {st.session_state.winner} has achieved a legendary Unicorn Grand Exit! 🚀🦄")
        if st.button("🏆 Start New Game", type="primary"):
            st.session_state.game_started = False
            st.rerun()

    # ------------------------------------------------------------------------------
    # 1. PLAYER SOLITAIRE BOARDS (Arena Grid)
    # ------------------------------------------------------------------------------
    num_players = len(st.session_state.players)
    player_cols = st.columns(num_players)

    for i, p in enumerate(st.session_state.players):
        with player_cols[i]:
            is_curr = (i == st.session_state.current_idx)
            container_class = "player-board-container player-board-active" if is_curr else "player-board-container"
            
            # Player Header
            crown = "👑" if i == 0 else "🤖"
            shield_txt = "🛡️ Protected" if p["has_shield"] else "None"
            lock_txt = "🔒 PMF LOCKED" if p["is_locked"] else "🔓 Stage Open"
            
            st.markdown(f"""
            <div class="{container_class}">
                <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:4px; margin-bottom:6px;">
                    <div style="font-weight:800; font-size:1.05rem; color:#fef08a;">{crown} {p['name']}</div>
                    <div style="font-size:0.72rem; color:#86efac;">{lock_txt}</div>
                </div>
                <div style="font-size:0.75rem; color:#94a3b8; margin-bottom:6px;">
                    Hand: <strong>{len(p['hand'])} cards</strong> | Shield: <strong>{shield_txt}</strong>
                </div>
            """, unsafe_allow_html=True)
            
            # Solitaire Slots: Phase 1 (MVP)
            s1_html = render_slot_html(p["phase1"]["idea"], "Idea", "💡", "Slot 1: MVP", "mvp")
            s2_html = render_slot_html(p["phase1"]["build"], "Build", "🛠️", "Slot 2: MVP", "mvp")
            st.markdown(f'<div class="slot-row">{s1_html}{s2_html}</div>', unsafe_allow_html=True)
            
            # Solitaire Slots: Phase 2 (PMF)
            s3_html = render_slot_html(p["phase2"]["user"], "User", "👥", "Slot 3: PMF", "locked" if p["is_locked"] else "mvp")
            s4_html = render_slot_html(p["phase2"]["traction"], "Traction", "🚀", "Slot 4: PMF 🔒", "locked" if p["is_locked"] else "mvp")
            st.markdown(f'<div class="slot-row">{s3_html}{s4_html}</div>', unsafe_allow_html=True)
            
            # Solitaire Slots: Phase 3 (Scale)
            inv_cnt = p["phase3"]["investment_count"]
            rev_cnt = p["phase3"]["revenue_count"]
            s5_html = render_slot_html(inv_cnt > 0, f"Invest ({inv_cnt}x)", "💰", "Slot 5: Scale", "scale", f"-{inv_cnt*10}% Equity" if inv_cnt > 0 else "")
            s6_html = render_slot_html(rev_cnt > 0, f"Revenue ({rev_cnt}x)", "📈", "Slot 6: Scale", "scale", f"+{rev_cnt*10}% Equity" if rev_cnt > 0 else "")
            st.markdown(f'<div class="slot-row">{s5_html}{s6_html}</div>', unsafe_allow_html=True)
            
            # Founder Equity Progress Bar
            eq = p["equity"]
            if eq >= 90:
                eq_status = f"🟢 {eq}% Equity (Safe)"
            elif eq >= 80:
                eq_status = f"🟡 {eq}% Equity (Borderline)"
            else:
                eq_status = f"🔴 {eq}% Equity (Disqualified <80%)"
                
            st.caption(f"Founder Equity: **{eq_status}**")
            st.progress(eq / 100.0)
            
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ------------------------------------------------------------------------------
    # 2. CENTER TABLE: DECK & DISCARD PILE
    # ------------------------------------------------------------------------------
    deck_count = len(st.session_state.deck)
    discard_count = len(st.session_state.discard_pile)
    top_discard = st.session_state.discard_pile[-1] if discard_count > 0 else "None"
    top_spec = CARD_SPECS.get(top_discard, {"icon": "🎴", "type": "Empty"})

    col_d1, col_d2, col_d3 = st.columns([2, 2, 4])

    with col_d1:
        st.markdown(f"""
        <div class="deck-facedown">
            <div style="font-size:1.4rem;">🎴</div>
            <div style="font-weight:800; font-size:0.95rem; margin-top:2px;">DRAW DECK</div>
            <div style="font-size:0.8rem; color:#86efac; font-weight:700;">{deck_count} cards remaining</div>
        </div>
        """, unsafe_allow_html=True)

    with col_d2:
        st.markdown(f"""
        <div class="deck-faceup">
            <div style="font-size:1.4rem;">{top_spec['icon']}</div>
            <div style="font-weight:800; font-size:0.95rem; margin-top:2px;">{top_discard}</div>
            <div style="font-size:0.75rem; color:#64748b;">Discard Pile ({discard_count})</div>
        </div>
        """, unsafe_allow_html=True)

    with col_d3:
        st.markdown(f"""
        <div style="background: rgba(10,35,20,0.6); border: 1px solid rgba(134,239,172,0.25); border-radius: 10px; padding: 12px; height: 95px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-weight:700; font-size:0.85rem; color:#fef08a;">💡 Founder Strategy Tip</div>
            <div style="font-size:0.75rem; color:#cbd5e1; margin-top:3px;">
                Place <strong>Idea</strong> & <strong>Build</strong> to unlock Phase 2. Once <strong>User</strong> & <strong>Traction</strong> are placed, your startup is permanently locked from competitor espionage!
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ------------------------------------------------------------------------------
    # 3. INTERACTIVE CONTROLS / HUMAN HAND / BOT EXECUTION
    # ------------------------------------------------------------------------------
    if not st.session_state.game_over:
        if active_player["is_bot"]:
            st.info(f"🤖 **{active_player['name']} is evaluating the board and taking actions...**")
            time.sleep(0.5)
            execute_bot_turn(st.session_state.current_idx)
            st.rerun()
        else:
            # HUMAN PLAYER VIEW
            h_col1, h_col2 = st.columns([3, 2])
            
            with h_col1:
                st.markdown(f"### 🎴 Your Hand ({active_player['name']})")
                st.caption(f"Play cards onto your Solitaire board or discard. Actions left: **{active_player['actions_left']}**")
                
                hand = active_player["hand"]
                if not hand:
                    st.warning("Your hand is empty! Click 'End Turn' below to draw new cards.")
                else:
                    card_cols = st.columns(min(len(hand), 6))
                    for c_idx, c_name in enumerate(hand):
                        spec = CARD_SPECS[c_name]
                        with card_cols[c_idx % len(card_cols)]:
                            st.markdown(f"""
                            <div class="hand-card-box">
                                <div>
                                    <div class="hand-card-header">
                                        <span class="hand-card-type" style="color:{spec['type_color']};">{spec['type']}</span>
                                        <span>{spec['icon']}</span>
                                    </div>
                                    <div class="hand-card-title">{c_name}</div>
                                    <div class="hand-card-desc">{spec['desc']}</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            btn_p, btn_d = st.columns(2)
                            with btn_p:
                                if c_name == "Competitor Steal":
                                    if st.button("Steal", key=f"btn_play_{c_idx}", use_container_width=True):
                                        st.session_state.pending_action = {"action": "steal", "card": c_name}
                                elif c_name == "Pivot":
                                    if st.button("Pivot", key=f"btn_play_{c_idx}", use_container_width=True):
                                        st.session_state.pending_action = {"action": "pivot", "card": c_name}
                                else:
                                    if st.button("▶ Play", key=f"btn_play_{c_idx}", type="primary", use_container_width=True):
                                        ok, err_msg = play_card_action(st.session_state.current_idx, c_name)
                                        if not ok:
                                            st.error(err_msg)
                                        else:
                                            st.rerun()
                            with btn_d:
                                if st.button("🗑️", key=f"btn_disc_{c_idx}", help=f"Discard {c_name}", use_container_width=True):
                                    discard_card_action(st.session_state.current_idx, c_name)
                                    st.rerun()

                # Pending Action: Steal Target Selection
                if st.session_state.pending_action:
                    p_act = st.session_state.pending_action
                    if p_act["action"] == "steal":
                        st.markdown("#### 🥷 Target Competitor Card to Steal")
                        stealable = []
                        for op in st.session_state.players:
                            if op["id"] != active_player["id"] and not op["is_locked"]:
                                if op["phase1"]["idea"]:
                                    stealable.append((op["id"], "idea", f"{op['name']} - 💡 Idea (Slot 1)"))
                                if op["phase1"]["build"]:
                                    stealable.append((op["id"], "build", f"{op['name']} - 🛠️ Build (Slot 2)"))
                        
                        if not stealable:
                            st.warning("No opponents currently have stealable (unlocked) Phase 1 cards!")
                            if st.button("Cancel Steal"):
                                st.session_state.pending_action = None
                                st.rerun()
                        else:
                            chosen_t = st.selectbox("Select Target Card", stealable, format_func=lambda x: x[2])
                            col_s_ok, col_s_cn = st.columns(2)
                            with col_s_ok:
                                if st.button("Execute Steal", type="primary", use_container_width=True):
                                    play_card_action(st.session_state.current_idx, "Competitor Steal", {"target_pid": chosen_t[0], "target_slot": chosen_t[1]})
                                    st.session_state.pending_action = None
                                    st.rerun()
                            with col_s_cn:
                                if st.button("Cancel", use_container_width=True):
                                    st.session_state.pending_action = None
                                    st.rerun()

                    # Pending Action: Pivot Board Card Selection
                    elif p_act["action"] == "pivot":
                        st.markdown("#### 🔄 Select Board Card to Swap with Deck")
                        piv_options = []
                        if active_player["phase1"]["idea"] and not active_player["is_locked"]:
                            piv_options.append(("idea", "Slot 1: 💡 Idea"))
                        if active_player["phase1"]["build"] and not active_player["is_locked"]:
                            piv_options.append(("build", "Slot 2: 🛠️ Build"))
                        if active_player["phase3"]["investment_count"] > 0:
                            piv_options.append(("investment", "Slot 5: 💰 Investment (+10% Equity refund)"))
                        if active_player["phase3"]["revenue_count"] > 0:
                            piv_options.append(("revenue", "Slot 6: 📈 Revenue (-10% Equity)"))
                            
                        if not piv_options:
                            st.warning("No valid board cards available to pivot.")
                            if st.button("Cancel Pivot"):
                                st.session_state.pending_action = None
                                st.rerun()
                        else:
                            chosen_piv = st.selectbox("Select Board Card to Swap", piv_options, format_func=lambda x: x[1])
                            col_p_ok, col_p_cn = st.columns(2)
                            with col_p_ok:
                                if st.button("Execute Pivot", type="primary", use_container_width=True):
                                    play_card_action(st.session_state.current_idx, "Pivot", {"slot": chosen_piv[0]})
                                    st.session_state.pending_action = None
                                    st.rerun()
                            with col_p_cn:
                                if st.button("Cancel", use_container_width=True):
                                    st.session_state.pending_action = None
                                    st.rerun()

                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🛑 Pass / End Turn", type="secondary", use_container_width=True):
                    end_player_turn()
                    st.rerun()

            # LIVE ACTIVITY LOG
            with h_col2:
                st.markdown("### 📜 Table Activity Log")
                log_markup = '<div class="felt-log-box">'
                for l in st.session_state.logs:
                    log_markup += f'<div class="felt-log-line"><span style="color:#64748b; font-size:0.75rem; margin-right:5px;">[{l["time"]}]</span><span style="color:{l["color"]};">{l["msg"]}</span></div>'
                log_markup += '</div>'
                st.markdown(log_markup, unsafe_allow_html=True)

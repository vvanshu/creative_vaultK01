import sqlite3
import datetime
import math
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lifeos.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # User Profile Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        avatar TEXT DEFAULT '⚡',
        current_identity TEXT NOT NULL,
        future_identity TEXT NOT NULL,
        goal_duration TEXT DEFAULT '90 Days',
        total_xp INTEGER DEFAULT 0,
        spent_xp INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Goals Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        duration TEXT DEFAULT '90 Days',
        final_target TEXT,
        monthly_target TEXT,
        weekly_actions TEXT,
        daily_tasks TEXT,
        hours_allocated REAL DEFAULT 10,
        category TEXT DEFAULT 'General',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Journey Stages Table (Nodes for Transformation Pipeline)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS journey_stages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal_id INTEGER,
        stage_order INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        required_xp INTEGER DEFAULT 0,
        is_completed INTEGER DEFAULT 0,
        FOREIGN KEY(goal_id) REFERENCES goals(id) ON DELETE CASCADE
    )
    """)

    # Tasks Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal_id INTEGER,
        title TEXT NOT NULL,
        task_type TEXT DEFAULT 'daily', -- 'daily' or 'weekly'
        difficulty TEXT DEFAULT 'Medium', -- 'Small', 'Medium', 'Large'
        xp_value INTEGER DEFAULT 30,
        is_completed INTEGER DEFAULT 0,
        completed_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(goal_id) REFERENCES goals(id) ON DELETE CASCADE
    )
    """)

    # Rewards Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rewards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        tier TEXT DEFAULT 'Medium', -- 'Small', 'Medium', 'Big'
        xp_cost INTEGER DEFAULT 100,
        expiry_date TEXT,
        is_claimed INTEGER DEFAULT 0,
        claimed_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Weekly Reviews Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weekly_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        week_start TEXT NOT NULL,
        completed_summary TEXT,
        what_failed TEXT,
        next_week_mission TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # XP Audit Log
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS xp_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action_type TEXT NOT NULL, -- 'earn' or 'spend'
        xp_amount INTEGER NOT NULL,
        description TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# Helper Math for RPG Level
def calculate_level_info(total_xp):
    # Level formula: Level = floor(total_xp / 100) + 1
    # Each level requires 100 XP
    level = math.floor(total_xp / 100) + 1
    current_level_xp = total_xp % 100
    next_level_xp = 100
    progress_pct = min(1.0, current_level_xp / next_level_xp)
    
    titles = [
        "Novice Adventurer", "Focused Apprentice", "Consistent Builder",
        "Master Architect", "Grand Strategist", "Visionary Creator",
        "Legendary Executor", "Sovereign Master"
    ]
    title_idx = min(len(titles) - 1, (level - 1) // 3)
    title = titles[title_idx]

    return {
        "level": level,
        "current_level_xp": current_level_xp,
        "next_level_xp": next_level_xp,
        "progress_pct": progress_pct,
        "title": title
    }

# Profile CRUD
def get_profile():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profile LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def create_profile(name, avatar, current_identity, future_identity, goal_duration):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO profile (name, avatar, current_identity, future_identity, goal_duration, total_xp, spent_xp)
    VALUES (?, ?, ?, ?, ?, 0, 0)
    """, (name, avatar, current_identity, future_identity, goal_duration))
    conn.commit()
    conn.close()

def update_profile_identity(current_identity, future_identity, avatar=None):
    conn = get_connection()
    cursor = conn.cursor()
    if avatar:
        cursor.execute("""
        UPDATE profile SET current_identity = ?, future_identity = ?, avatar = ? WHERE id = 1
        """, (current_identity, future_identity, avatar))
    else:
        cursor.execute("""
        UPDATE profile SET current_identity = ?, future_identity = ? WHERE id = 1
        """, (current_identity, future_identity))
    conn.commit()
    conn.close()

def update_xp(xp_change, action_type, description=""):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT total_xp, spent_xp FROM profile LIMIT 1")
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False

    total_xp = row["total_xp"]
    spent_xp = row["spent_xp"]

    if action_type == "earn":
        total_xp += xp_change
    elif action_type == "spend":
        available_xp = total_xp - spent_xp
        if available_xp < xp_change:
            conn.close()
            return False  # Not enough available XP
        spent_xp += xp_change

    cursor.execute("UPDATE profile SET total_xp = ?, spent_xp = ? WHERE id = 1", (total_xp, spent_xp))
    cursor.execute("INSERT INTO xp_logs (action_type, xp_amount, description) VALUES (?, ?, ?)", 
                   (action_type, xp_change, description))
    conn.commit()
    conn.close()
    return True

# Goals CRUD
def get_goals():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM goals ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_goal(name, duration, final_target, monthly_target, weekly_actions, daily_tasks, hours_allocated, category="General"):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO goals (name, duration, final_target, monthly_target, weekly_actions, daily_tasks, hours_allocated, category)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, duration, final_target, monthly_target, weekly_actions, daily_tasks, hours_allocated, category))
    goal_id = cursor.lastrowid

    # Create default Journey Stages based on profile identity & goal targets
    profile = get_profile()
    start_ident = profile["current_identity"] if profile else "Novice"
    end_ident = profile["future_identity"] if profile else "Master"

    stages = [
        (1, f"Initiate: {start_ident}", "Foundation & setup phase", 0, 1),
        (2, "Builder Stage", f"Active milestone: {monthly_target or 'Build MVP'}", 100, 0),
        (3, "Creator Stage", f"Scaling & refinement: {weekly_actions or 'Consistent action'}", 300, 0),
        (4, f"Achieved: {end_ident}", f"Final Target: {final_target or 'Goal Accomplished'}", 600, 0)
    ]

    for stage_order, title, desc, req_xp, is_comp in stages:
        cursor.execute("""
        INSERT INTO journey_stages (goal_id, stage_order, title, description, required_xp, is_completed)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (goal_id, stage_order, title, desc, req_xp, is_comp))

    # Generate initial daily/weekly tasks automatically if provided
    if daily_tasks:
        for t in daily_tasks.split("\n"):
            t_clean = t.strip("- *").strip()
            if t_clean:
                cursor.execute("""
                INSERT INTO tasks (goal_id, title, task_type, difficulty, xp_value)
                VALUES (?, ?, 'daily', 'Small', 10)
                """, (goal_id, t_clean))

    if weekly_actions:
        for w in weekly_actions.split("\n"):
            w_clean = w.strip("- *").strip()
            if w_clean:
                cursor.execute("""
                INSERT INTO tasks (goal_id, title, task_type, difficulty, xp_value)
                VALUES (?, ?, 'weekly', 'Medium', 30)
                """, (goal_id, w_clean))

    conn.commit()
    conn.close()
    return goal_id

def delete_goal(goal_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
    cursor.execute("DELETE FROM tasks WHERE goal_id = ?", (goal_id,))
    cursor.execute("DELETE FROM journey_stages WHERE goal_id = ?", (goal_id,))
    conn.commit()
    conn.close()

# Journey Stages CRUD
def get_journey_stages(goal_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    if goal_id:
        cursor.execute("SELECT * FROM journey_stages WHERE goal_id = ? ORDER BY stage_order ASC", (goal_id,))
    else:
        cursor.execute("SELECT * FROM journey_stages ORDER BY goal_id, stage_order ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def complete_journey_stage(stage_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE journey_stages SET is_completed = 1 WHERE id = ?", (stage_id,))
    conn.commit()
    conn.close()

# Tasks CRUD
def get_tasks(task_type=None, is_completed=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT tasks.*, goals.name as goal_name FROM tasks LEFT JOIN goals ON tasks.goal_id = goals.id WHERE 1=1"
    params = []
    if task_type:
        query += " AND task_type = ?"
        params.append(task_type)
    if is_completed is not None:
        query += " AND is_completed = ?"
        params.append(1 if is_completed else 0)
    query += " ORDER BY is_completed ASC, id DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_task(title, difficulty="Medium", task_type="daily", goal_id=None):
    xp_map = {"Small": 10, "Medium": 30, "Large": 100}
    xp_val = xp_map.get(difficulty, 30)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO tasks (goal_id, title, task_type, difficulty, xp_value)
    VALUES (?, ?, ?, ?, ?)
    """, (goal_id, title, task_type, difficulty, xp_val))
    conn.commit()
    conn.close()

def toggle_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    if not task:
        conn.close()
        return None

    new_status = 0 if task["is_completed"] else 1
    completed_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") if new_status else None
    
    cursor.execute("UPDATE tasks SET is_completed = ?, completed_at = ? WHERE id = ?", (new_status, completed_at, task_id))
    conn.commit()
    conn.close()

    # Award or remove XP
    xp_change = task["xp_value"]
    if new_status:
        update_xp(xp_change, "earn", f"Completed Quest: {task['title']}")
    else:
        # Revert XP if unchecked
        update_xp(-xp_change, "earn", f"Unchecked Quest: {task['title']}")

    return new_status

def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

# Rewards CRUD
def get_rewards(tier=None):
    conn = get_connection()
    cursor = conn.cursor()
    if tier:
        cursor.execute("SELECT * FROM rewards WHERE tier = ? ORDER BY is_claimed ASC, xp_cost ASC", (tier,))
    else:
        cursor.execute("SELECT * FROM rewards ORDER BY is_claimed ASC, xp_cost ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_reward(name, tier, xp_cost, expiry_date=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO rewards (name, tier, xp_cost, expiry_date)
    VALUES (?, ?, ?, ?)
    """, (name, tier, xp_cost, expiry_date))
    conn.commit()
    conn.close()

def claim_reward(reward_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rewards WHERE id = ?", (reward_id,))
    reward = cursor.fetchone()
    if not reward or reward["is_claimed"]:
        conn.close()
        return False, "Reward already claimed or not found."

    # Try spending XP
    success = update_xp(reward["xp_cost"], "spend", f"Claimed Reward: {reward['name']}")
    if not success:
        conn.close()
        return False, "Insufficient Available XP to unlock this reward."

    claimed_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE rewards SET is_claimed = 1, claimed_at = ? WHERE id = ?", (claimed_at, reward_id))
    conn.commit()
    conn.close()
    return True, "Reward claimed successfully!"

def delete_reward(reward_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rewards WHERE id = ?", (reward_id,))
    conn.commit()
    conn.close()

# Weekly Reviews CRUD
def get_weekly_reviews():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weekly_reviews ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_weekly_review(week_start, completed_summary, what_failed, next_week_mission):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO weekly_reviews (week_start, completed_summary, what_failed, next_week_mission)
    VALUES (?, ?, ?, ?)
    """, (week_start, completed_summary, what_failed, next_week_mission))
    conn.commit()
    conn.close()

# Default seed data generator
def seed_default_data_if_empty():
    profile = get_profile()
    if not profile:
        create_profile(
            name="Alex Vance",
            avatar="🚀",
            current_identity="Aspiring Creator",
            future_identity="Master Systems Architect",
            goal_duration="90 Days"
        )
        # Add seed goal
        goal_id = create_goal(
            name="Build & Ship LifeOS MVP",
            duration="90 Days",
            final_target="Launch fully functional RPG productivity suite",
            monthly_target="Complete core modules & visual identity map",
            weekly_actions="Ship 2 feature modules weekly\nRun user testing sessions",
            daily_tasks="Write clean python code (2 hrs)\nReview goal progress & log XP\nComplete 1 design polish item",
            hours_allocated=15.0,
            category="Career & Coding"
        )
        # Add default rewards
        create_reward("15-min Espresso & Music Break", "Small", 50, "Anytime")
        create_reward("Watch an Episode of Favorite Show", "Small", 100, "Weekend")
        create_reward("Gourmet Dinner / Cheat Meal", "Medium", 250, "This Sunday")
        create_reward("Buy New Tech Gadget / Book", "Medium", 400, "End of Month")
        create_reward("Weekend Getaway / Full Rest Day", "Big", 1000, "Goal Completion")

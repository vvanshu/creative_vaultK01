/* ===== HELPERS ===== */
const LS = {
  get: (k) => { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } },
  set: (k, v) => localStorage.setItem(k, JSON.stringify(v))
};
const genId = () => Date.now().toString(36) + Math.random().toString(36).substr(2);
const XP_MAP = { Small: 10, Medium: 30, Large: 100 };
const calcLevel = (xp) => {
  const level = Math.floor(xp / 100) + 1;
  const currentXp = xp % 100;
  const nextXp = 100;
  const progress = Math.min(1, currentXp / 100);
  const titles = ['Novice','Apprentice','Builder','Architect','Strategist','Creator','Legend','Sovereign'];
  return { level, currentXp, nextXp, progress, title: titles[Math.min(titles.length-1, Math.floor((level-1)/3))] };
};

/* ===== TOAST ===== */
function Toast({ message, onClose }) {
  React.useEffect(() => { const t = setTimeout(onClose, 3000); return () => clearTimeout(t); }, [message]);
  return <div className="toast">{message}</div>;
}

/* ===== ONBOARDING ===== */
function Onboarding({ onComplete }) {
  const [name, setName] = React.useState('');
  const [cur, setCur] = React.useState('');
  const [fut, setFut] = React.useState('');
  const [avatar, setAvatar] = React.useState('👨‍💻');
  
  const submit = (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    const p = { 
      name: name.trim(), 
      avatar: avatar, 
      currentIdentity: cur.trim() || 'Novice Developer', 
      futureIdentity: fut.trim() || 'Tech Architect', 
      totalXp: 0, 
      spentXp: 0, 
      createdAt: new Date().toISOString() 
    };
    LS.set('irisquest_profile', p);
    LS.set('irisquest_goals', [
      {
        id: 'g-seed-1',
        name: 'Build Portfolio Website',
        duration: '90 Days',
        finalTarget: 'Launch professional portfolio showing 3 flagship apps',
        monthlyTarget: 'Complete design and seed data for apps',
        weeklyActions: 'Write code 15 hours per week\nRefine design system',
        hoursPerWeek: 15,
        category: 'Creative',
        createdAt: new Date().toISOString()
      }
    ]);
    LS.set('irisquest_tasks', [
      { id: 't-seed-1', goalId: 'g-seed-1', title: 'Complete high contrast layout', difficulty: 'Medium', xpValue: 30, taskType: 'daily', isCompleted: false, completedAt: null, createdAt: new Date().toISOString() },
      { id: 't-seed-2', goalId: 'g-seed-1', title: 'Write copy for about page', difficulty: 'Small', xpValue: 10, taskType: 'daily', isCompleted: false, completedAt: null, createdAt: new Date().toISOString() }
    ]);
    LS.set('irisquest_rewards', [
      { id: 'r-seed-1', name: '15-minute coffee break', category: 'Break', xpCost: 50, expiryDate: 'Permanent', isClaimed: false, claimedAt: null },
      { id: 'r-seed-2', name: 'Watch favorite podcast episode', category: 'Entertainment', xpCost: 150, expiryDate: 'Weekend', isClaimed: false, claimedAt: null }
    ]);
    LS.set('irisquest_reviews', []);
    onComplete(p);
  };

  return (
    <div className="app-container" style={{ display: 'flex', alignItems: 'center', minHeight: '80vh' }}>
      <div className="premium-card" style={{ width: '100%', padding: '32px 24px' }}>
        <div style={{ textAlign: 'center', marginBottom: 28 }}>
          <div style={{ fontSize: '3.5rem', marginBottom: 12 }}>🛡️</div>
          <h1 className="large-title" style={{ marginBottom: 4 }}>IRIS QUEST</h1>
          <p className="caption">Premium RPG Productivity Operating System</p>
        </div>
        <form onSubmit={submit}>
          <div className="form-group">
            <label className="form-label">Avatar Emoji</label>
            <div style={{ display: 'flex', gap: 12, justifyContent: 'center', margin: '12px 0 20px' }}>
              {['👨‍💻', '👩‍🎨', '🧠', '⚡', '🏋️', '🚀'].map(emoji => (
                <button
                  key={emoji}
                  type="button"
                  onClick={() => setAvatar(emoji)}
                  style={{
                    fontSize: '2rem',
                    width: '56px',
                    height: '56px',
                    borderRadius: '50%',
                    border: avatar === emoji ? '2.5px solid var(--accent-purple)' : '1px solid var(--border-system)',
                    background: avatar === emoji ? 'rgba(88, 86, 214, 0.08)' : '#FFFFFF',
                    cursor: 'pointer',
                    transition: 'var(--transition-smooth)'
                  }}
                >
                  {emoji}
                </button>
              ))}
            </div>
          </div>
          <div className="form-group">
            <label className="form-label">Hero / Designer Name</label>
            <input className="form-input" value={name} onChange={e=>setName(e.target.value)} placeholder="e.g. Alex Vance" required />
          </div>
          <div className="form-group">
            <label className="form-label">Current Identity</label>
            <input className="form-input" value={cur} onChange={e=>setCur(e.target.value)} placeholder="e.g. Aspiring Builder" required />
          </div>
          <div className="form-group">
            <label className="form-label">Future Identity Target</label>
            <input className="form-input" value={fut} onChange={e=>setFut(e.target.value)} placeholder="e.g. Lead Product Architect" required />
          </div>
          <button className="btn-primary" type="submit" style={{ marginTop: 12 }}>⚡ Begin Your Quest</button>
        </form>
      </div>
    </div>
  );
}

/* ===== HOME PAGE ===== */
function HomePage({ profile, tasks, goals, setPage, setProfile, toast }) {
  const lv = calcLevel(profile.totalXp);
  const avail = profile.totalXp - profile.spentXp;
  const xpNeeded = lv.nextXp - lv.currentXp;

  const todayTasks = tasks.filter(t => t.taskType === 'daily' && !t.isCompleted);
  const completedTodayCount = tasks.filter(t => t.taskType === 'daily' && t.isCompleted).length;
  const totalTodayCount = todayTasks.length + completedTodayCount;
  const progressPct = totalTodayCount > 0 ? Math.round((completedTodayCount / totalTodayCount) * 100) : 100;

  // Next Quest details
  const nextQuest = todayTasks[0];
  const goalName = (gid) => { const g = goals.find(g => g.id === gid); return g ? g.name : ''; };

  return (
    <div>
      <div className="section-header">
        <h1 className="large-title" style={{ margin: 0 }}>Home</h1>
        <div className="memoji-avatar" style={{ width: 52, height: 52, fontSize: '26px' }}>{profile.avatar}</div>
      </div>

      {/* Profile Overview Card */}
      <div className="premium-card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
          <div>
            <h2 className="title" style={{ fontSize: '21px' }}>{profile.name}</h2>
            <p className="caption" style={{ marginTop: 2 }}>{profile.currentIdentity} ➔ <span style={{ color: 'var(--accent-purple)', fontWeight: 600 }}>{profile.futureIdentity}</span></p>
          </div>
          <span className="ios-badge ios-badge-purple" style={{ fontSize: '13px', padding: '6px 14px' }}>Lvl {lv.level}</span>
        </div>
      </div>

      {/* Today's Quest Highlights Card */}
      <div className="premium-card" style={{ cursor: 'pointer' }} onClick={() => setPage('quests')}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <h3 className="section-header" style={{ margin: 0 }}>Today's Quest Status</h3>
          <span className="caption" style={{ fontWeight: 600 }}>{completedTodayCount}/{totalTodayCount} Cleared</span>
        </div>
        <div style={{ display: 'flex', gap: 16, alignItems: 'center', marginBottom: 20 }}>
          <div className="progress-ring-container" style={{ width: 80, height: 80 }}>
            <svg width="80" height="80" viewBox="0 0 80 80">
              <circle className="progress-ring-bg" cx="40" cy="40" r="34" strokeWidth="6" fill="none" />
              <circle 
                className="progress-ring-indicator" 
                cx="40" 
                cy="40" 
                r="34" 
                strokeWidth="6" 
                fill="none" 
                strokeDasharray="213.6" 
                strokeDashoffset={213.6 - (213.6 * progressPct / 100)}
                transform="rotate(-90 40 40)"
              />
            </svg>
            <div className="progress-ring-text">
              <div style={{ fontSize: '18px', fontWeight: 800 }}>{progressPct}%</div>
            </div>
          </div>
          <div style={{ flexGrow: 1 }}>
            {nextQuest ? (
              <>
                <p className="caption" style={{ fontWeight: 700, textTransform: 'uppercase', fontSize: '11px', color: 'var(--accent-purple)' }}>Next Up</p>
                <h4 style={{ fontSize: '16px', fontWeight: 600, color: 'var(--text-primary)', marginTop: 2 }}>{nextQuest.title}</h4>
                <p className="caption" style={{ marginTop: 2 }}>{goalName(nextQuest.goalId) || 'General'}</p>
              </>
            ) : (
              <>
                <h4 style={{ fontSize: '16px', fontWeight: 600, color: 'var(--accent-green)' }}>All Daily Quests Cleared!</h4>
                <p className="caption" style={{ marginTop: 2 }}>Outstanding job. Reward yourself in the shop!</p>
              </>
            )}
          </div>
        </div>
      </div>

      {/* XP Card - Large Metrics */}
      <div className="premium-card" style={{ background: 'linear-gradient(135deg, #FFFFFF 0%, #F5F3FF 100%)', borderColor: 'rgba(88, 86, 214, 0.15)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: 12 }}>
          <div>
            <div style={{ fontSize: '38px', fontWeight: 800, color: 'var(--text-primary)', lineHeight: 1 }}>{profile.totalXp} XP</div>
            <p className="caption" style={{ fontSize: '14px', fontWeight: 500, color: 'var(--text-secondary)', marginTop: 8 }}>
              {xpNeeded} XP until Level {lv.level + 1}
            </p>
          </div>
          <span className="caption" style={{ fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.5px' }}>Level {lv.level} Progress</span>
        </div>
        <div className="ios-progress-container">
          <div className="ios-progress-track">
            <div className="ios-progress-fill" style={{ width: (lv.progress * 100) + '%' }} />
          </div>
        </div>
      </div>
    </div>
  );
}

/* ===== GOALS PAGE ===== */
function GoalsPage({ goals, setGoals, tasks, setTasks, toast }) {
  const [tab, setTab] = React.useState('list');
  const [name, setName] = React.useState('');
  const [cat, setCat] = React.useState('Career');
  const [dur, setDur] = React.useState('90 Days');
  const [hrs, setHrs] = React.useState(15);
  const [ft, setFt] = React.useState('');
  const [mt, setMt] = React.useState('');
  const [wa, setWa] = React.useState('');

  const addGoal = (e) => {
    e.preventDefault();
    if (!name.trim() || !ft.trim()) return;
    const g = { 
      id: genId(), 
      name: name.trim(), 
      duration: dur, 
      finalTarget: ft.trim(), 
      monthlyTarget: mt.trim(), 
      weeklyActions: wa.trim(), 
      hoursPerWeek: hrs, 
      category: cat, 
      createdAt: new Date().toISOString() 
    };
    const newGoals = [g, ...goals];
    LS.set('irisquest_goals', newGoals);
    setGoals(newGoals);

    if (wa.trim()) {
      const newTasks = wa.trim().split('\n').filter(l=>l.trim()).map(l => ({
        id: genId(), 
        goalId: g.id, 
        title: l.trim().replace(/^[-*]\s*/,''), 
        difficulty: 'Medium', 
        xpValue: 30, 
        taskType: 'weekly', 
        isCompleted: false, 
        completedAt: null, 
        createdAt: new Date().toISOString()
      }));
      const allTasks = [...newTasks, ...tasks];
      LS.set('irisquest_tasks', allTasks);
      setTasks(allTasks);
    }
    setName(''); setFt(''); setMt(''); setWa('');
    toast('Campaign initialized!');
    setTab('list');
  };

  const deleteGoal = (id) => {
    const ng = goals.filter(g=>g.id!==id);
    LS.set('irisquest_goals', ng); setGoals(ng);
    const nt = tasks.filter(t=>t.goalId!==id);
    LS.set('irisquest_tasks', nt); setTasks(nt);
    toast('Goal deleted.');
  };

  // Helper: calculate progress percentage for a specific goal based on linked tasks
  const getGoalProgress = (gid) => {
    const linked = tasks.filter(t => t.goalId === gid);
    if (linked.length === 0) return 0;
    const completed = linked.filter(t => t.isCompleted).length;
    return Math.round((completed / linked.length) * 100);
  };

  // Helper: get first active task description
  const getNextAction = (gid) => {
    const nextTask = tasks.find(t => t.goalId === gid && !t.isCompleted);
    return nextTask ? nextTask.title : 'All tasks completed';
  };

  return (
    <div>
      <div className="section-header">
        <h1 className="large-title" style={{ margin: 0 }}>Goals</h1>
      </div>

      <div className="segmented-control">
        <button className={'segmented-btn'+(tab==='list'?' active':'')} onClick={()=>setTab('list')}>Active Goals</button>
        <button className={'segmented-btn'+(tab==='create'?' active':'')} onClick={()=>setTab('create')}>Create Goal</button>
      </div>

      {tab === 'list' ? (
        goals.length === 0 ? (
          <div className="empty-state"><div className="empty-state-icon">🎯</div><p>No active goals. Add one above.</p></div>
        ) : (
          goals.map(g => {
            const prog = getGoalProgress(g.id);
            const badgeClass = g.category === 'Career' ? 'ios-badge-blue' :
                               g.category === 'Health' ? 'ios-badge-green' :
                               g.category === 'Finance' ? 'ios-badge-orange' :
                               g.category === 'Creative' ? 'ios-badge-purple' : 'ios-badge-pink';
            return (
              <div className="premium-card" key={g.id}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                  <span className={`ios-badge ${badgeClass}`}>{g.category}</span>
                  <span className="caption" style={{ fontWeight: 600 }}>{g.hoursPerWeek} hrs / week</span>
                </div>
                <h3 className="title" style={{ fontSize: '20px', marginBottom: 6 }}>{g.name.toUpperCase()}</h3>
                <p className="caption" style={{ marginBottom: 16 }}>⏱️ {g.duration}</p>
                
                <div className="goal-progress-bar-container" style={{ marginBottom: 20 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: 6 }}>
                    <span>Progress</span>
                    <span>{prog}%</span>
                  </div>
                  <div className="goal-progress-bar-track">
                    <div className="goal-progress-bar-fill" style={{ width: prog+'%' }} />
                  </div>
                </div>

                <div style={{ padding: '12px 14px', borderRadius: '10px', background: 'rgba(0,0,0,0.02)', border: '1px solid var(--border-system)', marginBottom: 16 }}>
                  <p className="caption" style={{ fontWeight: 700, fontSize: '11px', textTransform: 'uppercase', color: 'var(--accent-purple)' }}>Next Action</p>
                  <p className="body-text" style={{ fontWeight: 500, fontSize: '14px', marginTop: 2 }}>{getNextAction(g.id)}</p>
                </div>

                <button className="btn-danger-text" onClick={()=>deleteGoal(g.id)}>🗑️ Delete Goal</button>
              </div>
            );
          })
        )
      ) : (
        <div className="premium-card">
          <h3 className="section-header" style={{ marginBottom: 16 }}>Create New Goal Campaign</h3>
          <form onSubmit={addGoal}>
            <div className="form-group">
              <label className="form-label">Goal Name</label>
              <input className="form-input" value={name} onChange={e=>setName(e.target.value)} placeholder="e.g. Launch Portfolio App" required />
            </div>
            <div className="form-group">
              <label className="form-label">Category</label>
              <select className="form-select" value={cat} onChange={e=>setCat(e.target.value)}>
                <option>Career</option><option>Health</option><option>Finance</option><option>Creative</option><option>Mindset</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Duration</label>
              <select className="form-select" value={dur} onChange={e=>setDur(e.target.value)}>
                <option>30 Days</option><option>60 Days</option><option>90 Days</option><option>180 Days</option><option>1 Year</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Weekly Hour Budget</label>
              <input className="form-input" type="number" min={1} max={168} value={hrs} onChange={e=>setHrs(+e.target.value)} />
            </div>
            <div className="form-group">
              <label className="form-label">Final Target (Destination)</label>
              <input className="form-input" value={ft} onChange={e=>setFt(e.target.value)} placeholder="e.g. Live portfolio link with 3 case studies" required />
            </div>
            <div className="form-group">
              <label className="form-label">Monthly Target Milestone</label>
              <input className="form-input" value={mt} onChange={e=>setMt(e.target.value)} placeholder="e.g. Design assets complete" />
            </div>
            <div className="form-group">
              <label className="form-label">Weekly Actions (1 per line to seed weekly quests)</label>
              <textarea className="form-textarea" value={wa} onChange={e=>setWa(e.target.value)} placeholder="e.g. Code 15 hours&#10;Write 1 case study draft" />
            </div>
            <button className="btn-primary" type="submit">🎯 Create Goal Campaign</button>
          </form>
        </div>
      )}
    </div>
  );
}

/* ===== QUESTS PAGE ===== */
function QuestsPage({ profile, tasks, goals, setTasks, setProfile, toast }) {
  const [tab, setTab] = React.useState('active');
  const [title, setTitle] = React.useState('');
  const [diff, setDiff] = React.useState('Medium');
  const [ttype, setTtype] = React.useState('daily');
  const [goalId, setGoalId] = React.useState('');

  const toggleTask = (id) => {
    const updated = tasks.map(t => {
      if (t.id !== id) return t;
      const wasCompleted = t.isCompleted;
      const newP = { ...profile };
      if (wasCompleted) { 
        newP.totalXp = Math.max(0, newP.totalXp - t.xpValue); 
        toast('↩️ Quest restored to board'); 
      }
      else { 
        newP.totalXp += t.xpValue; 
        toast(`🎉 +${t.xpValue} XP Earned!`); 
      }
      LS.set('irisquest_profile', newP);
      setProfile(newP);
      return { ...t, isCompleted: !wasCompleted, completedAt: wasCompleted ? null : new Date().toISOString() };
    });
    LS.set('irisquest_tasks', updated);
    setTasks(updated);
  };

  const deleteTask = (id) => {
    const updated = tasks.filter(t => t.id !== id);
    LS.set('irisquest_tasks', updated);
    setTasks(updated);
    toast('Quest removed.');
  };

  const addTask = (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    const t = { 
      id: genId(), 
      goalId: goalId || null, 
      title: title.trim(), 
      difficulty: diff, 
      xpValue: XP_MAP[diff], 
      taskType: ttype, 
      isCompleted: false, 
      completedAt: null, 
      createdAt: new Date().toISOString() 
    };
    const updated = [t, ...tasks];
    LS.set('irisquest_tasks', updated);
    setTasks(updated);
    setTitle('');
    toast('New quest initialized!');
  };

  const filtered = tab === 'active' ? tasks.filter(t => !t.isCompleted && t.taskType === 'daily') :
                   tab === 'weekly' ? tasks.filter(t => !t.isCompleted && t.taskType === 'weekly') :
                   tasks.filter(t => t.isCompleted);

  const goalName = (gid) => { const g = goals.find(g => g.id === gid); return g ? g.name : ''; };

  return (
    <div>
      <div className="section-header">
        <h1 className="large-title" style={{ margin: 0 }}>Quests</h1>
      </div>

      <div className="segmented-control">
        <button className={'segmented-btn'+(tab==='active'?' active':'')} onClick={()=>setTab('active')}>Daily</button>
        <button className={'segmented-btn'+(tab==='weekly'?' active':'')} onClick={()=>setTab('weekly')}>Weekly</button>
        <button className={'segmented-btn'+(tab==='archive'?' active':'')} onClick={()=>setTab('archive')}>Archive</button>
      </div>

      {filtered.length === 0 ? (
        <div className="empty-state"><div className="empty-state-icon">{tab==='archive'?'📦':'⚔️'}</div><p>No quests here.</p></div>
      ) : (
        filtered.map(t => (
          <div key={t.id} className={'quest-item' + (t.isCompleted?' completed':'')}>
            <div className={'quest-checkbox'+(t.isCompleted?' checked':'')} onClick={()=>toggleTask(t.id)}>
              <svg className="quest-checkbox-icon" viewBox="0 0 12 12">
                <path d="M2.5 6L5 8.5L9.5 3.5" />
              </svg>
            </div>
            <div className="quest-info">
              <div className="quest-title">{t.title}</div>
              <div className="quest-meta">
                {goalName(t.goalId) && <span>{goalName(t.goalId)} · </span>}
                <span className={'ios-badge ' + (t.difficulty==='Small'?'ios-badge-blue':t.difficulty==='Medium'?'ios-badge-orange':'ios-badge-purple')}>{t.difficulty}</span>
              </div>
            </div>
            <span className="quest-xp-badge">+{t.xpValue} XP</span>
            <button className="btn-icon" style={{ width: 28, height: 28, borderRadius: '50%' }} onClick={()=>deleteTask(t.id)}>✕</button>
          </div>
        ))
      )}

      {/* Quick Add Quest form */}
      <div className="premium-card" style={{ marginTop: 24 }}>
        <h3 className="section-header" style={{ marginBottom: 16 }}>➕ Quick Add Quest</h3>
        <form onSubmit={addTask}>
          <div className="form-group">
            <label className="form-label">Quest Description</label>
            <input className="form-input" value={title} onChange={e=>setTitle(e.target.value)} placeholder="e.g. Core layout styling" required />
          </div>
          <div className="form-group">
            <label className="form-label">Difficulty</label>
            <select className="form-select" value={diff} onChange={e=>setDiff(e.target.value)}>
              <option>Small</option><option>Medium</option><option>Large</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Quest Type</label>
            <select className="form-select" value={ttype} onChange={e=>setTtype(e.target.value)}>
              <option value="daily">Daily</option><option value="weekly">Weekly</option>
            </select>
          </div>
          {goals.length > 0 && (
            <div className="form-group">
              <label className="form-label">Goal Link</label>
              <select className="form-select" value={goalId} onChange={e=>setGoalId(e.target.value)}>
                <option value="">None</option>
                {goals.map(g=><option key={g.id} value={g.id}>{g.name}</option>)}
              </select>
            </div>
          )}
          <button className="btn-primary" type="submit">⚡ Add Quest to Board</button>
        </form>
      </div>
    </div>
  );
}

/* ===== REWARDS PAGE ===== */
function RewardsPage({ profile, setProfile, rewards, setRewards, toast }) {
  const [tab, setTab] = React.useState('shop');
  const [filter, setFilter] = React.useState('All');
  const [rn, setRn] = React.useState('');
  const [rc, setRc] = React.useState('Treat');
  const [rxp, setRxp] = React.useState(100);
  const [rexp, setRexp] = React.useState('');

  const avail = profile.totalXp - profile.spentXp;

  const claim = (id) => {
    const r = rewards.find(r=>r.id===id);
    if (!r || r.isClaimed || avail < r.xpCost) return;
    const np = { ...profile, spentXp: profile.spentXp + r.xpCost };
    LS.set('irisquest_profile', np); setProfile(np);
    const nr = rewards.map(rw => rw.id===id ? { ...rw, isClaimed: true, claimedAt: new Date().toISOString() } : rw);
    LS.set('irisquest_rewards', nr); setRewards(nr);
    toast('🎁 Reward Unlocked!');
  };

  const addReward = (e) => {
    e.preventDefault();
    if (!rn.trim()) return;
    const r = { id: genId(), name: rn.trim(), category: rc, xpCost: rxp, expiryDate: rexp.trim(), isClaimed: false, claimedAt: null };
    const nr = [r, ...rewards];
    LS.set('irisquest_rewards', nr); setRewards(nr); setRn(''); setRexp('');
    toast('Reward added to list.'); setTab('shop');
  };

  const deleteReward = (id) => {
    const nr = rewards.filter(r=>r.id!==id);
    LS.set('irisquest_rewards', nr); setRewards(nr);
    toast('Reward deleted.');
  };

  const tierFilter = (r) => {
    if (filter==='All') return true;
    if (filter==='Small') return r.xpCost < 100;
    if (filter==='Medium') return r.xpCost >= 100 && r.xpCost < 500;
    return r.xpCost >= 500;
  };

  return (
    <div>
      <div className="section-header">
        <h1 className="large-title" style={{ margin: 0 }}>Rewards</h1>
      </div>

      <div className="premium-card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'linear-gradient(135deg, #FFFFFF, #FFF9F0)', borderColor: 'rgba(255, 149, 0, 0.15)' }}>
        <div>
          <span className="ios-badge ios-badge-orange">Perk Vault</span>
          <h2 className="title" style={{ fontSize: '18px', marginTop: 4 }}>Claim Perks</h2>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '24px', fontWeight: 800, color: 'var(--accent-orange)' }}>⚡ {avail} XP</div>
          <p className="caption">Available Balance</p>
        </div>
      </div>

      <div className="segmented-control">
        <button className={'segmented-btn'+(tab==='shop'?' active':'')} onClick={()=>setTab('shop')}>Storefront</button>
        <button className={'segmented-btn'+(tab==='add'?' active':'')} onClick={()=>setTab('add')}>Add Custom Reward</button>
      </div>

      {tab === 'shop' ? (
        <>
          <div style={{ display: 'flex', gap: 8, marginBottom: 20, flexWrap: 'wrap' }}>
            {['All','Small','Medium','Big'].map(f=>(
              <button 
                key={f} 
                className="btn-icon" 
                style={{ 
                  width: 'auto', 
                  height: '38px', 
                  borderRadius: '19px', 
                  padding: '0 16px', 
                  fontSize: '13px', 
                  fontWeight: 600,
                  background: filter === f ? 'var(--accent-orange)' : 'rgba(0,0,0,0.03)',
                  color: filter === f ? '#FFFFFF' : 'var(--text-primary)'
                }} 
                onClick={()=>setFilter(f)}
              >
                {f}
              </button>
            ))}
          </div>

          {rewards.filter(tierFilter).length === 0 ? (
            <div className="empty-state"><div className="empty-state-icon">🎁</div><p>No perks available.</p></div>
          ) : (
            rewards.filter(tierFilter).map(r => (
              <div className={'premium-card' + (r.isClaimed?' claimed-reward':'')} key={r.id} style={{ opacity: r.isClaimed ? 0.6 : 1 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                  <span className="ios-badge ios-badge-pink">{r.category}</span>
                  <span style={{ fontSize: '18px', fontWeight: 800, color: 'var(--accent-orange)' }}>⚡ {r.xpCost} XP</span>
                </div>
                <h3 className="title" style={{ fontSize: '18px', marginBottom: 4 }}>{r.name}</h3>
                <p className="caption" style={{ marginBottom: 16 }}>⌛ {r.expiryDate || 'Permanent'}</p>
                <div style={{ display: 'flex', gap: 12 }}>
                  {r.isClaimed ? (
                    <span className="ios-badge ios-badge-green" style={{ display: 'inline-flex', padding: '10px 16px', fontWeight: 700 }}>✓ Claimed</span>
                  ) : (
                    <button 
                      className="btn-primary" 
                      style={{ height: '40px', background: 'var(--accent-orange)', boxShadow: 'none' }}
                      disabled={avail < r.xpCost} 
                      onClick={()=>claim(r.id)}
                    >
                      Unlock perk
                    </button>
                  )}
                  <button className="btn-secondary" style={{ width: '40px', height: '40px', borderRadius: '10px' }} onClick={()=>deleteReward(r.id)}>✕</button>
                </div>
              </div>
            ))
          )}
        </>
      ) : (
        <div className="premium-card">
          <h3 className="section-header" style={{ marginBottom: 16 }}>Add Custom Perk</h3>
          <form onSubmit={addReward}>
            <div className="form-group">
              <label className="form-label">Reward Name</label>
              <input className="form-input" value={rn} onChange={e=>setRn(e.target.value)} placeholder="e.g. Afternoon film pass" required />
            </div>
            <div className="form-group">
              <label className="form-label">Category</label>
              <select className="form-select" value={rc} onChange={e=>setRc(e.target.value)}>
                <option>Treat</option><option>Entertainment</option><option>Shopping</option><option>Experience</option><option>Break</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">XP Cost</label>
              <input className="form-input" type="number" min={10} value={rxp} onChange={e=>setRxp(+e.target.value)} />
            </div>
            <div className="form-group">
              <label className="form-label">Expiry Date / Restriction</label>
              <input className="form-input" value={rexp} onChange={e=>setRexp(e.target.value)} placeholder="e.g. This Saturday" />
            </div>
            <button className="btn-primary" style={{ background: 'var(--accent-orange)', boxShadow: 'none' }} type="submit">🎁 Add Reward to Vault</button>
          </form>
        </div>
      )}
    </div>
  );
}

/* ===== PROFILE & WEEKLY REVIEW PAGE ===== */
function ProfilePage({ profile, setProfile, tasks, setTasks, rewards, setRewards, reviews, setReviews, toast }) {
  const [ci, setCi] = React.useState(profile.currentIdentity);
  const [fi, setFi] = React.useState(profile.futureIdentity);
  const [showReview, setShowReview] = React.useState(false);

  // Weekly review form fields
  const [comp, setComp] = React.useState('');
  const [fail, setFail] = React.useState('');
  const [next, setNext] = React.useState('');

  const now = new Date();
  const ws = new Date(now); ws.setDate(now.getDate() - now.getDay());
  const weekStr = 'Week of ' + ws.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  const completedTasks = tasks.filter(t=>t.isCompleted);
  const autoSummary = completedTasks.slice(0,8).map(t => '• ' + t.title + ' (+' + t.xpValue + ' XP)').join('\n') || 'No completed quests yet.';

  const updateIdentity = (e) => {
    e.preventDefault();
    const np = { ...profile, currentIdentity: ci, futureIdentity: fi };
    LS.set('irisquest_profile', np); setProfile(np);
    toast('Identity mapping updated.');
  };

  const softReset = () => {
    if (confirm('Are you sure you want to soft reset your XP and quests?')) {
      const np = { ...profile, totalXp: 0, spentXp: 0 };
      LS.set('irisquest_profile', np); setProfile(np);
      const nt = tasks.map(t=>({...t, isCompleted: false, completedAt: null}));
      LS.set('irisquest_tasks', nt); setTasks(nt);
      const nr = rewards.map(r=>({...r, isClaimed: false, claimedAt: null}));
      LS.set('irisquest_rewards', nr); setRewards(nr);
      toast('Progress reset.');
    }
  };

  const fullReset = () => {
    if (confirm('🚨 This will permanently delete all profile settings, goals, quests, and rewards. Proceed?')) {
      ['irisquest_profile','irisquest_goals','irisquest_tasks','irisquest_rewards','irisquest_reviews'].forEach(k=>localStorage.removeItem(k));
      window.location.reload();
    }
  };

  const deleteReview = (id) => {
    if (confirm('Are you sure you want to delete this weekly report log?')) {
      const nr = reviews.filter(r => r.id !== id);
      LS.set('irisquest_reviews', nr);
      setReviews(nr);
      toast('Weekly review log removed.');
    }
  };

  const submitReview = (e) => {
    e.preventDefault();
    const r = { id: genId(), weekStart: weekStr, completed: comp || autoSummary, failed: fail, nextMission: next, createdAt: new Date().toISOString() };
    const nr = [r, ...reviews];
    LS.set('irisquest_reviews', nr); setReviews(nr);
    const np = { ...profile, totalXp: profile.totalXp + 50 };
    LS.set('irisquest_profile', np); setProfile(np);
    setComp(''); setFail(''); setNext('');
    toast('📝 Weekly review cleared! +50 XP!');
    setShowReview(false);
  };

  return (
    <div>
      <div className="section-header">
        <h1 className="large-title" style={{ margin: 0 }}>Profile</h1>
      </div>

      {!showReview ? (
        <>
          {/* Identity Overview */}
          <div className="premium-card" style={{ textAlign: 'center' }}>
            <div className="memoji-avatar" style={{ margin: '0 auto 16px', width: 90, height: 90, fontSize: '3rem' }}>{profile.avatar}</div>
            <h2 className="title" style={{ fontSize: '22px' }}>{profile.name}</h2>
            <p className="caption" style={{ marginTop: 4 }}>{profile.currentIdentity} ➔ <span style={{ color: 'var(--accent-purple)', fontWeight: 600 }}>{profile.futureIdentity}</span></p>
            <div style={{ marginTop: 12 }}>
              <span className="ios-badge ios-badge-purple" style={{ fontSize: '13px' }}>Total XP Earned: {profile.totalXp}</span>
            </div>
          </div>

          {/* Weekly Review Prompt Box */}
          <div className="premium-card" style={{ background: 'rgba(88,86,214,0.04)', borderColor: 'rgba(88,86,214,0.15)' }}>
            <h3 className="section-header" style={{ marginBottom: 6 }}>Weekly Reflection Campaign</h3>
            <p className="body-text" style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>Reflect on weekly highlights, bottlenecks and log your strategy. Grants +50 XP bonus.</p>
            <button className="btn-primary" style={{ marginTop: 16, height: '46px' }} onClick={()=>setShowReview(true)}>Write Weekly Review</button>
          </div>

          {/* Edit Identity */}
          <div className="premium-card">
            <h3 className="section-header" style={{ marginBottom: 16 }}>Edit Identity Mapping</h3>
            <form onSubmit={updateIdentity}>
              <div className="form-group">
                <label className="form-label">Current Identity</label>
                <input className="form-input" value={ci} onChange={e=>setCi(e.target.value)} required />
              </div>
              <div className="form-group">
                <label className="form-label">Future Identity Target</label>
                <input className="form-input" value={fi} onChange={e=>setFi(e.target.value)} required />
              </div>
              <button className="btn-secondary" type="submit">Update Identity</button>
            </form>
          </div>

          {/* Past reviews */}
          {reviews.length > 0 && (
            <div style={{ marginTop: 24 }}>
              <h3 className="section-header" style={{ marginBottom: 12 }}>Review Log</h3>
              {reviews.map(r => (
                <div className="premium-card" key={r.id}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
                    <span className="ios-badge ios-badge-blue">{r.weekStart}</span>
                    <span className="caption">{r.createdAt?.slice(0,10)}</span>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                    <div><h4 className="caption" style={{ fontWeight: 700, color: 'var(--accent-green)' }}>Completed</h4><p className="body-text" style={{ fontSize: '14px', marginTop: 2 }}>{r.completed}</p></div>
                    <div><h4 className="caption" style={{ fontWeight: 700, color: 'var(--accent-orange)' }}>Obstacles</h4><p className="body-text" style={{ fontSize: '14px', marginTop: 2 }}>{r.failed || 'None logged.'}</p></div>
                    <div><h4 className="caption" style={{ fontWeight: 700, color: 'var(--accent-purple)' }}>Next Mission</h4><p className="body-text" style={{ fontSize: '14px', marginTop: 2 }}>{r.nextMission || '—'}</p></div>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 14, borderTop: '1px solid var(--border-system)', paddingTop: 10 }}>
                    <button className="btn-danger-text" onClick={() => deleteReview(r.id)}>🗑️ Delete Review</button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Reset Control Panel */}
          <div className="premium-card" style={{ marginTop: 24, border: '1.5px solid rgba(255, 45, 85, 0.15)' }}>
            <h3 className="section-header" style={{ color: 'var(--accent-pink)', marginBottom: 16 }}>⚠️ System Maintenance</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <button className="btn-secondary" style={{ color: 'var(--text-primary)' }} onClick={softReset}>🔄 Soft Reset (XP & tasks)</button>
              <button className="btn-primary" style={{ background: 'var(--accent-pink)', boxShadow: 'none' }} onClick={fullReset}>🚨 Full System Format</button>
            </div>
          </div>
        </>
      ) : (
        <div className="premium-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <h3 className="title" style={{ fontSize: '20px' }}>Reflection ({weekStr})</h3>
            <button className="btn-icon" onClick={()=>setShowReview(false)}>✕</button>
          </div>
          <form onSubmit={submitReview}>
            <div className="form-group">
              <label className="form-label">What did I complete?</label>
              <textarea className="form-textarea" value={comp} onChange={e=>setComp(e.target.value)} placeholder={autoSummary} />
            </div>
            <div className="form-group">
              <label className="form-label">What failed or caused friction?</label>
              <textarea className="form-textarea" value={fail} onChange={e=>setFail(e.target.value)} placeholder="e.g. Distracted, scope creep" required />
            </div>
            <div className="form-group">
              <label className="form-label">What is next week's mission?</label>
              <textarea className="form-textarea" value={next} onChange={e=>setNext(e.target.value)} placeholder="e.g. Launch design system case study" required />
            </div>
            <button className="btn-primary" type="submit">📝 Finalize & Earn +50 XP</button>
          </form>
        </div>
      )}
    </div>
  );
}

/* ===== MAIN APP ===== */
function App() {
  const [profile, setProfile] = React.useState(LS.get('irisquest_profile'));
  const [goals, setGoals] = React.useState(LS.get('irisquest_goals') || []);
  const [tasks, setTasks] = React.useState(LS.get('irisquest_tasks') || []);
  const [rewards, setRewards] = React.useState(LS.get('irisquest_rewards') || []);
  const [reviews, setReviews] = React.useState(LS.get('irisquest_reviews') || []);
  const [page, setPage] = React.useState('home');
  const [toastMsg, setToastMsg] = React.useState(null);

  const showToast = (msg) => { setToastMsg(msg); };

  if (!profile) return <Onboarding onComplete={(p) => { setProfile(p); setPage('home'); }} />;

  return (
    <div className="app-container">
      {toastMsg && <Toast message={toastMsg} onClose={()=>setToastMsg(null)} />}

      {/* Pages render container */}
      {page === 'home' && <HomePage profile={profile} tasks={tasks} goals={goals} setPage={setPage} setProfile={setProfile} toast={showToast} />}
      {page === 'goals' && <GoalsPage goals={goals} setGoals={setGoals} tasks={tasks} setTasks={setTasks} toast={showToast} />}
      {page === 'quests' && <QuestsPage profile={profile} tasks={tasks} goals={goals} setTasks={setTasks} setProfile={setProfile} toast={showToast} />}
      {page === 'rewards' && <RewardsPage profile={profile} setProfile={setProfile} rewards={rewards} setRewards={setRewards} toast={showToast} />}
      {page === 'profile' && <ProfilePage profile={profile} setProfile={setProfile} tasks={tasks} setTasks={setTasks} rewards={rewards} setRewards={setRewards} reviews={reviews} setReviews={setReviews} toast={showToast} />}

      {/* iOS Floating Bottom Navigation */}
      <nav className="bottom-nav">
        <button className={'nav-tab-btn'+(page==='home'?' active':'')} onClick={()=>setPage('home')}>
          <svg className="nav-tab-icon" viewBox="0 0 24 24">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
            <polyline points="9 22 9 12 15 12 15 22" />
          </svg>
          <span className="nav-tab-label">Home</span>
        </button>
        <button className={'nav-tab-btn'+(page==='goals'?' active':'')} onClick={()=>setPage('goals')}>
          <svg className="nav-tab-icon" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" />
            <circle cx="12" cy="12" r="6" />
            <circle cx="12" cy="12" r="2" />
          </svg>
          <span className="nav-tab-label">Goals</span>
        </button>
        <button className={'nav-tab-btn'+(page==='quests'?' active':'')} onClick={()=>setPage('quests')}>
          <svg className="nav-tab-icon" viewBox="0 0 24 24">
            <polyline points="9 11 12 14 22 4" />
            <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11" />
          </svg>
          <span className="nav-tab-label">Quests</span>
        </button>
        <button className={'nav-tab-btn'+(page==='rewards'?' active':'')} onClick={()=>setPage('rewards')}>
          <svg className="nav-tab-icon" viewBox="0 0 24 24">
            <rect x="3" y="8" width="18" height="12" rx="2" ry="2" />
            <line x1="12" y1="22" x2="12" y2="8" />
            <path d="M12 8H7.5a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8z" />
            <path d="M12 8h4.5a2.5 2.5 0 0 0 0-5C13 3 12 8 12 8z" />
          </svg>
          <span className="nav-tab-label">Rewards</span>
        </button>
        <button className={'nav-tab-btn'+(page==='profile'?' active':'')} onClick={()=>setPage('profile')}>
          <svg className="nav-tab-icon" viewBox="0 0 24 24">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
          <span className="nav-tab-label">Profile</span>
        </button>
      </nav>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);

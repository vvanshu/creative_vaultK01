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
  const titles = ['Novice','Apprentice','Builder','Architect','Strategist','Creator','Legend','Sovereign'];
  return { level, currentXp, nextXp: 100, progress: Math.min(1, currentXp / 100), title: titles[Math.min(titles.length-1, Math.floor((level-1)/3))] };
};

/* ===== TOAST ===== */
function Toast({ message, onClose }) {
  React.useEffect(() => { const t = setTimeout(onClose, 3000); return () => clearTimeout(t); }, []);
  return <div className="toast">{message}</div>;
}

/* ===== ONBOARDING ===== */
function Onboarding({ onComplete }) {
  const [name, setName] = React.useState('');
  const [cur, setCur] = React.useState('');
  const [fut, setFut] = React.useState('');
  const submit = (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    const p = { name: name.trim(), avatar: '⚔️', currentIdentity: cur.trim() || 'Novice', futureIdentity: fut.trim() || 'Master', totalXp: 0, spentXp: 0, createdAt: new Date().toISOString() };
    LS.set('irisquest_profile', p);
    LS.set('irisquest_goals', []);
    LS.set('irisquest_tasks', []);
    LS.set('irisquest_rewards', []);
    LS.set('irisquest_reviews', []);
    onComplete(p);
  };
  return (
    <div className="app-container" style={{ maxWidth: 540, marginTop: 60 }}>
      <div className="card" style={{ textAlign: 'center' }}>
        <div style={{ fontSize: '3rem', marginBottom: 8 }}>⚔️</div>
        <h1 style={{ fontSize: '1.8rem', marginBottom: 4 }}>Welcome to IRIS QUEST</h1>
        <p className="card-subtitle" style={{ marginBottom: 24 }}>Transform your goals into an RPG quest system</p>
        <form onSubmit={submit} style={{ textAlign: 'left' }}>
          <div className="form-group"><label className="form-label">Hero Name</label><input className="form-input" value={name} onChange={e=>setName(e.target.value)} placeholder="e.g. Alex Vance" required /></div>
          <div className="form-row">
            <div className="form-group"><label className="form-label">Current Identity</label><input className="form-input" value={cur} onChange={e=>setCur(e.target.value)} placeholder="Student" /></div>
            <div className="form-group"><label className="form-label">Future Identity</label><input className="form-input" value={fut} onChange={e=>setFut(e.target.value)} placeholder="Master Builder" /></div>
          </div>
          <button className="btn btn-primary btn-block" type="submit" style={{ marginTop: 8 }}>⚡ Begin Your Quest</button>
        </form>
      </div>
    </div>
  );
}

/* ===== DASHBOARD ===== */
function Dashboard({ profile, tasks, goals, setTasks, setProfile, toast }) {
  const [tab, setTab] = React.useState('active');
  const [title, setTitle] = React.useState('');
  const [diff, setDiff] = React.useState('Medium');
  const [ttype, setTtype] = React.useState('daily');
  const [goalId, setGoalId] = React.useState('');

  const lv = calcLevel(profile.totalXp);
  const avail = profile.totalXp - profile.spentXp;

  const toggleTask = (id) => {
    const updated = tasks.map(t => {
      if (t.id !== id) return t;
      const wasCompleted = t.isCompleted;
      const newP = { ...profile };
      if (wasCompleted) { newP.totalXp = Math.max(0, newP.totalXp - t.xpValue); toast('↩️ Quest Restored (−' + t.xpValue + ' XP)'); }
      else { newP.totalXp += t.xpValue; toast('🎉 +' + t.xpValue + ' XP Earned!'); }
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
  };

  const addTask = (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    const t = { id: genId(), goalId: goalId || null, title: title.trim(), difficulty: diff, xpValue: XP_MAP[diff], taskType: ttype, isCompleted: false, completedAt: null, createdAt: new Date().toISOString() };
    const updated = [t, ...tasks];
    LS.set('irisquest_tasks', updated);
    setTasks(updated);
    setTitle('');
    toast('Quest Created!');
  };

  const filtered = tab === 'active' ? tasks.filter(t => !t.isCompleted && t.taskType === 'daily') :
                   tab === 'weekly' ? tasks.filter(t => !t.isCompleted && t.taskType === 'weekly') :
                   tasks.filter(t => t.isCompleted);

  const goalName = (gid) => { const g = goals.find(g => g.id === gid); return g ? g.name : ''; };

  return (
    <>
      {/* Profile Banner */}
      <div className="profile-banner">
        <div className="avatar-circle">{profile.avatar}</div>
        <div className="profile-info">
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap' }}>
            <span className="badge badge-purple">Lvl {lv.level} {lv.title}</span>
          </div>
          <h2 style={{ margin: '6px 0 2px' }}>{profile.name}</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}><b>{profile.currentIdentity}</b> → <span style={{ color: 'var(--primary)', fontWeight: 700 }}>{profile.futureIdentity}</span></p>
          <div className="profile-stats">
            <div className="stat-box"><div className="stat-value">{lv.level}</div><div className="stat-label">Level</div></div>
            <div className="stat-box"><div className="stat-value">{profile.totalXp}</div><div className="stat-label">Total XP</div></div>
            <div className="stat-box"><div className="stat-value" style={{ color: 'var(--accent-green)' }}>{avail}</div><div className="stat-label">Available</div></div>
          </div>
          <div style={{ marginTop: 12 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: 'var(--text-secondary)', fontWeight: 600 }}>
              <span>Level Progress: {lv.currentXp}/{lv.nextXp} XP</span><span>{Math.round(lv.progress*100)}%</span>
            </div>
            <div className="progress-bar"><div className="progress-fill" style={{ width: (lv.progress*100)+'%' }}></div></div>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: 24, alignItems: 'start' }} className="dashboard-grid">
        <div>
          <div className="section-header"><h2 className="section-title">⚔️ Quest Board</h2></div>
          <div className="tabs">
            {[['active','⚡ Active'],['weekly','📅 Weekly'],['archive','📦 Archive']].map(([k,l]) => (
              <button key={k} className={'tab-btn'+(tab===k?' active':'')} onClick={()=>setTab(k)}>{l}</button>
            ))}
          </div>
          {filtered.length === 0 ? (
            <div className="empty-state"><div className="empty-icon">{tab==='archive'?'📦':'⚔️'}</div><p>{tab==='archive'?'No completed quests yet.':'No active quests. Add one!'}</p></div>
          ) : filtered.map(t => (
            <div key={t.id} className={'task-item' + (t.isCompleted?' completed':'')}>
              <button className={'task-check'+(t.isCompleted?' checked':'')} onClick={()=>toggleTask(t.id)}>{t.isCompleted?'✓':''}</button>
              <div className="task-info">
                <div className="task-title">{t.title}</div>
                <div className="task-meta">{goalName(t.goalId) && <span>{goalName(t.goalId)} · </span>}<span className={'badge badge-'+(t.difficulty==='Small'?'blue':t.difficulty==='Medium'?'orange':'purple')} style={{fontSize:'0.7rem',padding:'2px 8px'}}>{t.difficulty}</span>{t.completedAt && <span style={{marginLeft:6,fontSize:'0.75rem',color:'var(--text-muted)'}}>{t.completedAt.slice(0,10)}</span>}</div>
              </div>
              <span className="task-xp">+{t.xpValue} XP</span>
              <button className="task-delete" onClick={()=>deleteTask(t.id)}>✕</button>
            </div>
          ))}
        </div>

        <div>
          <div className="card">
            <h3 className="card-title" style={{ marginBottom: 16 }}>➕ Quick Add Quest</h3>
            <form onSubmit={addTask}>
              <div className="form-group"><label className="form-label">Quest Description</label><input className="form-input" value={title} onChange={e=>setTitle(e.target.value)} placeholder="e.g. Code 45 mins" required /></div>
              <div className="form-row">
                <div className="form-group"><label className="form-label">Difficulty</label>
                  <select className="form-select" value={diff} onChange={e=>setDiff(e.target.value)}><option>Small</option><option>Medium</option><option>Large</option></select>
                </div>
                <div className="form-group"><label className="form-label">Type</label>
                  <select className="form-select" value={ttype} onChange={e=>setTtype(e.target.value)}><option value="daily">Daily</option><option value="weekly">Weekly</option></select>
                </div>
              </div>
              {goals.length > 0 && (
                <div className="form-group"><label className="form-label">Link to Goal</label>
                  <select className="form-select" value={goalId} onChange={e=>setGoalId(e.target.value)}><option value="">None</option>{goals.map(g=><option key={g.id} value={g.id}>{g.name}</option>)}</select>
                </div>
              )}
              <button className="btn btn-primary btn-block" type="submit">⚡ Create Quest</button>
            </form>
          </div>
          <div className="card" style={{ background: 'var(--bg)' }}>
            <h4 style={{ marginBottom: 10, fontSize: '0.95rem' }}>⚡ XP Rules</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6, fontSize: '0.85rem' }}>
              <div><span className="badge badge-blue" style={{fontSize:'0.7rem',padding:'2px 8px'}}>Small</span> Quick task = <b>10 XP</b></div>
              <div><span className="badge badge-orange" style={{fontSize:'0.7rem',padding:'2px 8px'}}>Medium</span> Focused effort = <b>30 XP</b></div>
              <div><span className="badge badge-purple" style={{fontSize:'0.7rem',padding:'2px 8px'}}>Large</span> Deep work = <b>100 XP</b></div>
            </div>
          </div>
        </div>
      </div>
    </>
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
    const g = { id: genId(), name: name.trim(), duration: dur, finalTarget: ft.trim(), monthlyTarget: mt.trim(), weeklyActions: wa.trim(), hoursPerWeek: hrs, category: cat, createdAt: new Date().toISOString() };
    const newGoals = [g, ...goals];
    LS.set('irisquest_goals', newGoals);
    setGoals(newGoals);
    // Auto-create weekly tasks from weeklyActions
    if (wa.trim()) {
      const newTasks = wa.trim().split('\n').filter(l=>l.trim()).map(l => ({
        id: genId(), goalId: g.id, title: l.trim().replace(/^[-*]\s*/,''), difficulty: 'Medium', xpValue: 30, taskType: 'weekly', isCompleted: false, completedAt: null, createdAt: new Date().toISOString()
      }));
      const allTasks = [...newTasks, ...tasks];
      LS.set('irisquest_tasks', allTasks);
      setTasks(allTasks);
    }
    setName(''); setFt(''); setMt(''); setWa('');
    toast('Goal Created!');
    setTab('list');
  };

  const deleteGoal = (id) => {
    const ng = goals.filter(g=>g.id!==id);
    LS.set('irisquest_goals', ng); setGoals(ng);
    const nt = tasks.filter(t=>t.goalId!==id);
    LS.set('irisquest_tasks', nt); setTasks(nt);
    toast('Goal Deleted');
  };

  return (
    <>
      <div className="section-header"><h2 className="section-title">🎯 Life Goals</h2></div>
      <div className="tabs">
        <button className={'tab-btn'+(tab==='list'?' active':'')} onClick={()=>setTab('list')}>📋 Active Goals</button>
        <button className={'tab-btn'+(tab==='create'?' active':'')} onClick={()=>setTab('create')}>➕ Create Goal</button>
      </div>
      {tab === 'list' ? (
        goals.length === 0 ? <div className="empty-state"><div className="empty-icon">🎯</div><p>No goals yet. Create your first quest campaign!</p></div> :
        goals.map(g => (
          <div className="card" key={g.id}>
            <div className="card-header">
              <div><span className="badge badge-purple">{g.category}</span> <span className="badge badge-blue" style={{marginLeft:4}}>⏱ {g.duration}</span></div>
              <span style={{ fontWeight: 700, color: 'var(--primary)' }}>{g.hoursPerWeek} hrs/wk</span>
            </div>
            <h3 style={{ marginBottom: 4 }}>{g.name}</h3>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: 12 }}>🏆 {g.finalTarget}</p>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
              <div><h4 style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Monthly Target</h4><p style={{ fontSize: '0.9rem' }}>{g.monthlyTarget || '—'}</p></div>
              <div><h4 style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Weekly Actions</h4><p style={{ fontSize: '0.9rem', whiteSpace: 'pre-line' }}>{g.weeklyActions || '—'}</p></div>
            </div>
            <button className="btn btn-danger btn-sm" style={{ marginTop: 12 }} onClick={()=>deleteGoal(g.id)}>🗑 Delete Goal</button>
          </div>
        ))
      ) : (
        <div className="card">
          <h3 className="card-title" style={{ marginBottom: 16 }}>Craft a New Goal</h3>
          <form onSubmit={addGoal}>
            <div className="form-row">
              <div className="form-group"><label className="form-label">Goal Name</label><input className="form-input" value={name} onChange={e=>setName(e.target.value)} placeholder="e.g. Master Full-Stack Dev" required /></div>
              <div className="form-group"><label className="form-label">Category</label>
                <select className="form-select" value={cat} onChange={e=>setCat(e.target.value)}><option>Career</option><option>Health</option><option>Finance</option><option>Creative</option><option>Mindset</option></select>
              </div>
            </div>
            <div className="form-row">
              <div className="form-group"><label className="form-label">Duration</label>
                <select className="form-select" value={dur} onChange={e=>setDur(e.target.value)}>{['30 Days','60 Days','90 Days','180 Days','1 Year'].map(d=><option key={d}>{d}</option>)}</select>
              </div>
              <div className="form-group"><label className="form-label">Hours / Week</label><input className="form-input" type="number" min={1} max={100} value={hrs} onChange={e=>setHrs(+e.target.value)} /></div>
            </div>
            <div className="form-group"><label className="form-label">Final Target</label><input className="form-input" value={ft} onChange={e=>setFt(e.target.value)} placeholder="e.g. Launch 3 apps" required /></div>
            <div className="form-group"><label className="form-label">Monthly Target</label><input className="form-input" value={mt} onChange={e=>setMt(e.target.value)} placeholder="e.g. Ship MVP" /></div>
            <div className="form-group"><label className="form-label">Weekly Actions (1 per line)</label><textarea className="form-textarea" value={wa} onChange={e=>setWa(e.target.value)} placeholder={"Ship 1 feature\nRun 2 tests"} /></div>
            <button className="btn btn-primary btn-block" type="submit">🎯 Create Goal & Seed Quests</button>
          </form>
        </div>
      )}
    </>
  );
}

/* ===== JOURNEY ===== */
function JourneyPage({ profile, goals }) {
  const xp = profile.totalXp;
  const stages = [
    { title: 'Initiate: ' + profile.currentIdentity, desc: 'Foundation & Setup', req: 0 },
    { title: 'Builder Stage', desc: 'Active milestone building', req: 100 },
    { title: 'Creator Stage', desc: 'Scaling & refinement', req: 300 },
    { title: 'Achieved: ' + profile.futureIdentity, desc: 'Final transformation', req: 600 }
  ];
  const getStatus = (i) => { if (xp >= stages[i].req) return 'completed'; if (i === 0 || xp >= stages[i-1].req) return 'active'; return 'locked'; };
  return (
    <>
      <div className="section-header"><h2 className="section-title">🗺️ Transformation Journey</h2></div>
      <div className="card" style={{ background: 'linear-gradient(135deg, #FFFFFF 0%, #F0F2FF 100%)' }}>
        <span className="badge badge-purple">Identity Roadmap</span>
        <h3 style={{ margin: '8px 0 2px' }}>{profile.currentIdentity} → {profile.futureIdentity}</h3>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Total XP: <b>{xp}</b></p>
      </div>
      <div className="journey-pipeline">
        {stages.map((s, i) => {
          const st = getStatus(i);
          const icon = st === 'completed' ? '✅' : st === 'active' ? '🚀' : '🔒';
          return (
            <React.Fragment key={i}>
              <div className={'journey-node ' + st}>
                <div className={'journey-icon ' + st}>{icon}</div>
                <div>
                  <div style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', letterSpacing: 0.5 }}>
                    Stage {i+1} · {st === 'completed' ? 'Cleared' : st === 'active' ? 'Active' : `Locked (${s.req} XP)`}
                  </div>
                  <h4 style={{ margin: '4px 0 2px' }}>{s.title}</h4>
                  <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>{s.desc}</p>
                </div>
              </div>
              {i < stages.length - 1 && <div className="journey-connector" />}
            </React.Fragment>
          );
        })}
      </div>
    </>
  );
}

/* ===== REWARDS ===== */
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
    toast('🎁 Reward Unlocked: ' + r.name);
  };

  const addReward = (e) => {
    e.preventDefault();
    if (!rn.trim()) return;
    const r = { id: genId(), name: rn.trim(), category: rc, xpCost: rxp, expiryDate: rexp.trim(), isClaimed: false, claimedAt: null };
    const nr = [r, ...rewards];
    LS.set('irisquest_rewards', nr); setRewards(nr); setRn('');
    toast('Reward Added!'); setTab('shop');
  };

  const deleteReward = (id) => {
    const nr = rewards.filter(r=>r.id!==id);
    LS.set('irisquest_rewards', nr); setRewards(nr);
  };

  const tierFilter = (r) => {
    if (filter==='All') return true;
    if (filter==='Small') return r.xpCost < 100;
    if (filter==='Medium') return r.xpCost >= 100 && r.xpCost < 500;
    return r.xpCost >= 500;
  };

  return (
    <>
      <div className="section-header"><h2 className="section-title">🎁 Reward Store</h2></div>
      <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'linear-gradient(135deg,#FFFFFF,#FFFAF0)', borderColor: 'rgba(253,203,110,0.3)' }}>
        <div><span className="badge badge-orange">Perk Vault</span><h3 style={{margin:'6px 0 0'}}>Unlock Rewards</h3></div>
        <div style={{ textAlign: 'right' }}><div style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--primary)' }}>⚡ {avail}</div><div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Available XP</div></div>
      </div>
      <div className="tabs">
        <button className={'tab-btn'+(tab==='shop'?' active':'')} onClick={()=>setTab('shop')}>🛒 Rewards</button>
        <button className={'tab-btn'+(tab==='add'?' active':'')} onClick={()=>setTab('add')}>➕ Add Reward</button>
      </div>
      {tab === 'shop' ? (
        <>
          <div style={{ display: 'flex', gap: 6, marginBottom: 16, flexWrap: 'wrap' }}>
            {['All','Small','Medium','Big'].map(f=><button key={f} className={'btn btn-sm '+(filter===f?'btn-primary':'btn-secondary')} onClick={()=>setFilter(f)}>{f}</button>)}
          </div>
          {rewards.filter(tierFilter).length === 0 ? <div className="empty-state"><div className="empty-icon">🎁</div><p>No rewards in this tier.</p></div> : (
            <div className="rewards-grid">
              {rewards.filter(tierFilter).map(r => (
                <div className={'reward-card'+(r.isClaimed?' reward-claimed':'')} key={r.id}>
                  <div className="reward-header">
                    <span className="badge badge-rose">{r.category}</span>
                    <span className="reward-cost">⚡ {r.xpCost} XP</span>
                  </div>
                  <div className="reward-name">{r.name}</div>
                  <div className="reward-expiry">⌛ {r.expiryDate || 'Permanent'}</div>
                  <div style={{ display: 'flex', gap: 8 }}>
                    {r.isClaimed ? <span className="badge badge-green">✓ Claimed</span> :
                      <button className="btn btn-primary btn-sm" disabled={avail < r.xpCost} onClick={()=>claim(r.id)}>Unlock ⚡ {r.xpCost}</button>}
                    <button className="btn btn-danger btn-sm" onClick={()=>deleteReward(r.id)}>✕</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      ) : (
        <div className="card">
          <h3 className="card-title" style={{ marginBottom: 16 }}>Add Custom Reward</h3>
          <form onSubmit={addReward}>
            <div className="form-group"><label className="form-label">Reward Name</label><input className="form-input" value={rn} onChange={e=>setRn(e.target.value)} placeholder="e.g. Coffee Break" required /></div>
            <div className="form-row">
              <div className="form-group"><label className="form-label">Category</label>
                <select className="form-select" value={rc} onChange={e=>setRc(e.target.value)}><option>Treat</option><option>Entertainment</option><option>Shopping</option><option>Experience</option><option>Break</option></select>
              </div>
              <div className="form-group"><label className="form-label">XP Cost</label><input className="form-input" type="number" min={10} value={rxp} onChange={e=>setRxp(+e.target.value)} /></div>
            </div>
            <div className="form-group"><label className="form-label">Expiry / Availability</label><input className="form-input" value={rexp} onChange={e=>setRexp(e.target.value)} placeholder="e.g. This Weekend" /></div>
            <button className="btn btn-primary btn-block" type="submit">🎁 Add Reward</button>
          </form>
        </div>
      )}
    </>
  );
}

/* ===== REVIEW ===== */
function ReviewPage({ profile, setProfile, tasks, reviews, setReviews, toast }) {
  const [tab, setTab] = React.useState('write');
  const now = new Date();
  const ws = new Date(now); ws.setDate(now.getDate() - now.getDay());
  const weekStr = 'Week of ' + ws.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  const completedTasks = tasks.filter(t=>t.isCompleted);
  const autoSummary = completedTasks.slice(0,8).map(t => '• ' + t.title + ' (+' + t.xpValue + ' XP)').join('\n') || 'No completed quests yet.';

  const [comp, setComp] = React.useState('');
  const [fail, setFail] = React.useState('');
  const [next, setNext] = React.useState('');

  const submit = (e) => {
    e.preventDefault();
    const r = { id: genId(), weekStart: weekStr, completed: comp || autoSummary, failed: fail, nextMission: next, createdAt: new Date().toISOString() };
    const nr = [r, ...reviews];
    LS.set('irisquest_reviews', nr); setReviews(nr);
    const np = { ...profile, totalXp: profile.totalXp + 50 };
    LS.set('irisquest_profile', np); setProfile(np);
    setComp(''); setFail(''); setNext('');
    toast('📝 Review Saved! +50 Bonus XP!');
    setTab('past');
  };

  return (
    <>
      <div className="section-header"><h2 className="section-title">📝 Weekly Review</h2></div>
      <div className="tabs">
        <button className={'tab-btn'+(tab==='write'?' active':'')} onClick={()=>setTab('write')}>✍️ Write Review</button>
        <button className={'tab-btn'+(tab==='past'?' active':'')} onClick={()=>setTab('past')}>📜 Past Reviews</button>
      </div>
      {tab === 'write' ? (
        <div className="card">
          <h3 style={{ marginBottom: 4 }}>🗓️ {weekStr}</h3>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 16 }}>Completing this review earns you <b style={{color:'var(--primary)'}}>+50 Bonus XP</b></p>
          <form onSubmit={submit}>
            <div className="form-group"><label className="form-label">✅ What did I complete?</label><textarea className="form-textarea" value={comp} onChange={e=>setComp(e.target.value)} placeholder={autoSummary} /></div>
            <div className="form-group"><label className="form-label">⚠️ What failed or caused friction?</label><textarea className="form-textarea" value={fail} onChange={e=>setFail(e.target.value)} placeholder="e.g. Got distracted, underestimated scope" /></div>
            <div className="form-group"><label className="form-label">🎯 Next week's mission?</label><textarea className="form-textarea" value={next} onChange={e=>setNext(e.target.value)} placeholder="e.g. Ship MVP, 3 user tests" /></div>
            <button className="btn btn-primary btn-block" type="submit">📝 Submit Weekly Review</button>
          </form>
        </div>
      ) : (
        reviews.length === 0 ? <div className="empty-state"><div className="empty-icon">📜</div><p>No past reviews. Write your first one!</p></div> :
        reviews.map(r => (
          <div className="review-entry" key={r.id}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}><span className="badge badge-blue">{r.weekStart}</span><span className="review-date">{r.createdAt?.slice(0,10)}</span></div>
            <div className="review-section"><h4 style={{ color: 'var(--accent-green)' }}>✅ Completed</h4><p>{r.completed}</p></div>
            <div className="review-section" style={{marginTop:10}}><h4 style={{ color: '#E17055' }}>⚠️ Obstacles</h4><p>{r.failed || 'None logged.'}</p></div>
            <div className="review-section" style={{marginTop:10}}><h4 style={{ color: 'var(--primary)' }}>🎯 Next Mission</h4><p>{r.nextMission || '—'}</p></div>
          </div>
        ))
      )}
    </>
  );
}

/* ===== PROFILE PAGE ===== */
function ProfilePage({ profile, setProfile, tasks, setTasks, rewards, setRewards, toast }) {
  const [ci, setCi] = React.useState(profile.currentIdentity);
  const [fi, setFi] = React.useState(profile.futureIdentity);

  const update = (e) => {
    e.preventDefault();
    const np = { ...profile, currentIdentity: ci, futureIdentity: fi };
    LS.set('irisquest_profile', np); setProfile(np);
    toast('Identity Updated!');
  };

  const softReset = () => {
    const np = { ...profile, totalXp: 0, spentXp: 0 };
    LS.set('irisquest_profile', np); setProfile(np);
    const nt = tasks.map(t=>({...t, isCompleted: false, completedAt: null}));
    LS.set('irisquest_tasks', nt); setTasks(nt);
    const nr = rewards.map(r=>({...r, isClaimed: false, claimedAt: null}));
    LS.set('irisquest_rewards', nr); setRewards(nr);
    toast('🔄 Progress Reset!');
  };

  const fullReset = () => {
    ['irisquest_profile','irisquest_goals','irisquest_tasks','irisquest_rewards','irisquest_reviews'].forEach(k=>localStorage.removeItem(k));
    window.location.reload();
  };

  return (
    <>
      <div className="section-header"><h2 className="section-title">👤 Character Profile</h2></div>
      <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: 24, alignItems: 'start' }} className="profile-grid">
        <div className="card" style={{ textAlign: 'center' }}>
          <div className="avatar-circle" style={{ margin: '0 auto 14px', width: 80, height: 80, fontSize: '2.4rem' }}>{profile.avatar}</div>
          <h2 style={{ margin: 0 }}>{profile.name}</h2>
          <p style={{ color: 'var(--text-muted)', margin: '4px 0 14px' }}>{profile.currentIdentity} → {profile.futureIdentity}</p>
          <span className="badge badge-purple">Total XP: {profile.totalXp}</span>
        </div>
        <div>
          <div className="card">
            <h3 className="card-title" style={{ marginBottom: 16 }}>Edit Identity</h3>
            <form onSubmit={update}>
              <div className="form-group"><label className="form-label">Current Identity</label><input className="form-input" value={ci} onChange={e=>setCi(e.target.value)} /></div>
              <div className="form-group"><label className="form-label">Future Vision</label><input className="form-input" value={fi} onChange={e=>setFi(e.target.value)} /></div>
              <button className="btn btn-primary" type="submit">Update Identity</button>
            </form>
          </div>
          <div className="card">
            <h3 className="card-title" style={{ marginBottom: 16, color: '#E84393' }}>⚠️ Reset Options</h3>
            <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
              <button className="btn btn-secondary" onClick={softReset}>🔄 Soft Reset (XP & Tasks)</button>
              <button className="btn btn-danger" onClick={fullReset}>🚨 Full Account Reset</button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

/* ===== MAIN APP ===== */
function App() {
  const [profile, setProfile] = React.useState(LS.get('irisquest_profile'));
  const [goals, setGoals] = React.useState(LS.get('irisquest_goals') || []);
  const [tasks, setTasks] = React.useState(LS.get('irisquest_tasks') || []);
  const [rewards, setRewards] = React.useState(LS.get('irisquest_rewards') || []);
  const [reviews, setReviews] = React.useState(LS.get('irisquest_reviews') || []);
  const [page, setPage] = React.useState('dashboard');
  const [toastMsg, setToastMsg] = React.useState(null);

  const showToast = (msg) => { setToastMsg(msg); };

  if (!profile) return <Onboarding onComplete={(p) => { setProfile(p); setPage('dashboard'); }} />;

  const lv = calcLevel(profile.totalXp);
  const avail = profile.totalXp - profile.spentXp;

  const NAV = [
    ['dashboard', '⚡', 'Dashboard'],
    ['goals', '🎯', 'Goals'],
    ['journey', '🗺️', 'Journey'],
    ['rewards', '🎁', 'Rewards'],
    ['review', '📝', 'Review'],
    ['profile', '👤', 'Profile']
  ];

  return (
    <div className="app-container">
      {toastMsg && <Toast message={toastMsg} onClose={()=>setToastMsg(null)} />}

      {/* Header */}
      <header className="app-header">
        <div className="logo">
          <div className="logo-icon">⚔️</div>
          <div className="logo-text">
            <h1>IRIS QUEST</h1>
            <p>Personal RPG Productivity</p>
          </div>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <span className="badge badge-purple">Lvl {lv.level} · {lv.title}</span>
          <span className="badge badge-green">⚡ {avail} XP</span>
        </div>
      </header>

      {/* Nav */}
      <nav className="nav-bar">
        {NAV.map(([key, icon, label]) => (
          <button key={key} className={'nav-btn'+(page===key?' active':'')} onClick={()=>setPage(key)}>
            <span className="nav-icon">{icon}</span>{label}
          </button>
        ))}
      </nav>

      {/* Content */}
      {page === 'dashboard' && <Dashboard profile={profile} tasks={tasks} goals={goals} setTasks={setTasks} setProfile={setProfile} toast={showToast} />}
      {page === 'goals' && <GoalsPage goals={goals} setGoals={setGoals} tasks={tasks} setTasks={setTasks} toast={showToast} />}
      {page === 'journey' && <JourneyPage profile={profile} goals={goals} />}
      {page === 'rewards' && <RewardsPage profile={profile} setProfile={setProfile} rewards={rewards} setRewards={setRewards} toast={showToast} />}
      {page === 'review' && <ReviewPage profile={profile} setProfile={setProfile} tasks={tasks} reviews={reviews} setReviews={setReviews} toast={showToast} />}
      {page === 'profile' && <ProfilePage profile={profile} setProfile={setProfile} tasks={tasks} setTasks={setTasks} rewards={rewards} setRewards={setRewards} toast={showToast} />}
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);

/* ===== DATA PERSISTENCE HELPERS ===== */
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
  const titles = ['Novice','Scholar','Builder','Strategist','Architect','Creator','Master','Sage'];
  const title = titles[Math.min(titles.length-1, Math.floor((level-1)/3))];
  const rankClass = level >= 7 ? 'lvl-sage' : level >= 4 ? 'lvl-creator' : level >= 2 ? 'lvl-builder' : 'lvl-novice';
  return { level, currentXp, nextXp, progress, title, rankClass };
};

// PWA Recurring Tasks Reset Manager
const checkRecurringTasks = (tasksList) => {
  let updated = false;
  const now = new Date();
  const todayStr = now.toDateString();

  const newTasks = tasksList.map(t => {
    if (t.isCompleted && t.completedAt && t.repeatType && t.repeatType !== 'None') {
      const compDate = new Date(t.completedAt);
      const compDateStr = compDate.toDateString();
      let shouldReset = false;

      if (t.repeatType === 'Daily' && todayStr !== compDateStr) {
        if (!t.repeatEnd || new Date(t.repeatEnd) >= now) {
          shouldReset = true;
        }
      } else if (t.repeatType === 'Weekly') {
        const oneWeekMs = 7 * 24 * 3600 * 1000;
        if (now.getTime() - compDate.getTime() >= oneWeekMs) {
          if (!t.repeatEnd || new Date(t.repeatEnd) >= now) {
            shouldReset = true;
          }
        }
      }

      if (shouldReset) {
        updated = true;
        // Reset completed state for new occurrences
        return { ...t, isCompleted: false, completedAt: null };
      }
    }
    return t;
  });

  return { newTasks, updated };
};

// Campaign duration converter
const getDurationWeeks = (durationStr) => {
  if (!durationStr) return 12;
  const ds = durationStr.toLowerCase();
  if (ds.includes('3 month')) return 12;
  if (ds.includes('6 month')) return 26;
  if (ds.includes('1 year') || ds.includes('12 month')) return 52;
  const matches = ds.match(/\d+/);
  if (matches) {
    const val = parseInt(matches[0]);
    if (ds.includes('week')) return val;
    if (ds.includes('day')) return Math.max(1, Math.ceil(val / 7));
    if (ds.includes('month')) return Math.ceil(val * 4.33);
    return Math.max(1, Math.ceil(val / 7));
  }
  return 12;
};

// Estimate duration-based quest progress (prevents 100% completion in week 1)
const getDurationGoalProgress = (g, tasksList) => {
  const totalWeeks = getDurationWeeks(g.duration);
  const linked = tasksList.filter(t => t.goalId === g.id);
  const completedCount = linked.filter(t => t.isCompleted).length;
  
  // Assume average 3 quests per week across duration
  const estTotalQuests = totalWeeks * 3;
  let prog = Math.round((completedCount / estTotalQuests) * 100);
  if (completedCount > 0 && prog === 0) prog = 1; // minimum 1% if any is done
  
  // If they completed all actual linked tasks and duration has elapsed, show 100%
  if (linked.length > 0 && linked.every(t => t.isCompleted)) {
    const start = new Date(g.createdAt || new Date());
    const elapsedWeeks = Math.floor((new Date() - start) / (7 * 24 * 3600 * 1000));
    if (elapsedWeeks >= totalWeeks) return 100;
    return Math.min(95, prog || 10);
  }
  return Math.min(100, prog);
};

/* ===== TOAST ===== */
function Toast({ message, onClose }) {
  React.useEffect(() => { const t = setTimeout(onClose, 3000); return () => clearTimeout(t); }, [message]);
  return <div className="toast">{message}</div>;
}

/* ===== ONBOARDING (STEPS 1 - 6 SCREEN BY SCREEN) ===== */
function Onboarding({ onComplete }) {
  const [step, setStep] = React.useState(1);
  
  // Step 1: Identity Launchpad
  const [name, setName] = React.useState('Alex');
  const [avatarType, setAvatarType] = React.useState('Minimal Human');
  const [avatarEmoji, setAvatarEmoji] = React.useState('👤');
  const [curId, setCurId] = React.useState('Student');
  const [futId, setFutId] = React.useState('Product Designer');

  const avatarOptions = [
    { type: 'Minimal Human', emoji: '👤' },
    { type: 'Creative Designer', emoji: '🎨' },
    { type: 'Explorer', emoji: '🧭' },
    { type: 'Builder', emoji: '🛠️' },
    { type: 'Entrepreneur', emoji: '📈' },
    { type: 'AI Creator', emoji: '🤖' }
  ];

  const suggestedChips = [
    'Product Designer', 'Creative Director', 'Founder', 'AI Creator',
    'Independent Creator', 'Researcher', 'Entrepreneur', 'Expert'
  ];

  // Step 3: Goals Setup (Screen by Screen)
  const [tempGoals, setTempGoals] = React.useState([
    { id: 'g1', name: 'Portfolio Design', duration: '6 months', customDuration: '' }
  ]);
  const [goalIndex, setGoalIndex] = React.useState(0);

  const handleGoalNext = (addAnother) => {
    const currentGoalName = tempGoals[goalIndex].name.trim();
    if (!currentGoalName) return;

    if (addAnother) {
      const newId = 'g' + (tempGoals.length + 1);
      const newGoals = [...tempGoals];
      newGoals.push({ id: newId, name: '', duration: '6 months', customDuration: '' });
      setTempGoals(newGoals);
      setGoalIndex(goalIndex + 1);
    } else {
      // Proceed to milestones step
      const defaultMilestones = {};
      tempGoals.forEach(g => {
        defaultMilestones[g.id] = {
          monthlyTarget: 'Complete 1 project',
          weeklyCommitment: '2 hours/week',
          weeklyGoal: 'Design'
        };
      });
      setMilestones(defaultMilestones);
      setMilestoneIndex(0);
      setStep(4);
    }
  };

  const updateGoalField = (index, field, value) => {
    const updated = [...tempGoals];
    updated[index][field] = value;
    setTempGoals(updated);
  };

  // Step 4: Milestones Setup (Screen by Screen)
  const [milestones, setMilestones] = React.useState({});
  const [milestoneIndex, setMilestoneIndex] = React.useState(0);
  const milestoneChips = ['Research', 'Design', 'Prototype', 'Document'];

  const handleMilestoneNext = () => {
    if (milestoneIndex < tempGoals.length - 1) {
      setMilestoneIndex(milestoneIndex + 1);
    } else {
      // Proceed to quests step
      const initialQuests = {};
      const initialTitles = {};
      const initialDiffs = {};
      tempGoals.forEach(g => {
        const weeklyAction = milestones[g.id]?.weeklyGoal || 'Research';
        initialQuests[g.id] = [
          { id: genId(), title: `${weeklyAction} competitors`, difficulty: 'Small' },
          { id: genId(), title: `Define core ${weeklyAction.toLowerCase()} problem`, difficulty: 'Medium' }
        ];
        initialTitles[g.id] = '';
        initialDiffs[g.id] = 'Medium';
      });
      setWeek1Quests(initialQuests);
      setNewQuestTitle(initialTitles);
      setNewQuestDiff(initialDiffs);
      setQuestIndex(0);
      setStep(5);
    }
  };

  const updateMilestone = (goalId, field, value) => {
    setMilestones({
      ...milestones,
      [goalId]: {
        ...milestones[goalId],
        [field]: value
      }
    });
  };

  // Step 5: Quests Creation (Screen by Screen)
  const [week1Quests, setWeek1Quests] = React.useState({});
  const [newQuestTitle, setNewQuestTitle] = React.useState({});
  const [newQuestDiff, setNewQuestDiff] = React.useState({});
  const [questIndex, setQuestIndex] = React.useState(0);

  const handleQuestNext = () => {
    if (questIndex < tempGoals.length - 1) {
      setQuestIndex(questIndex + 1);
    } else {
      setStep(6);
    }
  };

  const addQuest = (goalId) => {
    const qTitle = newQuestTitle[goalId]?.trim();
    if (!qTitle) return;
    const diff = newQuestDiff[goalId] || 'Medium';
    const newQ = { id: genId(), title: qTitle, difficulty: diff };
    setWeek1Quests({
      ...week1Quests,
      [goalId]: [...(week1Quests[goalId] || []), newQ]
    });
    setNewQuestTitle({ ...newQuestTitle, [goalId]: '' });
  };

  const removeQuest = (goalId, questId) => {
    setWeek1Quests({
      ...week1Quests,
      [goalId]: week1Quests[goalId].filter(q => q.id !== questId)
    });
  };

  // Step 6: Reward Personalization presets
  const rewardPresets = [
    { id: 'rp1', name: 'Watch KDrama episode', category: 'Entertainment', type: 'Daily', duration: '30 min', xpCost: 50 },
    { id: 'rp2', name: 'Gaming session', category: 'Entertainment', type: 'Daily', duration: '1 hour', xpCost: 50 },
    { id: 'rp3', name: 'Movies session', category: 'Entertainment', type: 'Weekly', duration: '2 hours', xpCost: 150 },
    { id: 'rp4', name: 'Snack under ₹20', category: 'Food', type: 'Daily', duration: '15 min', xpCost: 50 },
    { id: 'rp5', name: 'Meal under ₹80', category: 'Food', type: 'Weekly', duration: '1 hour', xpCost: 150 },
    { id: 'rp6', name: 'Weekend outing', category: 'Experiences', type: 'Monthly', duration: 'Half day', xpCost: 500 },
    { id: 'rp7', name: 'Tarot reading card pull', category: 'Creative', type: 'Daily', duration: '15 min', xpCost: 50 },
    { id: 'rp8', name: 'Listening to music session', category: 'Creative', type: 'Daily', duration: '30 min', xpCost: 50 },
    { id: 'rp9', name: 'Spend on custom shopping gadgets', category: 'Shopping', type: 'Monthly', duration: 'Half day', xpCost: 500 }
  ];

  const [selectedRewardIds, setSelectedRewardIds] = React.useState(['rp1', 'rp4', 'rp8']);
  const [customRewards, setCustomRewards] = React.useState([]);

  // Custom reward creator form state
  const [crName, setCrName] = React.useState('');
  const [crCat, setCrCat] = React.useState('Entertainment');
  const [crType, setCrType] = React.useState('Daily');
  const [crDur, setCrDur] = React.useState('30 min');

  const addCustomReward = (e) => {
    e.preventDefault();
    if (!crName.trim()) return;
    const calcCost = crType === 'Daily' ? 50 : crType === 'Weekly' ? 150 : 500;
    const newCr = {
      id: genId(),
      name: crName.trim(),
      category: crCat,
      type: crType,
      duration: crDur,
      xpCost: calcCost,
      isClaimed: false,
      claimedAt: null
    };
    setCustomRewards([...customRewards, newCr]);
    setCrName('');
  };

  const togglePresetReward = (id) => {
    if (selectedRewardIds.includes(id)) {
      setSelectedRewardIds(selectedRewardIds.filter(x => x !== id));
    } else {
      setSelectedRewardIds([...selectedRewardIds, id]);
    }
  };

  // Compile final state to enter dashboard
  const finalizeOdyssey = () => {
    const profileData = {
      name: name.trim() || 'Alex',
      avatar: avatarEmoji,
      avatarType,
      currentIdentity: curId.trim() || 'Student',
      futureIdentity: futId.trim() || 'Product Designer',
      totalXp: 0,
      spentXp: 0,
      createdAt: new Date().toISOString()
    };

    const goalsData = tempGoals.map(tg => {
      const ms = milestones[tg.id] || {};
      const finalHrs = ms.weeklyCommitment === 'Custom'
        ? (parseInt(ms.customCommitment) || 10)
        : (parseInt(ms.weeklyCommitment) || 5);
      return {
        id: tg.id,
        name: tg.name || 'My Campaign Journey',
        duration: tg.duration === 'Custom' ? (tg.customDuration || 'Custom') : tg.duration,
        finalTarget: ms.monthlyTarget || 'Build Milestone App',
        monthlyTarget: ms.monthlyTarget || 'First checkpoint',
        weeklyActions: ms.weeklyGoal || 'Research & Design',
        hoursPerWeek: finalHrs,
        category: 'Career',
        createdAt: new Date().toISOString()
      };
    });

    const tasksData = [];
    tempGoals.forEach(tg => {
      const qList = week1Quests[tg.id] || [];
      qList.forEach(q => {
        tasksData.push({
          id: q.id,
          goalId: tg.id,
          title: q.title,
          difficulty: q.difficulty,
          xpValue: XP_MAP[q.difficulty] || 30,
          taskType: 'daily',
          isCompleted: false,
          completedAt: null,
          createdAt: new Date().toISOString()
        });
      });
    });

    const selectedPresetsData = rewardPresets
      .filter(rp => selectedRewardIds.includes(rp.id))
      .map(rp => ({
        id: rp.id,
        name: rp.name,
        category: rp.category,
        xpCost: rp.xpCost,
        expiryDate: rp.type,
        isClaimed: false,
        claimedAt: null
      }));

    const allRewards = [...selectedPresetsData, ...customRewards];

    LS.set('irisquest_profile', profileData);
    LS.set('irisquest_goals', goalsData);
    LS.set('irisquest_tasks', tasksData);
    LS.set('irisquest_rewards', allRewards);
    LS.set('irisquest_reviews', []);

    onComplete(profileData);
  };

  return (
    <div className="app-container" style={{ minHeight: '100vh', display: 'flex', alignItems: 'center' }}>
      
      {/* STEP 1: IDENTITY LAUNCHPAD */}
      {step === 1 && (
        <div className="premium-card" style={{ width: '100%', padding: '28px 20px' }}>
          <div style={{ textAlign: 'center', marginBottom: 20 }}>
            <div style={{ fontSize: '2.5rem', marginBottom: 6 }}>🧭</div>
            <h1 className="large-title" style={{ fontSize: '28px', marginBottom: 4 }}>Begin Your Journey</h1>
            <p className="caption">Transform your goals into a path towards your future self</p>
          </div>

          {/* Google Sign In Option */}
          <button 
            type="button" 
            className="btn-secondary" 
            style={{ 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center', 
              gap: 10, 
              height: '46px', 
              minHeight: '46px', 
              width: '100%', 
              marginBottom: 20, 
              border: '1px solid var(--border-system)',
              background: 'var(--bg-card)',
              color: 'var(--text-primary)',
              fontWeight: 600
            }}
            onClick={() => {
              const mockGoogleName = prompt("Simulated Google Auth: Enter your Google Account Display Name:", "Vanshu Dev");
              if (mockGoogleName) {
                setName(mockGoogleName);
                setAvatarType('Explorer');
                setAvatarEmoji('🧭');
                setCurId('Developer');
                setFutId('Independent Founder');
                alert(`Successfully signed in as ${mockGoogleName}! Profile details pre-populated.`);
              }
            }}
          >
            <svg width="18" height="18" viewBox="0 0 18 18" style={{ display: 'block' }}>
              <path d="M17.64 9.2c0-.63-.06-1.25-.16-1.84H9v3.47h4.84a4.14 4.14 0 0 1-1.8 2.71v2.26h2.91c1.7-1.56 2.69-3.86 2.69-6.6z" fill="#4285F4" />
              <path d="M9 18c2.43 0 4.47-.8 5.96-2.2l-2.91-2.26A5.58 5.58 0 0 1 9 14.54c-2.34 0-4.33-1.57-5.04-3.71H.92v2.33A9 9 0 0 0 9 18z" fill="#34A853" />
              <path d="M3.96 10.83a5.39 5.39 0 0 1 0-3.66V4.84H.92a9 9 0 0 0 0 8.32l3.04-2.33z" fill="#FBBC05" />
              <path d="M9 3.58c1.32 0 2.5.45 3.44 1.35L15 2.4A9 9 0 0 0 .92 4.84l3.04 2.33C4.67 5.15 6.66 3.58 9 3.58z" fill="#EA4335" />
            </svg>
            Sign in with Google
          </button>

          <form onSubmit={(e) => { e.preventDefault(); setStep(2); }}>
            <div className="form-group">
              <label className="form-label">Avatar Identity Type</label>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 10, margin: '10px 0' }}>
                {avatarOptions.map(opt => (
                  <button
                    key={opt.type}
                    type="button"
                    onClick={() => { setAvatarType(opt.type); setAvatarEmoji(opt.emoji); }}
                    style={{
                      padding: '12px 6px',
                      borderRadius: '12px',
                      border: avatarType === opt.type ? '2px solid var(--accent-indigo)' : '1px solid var(--border-system)',
                      background: avatarType === opt.type ? 'rgba(247, 208, 96, 0.12)' : 'var(--bg-card)',
                      cursor: 'pointer',
                      textAlign: 'center',
                      transition: 'var(--transition-ios)'
                    }}
                  >
                    <div style={{ fontSize: '1.6rem', marginBottom: 2 }}>{opt.emoji}</div>
                    <div style={{ fontSize: '10px', fontWeight: 600, color: 'var(--text-primary)' }}>{opt.type}</div>
                  </button>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Hero Name</label>
              <input className="form-input" value={name} onChange={e=>setName(e.target.value)} placeholder="e.g. Alex" required />
            </div>

            <div className="form-group">
              <label className="form-label">Current Identity</label>
              <input className="form-input" value={curId} onChange={e=>setCurId(e.target.value)} placeholder="e.g. Student" required />
            </div>

            <div className="form-group">
              <label className="form-label">Future Identity Destination</label>
              <input className="form-input" value={futId} onChange={e=>setFutId(e.target.value)} placeholder="e.g. Product Designer" required />
              
              <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginTop: 10 }}>
                {suggestedChips.map(chip => (
                  <button
                    key={chip}
                    type="button"
                    onClick={() => setFutId(chip)}
                    className="ios-badge ios-badge-purple"
                    style={{ border: 'none', cursor: 'pointer' }}
                  >
                    {chip}
                  </button>
                ))}
              </div>
            </div>

            <button className="btn-primary" type="submit">Continue</button>
          </form>
        </div>
      )}

      {/* STEP 2: ODYSSEY BLUEPRINT SCREEN */}
      {step === 2 && (
        <div className="premium-card" style={{ width: '100%', padding: '28px 20px' }}>
          <div style={{ textAlign: 'center', marginBottom: 20 }}>
            <h2 className="title">How ODYSSEY Works</h2>
            <p className="caption">A path mapped through daily actions</p>
          </div>

          <div className="infographic-container" style={{ margin: '20px 0' }}>
            {[
              { icon: '👁️', title: 'VISION', desc: 'Where you want to go' },
              { icon: '🎯', title: 'GOALS', desc: 'What you want to achieve' },
              { icon: '⚔️', title: 'QUESTS', desc: 'Small actions that move you forward' },
              { icon: '⚡', title: 'XP', desc: 'Progress you earn' },
              { icon: '🎁', title: 'REWARDS', desc: 'Experiences you unlock' },
              { icon: '🛡️', title: 'FUTURE SELF', desc: 'The person you become' }
            ].map((node) => (
              <div key={node.title} style={{ display: 'flex', gap: 14, alignItems: 'center' }}>
                <div style={{ fontSize: '1.8rem', width: 44, height: 44, display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'rgba(0,0,0,0.02)', borderRadius: '12px', border: '1px solid var(--border-system)' }}>
                  {node.icon}
                </div>
                <div>
                  <h4 style={{ fontSize: '14px', fontWeight: 700, color: 'var(--text-primary)' }}>{node.title}</h4>
                  <p className="caption" style={{ fontSize: '12px' }}>{node.desc}</p>
                </div>
              </div>
            ))}
          </div>

          <button className="btn-primary" onClick={() => setStep(3)}>Create My Odyssey</button>
        </div>
      )}

      {/* STEP 3: GOAL CREATION SCREEN (One by One) */}
      {step === 3 && (
        <div className="premium-card" style={{ width: '100%', padding: '28px 20px' }}>
          <div style={{ marginBottom: 16 }}>
            <span className="ios-badge ios-badge-purple" style={{ marginBottom: 8 }}>Journey Campaign {goalIndex + 1} of {tempGoals.length}</span>
            <h2 className="title" style={{ fontSize: '22px' }}>What journeys are you building?</h2>
            <p className="caption">Map out your campaigns one by one (Max 3)</p>
          </div>

          <div className="premium-card" style={{ padding: 14, border: '1px solid rgba(0,0,0,0.08)', background: 'rgba(0,0,0,0.01)' }}>
            <div className="form-group">
              <label className="form-label" style={{ fontSize: '11px' }}>Journey Name</label>
              <input 
                className="form-input" 
                value={tempGoals[goalIndex].name} 
                onChange={e => updateGoalField(goalIndex, 'name', e.target.value)} 
                placeholder="e.g. Portfolio Journey" 
                required 
              />
            </div>

            <div className="form-group" style={{ marginBottom: 0 }}>
              <label className="form-label" style={{ fontSize: '11px' }}>Duration</label>
              <select 
                className="form-select" 
                value={tempGoals[goalIndex].duration} 
                onChange={e => updateGoalField(goalIndex, 'duration', e.target.value)}
              >
                <option>3 months</option>
                <option>6 months</option>
                <option>1 year</option>
                <option>Custom</option>
              </select>
              {tempGoals[goalIndex].duration === 'Custom' && (
                <input 
                  className="form-input" 
                  style={{ marginTop: 8 }} 
                  value={tempGoals[goalIndex].customDuration} 
                  onChange={e => updateGoalField(goalIndex, 'customDuration', e.target.value)} 
                  placeholder="e.g. 45 Days" 
                  required 
                />
              )}
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            <button 
              className="btn-secondary" 
              type="button" 
              onClick={() => handleGoalNext(true)}
              disabled={!tempGoals[goalIndex].name.trim()}
            >
              ➕ Add another journey
            </button>
            
            <button 
              className="btn-primary" 
              onClick={() => handleGoalNext(false)}
              disabled={!tempGoals[goalIndex].name.trim()}
            >
              Set Milestones
            </button>
          </div>
        </div>
      )}

      {/* STEP 4: GOAL MILESTONE SETUP (One by One) */}
      {step === 4 && (
        <div className="premium-card" style={{ width: '100%', padding: '28px 20px' }}>
          <div style={{ marginBottom: 16 }}>
            <span className="ios-badge ios-badge-purple" style={{ marginBottom: 8 }}>Milestones {milestoneIndex + 1} of {tempGoals.length}</span>
            <h2 className="title" style={{ fontSize: '22px' }}>Define Campaign Milestones</h2>
            <p className="caption">Establish checkpoints for each journey campaign</p>
          </div>

          <div className="premium-card" style={{ padding: 14, background: 'rgba(0,0,0,0.01)', marginBottom: 20 }}>
            <h4 className="section-header" style={{ marginBottom: 12, color: 'var(--accent-indigo)' }}>
              {tempGoals[milestoneIndex].name}
            </h4>

            <div className="form-group">
              <label className="form-label">Monthly Target Milestone</label>
              <input 
                className="form-input" 
                value={milestones[tempGoals[milestoneIndex].id]?.monthlyTarget} 
                onChange={e => updateMilestone(tempGoals[milestoneIndex].id, 'monthlyTarget', e.target.value)} 
                placeholder="e.g. Complete 1 project" 
                required 
              />
            </div>

            <div className="form-group">
              <label className="form-label">Weekly Hour Commitment</label>
              <select 
                className="form-select" 
                value={milestones[tempGoals[milestoneIndex].id]?.weeklyCommitment} 
                onChange={e => updateMilestone(tempGoals[milestoneIndex].id, 'weeklyCommitment', e.target.value)}
              >
                <option>2 hours/week</option>
                <option>5 hours/week</option>
                <option>10 hours/week</option>
                <option>20 hours/week</option>
                <option>Custom</option>
              </select>
              {milestones[tempGoals[milestoneIndex].id]?.weeklyCommitment === 'Custom' && (
                <input 
                  type="number" 
                  className="form-input" 
                  style={{ marginTop: 8 }} 
                  value={milestones[tempGoals[milestoneIndex].id]?.customCommitment || ''} 
                  onChange={e => updateMilestone(tempGoals[milestoneIndex].id, 'customCommitment', e.target.value)} 
                  placeholder="Enter custom weekly hours (e.g. 15)" 
                  required 
                />
              )}
            </div>

            <div className="form-group" style={{ marginBottom: 0 }}>
              <label className="form-label">Weekly Objective / Action Type</label>
              <input 
                className="form-input" 
                value={milestones[tempGoals[milestoneIndex].id]?.weeklyGoal} 
                onChange={e => updateMilestone(tempGoals[milestoneIndex].id, 'weeklyGoal', e.target.value)} 
                placeholder="e.g. Design" 
                required 
              />
              
              <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginTop: 8 }}>
                {milestoneChips.map(chip => (
                  <button
                    key={chip}
                    type="button"
                    onClick={() => updateMilestone(tempGoals[milestoneIndex].id, 'weeklyGoal', chip)}
                    className="ios-badge ios-badge-blue"
                    style={{ border: 'none', cursor: 'pointer' }}
                  >
                    {chip}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <button className="btn-primary" onClick={handleMilestoneNext}>
            {milestoneIndex < tempGoals.length - 1 ? 'Next Campaign Milestones' : 'Create Weekly Quests'}
          </button>
        </div>
      )}

      {/* STEP 5: WEEK 1 QUEST CREATION (One by One) */}
      {step === 5 && (
        <div className="premium-card" style={{ width: '100%', padding: '28px 20px' }}>
          <div style={{ marginBottom: 16 }}>
            <span className="ios-badge ios-badge-purple" style={{ marginBottom: 8 }}>Quests {questIndex + 1} of {tempGoals.length}</span>
            <h2 className="title" style={{ fontSize: '20px' }}>What actions will you complete this week?</h2>
            <p className="caption">Input initial tasks to start your campaign quests</p>
          </div>

          <div className="premium-card" style={{ padding: 14, background: 'rgba(0,0,0,0.01)', marginBottom: 20 }}>
            <h4 className="section-header" style={{ marginBottom: 8, color: 'var(--accent-indigo)' }}>
              {tempGoals[questIndex].name}
            </h4>

            {/* Tasks List */}
            <div style={{ margin: '8px 0' }}>
              {(week1Quests[tempGoals[questIndex].id] || []).map(q => (
                <div key={q.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '6px 10px', background: 'var(--bg-card)', borderRadius: 8, border: '1px solid var(--border-system)', marginBottom: 6 }}>
                  <div style={{ fontSize: '14px', fontWeight: 500 }}>{q.title} <span className="caption">({q.difficulty})</span></div>
                  <button type="button" onClick={() => removeQuest(tempGoals[questIndex].id, q.id)} style={{ background: 'transparent', border: 'none', color: 'var(--accent-pink)', fontSize: '13px', cursor: 'pointer' }}>✕</button>
                </div>
              ))}
            </div>

            {/* Inline task creator */}
            <div style={{ display: 'flex', gap: 6, marginTop: 10 }}>
              <input 
                className="form-input" 
                style={{ flexGrow: 1, height: '40px' }} 
                value={newQuestTitle[tempGoals[questIndex].id]} 
                onChange={e => setNewQuestTitle({ ...newQuestTitle, [tempGoals[questIndex].id]: e.target.value })} 
                placeholder="Add quest details..." 
              />
              <select 
                className="form-select" 
                style={{ width: '90px', height: '40px', padding: '0 8px' }} 
                value={newQuestDiff[tempGoals[questIndex].id]} 
                onChange={e => setNewQuestDiff({ ...newQuestDiff, [tempGoals[questIndex].id]: e.target.value })}
              >
                <option>Small</option>
                <option>Medium</option>
                <option>Large</option>
              </select>
              <button 
                type="button" 
                className="btn-primary" 
                style={{ width: '40px', height: '40px', padding: 0 }} 
                onClick={() => addQuest(tempGoals[questIndex].id)}
              >
                ＋
              </button>
            </div>
          </div>

          <button className="btn-primary" onClick={handleQuestNext}>
            {questIndex < tempGoals.length - 1 ? 'Next Campaign Quests' : 'Select Rewards'}
          </button>
        </div>
      )}

      {/* STEP 6: REWARD PERSONALIZATION */}
      {step === 6 && (
        <div className="premium-card" style={{ width: '100%', padding: '28px 20px', maxHeight: '90vh', overflowY: 'auto' }}>
          <div style={{ marginBottom: 16 }}>
            <h2 className="title" style={{ fontSize: '22px' }}>What motivates your journey?</h2>
            <p className="caption">Complete quests. Earn XP. Unlock experiences.</p>
          </div>

          {/* Presets Library */}
          <div style={{ marginBottom: 20 }}>
            <h4 className="section-header" style={{ fontSize: '14px', textTransform: 'uppercase', color: 'var(--text-secondary)' }}>Library Presets</h4>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginTop: 8 }}>
              {rewardPresets.map(preset => {
                const isSelected = selectedRewardIds.includes(preset.id);
                return (
                  <div 
                    key={preset.id} 
                    onClick={() => togglePresetReward(preset.id)}
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '10px 14px',
                      borderRadius: '12px',
                      border: isSelected ? '2px solid var(--accent-orange)' : '1px solid var(--border-system)',
                      background: isSelected ? 'rgba(255, 149, 0, 0.05)' : 'var(--bg-card)',
                      cursor: 'pointer',
                      transition: 'var(--transition-ios)'
                    }}
                  >
                    <div>
                      <div style={{ fontSize: '14px', fontWeight: 600 }}>{preset.name}</div>
                      <div className="caption" style={{ fontSize: '11px' }}>{preset.category} · {preset.type} ({preset.duration})</div>
                    </div>
                    <div style={{ fontWeight: 800, color: 'var(--accent-orange)' }}>⚡ {preset.xpCost} XP</div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Add custom reward form */}
          <div className="premium-card" style={{ padding: 14, background: 'rgba(0,0,0,0.01)', marginBottom: 20 }}>
            <h4 className="section-header" style={{ fontSize: '13px' }}>➕ Create Custom Reward</h4>
            <form onSubmit={addCustomReward}>
              <div className="form-group">
                <input 
                  className="form-input" 
                  value={crName} 
                  onChange={e=>setCrName(e.target.value)} 
                  placeholder="Reward Name (e.g. Afternoon off)" 
                />
              </div>
              <div className="form-row" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10, marginBottom: 10 }}>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label" style={{ fontSize: '10px' }}>Category</label>
                  <select className="form-select" style={{ height: '38px', fontSize: '13px' }} value={crCat} onChange={e=>setCrCat(e.target.value)}>
                    <option>Entertainment</option><option>Food</option><option>Experiences</option><option>Creative</option><option>Shopping</option>
                  </select>
                </div>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label" style={{ fontSize: '10px' }}>Type</label>
                  <select className="form-select" style={{ height: '38px', fontSize: '13px' }} value={crType} onChange={e=>setCrType(e.target.value)}>
                    <option>Daily</option><option>Weekly</option><option>Monthly</option>
                  </select>
                </div>
              </div>
              <button className="btn-secondary" style={{ height: '38px', fontSize: '13px' }} type="submit">Add Custom Reward</button>
            </form>

            {/* Custom rewards created listing */}
            {customRewards.length > 0 && (
              <div style={{ marginTop: 12 }}>
                {customRewards.map(cr => (
                  <div key={cr.id} style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 10px', background: 'var(--bg-card)', borderRadius: 8, border: '1px solid var(--border-system)', marginBottom: 4, fontSize: '12px' }}>
                    <span>{cr.name} (⚡ {cr.xpCost} XP)</span>
                    <button type="button" onClick={() => setCustomRewards(customRewards.filter(x => x.id !== cr.id))} style={{ border: 'none', background: 'transparent', color: 'var(--accent-pink)', cursor: 'pointer' }}>✕</button>
                  </div>
                ))}
              </div>
            )}
          </div>

          <button className="btn-primary" onClick={finalizeOdyssey}>Enter Dashboard</button>
        </div>
      )}

    </div>
  );
}

/* ===== HOME PAGE (DASHBOARD) ===== */
function HomePage({ profile, tasks, goals, rewards, setPage, toast }) {
  const lv = calcLevel(profile.totalXp);
  const avail = profile.totalXp - profile.spentXp;
  const xpNeeded = lv.nextXp - lv.currentXp;

  const todayTasks = tasks.filter(t => t.taskType === 'daily' && !t.isCompleted);
  const completedTodayCount = tasks.filter(t => t.taskType === 'daily' && t.isCompleted).length;
  const totalTodayCount = todayTasks.length + completedTodayCount;
  const progressPct = totalTodayCount > 0 ? Math.round((completedTodayCount / totalTodayCount) * 100) : 100;

  const nextQuest = todayTasks[0];
  const goalName = (gid) => { const g = goals.find(g => g.id === gid); return g ? g.name : ''; };

  const [showNotif, setShowNotif] = React.useState(false);
  const activeUnusedTickets = rewards.filter(r => r.isClaimed && !r.isUsed).length;
  
  const notificationsList = [];
  if (todayTasks.length > 0) {
    notificationsList.push(`⚡ You have ${todayTasks.length} daily quests remaining on your board!`);
  } else {
    notificationsList.push(`✅ All daily quests cleared for today. Excellent work!`);
  }
  if (activeUnusedTickets > 0) {
    notificationsList.push(`🎁 You have ${activeUnusedTickets} active coupon tickets waiting to be redeemed!`);
  }
  
  const activeNotifsCount = (todayTasks.length > 0 ? 1 : 0) + (activeUnusedTickets > 0 ? 1 : 0);

  const getGoalProgress = (gid) => {
    const g = goals.find(x => x.id === gid);
    return g ? getDurationGoalProgress(g, tasks) : 0;
  };

  return (
    <div>
      {/* Top Header Card with PWA Alerts Bell */}
      <div className="section-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <div>
          <h1 className="large-title" style={{ margin: 0, fontSize: '28px' }}>ODYSSEY</h1>
          <p className="caption">Welcome, {profile.name}</p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          {/* Notification Bell trigger */}
          <button className="notif-bell-btn" type="button" onClick={() => setShowNotif(!showNotif)}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--text-primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
            </svg>
            {activeNotifsCount > 0 && <span className="notif-badge">{activeNotifsCount}</span>}
          </button>

          <div className="avatar-wrapper">
            <div className={`avatar-ring ${lv.rankClass}`}>
              <div className="avatar-main">{profile.avatar}</div>
            </div>
          </div>
        </div>
      </div>

      {showNotif && (
        <div className="notif-panel">
          <div className="notif-panel-header">
            <span style={{ fontWeight: 700, fontSize: '14px' }}>🔔 System Alerts</span>
            <button style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', fontSize: '12px', fontWeight: 600 }} onClick={() => setShowNotif(false)}>Close</button>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {notificationsList.map((notif, idx) => (
              <div className="notif-item" key={idx}>
                {notif}
              </div>
            ))}
            
            <button 
              className="btn-secondary" 
              style={{ height: '36px', minHeight: '36px', fontSize: '12px', marginTop: 10, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 6 }} 
              onClick={() => {
                if ('Notification' in window) {
                  Notification.requestPermission().then(perm => {
                    if (perm === 'granted') {
                      new Notification("ODYSSEY OS", { body: "Browser alerts successfully linked!", icon: "icon.png" });
                      toast("Browser notifications enabled!");
                    } else {
                      toast("Alert permissions denied.");
                    }
                  });
                } else {
                  toast("Browser notifications not supported.");
                }
              }}
            >
              🔔 Request Browser Alerts
            </button>
          </div>
        </div>
      )}

      {/* Profile/Identity Details Card */}
      <div className="premium-card">
        <span className="caption" style={{ fontWeight: 700, textTransform: 'uppercase', fontSize: '11px', color: 'var(--accent-indigo)' }}>Identity Transformation</span>
        <h2 style={{ fontSize: '18px', marginTop: 4 }}>{profile.currentIdentity}</h2>
        <p className="caption" style={{ margin: '2px 0 12px' }}>Destination Blueprint: <b style={{ color: 'var(--accent-indigo)' }}>{profile.futureIdentity}</b></p>
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
          <span className="ios-badge ios-badge-purple">Lvl {lv.level} · {lv.title}</span>
          <span className="ios-badge ios-badge-blue">{profile.avatarType}</span>
        </div>
      </div>

      {/* Today's Quests Card with Progress Ring */}
      <div className="premium-card" style={{ cursor: 'pointer' }} onClick={() => setPage('quests')}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 14 }}>
          <h3 className="section-header" style={{ margin: 0 }}>Today's Quests</h3>
          <span className="caption" style={{ fontWeight: 600 }}>{completedTodayCount}/{totalTodayCount} Cleared</span>
        </div>
        <div style={{ display: 'flex', gap: 16, alignItems: 'center' }}>
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
                <p className="caption" style={{ fontWeight: 700, textTransform: 'uppercase', fontSize: '11px', color: 'var(--accent-indigo)' }}>Active Focus</p>
                <h4 style={{ fontSize: '15px', fontWeight: 600, color: 'var(--text-primary)', marginTop: 2 }}>{nextQuest.title}</h4>
                <p className="caption" style={{ marginTop: 2 }}>{goalName(nextQuest.goalId) || 'General'}</p>
              </>
            ) : (
              <>
                <h4 style={{ fontSize: '15px', fontWeight: 600, color: 'var(--accent-emerald)' }}>All Daily Quests Cleared!</h4>
                <p className="caption" style={{ marginTop: 2 }}>Outstanding work.</p>
              </>
            )}
          </div>
        </div>
      </div>

      {/* XP Card */}
      <div className="premium-card" style={{ background: 'linear-gradient(135deg, var(--bg-card) 0%, var(--bg-system) 100%)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: 12 }}>
          <div>
            <div style={{ fontSize: '36px', fontWeight: 800, color: 'var(--text-primary)', lineHeight: 1 }}>{profile.totalXp} XP</div>
            <p className="caption" style={{ fontSize: '14px', fontWeight: 500, color: 'var(--text-secondary)', marginTop: 6 }}>
              {xpNeeded} XP until Lvl {lv.level + 1}
            </p>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '20px', fontWeight: 800, color: 'var(--accent-emerald)' }}>⚡ {avail}</div>
            <p className="caption">Available Balance</p>
          </div>
        </div>
        <div className="ios-progress-container">
          <div className="ios-progress-track">
            <div className="ios-progress-fill" style={{ width: (lv.progress * 100) + '%' }} />
          </div>
        </div>
      </div>

      {/* Goal Journey Progress Maps (Horizontal visual pathways) */}
      {goals.length > 0 && (
        <div style={{ marginTop: 24, marginBottom: 20 }}>
          <h3 className="section-header" style={{ marginBottom: 12 }}>Active Campaigns Map</h3>
          {goals.map(g => {
            const prog = getGoalProgress(g.id);
            const milestones = [
              { label: 'Start', done: true },
              { label: 'M1', done: prog >= 33 },
              { label: 'M2', done: prog >= 66 },
              { label: 'Dest', done: prog >= 100 }
            ];
            return (
              <div className="premium-card" key={g.id} style={{ padding: '16px 20px', cursor: 'pointer' }} onClick={() => setPage('goals')}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                  <span style={{ fontSize: '14px', fontWeight: 700, color: 'var(--text-primary)' }}>{g.name.toUpperCase()}</span>
                  <span style={{ fontSize: '14px', fontWeight: 800, color: 'var(--accent-indigo)' }}>{prog}%</span>
                </div>
                
                {/* Visual horizontal pipeline for dashboard */}
                <div style={{ position: 'relative', margin: '14px 0 10px' }}>
                  <svg width="100%" height="32" style={{ overflow: 'visible' }}>
                    <line x1="5%" y1="16" x2="95%" y2="16" stroke="var(--border-system)" strokeWidth="3" />
                    <line x1="5%" y1="16" x2={`${5 + (prog * 0.9)}%`} y2="16" stroke="var(--accent-indigo)" strokeWidth="3" />
                    {milestones.map((ms, idx) => {
                      const cx = 5 + (idx * 30);
                      return (
                        <circle 
                          key={idx}
                          cx={`${cx}%`} 
                          cy="16" 
                          r={ms.done ? '6' : '5'} 
                          fill={ms.done ? 'var(--accent-indigo)' : 'var(--bg-card)'} 
                          stroke={ms.done ? 'var(--accent-indigo)' : 'var(--border-system)'} 
                          strokeWidth="2" 
                        />
                      );
                    })}
                  </svg>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

/* ===== GOALS & JOURNEY MAP PAGE ===== */
function GoalsPage({ goals, setGoals, tasks, setTasks, toast }) {
  const [tab, setTab] = React.useState('list');
  const [name, setName] = React.useState('');
  const [cat, setCat] = React.useState('Career');
  const [dur, setDur] = React.useState('6 months');
  const [hrs, setHrs] = React.useState(10);
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
    const newGoals = [...goals, g];
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
    toast('Campaign journey map initialized!');
    setTab('list');
  };

  const deleteGoal = (id) => {
    const ng = goals.filter(g=>g.id!==id);
    LS.set('irisquest_goals', ng); setGoals(ng);
    const nt = tasks.filter(t=>t.goalId!==id);
    LS.set('irisquest_tasks', nt); setTasks(nt);
    toast('Campaign journey deleted.');
  };

  const [expandedWeek, setExpandedWeek] = React.useState({});
  const [expandedGoalIds, setExpandedGoalIds] = React.useState({});
  const [inlineTitle, setInlineTitle] = React.useState({});

  const getGoalProgress = (gId) => {
    const g = goals.find(x => x.id === gId);
    return g ? getDurationGoalProgress(g, tasks) : 0;
  };

  const getNextAction = (gid) => {
    const nextTask = tasks.find(t => t.goalId === gid && !t.isCompleted);
    return nextTask ? nextTask.title : 'All tasks completed';
  };

  return (
    <div>
      <div className="section-header">
        <h1 className="large-title" style={{ margin: 0 }}>Journeys</h1>
      </div>

      <div className="segmented-control">
        <button className={'segmented-btn'+(tab==='list'?' active':'')} onClick={()=>setTab('list')}>Journey Maps</button>
        <button className={'segmented-btn'+(tab==='create'?' active':'')} onClick={()=>setTab('create')}>Create Campaign</button>
      </div>

      {tab === 'list' ? (
        goals.length === 0 ? (
          <div className="empty-state"><div className="empty-state-icon">🧭</div><p>No active journey maps. Initialize a campaign.</p></div>
        ) : (
          goals.map(g => {
            const prog = getGoalProgress(g.id);
            const badgeClass = g.category === 'Career' ? 'ios-badge-blue' :
                               g.category === 'Health' ? 'ios-badge-green' :
                               g.category === 'Finance' ? 'ios-badge-orange' :
                               g.category === 'Creative' ? 'ios-badge-purple' : 'ios-badge-pink';
            
            const totalWeeks = getDurationWeeks(g.duration);
            const weeksArray = Array.from({ length: totalWeeks }, (_, i) => i + 1);

            const toggleWeek = (goalId, wk) => {
              const key = `${goalId}-${wk}`;
              setExpandedWeek(prev => ({
                ...prev,
                [goalId]: prev[goalId] === wk ? null : wk
              }));
            };

            const addInlineQuest = (goalId, wk) => {
              const titleKey = `${goalId}-${wk}`;
              const title = inlineTitle[titleKey]?.trim();
              if (!title) return;
              const t = {
                id: genId(),
                goalId: goalId,
                title: title,
                difficulty: 'Medium',
                xpValue: 30,
                taskType: 'weekly',
                weekNumber: wk,
                isCompleted: false,
                completedAt: null,
                createdAt: new Date().toISOString()
              };
              const updated = [t, ...tasks];
              LS.set('irisquest_tasks', updated);
              setTasks(updated);
              setInlineTitle(prev => ({ ...prev, [titleKey]: '' }));
              toast(`Quest initialized for Week ${wk}!`);
            };

            const toggleInlineTask = (id) => {
              const updated = tasks.map(t => {
                if (t.id !== id) return t;
                const wasCompleted = t.isCompleted;
                return { ...t, isCompleted: !wasCompleted, completedAt: wasCompleted ? null : new Date().toISOString() };
              });
              LS.set('irisquest_tasks', updated);
              setTasks(updated);
              toast('Quest status toggled.');
            };

            const deleteInlineTask = (id) => {
              const updated = tasks.filter(t => t.id !== id);
              LS.set('irisquest_tasks', updated);
              setTasks(updated);
              toast('Quest deleted.');
            };

            const isGoalOpen = !!expandedGoalIds[g.id];
            const toggleGoal = () => {
              setExpandedGoalIds(prev => ({
                ...prev,
                [g.id]: !prev[g.id]
              }));
            };

            return (
              <div className="premium-card" key={g.id} style={{ padding: '16px 20px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12, cursor: 'pointer' }} onClick={toggleGoal}>
                  <span className={`ios-badge ${badgeClass}`}>{g.category}</span>
                  <span className="caption" style={{ fontWeight: 600 }}>{g.hoursPerWeek} hrs / week</span>
                </div>
                
                <h3 className="title" style={{ fontSize: '20px', marginBottom: 4, letterSpacing: '-0.4px', cursor: 'pointer' }} onClick={toggleGoal}>
                  {g.name.toUpperCase()} {isGoalOpen ? '▼' : '▲'}
                </h3>
                <p className="caption" style={{ marginBottom: 16 }}>Timeline Horizon: <b>{g.duration}</b> ({totalWeeks} Weeks)</p>
                
                {/* Journey Duration-based Progress Bar */}
                <div style={{ marginBottom: 18, cursor: 'pointer' }} onClick={toggleGoal}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: 6 }}>
                    <span>Overall Journey Progress</span>
                    <span>{prog}%</span>
                  </div>
                  <div className="ios-progress-track" style={{ height: '6px' }}>
                    <div className="ios-progress-fill" style={{ width: prog + '%' }} />
                  </div>
                </div>

                {!isGoalOpen && (
                  <button className="btn-secondary" style={{ height: '40px', minHeight: '40px', fontSize: '13px', marginTop: 4 }} onClick={toggleGoal}>
                    🧭 View Journey Roadmap & Milestones
                  </button>
                )}

                {/* Collapsible content (Accordion roadmap & checkpoints) */}
                {isGoalOpen && (
                  <div style={{ marginTop: 20 }}>
                    {/* Collapsible Weeks Accordion */}
                    <div style={{ marginBottom: 20 }}>
                      <h4 className="section-header" style={{ fontSize: '13px', color: 'var(--text-secondary)', marginBottom: 8, textTransform: 'uppercase' }}>Weekly Action Roadmap</h4>
                      {weeksArray.map(wk => {
                        const isOpen = expandedWeek[g.id] === wk;
                        const weekTasks = tasks.filter(t => t.goalId === g.id && t.weekNumber === wk);
                        const completedWeekCount = weekTasks.filter(t => t.isCompleted).length;
                        const totalWeekCount = weekTasks.length;
                        const isWeekDone = totalWeekCount > 0 && completedWeekCount === totalWeekCount;

                        return (
                          <div className="collapsible-week" key={wk}>
                            <button className="collapsible-trigger" type="button" onClick={() => toggleWeek(g.id, wk)}>
                              <span style={{ fontSize: '14px', fontWeight: 700, color: isWeekDone ? 'var(--accent-emerald)' : 'var(--text-primary)' }}>
                                {isWeekDone ? '✓ ' : ''}Week {wk} Focus
                              </span>
                              <span className="caption" style={{ fontWeight: 600 }}>
                                {totalWeekCount > 0 ? `${completedWeekCount}/${totalWeekCount} Cleared` : 'No quests'} {isOpen ? '▼' : '▶'}
                              </span>
                            </button>
                            
                            {isOpen && (
                              <div className="collapsible-pane">
                                <div style={{ margin: '8px 0 12px' }}>
                                  {weekTasks.length === 0 ? (
                                    <p className="caption" style={{ fontStyle: 'italic', padding: '4px 0' }}>No quests defined for this week node.</p>
                                  ) : (
                                    weekTasks.map(t => (
                                      <div key={t.id} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '6px 8px', background: 'var(--bg-card)', borderRadius: '8px', border: '1px solid var(--border-system)', marginBottom: 6 }}>
                                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexGrow: 1 }}>
                                          <input 
                                            type="checkbox" 
                                            checked={t.isCompleted} 
                                            onChange={() => toggleInlineTask(t.id)} 
                                            style={{ width: '18px', height: '18px', cursor: 'pointer' }}
                                          />
                                          <span style={{ fontSize: '13px', textDecoration: t.isCompleted ? 'line-through' : 'none', color: t.isCompleted ? 'var(--text-secondary)' : 'var(--text-primary)' }}>
                                            {t.title}
                                          </span>
                                        </div>
                                        <button 
                                          type="button" 
                                          onClick={() => deleteInlineTask(t.id)} 
                                          style={{ background: 'transparent', border: 'none', color: 'var(--accent-pink)', cursor: 'pointer', fontSize: '12px' }}
                                        >
                                          ✕
                                        </button>
                                      </div>
                                    ))
                                  )}
                                </div>

                                {/* Inline task creator */}
                                <div style={{ display: 'flex', gap: 6 }}>
                                  <input 
                                    className="form-input" 
                                    style={{ flexGrow: 1, height: '36px', minHeight: '36px', fontSize: '13px', padding: '0 10px' }} 
                                    value={inlineTitle[`${g.id}-${wk}`] || ''} 
                                    onChange={e => setInlineTitle({ ...inlineTitle, [`${g.id}-${wk}`]: e.target.value })} 
                                    placeholder="Add weekly quest action..." 
                                  />
                                  <button 
                                    type="button" 
                                    className="btn-primary" 
                                    style={{ width: '36px', height: '36px', minHeight: '36px', padding: 0 }} 
                                    onClick={() => addInlineQuest(g.id, wk)}
                                  >
                                    ＋
                                  </button>
                                </div>
                              </div>
                            )}
                          </div>
                        );
                      })}
                    </div>

                    {/* Monthly Checkpoints */}
                    <div style={{ background: 'rgba(0,0,0,0.01)', borderRadius: '12px', padding: '14px 16px', border: '1px solid var(--border-system)', marginBottom: 16 }}>
                      <h4 className="section-header" style={{ fontSize: '12px', textTransform: 'uppercase', color: 'var(--text-secondary)', marginBottom: 10 }}>Monthly Milestones</h4>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <span style={{ fontSize: '13px', fontWeight: 600 }}>Month 1 Checkpoint: <span className="caption">{g.monthlyTarget || 'Checkpoint 1'}</span></span>
                          <span className={'ios-badge ' + (prog >= 33 ? 'ios-badge-green' : 'ios-badge-orange')}>
                            {prog >= 33 ? '✓ Cleared' : '⌛ In Progress'}
                          </span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <span style={{ fontSize: '13px', fontWeight: 600 }}>Month 2 Checkpoint: <span className="caption">Focus Optimization</span></span>
                          <span className={'ios-badge ' + (prog >= 66 ? 'ios-badge-green' : 'ios-badge-orange')}>
                            {prog >= 66 ? '✓ Cleared' : '⌛ Pending'}
                          </span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <span style={{ fontSize: '13px', fontWeight: 600 }}>Destination: <span className="caption">{g.finalTarget || 'Destination Launch'}</span></span>
                          <span className={'ios-badge ' + (prog >= 100 ? 'ios-badge-green' : 'ios-badge-orange')}>
                            {prog >= 100 ? '✓ Cleared' : '⌛ Pending'}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div style={{ display: 'flex', gap: 10, marginTop: 14 }}>
                      <button className="btn-secondary" style={{ height: '40px', minHeight: '40px', fontSize: '13px' }} onClick={toggleGoal}>
                        ▲ Close Journey Map
                      </button>
                      <button className="btn-danger-text" style={{ padding: '0 8px' }} onClick={()=>deleteGoal(g.id)}>🗑️ Delete Campaign</button>
                    </div>
                  </div>
                )}
              </div>
            );
          })
        )
      ) : (
        <div className="premium-card">
          <h3 className="section-header" style={{ marginBottom: 16 }}>Create Campaign Journey</h3>
          <form onSubmit={addGoal}>
            <div className="form-group">
              <label className="form-label">Goal Name</label>
              <input className="form-input" value={name} onChange={e=>setName(e.target.value)} placeholder="e.g. Master Design System" required />
            </div>
            <div className="form-group">
              <label className="form-label">Category</label>
              <select className="form-select" value={cat} onChange={e=>setCat(e.target.value)}>
                <option>Career</option><option>Health</option><option>Finance</option><option>Creative</option><option>Mindset</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Duration Horizon</label>
              <select className="form-select" value={dur} onChange={e=>setDur(e.target.value)}>
                <option>3 months</option><option>6 months</option><option>1 year</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Weekly Hour Budget</label>
              <input className="form-input" type="number" min={1} max={168} value={hrs} onChange={e=>setHrs(+e.target.value)} />
            </div>
            <div className="form-group">
              <label className="form-label">Final Target Milestone</label>
              <input className="form-input" value={ft} onChange={e=>setFt(e.target.value)} placeholder="e.g. Live portfolio link" required />
            </div>
            <div className="form-group">
              <label className="form-label">Monthly Target Milestone</label>
              <input className="form-input" value={mt} onChange={e=>setMt(e.target.value)} placeholder="e.g. Wireframes complete" />
            </div>
            <div className="form-group">
              <label className="form-label">Weekly Actions (1 per line)</label>
              <textarea className="form-textarea" value={wa} onChange={e=>setWa(e.target.value)} placeholder="e.g. Complete 2 layouts&#10;Write 1 case study writeup" />
            </div>
            <button className="btn-primary" type="submit">🎯 Initialize Journey Map</button>
          </form>
        </div>
      )}
    </div>
  );
}

/* ===== QUESTS BOARD PAGE ===== */
function QuestsPage({ profile, tasks, goals, setTasks, setProfile, toast }) {
  const [tab, setTab] = React.useState('active');
  const [title, setTitle] = React.useState('');
  const [diff, setDiff] = React.useState('Medium');
  const [ttype, setTtype] = React.useState('daily');
  const [goalId, setGoalId] = React.useState('');
  const [repeatType, setRepeatType] = React.useState('None');
  const [repeatEnd, setRepeatEnd] = React.useState('');

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
    toast('Quest deleted.');
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
      weekNumber: 1, // Default to Week 1 if linked to campaign
      isCompleted: false, 
      completedAt: null, 
      createdAt: new Date().toISOString(),
      repeatType: repeatType,
      repeatEnd: repeatEnd || null
    };
    const updated = [t, ...tasks];
    LS.set('irisquest_tasks', updated);
    setTasks(updated);
    setTitle('');
    setRepeatType('None');
    setRepeatEnd('');
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
        <div className="empty-state"><div className="empty-state-icon">{tab==='archive'?'📦':'⚔️'}</div><p>All objectives complete.</p></div>
      ) : (
        filtered.map(t => (
          <div key={t.id} className={'quest-item' + (t.isCompleted?' completed':'')}>
            <div className={'quest-checkbox'+(t.isCompleted?' checked':'')} onClick={()=>toggleTask(t.id)}>
              {t.isCompleted && (
                <svg className="quest-checkbox-icon" viewBox="0 0 12 12">
                  <path d="M2.5 6L5 8.5L9.5 3.5" />
                </svg>
              )}
            </div>
            <div className="quest-info">
              <div className="quest-title">{t.title}</div>
              <div className="quest-meta">
                {goalName(t.goalId) && <span>{goalName(t.goalId)} · </span>}
                <span className={'ios-badge ' + (t.difficulty==='Small'?'ios-badge-blue':t.difficulty==='Medium'?'ios-badge-orange':'ios-badge-purple')}>{t.difficulty}</span>
                {t.repeatType && t.repeatType !== 'None' && (
                  <span className="ios-badge ios-badge-pink" style={{ marginLeft: 6 }}>🔁 {t.repeatType}</span>
                )}
              </div>
            </div>
            <span className="quest-xp-badge">+{t.xpValue} XP</span>
            <button className="btn-icon" style={{ width: 28, height: 28, borderRadius: '50%', marginLeft: 10 }} onClick={()=>deleteTask(t.id)}>✕</button>
          </div>
        ))
      )}

      {/* Add custom quest form */}
      <div className="premium-card" style={{ marginTop: 24 }}>
        <h3 className="section-header" style={{ marginBottom: 16 }}>➕ Initialize Quest</h3>
        <form onSubmit={addTask}>
          <div className="form-group">
            <label className="form-label">Quest Description</label>
            <input className="form-input" value={title} onChange={e=>setTitle(e.target.value)} placeholder="e.g. Design details iteration" required />
          </div>
          <div className="form-group">
            <label className="form-label">Difficulty Tier</label>
            <select className="form-select" value={diff} onChange={e=>setDiff(e.target.value)}>
              <option>Small</option><option>Medium</option><option>Large</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Quest Timeline</label>
            <select className="form-select" value={ttype} onChange={e=>setTtype(e.target.value)}>
              <option value="daily">Daily</option><option value="weekly">Weekly</option>
            </select>
          </div>
          {goals.length > 0 && (
            <div className="form-group">
              <label className="form-label">Link Campaign</label>
              <select className="form-select" value={goalId} onChange={e=>setGoalId(e.target.value)}>
                <option value="">None</option>
                {goals.map(g=><option key={g.id} value={g.id}>{g.name}</option>)}
              </select>
            </div>
          )}
          
          {/* Recurrence Settings */}
          <div className="form-group">
            <label className="form-label">🔁 Recurrence / Repeat</label>
            <select className="form-select" value={repeatType} onChange={e=>setRepeatType(e.target.value)}>
              <option value="None">None</option>
              <option value="Daily">Daily</option>
              <option value="Weekly">Weekly</option>
            </select>
          </div>
          {repeatType !== 'None' && (
            <div className="form-group">
              <label className="form-label">Recurrence End Date (Optional)</label>
              <input type="date" className="form-input" value={repeatEnd} onChange={e=>setRepeatEnd(e.target.value)} />
            </div>
          )}

          <button className="btn-primary" type="submit">⚡ Add Quest to Board</button>
        </form>
      </div>
    </div>
  );
}

/* ===== REWARDS STORE PAGE ===== */
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
    const nr = rewards.map(rw => rw.id===id ? { ...rw, isClaimed: true, claimedAt: new Date().toISOString(), isUsed: false } : rw);
    LS.set('irisquest_rewards', nr); setRewards(nr);
    toast('🎁 Perk unlocked and added to ticket wallet!');
  };

  const redeem = (id) => {
    const nr = rewards.map(rw => {
      if (rw.id === id) {
        toast(`🎫 Coupon ticket redeemed: ${rw.name}`);
        // Log redemption event in life timeline history
        return { ...rw, isUsed: true, redeemedAt: new Date().toISOString() };
      }
      return rw;
    });
    LS.set('irisquest_rewards', nr);
    setRewards(nr);
  };

  const addReward = (e) => {
    e.preventDefault();
    if (!rn.trim()) return;
    const r = { id: genId(), name: rn.trim(), category: rc, xpCost: rxp, expiryDate: rexp.trim() || 'Expires in 7 days', isClaimed: false, claimedAt: null, isUsed: false };
    const nr = [r, ...rewards];
    LS.set('irisquest_rewards', nr); setRewards(nr); setRn(''); setRexp('');
    toast('Reward cataloged.'); setTab('shop');
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

  // Helper to calculate dynamic ticket expiry date from claimed time
  const getTicketExpiryStr = (r) => {
    if (!r.claimedAt) return r.expiryDate || 'Expires in 7 days';
    const claimDate = new Date(r.claimedAt);
    
    // Determine expiration duration: Daily = 1 day, Weekly = 7 days, Monthly = 30 days
    let daysToAdd = 7;
    const desc = (r.expiryDate || '').toLowerCase();
    if (desc.includes('daily') || desc.includes('day')) daysToAdd = 1;
    else if (desc.includes('monthly') || desc.includes('month')) daysToAdd = 30;

    const expiryDate = new Date(claimDate.getTime() + (daysToAdd * 24 * 3600 * 1000));
    return expiryDate.toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  };

  const unlockedTickets = rewards.filter(r => r.isClaimed && !r.isUsed);

  return (
    <div>
      <div className="section-header">
        <h1 className="large-title" style={{ margin: 0 }}>Perks</h1>
      </div>

      <div className="premium-card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'linear-gradient(135deg, var(--bg-card), var(--bg-system))', borderColor: 'rgba(88, 86, 214, 0.15)', marginBottom: 16 }}>
        <div>
          <span className="ios-badge ios-badge-orange">Perk Vault</span>
          <h2 className="title" style={{ fontSize: '18px', marginTop: 4 }}>Claim Perks</h2>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '24px', fontWeight: 800, color: 'var(--accent-orange)' }}>⚡ {avail} XP</div>
          <p className="caption">Available Balance</p>
        </div>
      </div>

      <div className="segmented-control" style={{ marginBottom: 16 }}>
        <button className={'segmented-btn'+(tab==='shop'?' active':'')} onClick={()=>setTab('shop')}>Perk Catalog</button>
        <button className={'segmented-btn'+(tab==='wallet'?' active':'')} onClick={()=>setTab('wallet')}>
          My Wallet ({unlockedTickets.length})
        </button>
        <button className={'segmented-btn'+(tab==='add'?' active':'')} onClick={()=>setTab('add')}>Catalog Custom</button>
      </div>

      {tab === 'shop' && (
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

          {rewards.filter(r => !r.isClaimed).filter(tierFilter).length === 0 ? (
            <div className="empty-state"><div className="empty-state-icon">🎁</div><p>No perks in this catalog tier.</p></div>
          ) : (
            rewards.filter(r => !r.isClaimed).filter(tierFilter).map(r => (
              <div className="premium-card" key={r.id}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                  <span className="ios-badge ios-badge-pink">{r.category}</span>
                  <span style={{ fontSize: '18px', fontWeight: 800, color: 'var(--accent-orange)' }}>⚡ {r.xpCost} XP</span>
                </div>
                <h3 className="title" style={{ fontSize: '18px', marginBottom: 4 }}>{r.name}</h3>
                <p className="caption" style={{ marginBottom: 16 }}>⌛ {r.expiryDate || 'Permanent'}</p>
                <div style={{ display: 'flex', gap: 12 }}>
                  <button 
                    className="btn-primary" 
                    style={{ height: '40px', background: 'var(--accent-orange)', boxShadow: 'none' }}
                    disabled={avail < r.xpCost} 
                    onClick={()=>claim(r.id)}
                  >
                    Unlock perk
                  </button>
                  <button className="btn-secondary" style={{ width: '40px', height: '40px', borderRadius: '10px' }} onClick={()=>deleteReward(r.id)}>✕</button>
                </div>
              </div>
            ))
          )}
        </>
      )}

      {tab === 'wallet' && (
        <>
          {unlockedTickets.length === 0 ? (
            <div className="empty-state"><div className="empty-state-icon">🎫</div><p>No active claim tickets. Unlock perks from catalog.</p></div>
          ) : (
            unlockedTickets.map(r => (
              <div className="coupon-card" key={r.id}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 4, width: '68%' }}>
                  <span className="ios-badge ios-badge-purple" style={{ width: 'fit-content', padding: '2px 8px', fontSize: '10px' }}>{r.category.toUpperCase()} TICKET</span>
                  <h3 className="title" style={{ fontSize: '16px', marginTop: 4, letterSpacing: '-0.3px' }}>{r.name}</h3>
                  <span className="caption" style={{ fontSize: '11px', color: 'var(--accent-pink)', fontWeight: 600 }}>⌛ Expiry: {getTicketExpiryStr(r)}</span>
                </div>
                
                <div className="coupon-dashed-border" />
                
                <div style={{ position: 'absolute', right: '4%', top: '50%', transform: 'translateY(-50%)', width: '22%', textAlign: 'center' }}>
                  <button 
                    className="btn-primary" 
                    style={{ height: '36px', minHeight: '36px', fontSize: '12px', padding: '0 8px', background: 'var(--accent-indigo)', borderRadius: '10px', boxShadow: 'none' }}
                    onClick={()=>redeem(r.id)}
                  >
                    Use Claim
                  </button>
                </div>
              </div>
            ))
          )}
        </>
      )}

      {tab === 'add' && (
        <div className="premium-card">
          <h3 className="section-header" style={{ marginBottom: 16 }}>Catalog Custom Perk</h3>
          <form onSubmit={addReward}>
            <div className="form-group">
              <label className="form-label">Reward Name</label>
              <input className="form-input" value={rn} onChange={e=>setRn(e.target.value)} placeholder="e.g. 15 min rest period" required />
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
              <label className="form-label">Expiry Restriction</label>
              <input className="form-input" value={rexp} onChange={e=>setRexp(e.target.value)} placeholder="e.g. Wednesday afternoons only" />
            </div>
            <button className="btn-primary" style={{ background: 'var(--accent-orange)', boxShadow: 'none' }} type="submit">🎁 Catalog Perk</button>
          </form>
        </div>
      )}
    </div>
  );
}

/* ===== PROFILE & TIMELINE PAGE ===== */
function ProfilePage({ profile, setProfile, tasks, setTasks, rewards, setRewards, reviews, setReviews, toast, deferredPrompt, setDeferredPrompt, isStandalone, theme, setTheme }) {
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
    toast('Profile and Identity customization updated.');
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

  const deleteReview = (id) => {
    if (confirm('Are you sure you want to delete this weekly report log?')) {
      const nr = reviews.filter(r => r.id !== id);
      LS.set('irisquest_reviews', nr);
      setReviews(nr);
      toast('Weekly review log removed.');
    }
  };

  // Dynamically assemble chronological timeline entries of all accomplishments
  const timelineEntries = React.useMemo(() => {
    const list = [];
    
    // Add completed tasks
    tasks.filter(t => t.isCompleted && t.completedAt).forEach(t => {
      list.push({
        id: t.id,
        date: new Date(t.completedAt),
        title: `Objective Cleared: ${t.title}`,
        desc: `Earned +${t.xpValue} XP`,
        icon: '✅'
      });
    });

    // Add claimed rewards
    rewards.filter(r => r.isClaimed && r.claimedAt).forEach(r => {
      list.push({
        id: r.id,
        date: new Date(r.claimedAt),
        title: `Perk Unlocked: ${r.name}`,
        desc: `Spent ${r.xpCost} XP`,
        icon: '🎁'
      });
    });

    // Add completed reviews
    reviews.forEach(r => {
      if (r.createdAt) {
        list.push({
          id: r.id,
          date: new Date(r.createdAt),
          title: `Weekly Reflection: ${r.weekStart}`,
          desc: `Completed review milestone. Earned +50 XP bonus.`,
          icon: '📝'
        });
      }
    });

    // Sort descending by date
    return list.sort((a, b) => b.date - a.date);
  }, [tasks, rewards, reviews]);

  const lv = calcLevel(profile.totalXp);

  return (
    <div>
      <div className="section-header">
        <h1 className="large-title" style={{ margin: 0 }}>System Settings</h1>
      </div>

      {!showReview ? (
        <>
          {/* Identity customization display */}
          <div className="premium-card" style={{ textAlign: 'center' }}>
            <div className="avatar-wrapper" style={{ margin: '0 auto 16px' }}>
              <div className={`avatar-ring ${lv.rankClass}`}>
                <div className="avatar-main">{profile.avatar}</div>
              </div>
            </div>
            <h2 className="title" style={{ fontSize: '22px' }}>{profile.name}</h2>
            <p className="caption" style={{ marginTop: 4 }}>{profile.currentIdentity} ➔ <span style={{ color: 'var(--accent-indigo)', fontWeight: 600 }}>{profile.futureIdentity}</span></p>
            <div style={{ marginTop: 12 }}>
              <span className="ios-badge ios-badge-purple" style={{ fontSize: '13px' }}>Total XP Earned: {profile.totalXp}</span>
            </div>
          </div>

          {/* PWA Install Prompt Card */}
          {!isStandalone && deferredPrompt && (
            <div className="premium-card" style={{ background: 'rgba(88,86,214,0.04)', borderColor: 'rgba(88,86,214,0.15)' }}>
              <h3 className="section-header" style={{ marginBottom: 6 }}>📲 Odyssey Home Screen App</h3>
              <p className="body-text" style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>Install ODYSSEY natively for offline access, full-screen view, and local notifications.</p>
              <button 
                className="btn-primary" 
                style={{ marginTop: 16, height: '46px' }} 
                onClick={async () => {
                  if (deferredPrompt) {
                    deferredPrompt.prompt();
                    const { outcome } = await deferredPrompt.userChoice;
                    console.log(`User choice outcome: ${outcome}`);
                    setDeferredPrompt(null);
                  }
                }}
              >
                Add to Home Screen
              </button>
            </div>
          )}
          {isStandalone && (
            <div className="premium-card" style={{ background: 'rgba(52, 199, 89, 0.04)', borderColor: 'rgba(52, 199, 89, 0.15)', textAlign: 'center' }}>
              <span className="ios-badge ios-badge-green">✓ PWA Standalone Active</span>
              <p className="caption" style={{ marginTop: 6 }}>Launched natively from your device home screen.</p>
            </div>
          )}

          {/* Weekly reflection campaign prompt */}
          <div className="premium-card" style={{ background: 'rgba(88,86,214,0.04)', borderColor: 'rgba(88,86,214,0.15)' }}>
            <h3 className="section-header" style={{ marginBottom: 6 }}>Weekly Reflection Log</h3>
            <p className="body-text" style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>Review milestones, assess obstacles and plan next week's campaign. Grants +50 XP.</p>
            <button className="btn-primary" style={{ marginTop: 16, height: '46px' }} onClick={()=>setShowReview(true)}>Write Weekly Review</button>
          </div>
          
          {/* Theme Settings Card */}
          <div className="premium-card">
            <h3 className="section-header" style={{ marginBottom: 12 }}>🎨 UI Appearance Mode</h3>
            <p className="caption" style={{ marginBottom: 14 }}>Customize the color palette appearance of ODYSSEY OS.</p>
            <div className="segmented-control" style={{ marginBottom: 0 }}>
              <button 
                type="button"
                className={'segmented-btn' + (theme === 'light' ? ' active' : '')} 
                onClick={() => { setTheme('light'); toast('Light Mode active'); }}
              >
                ☀️ Light
              </button>
              <button 
                type="button"
                className={'segmented-btn' + (theme === 'dark' ? ' active' : '')} 
                onClick={() => { setTheme('dark'); toast('Dark Mode active'); }}
              >
                🌙 Dark
              </button>
              <button 
                type="button"
                className={'segmented-btn' + (theme === 'system' ? ' active' : '')} 
                onClick={() => { setTheme('system'); toast('System Preference mode active'); }}
              >
                ⚙️ System
              </button>
            </div>
          </div>

          {/* Edit Identity mapping form */}
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
              <button className="btn-secondary" type="submit">Update Identity Mapping</button>
            </form>
          </div>

          {/* Life Timeline log */}
          <div className="premium-card">
            <h3 className="section-header" style={{ marginBottom: 12 }}>Life Timeline Log</h3>
            {timelineEntries.length === 0 ? (
              <p className="caption">Accomplishments, rewards, and milestones cleared will appear here chronologically.</p>
            ) : (
              <div className="timeline-container">
                <div className="timeline-line" />
                {timelineEntries.slice(0, 10).map((entry, idx) => (
                  <div className="timeline-item" key={entry.id + '-' + idx}>
                    <div className="timeline-dot" />
                    <div style={{ marginLeft: 10 }}>
                      <span className="caption" style={{ fontSize: '11px', fontWeight: 600 }}>
                        {entry.date.toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                      </span>
                      <h4 style={{ fontSize: '14px', fontWeight: 600, color: 'var(--text-primary)', marginTop: 2 }}>
                        {entry.icon} {entry.title}
                      </h4>
                      <p className="caption" style={{ marginTop: 2 }}>{entry.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Reflection Review log list */}
          {reviews.length > 0 && (
            <div style={{ marginTop: 24 }}>
              <h3 className="section-header" style={{ marginBottom: 12 }}>Reflection Logs</h3>
              {reviews.map(r => (
                <div className="premium-card" key={r.id}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
                    <span className="ios-badge ios-badge-blue">{r.weekStart}</span>
                    <span className="caption">{r.createdAt?.slice(0,10)}</span>
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
                    <div><h4 className="caption" style={{ fontWeight: 700, color: 'var(--accent-emerald)' }}>Accomplished</h4><p className="body-text" style={{ fontSize: '14px', marginTop: 2 }}>{r.completed}</p></div>
                    <div><h4 className="caption" style={{ fontWeight: 700, color: 'var(--accent-orange)' }}>Obstacles</h4><p className="body-text" style={{ fontSize: '14px', marginTop: 2 }}>{r.failed || 'None logged.'}</p></div>
                    <div><h4 className="caption" style={{ fontWeight: 700, color: 'var(--accent-indigo)' }}>Strategy</h4><p className="body-text" style={{ fontSize: '14px', marginTop: 2 }}>{r.nextMission || '—'}</p></div>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 14, borderTop: '1px solid var(--border-system)', paddingTop: 10 }}>
                    <button className="btn-danger-text" onClick={() => deleteReview(r.id)}>🗑️ Delete Review</button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Reset System Options */}
          <div className="premium-card" style={{ marginTop: 24, border: '1.5px solid rgba(255, 45, 85, 0.15)' }}>
            <h3 className="section-header" style={{ color: 'var(--accent-pink)', marginBottom: 16 }}>⚠️ System Settings</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <button 
                type="button"
                className="btn-secondary" 
                style={{ color: 'var(--text-primary)', fontWeight: 600 }} 
                onClick={() => {
                  if (confirm('Are you sure you want to sign out? Your profile settings will be cleared so you can log back in.')) {
                    localStorage.removeItem('irisquest_profile');
                    window.location.reload();
                  }
                }}
              >
                🚪 Sign Out / Log Out Profile
              </button>
              <button className="btn-secondary" style={{ color: 'var(--text-primary)' }} onClick={softReset}>🔄 Soft Reset (XP & quests)</button>
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
              <textarea className="form-textarea" value={fail} onChange={e=>setFail(e.target.value)} placeholder="e.g. Time management, technical blockages" required />
            </div>
            <div className="form-group">
              <label className="form-label">What is next week's mission?</label>
              <textarea className="form-textarea" value={next} onChange={e=>setNext(e.target.value)} placeholder="e.g. Draft Odyssey visual map layouts" required />
            </div>
            <button className="btn-primary" type="submit">📝 Log Reflection & Earn +50 XP</button>
          </form>
        </div>
      )}
    </div>
  );
}

/* ===== MAIN APP NAVIGATION ===== */
function App() {
  const [profile, setProfile] = React.useState(() => {
    const p = LS.get('irisquest_profile');
    if (p && !p.avatarType) {
      localStorage.removeItem('irisquest_profile');
      return null;
    }
    return p;
  });
  const [goals, setGoals] = React.useState(LS.get('irisquest_goals') || []);
  const [tasks, setTasks] = React.useState(() => {
    const cached = LS.get('irisquest_tasks') || [];
    const { newTasks, updated } = checkRecurringTasks(cached);
    if (updated) {
      LS.set('irisquest_tasks', newTasks);
    }
    return newTasks;
  });
  const [rewards, setRewards] = React.useState(LS.get('irisquest_rewards') || []);
  const [reviews, setReviews] = React.useState(LS.get('irisquest_reviews') || []);
  const [page, setPage] = React.useState('home');
  const [toastMsg, setToastMsg] = React.useState(null);

  const [theme, setTheme] = React.useState(() => {
    try {
      return localStorage.getItem('irisquest_theme') || 'system';
    } catch (e) {
      return 'system';
    }
  });

  const [deferredPrompt, setDeferredPrompt] = React.useState(null);
  const [isStandalone, setIsStandalone] = React.useState(false);

  React.useEffect(() => {
    const root = document.documentElement;
    root.classList.remove('theme-light', 'theme-dark');
    if (theme === 'light') {
      root.classList.add('theme-light');
    } else if (theme === 'dark') {
      root.classList.add('theme-dark');
    }
    try {
      localStorage.setItem('irisquest_theme', theme);
    } catch (e) {}
  }, [theme]);

  React.useEffect(() => {
    const standaloneMode = window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone;
    setIsStandalone(!!standaloneMode);

    const handleInstallPrompt = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
    };
    window.addEventListener('beforeinstallprompt', handleInstallPrompt);
    return () => window.removeEventListener('beforeinstallprompt', handleInstallPrompt);
  }, []);

  const showToast = (msg) => { setToastMsg(msg); };

  if (!profile) return <Onboarding onComplete={(p) => { setProfile(p); setPage('home'); }} />;

  return (
    <div className="app-container">
      {toastMsg && <Toast message={toastMsg} onClose={()=>setToastMsg(null)} />}

      {/* Dynamic Subpages */}
      {page === 'home' && <HomePage profile={profile} tasks={tasks} goals={goals} rewards={rewards} setPage={setPage} toast={showToast} />}
      {page === 'goals' && <GoalsPage goals={goals} setGoals={setGoals} tasks={tasks} setTasks={setTasks} toast={showToast} />}
      {page === 'quests' && <QuestsPage profile={profile} tasks={tasks} goals={goals} setTasks={setTasks} setProfile={setProfile} toast={showToast} />}
      {page === 'rewards' && <RewardsPage profile={profile} setProfile={setProfile} rewards={rewards} setRewards={setRewards} toast={showToast} />}
      {page === 'profile' && (
        <ProfilePage 
          profile={profile} 
          setProfile={setProfile} 
          tasks={tasks} 
          setTasks={setTasks} 
          rewards={rewards} 
          setRewards={setRewards} 
          reviews={reviews} 
          setReviews={setReviews} 
          toast={showToast} 
          deferredPrompt={deferredPrompt}
          setDeferredPrompt={setDeferredPrompt}
          isStandalone={isStandalone}
          theme={theme}
          setTheme={setTheme}
        />
      )}

      {/* Floating Bottom Nav */}
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
            <path d="M16.2 7.8l-2 2M7.8 16.2l2-2" />
            <path d="M12 2v4M12 18v4M2 12h4M18 12h4" />
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
            <circle cx="12" cy="12" r="3" />
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
          </svg>
          <span className="nav-tab-label">Profile</span>
        </button>
      </nav>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);

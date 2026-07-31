import streamlit as st
import datetime
import time
import math

# Page configuration
st.set_page_config(
    page_title="Retro Digital Clock & Dashboard",
    page_icon="📟",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom Styling for Streamlit Layout
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Courier+Prime:wght@400;700&display=swap" rel="stylesheet">
    
    <style>
        /* Define dark terminal style palette */
        :root {
            --term-bg: #07090e;
            --term-text: #8ea4a0;
            --term-accent: #00ffcc;
            --term-card: rgba(16, 22, 33, 0.7);
            --term-border: rgba(0, 255, 204, 0.15);
            --term-glow: rgba(0, 255, 204, 0.05);
        }

        .stApp {
            background-color: var(--term-bg);
            background-image: 
                radial-gradient(circle at 50% 30%, #0d1622 0%, #07090e 100%),
                linear-gradient(rgba(18, 24, 38, 0.1) 50%, transparent 50%);
            background-size: 100% 100%, 100% 4px;
            color: var(--term-text);
            font-family: 'Share Tech Mono', monospace;
        }

        /* Remove default stream-lit elements */
        header, footer, div[data-testid="stToolbar"] {
            visibility: hidden !important;
            display: none !important;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 680px !important;
        }

        /* Shell header styling */
        .terminal-header {
            border-bottom: 2px double var(--term-accent);
            padding-bottom: 1rem;
            margin-bottom: 1.5rem;
            text-align: center;
        }

        .terminal-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: #ffffff;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            text-shadow: 0 0 10px rgba(0, 255, 204, 0.3);
            margin: 0;
        }

        .terminal-subtitle {
            font-size: 0.75rem;
            color: var(--term-text);
            letter-spacing: 0.2em;
            text-transform: uppercase;
            opacity: 0.8;
            margin-top: 0.25rem;
        }

        /* Terminal card box style */
        .terminal-card {
            background: var(--term-card);
            border: 1px solid var(--term-border);
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), inset 0 0 20px var(--term-glow);
            margin-bottom: 1.5rem;
        }

        .terminal-card-title {
            font-size: 0.85rem;
            color: var(--term-accent);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-top: 0;
            margin-bottom: 0.75rem;
            border-bottom: 1px dashed var(--term-border);
            padding-bottom: 0.25rem;
        }

        /* Stats grids */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }

        @media (max-width: 480px) {
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }

        .stat-item {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 6px;
            padding: 0.5rem 0.75rem;
        }

        .stat-label {
            font-size: 0.7rem;
            color: var(--term-text);
            opacity: 0.7;
            text-transform: uppercase;
        }

        .stat-value {
            font-size: 1.1rem;
            font-weight: 700;
            color: #ffffff;
            margin-top: 0.15rem;
        }

        /* Terminal progress bar styling */
        .term-progress {
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
        }

        .progress-meta {
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            margin-bottom: 0.25rem;
        }

        .progress-bar-ascii {
            font-family: 'Courier Prime', monospace;
            font-size: 0.8rem;
            letter-spacing: 0.05em;
            color: var(--term-accent);
            white-space: pre;
            overflow-x: auto;
        }

        /* Styling for sidebar form inputs */
        div[data-testid="stSidebar"] {
            background-color: #05070a !important;
            border-right: 1px solid var(--term-border) !important;
        }
        
        .sidebar-header {
            font-size: 1rem;
            color: var(--term-accent);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 1rem;
            border-bottom: 1px solid var(--term-border);
            padding-bottom: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# Time calculations
now = datetime.datetime.now()

# 1. Swatch Internet Time (Beats)
# Biel Mean Time (BMT) is UTC+1. 
# Total seconds elapsed since midnight in BMT:
utc_now = datetime.datetime.utcnow()
bmt_now = utc_now + datetime.timedelta(hours=1)
seconds_since_midnight = (bmt_now.hour * 3600) + (bmt_now.minute * 60) + bmt_now.second + (bmt_now.microsecond / 1000000.0)
swatch_beats = int((seconds_since_midnight / 86.4) % 1000)

# 2. Julian Date (Simplified calculation)
# Epoch Julian date on Jan 1, 2000 is 2451545.0
# Number of days since Jan 1, 2000:
delta_days = (now - datetime.datetime(2000, 1, 1, 12, 0, 0)).total_seconds() / 86400.0
julian_date = 2451545.0 + delta_days

# 3. Star Date (Standard Sci-fi Formula)
# Approximate Star date = current_year + fraction of year
start_of_year = datetime.datetime(now.year, 1, 1)
end_of_year = datetime.datetime(now.year + 1, 1, 1)
year_duration = (end_of_year - start_of_year).total_seconds()
elapsed_year = (now - start_of_year).total_seconds()
year_fraction = elapsed_year / year_duration
stardate = now.year + year_fraction * 1000

# 4. Day & Year Progress
day_seconds_elapsed = (now.hour * 3600) + (now.minute * 60) + now.second
day_progress_pct = (day_seconds_elapsed / 86400.0) * 100.0
year_progress_pct = year_fraction * 100.0

def make_ascii_progress_bar(pct, length=24):
    filled = int(round((pct / 100.0) * length))
    bar = "[" + "=" * max(0, filled - 1) + (">" if filled > 0 else "") + "." * (length - filled) + "]"
    return bar

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.markdown('<div class="sidebar-header">📡 Control Deck</div>', unsafe_allow_html=True)
    
    st.markdown("### Terminal Settings")
    memo_input = st.text_input("Broadcast Memo to Screen", value="SYS_READY: ONLINE", max_chars=32, help="This text will print dynamically on the CRT screen")
    
    st.markdown("### Additional Info")
    st.markdown(f"""
    **Current Epoch:** `{int(time.time())}`  
    **Julian Day:** `{julian_date:.4f}`  
    **Star Date:** `[ {stardate:.2f} ]`  
    """)
    st.info("The screen matches a vintage computer CRT terminal. Use the screen buttons to toggle modes, themes, sound, and clock settings.")

# --- MAIN APP HEADER ---
st.markdown(f"""
    <div class="terminal-header">
        <h1 class="terminal-title">📟 CRT-88 Terminal</h1>
        <p class="terminal-subtitle">Chronos Computer v1.0.8</p>
    </div>
""", unsafe_allow_html=True)

# --- EMBEDDED RETRO DIGITAL CLOCK CABINET (HTML/CSS/JS Component) ---
# To keep UI response fluid and flicker-free, the physical clock panel is run inside standard JS component.
# Python variables like the memo_input are injected dynamically.

escaped_memo = memo_input.replace('"', '\\"').replace('\n', ' ')

clock_component_html = f"""
<!DOCTYPE html>
<html>
<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=VT323&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --color-primary: #33ffdd;
            --color-secondary: #00ccaa;
            --color-glow: rgba(51, 255, 221, 0.65);
            --color-bg: #0a1614;
            --color-border: #143b35;
            --color-glass: rgba(51, 255, 221, 0.03);
            
            --text-shadow: 0 0 5px var(--color-primary), 0 0 12px var(--color-glow);
            --box-shadow: 0 0 10px var(--color-border), inset 0 0 20px rgba(0,0,0,0.8);
            --screen-blur: 0.5px;
        }}

        body {{
            background: transparent;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Share Tech Mono', monospace;
            overflow: hidden;
            user-select: none;
        }}

        /* CRT Physical Bezel */
        .crt-bezel {{
            background: linear-gradient(135deg, #2d3135 0%, #1a1c1e 100%);
            border: 4px solid #121315;
            border-radius: 20px;
            padding: 15px;
            width: 100%;
            max-width: 580px;
            box-shadow: 
                0 20px 40px rgba(0,0,0,0.7),
                inset 0 2px 2px rgba(255,255,255,0.1),
                inset 0 -2px 2px rgba(0,0,0,0.4);
            box-sizing: border-box;
        }}

        /* The glass tube screen wrapper */
        .crt-screen-frame {{
            background: #030508;
            border-radius: 12px;
            border: 8px solid #1e2124;
            position: relative;
            overflow: hidden;
            box-shadow: inset 0 0 30px rgba(0,0,0,0.9);
        }}

        /* CRT Scanlines, screen curves, and flicker */
        .crt-screen-frame::before {{
            content: " ";
            display: block;
            position: absolute;
            top: 0; left: 0; bottom: 0; right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            z-index: 10;
            background-size: 100% 3px, 3px 100%;
            pointer-events: none;
        }}

        /* Radial Vignette simulation */
        .crt-screen-frame::after {{
            content: " ";
            display: block;
            position: absolute;
            top: 0; left: 0; bottom: 0; right: 0;
            background: radial-gradient(circle, transparent 65%, rgba(0, 0, 0, 0.5) 100%);
            z-index: 11;
            pointer-events: none;
        }}

        .crt-screen {{
            background: var(--color-bg);
            padding: 20px;
            height: 250px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            color: var(--color-primary);
            text-shadow: var(--text-shadow);
            filter: blur(var(--screen-blur));
            position: relative;
            z-index: 2;
            transition: all 0.3s ease;
            box-sizing: border-box;
        }}

        /* Screen flicker */
        .flicker {{
            animation: crt-flicker 0.15s infinite;
        }}

        @keyframes crt-flicker {{
            0% {{ opacity: 0.985; }}
            50% {{ opacity: 1; }}
            100% {{ opacity: 0.99; }}
        }}

        /* Header elements */
        .screen-header {{
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            letter-spacing: 0.1em;
            border-bottom: 1px solid var(--color-border);
            padding-bottom: 4px;
            margin-bottom: 5px;
            opacity: 0.85;
            text-transform: uppercase;
        }}

        .systime {{
            font-size: 0.75rem;
        }}

        /* Main Display Screen Content */
        .screen-content {{
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
        }}

        /* Huge clock digits style */
        .clock-display {{
            font-family: 'VT323', monospace;
            font-size: 5.5rem;
            line-height: 1;
            margin: 0;
            letter-spacing: 0.02em;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .clock-display span.colon {{
            animation: blink 1s step-end infinite;
        }}

        @keyframes blink {{
            from, to {{ opacity: 1; }}
            50% {{ opacity: 0.1; }}
        }}

        .ampm {{
            font-size: 1.8rem;
            margin-left: 5px;
            align-self: flex-end;
            margin-bottom: 10px;
        }}

        /* Bottom stats bar inside terminal screen */
        .screen-footer {{
            border-top: 1px solid var(--color-border);
            padding-top: 5px;
            font-size: 0.75rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            opacity: 0.9;
        }}

        .blinking-cursor {{
            animation: cursor-blink 0.8s infinite;
        }}

        @keyframes cursor-blink {{
            0%, 49% {{ opacity: 1; }}
            50%, 100% {{ opacity: 0; }}
        }}

        /* Tactile physical keyboard/buttons panel below CRT screen */
        .cabinet-controls {{
            margin-top: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 5px 5px 0 5px;
        }}

        .button-group {{
            display: flex;
            gap: 8px;
        }}

        .retro-btn {{
            background: linear-gradient(180deg, #4f5358 0%, #35383c 50%, #202224 100%);
            border: 1px solid #1a1c1d;
            border-radius: 4px;
            color: #d1d5db;
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.7rem;
            font-weight: 700;
            padding: 6px 10px;
            cursor: pointer;
            box-shadow: 
                0 3px 0 #111213,
                0 4px 6px rgba(0,0,0,0.3);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            transition: all 0.05s ease;
            outline: none;
        }}

        .retro-btn:active {{
            transform: translateY(2px);
            box-shadow: 
                0 1px 0 #111213,
                0 2px 3px rgba(0,0,0,0.4);
            color: #ffffff;
        }}

        .retro-btn.active {{
            background: linear-gradient(180deg, #1b2024 0%, #2b3036 100%);
            color: var(--color-primary);
            border-color: var(--color-border);
            box-shadow: 
                inset 0 1px 3px rgba(0,0,0,0.8),
                0 1px 0 rgba(255,255,255,0.05);
            text-shadow: 0 0 4px var(--color-glow);
        }}

        /* Round lights panel */
        .status-indicators {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .led-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 0.55rem;
            color: #9ca3af;
            gap: 3px;
        }}

        .led {{
            width: 8px;
            height: 8px;
            background: var(--color-primary);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--color-primary);
            transition: all 0.3s ease;
        }}

        .led.alarm-active {{
            background: #ff3366 !important;
            box-shadow: 0 0 10px #ff3366 !important;
            animation: alert-blink 0.5s infinite;
        }}

        @keyframes alert-blink {{
            0%, 49% {{ opacity: 1; }}
            50%, 100% {{ opacity: 0.2; }}
        }}

        /* Stopwatch sub-interface styling */
        .stopwatch-panel {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
        }}

        .lap-list {{
            width: 80%;
            height: 60px;
            overflow-y: auto;
            border: 1px dashed var(--color-border);
            padding: 4px 10px;
            font-size: 0.75rem;
            margin-top: 5px;
            box-sizing: border-box;
            background: rgba(0, 0, 0, 0.2);
        }}

        /* Custom scrollbar for terminal list */
        .lap-list::-webkit-scrollbar {{
            width: 4px;
        }}
        .lap-list::-webkit-scrollbar-thumb {{
            background: var(--color-primary);
            border-radius: 2px;
        }}

        /* Timer adjustment buttons style */
        .timer-setup {{
            display: flex;
            gap: 6px;
            margin-top: 10px;
        }}

        .timer-btn {{
            background: transparent;
            border: 1px dashed var(--color-border);
            color: var(--color-primary);
            font-family: 'Share Tech Mono', monospace;
            font-size: 0.7rem;
            padding: 3px 6px;
            cursor: pointer;
        }}
        .timer-btn:hover {{
            background: var(--color-border);
        }}

        /* Alarm trigger layout styling */
        .alarm-warning {{
            animation: full-screen-alert 0.8s infinite;
        }}

        @keyframes full-screen-alert {{
            0%, 100% {{ background: var(--color-bg); }}
            50% {{ background: rgba(255, 0, 70, 0.15); }}
        }}

        /* Progress indicator styled as ASCII bar */
        .ascii-progress-container {{
            font-family: monospace;
            font-size: 0.75rem;
            margin-top: 8px;
        }}
    </style>
</head>
<body>

<div class="crt-bezel">
    <!-- Physical CRT Glass Screen -->
    <div id="screen-frame" class="crt-screen-frame">
        <div id="screen" class="crt-screen flicker">
            <!-- Screen Header -->
            <div class="screen-header">
                <div>CHRONOS // <span id="mode-title">CLOCK</span></div>
                <div id="led-indicator-text">SYS_OK</div>
                <div id="uptime-display">UPT: 00:00</div>
            </div>

            <!-- Screen Center Content (Render changes by mode) -->
            <div id="main-content" class="screen-content">
                <!-- CLOCK MODE (Default) -->
                <div id="clock-mode-panel" style="width:100%; text-align:center;">
                    <div class="clock-display">
                        <span id="hours">12</span><span class="colon">:</span><span id="minutes">00</span><span class="colon" id="sec-colon">:</span><span id="seconds">00</span><span id="ampm-val" class="ampm">AM</span>
                    </div>
                    <div id="date-string" style="font-size: 1.1rem; letter-spacing: 0.1em; margin-top: 5px;">DATE: --/--/----</div>
                </div>

                <!-- STOPWATCH MODE -->
                <div id="stopwatch-mode-panel" class="stopwatch-panel" style="display:none;">
                    <div class="clock-display" style="font-size: 4.8rem;">
                        <span id="sw-time">00:00.00</span>
                    </div>
                    <div style="display:flex; gap:10px; margin-top:5px;">
                        <button class="timer-btn" onclick="toggleStopwatch()">START/STOP</button>
                        <button class="timer-btn" onclick="lapStopwatch()">LAP</button>
                        <button class="timer-btn" onclick="resetStopwatch()">RESET</button>
                    </div>
                    <div class="lap-list" id="sw-laps">
                        <div>LAP HISTORY IS EMPTY</div>
                    </div>
                </div>

                <!-- TIMER MODE -->
                <div id="timer-mode-panel" class="stopwatch-panel" style="display:none;">
                    <div class="clock-display" style="font-size: 5rem;">
                        <span id="timer-display">10:00</span>
                    </div>
                    <div class="timer-setup" id="timer-setup-controls">
                        <button class="timer-btn" onclick="adjustTimer(60)">+1M</button>
                        <button class="timer-btn" onclick="adjustTimer(600)">+10M</button>
                        <button class="timer-btn" onclick="adjustTimer(-60)">-1M</button>
                        <button class="timer-btn" onclick="adjustTimer(-600)">-10M</button>
                    </div>
                    <div style="display:flex; gap:10px; margin-top:8px;">
                        <button class="timer-btn" onclick="toggleTimer()">START/STOP</button>
                        <button class="timer-btn" onclick="resetTimer()">CLEAR</button>
                    </div>
                    <div class="ascii-progress-container" id="timer-ascii-bar">[........................] 0%</div>
                </div>

                <!-- ALARM MODE -->
                <div id="alarm-mode-panel" class="stopwatch-panel" style="display:none;">
                    <div style="font-size:1.1rem; margin-bottom:5px;">SET DAILY ALARM</div>
                    <div class="clock-display" style="font-size: 4.5rem;">
                        <span id="alarm-hours">07</span><span class="colon">:</span><span id="alarm-minutes">00</span><span id="alarm-ampm" class="ampm" style="font-size:1.5rem; margin-bottom:5px; cursor:pointer;" onclick="toggleAlarmAMPM()">AM</span>
                    </div>
                    <div style="display:flex; gap:8px; margin-top:5px;">
                        <button class="timer-btn" onclick="adjustAlarmHours(1)">HR+</button>
                        <button class="timer-btn" onclick="adjustAlarmHours(-1)">HR-</button>
                        <button class="timer-btn" onclick="adjustAlarmMinutes(1)">MIN+</button>
                        <button class="timer-btn" onclick="adjustAlarmMinutes(-1)">MIN-</button>
                    </div>
                    <div style="margin-top:10px; display:flex; gap:10px;">
                        <button id="alarm-toggle-btn" class="timer-btn" style="border-style:solid;" onclick="toggleAlarmArmed()">ARMED: OFF</button>
                        <button class="timer-btn" onclick="triggerTestAlarm()">TEST ALARM</button>
                    </div>
                </div>
            </div>

            <!-- Screen Footer -->
            <div class="screen-footer">
                <div style="max-width: 60%; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
                    MEMO: <span id="memo-display">{escaped_memo}</span><span class="blinking-cursor">_</span>
                </div>
                <div id="beats-display">@000.BEATS</div>
            </div>
        </div>
    </div>

    <!-- Cabinet Controls (Physical Buttons Panel Below Screen) -->
    <div class="cabinet-controls">
        <div class="button-group">
            <button id="btn-clock" class="retro-btn active" onclick="switchMode('clock')">TIME</button>
            <button id="btn-sw" class="retro-btn" onclick="switchMode('sw')">SWATCH</button>
            <button id="btn-timer" class="retro-btn" onclick="switchMode('timer')">TIMER</button>
            <button id="btn-alarm" class="retro-btn" onclick="switchMode('alarm')">ALARM</button>
        </div>

        <div class="status-indicators">
            <!-- Theme cycle button -->
            <button class="retro-btn" style="padding: 4px 8px; font-size: 0.6rem; background: linear-gradient(180deg, #374151 0%, #111827 100%);" onclick="cycleTheme()">THEME</button>
            
            <div class="led-container">
                <div id="indicator-led" class="led"></div>
                <span>POWER</span>
            </div>
        </div>
    </div>
</div>

<script>
    // Audio synthesizer Setup (Web Audio API)
    let audioCtx = null;
    let isMuted = false;
    let alarmTimerId = null;
    let alarmActive = false;

    function playBeep(frequency, duration, type='sine', volume=0.08) {{
        if (isMuted) return;
        try {{
            if (!audioCtx) {{
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }}
            if (audioCtx.state === 'suspended') {{
                audioCtx.resume();
            }}
            
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            
            osc.type = type;
            osc.frequency.setValueAtTime(frequency, audioCtx.currentTime);
            
            gain.gain.setValueAtTime(volume, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.00001, audioCtx.currentTime + duration);
            
            osc.start();
            osc.stop(audioCtx.currentTime + duration);
        }} catch(e) {{
            console.error("Audio failed to initialize", e);
        }}
    }}

    function playButtonSound() {{
        playBeep(1200, 0.05, 'sine', 0.05);
    }}

    function triggerBuzzer() {{
        // Vintage double buzzer beep
        playBeep(880, 0.12, 'square', 0.1);
        setTimeout(() => {{
            playBeep(880, 0.12, 'square', 0.1);
        }}, 160);
    }}

    // State Variables
    let currentMode = 'clock'; // clock, sw, timer, alarm
    let activeThemeIndex = 0;
    const themeList = ['vfd', 'amber', 'cyber', 'lcd'];
    
    // Config Options (default settings)
    let displayFormat24h = false;
    let showSeconds = true;
    let scanlinesEnabled = true;

    // Start App Uptime Timer
    let appStartTime = Date.now();
    setInterval(() => {{
        let diffMs = Date.now() - appStartTime;
        let diffSecs = Math.floor(diffMs / 1000);
        let mins = Math.floor(diffSecs / 60);
        let secs = diffSecs % 60;
        document.getElementById('uptime-display').textContent = 'UPT: ' + 
            String(mins).padStart(2, '0') + ':' + String(secs).padStart(2, '0');
    }}, 1000);

    // Toggle 24h & seconds settings inside iframe dynamically if double clicked
    document.getElementById('hours').addEventListener('dblclick', () => {{
        displayFormat24h = !displayFormat24h;
        playBeep(600, 0.1);
    }});
    document.getElementById('seconds').addEventListener('click', () => {{
        showSeconds = !showSeconds;
        playBeep(600, 0.1);
        document.getElementById('seconds').style.display = showSeconds ? 'inline' : 'none';
        document.getElementById('sec-colon').style.display = showSeconds ? 'inline' : 'none';
    }});

    // Cycle custom retro color Themes
    function cycleTheme() {{
        activeThemeIndex = (activeThemeIndex + 1) % themeList.length;
        applyTheme(themeList[activeThemeIndex]);
        playButtonSound();
    }}

    const themes = {{
        vfd: {{
            primary: '#33ffdd',
            secondary: '#00ccaa',
            glow: 'rgba(51, 255, 221, 0.65)',
            bg: '#0a1614',
            border: '#143b35',
            glass: 'rgba(51, 255, 221, 0.03)'
        }},
        amber: {{
            primary: '#ffb000',
            secondary: '#cc8d00',
            glow: 'rgba(255, 176, 0, 0.65)',
            bg: '#140c00',
            border: '#3b2000',
            glass: 'rgba(255, 176, 0, 0.03)'
        }},
        cyber: {{
            primary: '#ff007f',
            secondary: '#00f0ff',
            glow: 'rgba(255, 0, 127, 0.65)',
            bg: '#090214',
            border: '#2a0c4f',
            glass: 'rgba(255, 0, 127, 0.03)'
        }},
        lcd: {{
            primary: '#2e352c',
            secondary: '#4d5749',
            glow: 'rgba(0, 0, 0, 0)',
            bg: '#8ea388',
            border: '#556350',
            glass: 'rgba(0, 0, 0, 0.02)'
        }}
    }};

    function applyTheme(themeName) {{
        const t = themes[themeName];
        const root = document.documentElement;
        root.style.setProperty('--color-primary', t.primary);
        root.style.setProperty('--color-secondary', t.secondary);
        root.style.setProperty('--color-glow', t.glow);
        root.style.setProperty('--color-bg', t.bg);
        root.style.setProperty('--color-border', t.border);
        root.style.setProperty('--color-glass', t.glass);
        
        const led = document.getElementById('indicator-led');
        
        if (themeName === 'lcd') {{
            root.style.setProperty('--text-shadow', 'none');
            root.style.setProperty('--box-shadow', 'none');
            root.style.setProperty('--screen-blur', '0px');
            if (led) led.style.boxShadow = 'none';
        }} else {{
            root.style.setProperty('--text-shadow', `0 0 4px ${{t.primary}}, 0 0 10px ${{t.glow}}`);
            root.style.setProperty('--box-shadow', `0 0 10px ${{t.border}}, inset 0 0 20px rgba(0,0,0,0.8)`);
            root.style.setProperty('--screen-blur', '0.5px');
            if (led) led.style.boxShadow = `0 0 8px ${{t.primary}}`;
        }}
    }}

    // Switch Panel mode
    function switchMode(mode) {{
        currentMode = mode;
        playButtonSound();

        // Remove active state from all buttons
        document.querySelectorAll('.cabinet-controls .retro-btn').forEach(btn => {{
            btn.classList.remove('active');
        }});
        
        // Add active state to selected button
        document.getElementById('btn-' + mode).classList.add('active');

        // Hide all panels
        document.getElementById('clock-mode-panel').style.display = 'none';
        document.getElementById('stopwatch-mode-panel').style.display = 'none';
        document.getElementById('timer-mode-panel').style.display = 'none';
        document.getElementById('alarm-mode-panel').style.display = 'none';
        
        // Update header Mode Title
        document.getElementById('mode-title').textContent = mode.toUpperCase();

        // Reset alarm notification alert state if user switches panels during alarm
        if (alarmActive) {{
            dismissAlarm();
        }}

        // Show selected panel
        if (mode === 'clock') {{
            document.getElementById('clock-mode-panel').style.display = 'block';
        }} else if (mode === 'sw') {{
            document.getElementById('stopwatch-mode-panel').style.display = 'block';
        }} else if (mode === 'timer') {{
            document.getElementById('timer-mode-panel').style.display = 'block';
            drawTimerProgress();
        }} else if (mode === 'alarm') {{
            document.getElementById('alarm-mode-panel').style.display = 'block';
        }}
    }}

    // ----------------------------------------------------
    // CLOCK LOGIC
    // ----------------------------------------------------
    function updateClock() {{
        const timeNow = new Date();
        
        // Timezones & hours format
        let hours = timeNow.getHours();
        let minutes = timeNow.getMinutes();
        let seconds = timeNow.getSeconds();
        let ampm = '';

        if (!displayFormat24h) {{
            ampm = hours >= 12 ? 'PM' : 'AM';
            hours = hours % 12;
            hours = hours ? hours : 12; // if hour is 0, set to 12
        }}

        document.getElementById('hours').textContent = String(hours).padStart(2, '0');
        document.getElementById('minutes').textContent = String(minutes).padStart(2, '0');
        document.getElementById('seconds').textContent = String(seconds).padStart(2, '0');
        document.getElementById('ampm-val').textContent = ampm;
        document.getElementById('ampm-val').style.display = displayFormat24h ? 'none' : 'inline';

        // Date String Formatting
        const days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
        const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
        const dayName = days[timeNow.getDay()];
        const monthName = months[timeNow.getMonth()];
        const dayNum = String(timeNow.getDate()).padStart(2, '0');
        const year = timeNow.getFullYear();
        document.getElementById('date-string').textContent = `DATE: ${{dayName}} ${{monthName}} ${{dayNum}}, ${{year}}`;

        // Calculate Swatch Internet beats
        // Biel Mean Time is UTC+1.
        const utcHrs = timeNow.getUTCHours();
        const utcMins = timeNow.getUTCMinutes();
        const utcSecs = timeNow.getUTCSeconds();
        const bmtSeconds = ((utcHrs + 1) * 3600 + utcMins * 60 + utcSecs) % 86400;
        const beats = Math.floor(bmtSeconds / 86.4);
        document.getElementById('beats-display').textContent = '@' + String(beats).padStart(3, '0') + '.BEATS';

        // Check Alarm trigger
        checkAlarm(timeNow);
    }}
    setInterval(updateClock, 1000);
    updateClock(); // Initial call

    // ----------------------------------------------------
    // STOPWATCH LOGIC
    // ----------------------------------------------------
    let swRunning = false;
    let swStartTime = 0;
    let swElapsed = 0;
    let swIntervalId = null;
    let lapCounter = 0;

    function toggleStopwatch() {{
        playButtonSound();
        if (swRunning) {{
            // STOP
            swElapsed += Date.now() - swStartTime;
            clearInterval(swIntervalId);
            swRunning = false;
        }} else {{
            // START
            swStartTime = Date.now();
            swIntervalId = setInterval(updateStopwatchDisplay, 10);
            swRunning = true;
        }}
    }}

    function resetStopwatch() {{
        playButtonSound();
        clearInterval(swIntervalId);
        swRunning = false;
        swElapsed = 0;
        lapCounter = 0;
        document.getElementById('sw-time').textContent = '00:00.00';
        document.getElementById('sw-laps').innerHTML = '<div>LAP HISTORY IS EMPTY</div>';
    }}

    function updateStopwatchDisplay() {{
        let timeDiff = swElapsed;
        if (swRunning) {{
            timeDiff += Date.now() - swStartTime;
        }}
        
        let centiseconds = Math.floor((timeDiff % 1000) / 10);
        let seconds = Math.floor((timeDiff / 1000) % 60);
        let minutes = Math.floor((timeDiff / 60000) % 60);

        document.getElementById('sw-time').textContent = 
            String(minutes).padStart(2, '0') + ':' + 
            String(seconds).padStart(2, '0') + '.' + 
            String(centiseconds).padStart(2, '0');
    }}

    function lapStopwatch() {{
        if (swElapsed === 0 && !swRunning) return;
        playButtonSound();
        lapCounter++;
        let timeString = document.getElementById('sw-time').textContent;
        let newLap = document.createElement('div');
        newLap.textContent = `LAP ${{String(lapCounter).padStart(2, '0')}}: ${{timeString}}`;
        const lapContainer = document.getElementById('sw-laps');
        if (lapCounter === 1) lapContainer.innerHTML = '';
        lapContainer.appendChild(newLap);
        lapContainer.scrollTop = lapContainer.scrollHeight;
    }}

    // ----------------------------------------------------
    // TIMER LOGIC
    // ----------------------------------------------------
    let timerDuration = 600; // default 10 minutes in seconds
    let timerRemaining = 600;
    let timerRunning = false;
    let timerIntervalId = null;

    function adjustTimer(secs) {{
        playButtonSound();
        if (timerRunning) return;
        timerDuration = Math.max(10, timerDuration + secs);
        timerRemaining = timerDuration;
        updateTimerDisplay();
        drawTimerProgress();
    }}

    function toggleTimer() {{
        playButtonSound();
        if (timerRunning) {{
            // STOP
            clearInterval(timerIntervalId);
            timerRunning = false;
        }} else {{
            // START
            timerIntervalId = setInterval(() => {{
                if (timerRemaining > 0) {{
                    timerRemaining--;
                    updateTimerDisplay();
                    drawTimerProgress();
                }} else {{
                    // Timer Finished
                    clearInterval(timerIntervalId);
                    timerRunning = false;
                    triggerTimerAlarm();
                }}
            }}, 1000);
            timerRunning = true;
        }}
    }}

    function resetTimer() {{
        playButtonSound();
        clearInterval(timerIntervalId);
        timerRunning = false;
        timerRemaining = timerDuration;
        updateTimerDisplay();
        drawTimerProgress();
        dismissAlarm();
    }}

    function updateTimerDisplay() {{
        let minutes = Math.floor(timerRemaining / 60);
        let seconds = timerRemaining % 60;
        document.getElementById('timer-display').textContent = 
            String(minutes).padStart(2, '0') + ':' + String(seconds).padStart(2, '0');
    }}

    function drawTimerProgress() {{
        const totalBarLength = 20;
        const ratio = timerRemaining / timerDuration;
        const filledLength = Math.round(ratio * totalBarLength);
        const pct = Math.round(ratio * 100);
        
        let barStr = '[' + '='.repeat(Math.max(0, filledLength-1)) + 
                     (filledLength > 0 ? '>' : '') + 
                     '.'.repeat(totalBarLength - filledLength) + '] ' + pct + '%';
        document.getElementById('timer-ascii-bar').textContent = barStr;
    }}

    function triggerTimerAlarm() {{
        alarmActive = true;
        document.getElementById('screen').classList.add('alarm-warning');
        document.getElementById('indicator-led').classList.add('alarm-active');
        document.getElementById('led-indicator-text').textContent = 'TIMER_OUT';
        
        if (alarmTimerId) clearInterval(alarmTimerId);
        alarmTimerId = setInterval(() => {{
            triggerBuzzer();
        }}, 750);
        triggerBuzzer();
    }}

    // ----------------------------------------------------
    // ALARM CONFIG LOGIC
    // ----------------------------------------------------
    let alarmHours = 7;
    let alarmMinutes = 0;
    let alarmAMPM = 'AM';
    let alarmArmed = false;
    let alarmTriggeredToday = false;

    function updateAlarmConfigDisplay() {{
        document.getElementById('alarm-hours').textContent = String(alarmHours).padStart(2, '0');
        document.getElementById('alarm-minutes').textContent = String(alarmMinutes).padStart(2, '0');
        document.getElementById('alarm-ampm').textContent = alarmAMPM;
    }}

    function toggleAlarmAMPM() {{
        playButtonSound();
        alarmAMPM = alarmAMPM === 'AM' ? 'PM' : 'AM';
        updateAlarmConfigDisplay();
    }}

    function adjustAlarmHours(amt) {{
        playButtonSound();
        alarmHours = alarmHours + amt;
        if (alarmHours > 12) alarmHours = 1;
        if (alarmHours < 1) alarmHours = 12;
        updateAlarmConfigDisplay();
    }}

    function adjustAlarmMinutes(amt) {{
        playButtonSound();
        alarmMinutes = alarmMinutes + amt;
        if (alarmMinutes >= 60) alarmMinutes = 0;
        if (alarmMinutes < 0) alarmMinutes = 59;
        updateAlarmConfigDisplay();
    }}

    function toggleAlarmArmed() {{
        playButtonSound();
        alarmArmed = !alarmArmed;
        const btn = document.getElementById('alarm-toggle-btn');
        if (alarmArmed) {{
            btn.textContent = 'ARMED: ON';
            btn.style.color = '#ff3366';
            btn.style.borderColor = '#ff3366';
            alarmTriggeredToday = false;
        }} else {{
            btn.textContent = 'ARMED: OFF';
            btn.style.color = 'var(--color-primary)';
            btn.style.borderColor = 'var(--color-border)';
            dismissAlarm();
        }}
    }}

    function checkAlarm(currentDate) {{
        if (!alarmArmed || alarmActive) return;

        let curHours = currentDate.getHours();
        let curMinutes = currentDate.getMinutes();
        let curSec = currentDate.getSeconds();
        let curAMPM = curHours >= 12 ? 'PM' : 'AM';
        
        let checkHours = curHours % 12;
        checkHours = checkHours ? checkHours : 12;

        if (checkHours === alarmHours && 
            curMinutes === alarmMinutes && 
            curAMPM === alarmAMPM) {{
            
            // To prevent double triggering within the same minute, check seconds and toggle
            if (curSec < 5 && !alarmTriggeredToday) {{
                alarmTriggeredToday = true;
                triggerSystemAlarm();
            }}
        }}

        // Reset alarm triggered state at different hour/minute
        if (curMinutes !== alarmMinutes) {{
            alarmTriggeredToday = false;
        }}
    }}

    // Trigger Alarm State
    function triggerSystemAlarm() {{
        alarmActive = true;
        document.getElementById('screen').classList.add('alarm-warning');
        document.getElementById('indicator-led').classList.add('alarm-active');
        document.getElementById('led-indicator-text').textContent = 'ALARM_ALERT';
        
        if (alarmTimerId) clearInterval(alarmTimerId);
        alarmTimerId = setInterval(() => {{
            triggerBuzzer();
        }}, 700);
        triggerBuzzer();
    }}

    function triggerTestAlarm() {{
        playButtonSound();
        setTimeout(triggerSystemAlarm, 500);
    }}

    function dismissAlarm() {{
        alarmActive = false;
        document.getElementById('screen').classList.remove('alarm-warning');
        document.getElementById('indicator-led').classList.remove('alarm-active');
        document.getElementById('led-indicator-text').textContent = 'SYS_OK';
        if (alarmTimerId) {{
            clearInterval(alarmTimerId);
            alarmTimerId = null;
        }}
    }}

    // Initialize Default State
    applyTheme('vfd');
    updateAlarmConfigDisplay();
    updateTimerDisplay();
</script>

</body>
</html>
"""

st.components.v1.html(clock_component_html, height=360)

# --- SYSTEM TELEMETRY / DATA DISPLAY (Python Calculations) ---
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="terminal-card">
        <div class="terminal-card-title">📡 CYCLICAL PROGRESS</div>
        <div class="term-progress">
            <div class="progress-meta">
                <span>Solar Day Cycle</span>
                <span>{day_progress_pct:.2f}%</span>
            </div>
            <div class="progress-bar-ascii">{make_ascii_progress_bar(day_progress_pct)}</div>
        </div>
        <div class="term-progress" style="margin-top: 1rem;">
            <div class="progress-meta">
                <span>Annual Orbit Progress</span>
                <span>{year_progress_pct:.2f}%</span>
            </div>
            <div class="progress-bar-ascii">{make_ascii_progress_bar(year_progress_pct)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="terminal-card">
        <div class="terminal-card-title">🧮 SYSTEM TELEMETRY</div>
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-label">Swatch Time</div>
                <div class="stat-value">@{swatch_beats:03d} beats</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">System State</div>
                <div class="stat-value" style="color: #00ffcc;">NOMINAL</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Star Date</div>
                <div class="stat-value" style="font-size: 0.95rem;">{stardate:.2f}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Julian Day</div>
                <div class="stat-value" style="font-size: 0.95rem;">{julian_date:.3f}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Instructions on How to Use
st.markdown("""
<div style="font-size: 0.8rem; color: #506a64; text-align: center; margin-top: 1rem; border-top: 1px dashed rgba(0, 255, 204, 0.1); padding-top: 1rem;">
    <span>[ DOUBLE-CLICK Hours to toggle 12H/24H mode ]  &bull;  [ CLICK Seconds digits to toggle seconds display ]</span><br>
    <span>Built in Streamlit &bull; Designed by Antigravity v2.0</span>
</div>
""", unsafe_allow_html=True)

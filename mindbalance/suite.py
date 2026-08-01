"""Interactive pulse & breathing measurement suite (embedded HTML)."""
import streamlit.components.v1 as components

MEASUREMENT_SUITE_HTML = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
            background: linear-gradient(135deg, rgba(10, 20, 35, 0.7) 0%, rgba(15, 30, 45, 0.5) 100%);
            color: #F8FAFC;
            padding: 22px;
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(16px);
            box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        }
        
        .suite-title {
            font-size: 13px; font-weight: 800;
            color: #6EE7B7; margin-bottom: 14px;
            text-transform: uppercase; letter-spacing: 0.08em;
            display: flex; align-items: center; gap: 8px;
        }
        .suite-title::before {
            content: '';
            width: 8px; height: 8px;
            border-radius: 50%;
            background: #6EE7B7;
            box-shadow: 0 0 10px rgba(110, 231, 183, 0.6);
        }
        
        /* Side-by-side grid keeps both tools fully visible at once */
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 16px;
            align-items: start;
        }

        .tool-card { display: block; animation: fadeIn 0.4s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
        
        .tutor-box {
            background: rgba(52, 211, 153, 0.06);
            border-left: 3px solid #34D399;
            padding: 14px 18px; border-radius: 12px;
            font-size: 13px; line-height: 1.6;
            color: #CBD5E1; margin-bottom: 18px;
        }
        .tutor-box strong { color: #6EE7B7; }
        
        .counter-display {
            display: flex; align-items: center;
            justify-content: space-between;
            background: rgba(0,0,0,0.35);
            padding: 18px 24px; border-radius: 14px;
            border: 1px solid rgba(255,255,255,0.08);
            margin-bottom: 16px;
        }
        .counter-val {
            font-size: 36px; font-weight: 800;
            background: linear-gradient(135deg, #6EE7B7, #60A5FA);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            letter-spacing: -0.02em;
        }
        .counter-sub { font-size: 12px; color: #94A3B8; margin-top: 2px; }
        .tap-count {
            font-size: 20px; font-weight: 700;
            color: #F8FAFC;
            display: flex; align-items: center; gap: 8px;
        }
        
        .pulse-indicator {
            width: 12px; height: 12px;
            border-radius: 50%;
            background: #34D399;
            box-shadow: 0 0 12px rgba(52, 211, 153, 0.6);
            transition: transform 0.15s ease-out;
        }
        .pulse-indicator.pulse {
            transform: scale(1.8);
            box-shadow: 0 0 20px rgba(52, 211, 153, 0.9);
        }
        
        .action-btn {
            background: linear-gradient(135deg, #059669 0%, #10B981 100%);
            color: #FFFFFF; border: none;
            padding: 14px 24px; border-radius: 12px;
            font-size: 14px; font-weight: 700;
            cursor: pointer; width: 100%;
            margin-bottom: 8px;
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            font-family: inherit;
            position: relative; overflow: hidden;
        }
        .action-btn::before {
            content: '';
            position: absolute; top: 50%; left: 50%;
            width: 0; height: 0; border-radius: 50%;
            background: rgba(255,255,255,0.3);
            transform: translate(-50%, -50%);
            transition: width 0.5s, height 0.5s;
        }
        .action-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 28px rgba(16, 185, 129, 0.45);
        }
        .action-btn:active { transform: scale(0.98); }
        .action-btn:active::before { width: 300px; height: 300px; }
        
        .action-btn-secondary {
            background: rgba(255,255,255,0.04);
            color: #CBD5E1; border: 1px solid rgba(255,255,255,0.1);
            padding: 10px 18px; border-radius: 10px;
            font-size: 13px; font-weight: 600;
            cursor: pointer; width: 100%;
            transition: all 0.25s ease;
            font-family: inherit;
        }
        .action-btn-secondary:hover {
            background: rgba(255,255,255,0.08);
            color: #F8FAFC;
        }
        
        /* ─── Smooth Breathing Ring with CSS Keyframes ─── */
        .breath-visualizer {
            width: 140px; height: 140px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(52, 211, 153, 0.25) 0%, rgba(16, 185, 129, 0.02) 75%);
            border: 3px solid rgba(52, 211, 153, 0.5);
            box-shadow: 0 0 40px rgba(52, 211, 153, 0.25), inset 0 0 30px rgba(52, 211, 153, 0.1);
            margin: 20px auto;
            display: flex; align-items: center;
            justify-content: center;
            font-size: 14px; font-weight: 700;
            color: #F8FAFC; text-align: center;
            flex-direction: column; gap: 4px;
            transition: border-color 0.5s ease, box-shadow 0.5s ease;
            position: relative;
        }
        .breath-visualizer .breath-phase {
            font-size: 14px; font-weight: 700;
            color: #6EE7B7;
        }
        .breath-visualizer .breath-timer {
            font-size: 12px; color: #94A3B8;
        }
        
        /* Smooth 19-second breathing cycle animation (4-7-8) */
        @keyframes breathCycle {
            0% {
                transform: scale(0.85);
                border-color: rgba(96, 165, 250, 0.5);
                box-shadow: 0 0 40px rgba(96, 165, 250, 0.25), inset 0 0 30px rgba(96, 165, 250, 0.1);
            }
            21.05% {
                transform: scale(1.4);
                border-color: rgba(52, 211, 153, 0.7);
                box-shadow: 0 0 50px rgba(52, 211, 153, 0.4), inset 0 0 40px rgba(52, 211, 153, 0.2);
            }
            57.89% {
                transform: scale(1.4);
                border-color: rgba(251, 191, 36, 0.6);
                box-shadow: 0 0 50px rgba(251, 191, 36, 0.3), inset 0 0 40px rgba(251, 191, 36, 0.15);
            }
            100% {
                transform: scale(0.85);
                border-color: rgba(96, 165, 250, 0.5);
                box-shadow: 0 0 40px rgba(96, 165, 250, 0.25), inset 0 0 30px rgba(96, 165, 250, 0.1);
            }
        }
        .breath-visualizer.animating {
            animation: breathCycle 19s linear infinite;
        }
        
        /* Ripple effect for tap buttons */
        @keyframes ripple {
            to { transform: scale(2); opacity: 0; }
        }
        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255,255,255,0.4);
            width: 20px; height: 20px;
            pointer-events: none;
            animation: ripple 0.6s ease-out;
        }
</style>
    </head>
    <body>
        <div class="suite-title">Physiological Measurement Suite</div>
        
        <div class="tools-grid">
        
        <!-- Pulse Tool -->
        <div id="pulse-tool" class="tool-card active">
            <div class="tutor-box">
                <strong>How to measure your pulse:</strong><br>
                1. Gently place two fingers over your wrist or neck.<br>
                2. Tap <em>"Tap Pulse"</em> on every heartbeat for 5-10 beats to measure your resting BPM.
            </div>
            
            <div class="counter-display">
                <div>
                    <div id="hr-val" class="counter-val">--</div>
                    <div class="counter-sub">Measured Heart Rate (BPM)</div>
                </div>
                <div style="text-align: right;">
                    <div class="tap-count"><span id="p-dot" class="pulse-indicator"></span><span id="hr-taps">0</span></div>
                    <div class="counter-sub">Beats Recorded</div>
                </div>
            </div>
            
            <button class="action-btn" onclick="registerHeartTap(event)">Tap Pulse (Heartbeat)</button>
            <button class="action-btn-secondary" onclick="resetHeartTap()">Reset Pulse Counter</button>
        </div>
        
        <!-- Breath Tool -->
        <div id="breath-tool" class="tool-card">
            <div class="tutor-box">
                <strong>Guided 4-7-8 Breathing Tutor:</strong><br>
                Follow the visual ring rhythm (Inhale 4s → Hold 7s → Exhale 8s), or measure your rate: press <em>"Start 60s Counter"</em> and tap once per full breath cycle (one inhale + one exhale). After 60 seconds, Breaths/Minute = breaths counted.
            </div>
            
            <div id="breath-ring" class="breath-visualizer">
                <div class="breath-phase" id="ring-phase-text">Ready</div>
                <div class="breath-timer" id="ring-timer-text">Press start</div>
            </div>
            
            <div class="counter-display">
                <div>
                    <div id="br-val" class="counter-val">--</div>
                    <div class="counter-sub">Breaths / Minute</div>
                </div>
                <div style="text-align: right;">
                    <div id="breath-countdown" style="font-size: 24px; font-weight: 800; color: #FBBF24; line-height: 1.1;">--</div>
                    <div class="counter-sub">Seconds Remaining</div>
                    <div class="tap-count" style="margin-top: 6px;"><span id="b-dot" class="pulse-indicator"></span><span id="br-taps">0</span></div>
                    <div class="counter-sub">Breaths Counted</div>
                </div>
            </div>
            
            <button class="action-btn" onclick="toggleBreathingTutor()" id="tutor-toggle-btn">Start Guided Tutor</button>
            <button class="action-btn-secondary" onclick="startBreathCounter()" id="breath-counter-btn" style="margin-top: 6px;">Start 60s Counter</button>
            <button class="action-btn-secondary" onclick="registerBreathTap()" style="margin-top: 6px;">Tap Breath Cycle</button>
            <button class="action-btn-secondary" onclick="resetBreathTap()" style="margin-top: 6px;">Reset Breath Taps</button>
        </div>
        </div>
        
        <script>
            /* Ripple effect */
            function createRipple(e) {
                const btn = e.currentTarget;
                const rect = btn.getBoundingClientRect();
                const ripple = document.createElement('span');
                ripple.className = 'ripple';
                ripple.style.left = (e.clientX - rect.left - 10) + 'px';
                ripple.style.top = (e.clientY - rect.top - 10) + 'px';
                btn.appendChild(ripple);
                setTimeout(() => ripple.remove(), 600);
            }
            
            /* ─── Pulse Measurement Logic ─── */
            let heartTaps = [];
            function registerHeartTap(e) {
                createRipple(e);
                const now = performance.now();
                heartTaps.push(now);
                document.getElementById('hr-taps').innerText = heartTaps.length;
                
                const dot = document.getElementById('p-dot');
                dot.classList.add('pulse');
                setTimeout(() => dot.classList.remove('pulse'), 150);
                
                if (heartTaps.length >= 2) {
                    let intervals = [];
                    for (let i = 1; i < heartTaps.length; i++) {
                        intervals.push(heartTaps[i] - heartTaps[i-1]);
                    }
                    const avgInterval = intervals.reduce((a, b) => a + b, 0) / intervals.length;
                    const bpm = Math.round(60000 / avgInterval);
                    if (bpm >= 40 && bpm <= 190) {
                        document.getElementById('hr-val').innerText = bpm;
                    }
                }
            }
            
            function resetHeartTap() {
                heartTaps = [];
                document.getElementById('hr-taps').innerText = '0';
                document.getElementById('hr-val').innerText = '--';
            }
            
            /* ─── Breathing Tutor Logic ─── */
            let tutorTimer = null;
            let tutorRunning = false;
            let breathTaps = [];
            let breathTimer = null;
            let breathCounting = false;
            let breathCountdown = 60;
            
            function updateTutorUI(second) {
                const ringPhaseEl = document.getElementById('ring-phase-text');
                const ringTimerEl = document.getElementById('ring-timer-text');
                
                if (second <= 4) {
                    ringPhaseEl.innerText = 'Inhale';
                    ringTimerEl.innerText = (4 - second + 1) + 's';
                } else if (second <= 11) {
                    ringPhaseEl.innerText = 'Hold';
                    ringTimerEl.innerText = (11 - second + 1) + 's';
                } else {
                    ringPhaseEl.innerText = 'Exhale';
                    ringTimerEl.innerText = (19 - second + 1) + 's';
                }
            }
            
            function toggleBreathingTutor() {
                const btn = document.getElementById('tutor-toggle-btn');
                const ring = document.getElementById('breath-ring');
                
                if (tutorRunning) {
                    // Stop Logic
                    clearInterval(tutorTimer);
                    tutorRunning = false;
                    btn.innerText = 'Start Guided Tutor';
                    
                    document.getElementById('ring-phase-text').innerText = 'Ready';
                    document.getElementById('ring-timer-text').innerText = 'Press start';
                    
                    ring.classList.remove('animating');
                    return;
                }
                
                // Start Logic
                tutorRunning = true;
                btn.innerText = 'Pause Guided Tutor';
                ring.classList.add('animating');
                
                let second = 1;
                updateTutorUI(second); // Immediate update for the first second
                
                tutorTimer = setInterval(() => {
                    second = (second % 19) + 1;
                    updateTutorUI(second);
                }, 1000);
            }
            
            function updateBreathCountdown() {
                document.getElementById('breath-countdown').innerText =
                    breathCountdown <= 0 ? 'Done' : breathCountdown + 's';
            }
            
            function startBreathCounter() {
                if (breathCounting) return;
                breathCounting = true;
                breathTaps = [];
                breathCountdown = 60;
                document.getElementById('br-taps').innerText = '0';
                document.getElementById('br-val').innerText = '--';
                document.getElementById('breath-counter-btn').innerText = 'Counting...';
                updateBreathCountdown();
                breathTimer = setInterval(() => {
                    breathCountdown -= 1;
                    updateBreathCountdown();
                    if (breathCountdown <= 0) {
                        clearInterval(breathTimer);
                        breathTimer = null;
                        breathCounting = false;
                        document.getElementById('breath-counter-btn').innerText = 'Start 60s Counter';
                        document.getElementById('br-val').innerText = breathTaps.length;
                    }
                }, 1000);
            }
            
            function registerBreathTap() {
                if (!breathCounting) startBreathCounter();
                if (!breathCounting) return;
                
                breathTaps.push(performance.now());
                document.getElementById('br-taps').innerText = breathTaps.length;
                
                const dot = document.getElementById('b-dot');
                dot.classList.add('pulse');
                setTimeout(() => dot.classList.remove('pulse'), 150);
            }
            
            function resetBreathTap() {
                if (breathTimer) { clearInterval(breathTimer); breathTimer = null; }
                breathCounting = false;
                breathTaps = [];
                breathCountdown = 60;
                document.getElementById('br-taps').innerText = '0';
                document.getElementById('br-val').innerText = '--';
                document.getElementById('breath-countdown').innerText = '--';
                document.getElementById('breath-counter-btn').innerText = 'Start 60s Counter';
            }
        </script>
    </body>
    </html>
    """


def render_interactive_measurement_suite():
    """Fixed interactive measurement suite for accurate breathing tutor functionality"""
    components.html(MEASUREMENT_SUITE_HTML, height=720, scrolling=True)

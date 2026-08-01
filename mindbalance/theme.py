"""Global styling (CSS) and the ambient particle background."""
import streamlit as st
import streamlit.components.v1 as components

THEME_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ─── Global Reset & Dark Theme ─── */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background: #050A12 !important;
        color: #E2E8F0 !important;
        font-family: 'Plus Jakarta Sans', 'Inter', system-ui, sans-serif !important;
        overflow-x: hidden;
    }

    [data-testid="stHeader"] { background: transparent !important; }

    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 4rem;
        max-width: 1180px;
        position: relative;
        z-index: 2; /* Ensure content sits above the particle canvas */
    }

    #MainMenu, footer { visibility: hidden; }

    /* ─── Glassmorphic Sidebar ─── */
    [data-testid="stSidebar"] {
        background: rgba(8, 14, 24, 0.85) !important;
        backdrop-filter: blur(24px) saturate(180%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }
    [data-testid="stSidebar"] * { color: #CBD5E1 !important; }
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #6EE7B7 !important;
        font-weight: 700 !important;
    }

    /* ─── Ambient Animated Gradient Orbs ─── */
    .stApp::before {
        content: '';
        position: fixed;
        top: -20%; left: -10%;
        width: 700px; height: 700px;
        background: radial-gradient(circle, rgba(52, 211, 153, 0.18) 0%, transparent 70%);
        border-radius: 50%;
        filter: blur(100px);
        z-index: 0;
        pointer-events: none;
        animation: driftOrb1 25s ease-in-out infinite;
    }
    .stApp::after {
        content: '';
        position: fixed;
        bottom: -20%; right: -10%;
        width: 800px; height: 800px;
        background: radial-gradient(circle, rgba(96, 165, 250, 0.12) 0%, transparent 70%);
        border-radius: 50%;
        filter: blur(120px);
        z-index: 0;
        pointer-events: none;
        animation: driftOrb2 30s ease-in-out infinite;
    }

    @keyframes driftOrb1 {
        0%, 100% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(100px, 80px) scale(1.15); }
    }
    @keyframes driftOrb2 {
        0%, 100% { transform: translate(0, 0) scale(1); }
        50% { transform: translate(-80px, -100px) scale(1.2); }
    }

    /* ─── Hero Banner ─── */
    .hero-banner {
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.12) 0%, rgba(96, 165, 250, 0.04) 100%);
        border-radius: 24px;
        padding: 36px 40px;
        margin-bottom: 32px;
        border: 1px solid rgba(52, 211, 153, 0.2);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255,255,255,0.05);
        backdrop-filter: blur(20px);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent);
        animation: shimmer 8s infinite;
    }
    @keyframes shimmer {
        0% { left: -100%; }
        50%, 100% { left: 100%; }
    }
    .hero-title {
        font-size: 32px;
        font-weight: 800;
        background: linear-gradient(135deg, #6EE7B7 0%, #60A5FA 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        font-size: 15px;
        color: #94A3B8;
        margin: 0;
        line-height: 1.7;
        font-weight: 400;
    }

    /* ─── Glassmorphic Form ─── */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.025) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 24px !important;
        padding: 32px !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3) !important;
    }

    /* ─── Form Tabs ─── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(0, 0, 0, 0.4);
        padding: 6px;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: 600;
        color: #94A3B8 !important;
        background-color: transparent;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.2), rgba(96, 165, 250, 0.1)) !important;
        color: #6EE7B7 !important;
        border: 1px solid rgba(52, 211, 153, 0.3) !important;
        box-shadow: 0 4px 16px rgba(52, 211, 153, 0.15) !important;
    }

    /* ─── Input Fields ─── */
    label, [data-testid="stWidgetLabel"] p {
        color: #E2E8F0 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="input"], div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.04) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: #F8FAFC !important;
        transition: all 0.3s ease !important;
    }
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within {
        border-color: rgba(52, 211, 153, 0.5) !important;
        box-shadow: 0 0 0 3px rgba(52, 211, 153, 0.1) !important;
    }
    div[data-baseweb="input"] input { color: #F8FAFC !important; background: transparent !important; }

    /* ─── Calming Emerald Sliders ─── */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #34D399 !important;
        border-color: #34D399 !important;
        box-shadow: 0 0 16px rgba(52, 211, 153, 0.6) !important;
    }
    div[data-baseweb="slider"] [data-testid="stSliderTickBar"] + div > div {
        background-color: #059669 !important;
    }

    /* ─── Result Badges ─── */
    .result-badge {
        border-radius: 20px;
        padding: 32px;
        margin-bottom: 28px;
        backdrop-filter: blur(20px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s ease-out;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .result-badge::after {
        content: '';
        position: absolute;
        top: 0; right: 0;
        width: 200px; height: 200px;
        background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, transparent 70%);
        border-radius: 50%;
        transform: translate(50%, -50%);
    }
    .badge-low { background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(52, 211, 153, 0.3); }
    .badge-medium { background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(251, 191, 36, 0.3); }
    .badge-high { background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(248, 113, 113, 0.3); }

    .badge-label {
        font-size: 11px; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.1em;
        margin-bottom: 8px; position: relative;
    }
    .badge-low .badge-label { color: #6EE7B7; }
    .badge-medium .badge-label { color: #FDE68A; }
    .badge-high .badge-label { color: #FCA5A5; }

    .badge-title {
        font-size: 28px; font-weight: 800;
        margin-bottom: 10px; position: relative;
        letter-spacing: -0.02em;
    }
    .badge-low .badge-title { color: #A7F3D0; }
    .badge-medium .badge-title { color: #FEF3C7; }
    .badge-high .badge-title { color: #FEE2E2; }

    .badge-desc {
        font-size: 15px; line-height: 1.7;
        color: #CBD5E1; margin: 0; position: relative;
    }

    /* ─── Metric Cards ─── */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 18px;
        padding: 22px;
        backdrop-filter: blur(16px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    }
    .metric-header {
        display: flex; justify-content: space-between;
        align-items: center; margin-bottom: 12px;
    }
    .metric-label {
        font-size: 11.5px; font-weight: 700;
        color: #94A3B8; text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 24px; font-weight: 800;
        color: #F8FAFC; letter-spacing: -0.02em;
    }
    .metric-bar {
        height: 8px; background: rgba(255, 255, 255, 0.06);
        border-radius: 10px; overflow: hidden; margin-bottom: 10px;
        position: relative;
    }
    .metric-bar-fill {
        height: 100%; border-radius: 10px;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    .metric-bar-fill::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: shimmerBar 2s infinite;
    }
    @keyframes shimmerBar {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    .bar-low { background: linear-gradient(90deg, #10B981, #34D399); }
    .bar-medium { background: linear-gradient(90deg, #F59E0B, #FBBF24); }
    .bar-high { background: linear-gradient(90deg, #EF4444, #F87171); }

    /* ─── Recommendations ─── */
    .rec-section {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 28px;
        margin-top: 28px;
        backdrop-filter: blur(16px);
    }
    .rec-title {
        font-size: 18px; font-weight: 700;
        color: #F8FAFC; margin-bottom: 20px;
        display: flex; align-items: center; gap: 10px;
    }
    .rec-title::before {
        content: '';
        width: 10px; height: 10px;
        border-radius: 50%;
        background: linear-gradient(135deg, #34D399, #60A5FA);
        flex-shrink: 0;
        box-shadow: 0 0 12px rgba(52, 211, 153, 0.5);
    }
    .rec-list { list-style-type: none; padding: 0; margin: 0; }
    .rec-list li {
        padding: 16px 20px;
        margin-bottom: 12px;
        background: rgba(255, 255, 255, 0.025);
        border-radius: 14px;
        font-size: 14.5px;
        color: #E2E8F0;
        line-height: 1.6;
        border-left: 4px solid #34D399;
        display: flex; align-items: flex-start; gap: 14px;
        transition: all 0.3s ease;
        animation: slideIn 0.5s ease-out backwards;
    }
    .rec-list li:nth-child(1) { animation-delay: 0.1s; }
    .rec-list li:nth-child(2) { animation-delay: 0.2s; }
    .rec-list li:nth-child(3) { animation-delay: 0.3s; }
    .rec-list li:nth-child(4) { animation-delay: 0.4s; }
    .rec-list li:nth-child(5) { animation-delay: 0.5s; }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes mbPageFade {
        from { opacity: 0; transform: translateY(14px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .rec-list li:hover {
        background: rgba(255, 255, 255, 0.04);
        transform: translateX(4px);
    }
    .rec-list li::before {
        content: '';
        width: 8px; height: 8px;
        border-radius: 50%;
        background: #34D399;
        flex-shrink: 0; margin-top: 7px;
    }
    .rec-medium li { border-left-color: #FBBF24; }
    .rec-medium li::before { color: #FBBF24; }
    .rec-high li { border-left-color: #F87171; }
    .rec-high li::before { color: #F87171; }

    /* ─── Action Button ─── */
    .stButton > button {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 14px 32px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.35) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
        overflow: hidden;
    }
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%; left: 50%;
        width: 0; height: 0;
        border-radius: 50%;
        background: rgba(255,255,255,0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(16, 185, 129, 0.5) !important;
    }
    .stButton > button:hover::before {
        width: 300px; height: 300px;
    }

    /* ─── Sidebar Affirmation ─── */
    .sidebar-affirmation {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 18px;
        margin-top: 14px;
        position: relative;
        overflow: hidden;
    }
    .sidebar-affirmation::before {
        content: '"';
        position: absolute;
        top: -10px; left: 10px;
        font-size: 80px;
        color: rgba(110, 231, 183, 0.1);
        font-family: Georgia, serif;
    }
    .sidebar-affirmation-title {
        font-size: 10px; font-weight: 700;
        color: #6EE7B7; text-transform: uppercase;
        letter-spacing: 0.1em; margin-bottom: 8px;
    }
    .sidebar-affirmation-text {
        font-size: 13px; color: #CBD5E1;
        line-height: 1.6; margin: 0; font-style: italic;
    }

    /* ─── Insight Sections (EDA) ─── */
    .bq-head {
        display: flex; align-items: center; gap: 16px;
        margin: 36px 0 8px;
    }
    .bq-num {
        width: 48px; height: 48px; border-radius: 14px; flex-shrink: 0;
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; font-size: 13px; color: #FFFFFF;
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.25);
    }
    .bq-title { font-size: 21px; font-weight: 800; color: #F8FAFC; letter-spacing: -0.01em; }
    .bq-sub { font-size: 13.5px; color: #94A3B8; margin-top: 3px; }

    .insight-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-left: 4px solid #818CF8;
        border-radius: 18px;
        padding: 24px 28px;
        margin: 20px 0 10px;
        backdrop-filter: blur(16px);
    }
    .insight-q {
        font-size: 17px; font-weight: 800; color: #F8FAFC;
        line-height: 1.5; margin-bottom: 16px; padding-bottom: 14px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }
    .bq-ref {
        display: inline-block; font-size: 11.5px; font-weight: 800;
        letter-spacing: 0.08em; color: #C7D2FE;
        background: rgba(99, 102, 241, 0.2);
        border: 1px solid rgba(129, 140, 248, 0.35);
        border-radius: 999px; padding: 3px 12px;
        margin-right: 10px; vertical-align: 2px;
    }
    .insight-line {
        display: flex; align-items: flex-start; gap: 14px;
        margin: 12px 0;
    }
    .insight-tag {
        flex-shrink: 0; min-width: 172px;
        font-size: 11.5px; font-weight: 800;
        letter-spacing: 0.05em;
        padding: 6px 12px; border-radius: 999px;
        text-align: center; white-space: nowrap;
        margin-top: 1px;
    }
    .tag-what { background: rgba(99, 102, 241, 0.18); color: #A5B4FC; }
    .tag-why { background: rgba(16, 185, 129, 0.16); color: #6EE7B7; }
    .tag-action { background: rgba(245, 158, 11, 0.16); color: #FCD34D; }
    .insight-text {
        font-size: 15px; color: #E2E8F0; line-height: 1.75;
        flex: 1;
    }

    .stats-table {
        width: 100%; border-collapse: separate; border-spacing: 0;
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 16px; overflow: hidden; margin: 10px 0 6px;
        backdrop-filter: blur(16px);
    }
    .stats-table th {
        background: rgba(255, 255, 255, 0.06);
        color: #A5B4FC; font-size: 12px; font-weight: 800;
        letter-spacing: 0.06em; text-transform: uppercase;
        padding: 14px 18px; text-align: left;
    }
    .stats-table td {
        padding: 14px 18px; font-size: 15px; color: #CBD5E1;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        white-space: nowrap;
    }
    .stats-table tr td:first-child { color: #F1F5F9; font-weight: 600; }
    .stats-table .cat-low { color: #6EE7B7; font-weight: 700; }
    .stats-table .cat-medium { color: #FCD34D; font-weight: 700; }
    .stats-table .cat-high { color: #FCA5A5; font-weight: 700; }

</style>
"""

# Injected into the parent window: executed inside an iframe but draws the
# canvas directly into the parent Streamlit DOM so it is not constrained by
# the iframe's bounds.
PARTICLE_BG_HTML = """
<script>
    try {
        const parentDoc = window.parent.document;
        const parentWin = window.parent;
        
        // Remove existing canvas if app reruns to prevent duplicates
        let oldCanvas = parentDoc.getElementById('mindbalance-particle-canvas');
        if (oldCanvas) {
            oldCanvas.remove();
        }

        const canvas = parentDoc.createElement('canvas');
        canvas.id = 'mindbalance-particle-canvas';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.zIndex = '0'; // Sits behind the main application content (z-index: 2)
        canvas.style.pointerEvents = 'none';
        parentDoc.body.appendChild(canvas);

        const ctx = canvas.getContext('2d');
        let particles = [];
        let mouseX = 0, mouseY = 0;

        function resize() {
            canvas.width = parentWin.innerWidth;
            canvas.height = parentWin.innerHeight;
        }
        resize();
        parentWin.addEventListener('resize', resize);
        parentWin.addEventListener('mousemove', e => { 
            mouseX = e.clientX; 
            mouseY = e.clientY; 
        });

        class Particle {
            constructor() { this.reset(); }
            reset() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2.5 + 0.8;
                this.speedX = (Math.random() - 0.5) * 0.3;
                this.speedY = (Math.random() - 0.5) * 0.3;
                this.opacity = Math.random() * 0.4 + 0.15;
                this.color = Math.random() > 0.5 ? '52, 211, 153' : '96, 165, 250';
                this.pulseSpeed = Math.random() * 0.01 + 0.005;
                this.pulsePhase = Math.random() * Math.PI * 2;
            }
            update() {
                this.x += this.speedX;
                this.y += this.speedY;
                this.pulsePhase += this.pulseSpeed;
                
                const dx = mouseX - this.x;
                const dy = mouseY - this.y;
                const dist = Math.sqrt(dx*dx + dy*dy);
                if (dist < 150) {
                    this.x -= dx * 0.002;
                    this.y -= dy * 0.002;
                }
                
                if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
                if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
            }
            draw() {
                const pulseOpacity = this.opacity + Math.sin(this.pulsePhase) * 0.15;
                const gradient = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.size * 4);
                gradient.addColorStop(0, `rgba(${this.color}, ${pulseOpacity})`);
                gradient.addColorStop(1, `rgba(${this.color}, 0)`);
                ctx.fillStyle = gradient;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size * 4, 0, Math.PI * 2);
                ctx.fill();
                
                ctx.fillStyle = `rgba(${this.color}, ${pulseOpacity * 1.5})`;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        // Increased particle count for better visual density on full screen
        for (let i = 0; i < 110; i++) particles.push(new Particle());

        function drawConnections() {
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx*dx + dy*dy);
                    if (dist < 140) {
                        const opacity = (1 - dist/140) * 0.12;
                        ctx.strokeStyle = `rgba(110, 231, 183, ${opacity})`;
                        ctx.lineWidth = 0.5;
                        ctx.beginPath();
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawConnections();
            particles.forEach(p => { p.update(); p.draw(); });
            requestAnimationFrame(animate);
        }
        animate();
    } catch (e) {
        console.error("Particle JS error:", e);
    }
</script>
"""


def inject_theme():
    """Apply the global dark-theme stylesheet."""
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def inject_particles():
    """Start the ambient particle field behind the app content."""
    components.html(PARTICLE_BG_HTML, height=0, width=0, scrolling=False)

# Additional dashboard-specific components for the GitHub-ready edition.
EXTRA_THEME_CSS = r"""
<style>
@import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css');

:root {
  --mb-bg: #050A12;
  --mb-panel: rgba(15, 23, 42, 0.72);
  --mb-panel-soft: rgba(255,255,255,0.035);
  --mb-border: rgba(148,163,184,0.14);
  --mb-text: #E5EEF8;
  --mb-muted: #94A3B8;
  --mb-teal: #2DD4BF;
  --mb-blue: #60A5FA;
  --mb-amber: #FBBF24;
  --mb-rose: #FB7185;
}

/* More robust defaults across Streamlit versions */
[data-testid="stAppViewContainer"] > .main { background: transparent; }
[data-testid="stMainBlockContainer"], .block-container { max-width: 1240px; padding-top: 2.1rem; }
[data-testid="stToolbar"], [data-testid="stDecoration"] { visibility: hidden; height: 0; }
button, input, textarea, [data-baseweb="select"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }

.mb-brand { display:flex; align-items:center; gap:12px; padding:4px 2px 18px; }
.mb-brand-mark { width:42px; height:42px; border-radius:14px; display:grid; place-items:center; font-weight:900; font-size:20px; color:#042f2e; background:linear-gradient(135deg,#99F6E4,#60A5FA); box-shadow:0 10px 25px rgba(45,212,191,.2); }
.mb-brand-name { color:#F8FAFC; font-size:20px; line-height:1.1; font-weight:800; letter-spacing:-.03em; }
.mb-brand-sub { color:#64748B; font-size:11px; margin-top:4px; }
.mb-sidebar-divider { height:1px; background:rgba(148,163,184,.12); margin:20px 0; }
.mb-status-card,.mb-privacy-card { border:1px solid var(--mb-border); background:rgba(255,255,255,.025); border-radius:14px; padding:14px; margin-bottom:12px; font-size:12px; color:#94A3B8; line-height:1.5; }
.mb-status-line { display:flex; align-items:center; gap:8px; color:#E2E8F0; margin-bottom:5px; }
.mb-status-detail { white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.mb-dot { width:8px; height:8px; border-radius:50%; display:inline-block; box-shadow:0 0 12px currentColor; }
.mb-dot.ok { background:#2DD4BF; color:#2DD4BF; }
.mb-dot.warn { background:#FBBF24; color:#FBBF24; }
.mb-small-kicker,.mb-kicker { text-transform:uppercase; letter-spacing:.13em; color:#5EEAD4; font-weight:800; font-size:10px; }
.mb-sidebar-footer { color:#475569; font-size:10px; text-align:center; padding:12px 0 2px; }

.mb-page-hero { position:relative; display:flex; gap:20px; align-items:flex-start; padding:30px 32px; border:1px solid rgba(45,212,191,.18); border-radius:24px; margin-bottom:22px; overflow:hidden; background:linear-gradient(135deg,rgba(45,212,191,.10),rgba(96,165,250,.045) 60%,rgba(15,23,42,.34)); box-shadow:0 24px 80px rgba(0,0,0,.25); }
.mb-page-hero:after { content:""; position:absolute; width:220px; height:220px; right:-80px; top:-110px; background:radial-gradient(circle,rgba(96,165,250,.2),transparent 70%); }
.mb-page-icon { flex:0 0 auto; width:52px; height:52px; border-radius:17px; display:grid; place-items:center; font-size:23px; color:#99F6E4; border:1px solid rgba(45,212,191,.2); background:rgba(45,212,191,.08); }
.mb-page-hero h1 { color:#F8FAFC; font-size:clamp(28px,4vw,43px); line-height:1.08; letter-spacing:-.04em; margin:7px 0 9px; }
.mb-page-hero p { color:#A8B6CA; max-width:800px; font-size:15px; line-height:1.75; margin:0; }

.mb-notice { display:flex; gap:12px; align-items:flex-start; padding:15px 17px; border-radius:14px; border:1px solid var(--mb-border); margin:12px 0 20px; font-size:13px; line-height:1.6; }
.mb-notice i { margin-top:2px; font-size:16px; }
.mb-notice strong { display:block; margin-bottom:2px; color:#F8FAFC; }
.mb-notice.info { background:rgba(96,165,250,.07); border-color:rgba(96,165,250,.20); color:#BFDBFE; }
.mb-notice.warning { background:rgba(251,191,36,.07); border-color:rgba(251,191,36,.22); color:#FDE68A; }
.mb-notice.success { background:rgba(45,212,191,.07); border-color:rgba(45,212,191,.22); color:#99F6E4; }
.mb-notice.danger { background:rgba(251,113,133,.07); border-color:rgba(251,113,133,.24); color:#FECDD3; }

.mb-metric-card { min-height:144px; padding:18px; border-radius:18px; border:1px solid var(--mb-border); background:linear-gradient(145deg,rgba(255,255,255,.045),rgba(255,255,255,.018)); box-shadow:0 12px 35px rgba(0,0,0,.16); position:relative; overflow:hidden; }
.mb-metric-card:after { content:""; position:absolute; width:80px; height:80px; right:-25px; top:-25px; border-radius:50%; background:currentColor; opacity:.055; }
.mb-metric-card.teal { color:var(--mb-teal); }.mb-metric-card.blue { color:var(--mb-blue); }.mb-metric-card.amber { color:var(--mb-amber); }.mb-metric-card.rose { color:var(--mb-rose); }
.mb-metric-icon { font-size:17px; margin-bottom:12px; }
.mb-metric-label { color:#94A3B8; text-transform:uppercase; letter-spacing:.08em; font-size:9px; font-weight:800; }
.mb-metric-value { color:#F8FAFC; font-weight:850; font-size:25px; letter-spacing:-.035em; margin:4px 0; }
.mb-metric-detail { color:#73839A; font-size:11px; line-height:1.4; }

.mb-section-head { display:flex; gap:13px; align-items:flex-start; margin:34px 0 15px; }
.mb-section-head h2 { color:#F8FAFC; font-size:21px; letter-spacing:-.025em; margin:0 0 3px; }
.mb-section-head p { color:#7F8EA3; font-size:12px; margin:0; }
.mb-section-number { flex:0 0 auto; min-width:38px; padding:7px 8px; border-radius:10px; border:1px solid rgba(45,212,191,.2); color:#5EEAD4; background:rgba(45,212,191,.06); text-align:center; font-size:10px; font-weight:800; letter-spacing:.05em; }

.mb-step-card,.mb-feature-card { height:100%; border:1px solid var(--mb-border); border-radius:17px; padding:17px; background:rgba(255,255,255,.025); transition:transform .2s ease,border-color .2s ease; }
.mb-step-card:hover,.mb-feature-card:hover { transform:translateY(-3px); border-color:rgba(45,212,191,.27); }
.mb-step-top { display:flex; justify-content:space-between; color:#5EEAD4; font-weight:800; font-size:11px; }
.mb-step-card h3,.mb-feature-card h3 { color:#F8FAFC; font-size:14px; margin:16px 0 7px; }
.mb-step-card p,.mb-feature-card p { color:#7F8EA3; font-size:11px; line-height:1.55; margin:0; }
.mb-feature-symbol { width:38px; height:38px; border-radius:12px; display:grid; place-items:center; color:#99F6E4; background:rgba(45,212,191,.07); border:1px solid rgba(45,212,191,.15); }

.mb-form-intro { display:flex; justify-content:space-between; align-items:center; gap:15px; color:#F8FAFC; padding-bottom:18px; }
.mb-form-intro span { color:#7F8EA3; font-size:12px; }
.mb-result-banner { --risk-color:#2DD4BF; display:grid; grid-template-columns:1fr auto auto; gap:22px; align-items:center; padding:25px; border-radius:20px; border:1px solid color-mix(in srgb,var(--risk-color) 35%,transparent); background:linear-gradient(135deg,color-mix(in srgb,var(--risk-color) 13%,transparent),rgba(255,255,255,.018)); box-shadow:0 18px 50px rgba(0,0,0,.2); }
.mb-result-banner h2 { color:#F8FAFC; font-size:27px; margin:5px 0 7px; letter-spacing:-.035em; }
.mb-result-banner p { color:#A9B6C9; font-size:13px; line-height:1.6; margin:0; max-width:660px; }
.mb-score-pill,.mb-confidence { min-width:112px; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:14px; border:1px solid var(--mb-border); border-radius:15px; background:rgba(0,0,0,.15); }
.mb-score-pill span,.mb-confidence span { color:#F8FAFC; font-size:25px; font-weight:850; }
.mb-score-pill small,.mb-confidence small { color:#7F8EA3; font-size:9px; text-align:center; }

.mb-list-grid { display:grid; grid-template-columns:1fr; gap:10px; }
.mb-list-card { display:flex; gap:12px; padding:14px; border-radius:14px; border:1px solid var(--mb-border); background:rgba(255,255,255,.025); }
.mb-list-icon { flex:0 0 auto; width:34px; height:34px; border-radius:10px; display:grid; place-items:center; color:#5EEAD4; background:rgba(45,212,191,.07); }
.mb-list-card strong { color:#EAF2FB; font-size:12px; }
.mb-list-card p { color:#7F8EA3; font-size:11px; line-height:1.5; margin:3px 0 0; }
.mb-ground-number { color:#5EEAD4; font-size:32px; font-weight:900; line-height:1; margin-bottom:8px; }
.mb-checkin-summary,.mb-about-card { padding:20px; border-radius:17px; border:1px solid rgba(45,212,191,.18); background:rgba(45,212,191,.045); margin-top:16px; color:#A8B6CA; }
.mb-checkin-summary strong { color:#F8FAFC; }
.mb-checkin-summary p { margin:6px 0; font-size:12px; }
.mb-member { display:flex; align-items:center; gap:10px; padding:13px 14px; border-bottom:1px solid rgba(148,163,184,.1); color:#CBD5E1; }
.mb-member i { color:#5EEAD4; }
.mb-deploy-step { display:flex; align-items:center; gap:13px; padding:12px 0; border-bottom:1px solid rgba(148,163,184,.1); }
.mb-deploy-step span { width:30px; height:30px; border-radius:10px; display:grid; place-items:center; color:#042F2E; background:#5EEAD4; font-weight:900; font-size:11px; }
.mb-deploy-step p { color:#CBD5E1; margin:0; font-size:12px; }
.mb-limit-item { display:flex; gap:8px; padding:10px 0; color:#A8B6CA; border-bottom:1px solid rgba(148,163,184,.08); font-size:12px; line-height:1.55; }
.mb-limit-item i { color:#FB7185; }
.mb-footer { display:flex; justify-content:space-between; gap:20px; color:#475569; border-top:1px solid rgba(148,163,184,.1); padding-top:18px; margin-top:45px; font-size:10px; }


/* Assessment result layout inspired by the submitted dashboard reference */
.mb-result-banner {
  --risk-color:#2DD4BF;
  display:flex;
  justify-content:space-between;
  gap:28px;
  align-items:center;
  padding:31px 34px;
  margin:8px 0 28px;
  border-radius:23px;
  border:1px solid color-mix(in srgb,var(--risk-color) 38%,transparent);
  background:
    radial-gradient(circle at 95% 10%,color-mix(in srgb,var(--risk-color) 12%,transparent),transparent 35%),
    linear-gradient(135deg,color-mix(in srgb,var(--risk-color) 12%,#130D14),rgba(20,15,24,.90));
  box-shadow:0 24px 70px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.025);
  overflow:hidden;
}
.mb-result-copy { min-width:0; }
.mb-result-kicker { color:color-mix(in srgb,var(--risk-color) 75%,white); text-transform:uppercase; letter-spacing:.14em; font-size:10px; font-weight:900; }
.mb-result-banner h2 { color:#FFF7F8; font-size:clamp(27px,3vw,38px); line-height:1.12; margin:13px 0 13px; letter-spacing:-.04em; }
.mb-result-banner p { color:#CCD5E1; font-size:14px; line-height:1.72; margin:0; max-width:790px; }
.mb-result-meta { flex:0 0 auto; display:grid; grid-template-columns:repeat(2,minmax(112px,1fr)); gap:10px; }
.mb-result-stat { min-width:118px; padding:14px 15px; border-radius:15px; border:1px solid rgba(255,255,255,.08); background:rgba(4,8,15,.30); text-align:center; }
.mb-result-stat span { display:block; color:#F8FAFC; font-size:23px; font-weight:900; letter-spacing:-.04em; }
.mb-result-stat small { display:block; color:#8491A4; font-size:9px; margin-top:3px; text-transform:uppercase; letter-spacing:.06em; }

.mb-result-subheading { margin:13px 0 10px; }
.mb-result-subheading h3 { color:#F8FAFC; font-size:22px; letter-spacing:-.03em; margin:0 0 4px; }
.mb-result-subheading p { color:#718096; font-size:11px; margin:0; }

.mb-index-stack { display:grid; gap:0; margin-top:20px; border-radius:20px; overflow:hidden; border:1px solid rgba(148,163,184,.13); background:rgba(11,18,29,.64); box-shadow:0 18px 55px rgba(0,0,0,.19); }
.mb-index-card { padding:24px 25px 23px; border-bottom:1px solid rgba(148,163,184,.12); background:linear-gradient(120deg,rgba(255,255,255,.018),rgba(255,255,255,.008)); }
.mb-index-card:last-child { border-bottom:0; }
.mb-index-head { display:flex; justify-content:space-between; align-items:center; gap:18px; margin-bottom:17px; }
.mb-index-head span { color:#91A1B8; text-transform:uppercase; letter-spacing:.09em; font-size:10px; font-weight:900; }
.mb-index-head strong { color:#F8FAFC; font-size:25px; line-height:1; font-weight:900; letter-spacing:-.04em; }
.mb-index-track { height:8px; border-radius:99px; background:rgba(148,163,184,.12); overflow:hidden; box-shadow:inset 0 1px 3px rgba(0,0,0,.35); }
.mb-index-fill { width:var(--index-value); height:100%; border-radius:inherit; background:linear-gradient(90deg,var(--index-color),color-mix(in srgb,var(--index-color) 66%,white)); box-shadow:0 0 18px color-mix(in srgb,var(--index-color) 40%,transparent); }
.mb-index-card p { color:#8492A7; font-size:11px; line-height:1.5; margin:13px 0 0; }

.mb-guidance-panel { margin:31px 0 12px; padding:25px 28px 28px; border:1px solid rgba(148,163,184,.14); border-radius:21px; background:linear-gradient(135deg,rgba(255,255,255,.025),rgba(15,23,42,.58)); box-shadow:0 20px 58px rgba(0,0,0,.18); }
.mb-guidance-heading { display:flex; align-items:center; gap:11px; margin-bottom:18px; }
.mb-guidance-heading > span { width:10px; height:10px; border-radius:50%; background:linear-gradient(135deg,#2DD4BF,#60A5FA); box-shadow:0 0 18px rgba(45,212,191,.55); }
.mb-guidance-heading h3 { color:#F8FAFC; font-size:17px; margin:0; letter-spacing:-.02em; }
.mb-guidance-list { display:grid; gap:11px; }
.mb-guidance-item { position:relative; display:flex; gap:13px; align-items:flex-start; padding:17px 19px 17px 23px; border-radius:14px; border-left:4px solid #FB7185; background:rgba(255,255,255,.023); }
.mb-guidance-item:after { content:""; position:absolute; inset:0; border-radius:inherit; border:1px solid rgba(148,163,184,.045); pointer-events:none; }
.mb-guidance-dot { flex:0 0 auto; width:8px; height:8px; margin-top:7px; border-radius:50%; background:#34D399; box-shadow:0 0 12px rgba(52,211,153,.35); }
.mb-guidance-item strong { color:#EEF4FA; font-size:12px; }
.mb-guidance-item p { color:#97A5B8; font-size:11px; line-height:1.52; margin:4px 0 0; }

/* Streamlit controls */
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] { background:linear-gradient(135deg,#14B8A6,#3B82F6) !important; border:0 !important; color:white !important; font-weight:800 !important; box-shadow:0 10px 28px rgba(20,184,166,.22) !important; }
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button { border-radius:12px !important; min-height:43px; }
[data-testid="stDataFrame"] { border:1px solid var(--mb-border); border-radius:15px; overflow:hidden; }
[data-testid="stExpander"] { border:1px solid var(--mb-border) !important; background:rgba(255,255,255,.02) !important; border-radius:14px !important; }
[data-testid="stPlotlyChart"] { border:1px solid rgba(148,163,184,.10); border-radius:18px; background:rgba(255,255,255,.018); overflow:hidden; }

@media (max-width: 900px) {
  .mb-page-hero { padding:24px; }
  .mb-result-banner { flex-direction:column; align-items:flex-start; }
  .mb-result-meta { width:100%; }
  .mb-form-intro,.mb-footer { flex-direction:column; align-items:flex-start; }
}
@media (max-width: 620px) {
  .mb-page-icon { display:none; }
  .mb-page-hero h1 { font-size:29px; }
  .mb-result-banner { padding:24px 21px; }
  .mb-result-meta { grid-template-columns:1fr; }
  .mb-result-stat { min-width:0; }
  .mb-guidance-panel { padding:21px 17px; }
  .mb-index-card { padding:21px 18px; }
}
</style>
"""


def inject_theme():  # noqa: F811
    """Apply the complete global theme."""
    st.markdown(THEME_CSS + EXTRA_THEME_CSS, unsafe_allow_html=True)

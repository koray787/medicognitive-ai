import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from PIL import Image
import matplotlib.pyplot as plt

from clinical_model import clinical_risk_assessment

# =========================================================

# PAGE CONFIG

# =========================================================

st.set_page_config(
page_title="MEDICOGNITIVE AI — Dr. Omnia Ali",
page_icon="🩺",
layout="wide",
initial_sidebar_state="collapsed"
)

# =========================================================

# LUXURY MEDICAL AI DESIGN SYSTEM

# =========================================================

st.markdown("""

<style>

@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Tajawal:wght@300;400;500;700;800&family=Inter:wght@400;500;600;700;800&display=swap');


/* =========================================================
   GLOBAL
========================================================= */

html, body, [class*="css"] {
    font-family: "Tajawal", "Inter", Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 50% 12%,
            rgba(212, 175, 55, 0.11),
            transparent 28%
        ),
        radial-gradient(
            circle at 5% 80%,
            rgba(170, 124, 17, 0.08),
            transparent 25%
        ),
        radial-gradient(
            circle at 95% 85%,
            rgba(212, 175, 55, 0.07),
            transparent 25%
        ),
        linear-gradient(
            145deg,
            #050505 0%,
            #0a0a09 45%,
            #030303 100%
        );

    color: #ffffff;
    min-height: 100vh;
}


/* =========================================================
   MAIN CONTAINER
========================================================= */

.main .block-container {
    max-width: 1550px;
    padding-top: 110px;
    padding-bottom: 4rem;
    padding-left: 2.5rem;
    padding-right: 2.5rem;
}


/* =========================================================
   SCROLLBAR
========================================================= */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #050505;
}

::-webkit-scrollbar-thumb {
    background: #6f5515;
    border-radius: 20px;
}

::-webkit-scrollbar-thumb:hover {
    background: #D4AF37;
}


/* =========================================================
   TOP NAVIGATION
========================================================= */

.luxury-nav {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 76px;
    z-index: 9999;

    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 0 5%;

    background:
        linear-gradient(
            90deg,
            rgba(5, 5, 5, 0.97),
            rgba(16, 14, 9, 0.96),
            rgba(5, 5, 5, 0.97)
        );

    backdrop-filter: blur(18px);

    border-bottom:
        1px solid rgba(212, 175, 55, 0.22);

    box-shadow:
        0 10px 40px rgba(0, 0, 0, 0.55);
}

.luxury-logo {
    font-family: "Cinzel", Georgia, serif;
    font-size: 22px;
    font-weight: 900;
    letter-spacing: 2px;

    background:
        linear-gradient(
            135deg,
            #BF953F,
            #FCF6BA,
            #B38728,
            #FBF5B7,
            #AA7C11
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    position: relative;
}

.luxury-logo::after {
    content: "";

    position: absolute;

    left: -40%;
    top: 0;

    width: 35%;
    height: 100%;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(255,255,255,0.8),
            transparent
        );

    transform: skewX(-20deg);

    animation: logoShine 4.5s infinite;
}

@keyframes logoShine {

    0% {
        left: -40%;
    }

    20% {
        left: 110%;
    }

    100% {
        left: 110%;
    }
}

.nav-medical-badge {
    display: flex;
    align-items: center;
    gap: 10px;

    color: #cfcfcf;

    font-size: 12px;
    letter-spacing: 1px;
}

.nav-medical-badge span {
    color: #D4AF37;
    font-size: 20px;
}


/* =========================================================
   BACKGROUND ORBS
========================================================= */

.luxury-bg {
    position: fixed;
    inset: 0;

    z-index: -1;

    pointer-events: none;

    overflow: hidden;
}

.luxury-orb {
    position: absolute;

    border-radius: 50%;

    filter: blur(90px);

    opacity: 0.13;

    animation:
        luxuryFloat 13s infinite alternate ease-in-out;
}

.luxury-orb.one {
    width: 420px;
    height: 420px;

    top: -170px;
    left: -130px;

    background: #D4AF37;
}

.luxury-orb.two {
    width: 520px;
    height: 520px;

    right: -220px;
    bottom: -260px;

    background: #8A6D3B;

    animation-delay: -5s;
}

@keyframes luxuryFloat {

    0% {
        transform: translate(0, 0) scale(1);
    }

    100% {
        transform: translate(45px, 70px) scale(1.12);
    }
}


/* =========================================================
   HERO
========================================================= */

.premium-hero {
    position: relative;

    min-height: 390px;

    padding: 55px 50px;

    margin-bottom: 35px;

    border-radius: 30px;

    overflow: hidden;

    text-align: center;

    background:
        radial-gradient(
            circle at 50% 35%,
            rgba(212, 175, 55, 0.10),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            rgba(17, 16, 12, 0.98),
            rgba(4, 4, 4, 0.99)
        );

    border:
        1px solid rgba(212, 175, 55, 0.28);

    box-shadow:
        0 35px 90px rgba(0, 0, 0, 0.60),
        0 0 80px rgba(212, 175, 55, 0.06),
        inset 0 1px 0 rgba(255,255,255,0.05);

    animation: heroFade 1.1s ease-out;
}

@keyframes heroFade {

    from {
        opacity: 0;
        transform: translateY(25px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.premium-hero::before {
    content: "";

    position: absolute;

    width: 600px;
    height: 600px;

    left: 50%;
    top: 50%;

    transform: translate(-50%, -50%);

    border-radius: 50%;

    border:
        1px solid rgba(212,175,55,0.08);

    box-shadow:
        0 0 100px rgba(212,175,55,0.05);

    animation: heroPulse 5s infinite ease-in-out;
}

@keyframes heroPulse {

    0%, 100% {
        transform:
            translate(-50%, -50%)
            scale(0.92);

        opacity: 0.45;
    }

    50% {
        transform:
            translate(-50%, -50%)
            scale(1.08);

        opacity: 0.9;
    }
}


/* =========================================================
   MEDICAL SYMBOL
========================================================= */

.doctor-symbol {
    position: relative;

    width: 92px;
    height: 92px;

    margin: 0 auto 25px auto;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(212,175,55,0.20),
            rgba(212,175,55,0.04)
        );

    border:
        1px solid rgba(212,175,55,0.45);

    box-shadow:
        0 0 45px rgba(212,175,55,0.16),
        inset 0 0 30px rgba(212,175,55,0.05);

    font-size: 46px;

    animation:
        doctorFloat 4s infinite ease-in-out;
}

@keyframes doctorFloat {

    0%, 100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-8px);
    }
}


/* =========================================================
   HERO TEXT
========================================================= */

.hero-subtitle-luxury {
    color: #D4AF37;

    font-size: 14px;

    letter-spacing: 4px;

    font-weight: 700;

    margin-bottom: 14px;
}

.hero-brand {
    font-family: "Cinzel", Georgia, serif;

    font-size: 47px;

    font-weight: 900;

    letter-spacing: 4px;

    margin-bottom: 12px;

    background:
        linear-gradient(
            135deg,
            #BF953F,
            #FCF6BA,
            #B38728,
            #FBF5B7,
            #AA7C11
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    color: #8f8f8f;

    font-size: 13px;

    letter-spacing: 2px;

    margin-bottom: 25px;
}

.doctor-name {
    font-family: "Tajawal", sans-serif;

    color: #ffffff;

    font-size: 28px;

    font-weight: 700;

    margin-top: 20px;
}

.doctor-title {
    color: #D4AF37;

    font-size: 12px;

    letter-spacing: 2px;

    margin-top: 5px;
}


/* =========================================================
   HERO GOLD LINE
========================================================= */

.gold-line {
    position: relative;

    width: 75%;

    height: 2px;

    margin: 30px auto 0 auto;

    background:
        linear-gradient(
            90deg,
            transparent,
            #D4AF37,
            #FFF099,
            #D4AF37,
            transparent
        );

    opacity: 0.65;

    overflow: hidden;
}

.gold-line::after {
    content: "";

    position: absolute;

    top: 0;
    left: -30%;

    width: 30%;
    height: 100%;

    background: #ffffff;

    filter: blur(4px);

    animation: goldScan 4s infinite;
}

@keyframes goldScan {

    0% {
        left: -30%;
    }

    50% {
        left: 100%;
    }

    100% {
        left: 100%;
    }
}


/* =========================================================
   ONLINE STATUS
========================================================= */

.system-status {
    display: inline-flex;

    align-items: center;

    margin-top: 25px;

    padding: 10px 18px;

    border-radius: 30px;

    background:
        rgba(212,175,55,0.06);

    border:
        1px solid rgba(212,175,55,0.22);

    color: #d9bd65;

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 1px;
}

.status-dot {
    width: 8px;
    height: 8px;

    display: inline-block;

    margin-left: 8px;

    border-radius: 50%;

    background: #D4AF37;

    box-shadow:
        0 0 12px #D4AF37;

    animation: goldStatus 1.8s infinite;
}

@keyframes goldStatus {

    0%, 100% {
        opacity: 1;
        transform: scale(1);
    }

    50% {
        opacity: 0.35;
        transform: scale(0.75);
    }
}


/* =========================================================
   HEADINGS
========================================================= */

h1, h2, h3, h4 {
    color: #ffffff !important;

    font-weight: 800 !important;
}

h3 {
    border-right:
        3px solid #D4AF37;

    padding-right: 12px;
}


/* =========================================================
   AI BANNER
========================================================= */

.ai-banner {
    position: relative;

    padding: 17px 22px;

    margin: 14px 0 24px 0;

    border-radius: 15px;

    background:
        linear-gradient(
            90deg,
            rgba(212,175,55,0.09),
            rgba(212,175,55,0.025),
            rgba(0,0,0,0.25)
        );

    border:
        1px solid rgba(212,175,55,0.18);

    color: #d8c47b;

    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.035);
}


/* =========================================================
   GLASS CARD
========================================================= */

.glass-card {
    background:
        linear-gradient(
            145deg,
            rgba(24,23,19,0.94),
            rgba(7,7,6,0.97)
        );

    border:
        1px solid rgba(212,175,55,0.16);

    border-radius: 20px;

    padding: 24px;

    margin-bottom: 18px;

    box-shadow:
        0 20px 50px rgba(0,0,0,0.45),
        inset 0 1px 0 rgba(255,255,255,0.035);

    transition: all 0.3s ease;
}

.glass-card:hover {
    transform: translateY(-4px);

    border-color:
        rgba(212,175,55,0.40);

    box-shadow:
        0 25px 65px rgba(0,0,0,0.52),
        0 0 30px rgba(212,175,55,0.07);
}


/* =========================================================
   VITAL CARDS
========================================================= */

.vital-card {
    position: relative;

    overflow: hidden;

    min-height: 145px;

    padding: 25px;

    border-radius: 20px;

    background:
        linear-gradient(
            145deg,
            rgba(22,21,17,0.97),
            rgba(5,5,5,0.98)
        );

    border:
        1px solid rgba(212,175,55,0.17);

    box-shadow:
        0 16px 40px rgba(0,0,0,0.40);

    transition: all 0.3s ease;
}

.vital-card::before {
    content: "";

    position: absolute;

    width: 150px;
    height: 150px;

    right: -80px;
    top: -80px;

    border-radius: 50%;

    background:
        rgba(212,175,55,0.07);
}

.vital-card:hover {
    transform: translateY(-6px);

    border-color:
        rgba(212,175,55,0.42);

    box-shadow:
        0 24px 55px rgba(0,0,0,0.50),
        0 0 30px rgba(212,175,55,0.08);
}

.vital-label {
    color: #8e8057;

    font-size: 11px;

    font-weight: 700;

    text-transform: uppercase;

    letter-spacing: 1.5px;
}

.vital-value {
    margin-top: 10px;

    font-size: 35px;

    font-weight: 900;

    color: #ffffff;
}

.vital-unit {
    margin-top: 5px;

    color: #716d62;

    font-size: 12px;
}


/* =========================================================
   RISK PANEL
========================================================= */

.risk-panel {
    position: relative;

    overflow: hidden;

    padding: 40px 25px;

    border-radius: 27px;

    text-align: center;

    background:
        radial-gradient(
            circle at center,
            rgba(212,175,55,0.12),
            rgba(5,5,5,0.98) 68%
        );

    border:
        1px solid rgba(212,175,55,0.28);

    box-shadow:
        0 30px 75px rgba(0,0,0,0.55),
        inset 0 1px 0 rgba(255,255,255,0.04);
}

.risk-panel::before {
    content: "";

    position: absolute;

    width: 220px;
    height: 220px;

    left: 50%;
    top: 50%;

    transform:
        translate(-50%, -50%);

    border-radius: 50%;

    border:
        1px solid rgba(212,175,55,0.10);

    box-shadow:
        0 0 60px rgba(212,175,55,0.06);
}

.risk-number {
    position: relative;

    font-size: 76px;

    font-weight: 900;

    line-height: 1;

    background:
        linear-gradient(
            180deg,
            #FFF099,
            #D4AF37,
            #AA7C11
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.risk-label {
    margin-top: 12px;

    color: #857a5c;

    font-size: 11px;

    font-weight: 700;

    letter-spacing: 3px;
}


/* =========================================================
   INPUTS
========================================================= */

.stTextInput input,
.stNumberInput input {

    background:
        rgba(10,10,9,0.90) !important;

    color:
        #ffffff !important;

    border:
        1px solid rgba(212,175,55,0.20) !important;

    border-radius:
        12px !important;
}

.stTextInput input:focus,
.stNumberInput input:focus {

    border-color:
        rgba(212,175,55,0.65) !important;

    box-shadow:
        0 0 15px rgba(212,175,55,0.08) !important;
}

.stSelectbox > div > div {

    background:
        rgba(10,10,9,0.90) !important;

    border-radius:
        12px !important;

    border-color:
        rgba(212,175,55,0.20) !important;
}

.stSlider {
    padding-top: 5px;
}


/* =========================================================
   BUTTONS
========================================================= */

.stButton > button {

    width: 100%;

    min-height: 48px;

    border-radius: 13px;

    border:
        1px solid rgba(212,175,55,0.38);

    background:
        linear-gradient(
            135deg,
            #8f6c17,
            #D4AF37,
            #9b7417
        );

    color:
        #050505;

    font-weight:
        800;

    letter-spacing:
        0.5px;

    box-shadow:
        0 10px 30px rgba(212,175,55,0.12);

    transition:
        all 0.25s ease;
}

.stButton > button:hover {

    transform:
        translateY(-3px);

    border-color:
        #FFF099;

    box-shadow:
        0 15px 40px rgba(212,175,55,0.25);
}


/* =========================================================
   TABS
========================================================= */

.stTabs [data-baseweb="tab-list"] {

    gap: 7px;

    padding: 7px;

    border-radius: 18px;

    background:
        rgba(5,5,5,0.82);

    border:
        1px solid rgba(212,175,55,0.13);

    box-shadow:
        0 14px 35px rgba(0,0,0,0.35);
}

.stTabs [data-baseweb="tab"] {

    border-radius: 13px;

    padding: 12px 21px;

    color:
        #7e786b;

    font-weight:
        700;

    transition:
        all 0.25s ease;
}

.stTabs [data-baseweb="tab"]:hover {

    color:
        #F4D96B;
}

.stTabs [aria-selected="true"] {

    background:
        linear-gradient(
            135deg,
            rgba(212,175,55,0.18),
            rgba(212,175,55,0.05)
        );

    color:
        #F1D768 !important;

    box-shadow:
        0 0 25px rgba(212,175,55,0.07);
}


/* =========================================================
   ALERTS
========================================================= */

div[data-testid="stAlert"] {

    border-radius: 15px;

    border:
        1px solid rgba(212,175,55,0.12);

    background:
        rgba(15,15,13,0.82);
}


/* =========================================================
   FILE UPLOADER
========================================================= */

[data-testid="stFileUploader"] {

    background:
        rgba(8,8,7,0.72);

    border-radius:
        18px;

    padding:
        8px;

    border:
        1px dashed rgba(212,175,55,0.30);
}


/* =========================================================
   DATAFRAME
========================================================= */

[data-testid="stDataFrame"] {

    border-radius:
        16px;

    overflow:
        hidden;

    border:
        1px solid rgba(212,175,55,0.15);
}


/* =========================================================
   ECG
========================================================= */

.ecg-line {

    height: 45px;

    margin-top: 25px;

    opacity: 0.55;

    overflow: hidden;
}

.ecg-line svg {

    width: 100%;

    height: 45px;
}


/* =========================================================
   FOOTER
========================================================= */

.premium-footer {

    position: relative;

    text-align: center;

    margin-top: 65px;

    padding: 35px 20px;

    border-top:
        1px solid rgba(212,175,55,0.14);

    color:
        #655f51;

    font-size:
        11px;

    letter-spacing:
        0.5px;
}

.footer-brand {

    font-family:
        "Cinzel", Georgia, serif;

    color:
        #D4AF37;

    font-size:
        15px;

    font-weight:
        900;

    letter-spacing:
        2px;

    margin-bottom:
        10px;
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 768px) {

    .main .block-container {

        padding-left:
            1rem;

        padding-right:
            1rem;

        padding-top:
            95px;
    }

    .luxury-nav {

        height:
            65px;

        padding:
            0 20px;
    }

    .luxury-logo {

        font-size:
            16px;
    }

    .nav-medical-badge {

        display:
            none;
    }

    .premium-hero {

        padding:
            35px 20px;

        min-height:
            360px;
    }

    .hero-brand {

        font-size:
            28px;

        letter-spacing:
            1px;
    }

    .hero-subtitle-luxury {

        font-size:
            11px;

        letter-spacing:
            2px;
    }

    .hero-description {

        font-size:
            10px;

        letter-spacing:
            1px;
    }

    .doctor-name {

        font-size:
            23px;
    }

    .doctor-symbol {

        width:
            70px;

        height:
            70px;

        font-size:
            35px;
    }

    .risk-number {

        font-size:
            58px;
    }

    .stTabs [data-baseweb="tab"] {

        padding:
            10px 9px;

        font-size:
            11px;
    }
}


/* =========================================================
   HIDE STREAMLIT BRANDING
========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background:
        transparent !important;
}

</style>

""", unsafe_allow_html=True)

# =========================================================

# LUXURY BACKGROUND

# =========================================================

st.markdown("""

<div class="luxury-bg">
    <div class="luxury-orb one"></div>
    <div class="luxury-orb two"></div>
</div>
""", unsafe_allow_html=True)

# =========================================================

# LUXURY NAVIGATION

# =========================================================

st.markdown("""

<div class="luxury-nav">

```
<div class="luxury-logo">
    DR. OMNIA ALI
</div>

<div class="nav-medical-badge">
    <span>🩺</span>
    MEDICAL AI RESEARCH PLATFORM
</div>
```

</div>
""", unsafe_allow_html=True)

# =========================================================

# PREMIUM HERO

# =========================================================

st.markdown("""

<div class="premium-hero">

```
<div class="doctor-symbol">
    🩺
</div>

<div class="hero-subtitle-luxury">
    رعاية طبية بمقاييس عالمية
</div>

<div class="hero-brand">
    MEDICOGNITIVE AI
</div>

<div class="hero-description">
    MULTIMODAL CLINICAL INTELLIGENCE • EARLY WARNING • AI RESEARCH PLATFORM
</div>

<div class="doctor-name">
    الدكتورة أمنية علي
</div>

<div class="doctor-title">
    MEDICAL AI RESEARCH & CLINICAL INTELLIGENCE
</div>

<div class="gold-line"></div>

<div class="ecg-line">

    <svg viewBox="0 0 1000 45" preserveAspectRatio="none">

        <polyline
            points="
            0,23
            100,23
            125,23
            140,10
            150,37
            165,23
            300,23
            330,23
            350,6
            360,40
            375,23
            500,23
            530,23
            550,12
            560,35
            575,23
            700,23
            730,23
            750,8
            760,38
            775,23
            900,23
            930,23
            950,10
            960,37
            975,23
            1000,23"
            fill="none"
            stroke="#D4AF37"
            stroke-width="2"
        />

    </svg>

</div>

<div class="system-status">

    <span class="status-dot"></span>

    AI SYSTEM ONLINE
    &nbsp; • &nbsp;
    CLINICAL ENGINE ACTIVE

</div>
```

</div>
""", unsafe_allow_html=True)

# =========================================================

# TABS

# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
"👤 PATIENT PROFILE",
"📈 CLINICAL TRENDS",
"👁️ AI VISION",
"🧠 AI RISK INTELLIGENCE"
])

# =========================================================

# TAB 1 — PATIENT

# =========================================================

with tab1:

```
st.markdown("### 👤 Patient Clinical Profile")

st.markdown(
    '<div class="ai-banner">'
    '✦ Clinical intelligence interface ready — enter patient parameters to activate analysis.'
    '</div>',
    unsafe_allow_html=True
)

patient_id = st.text_input(
    "Patient Identification Number",
    value="MC-10482",
    disabled=True
)

col1, col2 = st.columns(2)

with col1:

    age = st.number_input(
        "Age (Years)",
        min_value=1,
        max_value=120,
        value=62
    )

    sex = st.selectbox(
        "Sex",
        ["Male", "Female"]
    )

    spo2 = st.slider(
        "Oxygen Saturation — SpO₂ (%)",
        min_value=50,
        max_value=100,
        value=91
    )

    hr = st.number_input(
        "Heart Rate (bpm)",
        min_value=30,
        max_value=220,
        value=112
    )

with col2:

    temp = st.number_input(
        "Body Temperature (°C)",
        min_value=30.0,
        max_value=45.0,
        value=38.9,
        step=0.1
    )

    rr = st.number_input(
        "Respiratory Rate (/min)",
        min_value=5,
        max_value=60,
        value=25
    )

    crp = st.number_input(
        "C-Reactive Protein — CRP (mg/L)",
        min_value=0.0,
        max_value=300.0,
        value=45.0
    )

    wbc = st.number_input(
        "White Blood Cell Count — WBC (k/µL)",
        min_value=0.0,
        max_value=50.0,
        value=14.5
    )


# =====================================================
# LIVE DASHBOARD
# =====================================================

st.markdown("### 📡 Live Clinical Parameters")

v1, v2, v3, v4 = st.columns(4)

with v1:

    st.markdown(
        f"""
        <div class="vital-card">

            <div class="vital-label">
                Oxygen Saturation
            </div>

            <div class="vital-value">
                {spo2}%
            </div>

            <div class="vital-unit">
                SpO₂
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with v2:

    st.markdown(
        f"""
        <div class="vital-card">

            <div class="vital-label">
                Heart Rate
            </div>

            <div class="vital-value">
                {hr}
            </div>

            <div class="vital-unit">
                Beats / Minute
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with v3:

    st.markdown(
        f"""
        <div class="vital-card">

            <div class="vital-label">
                Temperature
            </div>

            <div class="vital-value">
                {temp}
            </div>

            <div class="vital-unit">
                ° Celsius
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

with v4:

    st.markdown(
        f"""
        <div class="vital-card">

            <div class="vital-label">
                Respiratory Rate
            </div>

            <div class="vital-value">
                {rr}
            </div>

            <div class="vital-unit">
                Breaths / Minute
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )
```

# =========================================================

# TAB 2 — TRENDS

# =========================================================

with tab2:

```
st.markdown("### 📈 Longitudinal Clinical Intelligence")

st.markdown(
    '<div class="ai-banner">'
    '◈ Temporal AI engine — tracking physiological trajectory and deterioration patterns.'
    '</div>',
    unsafe_allow_html=True
)

dates = [
    datetime.now() - timedelta(days=i)
    for i in range(6, -1, -1)
]

dates_str = [
    d.strftime("%b %d")
    for d in dates
]

mock_spo2 = [
    98, 97, 96, 94, 93, 92, spo2
]

mock_temp = [
    36.6, 36.9, 37.2, 37.8, 38.2, 38.6, temp
]

mock_hr = [
    70, 75, 82, 90, 98, 105, hr
]

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=dates_str,
        y=mock_spo2,
        mode="lines+markers",
        name="SpO₂",
        line=dict(
            color="#D4AF37",
            width=4
        ),
        marker=dict(
            size=8
        )
    )
)

fig.add_trace(
    go.Scatter(
        x=dates_str,
        y=mock_temp,
        mode="lines+markers",
        name="Temperature",
        line=dict(
            color="#FFF099",
            width=3
        )
    )
)

fig.add_trace(
    go.Scatter(
        x=dates_str,
        y=mock_hr,
        mode="lines+markers",
        name="Heart Rate",
        line=dict(
            color="#B38728",
            width=3
        )
    )
)

fig.update_layout(
    title="7-Day Physiological Trajectory",
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(10,9,7,0.75)",
    font=dict(
        color="#d9c989"
    ),
    xaxis=dict(
        gridcolor="rgba(212,175,55,0.08)"
    ),
    yaxis=dict(
        gridcolor="rgba(212,175,55,0.08)"
    ),
    hovermode="x unified",
    margin=dict(
        l=15,
        r=15,
        t=60,
        b=15
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

if spo2 < 92 or temp > 38.5:

    st.error(
        "⚠️ TEMPORAL WARNING — Current parameters indicate a potentially abnormal physiological trajectory."
    )

else:

    st.success(
        "✓ No critical temporal alert detected in the current prototype."
    )
```

# =========================================================

# TAB 3 — AI VISION

# =========================================================

with tab3:

```
st.markdown("### 👁️ AI Medical Vision")

st.markdown(
    '<div class="ai-banner">'
    '◉ Computer Vision Module — Chest X-Ray analysis pipeline.'
    '</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload Chest X-Ray",
    type=[
        "png",
        "jpg",
        "jpeg"
    ]
)

if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    ).convert("RGB")

    col_img1, col_img2 = st.columns(2)

    with col_img1:

        st.markdown("#### ORIGINAL IMAGE")

        st.image(
            image,
            use_container_width=True
        )

    with col_img2:

        st.markdown("#### AI ATTENTION MAP")

        img_np = np.array(
            image.resize((224, 224))
        )

        heatmap = np.zeros(
            (224, 224)
        )

        heatmap[
            100:180,
            120:200
        ] = 0.8

        fig_cam, ax = plt.subplots(
            figsize=(5, 5)
        )

        ax.imshow(
            img_np
        )

        ax.imshow(
            heatmap,
            cmap="jet",
            alpha=0.40
        )

        ax.axis("off")

        st.pyplot(
            fig_cam
        )

    st.warning(
        "⚠️ Current imaging visualization is a prototype. "
        "A validated medical imaging model will be integrated "
        "in the next development stage."
    )

else:

    st.info(
        "📤 Upload a chest X-Ray image to activate the computer-vision interface."
    )
```

# =========================================================

# TAB 4 — AI RISK REPORT

# =========================================================

with tab4:

```
st.markdown("### 🧠 Multimodal Clinical Intelligence")

st.markdown(
    '<div class="ai-banner">'
    '✦ AI clinical reasoning engine integrating physiological and laboratory parameters.'
    '</div>',
    unsafe_allow_html=True
)


# =====================================================
# CLINICAL MODEL
# =====================================================

score, risk_level, contributions = clinical_risk_assessment(
    age=age,
    sex=sex,
    spo2=spo2,
    heart_rate=hr,
    temperature=temp,
    respiratory_rate=rr,
    crp=crp,
    wbc=wbc
)


# =====================================================
# RISK DISPLAY
# =====================================================

left, right = st.columns([1, 2])

with left:

    st.markdown(
        f"""
        <div class="risk-panel">

            <div class="risk-number">
                {score}
            </div>

            <div class="risk-label">
                AI RISK SCORE / 100
            </div>

            <br>

            <strong style="
                color:#D4AF37;
                font-size:23px;
                letter-spacing:1px;
            ">
                {risk_level}
            </strong>

        </div>
        """,
        unsafe_allow_html=True
    )

with right:

    st.markdown("#### 🔎 Clinical Interpretation")

    if risk_level == "HIGH":

        st.error(
            "HIGH RISK — Multiple abnormal clinical parameters are contributing to the calculated prototype risk score."
        )

    elif risk_level == "MODERATE":

        st.warning(
            "MODERATE RISK — Abnormal parameters detected. Increased monitoring may be appropriate."
        )

    else:

        st.success(
            "LOWER RISK — No major abnormalities detected by the current prototype scoring engine."
        )

    st.markdown(
        f"""
        <div class="glass-card">

            <div style="
                color:#8e8057;
                font-size:11px;
                letter-spacing:1.5px;
                text-transform:uppercase;
            ">
                Patient Intelligence Record
            </div>

            <br>

            <b>Patient:</b>
            {patient_id}

            <br><br>

            <b>AI Assessment:</b>
            {risk_level}

            <br><br>

            <b>Risk Score:</b>
            {score}/100

            <br><br>

            <b>Analysis Time:</b>
            {datetime.now().strftime("%H:%M:%S")}

        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# CONTRIBUTIONS
# =====================================================

st.markdown("### 🧬 AI Contributing Factors")

contribution_df = pd.DataFrame(
    {
        "Clinical Factor": list(
            contributions.keys()
        ),
        "Contribution": list(
            contributions.values()
        )
    }
)

contribution_df = contribution_df.sort_values(
    "Contribution",
    ascending=False
)

st.bar_chart(
    contribution_df.set_index(
        "Clinical Factor"
    )
)


# =====================================================
# CLINICAL DATA
# =====================================================

st.markdown("### 📊 Multimodal Patient Profile")

profile = pd.DataFrame(
    {
        "Parameter": [
            "Age",
            "Sex",
            "SpO₂",
            "Heart Rate",
            "Temperature",
            "Respiratory Rate",
            "CRP",
            "WBC"
        ],

        "Value": [
            f"{age} years",
            sex,
            f"{spo2} %",
            f"{hr} bpm",
            f"{temp} °C",
            f"{rr} /min",
            f"{crp} mg/L",
            f"{wbc} k/µL"
        ]
    }
)

st.dataframe(
    profile,
    use_container_width=True,
    hide_index=True
)


# =====================================================
# REPORT
# =====================================================

st.markdown("### 📄 Generate Clinical AI Report")

report_content = f"""
```

============================================================
MEDICOGNITIVE AI
DR. OMNIA ALI
MULTIMODAL CLINICAL AI REPORT
=============================

SYSTEM STATUS:
AI CLINICAL ENGINE ACTIVE

DATE:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

PATIENT ID:
{patient_id}

---

## PATIENT PROFILE

Age: {age}
Sex: {sex}

---

## PHYSIOLOGICAL PARAMETERS

SpO2: {spo2} %
Heart Rate: {hr} bpm
Temperature: {temp} °C
Respiratory Rate: {rr} /min

---

## LABORATORY PARAMETERS

CRP: {crp} mg/L
WBC: {wbc} k/µL

---

## AI CLINICAL RISK ASSESSMENT

Risk Score: {score}/100
Risk Level: {risk_level}

---

## CONTRIBUTING FACTORS

"""

```
for factor, contribution in contributions.items():

    report_content += (
        f"{factor}: {contribution}\n"
    )

report_content += """
```

---

## IMPORTANT SAFETY NOTICE

MEDICOGNITIVE AI is a research prototype designed
for educational, experimental and clinical decision-support
research purposes.

It is NOT a replacement for professional medical diagnosis,
clinical examination, or physician judgment.

All AI outputs require appropriate clinical validation
before real-world medical use.

============================================================
DR. OMNIA ALI
MEDICOGNITIVE AI
================

"""

```
st.download_button(
    label="📥 DOWNLOAD AI CLINICAL REPORT",
    data=report_content,
    file_name=(
        f"MEDICOGNITIVE_AI_"
        f"{patient_id}.txt"
    ),
    mime="text/plain"
)
```

# =========================================================

# PREMIUM FOOTER

# =========================================================

st.markdown("""

<div class="premium-footer">

```
<div class="footer-brand">
    🩺 MEDICOGNITIVE AI
</div>

<b style="color:#D4AF37;">
    الدكتورة أمنية علي
</b>

<br><br>

Multimodal Clinical Intelligence Research Platform

<br><br>

🧠 Clinical Risk Engine
&nbsp; • &nbsp;
👁️ Computer Vision
&nbsp; • &nbsp;
📈 Temporal Analysis
&nbsp; • &nbsp;
📊 Multimodal Decision Support

<br><br>

<span style="color:#514c40;">
    Research Prototype • Clinical Validation Required
</span>
```

</div>
""", unsafe_allow_html=True)

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
# PREMIUM MEDICAL AI DESIGN SYSTEM
# =========================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');

    /* GLOBAL */
    html, body, [class*="css"] {
        font-family: "Inter", "Segoe UI", Arial, sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 5% 5%,
                rgba(45, 212, 191, 0.10),
                transparent 24%
            ),
            radial-gradient(
                circle at 95% 10%,
                rgba(14, 165, 233, 0.13),
                transparent 28%
            ),
            radial-gradient(
                circle at 50% 95%,
                rgba(16, 185, 129, 0.07),
                transparent 30%
            ),
            linear-gradient(
                145deg,
                #020817 0%,
                #06121c 48%,
                #031019 100%
            );

        color: #e6fffb;
    }

    .main .block-container {
        max-width: 1550px;
        padding-top: 1.5rem;
        padding-bottom: 4rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }

    /* SCROLLBAR */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #020817;
    }

    ::-webkit-scrollbar-thumb {
        background: #155e75;
        border-radius: 20px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #14b8a6;
    }

    /* HERO */
    .premium-hero {
        position: relative;
        min-height: 260px;
        padding: 38px 45px;
        margin-bottom: 28px;
        border-radius: 30px;
        overflow: hidden;

        background:
            linear-gradient(
                135deg,
                rgba(7, 30, 42, 0.98),
                rgba(3, 18, 30, 0.98)
            );

        border: 1px solid rgba(45, 212, 191, 0.22);

        box-shadow:
            0 30px 80px rgba(0,0,0,0.45),
            0 0 80px rgba(20,184,166,0.05),
            inset 0 1px 0 rgba(255,255,255,0.05);
    }

    .premium-hero::before {
        content: "";
        position: absolute;

        width: 520px;
        height: 520px;

        right: -220px;
        top: -250px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(45,212,191,0.20),
                rgba(14,165,233,0.08),
                transparent 70%
            );

        animation: pulseGlow 5s infinite ease-in-out;
    }

    .premium-hero::after {
        content: "";
        position: absolute;

        width: 700px;
        height: 1px;

        left: 0;
        bottom: 0;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(45,212,191,0.45),
                transparent
            );

        animation: scanLine 5s infinite linear;
    }

    @keyframes pulseGlow {
        0%,100% {
            transform: scale(1);
            opacity: .65;
        }

        50% {
            transform: scale(1.15);
            opacity: 1;
        }
    }

    @keyframes scanLine {
        0% {
            transform: translateX(-100%);
        }

        100% {
            transform: translateX(200%);
        }
    }

    /* DOCTOR ICON */
    .doctor-symbol {
        width: 74px;
        height: 74px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 22px;

        background:
            linear-gradient(
                145deg,
                rgba(20,184,166,0.20),
                rgba(14,165,233,0.10)
            );

        border: 1px solid rgba(94,234,212,0.30);

        box-shadow:
            0 0 30px rgba(20,184,166,0.12),
            inset 0 1px 0 rgba(255,255,255,0.07);

        font-size: 38px;

        animation:
            floatingDoctor 4s infinite ease-in-out;
    }

    @keyframes floatingDoctor {
        0%,100% {
            transform: translateY(0px);
        }

        50% {
            transform: translateY(-7px);
        }
    }

    /* HERO TITLE */
    .hero-brand {
        font-size: 42px;
        font-weight: 800;
        letter-spacing: 3px;
        margin-top: 18px;

        background:
            linear-gradient(
                90deg,
                #ffffff,
                #ccfbf1,
                #5eead4,
                #38bdf8
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-description {
        margin-top: 7px;
        color: #7da1ad;
        font-size: 14px;
        letter-spacing: 1.5px;
    }

    /* DOCTOR SIGNATURE */
    .doctor-name {
        margin-top: 25px;

        font-family:
            "Playfair Display",
            Georgia,
            serif;

        font-size: 25px;
        color: #d9fffa;
        letter-spacing: .5px;
    }

    .doctor-title {
        color: #55d6c2;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 2px;
    }

    /* ONLINE STATUS */
    .system-status {
        position: absolute;

        right: 38px;
        bottom: 30px;

        padding: 11px 18px;

        border-radius: 30px;

        background:
            rgba(16,185,129,0.08);

        border:
            1px solid rgba(52,211,153,0.25);

        color: #6ee7b7;

        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;

        box-shadow:
            0 0 25px rgba(16,185,129,0.08);
    }

    .status-dot {
        display: inline-block;

        width: 8px;
        height: 8px;

        margin-right: 8px;

        border-radius: 50%;

        background: #34d399;

        box-shadow:
            0 0 12px #34d399;

        animation: statusPulse 1.8s infinite;
    }

    @keyframes statusPulse {
        0%,100% {
            opacity: 1;
            transform: scale(1);
        }

        50% {
            opacity: .4;
            transform: scale(.75);
        }
    }

    /* HEADINGS */
    h1, h2, h3, h4 {
        color: #ecfffc !important;
        font-weight: 750 !important;
    }

    /* AI BANNER */
    .ai-banner {
        position: relative;

        padding: 17px 21px;

        margin: 14px 0 22px 0;

        border-radius: 16px;

        background:
            linear-gradient(
                90deg,
                rgba(20,184,166,0.09),
                rgba(14,165,233,0.07),
                rgba(99,102,241,0.05)
            );

        border:
            1px solid rgba(45,212,191,0.15);

        color: #a9e8df;

        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.03);
    }

    /* GLASS CARD */
    .glass-card {
        background:
            linear-gradient(
                145deg,
                rgba(13,36,48,0.90),
                rgba(4,19,29,0.94)
            );

        border:
            1px solid rgba(94,234,212,0.12);

        border-radius: 20px;

        padding: 23px;

        margin-bottom: 18px;

        box-shadow:
            0 18px 45px rgba(0,0,0,0.30),
            inset 0 1px 0 rgba(255,255,255,0.035);

        transition:
            all .3s ease;
    }

    .glass-card:hover {
        transform: translateY(-4px);

        border-color:
            rgba(45,212,191,0.28);

        box-shadow:
            0 22px 60px rgba(0,0,0,.38),
            0 0 35px rgba(20,184,166,.07);
    }

    /* VITAL CARDS */
    .vital-card {
        position: relative;
        overflow: hidden;

        min-height: 135px;

        padding: 23px;

        border-radius: 21px;

        background:
            linear-gradient(
                145deg,
                rgba(12,38,51,0.96),
                rgba(4,19,29,0.96)
            );

        border:
            1px solid rgba(56,189,248,0.14);

        box-shadow:
            0 14px 35px rgba(0,0,0,.28);

        transition:
            transform .3s ease,
            border-color .3s ease,
            box-shadow .3s ease;
    }

    .vital-card::before {
        content: "";

        position: absolute;

        width: 120px;
        height: 120px;

        right: -65px;
        top: -65px;

        border-radius: 50%;

        background:
            rgba(45,212,191,.08);

        filter: blur(2px);
    }

    .vital-card:hover {
        transform: translateY(-6px);

        border-color:
            rgba(94,234,212,.30);

        box-shadow:
            0 20px 55px rgba(0,0,0,.35),
            0 0 28px rgba(20,184,166,.07);
    }

    .vital-label {
        color: #6f98a6;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.7px;
    }

    .vital-value {
        margin-top: 9px;

        font-size: 34px;
        font-weight: 800;

        color: #edfffc;
        letter-spacing: -1px;
    }

    .vital-unit {
        margin-top: 5px;
        color: #64828f;
        font-size: 12px;
    }

    /* RISK PANEL */
    .risk-panel {
        position: relative;
        overflow: hidden;

        padding: 38px 25px;

        border-radius: 27px;

        text-align: center;

        background:
            radial-gradient(
                circle at center,
                rgba(20,184,166,.13),
                rgba(3,17,27,.96) 65%
            );

        border:
            1px solid rgba(94,234,212,.20);

        box-shadow:
            0 25px 70px rgba(0,0,0,.38),
            inset 0 1px 0 rgba(255,255,255,.04);
    }

    .risk-panel::before {
        content: "";

        position: absolute;

        width: 220px;
        height: 220px;

        left: 50%;
        top: 50%;

        transform:
            translate(-50%,-50%);

        border-radius: 50%;

        border:
            1px solid rgba(45,212,191,.08);

        box-shadow:
            0 0 50px rgba(20,184,166,.05);
    }

    .risk-number {
        position: relative;

        font-size: 76px;
        font-weight: 900;
        line-height: 1;

        background:
            linear-gradient(
                180deg,
                #ffffff,
                #99f6e4,
                #2dd4bf
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .risk-label {
        margin-top: 12px;

        color: #71909b;

        font-size: 11px;
        font-weight: 700;
        letter-spacing: 3px;
    }

    /* INPUTS */
    .stTextInput input,
    .stNumberInput input {
        background:
            rgba(5,22,32,.85) !important;

        color: #eafffb !important;

        border:
            1px solid rgba(94,234,212,.13) !important;

        border-radius: 12px !important;
    }

    .stSelectbox > div > div {
        background:
            rgba(5,22,32,.85) !important;

        border-radius: 12px !important;

        border-color:
            rgba(94,234,212,.13) !important;
    }

    .stSlider {
        padding-top: 5px;
    }

    /* BUTTONS */
    .stButton > button {
        width: 100%;

        min-height: 48px;

        border-radius: 13px;

        border:
            1px solid rgba(94,234,212,.25);

        background:
            linear-gradient(
                135deg,
                #0f766e,
                #0369a1
            );

        color: white;

        font-weight: 750;
        letter-spacing: .5px;

        box-shadow:
            0 8px 25px rgba(14,165,233,.12);

        transition:
            all .25s ease;
    }

    .stButton > button:hover {
        transform: translateY(-3px);

        border-color:
            rgba(153,246,228,.55);

        box-shadow:
            0 12px 35px rgba(20,184,166,.22);
    }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 7px;

        padding: 7px;

        border-radius: 18px;

        background:
            rgba(2,12,20,.72);

        border:
            1px solid rgba(94,234,212,.10);

        box-shadow:
            0 12px 30px rgba(0,0,0,.22);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 13px;

        padding: 12px 21px;

        color: #6d8995;

        font-weight: 700;

        transition:
            all .25s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #b8fff5;
    }

    .stTabs [aria-selected="true"] {
        background:
            linear-gradient(
                135deg,
                rgba(20,184,166,.18),
                rgba(14,165,233,.12)
            );

        color: #7df5df !important;

        box-shadow:
            0 0 25px rgba(20,184,166,.07);
    }

    /* ALERTS */
    div[data-testid="stAlert"] {
        border-radius: 15px;

        border:
            1px solid rgba(255,255,255,.08);

        background:
            rgba(8,25,35,.72);
    }

    /* FILE UPLOADER */
    [data-testid="stFileUploader"] {
        background:
            rgba(5,22,32,.55);

        border-radius: 18px;

        padding: 8px;

        border:
            1px dashed rgba(94,234,212,.20);
    }

    /* DATAFRAME */
    [data-testid="stDataFrame"] {
        border-radius: 16px;

        overflow: hidden;

        border:
            1px solid rgba(94,234,212,.10);
    }

    /* FOOTER */
    .premium-footer {
        position: relative;

        text-align: center;

        margin-top: 60px;

        padding: 30px 20px;

        border-top:
            1px solid rgba(255,255,255,.06);

        color: #52717d;

        font-size: 11px;

        letter-spacing: .5px;
    }

    .footer-brand {
        color: #73daca;

        font-size: 14px;

        font-weight: 800;

        letter-spacing: 2px;

        margin-bottom: 8px;
    }

    /* MOBILE */
    @media (max-width: 768px) {

        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .premium-hero {
            padding: 28px 22px;
            min-height: 330px;
        }

        .hero-brand {
            font-size: 28px;
            letter-spacing: 1px;
        }

        .system-status {
            position: relative;

            right: auto;
            bottom: auto;

            display: inline-block;

            margin-top: 20px;
        }

        .doctor-symbol {
            width: 60px;
            height: 60px;
            font-size: 30px;
        }

        .risk-number {
            font-size: 58px;
        }
    }

    /* HIDE STREAMLIT BRANDING */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* ECG LINE */
    .ecg-line {
        height: 45px;

        margin-top: 22px;

        opacity: .45;

        overflow: hidden;
    }

    .ecg-line svg {
        width: 100%;
        height: 45px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# PREMIUM HERO
# =========================================================

st.markdown(
    """
    <div class="premium-hero">

        <div class="doctor-symbol">
            🩺
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
            Medical AI Research & Clinical Intelligence
        </div>

        <div class="ecg-line">

            <svg viewBox="0 0 1000 45"
                 preserveAspectRatio="none">

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
                    stroke="#43e6d1"
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

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "👤 PATIENT PROFILE",
        "📈 CLINICAL TRENDS",
        "👁️ AI VISION",
        "🧠 AI RISK INTELLIGENCE"
    ]
)


# =========================================================
# TAB 1 — PATIENT
# =========================================================

with tab1:

    st.markdown("### 👤 Patient Clinical Profile")

    st.markdown(
        """
        <div class="ai-banner">
            ✦ Clinical intelligence interface ready —
            enter patient parameters to activate analysis.
        </div>
        """,
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


# =========================================================
# TAB 2 — TRENDS
# =========================================================

with tab2:

    st.markdown("### 📈 Longitudinal Clinical Intelligence")

    st.markdown(
        """
        <div class="ai-banner">
            ◈ Temporal AI engine — tracking physiological trajectory
            and deterioration patterns.
        </div>
        """,
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
                color="#2dd4bf",
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
                color="#f59e0b",
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
                color="#60a5fa",
                width=3
            )
        )
    )

    fig.update_layout(

        title="7-Day Physiological Trajectory",

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(3,15,24,0.65)",

        font=dict(
            color="#b8dcea"
        ),

        xaxis=dict(
            gridcolor="rgba(255,255,255,0.05)"
        ),

        yaxis=dict(
            gridcolor="rgba(255,255,255,0.05)"
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
            "⚠️ TEMPORAL WARNING — Current parameters indicate "
            "a potentially abnormal physiological trajectory."
        )

    else:

        st.success(
            "✓ No critical temporal alert detected "
            "in the current prototype."
        )


# =========================================================
# TAB 3 — AI VISION
# =========================================================

with tab3:

    st.markdown("### 👁️ AI Medical Vision")

    st.markdown(
        """
        <div class="ai-banner">
            ◉ Computer Vision Module — Chest X-Ray analysis pipeline.
        </div>
        """,
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

            plt.close(fig_cam)

        st.warning(
            "⚠️ Current imaging visualization is a prototype. "
            "A validated medical imaging model will be integrated "
            "in the next development stage."
        )

    else:

        st.info(
            "📤 Upload a chest X-Ray image to activate "
            "the computer-vision interface."
        )


# =========================================================
# TAB 4 — AI RISK REPORT
# =========================================================

with tab4:

    st.markdown("### 🧠 Multimodal Clinical Intelligence")

    st.markdown(
        """
        <div class="ai-banner">
            ✦ AI clinical reasoning engine integrating
            physiological and laboratory parameters.
        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # CLINICAL MODEL
    # =====================================================

    try:

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

    except Exception as e:

        st.error(
            "Clinical model error: "
            + str(e)
        )

        score = 0
        risk_level = "UNKNOWN"
        contributions = {
            "Model Error": 0
        }

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
                    color:#5eead4;
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
                "HIGH RISK — Multiple abnormal clinical parameters "
                "are contributing to the calculated prototype risk score."
            )

        elif risk_level == "MODERATE":

            st.warning(
                "MODERATE RISK — Abnormal parameters detected. "
                "Increased monitoring may be appropriate."
            )

        elif risk_level == "LOW":

            st.success(
                "LOWER RISK — No major abnormalities detected "
                "by the current prototype scoring engine."
            )

        else:

            st.info(
                "Risk level could not be determined."
            )

        st.markdown(
            f"""
            <div class="glass-card">

                <div style="
                    color:#6f98a6;
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
============================================================
                MEDICOGNITIVE AI
                    DR. OMNIA ALI
             MULTIMODAL CLINICAL AI REPORT
============================================================

SYSTEM STATUS:
AI CLINICAL ENGINE ACTIVE

DATE:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

PATIENT ID:
{patient_id}

------------------------------------------------------------
PATIENT PROFILE
------------------------------------------------------------

Age: {age}
Sex: {sex}

------------------------------------------------------------
PHYSIOLOGICAL PARAMETERS
------------------------------------------------------------

SpO2: {spo2} %
Heart Rate: {hr} bpm
Temperature: {temp} °C
Respiratory Rate: {rr} /min

------------------------------------------------------------
LABORATORY PARAMETERS
------------------------------------------------------------

CRP: {crp} mg/L
WBC: {wbc} k/µL

------------------------------------------------------------
AI CLINICAL RISK ASSESSMENT
------------------------------------------------------------

Risk Score: {score}/100
Risk Level: {risk_level}

------------------------------------------------------------
CONTRIBUTING FACTORS
------------------------------------------------------------

"""

    for factor, contribution in contributions.items():

        report_content += (
            f"{factor}: {contribution}\n"
        )

    report_content += """

------------------------------------------------------------
IMPORTANT SAFETY NOTICE
------------------------------------------------------------

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
============================================================
"""

    st.download_button(

        label="📥 DOWNLOAD AI CLINICAL REPORT",

        data=report_content,

        file_name=(
            f"MEDICOGNITIVE_AI_"
            f"{patient_id}.txt"
        ),

        mime="text/plain"

    )


# =========================================================
# PREMIUM FOOTER
# =========================================================

st.markdown(
    """
    <div class="premium-footer">

        <div class="footer-brand">
            🩺 MEDICOGNITIVE AI
        </div>

        <b style="color:#83aaa9;">
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

        <span style="color:#3f5d68;">
            Research Prototype • Clinical Validation Required
        </span>

    </div>
    """,
    unsafe_allow_html=True
)

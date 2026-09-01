```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from PIL import Image
import io

from clinical_model import clinical_risk_assessment


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MEDICOGNITIVE AI — Dr. Omnia Ali",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# PREMIUM MEDICAL DESIGN
# =========================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Tajawal:wght@300;400;500;700;800;900&family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --gold: #D4AF37;
    --gold-light: #FFF099;
    --gold-dark: #AA7C11;
    --gold-soft: #E7C95C;
    --black: #030303;
    --black2: #090909;
}

html {
    scroll-behavior: smooth;
}

html, body, [class*="css"] {
    font-family: "Tajawal", "Inter", Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 50% 5%, rgba(212,175,55,0.13), transparent 30%),
        radial-gradient(circle at 0% 70%, rgba(212,175,55,0.06), transparent 28%),
        radial-gradient(circle at 100% 85%, rgba(170,124,17,0.07), transparent 30%),
        linear-gradient(145deg, #020202 0%, #080808 50%, #020202 100%);
    color: white;
    min-height: 100vh;
}

.main .block-container {
    max-width: 1550px;
    padding: 2rem 2.5rem 4rem 2.5rem;
}

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #030303;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #D4AF37, #80600E);
    border-radius: 20px;
}


/* NAVBAR */

.luxury-nav {
    position: relative;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 25px;
    padding: 18px 28px;
    margin-bottom: 28px;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(18,18,18,.95), rgba(5,5,5,.95));
    border: 1px solid rgba(212,175,55,.25);
    box-shadow:
        0 20px 55px rgba(0,0,0,.55),
        inset 0 1px 0 rgba(255,255,255,.04);
    backdrop-filter: blur(18px);
}

.luxury-logo {
    font-family: "Cinzel", serif;
    font-size: 25px;
    font-weight: 900;
    letter-spacing: 2px;
    color: #D4AF37;
}

.luxury-nav-links {
    display: flex;
    gap: 28px;
    color: #aaa;
    font-size: 14px;
    font-weight: 500;
}

.luxury-nav-links span:hover {
    color: #FFF099;
}

.vip-badge {
    padding: 9px 20px;
    border-radius: 30px;
    background: linear-gradient(135deg, #D4AF37, #AA7C11);
    color: #050505;
    font-weight: 900;
    font-size: 13px;
}


/* HERO */

.premium-hero {
    position: relative;
    z-index: 1;
    min-height: 390px;
    padding: 55px 50px;
    margin-bottom: 30px;
    border-radius: 32px;
    overflow: hidden;
    text-align: center;
    background:
        radial-gradient(circle at 50% 20%, rgba(212,175,55,.12), transparent 35%),
        linear-gradient(145deg, rgba(18,18,18,.97), rgba(3,3,3,.98));
    border: 1px solid rgba(212,175,55,.30);
    box-shadow:
        0 35px 90px rgba(0,0,0,.62),
        0 0 80px rgba(212,175,55,.05),
        inset 0 1px 0 rgba(255,255,255,.05);
    animation: heroAppear 1s ease-out;
}

@keyframes heroAppear {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.hero-medical-symbol {
    width: 86px;
    height: 86px;
    margin: 0 auto 22px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(212,175,55,.18), rgba(212,175,55,.03));
    border: 1px solid rgba(212,175,55,.45);
    box-shadow:
        0 0 35px rgba(212,175,55,.16),
        inset 0 0 25px rgba(212,175,55,.06);
    font-size: 42px;
    animation: doctorFloat 4s infinite ease-in-out;
}

@keyframes doctorFloat {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-8px);
    }
}

.hero-subtitle {
    color: #D4AF37;
    font-size: 14px;
    letter-spacing: 4px;
    font-weight: 700;
    margin-bottom: 14px;
}

.hero-brand {
    font-family: "Cinzel", serif;
    font-size: 50px;
    font-weight: 900;
    letter-spacing: 4px;
    line-height: 1.1;
    color: #E7C95C;
}

.hero-description {
    margin-top: 15px;
    color: #888;
    font-size: 14px;
    letter-spacing: 2px;
}

.doctor-name {
    margin-top: 28px;
    font-size: 29px;
    font-weight: 700;
    color: #fff;
}

.doctor-title {
    margin-top: 7px;
    color: #C6A83E;
    font-size: 12px;
    letter-spacing: 2px;
}

.system-status {
    display: inline-block;
    margin-top: 22px;
    padding: 10px 20px;
    border-radius: 30px;
    background: rgba(212,175,55,.06);
    border: 1px solid rgba(212,175,55,.22);
    color: #DCC36B;
    font-size: 11px;
    font-weight: 700;
}

.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    margin-left: 7px;
    border-radius: 50%;
    background: #D4AF37;
    box-shadow: 0 0 12px #D4AF37;
    animation: statusPulse 1.8s infinite;
}

@keyframes statusPulse {
    0%, 100% {
        opacity: 1;
        transform: scale(1);
    }
    50% {
        opacity: .35;
        transform: scale(.75);
    }
}


/* SECTION */

.section-heading {
    position: relative;
    z-index: 1;
    margin-top: 30px;
    margin-bottom: 18px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(212,175,55,.12);
    color: #fff;
    font-size: 24px;
    font-weight: 800;
}

.section-heading span {
    color: #D4AF37;
    font-size: 13px;
    letter-spacing: 2px;
    margin-left: 10px;
}

.ai-banner {
    padding: 17px 21px;
    margin: 14px 0 22px 0;
    border-radius: 16px;
    background: linear-gradient(
        90deg,
        rgba(212,175,55,.09),
        rgba(170,124,17,.05),
        rgba(255,255,255,.015)
    );
    border: 1px solid rgba(212,175,55,.18);
    color: #D9C77C;
}


/* FEATURES */

.feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 30px;
}

.feature-card {
    position: relative;
    overflow: hidden;
    padding: 30px 24px;
    min-height: 190px;
    border-radius: 20px;
    text-align: center;
    background: linear-gradient(145deg, rgba(24,24,24,.86), rgba(6,6,6,.95));
    border: 1px solid rgba(212,175,55,.16);
    box-shadow: 0 18px 45px rgba(0,0,0,.4);
    transition: all .35s ease;
}

.feature-card:hover {
    transform: translateY(-7px);
    border-color: rgba(212,175,55,.5);
    box-shadow:
        0 25px 60px rgba(0,0,0,.55),
        0 0 30px rgba(212,175,55,.08);
}

.feature-icon {
    font-size: 34px;
    margin-bottom: 14px;
    color: #D4AF37;
}

.feature-title {
    font-size: 18px;
    font-weight: 800;
    color: #fff;
    margin-bottom: 9px;
}

.feature-text {
    color: #777;
    font-size: 13px;
    line-height: 1.8;
}


/* CARDS */

.glass-card {
    background: linear-gradient(145deg, rgba(22,22,22,.88), rgba(5,5,5,.96));
    border: 1px solid rgba(212,175,55,.13);
    border-radius: 20px;
    padding: 23px;
    margin-bottom: 18px;
    box-shadow: 0 18px 45px rgba(0,0,0,.35);
}

.vital-card {
    position: relative;
    overflow: hidden;
    min-height: 145px;
    padding: 23px;
    border-radius: 21px;
    background: linear-gradient(145deg, rgba(24,24,24,.95), rgba(5,5,5,.97));
    border: 1px solid rgba(212,175,55,.16);
    box-shadow: 0 14px 35px rgba(0,0,0,.32);
}

.vital-label {
    color: #8C7A43;
    font-size: 10px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.vital-value {
    margin-top: 9px;
    font-size: 34px;
    font-weight: 900;
    color: #F9F3D4;
}

.vital-unit {
    margin-top: 5px;
    color: #666;
    font-size: 11px;
}


/* RISK */

.risk-panel {
    position: relative;
    overflow: hidden;
    padding: 38px 25px;
    border-radius: 27px;
    text-align: center;
    background:
        radial-gradient(
            circle at center,
            rgba(212,175,55,.12),
            rgba(4,4,4,.98) 65%
        );
    border: 1px solid rgba(212,175,55,.25);
    box-shadow: 0 25px 70px rgba(0,0,0,.5);
}

.risk-number {
    position: relative;
    font-size: 76px;
    font-weight: 900;
    line-height: 1;
    color: #D4AF37;
}

.risk-label {
    margin-top: 12px;
    color: #80744D;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 3px;
}


/* INPUTS */

.stTextInput input,
.stNumberInput input {
    background: rgba(10,10,10,.92) !important;
    color: #F8F1D1 !important;
    border: 1px solid rgba(212,175,55,.18) !important;
    border-radius: 12px !important;
}

.stSelectbox > div > div {
    background: rgba(10,10,10,.92) !important;
    border-radius: 12px !important;
    border-color: rgba(212,175,55,.18) !important;
}

label {
    color: #C8B974 !important;
    font-weight: 600 !important;
}


/* BUTTON */

.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 13px;
    border: 1px solid rgba(212,175,55,.35);
    background: linear-gradient(135deg, #D4AF37, #AA7C11);
    color: #080808;
    font-weight: 900;
    letter-spacing: .5px;
    box-shadow: 0 8px 25px rgba(212,175,55,.12);
    transition: .25s;
}

.stButton > button:hover {
    transform: translateY(-3px);
    border-color: #FFF099;
    box-shadow: 0 12px 35px rgba(212,175,55,.25);
}


/* TABS */

.stTabs [data-baseweb="tab-list"] {
    gap: 7px;
    padding: 7px;
    border-radius: 18px;
    background: rgba(5,5,5,.85);
    border: 1px solid rgba(212,175,55,.12);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 13px;
    padding: 12px 21px;
    color: #756E5A;
    font-weight: 800;
}

.stTabs [aria-selected="true"] {
    background: rgba(212,175,55,.14);
    color: #F1D96D !important;
}


/* UPLOADER */

[data-testid="stFileUploader"] {
    background: rgba(8,8,8,.72);
    border-radius: 18px;
    padding: 8px;
    border: 1px dashed rgba(212,175,55,.25);
}


/* FOOTER */

.premium-footer {
    text-align: center;
    margin-top: 60px;
    padding: 35px 20px;
    border-top: 1px solid rgba(212,175,55,.12);
    color: #555;
    font-size: 11px;
}

.footer-brand {
    font-family: "Cinzel", serif;
    color: #D4AF37;
    font-size: 16px;
    font-weight: 900;
    letter-spacing: 2px;
    margin-bottom: 9px;
}


/* MOBILE */

@media (max-width: 900px) {

    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .luxury-nav {
        flex-direction: column;
        text-align: center;
    }

    .luxury-nav-links {
        display: none;
    }

    .premium-hero {
        padding: 40px 20px;
    }

    .hero-brand {
        font-size: 31px;
        letter-spacing: 2px;
    }

    .feature-grid {
        grid-template-columns: 1fr;
    }

    .risk-number {
        font-size: 58px;
    }
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# NAVIGATION
# =========================================================

st.markdown(
    """
<div class="luxury-nav">
    <div class="luxury-logo">Dr. Omnia Ali</div>

    <div class="luxury-nav-links">
        <span>الرئيسية</span>
        <span>عن الدكتورة</span>
        <span>الخدمات الطبية</span>
        <span>الذكاء الاصطناعي</span>
    </div>

    <div class="vip-badge">✦ VIP MEDICAL AI</div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
<div class="premium-hero">

    <div class="hero-medical-symbol">🩺</div>

    <div class="hero-subtitle">
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

    <div class="system-status">
        <span class="status-dot"></span>
        AI SYSTEM ONLINE
        &nbsp; • &nbsp;
        CLINICAL ENGINE ACTIVE
    </div>

</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# FEATURES
# =========================================================

st.markdown(
    """
<div class="feature-grid">

    <div class="feature-card">
        <div class="feature-icon">♛</div>
        <div class="feature-title">رعاية VIP خاصة</div>
        <div class="feature-text">
            تجربة طبية متقدمة تجمع الخصوصية والدقة وأحدث تقنيات الذكاء الاصطناعي.
        </div>
    </div>

    <div class="feature-card">
        <div class="feature-icon">⚕</div>
        <div class="feature-title">تشخيص ذكي</div>
        <div class="feature-text">
            تحليل متعدد الأبعاد للبيانات السريرية والمؤشرات الحيوية ضمن منصة واحدة.
        </div>
    </div>

    <div class="feature-card">
        <div class="feature-icon">✦</div>
        <div class="feature-title">Clinical Intelligence</div>
        <div class="feature-text">
            منصة بحثية متقدمة لدعم القرار السريري وتحليل المخاطر والاتجاهات الزمنية.
        </div>
    </div>

</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "👤 PATIENT PROFILE",
        "📈 CLINICAL TRENDS",
        "👁️ AI VISION",
        "🧠 AI RISK INTELLIGENCE",
    ]
)


# =========================================================
# TAB 1 — PATIENT PROFILE
# =========================================================

with tab1:

    st.markdown(
        '<div class="section-heading"><span>01</span> 👤 Patient Clinical Profile</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="ai-banner">✦ Clinical intelligence interface ready — enter patient parameters to activate analysis.</div>',
        unsafe_allow_html=True,
    )

    patient_id = st.text_input(
        "Patient Identification Number",
        value="MC-10482",
        disabled=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input(
            "Age (Years)",
            min_value=1,
            max_value=120,
            value=62,
        )

        sex = st.selectbox(
            "Sex",
            ["Male", "Female"],
        )

        spo2 = st.slider(
            "Oxygen Saturation — SpO₂ (%)",
            min_value=50,
            max_value=100,
            value=91,
        )

        hr = st.number_input(
            "Heart Rate (bpm)",
            min_value=30,
            max_value=220,
            value=112,
        )

    with col2:

        temp = st.number_input(
            "Body Temperature (°C)",
            min_value=30.0,
            max_value=45.0,
            value=38.9,
            step=0.1,
        )

        rr = st.number_input(
            "Respiratory Rate (/min)",
            min_value=5,
            max_value=60,
            value=25,
        )

        crp = st.number_input(
            "C-Reactive Protein — CRP (mg/L)",
            min_value=0.0,
            max_value=300.0,
            value=45.0,
            step=0.5,
        )

        wbc = st.number_input(
            "White Blood Cell Count — WBC (k/µL)",
            min_value=0.0,
            max_value=50.0,
            value=14.5,
            step=0.1,
        )


    # =====================================================
    # LIVE PARAMETERS
    # =====================================================

    st.markdown(
        '<div class="section-heading"><span>LIVE</span> 📡 Live Clinical Parameters</div>',
        unsafe_allow_html=True,
    )

    v1, v2, v3, v4 = st.columns(4)

    with v1:
        st.markdown(
            f"""
            <div class="vital-card">
                <div class="vital-label">Oxygen Saturation</div>
                <div class="vital-value">{spo2}%</div>
                <div class="vital-unit">SpO₂</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with v2:
        st.markdown(
            f"""
            <div class="vital-card">
                <div class="vital-label">Heart Rate</div>
                <div class="vital-value">{hr}</div>
                <div class="vital-unit">Beats / Minute</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with v3:
        st.markdown(
            f"""
            <div class="vital-card">
                <div class="vital-label">Temperature</div>
                <div class="vital-value">{temp:.1f}</div>
                <div class="vital-unit">° Celsius</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with v4:
        st.markdown(
            f"""
            <div class="vital-card">
                <div class="vital-label">Respiratory Rate</div>
                <div class="vital-value">{rr}</div>
                <div class="vital-unit">Breaths / Minute</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# TAB 2 — CLINICAL TRENDS
# =========================================================

with tab2:

    st.markdown(
        '<div class="section-heading"><span>02</span> 📈 Longitudinal Clinical Intelligence</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="ai-banner">◈ Temporal AI engine — tracking physiological trajectory and deterioration patterns.</div>',
        unsafe_allow_html=True,
    )

    dates = [
        datetime.now() - timedelta(days=i)
        for i in range(6, -1, -1)
    ]

    dates_str = [
        d.strftime("%b %d")
        for d in dates
    ]

    mock_spo2 = [98, 97, 96, 94, 93, 92, spo2]
    mock_temp = [36.6, 36.9, 37.2, 37.8, 38.2, 38.6, temp]
    mock_hr = [70, 75, 82, 90, 98, 105, hr]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=dates_str,
            y=mock_spo2,
            mode="lines+markers",
            name="SpO₂ (%)",
            line=dict(
                color="#D4AF37",
                width=4,
            ),
            marker=dict(size=8),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=dates_str,
            y=mock_hr,
            mode="lines+markers",
            name="Heart Rate (bpm)",
            line=dict(
                color="#AA7C11",
                width=2,
                dash="dot",
            ),
            marker=dict(size=6),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=dates_str,
            y=mock_temp,
            mode="lines+markers",
            name="Temperature (°C)",
            yaxis="y2",
            line=dict(
                color="#E7C95C",
                width=3,
                dash="dash",
            ),
            marker=dict(size=6),
        )
    )

    # IMPORTANT:
    # Plotly sometimes rejects old/invalid layout properties.
    # This layout only uses supported properties.

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(10,10,10,0.5)",
        font=dict(
            color="#D9C77C",
            family="Tajawal, Arial",
        ),
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=30,
        ),
        height=500,

        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(212,175,55,0.10)",
            zeroline=False,
            tickfont=dict(
                color="#D4AF37",
            ),
        ),

        yaxis=dict(
            title=dict(
                text="SpO₂ / Heart Rate",
                font=dict(
                    color="#D4AF37",
                ),
            ),
            showgrid=True,
            gridcolor="rgba(212,175,55,0.10)",
            tickfont=dict(
                color="#D4AF37",
            ),
            zeroline=False,
        ),

        yaxis2=dict(
            title=dict(
                text="Temperature (°C)",
                font=dict(
                    color="#E7C95C",
                ),
            ),
            overlaying="y",
            side="right",
            showgrid=False,
            tickfont=dict(
                color="#E7C95C",
            ),
            zeroline=False,
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(
                color="#D9C77C",
            ),
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# =========================================================
# TAB 3 — AI VISION
# =========================================================

with tab3:

    st.markdown(
        '<div class="section-heading"><span>03</span> 👁️ Medical Imaging & Diagnostics</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="ai-banner">✦ Computer Vision Diagnostic Interface — Upload an image for visualization and analysis workflow.</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload Medical Image",
        type=["jpg", "jpeg", "png"],
    )

    if uploaded_file is not None:

        col_img, col_diag = st.columns(2)

        with col_img:

            try:

                image = Image.open(uploaded_file)

                st.image(
                    image,
                    caption="Uploaded Clinical Image",
                    use_container_width=True,
                )

            except Exception:
                st.error(
                    "Unable to read this image file."
                )

        with col_diag:

            st.markdown(
                """
                <div class="glass-card">

                    <h3 style="color:#D4AF37;margin-top:0;">
                        AI Imaging Diagnostics
                    </h3>

                    <p style="color:#ccc;">
                        <strong>Analysis Status:</strong>
                        Image received successfully.
                    </p>

                    <p style="color:#ccc;">
                        <strong>Processing Mode:</strong>
                        Computer Vision Pipeline
                    </p>

                    <p style="color:#ccc;">
                        <strong>Clinical Note:</strong>
                        This interface is a research/demo visualization and
                        does not independently establish a medical diagnosis.
                    </p>

                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button("GENERATE IMAGING REPORT"):

                st.info(
                    "Imaging report workflow activated. "
                    "A validated medical imaging model/API can be connected here."
                )

    else:

        st.markdown(
            """
            <div class="glass-card" style="text-align:center;">
                <div style="font-size:45px;">👁️</div>
                <h3 style="color:#D4AF37;">
                    AI Vision Ready
                </h3>
                <p style="color:#777;">
                    Upload a JPG, JPEG, or PNG medical image to begin.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# TAB 4 — AI RISK INTELLIGENCE
# =========================================================

with tab4:

    st.markdown(
        '<div class="section-heading"><span>04</span> 🧠 AI Risk Intelligence Engine</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="ai-banner">
            ✦ Clinical Risk Engine — combines entered physiological and laboratory
            parameters into a transparent research-oriented risk score.
        </div>
        """,
        unsafe_allow_html=True,
    )

    run_assessment = st.button(
        "RUN CLINICAL RISK ASSESSMENT",
        key="run_risk_assessment",
    )

    if run_assessment:

        inputs = {
            "age": float(age),
            "sex": sex,
            "spo2": float(spo2),
            "hr": float(hr),
            "temp": float(temp),
            "rr": float(rr),
            "crp": float(crp),
            "wbc": float(wbc),
        }

        try:

            result = clinical_risk_assessment(inputs)

            risk_score = float(result[0])
            risk_level = str(result[1])
            recommendations = result[2]

            risk_score = max(
                0.0,
                min(100.0, risk_score)
            )

            if not isinstance(
                recommendations,
                (list, tuple)
            ):
                recommendations = [
                    str(recommendations)
                ]

            r_col1, r_col2 = st.columns(
                [1, 2]
            )

            with r_col1:

                st.markdown(
                    f"""
                    <div class="risk-panel">

                        <div class="risk-number">
                            {risk_score:.0f}%
                        </div>

                        <div class="risk-label">
                            {risk_level.upper()} RISK
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with r_col2:

                recs_html = "".join(
                    [
                        f"<li>{str(rec)}</li>"
                        for rec in recommendations
                    ]
                )

                st.markdown(
                    f"""
                    <div class="glass-card">

                        <h3 style="color:#D4AF37;margin-top:0;">
                            Clinical Decision Guidance
                        </h3>

                        <ul style="
                            color:#ddd;
                            line-height:1.9;
                        ">
                            {recs_html}
                        </ul>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.caption(
                "Research/demo output only. "
                "This score is not a substitute for professional medical assessment."
            )

        except Exception as exc:

            st.error(
                "The clinical risk engine could not complete the calculation."
            )

            st.exception(exc)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<div class="premium-footer">

    <div class="footer-brand">
        MEDICOGNITIVE AI
    </div>

    <div>
        Developed for Clinical Excellence & AI Research
        • Dr. Omnia Ali
    </div>

    <div style="margin-top:5px;color:#444;">
        © 2026 All Rights Reserved
    </div>

</div>
""",
    unsafe_allow_html=True,
)
```

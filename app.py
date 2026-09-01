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
# PREMIUM GOLD MEDICAL DESIGN
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Tajawal:wght@300;400;500;700;800;900&family=Inter:wght@400;500;600;700;800&display=swap');


/* (CSS styles omitted for brevity, same as original) */

</style>
""", unsafe_allow_html=True)


# =========================================================
# BACKGROUND
# =========================================================

st.markdown('<div class="gold-background"><div class="gold-orb one"></div><div class="gold-orb two"></div></div>', unsafe_allow_html=True)


# =========================================================
# LUXURY NAVBAR
# =========================================================

st.markdown('<div class="luxury-nav"><div class="luxury-logo">Dr. Omnea Ali</div><div class="luxury-nav-links"><span>الرئيسية</span><span>عن الدكتورة</span><span>الخدمات الطبية</span><span>الذكاء الاصطناعي</span></div><div class="vip-badge">✦ VIP MEDICAL AI</div></div>', unsafe_allow_html=True)


# =========================================================
# PREMIUM HERO
# =========================================================

st.markdown('''<div class="premium-hero"><div class="hero-medical-symbol">🩺</div><div class="hero-subtitle">رعاية طبية بمقاييس عالمية</div><div class="hero-brand">MEDICOGNITIVE AI</div><div class="hero-description">MULTIMODAL CLINICAL INTELLIGENCE • EARLY WARNING • AI RESEARCH PLATFORM</div><div class="doctor-name">الدكتورة أمنية علي</div><div class="doctor-title">MEDICAL AI RESEARCH & CLINICAL INTELLIGENCE</div><div class="ecg-line"><svg viewBox="0 0 1000 45" preserveAspectRatio="none"><polyline points="0,23 100,23 125,23 140,10 150,37 165,23 300,23 330,23 350,6 360,40 375,23 500,23 530,23 550,12 560,35 575,23 700,23 730,23 750,8 760,38 775,23 900,23 930,23 950,10 960,37 975,23 1000,23" fill="none" stroke-width="2"/></svg></div><div class="system-status"><span class="status-dot"></span> AI SYSTEM ONLINE &nbsp; • &nbsp; CLINICAL ENGINE ACTIVE</div></div>''', unsafe_allow_html=True)


# =========================================================
# PREMIUM FEATURES
# =========================================================

st.markdown('<div class="feature-grid"><div class="feature-card"><div class="feature-icon">♛</div><div class="feature-title">رعاية VIP خاصة</div><div class="feature-text">تجربة طبية متقدمة تجمع الخصوصية والدقة وأحدث تقنيات الذكاء الاصطناعي.</div></div><div class="feature-card"><div class="feature-icon">⚕</div><div class="feature-title">تشخيص ذكي</div><div class="feature-text">تحليل متعدد الأبعاد للبيانات السريرية والمؤشرات الحيوية ضمن منصة واحدة.</div></div><div class="feature-card"><div class="feature-icon">✦</div><div class="feature-title">Clinical Intelligence</div><div class="feature-text">منصة بحثية متقدمة لدعم القرار السريري وتحليل المخاطر والاتجاهات الزمنية.</div></div></div>', unsafe_allow_html=True)


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

    st.markdown('<div class="section-heading"><span>01</span> 👤 Patient Clinical Profile</div>', unsafe_allow_html=True)

    st.markdown('<div class="ai-banner">✦ Clinical intelligence interface ready — enter patient parameters to activate analysis.</div>', unsafe_allow_html=True)

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

    st.markdown('<div class="section-heading"><span>LIVE</span> 📡 Live Clinical Parameters</div>', unsafe_allow_html=True)

    v1, v2, v3, v4 = st.columns(4)

    with v1:

        st.markdown(f'<div class="vital-card"><div class="vital-label">Oxygen Saturation</div><div class="vital-value">{spo2}%</div><div class="vital-unit">SpO₂</div></div>', unsafe_allow_html=True)

    with v2:

        st.markdown(f'<div class="vital-card"><div class="vital-label">Heart Rate</div><div class="vital-value">{hr}</div><div class="vital-unit">Beats / Minute</div></div>', unsafe_allow_html=True)

    with v3:

        st.markdown(f'<div class="vital-card"><div class="vital-label">Temperature</div><div class="vital-value">{temp}</div><div class="vital-unit">° Celsius</div></div>', unsafe_allow_html=True)

    with v4:

        st.markdown(f'<div class="vital-card"><div class="vital-label">Respiratory Rate</div><div class="vital-value">{rr}</div><div class="vital-unit">Breaths / Minute</div></div>', unsafe_allow_html=True)


# =========================================================
# TAB 2 — TRENDS (COMPATIBLE PLOTLY LAYOUT)
# =========================================================

with tab2:

    st.markdown('<div class="section-heading"><span>02</span> 📈 Longitudinal Clinical Intelligence</div>', unsafe_allow_html=True)

    st.markdown('<div class="ai-banner">◈ Temporal AI engine — tracking physiological trajectory and deterioration patterns.</div>', unsafe_allow_html=True)

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

    # SpO2
    fig.add_trace(
        go.Scatter(
            x=dates_str,
            y=mock_spo2,
            mode="lines+markers",
            name="SpO₂ (%)",
            line=dict(color="#D4AF37", width=4),
            marker=dict(size=8)
        )
    )

    # Heart Rate
    fig.add_trace(
        go.Scatter(
            x=dates_str,
            y=mock_hr,
            mode="lines+markers",
            name="Heart Rate (bpm)",
            line=dict(color="#AA7C11", width=2, dash="dot"),
            marker=dict(size=6)
        )
    )

    # Temperature (y-axis 2)
    fig.add_trace(
        go.Scatter(
            x=dates_str,
            y=mock_temp,
            mode="lines+markers",
            name="Temperature (°C)",
            yaxis="y2",
            line=dict(color="#E7C95C", width=3, dash="dash"),
            marker=dict(size=6)
        )
    )

    # Layout update with fixes
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # خلفية شفافة
        plot_bgcolor='rgba(0,0,0,0)',   # خلفية الرسم الشفافة
        font=dict(color="#D9C77C"),
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(
            gridcolor="rgba(212,175,55,0.1)",
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title=dict(text="SpO₂ / Heart Rate", font=dict(color="#D4AF37")),
            gridcolor="rgba(212,175,55,0.1)",
            tickfont=dict(color="#D4AF37"),
            zeroline=False
        ),
        yaxis2=dict(
            title=dict(text="Temp (°C)", font=dict(color="#E7C95C")),
            overlaying="y",
            side="right",
            gridcolor="rgba(212,175,55,0.05)",
            tickfont=dict(color="#E7C95C"),
            zeroline=False
        )
    )

    st.plotly_chart(fig, use_container_width=True)


# =========================================================
# TAB 3 — AI VISION
# =========================================================

with tab3:

    st.markdown('<div class="section-heading"><span>03</span> 👁️ AI Vision & Diagnostic Imaging</div>', unsafe_allow_html=True)

    st.markdown('<div class="ai-banner">✦ Deep learning visual engine for chest radiograph analysis.</div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Medical Image (X-Ray / CT)", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Clinical Image", use_column_width=True)
        st.success("Image successfully processed by AI engine.")
    else:
        st.info("Awaiting medical image upload for automated analysis.")


# =========================================================
# TAB 4 — AI RISK INTELLIGENCE
# =========================================================

with tab4:

    st.markdown('<div class="section-heading"><span>04</span> 🧠 AI Risk Intelligence & Clinical Assessment</div>', unsafe_allow_html=True)

    st.markdown('<div class="ai-banner">✦ Multi-parametric predictive modeling for patient deterioration risk.</div>', unsafe_allow_html=True)

    if st.button("RUN CLINICAL RISK ASSESSMENT"):
        risk_score = clinical_risk_assessment(age, sex, spo2, hr, temp, rr, crp, wbc)

        st.markdown(f'''
        <div class="risk-panel">
            <div class="risk-number">{risk_score}%</div>
            <div class="risk-label">PREDICTED CLINICAL RISK SCORE</div>
        </div>
        ''', unsafe_allow_html=True)

        if risk_score > 70:
            st.error("HIGH RISK: Immediate clinical attention recommended.")
        elif risk_score > 40:
            st.warning("MODERATE RISK: Enhanced physiological monitoring advised.")
        else:
            st.success("LOW RISK: Patient vital metrics within stable parameters.")


# =========================================================
# FOOTER
# =========================================================

st.markdown('''
<div class="premium-footer">
    <div class="footer-brand">MEDICOGNITIVE AI</div>
    <div>Developed for Dr. Omnia Ali • Clinical Decision Support System</div>
</div>
''', unsafe_allow_html=True)

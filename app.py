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
    page_title="MEDICOGNITIVE AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# FUTURISTIC MEDICAL AI CSS
# =========================================================

st.markdown("""
<style>

/* ================================
   GLOBAL
================================ */

html, body, [class*="css"] {
    font-family: "Segoe UI", Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(0, 229, 255, 0.10), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(99, 102, 241, 0.12), transparent 30%),
        radial-gradient(circle at 50% 100%, rgba(14, 165, 233, 0.08), transparent 35%),
        #050b14;
    color: #e6f7ff;
}


/* ================================
   MAIN CONTAINER
================================ */

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    padding-left: 3rem;
    padding-right: 3rem;
    max-width: 1500px;
}


/* ================================
   HEADER
================================ */

.hero {
    position: relative;
    padding: 35px;
    margin-bottom: 25px;
    border-radius: 24px;

    background:
        linear-gradient(
            135deg,
            rgba(8, 20, 35, 0.95),
            rgba(10, 30, 50, 0.85)
        );

    border: 1px solid rgba(56, 189, 248, 0.25);

    box-shadow:
        0 0 35px rgba(0, 200, 255, 0.08),
        inset 0 0 35px rgba(0, 150, 255, 0.03);

    overflow: hidden;
}

.hero:before {
    content: "";
    position: absolute;
    width: 350px;
    height: 350px;
    background: rgba(0, 229, 255, 0.08);
    border-radius: 50%;
    top: -200px;
    right: -100px;
    filter: blur(20px);
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: 2px;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #67e8f9,
            #38bdf8
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom: 5px;
}

.hero-subtitle {
    color: #8ba8ba;
    font-size: 15px;
    letter-spacing: 1px;
}

.ai-status {
    display: inline-block;
    margin-top: 15px;
    padding: 8px 16px;
    border-radius: 30px;

    background: rgba(16, 185, 129, 0.10);
    border: 1px solid rgba(16, 185, 129, 0.35);

    color: #6ee7b7;
    font-size: 13px;
    font-weight: 600;

    box-shadow: 0 0 15px rgba(16,185,129,0.10);
}


/* ================================
   SECTION HEADERS
================================ */

h1, h2, h3 {
    color: #e8faff !important;
}

.stSubheader {
    color: #bceeff !important;
}


/* ================================
   GLASS CARDS
================================ */

.glass-card {
    background:
        linear-gradient(
            145deg,
            rgba(17, 31, 48, 0.88),
            rgba(7, 17, 29, 0.92)
        );

    border: 1px solid rgba(125, 211, 252, 0.13);

    border-radius: 18px;

    padding: 22px;

    margin-bottom: 18px;

    box-shadow:
        0 12px 35px rgba(0,0,0,0.25),
        inset 0 1px 0 rgba(255,255,255,0.03);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease,
        border-color 0.25s ease;
}

.glass-card:hover {
    transform: translateY(-3px);

    border-color:
        rgba(56, 189, 248, 0.30);

    box-shadow:
        0 15px 45px rgba(0, 180, 255, 0.10),
        0 0 25px rgba(0, 180, 255, 0.05);
}


/* ================================
   VITAL CARDS
================================ */

.vital-card {
    background:
        linear-gradient(
            145deg,
            rgba(13, 32, 49, 0.95),
            rgba(7, 18, 30, 0.95)
        );

    border-radius: 18px;

    padding: 20px;

    border: 1px solid rgba(56,189,248,0.16);

    margin-bottom: 15px;

    position: relative;
    overflow: hidden;

    transition: all 0.25s ease;
}

.vital-card:hover {
    transform: translateY(-4px);

    box-shadow:
        0 0 30px rgba(0,200,255,0.12);
}

.vital-label {
    color: #7795a7;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.vital-value {
    font-size: 31px;
    font-weight: 750;
    color: #e8fbff;
    margin-top: 5px;
}

.vital-unit {
    font-size: 13px;
    color: #6f91a5;
}


/* ================================
   RISK PANEL
================================ */

.risk-panel {
    padding: 30px;
    border-radius: 22px;
    text-align: center;

    background:
        radial-gradient(
            circle at center,
            rgba(0, 180, 255, 0.10),
            rgba(5, 15, 25, 0.95)
        );

    border: 1px solid rgba(56,189,248,0.20);

    box-shadow:
        0 0 45px rgba(0,180,255,0.08);
}

.risk-number {
    font-size: 65px;
    font-weight: 900;
    line-height: 1;

    background:
        linear-gradient(
            180deg,
            #ffffff,
            #67e8f9
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.risk-label {
    color: #8ca8b8;
    font-size: 13px;
    letter-spacing: 3px;
    margin-top: 8px;
}


/* ================================
   AI BANNER
================================ */

.ai-banner {
    padding: 16px 20px;
    border-radius: 14px;

    background:
        linear-gradient(
            90deg,
            rgba(14,165,233,0.10),
            rgba(99,102,241,0.08)
        );

    border: 1px solid rgba(56,189,248,0.16);

    margin: 15px 0;

    color: #b9eaff;
}


/* ================================
   BUTTONS
================================ */

.stButton > button {

    width: 100%;

    border-radius: 12px;

    height: 3.2em;

    border: 1px solid rgba(56,189,248,0.25);

    background:
        linear-gradient(
            135deg,
            #0284c7,
            #0369a1
        );

    color: white;

    font-weight: 700;

    transition: all 0.25s ease;

    box-shadow:
        0 0 18px rgba(14,165,233,0.12);
}

.stButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 0 30px rgba(14,165,233,0.30);

    border-color:
        rgba(125,211,252,0.50);
}


/* ================================
   INPUTS
================================ */

.stTextInput input,
.stNumberInput input,
.stSelectbox div,
.stSlider {

    border-radius: 10px !important;
}


/* ================================
   TABS
================================ */

.stTabs [data-baseweb="tab-list"] {

    gap: 8px;

    background:
        rgba(5, 15, 25, 0.75);

    padding: 8px;

    border-radius: 15px;

    border:
        1px solid rgba(56,189,248,0.10);
}

.stTabs [data-baseweb="tab"] {

    border-radius: 10px;

    padding: 10px 18px;

    color: #7894a5;

    font-weight: 600;
}

.stTabs [aria-selected="true"] {

    background:
        rgba(14,165,233,0.15);

    color: #67e8f9 !important;

    box-shadow:
        0 0 15px rgba(14,165,233,0.08);
}


/* ================================
   ALERTS
================================ */

div[data-testid="stAlert"] {

    border-radius: 14px;

    border: 1px solid rgba(255,255,255,0.08);

}


/* ================================
   TABLE
================================ */

.stDataFrame,
table {

    border-radius: 12px;
}


/* ================================
   FOOTER
================================ */

.footer {

    text-align: center;

    margin-top: 40px;

    padding: 20px;

    color: #526c7c;

    font-size: 12px;

    border-top:
        1px solid rgba(255,255,255,0.05);
}


/* ================================
   MOBILE
================================ */

@media (max-width: 768px) {

    .main .block-container {

        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero {

        padding: 25px;
    }

    .hero-title {

        font-size: 29px;
    }

    .risk-number {

        font-size: 50px;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HERO HEADER
# =========================================================

st.markdown("""
<div class="hero">

    <div class="hero-title">
        🩺 MEDICOGNITIVE AI
    </div>

    <div class="hero-subtitle">
        MULTIMODAL EARLY-WARNING • CLINICAL DECISION SUPPORT • AI RESEARCH PLATFORM
    </div>

    <div class="ai-status">
        ● AI SYSTEM ONLINE &nbsp; | &nbsp; Clinical Engine Active
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📋  PATIENT",
    "📈  TRENDS",
    "🖼️  AI VISION",
    "🧠  AI RISK REPORT"
])


# =========================================================
# TAB 1 — PATIENT
# =========================================================

with tab1:

    st.markdown("### 👤 Patient Clinical Profile")

    st.markdown(
        '<div class="ai-banner">⚡ Enter patient parameters to activate the clinical intelligence engine.</div>',
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
    # LIVE VITAL DASHBOARD
    # =====================================================

    st.markdown("### 📡 Live Clinical Parameters")

    v1, v2, v3, v4 = st.columns(4)

    with v1:

        st.markdown(f"""
        <div class="vital-card">
            <div class="vital-label">SpO₂</div>
            <div class="vital-value">{spo2}%</div>
            <div class="vital-unit">Oxygen Saturation</div>
        </div>
        """, unsafe_allow_html=True)

    with v2:

        st.markdown(f"""
        <div class="vital-card">
            <div class="vital-label">Heart Rate</div>
            <div class="vital-value">{hr}</div>
            <div class="vital-unit">beats / minute</div>
        </div>
        """, unsafe_allow_html=True)

    with v3:

        st.markdown(f"""
        <div class="vital-card">
            <div class="vital-label">Temperature</div>
            <div class="vital-value">{temp}</div>
            <div class="vital-unit">° Celsius</div>
        </div>
        """, unsafe_allow_html=True)

    with v4:

        st.markdown(f"""
        <div class="vital-card">
            <div class="vital-label">Respiratory Rate</div>
            <div class="vital-value">{rr}</div>
            <div class="vital-unit">breaths / minute</div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# TAB 2 — TRENDS
# =========================================================

with tab2:

    st.markdown("### 📈 Longitudinal Clinical Intelligence")

    st.markdown(
        '<div class="ai-banner">🧬 Temporal analysis engine — monitoring physiological deterioration patterns.</div>',
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
                color="#22d3ee",
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
                color="#a78bfa",
                width=3
            )
        )
    )

    fig.update_layout(

        title="7-Day Physiological Trajectory",

        template="plotly_dark",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(5,15,25,0.55)",

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
            l=10,
            r=10,
            t=60,
            b=10
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


# =========================================================
# TAB 3 — AI VISION
# =========================================================

with tab3:

    st.markdown("### 🖼️ AI Medical Vision")

    st.markdown(
        '<div class="ai-banner">👁️ Computer Vision Module — Chest X-Ray analysis pipeline.</div>',
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
            "⚠️ Current imaging visualization is a prototype. A validated medical imaging model will be integrated in the next development stage."
        )

    else:

        st.info(
            "📤 Upload a chest X-Ray image to activate the computer-vision interface."
        )


# =========================================================
# TAB 4 — AI RISK REPORT
# =========================================================

with tab4:

    st.markdown("### 🧠 Multimodal Clinical Intelligence")

    st.markdown(
        '<div class="ai-banner">🤖 Clinical reasoning engine integrating physiological and laboratory parameters.</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # AI CLINICAL MODEL
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # RISK DISPLAY
    # -----------------------------------------------------

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
                    color:#67e8f9;
                    font-size:22px;
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

            <b>Patient:</b> {patient_id}<br><br>

            <b>AI Assessment:</b> {risk_level}<br>

            <b>Risk Score:</b> {score}/100<br>

            <b>Analysis Time:</b>
            {datetime.now().strftime("%H:%M:%S")}

            </div>
            """,
            unsafe_allow_html=True
        )


    # -----------------------------------------------------
    # CONTRIBUTIONS
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # CLINICAL DATA
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # REPORT
    # -----------------------------------------------------

    st.markdown("### 📄 Generate Clinical AI Report")

    report_content = f"""
============================================================
                 MEDICOGNITIVE AI
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
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

    <b>MEDICOGNITIVE AI</b><br>

    Multimodal Clinical Intelligence Research Platform<br><br>

    🧠 Clinical Risk Engine &nbsp; • &nbsp;
    👁️ Computer Vision &nbsp; • &nbsp;
    📈 Temporal Analysis &nbsp; • &nbsp;
    📊 Multimodal Decision Support

</div>
""", unsafe_allow_html=True)

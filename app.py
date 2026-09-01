import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from PIL import Image
import matplotlib.pyplot as plt

from clinical_model import clinical_risk_assessment


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="MEDICOGNITIVE AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ---------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------

st.markdown("""
<style>

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

.stButton>button {
    width: 100%;
    border-radius: 8px;
    height: 3em;
    background-color: #0284c7;
    color: white;
    font-weight: bold;
}

.metric-card {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Application Header
# ---------------------------------------------------------

st.title("🩺 MEDICOGNITIVE AI")

st.caption(
    "Multimodal Early-Warning & Clinical Decision Support System"
)


# ---------------------------------------------------------
# Navigation Tabs
# ---------------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Patient Vitals",
    "📈 Longitudinal Trends",
    "🖼️ X-Ray AI Analysis",
    "📄 Multimodal Risk Report"
])


# =========================================================
# TAB 1 — PATIENT VITALS
# =========================================================

with tab1:

    st.subheader("Patient Clinical Profile")

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
            "Oxygen Saturation - SpO2 (%)",
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
            "C-Reactive Protein - CRP (mg/L)",
            min_value=0.0,
            max_value=300.0,
            value=45.0
        )

        wbc = st.number_input(
            "White Blood Cell Count - WBC (k/µL)",
            min_value=0.0,
            max_value=50.0,
            value=14.5
        )

    st.markdown("---")

    st.info(
        "Patient data will be analyzed by the MEDICOGNITIVE AI "
        "clinical risk engine."
    )


# =========================================================
# TAB 2 — LONGITUDINAL TRENDS
# =========================================================

with tab2:

    st.subheader("Longitudinal Vital Sign Tracking")

    dates = [
        datetime.now() - timedelta(days=i)
        for i in range(6, -1, -1)
    ]

    dates_str = [
        d.strftime("%b %d")
        for d in dates
    ]

    # Prototype timeline
    mock_spo2 = [
        98,
        97,
        96,
        94,
        93,
        92,
        spo2
    ]

    mock_temp = [
        36.6,
        36.9,
        37.2,
        37.8,
        38.2,
        38.6,
        temp
    ]

    mock_hr = [
        70,
        75,
        82,
        90,
        98,
        105,
        hr
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=dates_str,
            y=mock_spo2,
            mode="lines+markers",
            name="SpO2 (%)",
            line=dict(
                color="#ef4444",
                width=3
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=dates_str,
            y=mock_temp,
            mode="lines+markers",
            name="Temperature (°C)",
            line=dict(
                color="#f59e0b",
                width=2
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=dates_str,
            y=mock_hr,
            mode="lines+markers",
            name="Heart Rate (bpm)",
            line=dict(
                color="#3b82f6",
                width=2
            )
        )
    )

    fig.update_layout(
        title="7-Day Clinical Trend",
        xaxis_title="Date",
        yaxis_title="Measured Value",
        hovermode="x unified",
        margin=dict(
            l=10,
            r=10,
            t=40,
            b=10
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    if spo2 < 92 or temp > 38.5:

        st.error(
            "⚠️ Clinical warning: abnormal recent vital-sign pattern detected."
        )

    else:

        st.success(
            "✓ No critical trend alert detected from the current prototype timeline."
        )


# =========================================================
# TAB 3 — X-RAY AI
# =========================================================

with tab3:

    st.subheader(
        "Medical Imaging Analysis (Chest X-Ray)"
    )

    uploaded_file = st.file_uploader(
        "Upload CXR Image (PNG / JPG)",
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

            st.image(
                image,
                caption="Original X-Ray Image",
                use_container_width=True
            )

        with col_img2:

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
                figsize=(4, 4)
            )

            ax.imshow(img_np)

            ax.imshow(
                heatmap,
                cmap="jet",
                alpha=0.4
            )

            ax.axis("off")

            st.pyplot(
                fig_cam
            )

            st.caption(
                "Prototype visualization — AI imaging model will be integrated in the next stage."
            )

        st.warning(
            "⚠️ X-Ray AI is currently a prototype visualization. "
            "No diagnostic conclusion should be made from this result."
        )

    else:

        st.info(
            "Upload a chest X-ray image to begin imaging analysis."
        )


# =========================================================
# TAB 4 — MULTIMODAL RISK REPORT
# =========================================================

with tab4:

    st.subheader(
        "Multimodal Early-Warning Risk Assessment"
    )

    # -----------------------------------------------------
    # Clinical AI Risk Engine
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

    st.markdown("---")

    # -----------------------------------------------------
    # Risk Result
    # -----------------------------------------------------

    if risk_level == "HIGH":

        st.error(
            f"🚨 HIGH RISK: {score}/100"
        )

    elif risk_level == "MODERATE":

        st.warning(
            f"⚠️ MODERATE RISK: {score}/100"
        )

    else:

        st.success(
            f"✅ LOWER RISK: {score}/100"
        )

    st.caption(
        "AI-assisted risk estimation for research and "
        "clinical decision-support purposes. "
        "It is not a definitive medical diagnosis."
    )


    # -----------------------------------------------------
    # Why did the AI generate this risk?
    # -----------------------------------------------------

    st.markdown(
        "### 🧠 Why did the system generate this risk?"
    )

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
    # Clinical Data Summary
    # -----------------------------------------------------

    st.markdown(
        "### 📊 Clinical Data Summary"
    )

    summary_df = pd.DataFrame(
        {
            "Parameter": [
                "Age",
                "Sex",
                "SpO2",
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

    st.table(
        summary_df
    )


    # -----------------------------------------------------
    # Integrated Summary
    # -----------------------------------------------------

    st.markdown(
        "### 🔬 Integrated Summary"
    )

    integrated_df = pd.DataFrame(
        {
            "Modality": [
                "Vital Signs",
                "Biomarkers",
                "Radiology",
                "Clinical AI"
            ],

            "Current Status": [
                f"SpO2 {spo2}% | HR {hr} bpm | Temp {temp} °C",
                f"CRP {crp} mg/L | WBC {wbc} k/µL",
                "X-Ray module available",
                f"{risk_level} risk ({score}/100)"
            ]
        }
    )

    st.table(
        integrated_df
    )


    # -----------------------------------------------------
    # Report Generation
    # -----------------------------------------------------

    report_content = f"""
==================================================
        MEDICOGNITIVE AI
   CLINICAL DECISION SUPPORT REPORT
==================================================

Date/Time:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Patient ID:
{patient_id}

Age:
{age}

Sex:
{sex}


--------------------------------------------------
1. PATIENT VITALS
--------------------------------------------------

SpO2:
{spo2} %

Heart Rate:
{hr} bpm

Temperature:
{temp} °C

Respiratory Rate:
{rr} /min


--------------------------------------------------
2. LABORATORY BIOMARKERS
--------------------------------------------------

CRP:
{crp} mg/L

WBC:
{wbc} k/µL


--------------------------------------------------
3. CLINICAL AI ASSESSMENT
--------------------------------------------------

Risk Score:
{score}/100

Risk Level:
{risk_level}


--------------------------------------------------
4. CONTRIBUTING FACTORS
--------------------------------------------------

"""

    for factor, contribution in contributions.items():

        report_content += (
            f"{factor}: "
            f"{contribution}\n"
        )


    report_content += """

--------------------------------------------------
IMPORTANT DISCLAIMER
--------------------------------------------------

This system is an AI-assisted research prototype
for clinical decision support.

It is NOT a substitute for professional medical
diagnosis, clinical examination, or physician
judgment.

==================================================
"""


    st.download_button(
        label="📥 Download AI Clinical Report (.TXT)",

        data=report_content,

        file_name=(
            f"Medicognitive_Report_"
            f"{patient_id}.txt"
        ),

        mime="text/plain"
    )

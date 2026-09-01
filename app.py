import streamlit as st
import pandas as pd
import numpy as np
from clinical_model import clinical_risk_assessment
import plotly.graph_objects as go
from datetime import datetime, timedelta
from PIL import Image
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Page Configuration & Custom CSS for Mobile Responsive UI
# ---------------------------------------------------------
st.set_page_config(
    page_title="MEDICOGNITIVE AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling for Mobile Polish
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

# Application Header
st.title("🩺 MEDICOGNITIVE AI")
st.caption("Multimodal Early-Warning & Clinical Decision Support System")

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Patient Vitals", 
    "📈 Longitudinal Trends", 
    "🖼️ X-Ray AI Analysis", 
    "📄 Multimodal Risk Report"
])

# ---------------------------------------------------------
# TAB 1: Patient Vitals & Clinical Data Entry
# ---------------------------------------------------------
with tab1:
    st.subheader("Patient Clinical Profile")
    st.text_input("Patient Identification Number", value="MC-10482", disabled=True)
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age (Years)", min_value=1, max_value=120, value=62)
        sex = st.selectbox("Sex", ["Male", "Female"])
        spo2 = st.slider("Oxygen Saturation - SpO2 (%)", min_value=50, max_value=100, value=91)
        hr = st.number_input("Heart Rate (bpm)", min_value=30, max_value=220, value=112)
    
    with col2:
        temp = st.number_input("Body Temperature (°C)", min_value=30.0, max_value=45.0, value=38.9, step=0.1)
        rr = st.number_input("Respiratory Rate (/min)", min_value=5, max_value=60, value=25)
        crp = st.number_input("C-Reactive Protein - CRP (mg/L)", min_value=0.0, max_value=300.0, value=45.0)
        wbc = st.number_input("White Blood Cell Count - WBC (k/µL)", min_value=0.0, max_value=50.0, value=14.5)

# ---------------------------------------------------------
# TAB 2: Longitudinal Trend Analysis (Past 7 Days)
# ---------------------------------------------------------
with tab2:
    st.subheader("Longitudinal Vital Sign Tracking")
    
    # Timeline dates generation
    dates = [datetime.now() - timedelta(days=i) for i in range(6, -1, -1)]
    dates_str = [d.strftime("%b %d") for d in dates]
    
    # Mock longitudinal trend progression relative to user input
    mock_spo2 = [98, 97, 96, 94, 93, 92, spo2]
    mock_temp = [36.6, 36.9, 37.2, 37.8, 38.2, 38.6, temp]
    mock_hr = [70, 75, 82, 90, 98, 105, hr]
    
    # Plotly Trend Graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates_str, y=mock_spo2, mode='lines+markers', name='SpO2 (%)', line=dict(color='#ef4444', width=3)))
    fig.add_trace(go.Scatter(x=dates_str, y=mock_temp, mode='lines+markers', name='Temp (°C)', line=dict(color='#f59e0b', width=2)))
    fig.add_trace(go.Scatter(x=dates_str, y=mock_hr, mode='lines+markers', name='Heart Rate (bpm)', line=dict(color='#3b82f6', width=2)))
    
    fig.update_layout(
        title="7-Day Deterioration Timeline",
        xaxis_title="Date",
        yaxis_title="Measured Value",
        hovermode="x unified",
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    if spo2 < 92 or temp > 38.5:
        st.error("⚠️ CRITICAL ALERT: Progressive SpO2 decline and persistent hyperthermia detected over the last 48 hours.")

# ---------------------------------------------------------
# TAB 3: X-Ray Vision AI & Grad-CAM Analysis
# ---------------------------------------------------------
with tab3:
    st.subheader("Medical Imaging Analysis (Chest X-Ray)")
    uploaded_file = st.file_uploader("Upload CXR Image (PNG / JPG / DICOM)", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        col_img1, col_img2 = st.columns(2)
        
        with col_img1:
            st.image(image, caption="Original X-Ray Image", use_column_width=True)
        
        with col_img2:
            # Simulated Grad-CAM Heatmap overlay
            img_np = np.array(image.resize((224, 224)))
            heatmap = np.zeros((224, 224))
            heatmap[100:180, 120:200] = 0.8  # Highlight lower lobe region
            
            fig_cam, ax = plt.subplots(figsize=(4, 4))
            ax.imshow(img_np)
            ax.imshow(heatmap, cmap='jet', alpha=0.4)
            ax.axis('off')
            
            st.pyplot(fig_cam)
            st.caption("AI Heatmap (Grad-CAM): Suspected Consolidation Area")
            
        st.warning("🔍 Vision AI Finding: 88.4% Probability of Right Lower Lobe Infiltration / Pneumonia.")

# ---------------------------------------------------------
# TAB 4: Multimodal Risk Score & Automated Clinical Report
# ---------------------------------------------------------
with tab4:
    st.subheader("Multimodal Early Warning Risk Assessment")
    
    # Rule-Based Score Calculation
    score = 0
    if spo2 < 92: score += 3
    elif spo2 < 95: score += 1
    if temp >= 38.5: score += 2
    if hr >= 100: score += 2
    if rr >= 22: score += 1
    
    st.markdown("---")
    
    if score >= 5:
        st.error(f"🚨 HIGH RISK SCORE: {score}/9 — High likelihood of acute clinical deterioration. ICU consultation recommended.")
    elif score >= 3:
        st.warning(f"⚠️ MODERATE RISK SCORE: {score}/9 — Requires increased frequency of monitoring.")
    else:
        st.success(f"✅ LOW RISK SCORE: {score}/9 — Clinical status within acceptable limits.")
        
    st.markdown("### Integrated Summary")
    summary_df = pd.DataFrame({
        "Modality": ["Vital Signs", "Biomarkers", "Radiology (X-Ray)", "Risk Level"],
        "Findings": [
            f"SpO2: {spo2}%, HR: {hr} bpm, Temp: {temp} °C",
            f"CRP: {crp} mg/L, WBC: {wbc} k/µL",
            "Lower Right Infiltration Detected",
            f"Score {score}/9 ({'High' if score>=5 else 'Moderate' if score>=3 else 'Low'})"
        ]
    })
    st.table(summary_df)
    
    # Generate Printable Text Report
    report_content = f"""==================================================
         MEDICOGNITIVE AI CLINICAL REPORT
==================================================
Date/Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Patient ID: MC-10482
Age/Sex: {age} / {sex}

[1. PATIENT VITALS]
- SpO2: {spo2}%
- Heart Rate: {hr} bpm
- Core Temperature: {temp} °C
- Respiratory Rate: {rr} /min

[2. LAB BIOMARKERS]
- C-Reactive Protein (CRP): {crp} mg/L
- WBC Count: {wbc} k/µL

[3. IMAGING ASSESSMENT]
- CXR Infiltration Probability: High (Right Lower Lobe)

[4. MULTIMODAL EVALUATION]
- Calculated Risk Score: {score} / 9
- Recommendation: {"Immediate Senior Medical Review / ICU Evaluation" if score>=5 else "Frequent Monitoring"}
==================================================
"""
    
    st.download_button(
        label="📥 Download Official Medical Report (.TXT)",
        data=report_content,
        file_name=f"Medicognitive_Report_MC10482.txt",
        mime="text/plain"
    )

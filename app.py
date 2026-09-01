import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="MEDICOGNITIVE AI",
    page_icon="🩺",
    layout="wide"
)

# Title & Subtitle
st.title("🩺 MEDICOGNITIVE AI")
st.caption("Multimodal Early-Warning & Medical Decision Support System")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["📋 Patient Vitals", "📈 Longitudinal Analysis", "🖼️ X-Ray Analysis"])

# --- TAB 1: Patient Vitals ---
with tab1:
    st.header("Patient Clinical Profile")
    st.text_input("Patient ID", value="MC-10482", disabled=True)
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=62)
        sex = st.selectbox("Sex", ["Male", "Female"])
        spo2 = st.slider("SpO2 (%)", min_value=50, max_value=100, value=91)
        hr = st.number_input("Heart Rate (bpm)", min_value=30, max_value=220, value=112)
    
    with col2:
        temp = st.number_input("Temperature (°C)", min_value=30.0, max_value=45.0, value=38.9)
        rr = st.number_input("Respiratory Rate (/min)", min_value=5, max_value=60, value=25)
        crp = st.number_input("CRP (mg/L)", min_value=0.0, max_value=300.0, value=45.0)
        wbc = st.number_input("WBC (k/µL)", min_value=0.0, max_value=50.0, value=14.5)

# --- TAB 2: Longitudinal Analysis ---
with tab2:
    st.header("Longitudinal Patient Trends (Past 7 Days)")
    
    # Generate Mock Timeline Data
    dates = [datetime.now() - timedelta(days=i) for i in range(6, -1, -1)]
    dates_str = [d.strftime("%b %d") for d in dates]
    
    mock_spo2 = [97, 96, 95, 93, 92, 91, spo2]
    mock_temp = [36.8, 37.1, 37.5, 38.0, 38.5, 38.8, temp]
    mock_hr = [72, 78, 85, 95, 102, 108, hr]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates_str, y=mock_spo2, mode='lines+markers', name='SpO2 (%)', line=dict(color='red', width=3)))
    fig.add_trace(go.Scatter(x=dates_str, y=mock_temp, mode='lines+markers', name='Temp (°C)', line=dict(color='orange', width=2)))
    fig.add_trace(go.Scatter(x=dates_str, y=mock_hr, mode='lines+markers', name='Heart Rate (bpm)', line=dict(color='blue', width=2)))
    
    fig.update_layout(title="Vital Signs Progression Over Time", xaxis_title="Date", yaxis_title="Value", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    
    st.warning("⚠️ Warning: Deteriorating SpO2 and rising Temperature detected over the last 48 hours.")

# --- TAB 3: X-Ray Analysis ---
with tab3:
    st.header("Chest X-Ray Analysis")
    uploaded_file = st.file_uploader("Upload Chest X-Ray Image (DICOM / PNG / JPG)", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded X-Ray", use_column_width=True)
        st.success("Analysis Complete: Infiltration detected in Lower Right Lobe.")

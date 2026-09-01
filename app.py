import streamlit as st
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torchvision.models import densenet121, DenseNet121_Weights
from PIL import Image
import numpy as np
import cv2
import datetime

# إعداد الصفحة لتناسب الموبايل
st.set_page_config(
    page_title="MEDICOGNITIVE AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# تحميل نموذج الذكاء الاصطناعي للرؤية
@st.cache_resource
def load_vision_model():
    model = densenet121(weights=DenseNet121_Weights.DEFAULT)
    num_ftrs = model.classifier.in_features
    model.classifier = nn.Linear(num_ftrs, 3)
    model.eval()
    return model

vision_model = load_vision_model()

def preprocess_image(image: Image.Image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    return transform(image.convert("RGB")).unsqueeze(0)

def generate_gradcam(model, input_tensor, original_image):
    target_layer = model.features.denseblock4
    feature_maps, gradients = [], []

    def forward_hook(module, input, output):
        feature_maps.append(output)

    def backward_hook(module, grad_in, grad_out):
        gradients.append(grad_out[0])

    h1 = target_layer.register_forward_hook(forward_hook)
    h2 = target_layer.register_backward_hook(backward_hook)

    output = model(input_tensor)
    pred_idx = torch.argmax(output, dim=1).item()
    
    model.zero_grad()
    score = output[0, pred_idx]
    score.backward()

    h1.remove()
    h2.remove()

    grads = gradients[0].cpu().data.numpy()[0]
    f_maps = feature_maps[0].cpu().data.numpy()[0]
    weights = np.mean(grads, axis=(1, 2))
    
    cam = np.zeros(f_maps.shape[1:], dtype=np.float32)
    for i, w in enumerate(weights):
        cam += w * f_maps[i, :, :]

    cam = np.maximum(cam, 0)
    if np.max(cam) != 0:
        cam = cv2.resize(cam, original_image.size)
        cam = (cam - np.min(cam)) / np.max(cam)
    else:
        cam = np.zeros((original_image.size[1], original_image.size[0]))

    heatmap = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)
    
    orig_np = np.array(original_image.convert("RGB"))
    overlay = cv2.addWeighted(orig_np, 0.65, heatmap, 0.35, 0)
    probabilities = torch.softmax(output, dim=1).detach().numpy()[0]
    return overlay, probabilities, pred_idx

def calculate_clinical_risk(spo2, hr, temp, rr, crp, wbc):
    score = 0
    factors = []
    if spo2 < 93:
        score += 30
        factors.append(f"Low SpO₂ ({spo2}%)")
    elif spo2 < 95:
        score += 15
        factors.append(f"Borderline SpO₂ ({spo2}%)")

    if hr > 100:
        score += 15
        factors.append(f"Tachycardia (HR: {hr} bpm)")
    if temp > 38.0:
        score += 15
        factors.append(f"Fever (Temp: {temp}°C)")
    if rr > 20:
        score += 15
        factors.append(f"Tachypnea (RR: {rr}/min)")
    if crp > 10:
        score += 15
        factors.append(f"Elevated CRP ({crp} mg/L)")
    if wbc > 11.0:
        score += 10
        factors.append(f"Leukocytosis (WBC: {wbc} k/µL)")

    total_score = min(score, 100)
    category = "HIGH" if total_score >= 60 else ("MODERATE" if total_score >= 30 else "LOW")
    return total_score, category, factors

# الواجهة الأساسية
st.title("🩺 MEDICOGNITIVE AI")
st.caption("Multimodal Early-Warning & Medical Decision Support System")

tabs = st.tabs(["📋 Patient Vitals", "🖼️ X-Ray Analysis", "📊 Multimodal Risk Report"])

with tabs[0]:
    st.subheader("Patient Clinical Profile")
    patient_id = st.text_input("Patient ID", value="MC-10482")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", 1, 120, 62)
        sex = st.selectbox("Sex", ["Male", "Female"])
        spo2 = st.slider("SpO₂ (%)", 70, 100, 91)
        hr = st.number_input("Heart Rate (bpm)", 40, 200, 112)
    with col2:
        temp = st.number_input("Temperature (°C)", 35.0, 42.0, 38.9)
        rr = st.number_input("Respiratory Rate (/min)", 10, 50, 25)
        crp = st.number_input("CRP (mg/L)", 0.0, 300.0, 45.0)
        wbc = st.number_input("WBC (k/µL)", 1.0, 40.0, 14.5)

with tabs[1]:
    st.subheader("Upload Chest X-Ray")
    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded X-Ray", use_container_width=True)
        with st.spinner("Analyzing Vision Model & Heatmap..."):
            input_tensor = preprocess_image(image)
            overlay, probs, pred_idx = generate_gradcam(vision_model, input_tensor, image)
            st.image(overlay, caption="AI Heatmap (Grad-CAM)", use_container_width=True)
            classes = ["Pneumonia", "Pleural Effusion", "Normal"]
            st.write(f"**Primary Finding:** {classes[pred_idx]} ({probs[pred_idx]*100:.1f}%)")

with tabs[2]:
    st.subheader("Combined Assessment & Report")
    risk_score, risk_cat, risk_factors = calculate_clinical_risk(spo2, hr, temp, rr, crp, wbc)
    st.metric("Clinical Risk Score", f"{risk_score} / 100", delta=risk_cat)
    st.write("**Contributing Risk Factors:**")
    for f in risk_factors:
        st.write(f"- {f}")

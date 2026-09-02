import os
import base64
import io
from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from PIL import Image, UnidentifiedImageError

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
# OPENAI CONFIGURATION
# =========================================================

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


AI_MODEL = "gpt-5.6-luna"


def get_openai_api_key():
    """
    Reads OPENAI_API_KEY from Streamlit Secrets first,
    then from environment variables.
    """

    api_key = None

    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        pass

    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        api_key = str(api_key).strip()

    return api_key


def get_openai_client():
    """
    Safely creates an OpenAI client.
    """

    if OpenAI is None:
        return None, (
            "The OpenAI Python package is not installed. "
            "Add 'openai' to requirements.txt."
        )

    api_key = get_openai_api_key()

    if not api_key:
        return None, (
            "OPENAI_API_KEY is not configured. "
            "Add it to Streamlit Secrets or environment variables."
        )

    try:
        client = OpenAI(api_key=api_key)
        return client, None
    except Exception as exc:
        return None, f"Unable to initialize the AI client: {exc}"


# =========================================================
# GENERIC AI CALL
# =========================================================

def ask_medical_ai(prompt, conversation_history=None):
    """
    General medical AI assistant.

    Returns:
        text result or error message
    """

    client, error = get_openai_client()

    if client is None:
        return f"AI SERVICE ERROR\n\n{error}"

    system_instructions = """
You are MEDICOGNITIVE AI, an advanced medical clinical decision-support
assistant designed for healthcare professionals.

Your task is to provide structured, evidence-aware medical reasoning.

IMPORTANT SAFETY RULES:
- You are an AI clinical decision-support system.
- Do not claim certainty when the available information is insufficient.
- Do not replace a qualified physician, radiologist, surgeon, or other healthcare professional.
- Do not fabricate laboratory values, imaging findings, symptoms, history, examination findings, or diagnoses.
- Clearly distinguish observed information from clinical inference.
- Give differential diagnoses when appropriate.
- Highlight clinically important red flags.
- If a potentially life-threatening condition is possible, clearly state that urgent medical evaluation may be required.
- Do not prescribe medication doses.
- For treatment, provide GENERAL MANAGEMENT CONSIDERATIONS rather than individualized prescriptions.
- Use professional medical English.
- Use standard medical terminology.
- Be concise but clinically useful.
"""

    try:
        messages = []

        if conversation_history:
            for item in conversation_history:
                if not isinstance(item, dict):
                    continue

                role = item.get("role")
                content = item.get("content")

                if role in ("user", "assistant") and content:
                    messages.append({
                        "role": role,
                        "content": str(content)
                    })

        messages.append({
            "role": "user",
            "content": str(prompt)
        })

        response = client.responses.create(
            model=AI_MODEL,
            instructions=system_instructions,
            input=messages
        )

        result = getattr(response, "output_text", None)

        if result is None:
            result = ""

        result = str(result).strip()

        if not result:
            return (
                "AI SERVICE ERROR\n\n"
                "The AI returned an empty response. "
                "Please try again."
            )

        return result

    except Exception as exc:
        return (
            "AI SERVICE ERROR\n\n"
            f"{type(exc).__name__}: {exc}"
        )


# =========================================================
# IMAGE PREPARATION
# =========================================================

def prepare_medical_image(uploaded_file):
    """
    Validates and optimizes an uploaded image.

    Returns:
        image_bytes, PIL image, error
    """

    if uploaded_file is None:
        return None, None, "No image was uploaded."

    try:
        raw_bytes = uploaded_file.getvalue()

        if not raw_bytes:
            return None, None, "The uploaded file is empty."

        if len(raw_bytes) > 25 * 1024 * 1024:
            return (
                None,
                None,
                "The image is larger than 25 MB. Please upload a smaller image."
            )

        image = Image.open(io.BytesIO(raw_bytes))

        image.load()

        if image.width < 64 or image.height < 64:
            return (
                None,
                None,
                "The image resolution is too small for meaningful analysis."
            )

        image = image.convert("RGB")

        max_dimension = 2048

        if max(image.size) > max_dimension:
            ratio = max_dimension / float(max(image.size))

            new_size = (
                max(1, int(image.width * ratio)),
                max(1, int(image.height * ratio))
            )

            image = image.resize(
                new_size,
                Image.Resampling.LANCZOS
            )

        output = io.BytesIO()

        image.save(
            output,
            format="JPEG",
            quality=94,
            optimize=True
        )

        image_bytes = output.getvalue()

        return image_bytes, image, None

    except UnidentifiedImageError:
        return (
            None,
            None,
            "The uploaded file is not a valid supported image."
        )

    except Exception as exc:
        return (
            None,
            None,
            f"Unable to process the image: {exc}"
        )


# =========================================================
# AI X-RAY ANALYSIS
# =========================================================

def analyze_xray_with_ai(image_bytes, filename):
    """
    Sends a medical image to the multimodal AI model.

    Returns:
        radiology report
    """

    client, error = get_openai_client()

    if client is None:
        return f"AI RADIOLOGY SERVICE ERROR\n\n{error}"

    if not image_bytes:
        return "AI RADIOLOGY SERVICE ERROR\n\nNo image data was supplied."

    try:
        encoded_image = base64.b64encode(image_bytes).decode("utf-8")

        image_data_url = (
            "data:image/jpeg;base64,"
            + encoded_image
        )

        radiology_instructions = """
You are MEDICOGNITIVE AI Radiology Intelligence.

You assist qualified healthcare professionals with preliminary
radiographic interpretation.

Analyze the supplied image carefully.

DO NOT invent findings.

If the image is not clearly a radiograph, state that.

If image quality is insufficient, state that.

If a fracture cannot be confidently identified, do not invent one.

Use professional radiology terminology.

Your report MUST be written in professional medical English.

Use exactly this structure:

1. EXAMINATION
2. IMAGE QUALITY
3. ANATOMICAL REGION
4. LATERALITY
5. RADIOGRAPHIC FINDINGS
6. FRACTURE / DISLOCATION ASSESSMENT
7. FRACTURE LOCATION
8. FRACTURE MORPHOLOGY
9. DISPLACEMENT / ANGULATION
10. ARTICULAR INVOLVEMENT
11. JOINT ALIGNMENT
12. SOFT TISSUE FINDINGS
13. RADIOLOGICAL IMPRESSION
14. CLINICAL SIGNIFICANCE
15. ESTIMATED HEALING TIME
16. GENERAL MANAGEMENT CONSIDERATIONS
17. RED FLAGS
18. RECOMMENDED CLINICAL CORRELATION
19. AI SAFETY NOTE

For ESTIMATED HEALING TIME:
- Give a typical range only if a fracture is actually suspected.
- Explain that healing varies according to age, fracture type,
  displacement, vascularity, comorbidities, treatment and complications.
- Do not promise an exact healing date.

For GENERAL MANAGEMENT CONSIDERATIONS:
- Discuss general principles such as immobilization,
  orthopedic evaluation, repeat imaging, operative versus
  non-operative considerations when appropriate.
- Do not prescribe medication doses.

The final impression should clearly distinguish:
A) findings directly visible on the image
B) interpretation/inference
C) limitations.
"""

        user_text = f"""
Analyze the uploaded radiographic image.

Filename:
{filename}

Provide a preliminary AI-assisted radiology report.
Use professional medical English.
"""

        response = client.responses.create(
            model=AI_MODEL,
            instructions=radiology_instructions,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": user_text
                        },
                        {
                            "type": "input_image",
                            "image_url": image_data_url
                        }
                    ]
                }
            ]
        )

        result = getattr(response, "output_text", None)

        if result is None:
            result = ""

        result = str(result).strip()

        if not result:
            return (
                "AI RADIOLOGY SERVICE ERROR\n\n"
                "The AI returned an empty radiology report."
            )

        return result

    except Exception as exc:
        return (
            "AI RADIOLOGY SERVICE ERROR\n\n"
            f"{type(exc).__name__}: {exc}"
        )


# =========================================================
# SAFE RISK SCORE NORMALIZATION
# =========================================================

def normalize_risk_score(raw_value):
    """
    Converts different possible clinical model outputs into
    a single numeric percentage from 0 to 100.
    """

    value = raw_value

    # Dictionary
    if isinstance(value, dict):

        possible_keys = [
            "risk_score",
            "riskScore",
            "score",
            "risk",
            "probability",
            "prediction",
            "prob",
            "percentage"
        ]

        extracted = None

        for key in possible_keys:
            if key in value:
                extracted = value[key]
                break

        if extracted is None:
            numeric_values = []

            for item in value.values():
                if isinstance(item, (int, float, np.integer, np.floating)):
                    numeric_values.append(item)

            if len(numeric_values) == 1:
                extracted = numeric_values[0]

        if extracted is None:
            raise ValueError(
                "Clinical model returned a dictionary without "
                "a recognizable numeric risk value."
            )

        value = extracted

    # List / Tuple
    elif isinstance(value, (list, tuple)):

        if len(value) == 0:
            raise ValueError(
                "Clinical model returned an empty list or tuple."
            )

        numeric_candidates = []

        for item in value:
            if isinstance(item, (int, float, np.integer, np.floating)):
                numeric_candidates.append(item)

        if not numeric_candidates:
            raise ValueError(
                "Clinical model returned a list/tuple "
                "without a numeric risk value."
            )

        value = numeric_candidates[0]

    # NumPy array
    elif isinstance(value, np.ndarray):

        if value.size == 0:
            raise ValueError(
                "Clinical model returned an empty NumPy array."
            )

        if value.size == 1:
            value = value.reshape(-1)[0]
        else:
            flat = value.reshape(-1)

            numeric_candidates = []

            for item in flat:
                if isinstance(
                    item,
                    (int, float, np.integer, np.floating)
                ):
                    numeric_candidates.append(item)

            if not numeric_candidates:
                raise ValueError(
                    "Clinical model returned an array "
                    "without numeric values."
                )

            value = numeric_candidates[0]

    # Tensor-like / scalar-like
    elif hasattr(value, "item"):

        try:
            value = value.item()
        except Exception:
            pass

    try:
        score = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(
            f"Clinical model returned an invalid risk score: {exc}"
        )

    if not np.isfinite(score):
        raise ValueError(
            "Clinical model returned a non-finite risk score."
        )

    # Convert probability 0-1 to percentage
    if 0 <= score <= 1:
        score *= 100

    score = max(0.0, min(100.0, score))

    return score


# =========================================================
# PREMIUM CSS
# =========================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;800;900&family=Inter:wght@300;400;500;600;700&family=Tajawal:wght@300;400;500;600;700;800&display=swap');

:root {
    --gold-primary: #D4AF37;
    --gold-light: #FFF099;
    --gold-dark: #AA7C11;
    --gold-soft: #E7C95C;
    --black: #050505;
    --black-2: #090909;
    --card: rgba(20,20,20,0.72);
    --border: rgba(212,175,55,0.28);
    --gold-gradient: linear-gradient(
        135deg,
        #BF953F,
        #FCF6BA,
        #B38728,
        #FBF5B7,
        #AA771C
    );
}

html,
body,
[class*="css"] {
    font-family: 'Tajawal', 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(212,175,55,0.10),
            transparent 25%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(212,175,55,0.08),
            transparent 28%
        ),
        radial-gradient(
            circle at 50% 90%,
            rgba(212,175,55,0.06),
            transparent 30%
        ),
        #050505;
    color: #f3e7a6;
}

.main {
    background: transparent;
}

.block-container {
    max-width: 1550px;
    padding-top: 1rem;
    padding-bottom: 2rem;
}

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #050505;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(
        180deg,
        #D4AF37,
        #6f5310
    );
    border-radius: 10px;
}

.gold-background {
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}

.gold-orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(90px);
    opacity: 0.10;
    background: #D4AF37;
    animation: floatOrb 10s ease-in-out infinite;
}

.gold-orb.one {
    width: 300px;
    height: 300px;
    top: 10%;
    left: -100px;
}

.gold-orb.two {
    width: 350px;
    height: 350px;
    right: -120px;
    bottom: 10%;
    animation-delay: -4s;
}

@keyframes floatOrb {
    0%, 100% {
        transform: translateY(0px) scale(1);
    }
    50% {
        transform: translateY(-25px) scale(1.08);
    }
}

.luxury-nav {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;
    padding: 18px 24px;
    margin-bottom: 24px;
    border: 1px solid rgba(212,175,55,0.22);
    border-radius: 18px;
    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,0.04),
            rgba(255,255,255,0.015)
        );
    backdrop-filter: blur(20px);
    box-shadow:
        0 20px 70px rgba(0,0,0,0.35),
        inset 0 0 30px rgba(212,175,55,0.025);
}

.luxury-logo {
    font-family: 'Cinzel', serif;
    color: #E7C95C;
    font-size: 1.3rem;
    font-weight: 800;
    letter-spacing: 2px;
    white-space: nowrap;
}

.luxury-nav-links {
    display: flex;
    gap: 28px;
    color: #d7ca87;
    font-size: 0.95rem;
}

.luxury-nav-links span {
    transition: 0.3s;
}

.luxury-nav-links span:hover {
    color: #FFF099;
}

.vip-badge {
    padding: 8px 14px;
    border-radius: 999px;
    border: 1px solid rgba(212,175,55,0.45);
    background: rgba(212,175,55,0.07);
    color: #F7E98D;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 1px;
    white-space: nowrap;
}

.premium-hero {
    position: relative;
    z-index: 2;
    text-align: center;
    padding: 55px 25px 45px;
    margin-bottom: 25px;
    border-radius: 28px;
    border: 1px solid rgba(212,175,55,0.20);
    background:
        radial-gradient(
            circle at center,
            rgba(212,175,55,0.09),
            transparent 55%
        ),
        rgba(8,8,8,0.70);
    box-shadow:
        0 25px 100px rgba(0,0,0,0.50),
        inset 0 0 80px rgba(212,175,55,0.025);
    overflow: hidden;
}

.hero-medical-symbol {
    font-size: 4.5rem;
    margin-bottom: 5px;
    filter: drop-shadow(0 0 18px rgba(212,175,55,0.35));
}

.hero-subtitle {
    color: #bcae6e;
    font-size: 1rem;
    letter-spacing: 3px;
    margin-bottom: 15px;
}

.hero-brand {
    font-family: 'Cinzel', serif;
    font-size: clamp(2.3rem, 6vw, 5.2rem);
    font-weight: 900;
    letter-spacing: 7px;
    background: var(--gold-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 35px rgba(212,175,55,0.10);
}

.hero-description {
    margin-top: 12px;
    color: #81794f;
    font-size: 0.78rem;
    letter-spacing: 2.4px;
}

.doctor-name {
    margin-top: 22px;
    color: #F7E98D;
    font-size: 1.8rem;
    font-weight: 700;
}

.doctor-title {
    color: #9f9257;
    margin-top: 5px;
    font-size: 0.82rem;
    letter-spacing: 2px;
}

.ecg-line {
    max-width: 850px;
    margin: 24px auto 10px;
}

.ecg-line svg {
    width: 100%;
    height: 45px;
}

.ecg-line polyline {
    stroke: #D4AF37;
    filter: drop-shadow(0 0 5px rgba(212,175,55,0.7));
}

.system-status {
    display: inline-block;
    margin-top: 10px;
    padding: 9px 18px;
    border-radius: 999px;
    border: 1px solid rgba(212,175,55,0.20);
    background: rgba(212,175,55,0.045);
    color: #B9AA67;
    font-size: 0.72rem;
    letter-spacing: 1.5px;
}

.status-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #D4AF37;
    box-shadow: 0 0 12px #D4AF37;
    animation: pulseDot 1.7s infinite;
}

@keyframes pulseDot {
    0%, 100% {
        opacity: 1;
        transform: scale(1);
    }
    50% {
        opacity: 0.45;
        transform: scale(0.75);
    }
}

.feature-grid {
    position: relative;
    z-index: 2;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    margin: 25px 0 32px;
}

.feature-card {
    border: 1px solid rgba(212,175,55,0.18);
    background: rgba(15,15,15,0.72);
    border-radius: 20px;
    padding: 25px;
    transition: 0.35s ease;
    box-shadow: 0 20px 50px rgba(0,0,0,0.28);
}

.feature-card:hover {
    transform: translateY(-5px);
    border-color: rgba(212,175,55,0.42);
    box-shadow:
        0 25px 70px rgba(0,0,0,0.45),
        0 0 30px rgba(212,175,55,0.06);
}

.feature-icon {
    font-size: 2rem;
    color: #D4AF37;
    margin-bottom: 12px;
}

.feature-title {
    color: #F3DF76;
    font-weight: 800;
    font-size: 1.05rem;
}

.feature-text {
    margin-top: 8px;
    color: #8f8658;
    line-height: 1.8;
    font-size: 0.9rem;
}

.ai-banner {
    border: 1px solid rgba(212,175,55,0.25);
    border-left: 3px solid #D4AF37;
    padding: 15px 18px;
    margin: 12px 0 25px;
    border-radius: 12px;
    background:
        linear-gradient(
            90deg,
            rgba(212,175,55,0.08),
            rgba(212,175,55,0.015)
        );
    color: #D8C879;
    box-shadow: inset 0 0 25px rgba(212,175,55,0.025);
}

.section-heading {
    position: relative;
    margin: 20px 0 14px;
    padding: 14px 18px;
    border-bottom: 1px solid rgba(212,175,55,0.16);
    color: #F5E58B;
    font-family: 'Cinzel', 'Tajawal', sans-serif;
    font-size: 1.3rem;
    font-weight: 800;
    letter-spacing: 1px;
}

.section-heading span {
    color: #7f6a1d;
    margin-right: 10px;
    font-size: 0.8rem;
}

.glass-card {
    border: 1px solid rgba(212,175,55,0.18);
    border-radius: 20px;
    padding: 24px;
    background:
        linear-gradient(
            135deg,
            rgba(25,25,25,0.82),
            rgba(10,10,10,0.72)
        );
    box-shadow:
        0 20px 65px rgba(0,0,0,0.35),
        inset 0 0 40px rgba(212,175,55,0.015);
    margin-bottom: 20px;
}

.vital-card {
    border: 1px solid rgba(212,175,55,0.20);
    background: rgba(17,17,17,0.78);
    border-radius: 18px;
    padding: 20px;
    text-align: center;
    min-height: 130px;
    box-shadow: 0 15px 45px rgba(0,0,0,0.30);
}

.vital-label {
    color: #8f8658;
    font-size: 0.82rem;
}

.vital-value {
    color: #F4DF78;
    font-family: 'Cinzel', serif;
    font-size: 2rem;
    font-weight: 800;
    margin-top: 10px;
}

.vital-unit {
    color: #70683f;
    font-size: 0.72rem;
    margin-top: 3px;
}

.risk-panel {
    border: 1px solid rgba(212,175,55,0.30);
    border-radius: 25px;
    text-align: center;
    padding: 40px 20px;
    margin: 20px 0;
    background:
        radial-gradient(
            circle at center,
            rgba(212,175,55,0.10),
            rgba(8,8,8,0.85) 65%
        );
    box-shadow:
        0 20px 80px rgba(0,0,0,0.45),
        inset 0 0 50px rgba(212,175,55,0.025);
}

.risk-number {
    font-family: 'Cinzel', serif;
    font-size: 4.5rem;
    font-weight: 900;
    background: var(--gold-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.risk-label {
    color: #948651;
    letter-spacing: 2px;
    font-size: 0.75rem;
    margin-top: 5px;
}

.stTextInput > div > div,
.stNumberInput > div > div,
.stTextArea > div > div,
.stSelectbox > div > div {
    background: rgba(15,15,15,0.85) !important;
    border: 1px solid rgba(212,175,55,0.22) !important;
    border-radius: 12px !important;
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    color: #F0E5A3 !important;
}

.stSelectbox label,
.stNumberInput label,
.stTextInput label,
.stTextArea label,
.stSlider label {
    color: #CFC17D !important;
}

.stSlider [data-baseweb="slider"] {
    color: #D4AF37 !important;
}

.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 12px;
    border: 1px solid rgba(212,175,55,0.45);
    background:
        linear-gradient(
            135deg,
            rgba(212,175,55,0.15),
            rgba(170,124,17,0.08)
        );
    color: #F3DF76;
    font-weight: 800;
    letter-spacing: 1px;
    transition: 0.3s ease;
}

.stButton > button:hover {
    border-color: #D4AF37;
    background:
        linear-gradient(
            135deg,
            rgba(212,175,55,0.25),
            rgba(170,124,17,0.13)
        );
    color: #FFF4B0;
    box-shadow: 0 0 25px rgba(212,175,55,0.12);
    transform: translateY(-1px);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: rgba(7,7,7,0.85);
    padding: 8px;
    border-radius: 16px;
    border: 1px solid rgba(212,175,55,0.15);
}

.stTabs [data-baseweb="tab"] {
    color: #8e8555;
    border-radius: 10px;
    padding: 12px 16px;
    font-weight: 700;
}

.stTabs [aria-selected="true"] {
    color: #F3DF76 !important;
    background: rgba(212,175,55,0.08) !important;
}

.stAlert {
    border-radius: 14px !important;
}

[data-testid="stFileUploader"] {
    border: 1px dashed rgba(212,175,55,0.35);
    border-radius: 18px;
    background: rgba(15,15,15,0.50);
    padding: 8px;
}

[data-testid="stFileUploader"] section {
    background: transparent !important;
}

[data-testid="stFileUploader"] small {
    color: #8d8352 !important;
}

.stChatMessage {
    border: 1px solid rgba(212,175,55,0.12);
    background: rgba(15,15,15,0.65);
    border-radius: 18px;
}

[data-testid="stChatInput"] {
    border-color: rgba(212,175,55,0.25) !important;
}

[data-testid="stChatInput"] textarea {
    color: #EFE3A1 !important;
    background: #0c0c0c !important;
}

.premium-footer {
    position: relative;
    z-index: 2;
    text-align: center;
    margin-top: 45px;
    padding: 35px 20px;
    border-top: 1px solid rgba(212,175,55,0.15);
    color: #6d6541;
    font-size: 0.78rem;
    letter-spacing: 1px;
}

.footer-brand {
    color: #D4AF37;
    font-family: 'Cinzel', serif;
    font-weight: 800;
    font-size: 1.15rem;
    letter-spacing: 3px;
    margin-bottom: 8px;
}

@media (max-width: 900px) {

    .luxury-nav {
        flex-direction: column;
        text-align: center;
    }

    .luxury-nav-links {
        flex-wrap: wrap;
        justify-content: center;
    }

    .feature-grid {
        grid-template-columns: 1fr;
    }

    .hero-brand {
        letter-spacing: 3px;
    }

    .risk-number {
        font-size: 3.2rem;
    }
}

@media (max-width: 600px) {

    .block-container {
        padding-left: 0.7rem;
        padding-right: 0.7rem;
    }

    .premium-hero {
        padding: 35px 15px;
    }

    .hero-medical-symbol {
        font-size: 3.2rem;
    }

    .hero-description {
        letter-spacing: 1px;
    }

    .luxury-nav-links {
        gap: 10px;
        font-size: 0.78rem;
    }

    .section-heading {
        font-size: 1rem;
    }
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# BACKGROUND
# =========================================================

st.markdown(
    """
    <div class="gold-background">
        <div class="gold-orb one"></div>
        <div class="gold-orb two"></div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# NAVBAR
# =========================================================

st.markdown(
    """
    <div class="luxury-nav">
        <div class="luxury-logo">
            Dr. Omnea Ali
        </div>

        <div class="luxury-nav-links">
            <span>الرئيسية</span>
            <span>عن الدكتورة</span>
            <span>الخدمات الطبية</span>
            <span>الذكاء الاصطناعي</span>
        </div>

        <div class="vip-badge">
            ✦ VIP MEDICAL AI
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="premium-hero">

        <div class="hero-medical-symbol">
            🩺
        </div>

        <div class="hero-subtitle">
            رعاية طبية بمقاييس عالمية
        </div>

        <div class="hero-brand">
            MEDICOGNITIVE AI
        </div>

        <div class="hero-description">
            MULTIMODAL CLINICAL INTELLIGENCE
            •
            AI RADIOLOGY
            •
            EARLY WARNING
            •
            CLINICAL DECISION SUPPORT
        </div>

        <div class="doctor-name">
            الدكتورة أمنية علي
        </div>

        <div class="doctor-title">
            MEDICAL AI RESEARCH & CLINICAL INTELLIGENCE
        </div>

        <div class="ecg-line">
            <svg
                viewBox="0 0 1000 45"
                preserveAspectRatio="none"
            >
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
                    1000,23
                    "
                    fill="none"
                    stroke-width="2"
                />
            </svg>
        </div>

        <div class="system-status">
            <span class="status-dot"></span>
            AI SYSTEM ONLINE
            &nbsp; • &nbsp;
            CLINICAL ENGINE ACTIVE
            &nbsp; • &nbsp;
            MULTIMODAL AI READY
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# FEATURE CARDS
# =========================================================

st.markdown(
    """
    <div class="feature-grid">

        <div class="feature-card">
            <div class="feature-icon">
                ♛
            </div>
            <div class="feature-title">
                رعاية VIP خاصة
            </div>
            <div class="feature-text">
                تجربة طبية متقدمة تجمع الخصوصية
                والدقة وأحدث تقنيات الذكاء الاصطناعي.
            </div>
        </div>

        <div class="feature-card">
            <div class="feature-icon">
                ⚕
            </div>
            <div class="feature-title">
                تشخيص ذكي
            </div>
            <div class="feature-text">
                تحليل متعدد الأبعاد للبيانات السريرية
                والمؤشرات الحيوية والصور الطبية.
            </div>
        </div>

        <div class="feature-card">
            <div class="feature-icon">
                ✦
            </div>
            <div class="feature-title">
                Clinical Intelligence
            </div>
            <div class="feature-text">
                منصة بحثية متقدمة لدعم القرار السريري
                وتحليل المخاطر والاتجاهات الزمنية.
            </div>
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "medical_chat_history" not in st.session_state:
    st.session_state.medical_chat_history = []

if "radiology_result" not in st.session_state:
    st.session_state.radiology_result = None

if "clinical_result" not in st.session_state:
    st.session_state.clinical_result = None

if "risk_result" not in st.session_state:
    st.session_state.risk_result = None


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "👤 PATIENT PROFILE",
        "📈 CLINICAL TRENDS",
        "🩻 AI RADIOLOGY",
        "🧠 AI RISK INTELLIGENCE",
        "💬 AI MEDICAL CHAT",
        "🩺 AI CLINICAL ASSESSMENT"
    ]
)


# =========================================================
# TAB 1 — PATIENT PROFILE
# =========================================================

with tab1:

    st.markdown(
        """
        <div class="section-heading">
            <span>01</span>
            👤 Patient Clinical Profile
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="ai-banner">
            ✦ Clinical intelligence interface ready —
            enter patient parameters to activate AI analysis.
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
            value=62,
            step=1
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
            value=112,
            step=1
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
            value=25,
            step=1
        )

        crp = st.number_input(
            "C-Reactive Protein — CRP (mg/L)",
            min_value=0.0,
            max_value=300.0,
            value=45.0,
            step=0.1
        )

        wbc = st.number_input(
            "White Blood Cell Count — WBC (k/µL)",
            min_value=0.0,
            max_value=50.0,
            value=14.5,
            step=0.1
        )

    st.markdown(
        """
        <div class="section-heading">
            <span>LIVE</span>
            📡 Live Clinical Parameters
        </div>
        """,
        unsafe_allow_html=True
    )

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
                    {temp:.1f}
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

    st.markdown(
        """
        <div class="glass-card">
            <b style="color:#F3DF76;">
                Clinical Profile Summary
            </b>
            <br><br>
            The entered physiological and laboratory parameters
            are available to the AI clinical assessment engine,
            medical assistant and risk intelligence modules.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# TAB 2 — CLINICAL TRENDS
# =========================================================

with tab2:

    st.markdown(
        """
        <div class="section-heading">
            <span>02</span>
            📈 Longitudinal Clinical Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="ai-banner">
            ◈ Temporal AI engine —
            tracking physiological trajectory and deterioration patterns.
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
            name="SpO₂ (%)",
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
            y=mock_hr,
            mode="lines+markers",
            name="Heart Rate (bpm)",
            line=dict(
                color="#AA7C11",
                width=2,
                dash="dot"
            ),
            marker=dict(
                size=6
            )
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
                dash="dash"
            ),
            marker=dict(
                size=6
            )
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(10,10,10,0.5)",
        font=dict(
            color="#D9C77C"
        ),
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20
        ),
        xaxis=dict(
            gridcolor="rgba(212,175,55,0.1)",
            showgrid=True
        ),
        yaxis=dict(
            title=dict(
                text="SpO₂ / Heart Rate",
                font=dict(
                    color="#D4AF37"
                )
            ),
            gridcolor="rgba(212,175,55,0.1)",
            tickfont=dict(
                color="#D4AF37"
            )
        ),
        yaxis2=dict(
            title=dict(
                text="Temp (°C)",
                font=dict(
                    color="#E7C95C"
                )
            ),
            overlaying="y",
            side="right",
            gridcolor="rgba(212,175,55,0.05)",
            tickfont=dict(
                color="#E7C95C"
            )
        ),
        legend=dict(
            font=dict(
                color="#D9C77C"
            )
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        """
        <div class="glass-card">
            <b style="color:#F3DF76;">
                AI Trend Interpretation
            </b>
            <br><br>
            The longitudinal graph provides a visual representation
            of physiological trajectory. The displayed historical
            values are demonstration values unless connected to a
            validated longitudinal patient dataset.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# TAB 3 — AI RADIOLOGY
# =========================================================

with tab3:

    st.markdown(
        """
        <div class="section-heading">
            <span>03</span>
            🩻 AI Radiology & Diagnostic Imaging
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="ai-banner">
            ✦ Multimodal AI radiology engine —
            preliminary X-Ray image interpretation and
            structured radiology intelligence.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="glass-card">

        <b style="color:#F3DF76;">
            RADIOLOGY AI ENGINE
        </b>

        <br><br>

        Upload a radiographic image in JPG, JPEG or PNG format.
        The AI will generate a structured preliminary report.

        <br><br>

        <span style="color:#8f8658;">
        Supported analysis may include fracture location,
        morphology, displacement, angulation, joint involvement,
        alignment, soft-tissue findings and general management
        considerations when visible.
        </span>

        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload Medical X-Ray",
        type=[
            "jpg",
            "jpeg",
            "png"
        ],
        key="radiology_uploader"
    )

    if uploaded_file is not None:

        image_bytes, image, image_error = prepare_medical_image(
            uploaded_file
        )

        if image_error:

            st.error(image_error)

        else:

            st.markdown(
                '<div class="glass-card">',
                unsafe_allow_html=True
            )

            st.image(
                image,
                caption="Uploaded Radiographic Image",
                use_container_width=True
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="glass-card">

                <b style="color:#F3DF76;">
                    IMAGE INFORMATION
                </b>

                <br><br>

                Filename:
                <span style="color:#D4AF37;">
                    {uploaded_file.name}
                </span>

                <br>

                Image Size:
                <span style="color:#D4AF37;">
                    {image.width} × {image.height}
                </span>

                </div>
                """,
                unsafe_allow_html=True
            )

            if st.button(
                "✦ ANALYZE RADIOGRAPH WITH AI",
                key="analyze_xray_button"
            ):

                with st.spinner(
                    "AI radiology engine is analyzing the image..."
                ):

                    radiology_result = analyze_xray_with_ai(
                        image_bytes,
                        uploaded_file.name
                    )

                st.session_state.radiology_result = radiology_result

            if st.session_state.radiology_result:

                st.markdown(
                    """
                    <div class="section-heading">
                        <span>AI</span>
                        🩻 Radiology Report
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="glass-card">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    st.session_state.radiology_result
                )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

                st.warning(
                    "AI-assisted radiology interpretation only. "
                    "Final diagnosis should be confirmed by a qualified radiologist or physician."
                )

    else:

        st.info(
            "Upload an X-Ray image to activate AI-assisted radiographic analysis."
        )


# =========================================================
# TAB 4 — AI RISK INTELLIGENCE
# =========================================================

with tab4:

    st.markdown(
        """
        <div class="section-heading">
            <span>04</span>
            🧠 AI Risk Intelligence & Clinical Assessment
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="ai-banner">
            ✦ Multi-parametric predictive modeling
            for patient deterioration risk.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="glass-card">

        <b style="color:#F3DF76;">
            CURRENT PATIENT PARAMETERS
        </b>

        <br><br>

        The existing clinical risk model receives:

        <br><br>

        Age • Sex • SpO₂ • Heart Rate • Temperature
        • Respiratory Rate • CRP • WBC

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "RUN CLINICAL RISK ASSESSMENT",
        key="run_clinical_risk"
    ):

        try:

            raw_risk_score = clinical_risk_assessment(
                age,
                sex,
                spo2,
                hr,
                temp,
                rr,
                crp,
                wbc
            )

            risk_score = normalize_risk_score(
                raw_risk_score
            )

            st.session_state.risk_result = risk_score

        except Exception as exc:

            st.session_state.risk_result = None

            st.error(
                "Clinical risk model returned an invalid result."
            )

            st.code(
                f"{type(exc).__name__}: {exc}"
            )

    if st.session_state.risk_result is not None:

        risk_score = st.session_state.risk_result

        st.markdown(
            f"""
            <div class="risk-panel">

                <div class="risk-number">
                    {risk_score:.1f}%
                </div>

                <div class="risk-label">
                    PREDICTED CLINICAL RISK SCORE
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if risk_score > 70:

            st.error(
                "HIGH RISK: Immediate clinical attention and close monitoring may be required."
            )

        elif risk_score > 40:

            st.warning(
                "MODERATE RISK: Enhanced physiological monitoring and clinical reassessment advised."
            )

        else:

            st.success(
                "LOWER PREDICTED RISK: Current model output does not indicate high predicted risk."
            )

        st.markdown(
            """
            <div class="glass-card">

            <b style="color:#F3DF76;">
                Risk Interpretation
            </b>

            <br><br>

            This percentage is the output of the configured
            clinical risk model. It should not be interpreted
            as a definitive diagnosis or as a substitute for
            clinical examination.

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# TAB 5 — AI MEDICAL CHAT
# =========================================================

with tab5:

    st.markdown(
        """
        <div class="section-heading">
            <span>05</span>
            💬 AI Medical Clinical Assistant
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="ai-banner">
            ✦ Interactive medical AI —
            clinical reasoning, symptom analysis,
            differential diagnosis and medical education.
        </div>
        """,
        unsafe_allow_html=True
    )

    chat_controls_col1, chat_controls_col2 = st.columns(2)

    with chat_controls_col1:

        st.markdown(
            """
            <div class="glass-card">

            <b style="color:#F3DF76;">
                PATIENT CONTEXT
            </b>

            <br><br>

            Age:
            <b style="color:#D4AF37;">
            """
            + str(age)
            + """
            </b>

            <br>

            Sex:
            <b style="color:#D4AF37;">
            """
            + str(sex)
            + """
            </b>

            <br>

            SpO₂:
            <b style="color:#D4AF37;">
            """
            + str(spo2)
            + """
            %
            </b>

            <br>

            Heart Rate:
            <b style="color:#D4AF37;">
            """
            + str(hr)
            + """
            bpm
            </b>

            </div>
            """,
            unsafe_allow_html=True
        )

    with chat_controls_col2:

        if st.button(
            "CLEAR MEDICAL CHAT",
            key="clear_medical_chat"
        ):

            st.session_state.medical_chat_history = []

            st.rerun()

    for message in st.session_state.medical_chat_history:

        role = message.get("role", "assistant")

        content = message.get("content", "")

        with st.chat_message(role):

            st.markdown(content)

    user_question = st.chat_input(
        "Describe symptoms, medical problem or clinical question..."
    )

    if user_question:

        user_question = user_question.strip()

        if user_question:

            previous_history = list(
                st.session_state.medical_chat_history
            )

            st.session_state.medical_chat_history.append(
                {
                    "role": "user",
                    "content": user_question
                }
            )

            with st.chat_message("user"):

                st.markdown(user_question)

            patient_context = f"""
PATIENT CLINICAL CONTEXT

Age: {age} years
Sex: {sex}

CURRENT VITAL SIGNS:
Temperature: {temp} °C
SpO2: {spo2} %
Heart Rate: {hr} bpm
Respiratory Rate: {rr} /min

LABORATORY PARAMETERS:
CRP: {crp} mg/L
WBC: {wbc} k/uL

PATIENT'S CLINICAL QUESTION:
{user_question}

Provide professional medical reasoning.

Include when relevant:

1. CLINICAL INTERPRETATION
2. POSSIBLE DIAGNOSES
3. DIFFERENTIAL DIAGNOSIS
4. SEVERITY
5. RED FLAGS
6. RECOMMENDED INVESTIGATIONS
7. GENERAL MANAGEMENT CONSIDERATIONS
8. FOLLOW-UP
9. AI SAFETY NOTE

Do not provide medication doses.
Do not claim a definitive diagnosis when insufficient information is available.
"""

            with st.chat_message("assistant"):

                with st.spinner(
                    "Clinical AI is analyzing the case..."
                ):

                    answer = ask_medical_ai(
                        patient_context,
                        conversation_history=previous_history
                    )

                st.markdown(answer)

            st.session_state.medical_chat_history.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


# =========================================================
# TAB 6 — AI CLINICAL ASSESSMENT
# =========================================================

with tab6:

    st.markdown(
        """
        <div class="section-heading">
            <span>06</span>
            🩺 AI Clinical Assessment
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="ai-banner">
            ✦ AI-assisted clinical interpretation based on
            vital signs, laboratory parameters and symptoms.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="glass-card">

        <b style="color:#F3DF76;">
            ENTER / VERIFY CLINICAL PARAMETERS
        </b>

        <br><br>

        These values are sent to the AI clinical reasoning
        engine together with the patient's symptoms.

        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        assessment_temperature = st.number_input(
            "Temperature (°C)",
            min_value=30.0,
            max_value=45.0,
            value=float(temp),
            step=0.1,
            key="assessment_temperature"
        )

        assessment_spo2 = st.slider(
            "Oxygen Saturation — SpO₂ (%)",
            min_value=50,
            max_value=100,
            value=int(spo2),
            key="assessment_spo2"
        )

        assessment_hr = st.number_input(
            "Heart Rate (bpm)",
            min_value=30,
            max_value=220,
            value=int(hr),
            step=1,
            key="assessment_hr"
        )

        assessment_rr = st.number_input(
            "Respiratory Rate (/min)",
            min_value=5,
            max_value=60,
            value=int(rr),
            step=1,
            key="assessment_rr"
        )

    with c2:

        assessment_crp = st.number_input(
            "C-Reactive Protein — CRP (mg/L)",
            min_value=0.0,
            max_value=300.0,
            value=float(crp),
            step=0.1,
            key="assessment_crp"
        )

        assessment_wbc = st.number_input(
            "White Blood Cell Count — WBC (k/µL)",
            min_value=0.0,
            max_value=50.0,
            value=float(wbc),
            step=0.1,
            key="assessment_wbc"
        )

        symptoms = st.text_area(
            "Clinical Symptoms / Patient Complaint",
            placeholder=(
                "Example: fever, productive cough, "
                "dyspnea, chest pain, fatigue..."
            ),
            height=150,
            key="assessment_symptoms"
        )

    st.markdown(
        """
        <div class="section-heading">
            <span>AI</span>
            Clinical Reasoning Engine
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "✦ RUN AI CLINICAL ASSESSMENT",
        key="run_ai_clinical_assessment"
    ):

        if not symptoms.strip():

            st.warning(
                "Please enter the patient's symptoms or clinical complaint."
            )

        else:

            clinical_prompt = f"""
Perform an AI-assisted clinical assessment.

PATIENT PROFILE:

Age:
{age} years

Sex:
{sex}

VITAL SIGNS:

Temperature:
{assessment_temperature} °C

SpO2:
{assessment_spo2} %

Heart Rate:
{assessment_hr} bpm

Respiratory Rate:
{assessment_rr} /min

LABORATORY PARAMETERS:

CRP:
{assessment_crp} mg/L

WBC:
{assessment_wbc} k/uL

SYMPTOMS / CLINICAL COMPLAINT:

{symptoms}

Analyze the case using professional medical English.

Structure the response exactly as:

1. CLINICAL SUMMARY

2. ABNORMAL PARAMETERS

3. CLINICAL INTERPRETATION

4. POSSIBLE DIAGNOSES

5. DIFFERENTIAL DIAGNOSIS

6. SEVERITY ASSESSMENT

7. RED FLAGS

8. RECOMMENDED INVESTIGATIONS

9. GENERAL MANAGEMENT CONSIDERATIONS

10. FOLLOW-UP

11. AI SAFETY NOTE

Important:

- Do not make a definitive diagnosis if information is insufficient.
- Clearly separate measured data from clinical inference.
- Do not fabricate examination findings.
- Do not prescribe medication doses.
- Mention urgent evaluation if red flags are present.
- Use appropriate medical terminology.
"""

            with st.spinner(
                "AI clinical engine is processing the patient data..."
            ):

                clinical_result = ask_medical_ai(
                    clinical_prompt
                )

            st.session_state.clinical_result = clinical_result

    if st.session_state.clinical_result:

        st.markdown(
            """
            <div class="glass-card">
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            st.session_state.clinical_result
        )

        st.markdown(
            """
            </div>
            """,
            unsafe_allow_html=True
        )

        st.warning(
            "This is AI-assisted clinical decision support. "
            "The final diagnosis and treatment decision must be made by a qualified healthcare professional."
        )


# =========================================================
# AI STATUS
# =========================================================

st.markdown(
    """
    <div class="glass-card">

        <b style="color:#F3DF76;">
            ✦ MEDICOGNITIVE AI ENGINE STATUS
        </b>

        <br><br>

        <span style="color:#8f8658;">
            Multimodal Radiology
        </span>

        <span style="color:#D4AF37;">
            •
        </span>

        <span style="color:#8f8658;">
            Clinical Reasoning
        </span>

        <span style="color:#D4AF37;">
            •
        </span>

        <span style="color:#8f8658;">
            Risk Intelligence
        </span>

        <span style="color:#D4AF37;">
            •
        </span>

        <span style="color:#8f8658;">
            Medical Conversational AI
        </span>

    </div>
    """,
    unsafe_allow_html=True
)


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
            Developed for Dr. Omnia Ali
            •
            Clinical Decision Support System
            •
            AI Research Platform
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

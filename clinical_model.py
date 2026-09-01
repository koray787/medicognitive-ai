import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# ---------------------------------------------------------
# MEDICOGNITIVE AI - Clinical Risk Model
# ---------------------------------------------------------

FEATURE_NAMES = [
    "age",
    "sex",
    "spo2",
    "heart_rate",
    "temperature",
    "respiratory_rate",
    "crp",
    "wbc"
]


def prepare_input(
    age,
    sex,
    spo2,
    heart_rate,
    temperature,
    respiratory_rate,
    crp,
    wbc
):
    sex_value = 1 if sex == "Male" else 0

    return np.array([[
        age,
        sex_value,
        spo2,
        heart_rate,
        temperature,
        respiratory_rate,
        crp,
        wbc
    ]])


def calculate_clinical_features(
    age,
    sex,
    spo2,
    heart_rate,
    temperature,
    respiratory_rate,
    crp,
    wbc
):
    """
    Temporary clinical feature engine.

    This is a prototype layer.
    The final competition version will use a model
    trained and validated on an appropriate clinical dataset.
    """

    features = prepare_input(
        age,
        sex,
        spo2,
        heart_rate,
        temperature,
        respiratory_rate,
        crp,
        wbc
    )

    return features


def get_feature_contributions(
    age,
    sex,
    spo2,
    heart_rate,
    temperature,
    respiratory_rate,
    crp,
    wbc
):
    """
    Provides interpretable clinical factors for the prototype.
    """

    contributions = {
        "SpO₂": 0,
        "Heart Rate": 0,
        "Temperature": 0,
        "Respiratory Rate": 0,
        "CRP": 0,
        "WBC": 0,
        "Age": 0
    }

    if spo2 < 92:
        contributions["SpO₂"] = 3
    elif spo2 < 95:
        contributions["SpO₂"] = 1

    if heart_rate >= 120:
        contributions["Heart Rate"] = 3
    elif heart_rate >= 100:
        contributions["Heart Rate"] = 2

    if temperature >= 39:
        contributions["Temperature"] = 3
    elif temperature >= 38.5:
        contributions["Temperature"] = 2

    if respiratory_rate >= 30:
        contributions["Respiratory Rate"] = 3
    elif respiratory_rate >= 22:
        contributions["Respiratory Rate"] = 1

    if crp >= 100:
        contributions["CRP"] = 3
    elif crp >= 40:
        contributions["CRP"] = 2

    if wbc >= 20:
        contributions["WBC"] = 3
    elif wbc >= 12:
        contributions["WBC"] = 2

    if age >= 75:
        contributions["Age"] = 2
    elif age >= 65:
        contributions["Age"] = 1

    return contributions


def clinical_risk_assessment(
    age,
    sex,
    spo2,
    heart_rate,
    temperature,
    respiratory_rate,
    crp,
    wbc
):
    """
    Prototype risk assessment.

    Returns:
        score
        risk_level
        contributions
    """

    contributions = get_feature_contributions(
        age,
        sex,
        spo2,
        heart_rate,
        temperature,
        respiratory_rate,
        crp,
        wbc
    )

    raw_score = sum(contributions.values())

    max_score = 20

    score = round((raw_score / max_score) * 100)

    if score >= 70:
        risk_level = "HIGH"
    elif score >= 40:
        risk_level = "MODERATE"
    else:
        risk_level = "LOW"

    return score, risk_level, contributions

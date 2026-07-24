import numpy as np

# ============================================================
# CONSTANTS
# ============================================================

CRITIC_WEIGHTS = {
    "CEI": 0.3624,
    "API": 0.3120,
    "BWI": 0.3257
}


# ============================================================
# BASIC UTILITIES
# ============================================================

def clip_value(value, lower=0.0, upper=100.0):
    """Simple clipping (demo replacement for notebook winsorization)."""
    return np.clip(value, lower, upper)


def normalize(value, min_val, max_val):
    """Min-Max normalization to [0,1]."""

    if max_val == min_val:
        return 0.0

    value = np.clip(value, min_val, max_val)

    return (value - min_val) / (max_val - min_val)


# ============================================================
# EEG PROCESSING
# ============================================================

def theta_beta_ratio(theta, beta):

    beta = max(beta, 1e-6)

    return theta / beta


def activation_pc1(theta_norm, beta_norm):
    """
    Approximation of PCA projection.

    Later this can be replaced by:
    pca_model.transform([[theta,beta]])
    """

    return 0.6 * theta_norm + 0.4 * beta_norm


def compute_cei(theta, beta):

    # --------------------------------------------------------
    # Notebook style pipeline
    # Theta
    # Beta
    # ↓
    # TBR
    # ↓
    # Normalization
    # ↓
    # PCA
    # ↓
    # Activation_PC1
    # +
    # Attention_TBR
    # ↓
    # CEI
    # --------------------------------------------------------

    theta = clip_value(theta)
    beta = clip_value(beta)

    theta_norm = normalize(theta, 0, 100)
    beta_norm = normalize(beta, 0, 100)

    activation = activation_pc1(theta_norm, beta_norm)

    tbr = theta_beta_ratio(theta, beta)

    attention = normalize(tbr, 0, 5)

    cei = (activation + attention) / 2

    cei = np.clip(cei, 0, 1)

    return {
        "Theta": theta,
        "Beta": beta,
        "Theta_Norm": theta_norm,
        "Beta_Norm": beta_norm,
        "TBR": tbr,
        "Attention_TBR": attention,
        "Activation_PC1": activation,
        "CEI": cei
    }


# ============================================================
# WELLNESS
# ============================================================

def compute_bwi(stress,
                sleep,
                mental_health,
                social_level,
                social_support):

    stress = normalize(stress, 0, 100)

    sleep = normalize(sleep, 0, 100)

    mental_health = normalize(mental_health, 0, 100)

    social_level = normalize(social_level, 0, 100)

    social_support = normalize(social_support, 0, 100)

    bwi = np.mean([
        stress,
        sleep,
        mental_health,
        social_level,
        social_support
    ])

    return np.clip(bwi, 0, 1)


# ============================================================
# ACADEMIC
# ============================================================

def compute_api(engagement,
                assessment,
                performance):

    engagement = normalize(engagement, 0, 100)

    assessment = normalize(assessment, 0, 100)

    performance = normalize(performance, 0, 100)

    api = np.mean([
        engagement,
        assessment,
        performance
    ])

    return np.clip(api, 0, 1)


# ============================================================
# CLRI
# ============================================================

def compute_clri(cei, api, bwi):

    clri = (
        CRITIC_WEIGHTS["CEI"] * cei
        + CRITIC_WEIGHTS["API"] * api
        + CRITIC_WEIGHTS["BWI"] * bwi
    )

    return np.clip(clri, 0, 1)


# ============================================================
# INTERPRETATION
# ============================================================

def readiness_label(score):

    if score < 0.25:
        return "Very Low"

    elif score < 0.50:
        return "Moderate"

    elif score < 0.75:
        return "High"

    return "Excellent"


def recommendation(score):

    if score < 0.25:
        return (
            "Significant intervention recommended. "
            "Consider improving cognitive engagement, "
            "wellness, and academic preparedness."
        )

    elif score < 0.50:
        return (
            "Moderate readiness detected. "
            "Targeted academic and wellness support "
            "is recommended."
        )

    elif score < 0.75:
        return (
            "Good learning readiness. "
            "Maintain healthy habits and continue "
            "improving engagement."
        )

    return (
        "Excellent learning readiness. "
        "Current cognitive, behavioural, and academic "
        "indicators are well balanced."
    )

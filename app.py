import streamlit as st
import pandas as pd
import numpy as np

from utils import (
    compute_cei,
    compute_api,
    compute_bwi,
    compute_clri,
    readiness_label,
    recommendation,
    CRITIC_WEIGHTS
)

from visualizations import (
    gauge_chart,
    radar_chart,
    critic_bar
)

from styles import CSS


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Composite Learning Readiness Framework",
    page_icon="🧠",
    layout="wide"
)

st.markdown(CSS, unsafe_allow_html=True)

st.title("🧠 Composite Learning Readiness Framework")
st.caption("Educational Decision Support Dashboard")


# ---------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------

col1, col2, col3 = st.columns(3)

# ==============================
# EEG
# ==============================

with col1:

    st.subheader("EEG Domain")

    theta = st.number_input(
        "Theta Power",
        min_value=0.0,
        max_value=100.0,
        value=25.0,
        step=0.1
    )

    beta = st.number_input(
        "Beta Power",
        min_value=0.1,
        max_value=100.0,
        value=12.0,
        step=0.1
    )

# ==============================
# Behaviour
# ==============================

with col2:

    st.subheader("Behavioural Wellness")

    stress = st.slider(
        "Stress Level",
        0,
        100,
        70
    )

    sleep = st.slider(
        "Sleep Quality",
        0,
        100,
        75
    )

    mental = st.slider(
        "Mental Health",
        0,
        100,
        80
    )

    social = st.slider(
        "Social Interaction",
        0,
        100,
        65
    )

    support = st.slider(
        "Social Support",
        0,
        100,
        85
    )

# ==============================
# Academic
# ==============================

with col3:

    st.subheader("Academic Performance")

    engagement = st.slider(
        "Engagement",
        0,
        100,
        80
    )

    assessment = st.slider(
        "Assessment",
        0,
        100,
        74
    )

    performance = st.slider(
        "Performance",
        0,
        100,
        78
    )


st.divider()


generate = st.button(
    "Generate Composite Learning Readiness Index",
    use_container_width=True
)

# ==========================================================
# COMPUTATION
# ==========================================================

if generate:

    eeg = compute_cei(theta, beta)

    cei = eeg["CEI"]

    api = compute_api(
        engagement,
        assessment,
        performance
    )

    bwi = compute_bwi(
        stress,
        sleep,
        mental,
        social,
        support
    )

    clri = compute_clri(
        cei,
        api,
        bwi
    )

    st.success("Pipeline Executed Successfully")

    st.divider()

    st.header("Intermediate Processing")

    proc1, proc2, proc3 = st.columns(3)

    with proc1:

        st.markdown("### EEG Processing")

        st.write(f"**Theta:** {theta:.2f}")

        st.write(f"**Beta:** {beta:.2f}")

        st.write(f"**Theta/Beta Ratio:** {eeg['TBR']:.3f}")

        st.write(
            f"**Activation_PC1:** {eeg['Activation_PC1']:.3f}"
        )

        st.write(
            f"**Attention_TBR:** {eeg['Attention_TBR']:.3f}"
        )

        st.write(
            f"**Cognitive Engagement Index:** {cei:.3f}"
        )
    with proc2:

        st.markdown("### Behaviour Processing")

        st.write("Stress → Normalization")

        st.progress(float(stress) / 100)

        st.write("Sleep → Normalization")

        st.progress(float(sleep) / 100)

        st.write("Mental Health → Normalization")

        st.progress(float(mental) / 100)

        st.write("Social Interaction → Normalization")

        st.progress(float(social) / 100)

        st.write("Social Support → Normalization")

        st.progress(float(support) / 100)

        st.markdown("---")

        st.metric(
            "Behaviour Wellness Index (BWI)",
            f"{bwi:.3f}"
        )


    with proc3:

        st.markdown("### Academic Processing")

        st.write("Engagement → Normalization")

        st.progress(float(engagement) / 100)

        st.write("Assessment → Normalization")

        st.progress(float(assessment) / 100)

        st.write("Performance → Normalization")

        st.progress(float(performance) / 100)

        st.markdown("---")

        st.metric(
            "Academic Performance Index (API)",
            f"{api:.3f}"
        )

    st.divider()

    st.header("Domain Representations")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "CEI",
            f"{cei:.3f}"
        )

    with m2:
        st.metric(
            "API",
            f"{api:.3f}"
        )

    with m3:
        st.metric(
            "BWI",
            f"{bwi:.3f}"
        )

    st.divider()

    st.header("CRITIC Objective Weighting")

    critic_df = pd.DataFrame({

        "Domain": [
            "CEI",
            "API",
            "BWI"
        ],

        "Weight": [
            CRITIC_WEIGHTS["CEI"],
            CRITIC_WEIGHTS["API"],
            CRITIC_WEIGHTS["BWI"]
        ]

    })

    st.dataframe(
        critic_df,
        use_container_width=True,
        hide_index=True
    )

    st.plotly_chart(
        critic_bar(CRITIC_WEIGHTS),
        use_container_width=True
    )

    st.divider()

    st.header("Composite Learning Readiness Index")

    g1, g2 = st.columns([2, 1])

    with g1:

        st.plotly_chart(
            gauge_chart(clri),
            use_container_width=True
        )

    with g2:

        st.metric(
            "CLRI",
            f"{clri:.3f}"
        )

        st.metric(
            "Readiness",
            readiness_label(clri)
        )

        st.progress(clri)

        st.write(
            recommendation(clri)
        )

    st.divider()

    st.header("Learning Readiness Profile")

    st.plotly_chart(
        radar_chart(
            cei,
            api,
            bwi
        ),
        use_container_width=True
    )
        st.divider()

    st.header("Framework Summary")

    st.markdown("""
### Composite Learning Readiness Framework Pipeline

**EEG Domain**
- Theta Power
- Beta Power
- Theta/Beta Ratio
- Activation_PC1
- Attention_TBR
- **Cognitive Engagement Index (CEI)**

**Behaviour Domain**
- Stress
- Sleep
- Mental Health
- Social Interaction
- Social Support
- **Behaviour Wellness Index (BWI)**

**Academic Domain**
- Engagement
- Assessment
- Performance
- **Academic Performance Index (API)**

These three domain representations are fused using **CRITIC objective weighting** to compute the final Composite Learning Readiness Index.
""")

    st.latex(
        r"CLRI = 0.3624\times CEI + 0.3120\times API + 0.3257\times BWI"
    )

    st.divider()

    st.header("Computed Results")

    results = pd.DataFrame({
        "Metric": [
            "Activation_PC1",
            "Attention_TBR",
            "CEI",
            "API",
            "BWI",
            "CLRI"
        ],
        "Value": [
            round(eeg["Activation_PC1"], 3),
            round(eeg["Attention_TBR"], 3),
            round(cei, 3),
            round(api, 3),
            round(bwi, 3),
            round(clri, 3)
        ]
    })

    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True
    )

    csv = results.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Results (.csv)",
        csv,
        "CLRI_results.csv",
        "text/csv",
        use_container_width=True
    )

    st.divider()

    st.info(
        "This dashboard demonstrates the Composite Learning Readiness Framework "
        "developed during the project. EEG representations are derived from "
        "Activation_PC1 and Attention_TBR, Behaviour and Academic representations "
        "are normalized to a common scale, and the final CLRI is computed using "
        "CRITIC objective weights."
    )

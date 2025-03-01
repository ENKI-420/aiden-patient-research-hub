import streamlit as st
import os
from modules.digital_twins import generate_digital_twin
from modules.tumor_evolution import predict_tumor_evolution
from modules.crispr_ai import analyze_crispr_feasibility
from modules.nanoparticle_simulation import simulate_nanoparticle_delivery

# Load API keys from Streamlit secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Sidebar Navigation
st.sidebar.title("🩺 AGILE Oncology AI Hub")
page = st.sidebar.radio("Navigation", ["Digital Twin AI", "Tumor Evolution", "CRISPR AI", "Nanoparticle AI"])

# Page Logic
if page == "Digital Twin AI":
    st.title("👥 Digital Twin AI System")
    patient_id = st.text_input("Enter Patient ID:")
    if st.button("Generate Digital Twin"):
        result = generate_digital_twin(patient_id)
        st.json(result)

elif page == "Tumor Evolution":
    st.title("🔬 Tumor Evolution Prediction")
    patient_id = st.text_input("Enter Patient ID:")
    if st.button("Predict Tumor Evolution"):
        result = predict_tumor_evolution(patient_id, ["TP53", "KRAS"])
        st.json(result)

elif page == "CRISPR AI":
    st.title("🧬 CRISPR Editing Feasibility AI")
    patient_id = st.text_input("Enter Patient ID:")
    if st.button("Analyze CRISPR Feasibility"):
        result = analyze_crispr_feasibility(patient_id, ["BRAF", "EGFR"])
        st.json(result)

elif page == "Nanoparticle AI":
    st.title("💊 Nanoparticle Drug Delivery AI")
    patient_id = st.text_input("Enter Patient ID:")
    if st.button("Simulate Drug Delivery"):
        result = simulate_nanoparticle_delivery(patient_id)
        st.json(result)

st.sidebar.caption("🔗 Powered by AI-driven Precision Medicine")

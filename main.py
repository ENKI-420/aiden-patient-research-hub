import streamlit as st
from models.ai_agents import MultiAgentRiskModel
from utils.fhir_data import authenticate_epic, fetch_genomic_data

st.sidebar.header("🩺 AGILE Oncology Research Hub")
selected_option = st.sidebar.radio("Select a module:", [
    "Mutation Risk Assessment",
    "Tumor Evolution Prediction",
    "Digital Twin AI",
    "CRISPR Editing AI",
    "Nanoparticle Drug Delivery AI",
    "Blockchain Pharmacovigilance"
])

st.title(f"🚀 {selected_option}")
st.caption("AI-driven mutation risk prediction for personalized cancer treatment.")

if selected_option == "Mutation Risk Assessment":
    st.subheader("🧬 Predict Oncogenic Risk from Mutations")
    
    if st.button("Authenticate with Epic"):
        auth_token = authenticate_epic()
        if auth_token:
            st.session_state["auth_token"] = auth_token
            st.success("✅ Epic Authentication Successful!")

    patient_id = st.text_input("Enter Patient ID for AI Risk Assessment")

    if st.button("Run AI Risk Analysis"):
        auth_token = st.session_state.get("auth_token")
        if auth_token:
            genomic_data = fetch_genomic_data(patient_id, auth_token)
            if genomic_data:
                st.json(genomic_data)
                st.write("### 🦾 AI-Powered Mutation Risk Score")

                mutation_data = [{"pathogenicity_score": 5} for _ in range(5)]
                model = MultiAgentRiskModel(num_agents=3, mutation_data=mutation_data)
                risk_score = model.run_model()

                st.write(f"🧬 Estimated Risk Score: **{risk_score:.2f}**")
            else:
                st.error("❌ No genomic data found for the patient.")
        else:
            st.error("❌ Please log in to Epic first.")

st.caption("🔗 Powered by AGILE AI | Epic EHR | AI-Driven Precision Medicine")
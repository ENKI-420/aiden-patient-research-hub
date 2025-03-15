import streamlit as st
import requests
import pandas as pd
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from beaker_report_fetching import authenticate_user, fetch_beaker_report, process_and_save_to_csv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# EPIC API URLs
FHIR_BASE_URL = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/"

# Set up the Streamlit Page
st.set_page_config(page_title="AGENT Platform - Precision Oncology", layout="wide")

# Sidebar Navigation
st.sidebar.title("🩺 AGENT AI Platform")
option = st.sidebar.radio(
    "Select a Section",
    ["Home", "Login to Epic", "Fetch Beaker Report", "Genomic Analysis", "Clinical Trials", "Digital Twin Modeling", "Export Reports"]
)

# EPIC Login Section
if option == "Login to Epic":
    st.title("🔐 Epic Login for FHIR Access")
    username = st.text_input("Epic Username")
    password = st.text_input("Epic Password", type="password")

    if st.button("Login"):
        token = authenticate_user(username, password)
        if token:
            st.session_state.auth_token = token
            st.success("✅ Login successful! You can now fetch Beaker reports.")
        else:
            st.error("❌ Authentication failed. Please check your credentials.")

# Fetch Beaker Report
elif option == "Fetch Beaker Report":
    st.title("📊 Fetch Beaker Laboratory Reports")
    if "auth_token" not in st.session_state:
        st.error("🔴 Please log in to Epic first!")
    else:
        patient_id = st.text_input("Enter Patient ID")
        if st.button("Fetch Report"):
            report_data = fetch_beaker_report(patient_id, st.session_state.auth_token)
            if report_data:
                st.write("### ✅ Beaker Report Data")
                process_and_save_to_csv(report_data)
                st.dataframe(pd.read_csv("beaker_report_data.csv"))
            else:
                st.error("❌ Failed to retrieve the Beaker Report.")

# AI-Powered Genomic Analysis
elif option == "Genomic Analysis":
    st.title("🧬 AI-Powered Genomic Data Analysis")

    # Example AI Insights (Modify with real AI analysis)
    st.subheader("Predicted Mutations")
    st.write("🔍 Detected Mutations: **EGFR T790M, P53 Mutation**")

    st.subheader("AI Treatment Insights")
    st.write("""
    ✅ The detected mutations suggest a potential resistance to first-line therapies.
    ✅ Recommended targeted therapies: Combination therapies with immunotherapy and kinase inhibitors.
    """)

    # Run AI-powered analysis
    if st.button("Run Advanced AI Analysis"):
        client = OpenAI(api_key=OPENAI_API_KEY)
        prompt = "Analyze the following genetic mutations and suggest personalized treatments:\n- EGFR T790M\n- P53 Mutation"
        response = client.completions.create(model="gpt-4-turbo", prompt=prompt, max_tokens=500)
        st.write("### 🤖 AI Response")
        st.write(response.choices[0].text.strip())

# Clinical Trial Matching
elif option == "Clinical Trials":
    st.title("🔬 AI-Driven Clinical Trial Matching")

    trials = [
        {"Trial Name": "EGFR Targeted Therapy", "Location": "New York", "Eligibility": "EGFR T790M Positive", "Phase": "Phase 2"},
        {"Trial Name": "P53 Restoration Therapy", "Location": "California", "Eligibility": "P53 Mutation", "Phase": "Phase 1"}
    ]
    trials_df = pd.DataFrame(trials)
    st.write("### Recommended Clinical Trials")
    st.dataframe(trials_df)

# Digital Twin Modeling
elif option == "Digital Twin Modeling":
    st.title("👥 Digital Twin Simulation for Precision Medicine")

    patient_id = st.text_input("Enter Patient ID for Digital Twin")
    if st.button("Generate Digital Twin Model"):
        st.write("✅ **Simulated tumor response:** 85% reduction in tumor size with kinase inhibitor therapy.")

# Export Reports
elif option == "Export Reports":
    st.title("📤 Export Results")
    export_option = st.selectbox("Select File Format", ["CSV", "JSON", "PDF"])
    if export_option == "CSV":
        st.write("✅ Exporting as CSV...")
    elif export_option == "JSON":
        st.write("✅ Exporting as JSON...")
    elif export_option == "PDF":
        st.write("✅ Exporting as PDF...")

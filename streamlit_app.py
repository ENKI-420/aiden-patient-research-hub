import streamlit as st
import requests
import pandas as pd
import os
import time
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Constants
FHIR_BASE_URL = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4/"
OAUTH_URL = "https://fhir.epic.com/interconnect-fhir-oauth/oauth2/token"
TRIALS_API_URL = "https://api.3oncologyresearchhub.com/v2/studies"

# Load OpenAI API Key from .env
openai_api_key = os.getenv("OPENAI_API_KEY", "")

# Sidebar Configuration
with st.sidebar:
    st.header("🩺 Norton Oncology Research Hub")
    st.subheader("📌 Navigation")
    
    menu_options = [
        "Chatbot",
        "File Q&A",
        "Chat with Search",
        "Beaker Report Analysis",
        "Genomic AI Analysis",
        "Clinical Trial Matching"
    ]
    selected_option = st.radio("Select a module:", menu_options)

    st.subheader("🔑 OpenAI API Key")
    openai_api_key = st.text_input("Enter your OpenAI API Key", value=openai_api_key, type="password")

    st.subheader("🔗 Quick Links")
    st.markdown("[Get an OpenAI API Key](https://platform.openai.com/account/api-keys)")
    st.markdown("[Epic EHR Integration](https://www.epic.com/)")

# Display selected module
st.title(f"🚀 {selected_option}")
st.caption("AI-driven oncology assistant for research and precision medicine.")

# Epic Authentication Function
def authenticate_epic(username, password):
    payload = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "client_id": os.getenv("EPIC_CLIENT_ID", ""),
        "client_secret": os.getenv("EPIC_CLIENT_SECRET", "")
    }
    try:
        response = requests.post(OAUTH_URL, data=payload)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.RequestException as e:
        st.error(f"Epic Authentication Failed: {e}")
        return None

# Fetch Beaker Report
def fetch_beaker_report(patient_id, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}", "Accept": "application/fhir+json"}
    try:
        response = requests.get(f"{FHIR_BASE_URL}DiagnosticReport?patient={patient_id}", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch Beaker Report: {e}")
        return None

# Process Beaker Report
def process_beaker_report(report_data):
    records = report_data.get("entry", [])
    processed = [
        {
            "Test Name": r.get("resource", {}).get("code", {}).get("text", ""),
            "Result": r.get("resource", {}).get("result", ""),
            "Status": r.get("resource", {}).get("status", "")
        } for r in records
    ]
    return pd.DataFrame(processed) if processed else pd.DataFrame(columns=["Test Name", "Result", "Status"])

# AI Treatment Suggestions
def generate_ai_treatment_suggestions(test_results):
    if not openai_api_key:
        st.error("OpenAI API Key is missing. Please provide a valid key.")
        return None
    client = OpenAI(api_key=openai_api_key)
    prompt = f"Analyze these oncology test results and provide treatment suggestions:\n{test_results.to_string(index=False)}"
    
    try:
        response = client.completions.create(model="gpt-4-turbo", prompt=prompt, max_tokens=500)
        return response.choices[0].text.strip() if response.choices else "No response received."
    except Exception as e:
        st.error(f"Error generating AI treatment suggestions: {e}")
        return None

# Fetch Clinical Trials
def fetch_clinical_trials():
    try:
        response = requests.get(TRIALS_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Failed to fetch clinical trials: {e}")
        return None

# Epic Login UI
st.subheader("🔐 Epic EHR Login (Optional)")
epic_username = st.text_input("Epic Username")
epic_password = st.text_input("Epic Password", type="password")

if st.button("Login to Epic"):
    with st.spinner("Authenticating..."):
        token = authenticate_epic(epic_username, epic_password)
        if token:
            st.session_state["auth_token"] = token
            st.success("Epic Authentication Successful ✅")

# AI Chatbot
st.subheader("💬 AI-Powered Oncology Chatbot")
prompt = st.text_area("Ask a question about cancer treatment, trials, or genomic analysis")
if st.button("Get AI Response"):
    if prompt and openai_api_key:
        with st.spinner("Processing..."):
            client = OpenAI(api_key=openai_api_key)
            try:
                response = client.chat.completions.create(model="gpt-4-turbo", messages=[{"role": "user", "content": prompt}])
                st.write("### 🤖 AI Response")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Failed to retrieve AI response: {e}")
    else:
        st.error("Please enter a prompt and ensure the OpenAI API key is provided.")

# Beaker Report Section
st.subheader("📊 Fetch & Analyze Beaker Report")
patient_id = st.text_input("Enter Patient ID for Beaker Report")

if st.button("Fetch Report"):
    auth_token = st.session_state.get("auth_token")
    if auth_token:
        with st.spinner("Fetching Beaker Report..."):
            report_data = fetch_beaker_report(patient_id, auth_token)
            if report_data:
                test_results = process_beaker_report(report_data)
                st.dataframe(test_results)
                if not test_results.empty:
                    st.write("### 🤖 AI-Powered Treatment Insights")
                    ai_response = generate_ai_treatment_suggestions(test_results)
                    if ai_response:
                        st.write(ai_response)
    else:
        st.error("Please log in to Epic first.")

# Clinical Trial Matching Section
st.subheader("🔬 AI-Driven Clinical Trial Matching")
if st.button("Find Clinical Trials"):
    with st.spinner("Fetching clinical trials..."):
        trial_data = fetch_clinical_trials()
        if trial_data:
            st.json(trial_data)

st.caption("🔗 Powered by Agile Defense Systems | Norton Oncology | Epic EHR | AI-Driven Precision Medicine")

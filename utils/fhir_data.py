import requests
import os

FHIR_BASE_URL = os.getenv("FHIR_BASE_URL")
OAUTH_URL = os.getenv("OAUTH_URL")

def authenticate_epic():
    payload = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("EPIC_CLIENT_ID"),
        "client_secret": os.getenv("EPIC_CLIENT_SECRET")
    }
    response = requests.post(OAUTH_URL, data=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None

def fetch_genomic_data(patient_id, auth_token):
    headers = {"Authorization": f"Bearer {auth_token}", "Accept": "application/fhir+json"}
    response = requests.get(f"{FHIR_BASE_URL}Observation?patient={patient_id}", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None
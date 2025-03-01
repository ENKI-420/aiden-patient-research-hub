from api_oncolo_ai__jit_plugin import treatmentPathwayRecommendation

def generate_digital_twin(patient_id):
    return treatmentPathwayRecommendation(patient_id=patient_id, available_clinical_trials=True)

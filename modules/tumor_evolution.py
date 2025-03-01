from api_oncolo_ai__jit_plugin import tumorEvolutionPrediction

def predict_tumor_evolution(patient_id, current_mutations):
    return tumorEvolutionPrediction(patient_id=patient_id, current_mutations=current_mutations)

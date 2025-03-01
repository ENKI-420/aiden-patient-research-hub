from api_oncolo_ai__jit_plugin import mutationAnalysis

def analyze_crispr_feasibility(patient_id, gene_variants):
    return mutationAnalysis(patient_id=patient_id, gene_variants=gene_variants)

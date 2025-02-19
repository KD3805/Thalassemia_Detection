# File: parse_blood_report.py
import re

def parse_blood_report(text):
    """
    Extracts blood report parameters using regular expressions.
    Expected keys:
      - sex, hb, pcv, rbc, mcv, mch, mchc, rdw, wbc,
        neut, lymph, plt, hba, hba2, hbf.
    
    This function uses robust regex patterns for numeric extraction (similar to your 
    original parse_blood_report logic) and also extracts 'sex' using a simple pattern.
    """
    parameters = {}

    # Extract 'sex' from text.
    sex_match = re.search(r"(?:Sex|Gender)\s*[:\-]?\s*(male|female)", text, re.IGNORECASE)
    parameters['sex'] = sex_match.group(1).lower() if sex_match else None

    # Helper function to extract numeric fields.
    def extract_field(field_names, unit_pattern=""):
        """
        field_names: a list of alternative names for the field.
        unit_pattern: an optional regex pattern for units.
        Returns the first numeric match as a float, or None if not found.
        """
        # Build a pattern that matches any of the provided field names.
        # The pattern will match one of the names, then any non-digit characters, then a numeric value.
        pattern = r"(?:{})[^\d]*(\d+\.?\d*)".format("|".join(field_names))
        if unit_pattern:
            pattern += r"\s*{}".format(unit_pattern)
        match = re.search(pattern, text, re.IGNORECASE)
        try:
            return float(match.group(1)) if match else None
        except Exception:
            return None

    # Use robust patterns based on your model notebook.
    parameters['hb']    = extract_field(['Haemoglobin', 'Hemoglobin', 'Hb'], r"(?:g/dL|g/L|g%)?")
    parameters['pcv']   = extract_field(['PCV', 'Packed Cell Volume', 'Hematocrit'], r"(?:/mm3|x10\^3/µL|x10\^9/L)?")
    parameters['rbc']   = extract_field(['Red Blood Cell Count', 'Total RBC Count', 'RBC Count', r"RBC\s+Count"], r"(?:million/mm3|x10\^6/µL|x10\^12/L)?")
    parameters['mcv']   = extract_field(['Mean Corpuscular Volume', 'MCV'], r"(?:µm3|fL)?")
    parameters['mch']   = extract_field(['Mean Corpuscular Hemoglobin', 'MCH'], r"(?:pg)?")
    parameters['mchc']  = extract_field(['Mean Corpuscular Hemoglobin Concentration', 'MCHC'], r"(?:g/dL)?")
    parameters['rdw']   = extract_field(['RDW', 'Red cell distribution width'], r"(?:g/dL)?")
    parameters['wbc']   = extract_field(['White Blood Cell Count', 'Leukocytes', 'TOTAL WBC COUNT'], r"(?:/mm3|x10\^3/µL|x10\^9/L)?")
    parameters['neut']  = extract_field(['Neutrophils'], r"(?:%|/mm3|x10\^3/µL|x10\^9/L)?")
    parameters['lymph'] = extract_field(['Lymphocytes'], r"(?:%|/mm3|x10\^3/µL|x10\^9/L)?")
    parameters['plt']   = extract_field(['Platelet Count', 'Thrombocytes'], r"(?:/mm3|x10\^3/µL|x10\^9/L)?")
    parameters['hba']   = extract_field(['HbA'])
    parameters['hba2']  = extract_field(['HbA2'])
    parameters['hbf']   = extract_field(['HbF'])

    # Also store the raw text for debugging if needed.
    # parameters["raw_text"] = text
    return parameters

# For testing:
if __name__ == "__main__":
    sample_text = """
    Patient Gender: Female
    Hemoglobin: 10.8 g/dL
    PCV: 35.2%
    RBC Count: 5.12 x10^6/µL
    MCV: 68.7 fL
    MCH: 21.2 pg
    MCHC: 30.8 g/dL
    RDW: 13.4%
    WBC: 9.6 x10^3/µL
    Neutrophils: 53%
    Lymphocytes: 33%
    Platelet Count: 309 x10^3/µL
    HbA: 88.5
    HbA2: 2.6
    HbF: 0.11
    """
    params = parse_blood_report(sample_text)
    print("Extracted Parameters:")
    for key, value in params.items():
        print(f"{key}: {value}")

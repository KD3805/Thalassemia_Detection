# File: ml_model.py
import numpy as np
import joblib
import os

# Use os.path.join for cross-platform compatibility.
working_dir = os.path.dirname(os.path.abspath(__file__))
PICKLE_MODEL_PATH = os.path.join(working_dir, "model", "thalassemia_model.pkl")

if not os.path.exists(PICKLE_MODEL_PATH):
    raise FileNotFoundError(f"Pickle model file not found at {PICKLE_MODEL_PATH}")

def load_model():
    """
    Load the trained model from the pickle file.
    """
    try:
        model = joblib.load(PICKLE_MODEL_PATH)
        return model
    except Exception as e:
        raise RuntimeError("Failed to load the model: " + str(e))

def convert_sex_one_hot(sex: str):
    """
    Convert the 'sex' field to one-hot encoding:
      - 'male'   -> [1, 0]
      - 'female' -> [0, 1]
    """
    if isinstance(sex, str):
        if sex.lower() == "male":
            return [1, 0]
        elif sex.lower() == "female":
            return [0, 1]
    # Fallback if sex is missing or unrecognized.
    return [0, 0]

def predict_thalassemia(features: dict) -> int:
    """
    Predict thalassemia status using the loaded model.
    
    Expected keys in features:
      - sex, hb, pcv, rbc, mcv, mch, mchc, rdw, wbc,
        neut, lymph, plt, hba, hba2, hbf
    
    The model was trained with one-hot encoding for 'sex', so the feature vector
    should contain 2 columns for 'sex' followed by 14 numeric columns (total 16 features).
    Returns:
      - 0 for a normal individual,
      - 1 for an alpha thalassemia carrier.
    """
    # One-hot encode the 'sex' field.
    sex_encoded = convert_sex_one_hot(features.get("sex", "male"))
    
    # Define the order of numeric features.
    numeric_features_keys = [
        "hb", "pcv", "rbc", "mcv", "mch", "mchc",
        "rdw", "wbc", "neut", "lymph", "plt", "hba",
        "hba2", "hbf"
    ]
    numeric_features = []
    for key in numeric_features_keys:
        try:
            numeric_features.append(float(features.get(key, 0)))
        except ValueError:
            numeric_features.append(0.0)
    
    # Combine one-hot encoded 'sex' with numeric features: 2 + 14 = 16 features.
    feature_vector = sex_encoded + numeric_features
    input_array = np.array(feature_vector).reshape(1, -1)

    # Load the model and make a prediction.
    model = load_model()

    try:
        pred = model.predict(input_array)[0]
        print("Prediction probability:", model.predict_proba(input_array))
        return int(pred)
    except Exception as e:
        raise RuntimeError("Error during prediction: " + str(e))

# For testing:
if __name__ == "__main__":
    sample_features = {
        "sex": "female",
        "hb": 10.8,
        "pcv": 35.2,
        "rbc": 5.12,
        "mcv": 68.7,
        "mch": 21.2,
        "mchc": 30.8,
        "rdw": 13.4,
        "wbc": 9.6,
        "neut": 53,
        "lymph": 33,
        "plt": 309,
        "hba": 88.5,
        "hba2": 2.6,
        "hbf": 0.11
    }
    prediction = predict_thalassemia(sample_features)
    print("Prediction (0: Normal, 1: Alpha Carrier):", prediction)

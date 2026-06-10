import joblib
from feature_extractor import extract_features

model = joblib.load("model/trained_model.pkl")

def predict_url(url):
    features = extract_features(url)
    result = model.predict([features])[0]
    prob = model.predict_proba([features])[0].max()

    trust_score = int(prob * 100)

    if result == -1:
        status = "Fraud Website"
    else:
        status = "Genuine Website"

    return status, trust_score

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from feature_extractor import extract_features
from recommend import recommend_sites

app = Flask(__name__)
CORS(app)

model = joblib.load("model/trained_model.pkl")

@app.route("/")
def home():
    return "WebGuard AI Backend is Running"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    url = data["url"].lower()

    # Rule-based check for common phishing keywords
    suspicious_keywords = ["login", "verify", "secure", "free", "update", "bank", "account", "paypal", "amazon"]
    is_suspicious = any(word in url for word in suspicious_keywords)

    if is_suspicious:
        status = "Fraud Website"
        trust_score = 20
        recommendation = "This website looks suspicious and may be a phishing site."
        alternatives = recommend_sites(url)
    else:
        # ML Model prediction
        features = extract_features(url)
        result = model.predict([features])[0]
        probability = model.predict_proba([features])[0].max()
        trust_score = int(probability * 100)

        if result == -1:
            status = "Fraud Website"
            recommendation = "This website is unsafe. Avoid it and use trusted alternatives."
            alternatives = recommend_sites(url)
        else:
            status = "Genuine Website"
            recommendation = "This website is safe to use."
            alternatives = []

    return jsonify({
        "status": status,
        "trust_score": trust_score,
        "recommendation": recommendation,
        "alternatives": alternatives
    })

if __name__ == "__main__":
    app.run(debug=True)

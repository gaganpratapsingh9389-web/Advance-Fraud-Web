import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_curve, auc
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
import joblib
import os

# Load Dataset
data_path = "data/phishing_data.csv"
df = pd.read_csv(data_path)

X = df.drop("Result", axis=1)
y = df["Result"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Stronger Model
base_model = RandomForestClassifier(
    n_estimators=300,
    max_depth=20,
    random_state=42
)

model = OneVsRestClassifier(base_model)
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)

# Accuracy
acc = accuracy_score(y_test, y_pred)
print("Model Accuracy:", acc)

# Precision, Recall, F1
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:\n", cm)

# ROC Curve for Multiclass
classes = [-1, 0, 1]
y_test_bin = label_binarize(y_test, classes=classes)

plt.figure()
for i in range(len(classes)):
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_prob[:, i])
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f"Class {classes[i]} (AUC = {roc_auc:.2f})")

plt.plot([0,1], [0,1], 'k--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Multiclass ROC Curve")
plt.legend()
plt.show()

# Save Model
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/trained_model.pkl")
print("Model saved at model/trained_model.pkl")

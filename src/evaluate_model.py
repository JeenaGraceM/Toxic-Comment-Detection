
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from traditional_classifier import TraditionalToxicClassifier

# Load dataset
df = pd.read_csv("data/sample_dataset.csv")

# Binary label: 1 for toxic, 0 for non-toxic
X = df["comment"]
y = df["label"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train and evaluate
model = TraditionalToxicClassifier()
model.train(X_train, y_train)
report = model.evaluate(X_test, y_test)
print("Classification Report:\n", report)

# Confusion matrix
y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.savefig("docs/confusion_matrix.png")
plt.close()

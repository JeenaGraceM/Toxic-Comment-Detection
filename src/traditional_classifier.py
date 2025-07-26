
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from preprocessing import clean_text

class TraditionalToxicClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.model = LogisticRegression()

    def train(self, X, y):
        X_clean = [clean_text(text) for text in X]
        X_vec = self.vectorizer.fit_transform(X_clean)
        self.model.fit(X_vec, y)
        return self.model

    def predict(self, texts):
        texts_clean = [clean_text(text) for text in texts]
        X_vec = self.vectorizer.transform(texts_clean)
        return self.model.predict(X_vec)

    def evaluate(self, X, y_true):
        X_clean = [clean_text(text) for text in X]
        X_vec = self.vectorizer.transform(X_clean)
        y_pred = self.model.predict(X_vec)
        return classification_report(y_true, y_pred, output_dict=True)

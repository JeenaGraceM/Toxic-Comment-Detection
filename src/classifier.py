import numpy as np
from transformers import AutoTokenizer, AutoModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from textblob import TextBlob
import torch
import string

# Load BERT model and tokenizer
MODEL_NAME = "unitary/toxic-bert"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
bert_model = AutoModel.from_pretrained(MODEL_NAME)

# Define bad words for handcrafted features
bad_words = {"hate", "stupid", "idiot", "dumb", "worst", "horrible"}

# Example data for fitting TF-IDF (you can replace with actual dataset)
example_texts = [
    "You are a horrible person!",
    "I love this product, very useful.",
    "This is the worst comment I've ever seen.",
    "Great job, well done!",
    "I hate you and your stupid posts."
]
labels = [1, 0, 1, 0, 1]

# Fit TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=100)
tfidf_vectorizer.fit(example_texts)

# === Feature extractors ===
def get_bert_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

def get_tfidf_embedding(text):
    return tfidf_vectorizer.transform([text]).toarray().squeeze()

def extract_handcrafted_features(text):
    words = text.split()
    return np.array([
        len(text),
        len(words),
        sum(1 for word in words if word.isupper()),
        text.count("!"),
        sum(1 for word in words if word.lower() in bad_words),
        sum(1 for c in text if c in string.punctuation) / max(1, len(text))
    ])

def get_sentiment_score(text):
    return np.array([TextBlob(text).sentiment.polarity])

def combine_features(bert_emb, tfidf_emb, handcrafted, sentiment):
    return np.concatenate([bert_emb, tfidf_emb, handcrafted, sentiment])

# Train initial classifier on small demo set
X_train = [
    combine_features(
        get_bert_embedding(t),
        get_tfidf_embedding(t),
        extract_handcrafted_features(t),
        get_sentiment_score(t)
    )
    for t in example_texts
]

clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, labels)

# === Final classification function used in dashboard ===
def classify_text(text):
    bert_emb = get_bert_embedding(text)
    tfidf_emb = get_tfidf_embedding(text)
    handcrafted = extract_handcrafted_features(text)
    sentiment = get_sentiment_score(text)
    features = combine_features(bert_emb, tfidf_emb, handcrafted, sentiment)
    proba = clf.predict_proba([features])[0]
    pred = clf.predict([features])[0]
    return {
        "prediction": int(pred),
        "probability_non_toxic": round(float(proba[0]), 3),
        "probability_toxic": round(float(proba[1]), 3)
    }

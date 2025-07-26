from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_NAME = "unitary/toxic-bert"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

LABELS = ["Toxic", "Severe Toxic", "Obscene", "Threat", "Insult", "Identity Hate"]

def classify_message(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    probs = torch.sigmoid(outputs.logits)[0].detach().numpy()
    return {label: round(float(score), 3) for label, score in zip(LABELS, probs)}
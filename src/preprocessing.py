import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Check and download required NLTK data only if missing
def ensure_nltk_data():
    try:
        stopwords.words('english')
    except LookupError:
        nltk.download('stopwords')
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')
    try:
        nltk.data.find('corpora/omw-1.4')  # Optional but good for better lemmatization
    except LookupError:
        nltk.download('omw-1.4')

ensure_nltk_data()

# Initialize tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# Main cleaning function
def clean_text(text):
    text = re.sub(r"http\S+|@\S+|#\S+", "", text.lower())
    text = re.sub(r"[^\w\s]", "", text)
    tokens = [lemmatizer.lemmatize(w) for w in text.split() if w not in stop_words]
    return " ".join(tokens)

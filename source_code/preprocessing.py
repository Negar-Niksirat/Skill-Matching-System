import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def normalize_text(text):
    if isinstance(text, str):
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text)
        return text
    return ''

def load_data(filepath):
    df = pd.read_csv(filepath)
    return df

def generate_TFIDF(df):
    vectorizer = TfidfVectorizer(stop_words='english')
    x = vectorizer.fit_transform(df['normalized_resume'])
    return x, vectorizer 

def preprocess_text(text):
            normalized_text = normalize_text(text)
            stop_words = set(stopwords.words('english'))
            def tokenize_and_filter(text):
                tokens = word_tokenize(text)  
                return [w for w in tokens if w not in stop_words]
            return tokenize_and_filter(normalized_text)


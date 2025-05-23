import joblib
import numpy as np
from source_code.preprocessing import normalize_text

model = joblib.load('models/naive_bayes_model.pkl')
vectorizer = joblib.load('models/tfidf_vectorizer.pkl')

def predict_3_top_job(resume_text):
    if not resume_text.strip():
        return []
    cleaned_resume = normalize_text(resume_text)
    x= vectorizer.transform([cleaned_resume])

    probs = model.predict_proba(x)[0]
    classes = model.classes_

    top_indices = np.argsort(probs)[-3:][::-1]
    top_3_roles = classes[top_indices]
    return top_3_roles
    

def predict_top_job(resume_text):
    if not resume_text.strip():
        return []
    cleaned_resume = normalize_text(resume_text)
    x = vectorizer.transform([cleaned_resume])
    top_role = model.predict(x)
    return top_role






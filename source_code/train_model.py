from source_code.preprocessing import load_data, generate_TFIDF , normalize_text
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, 'data', 'Role-Resume-Dataset.csv')


df_role_resume = load_data(file_path)
df_role_resume['normalized_resume'] = df_role_resume['resume'].apply(normalize_text)
x, vectorizer = generate_TFIDF(df_role_resume)

y = df_role_resume['job_title']

model = MultinomialNB()
model.fit(x, y)

joblib.dump(model, 'models/naive_bayes_model.pkl')
joblib.dump(vectorizer, 'models/tfidf_vectorizer.pkl')

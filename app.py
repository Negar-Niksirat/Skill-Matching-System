import streamlit as st
import joblib
from source_code.inference import predict_3_top_job , predict_top_job
from source_code.preprocessing import  normalize_text , load_data , preprocess_text ,extract_text_from_pdf
from source_code.plot import plot_experience_histogram , plot_salary_boxplot , plot_gender_preference
from source_code.semantic_matching import find_most_similar_job_titles
from API.summarization import summarize_job_descriptions
from API.roadmap import generate_learning_roadmap
from API.skills_process import  skills_process
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
flag = False

@st.cache_resource


def load_model_and_vectorizer():
    model = joblib.load('models/naive_bayes_model.pkl')
    vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
    return model, vectorizer

model, vectorizer = load_model_and_vectorizer()

st.title("Job Title Prediction")
resume = st.text_area("Please enter the resume text here:")
uploaded_file = st.file_uploader("Upload a PDF resume", type="pdf")

if st.button("Predict Job Titles"):
    if uploaded_file is not None and not resume:
        resume_text = extract_text_from_pdf(uploaded_file)
        if not resume_text:
            st.error("Unable to extract readable text from the PDF.")
        else:
            flag = True
    elif resume.strip() and uploaded_file is None:
        resume_text = resume
        flag = True
    elif resume and uploaded_file is not None:
        st.error("Please provide either text or file, not both.")
    else:
        st.error("Please enter resume text or upload a file.")
if flag== True:
    clean_resume =  normalize_text(resume_text)  
    top_jobs = predict_3_top_job(clean_resume)  # Predict top jobs
    st.subheader("Top 3 Job Recommendations:")
    for i, job in enumerate(top_jobs, 1):
        st.write(f"{i}. {job}")
    top_job = predict_top_job(clean_resume)

    best_match_indices = find_most_similar_job_titles(top_job, threshold=0.7)

    st.subheader("📊 Exploratory Analysis for Best Match")
    plot_experience_histogram(best_match_indices, top_job)
    plot_gender_preference(best_match_indices, top_job)
    plot_salary_boxplot(best_match_indices, top_job)
    df_job_description = load_data('data/Job-Description-Dataset.csv')
    df_matched_rows = df_job_description.iloc[best_match_indices].reset_index(drop=True)
    summary =summarize_job_descriptions(df_matched_rows['Job Description'].tolist(), top_job)
    st.subheader("📝 Summary of Job Descriptions")
    st.write(summary)

    all_skills_str = ", ".join(df_matched_rows['skills'].dropna().astype(str))
    skills_str = skills_process(all_skills_str)

    all_skills_set = ast.literal_eval(skills_str)
    missing_skills = []
    for skill in all_skills_set:
        if skill not in clean_resume:
            missing_skills.append(skill)

    roadmap = generate_learning_roadmap(missing_skills,top_job)
    st.subheader("📝 roadmap for learning")
    st.write(roadmap)


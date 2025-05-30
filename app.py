import streamlit as st
import joblib
from source_code.inference import predict_3_top_job , predict_top_job
from source_code.preprocessing import  normalize_text , load_data , preprocess_text ,extract_text_from_pdf
from source_code.plot import plot_experience_histogram , plot_salary_boxplot , plot_gender_preference
from source_code.semantic_matching import find_most_similar_job_titles
from API.summarization import summarize_job_descriptions
from API.roadmap import generate_learning_roadmap
from API.skills_process import  skills_process
from API.chat import chat_with_chatbot
import streamlit.components.v1 as components
import nltk
import ast
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

if 'flag' not in st.session_state:
    st.session_state.flag = False
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

@st.cache_resource

def load_model_and_vectorizer():
    model = joblib.load('models/naive_bayes_model.pkl')
    vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
    return model, vectorizer

model, vectorizer = load_model_and_vectorizer()

st.title("🔍 Let’s guess your perfect job!")
resume = st.text_area("Enter the resume text")
uploaded_file = st.file_uploader("Upload a PDF Resume", type="pdf")

if st.button("Predict"):
    if uploaded_file is not None and not resume:
        extracted_text = extract_text_from_pdf(uploaded_file)
        if not extracted_text:
            st.error("Unable to extract readable text from the PDF.")
        else:
            st.session_state.resume_text = extracted_text
            st.session_state.flag = True
    elif resume.strip() and uploaded_file is None:
        st.session_state.resume_text = resume
        st.session_state.flag = True
    elif resume and uploaded_file is not None:
        st.error("Please provide either text or file, not both.")
    else:
        st.error("Please enter resume text or upload a file.")

if st.session_state.flag:
    clean_resume = normalize_text(st.session_state.resume_text)
    if(len(clean_resume.strip())==0):
        st.error("Your input is invalid.")
    else:

    
        if 'top_jobs' not in st.session_state:
            st.session_state.top_jobs = predict_3_top_job(clean_resume)

            if 'top_job' not in st.session_state:
                st.session_state.top_job = predict_top_job(clean_resume)
                st.session_state.best_match_indices = find_most_similar_job_titles(st.session_state.top_job, threshold=0.7)

        st.subheader("🎯 Top 3 Job Matches – Just for You!")
        for i, job in enumerate(st.session_state.top_jobs, 1):
            st.write(f"{i}. {job}")

        st.subheader("📊 What the job posts are really saying?")
        plot_experience_histogram(st.session_state.best_match_indices, st.session_state.top_job)
        plot_gender_preference(st.session_state.best_match_indices, st.session_state.top_job)
        plot_salary_boxplot(st.session_state.best_match_indices, st.session_state.top_job)

        df_job_description = load_data('data/Job-Description-Dataset.csv')
        df_matched_rows = df_job_description.iloc[st.session_state.best_match_indices].reset_index(drop=True)

        if 'summary' not in st.session_state:
            st.session_state.summary = summarize_job_descriptions(df_matched_rows['Job Description'].tolist(), st.session_state.top_job)

        st.subheader("🧾 Job description summary:")
        st.write(st.session_state.summary)

        if 'roadmap' not in st.session_state:
            all_skills_str = ", ".join(df_matched_rows['skills'].dropna().astype(str))
            skills_str = skills_process(all_skills_str)
            all_skills_set = ast.literal_eval(skills_str)
            missing_skills = [skill for skill in all_skills_set if skill not in clean_resume]
            st.session_state.roadmap = generate_learning_roadmap(missing_skills, st.session_state.top_job)

        st.subheader("🧭 Learning roadmap for your future job:")
        st.write(st.session_state.roadmap)


        st.markdown("---")
        st.subheader("💬 Ask me anything!")

        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input( "",placeholder="Your message")
            submitted = st.form_submit_button("Send")
        chat_html = """
    <div style="
    height: 300px; 
    overflow-y: auto; 
    border: 1px solid #ddd; 
    padding: 10px; 
    background-color: #f9f9f9;
    font-family: Arial, sans-serif;
    ">
    """

        st.markdown("### 📜 Conversation")

        if  submitted and not user_input.strip():
            st.error("What do you want to ask the AI?")
        elif submitted and user_input.strip():
            st.session_state.chat_history.append(("user", user_input))
            bot_reply = chat_with_chatbot(user_input)
            st.session_state.chat_history.append(("assistant", bot_reply))
        
            for role, message in st.session_state.chat_history:
                if role == "user":
                    chat_html += f"<p style='color: #52B2CF; margin: 4px 0;'><b>🧑 You:</b></p><pre style='color: #313D5A;'>{message}</pre>"

                else:
                    chat_html += f"<p style='color: #AB90CE; margin: 4px 0;'><b>🤖 Assistant:</b></p><pre style='color: #73628A;'>{message}</pre>"

        chat_html += "</div>"
        components.html(chat_html, height=320, scrolling=False)
    
from source_code.preprocessing import load_data, preprocess_text
from source_code.inference import predict_top_job
from source_code.semantic_matching import find_most_similar_job_titles
import matplotlib.pyplot as plt
import re
import pandas as pd
import streamlit as st
import numpy as np

df_job_description = load_data('data/Job-Description-Dataset.csv')

def extract_salary_range(salary):
    salary = str(salary).lower().replace(',', '').replace(' ', '')
    if 'k' in salary:
        salary = salary.replace('k', '000')
    match = re.findall(r'(\d+)', salary)
    if len(match) == 2:
        return pd.Series([int(match[0]), int(match[1])])
    elif len(match) == 1:
        return pd.Series([int(match[0]), int(match[0])])
    else:
        return pd.Series([None, None])


def extract_years(experience):
    numbers = re.findall(r'\d+', str(experience))
    if len(numbers) >= 2:
        return int(numbers[0]), int(numbers[1])
    elif len(numbers) == 1:
        return int(numbers[0]), int(numbers[0])
    else:
        return None, None 




def plot_experience_histogram(best_match_indices, predicted_title):
    df_job_description[['Min_Years', 'Max_Years']] = df_job_description['Experience'].apply(lambda x: pd.Series(extract_years(x)))
    df_matched_rows = df_job_description.iloc[best_match_indices].reset_index(drop=True)
    min_years = df_matched_rows['Min_Years'].astype(int)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    counts, bins, patches = ax.hist(min_years, bins=range(min(min_years), max(min_years) + 2), 
                                    align='left', color='skyblue', edgecolor='black', rwidth=0.8)
    
    ax.set_title(f'Minimum experience for {predicted_title[0]}')
    ax.set_xlabel('Minimum Required Experience (Years)')
    ax.set_ylabel('Number of Job Descriptions')
    ax.set_xticks(range(min(min_years), max(min_years) + 1))
    
    # تنظیم فاصله محور Y به صورت عدد صحیح
    ax.set_yticks(np.arange(0, max(counts)+1, 1))
    
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)


   


def plot_gender_preference(best_match_indices, predicted_title):
    df_matched = df_job_description.iloc[best_match_indices]
    gender_counts = df_matched['Preference'].value_counts()

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=140,
           colors=['#4e79a7', '#f28e2b', '#76b7b2'])
    ax.set_title(f'Gender preference for {predicted_title[0]}')
    ax.axis('equal')
    st.pyplot(fig)


def plot_salary_boxplot(best_match_indices, predicted_title):
    df_job_description[['Min_Salary', 'Max_Salary']] = df_job_description['Salary Range'].apply(lambda x: pd.Series(extract_salary_range(x)))
    df_matched = df_job_description.iloc[best_match_indices]
    
    min_salary = df_matched['Min_Salary'].min()
    max_salary = df_matched['Max_Salary'].max()
    avg_min_salary =df_matched['Min_Salary'].mean()
    avg_max_salary = df_matched['Max_Salary'].mean()
    avg_salary = (avg_min_salary + avg_max_salary) / 2

    fig, ax = plt.subplots(figsize=(8,4))
    ax.hlines(1, min_salary, max_salary, color='lightgreen', linewidth=6)
    ax.plot([min_salary, avg_salary, max_salary], [1, 1, 1], 'o', color='green')

    ax.text(min_salary, 1.05, f'Min: {min_salary:.0f}', ha='center')
    ax.text(avg_salary, 0.85, f'Avg: {avg_salary:.0f}', ha='center')
    ax.text(max_salary, 1.05, f'Max: {max_salary:.0f}', ha='center')

    ax.set_yticks([])
    ax.set_xlabel('Salary')
    ax.set_title('Salary Range Overview')
    plt.tight_layout()
    st.pyplot(fig)




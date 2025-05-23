from sentence_transformers import SentenceTransformer, util
from source_code.preprocessing import load_data
import pandas as pd

df_job_description = load_data('data\Job-Description-Dataset.csv')
job_titles_list = df_job_description['Job Title']
model_embed = SentenceTransformer('all-MiniLM-L6-v2')

def find_most_similar_job_titles(predicted_title , threshold=0.7):
    predicted_embedding = model_embed.encode(predicted_title, convert_to_tensor=True)
    job_embeddings = model_embed.encode(job_titles_list, convert_to_tensor=True)

    cos_scores = util.cos_sim(predicted_embedding, job_embeddings)[0]
    max_score = max(cos_scores)
    max_score = cos_scores.max().item()

    if max_score> threshold:
        best_match_indices = [i for i in range(len(cos_scores)) if cos_scores[i] == max_score]
        return best_match_indices
    return []

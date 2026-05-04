import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import re

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def build_pipeline():
    df = pd.read_csv('mental_health_faq.csv')
    df['clean_question'] = df['Questions'].apply(clean_text)
    
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    embeddings = model.encode(df['clean_question'].tolist(), show_progress_bar=True)
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    
    faiss.write_index(index, 'mental_health.index')
    df.to_pickle('mental_health_data.pkl')
    print("Success: Index and data saved.")

if __name__ == "__main__":
    build_pipeline()

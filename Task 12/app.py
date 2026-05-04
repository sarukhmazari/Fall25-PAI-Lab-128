import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

from flask import Flask, render_template, request, jsonify
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import re

app = Flask(__name__)

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
index = faiss.read_index('mental_health.index')
df = pd.read_pickle('mental_health_data.pkl')

def search(query, k=5):
    clean_query = clean_text(query)
    query_vector = model.encode([clean_query]).astype('float32')
    distances, indices = index.search(query_vector, k)
    
    results = []
    for i in range(len(indices[0])):
        idx = indices[0][i]
        if idx < len(df):
            results.append({
                'question': df.iloc[idx]['Questions'],
                'answer': df.iloc[idx]['Answers'],
                'score': float(distances[0][i])
            })
    return results

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'No query provided'})
    results = search(query)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5000)

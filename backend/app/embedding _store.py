# app/embedding_store.py
import pandas as pd
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DATA_PATH = "data/amazon.csv"
INDEX_FILE = "vector_store/amazon.index"

def build_faiss_index():
    df = pd.read_csv(DATA_PATH)
    df.dropna(subset=['review_content'], inplace=True)
    texts = df['review_content'].tolist()

    model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = model.encode(texts, show_progress_bar=True)

    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    faiss.write_index(index, INDEX_FILE)
    print("FAISS index built and saved.")

    return index, texts

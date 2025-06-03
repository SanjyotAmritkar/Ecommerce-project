# app/rag.py
import openai
from app.embedding_store import build_faiss_index
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

openai.api_key = os.getenv("OPENAI_API_KEY")

INDEX_FILE = "vector_store/amazon.index"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
model = SentenceTransformer(EMBEDDING_MODEL)

# Load FAISS index and texts
index, texts = build_faiss_index()

def retrieve_and_answer(query, top_k=5):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), top_k)

    retrieved_texts = [texts[i] for i in I[0]]
    context = "\n".join(retrieved_texts)

    prompt = f"""Answer the following question based on the product reviews below:\n\n{context}\n\nQuestion: {query}\nAnswer:"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

import os
import faiss, pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query, domain, k=3):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    index_path = os.path.join(base_dir, "embeddings", f"{domain}.index")
    texts_path = os.path.join(base_dir, "embeddings", f"{domain}_texts.pkl")
    
    index = faiss.read_index(index_path)
    texts = pickle.load(open(texts_path, "rb"))

    q_emb = model.encode([query])
    _, idx = index.search(q_emb, k)

    return "\n".join([texts[i] for i in idx[0]])

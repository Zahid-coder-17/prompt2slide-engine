import faiss, pickle
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query, domain, k=3):
    index = faiss.read_index(f"embeddings/{domain}.index")
    texts = pickle.load(open(f"embeddings/{domain}_texts.pkl", "rb"))

    q_emb = model.encode([query])
    _, idx = index.search(q_emb, k)

    return "\n".join([texts[i] for i in idx[0]])

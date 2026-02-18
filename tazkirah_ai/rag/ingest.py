import os, pickle, faiss
from sentence_transformers import SentenceTransformer
from utils.pdf_utils import extract_text_from_pdf, clean_text, chunk_text


model = SentenceTransformer("all-MiniLM-L6-v2")

def ingest_domain(domain):
    texts = []
    folder = f"data/{domain}"

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        if file.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                texts.append(f.read())

        elif file.endswith(".pdf"):
            raw = extract_text_from_pdf(path)
            clean = clean_text(raw)
            chunks = chunk_text(clean)
            texts.extend(chunks)

    embeddings = model.encode(texts)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, f"embeddings/{domain}.index")
    pickle.dump(texts, open(f"embeddings/{domain}_texts.pkl", "wb"))

    print(f"✅ {domain} RAG built with {len(texts)} chunks")


if __name__ == "__main__":
    ingest_domain("ml")
    ingest_domain("islamic")

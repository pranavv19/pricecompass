from sentence_transformers import SentenceTransformer
import numpy as np

_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed(text: str) -> np.ndarray:
    return _model.encode(text, convert_to_numpy=True, normalize_embeddings=True)

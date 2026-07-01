"""
embeddings.py
-------------
Wraps a sentence-transformers model to turn text into vector embeddings.

Using a local, free, open-source model (all-MiniLM-L6-v2) means the app
works fully offline with no embedding API key required. Swap this out
for OpenAI/Cohere embeddings if you prefer -- just make sure the
EMBEDDING_DIMENSION constant matches your model and your Pinecone index.
"""

from typing import List
import streamlit as st
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384  # dimension produced by all-MiniLM-L6-v2


@st.cache_resource(show_spinner=False)
def load_embedding_model() -> SentenceTransformer:
    """Load (and cache) the sentence-transformers model once per session."""
    return SentenceTransformer(MODEL_NAME)


def embed_texts(texts: List[str]) -> List[List[float]]:
    """Embed a batch of strings and return plain Python lists of floats."""
    if not texts:
        return []
    model = load_embedding_model()
    vectors = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
    return vectors.tolist()


def embed_query(query: str) -> List[float]:
    """Embed a single search query string."""
    model = load_embedding_model()
    vector = model.encode([query], show_progress_bar=False, normalize_embeddings=True)
    return vector[0].tolist()

"""
pinecone_utils.py
------------------
Handles all interaction with the Pinecone vector database:
- creating/connecting to an index
- upserting chunk embeddings + metadata
- querying for the top-K most similar chunks
"""

from typing import List, Dict
import time
from pinecone import Pinecone, ServerlessSpec

from utils.embeddings import EMBEDDING_DIMENSION


def get_pinecone_client(api_key: str) -> Pinecone:
    """Create a Pinecone client instance."""
    return Pinecone(api_key=api_key)


def get_or_create_index(
    pc: Pinecone,
    index_name: str,
    dimension: int = EMBEDDING_DIMENSION,
    cloud: str = "aws",
    region: str = "us-east-1",
):
    """
    Connect to an existing Pinecone index, or create it if it doesn't exist.
    Returns an Index object ready for upsert/query.
    """
    existing_indexes = [idx["name"] for idx in pc.list_indexes()]

    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud=cloud, region=region),
        )
        # Wait until the index is ready before returning
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)

    return pc.Index(index_name)


def upsert_chunks(index, doc_id: str, doc_name: str, records: List[Dict], vectors: List[List[float]], batch_size: int = 100):
    """
    Upsert a document's chunk vectors + metadata into Pinecone.

    records: list of {"page": int, "chunk_id": int, "text": str}
    vectors: list of embedding vectors, aligned index-for-index with records
    """
    items = []
    for i, (record, vector) in enumerate(zip(records, vectors)):
        vector_id = f"{doc_id}-p{record['page']}-c{record['chunk_id']}"
        metadata = {
            "doc_name": doc_name,
            "page": record["page"],
            "chunk_id": record["chunk_id"],
            "text": record["text"],
        }
        items.append({"id": vector_id, "values": vector, "metadata": metadata})

    for i in range(0, len(items), batch_size):
        index.upsert(vectors=items[i : i + batch_size])


def query_index(index, query_vector: List[float], top_k: int = 5) -> List[Dict]:
    """
    Run a similarity search against the index and return a clean list of results.
    """
    response = index.query(vector=query_vector, top_k=top_k, include_metadata=True)

    results = []
    for match in response.get("matches", []):
        metadata = match.get("metadata", {})
        results.append(
            {
                "score": match.get("score", 0.0),
                "doc_name": metadata.get("doc_name", "Unknown"),
                "page": metadata.get("page", "-"),
                "text": metadata.get("text", ""),
            }
        )
    return results


def delete_all(index):
    """Clear all vectors from the index (useful for re-indexing during testing)."""
    try:
        index.delete(delete_all=True)
    except Exception:
        # Some Pinecone free-tier indexes throw if the index is already empty
        pass

"""
Mini Search Engine -- Semantic PDF Search with Streamlit + Pinecone
=====================================================================
Upload PDFs, index them as vector embeddings in Pinecone, and search
them with natural-language queries (Google-like semantic search).
"""

import os
import uuid
import streamlit as st
from dotenv import load_dotenv

from utils.pdf_utils import extract_text_from_pdf
from utils.chunking import chunk_document_pages
from utils.embeddings import embed_texts, embed_query
from utils.pinecone_utils import get_pinecone_client, get_or_create_index, upsert_chunks, query_index, delete_all

load_dotenv()

st.set_page_config(page_title="Mini Search Engine", page_icon="🔎", layout="wide")

# ----------------------------------------------------------------------------
# Sidebar -- configuration
# ----------------------------------------------------------------------------
st.sidebar.title(" Configuration")

default_api_key = os.getenv("PINECONE_API_KEY", "")
default_index = os.getenv("PINECONE_INDEX_NAME", "mini-search-engine")

pinecone_api_key = st.sidebar.text_input("Pinecone API Key", value=default_api_key, type="password")
index_name = st.sidebar.text_input("Pinecone Index Name", value=default_index)

chunk_size = st.sidebar.slider("Chunk size (characters)", 300, 1500, 800, step=100)
chunk_overlap = st.sidebar.slider("Chunk overlap (characters)", 0, 400, 150, step=50)
top_k = st.sidebar.slider("Top-K results", 1, 20, 5)

st.sidebar.markdown("---")
if st.sidebar.button("🗑️ Clear index (delete all vectors)"):
    if pinecone_api_key and index_name:
        try:
            pc = get_pinecone_client(pinecone_api_key)
            index = get_or_create_index(pc, index_name)
            delete_all(index)
            st.sidebar.success("Index cleared.")
        except Exception as e:
            st.sidebar.error(f"Could not clear index: {e}")
    else:
        st.sidebar.warning("Enter your Pinecone API key and index name first.")

st.sidebar.markdown(
    "Get a free Pinecone API key at [pinecone.io](https://www.pinecone.io/) "
    "and paste it above (or set `PINECONE_API_KEY` in a `.env` file)."
)

# ----------------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------------
st.title(" Mini Search Engine")
st.caption("Semantic search over your own PDF documents, powered by embeddings + Pinecone.")

if "indexed_docs" not in st.session_state:
    st.session_state.indexed_docs = []

# ----------------------------------------------------------------------------
# Step 1 -- Upload & Index PDFs
# ----------------------------------------------------------------------------
st.header("1. Upload PDFs")
uploaded_files = st.file_uploader(
    "Upload at least 5 PDF documents",
    type=["pdf"],
    accept_multiple_files=True,
)

col_a, col_b = st.columns([1, 3])
with col_a:
    index_button = st.button(" Process & Index PDFs", type="primary", use_container_width=True)

if uploaded_files:
    st.write(f"**{len(uploaded_files)} file(s) selected:** " + ", ".join(f.name for f in uploaded_files))
    if len(uploaded_files) < 5:
        st.info("Tip: upload at least 5 PDFs to fully exercise the search engine.")

if index_button:
    if not pinecone_api_key:
        st.error("Please provide your Pinecone API key in the sidebar.")
    elif not uploaded_files:
        st.error("Please upload at least one PDF file first.")
    else:
        try:
            pc = get_pinecone_client(pinecone_api_key)
            index = get_or_create_index(pc, index_name)
        except Exception as e:
            st.error(f"Could not connect to Pinecone: {e}")
            st.stop()

        progress = st.progress(0.0, text="Starting...")
        total = len(uploaded_files)

        for i, file in enumerate(uploaded_files):
            progress.progress(i / total, text=f"Extracting text from {file.name}...")
            pages = extract_text_from_pdf(file)

            if not pages:
                st.warning(f"No extractable text found in {file.name} (skipped).")
                continue

            records = chunk_document_pages(pages, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            texts = [r["text"] for r in records]

            progress.progress((i + 0.5) / total, text=f"Embedding {file.name} ({len(texts)} chunks)...")
            vectors = embed_texts(texts)

            doc_id = str(uuid.uuid4())[:8]
            upsert_chunks(index, doc_id=doc_id, doc_name=file.name, records=records, vectors=vectors)

            if file.name not in st.session_state.indexed_docs:
                st.session_state.indexed_docs.append(file.name)

        progress.progress(1.0, text="Done!")
        st.success(f"Indexed {total} document(s) into Pinecone index '{index_name}'.")

if st.session_state.indexed_docs:
    with st.expander(f" Documents indexed this session ({len(st.session_state.indexed_docs)})"):
        for name in st.session_state.indexed_docs:
            st.write(f"- {name}")

st.markdown("---")

# ----------------------------------------------------------------------------
# Step 2 -- Search
# ----------------------------------------------------------------------------
st.header("2. Search your documents")

query = st.text_input("Enter a natural-language search query", placeholder="e.g. What are the health benefits of exercise?")
search_col, _ = st.columns([1, 3])
with search_col:
    search_button = st.button(" Search", type="primary", use_container_width=True)

if search_button:
    if not pinecone_api_key:
        st.error("Please provide your Pinecone API key in the sidebar.")
    elif not query.strip():
        st.error("Please enter a search query.")
    else:
        try:
            pc = get_pinecone_client(pinecone_api_key)
            index = get_or_create_index(pc, index_name)
        except Exception as e:
            st.error(f"Could not connect to Pinecone: {e}")
            st.stop()

        with st.spinner("Searching..."):
            query_vector = embed_query(query)
            results = query_index(index, query_vector, top_k=top_k)

        st.subheader("Results")
        if not results:
            st.info("No results found. Have you indexed any PDFs yet?")
        else:
            for rank, result in enumerate(results, start=1):
                with st.container(border=True):
                    header_col, score_col = st.columns([4, 1])
                    with header_col:
                        st.markdown(f"**#{rank} &nbsp; {result['doc_name']}**  &nbsp;|&nbsp; Page {result['page']}")
                    with score_col:
                        st.metric("Similarity", f"{result['score']:.3f}")
                    st.write(result["text"])

st.markdown("---")
st.caption(
    "Built with Streamlit, Pinecone, and Sentence-Transformers. "
    "Embeddings run locally (all-MiniLM-L6-v2) — no OpenAI key required."
)

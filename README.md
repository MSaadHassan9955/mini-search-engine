 **Live App:** https://mini-search-engine-bxsdfb6weuqn4bnz6lgweu.streamlit.app/ (fully working — try it now!)
 **Source Code:** https://github.com/MSaadHassan9955/mini-search-engine

**Author:** Muhammad Saad Hassan



#  Mini Search Engine — Semantic PDF Search with Streamlit + Pinecone

A Google-like semantic search application. Upload PDF documents, and search them
using natural-language queries powered by vector embeddings and Pinecone.

## Features

-  Upload multiple PDF documents (5+ supported)
-  Automatic text extraction and chunking
-  Local, free embeddings via `sentence-transformers` (`all-MiniLM-L6-v2`) — no OpenAI key needed
-  Vector storage and retrieval via [Pinecone](https://www.pinecone.io/)
-  Natural-language semantic search with Top-K retrieval
-  Results show document name, page number, similarity score, and matched text

## Project Structure

```
mini-search-engine/
├── app.py                     # Main Streamlit application
├── generate_sample_pdfs.py    # Script to generate the 5 sample dataset PDFs
├── requirements.txt           # Python dependencies
├── .env.example                # Template for environment variables
├── .streamlit/
│   └── config.toml            # Streamlit theme/server config
├── utils/
│   ├── pdf_utils.py           # PDF text extraction
│   ├── chunking.py            # Text splitting into chunks
│   ├── embeddings.py          # Embedding generation
│   └── pinecone_utils.py      # Pinecone index management, upsert, query
└── sample_pdfs/               # 5 ready-to-use sample PDFs (dataset)
    ├── artificial_intelligence.pdf
    ├── space_exploration.pdf
    ├── human_health.pdf
    ├── personal_finance.pdf
    └── ancient_civilizations.pdf
```

## How It Works

1. **Upload** — User uploads one or more PDF files via the Streamlit UI.
2. **Extract** — `PyPDF2` extracts raw text from each page of every PDF.
3. **Chunk** — Text is split into overlapping ~800-character chunks (configurable) so that
   each chunk is small enough to embed meaningfully while preserving context.
4. **Embed** — Each chunk is converted into a 384-dimension vector using the local
   `all-MiniLM-L6-v2` sentence-transformers model.
5. **Store** — Vectors + metadata (document name, page number, chunk text) are upserted
   into a Pinecone serverless index.
6. **Query** — When the user searches, the query is embedded using the same model.
7. **Retrieve** — Pinecone returns the Top-K most similar chunks by cosine similarity.
8. **Display** — Results show the source PDF, page number, similarity score, and the
   matched paragraph.

## Setup

### 1. Clone and install dependencies

```bash
git clone <your-github-repo-url>
cd mini-search-engine
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Get a free Pinecone API key

Sign up at [pinecone.io](https://www.pinecone.io/) and copy your API key from the
dashboard. The app will automatically create a serverless index for you the first
time you index documents.

### 3. Configure your API key

Copy `.env.example` to `.env` and fill in your key:

```bash
cp .env.example .env
```

```
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_INDEX_NAME=mini-search-engine
```

Alternatively, you can paste the API key directly into the sidebar text field
when the app is running — no `.env` file required.

### 4. Generate the sample dataset (optional)

Five sample PDFs are already included in `sample_pdfs/`, but you can regenerate
them (or create your own topics) at any time:

```bash
python generate_sample_pdfs.py
```

### 5. Run the app

```bash
streamlit run app.py
```

Open the URL Streamlit prints (typically `http://localhost:8501`) in your browser.

## Usage

1. Open the app and paste your Pinecone API key into the sidebar (or set it via `.env`).
2. Upload 5+ PDF files (you can use the ones in `sample_pdfs/` to get started).
3. Click **Process & Index PDFs** — this extracts, chunks, embeds, and stores the
   documents in Pinecone.
4. Type a natural-language question into the search box, e.g. *"How does compound
   interest help retirement savings?"*
5. Click **Search** to see the Top-K most relevant passages, ranked by similarity
   score, along with the source document and page number.

## Deployment

This app deploys easily on [Streamlit Community Cloud](https://streamlit.io/cloud):

1. Push this repository to GitHub.
2. On Streamlit Cloud, create a new app pointing at `app.py`.
3. Add `PINECONE_API_KEY` and `PINECONE_INDEX_NAME` as app secrets
   (Settings → Secrets), using the same format as `.env`.
4. Deploy — Streamlit Cloud will install `requirements.txt` automatically.

## Tech Stack

| Component        | Technology                                  |
|-------------------|----------------------------------------------|
| Frontend/UI       | Streamlit                                    |
| PDF text extraction | PyPDF2                                     |
| Text chunking     | Custom overlapping character-based splitter  |
| Embeddings        | sentence-transformers (`all-MiniLM-L6-v2`)   |
| Vector database   | Pinecone (serverless)                        |
| Sample dataset    | Generated with ReportLab                     |

## Learning Outcomes

- Understand how text embeddings represent semantic meaning as vectors
- Learn how to provision and query a Pinecone vector database
- Implement an end-to-end semantic (retrieval) search pipeline
- Understand chunking strategies and their effect on retrieval quality

## License

MIT License — feel free to use and adapt this project.

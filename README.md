Yes. I reviewed the **actual first ZIP project**, not just the README you pasted, so the README below matches the implemented FastAPI, frontend, RAG, FAISS, SQLite, ingestion, citation, and notebook behavior.

I also made a few important corrections:

* Removed the nonexistent `data/` entry from the structure.
* Added the actual `__init__.py` files where appropriate.
* Described **MMR retrieval**, chunk metadata, persistent per-notebook FAISS stores, bounded conversation history, and citation persistence because they are implemented in the code.
* Kept all API keys as placeholders only.
* Added **Context Engineering** through the actual context-building/prompting architecture rather than falsely claiming a separate framework.
* Kept the wording professional and suitable for a GitHub portfolio/interview review.
* Avoided claiming things like authentication, cloud deployment, tests, or production hosting because the uploaded project does not establish those.

## README.md — copy this directly

 
# JERRY.AI — Production-Style Local RAG

> A FastAPI-based conversational Retrieval-Augmented Generation (RAG) application with persistent notebooks, document ingestion, semantic retrieval, grounded responses, and source-level citations.

JERRY.AI is a local-first document assistant built without Streamlit.

The application uses a **plain HTML/CSS/JavaScript frontend** and a **FastAPI backend**, while the RAG pipeline remains modular Python code using LangChain, Gemini embeddings, FAISS, SQLite, and a Groq-hosted LLM.

The system is designed around one core goal:

**retrieve relevant source context, construct a controlled prompt, and generate answers grounded in the uploaded documents.**

---

## ✨ Key Features

- 📚 **Notebook-based document organization**
- 📄 Upload and index **PDF, DOCX, TXT, and Markdown** files
- 🔎 **Semantic retrieval** using Gemini embeddings and FAISS
- 🧠 **MMR (Maximal Marginal Relevance)** retrieval to improve result diversity
- 💬 **Persistent multi-session conversation history**
- 🧩 **Context engineering** for controlled context assembly and grounded prompting
- 📌 **Source-level citations** with source and chunk metadata
- 🛡️ **Grounded response behavior** that avoids unsupported document claims
- 🗃️ **SQLite persistence** for notebooks, sources, messages, and citations
- 💾 **Persistent FAISS vector stores per notebook**
- 🖥️ Simple browser UI served directly by FastAPI
- 🔌 REST API with automatic Swagger/OpenAPI documentation
- 🧹 Source deletion with corresponding vector cleanup
- ⚙️ Configurable chunking, retrieval, history, and file-size limits

---

## 🏗️ Architecture

 '
                         ┌──────────────────────┐
                         │     Browser UI        │
                         │ HTML / CSS / JS       │
                         └──────────┬───────────┘
                                    │
                               fetch() / HTTP
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       FastAPI        │
                         │   REST API + UI      │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                    ▼               ▼                ▼
              ┌──────────┐   ┌─────────────┐   ┌────────────┐
              │ SQLite   │   │ RAG Pipeline│   │ File Store │
              │          │   │             │   │            │
              │ notebooks│   │ retrieval   │   │ uploads    │
              │ sources  │   │ context     │   │ vectorstore│
              │ messages │   │ prompting   │   │            │
              │ citations│   │ generation  │   │            │
              └──────────┘   └──────┬──────┘   └────────────┘
                                    │
                        ┌───────────┴────────────┐
                        │                        │
                        ▼                        ▼
               Gemini Embeddings            Groq LLM
                        │
                        ▼
                 Persistent FAISS
 

FastAPI serves the frontend itself, so the normal local setup runs as a **single application process** with same-origin frontend requests.

---

## 🔄 RAG Pipeline

### Document ingestion

 
Upload document
       ↓
Validate file type / size
       ↓
Load document
(PDF / DOCX / TXT / MD)
       ↓
Recursive chunking
       ↓
Attach source + chunk metadata
       ↓
Gemini embeddings
       ↓
FAISS vector store
       ↓
Persist per notebook
 

### Question answering
 
User question
       ↓
Question embedding
       ↓
MMR retrieval
       ↓
Top relevant + diverse chunks
       ↓
Context engineering
       ↓
Conversation history
       ↓
Grounded prompt
       ↓
Groq LLM
       ↓
Answer + source citations
 

 

## 🧠 Context Engineering

JERRY.AI uses context engineering as part of the RAG pipeline.

Instead of sending raw retrieved documents directly to the LLM, the application:

1. Retrieves relevant document chunks.
2. Preserves source and chunk metadata.
3. Builds numbered context blocks.
4. Adds bounded conversation history.
5. Combines the retrieved context, history, and user question into a structured prompt.
6. Instructs the model to treat retrieved context as the source of truth.
7. Extracts citation references from the generated answer and persists the corresponding source information.

Example context structure:

 
[1] Source: document.pdf (Chunk 3/12)
<retrieved content>

[2] Source: notes.md (Chunk 1/7)
<retrieved content>
 

This helps keep generation focused on the retrieved evidence instead of the model relying only on its pretrained knowledge.

---

## 📌 Grounding & Citations

The system is designed to reduce unsupported answers for document-based questions.

The prompt explicitly instructs the LLM to:

* use retrieved context as the source of truth,
* cite claims using numbered sources,
* avoid inventing facts not supported by the retrieved context,
* state when the required information is not available in the provided sources.

Returned citations contain metadata such as:

 
Source
Chunk ID
Total chunks
Retrieved content
 

Citations are also persisted in SQLite so they remain available with conversation history.

---

## 💾 Persistence

JERRY.AI maintains local persistent state using SQLite and FAISS.

### SQLite stores

* Notebook metadata
* Uploaded source metadata
* Human messages
* AI responses
* Citation records

### FAISS stores

Each notebook has its own persistent vector store:

 
storage/
└── vectorstores/
    ├── notebook_1/
    ├── notebook_2/
    └── ...
 

This keeps document retrieval isolated between notebooks.

---

## 🗂️ Project Structure

 
.
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   └── services.py
│
├── database/
│   ├── __init__.py
│   └── db.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── llm/
│   ├── __init__.py
│   ├── model.py
│   └── prompt.py
│
├── rag/
│   ├── __init__.py
│   ├── pipeline.py
│   ├── retriever.py
│   └── vectorstore.py
│
├── storage/
│   ├── uploads/
│   └── vectorstores/
│
├── config.py
├── requirements.txt
├── .gitignore
└── README.md
 

### Module responsibilities

| Module                | Responsibility                                                           |
| --------------------- | ------------------------------------------------------------------------ |
| `backend/main.py`     | FastAPI app, routes, frontend serving, lifecycle                         |
| `backend/services.py` | Notebook, upload, chat, deletion, and RAG service logic                  |
| `backend/schemas.py`  | API request models                                                       |
| `database/db.py`      | SQLite schema and persistence operations                                 |
| `rag/vectorstore.py`  | File loading, chunking, embeddings, FAISS persistence                    |
| `rag/retriever.py`    | MMR-based retrieval                                                      |
| `rag/pipeline.py`     | Retrieval, context construction, conversation history, answer generation |
| `llm/model.py`        | Groq LLM initialization                                                  |
| `llm/prompt.py`       | Grounded RAG prompt and citation instructions                            |
| `frontend/`           | Browser interface and API interaction                                    |
| `config.py`           | Environment-driven application configuration                             |

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

### RAG / LLM

* LangChain
* Google Gemini Embeddings
* Groq
* Llama 3.1
* FAISS
* Recursive Character Text Splitter

### Document Processing

* PyPDF
* PyMuPDF
* DOCX2TXT
* TXT / Markdown loaders

### Database

* SQLite

### Frontend

* HTML
* CSS
* JavaScript

---

## ⚙️ Configuration

Create a local `.env` file in the project root.

> **Do not commit this file to GitHub.**

 env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
 

Optional configuration:

 env
LLM_MODEL=llama-3.1-8b-instant
EMBEDDING_MODEL=models/gemini-embedding-001

CHUNK_SIZE=1000
CHUNK_OVERLAP=150

RETRIEVER_K=4
RETRIEVER_FETCH_K=12
LAMBDA_MULT=0.5

MAX_HISTORY_MESSAGES=12
MAX_FILE_SIZE_MB=20
 

### Configuration overview

| Variable               | Purpose                                  |                       Default |
| ---------------------- | ---------------------------------------- | ----------------------------: |
| `LLM_MODEL`            | Groq chat model                          |        `llama-3.1-8b-instant` |
| `EMBEDDING_MODEL`      | Gemini embedding model                   | `models/gemini-embedding-001` |
| `CHUNK_SIZE`           | Maximum chunk size                       |                        `1000` |
| `CHUNK_OVERLAP`        | Chunk overlap                            |                         `150` |
| `RETRIEVER_K`          | Final retrieved chunks                   |                           `4` |
| `RETRIEVER_FETCH_K`    | Candidate chunks considered by MMR       |                          `12` |
| `LAMBDA_MULT`          | MMR relevance/diversity trade-off        |                         `0.5` |
| `MAX_HISTORY_MESSAGES` | Conversation messages retained in prompt |                          `12` |
| `MAX_FILE_SIZE_MB`     | Maximum uploaded file size               |                          `20` |

---

## 🚀 Local Setup

### 1. Clone the repository

 bash
git clone https://github.com/<your-username>/<your-repository>.git
cd <your-repository>
 

### 2. Create a virtual environment

Windows:

 
python -m venv .venv
.venv\Scripts\activate
 

Linux / macOS:

 
python3 -m venv .venv
source .venv/bin/activate
 

### 3. Install dependencies

 
pip install -r requirements.txt
 

### 4. Configure environment variables

Create:

 
.env
 

Add your own API keys:

 env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
 

Never place real keys in `README.md`, source code, screenshots, commits, or public repositories.

### 5. Start the application


uvicorn backend.main:app --reload
 

### 6. Open the application

 
http://127.0.0.1:8000
 

### 7. Open API documentation

FastAPI Swagger UI:

 
http://127.0.0.1:8000/docs
 

---

## 🔌 API Endpoints

### Health

http
GET /api/health


### Notebooks

http
GET    /api/notebooks
POST   /api/notebooks
GET    /api/notebooks/{id}
DELETE /api/notebooks/{id}


### Sources

http
GET    /api/notebooks/{id}/sources
POST   /api/notebooks/{id}/sources
DELETE /api/notebooks/{id}/sources/{source_id}


### Conversation

http
GET  /api/notebooks/{id}/messages
POST /api/notebooks/{id}/chat


FastAPI automatically exposes interactive documentation through:

text
/docs


---

## 📄 Supported Documents

The ingestion pipeline currently supports:

text
.pdf
.docx
.txt
.md


Uploaded files are validated for both supported type and configured maximum size before indexing.

---

## 🔎 Retrieval Strategy

JERRY.AI uses **Maximal Marginal Relevance (MMR)** for retrieval.

Instead of selecting chunks purely by similarity, MMR balances:

text
Relevance to the query
        +
Diversity among retrieved results


The retrieval configuration is controlled by:

env
RETRIEVER_K=4
RETRIEVER_FETCH_K=12
LAMBDA_MULT=0.5


This allows the system to retrieve multiple useful pieces of information while reducing redundant results.

---

## 🧱 Chunking Strategy

Documents are split using LangChain's `RecursiveCharacterTextSplitter`.

Default configuration:


Chunk size:       1000
Chunk overlap:     150


Each generated chunk receives metadata such as:

 
source_id
source
chunk_id
total_chunks


This metadata is later used for source tracking and citations.

---

## 💬 Conversation Memory

Conversation history is persisted in SQLite.

For each notebook, the application stores:

Human message
AI response
Timestamp
Citation records


Only the most recent configured number of messages are included in the LLM prompt:

env
MAX_HISTORY_MESSAGES=12


This provides conversational continuity while keeping prompt context bounded.

---

## 🧹 Source Deletion

Removing a source does more than delete its database record.

The application also:

1. Removes the associated vectors from the notebook's FAISS index.
2. Removes the source metadata from SQLite.
3. Removes the stored uploaded file.

This keeps document metadata, files, and vector data synchronized.

---

## 🔐 Security & Data Handling

### Secrets

API keys are loaded through environment variables.

Never commit:


.env


to the repository.

The included `.gitignore` excludes the environment file and generated local storage.

### Local data

The following runtime data is intentionally ignored by Git:


storage/*.db
storage/uploads/*
storage/vectorstores/*


This prevents local databases, uploaded documents, and generated vector stores from being pushed accidentally.

### FAISS deserialization

The application uses:


allow_dangerous_deserialization=True


when loading FAISS indexes.

This is used only for indexes created and stored by this application under:

storage/vectorstores/


Do **not** load arbitrary FAISS index files from untrusted sources.

---

## 🖥️ Frontend

The application does not depend on Streamlit.

The browser interface is implemented with:

 
HTML
CSS
JavaScript


FastAPI serves the frontend directly, allowing the browser to communicate with the backend through same-origin API requests.

The interface provides:

* Notebook selection
* Notebook creation
* Source upload
* Source search/filtering
* Source deletion
* Chat interaction
* Conversation history
* Citation display

---

## 🧪 Example Usage

### 1. Create a notebook

Create a notebook from the web interface.

### 2. Upload documents

Supported formats:

 
PDF
DOCX
TXT
MD


### 3. Indexing

The uploaded document is:

 
Loaded
→ Split into chunks
→ Embedded
→ Stored in FAISS
 

### 4. Ask a question

Example:

 
What are the main concepts discussed in these documents?
 

### 5. Retrieval

The query is embedded and relevant chunks are selected using MMR.

### 6. Generation

The selected context and recent conversation history are passed into the grounded prompt.

### 7. Response

The LLM returns an answer with inline source references where applicable.

---

## 🎯 Engineering Focus

This project demonstrates practical implementation of:


RAG Architecture
Semantic Search
Vector Databases
MMR Retrieval
Context Engineering
Prompt Engineering
Grounded Generation
Citation Tracking
Conversation Memory
FastAPI Backend Development
REST API Design
SQLite Persistence
Document Processing
Frontend ↔ Backend Integration
Configuration Management


The architecture separates ingestion, retrieval, prompt construction, generation, persistence, and HTTP API responsibilities so that each layer can be developed and maintained independently.

---

## 📈 Future Improvements

Potential next steps include:

* Authentication and user-level data isolation
* Streaming token responses
* Background document indexing jobs
* Hybrid keyword + semantic retrieval
* Reranking models
* Evaluation datasets and retrieval metrics
* Automated RAG quality testing
* Dockerized deployment
* Cloud object storage
* Observability and request tracing

These are **planned extensions**, not claims about the current implementation.

---

## 📜 License

This project is currently provided for educational and portfolio purposes.

Add a project-specific license before distributing it publicly if required.

---

## 👤 Author

**Vishnu Pavan Kumar Marella**

B.Tech — Artificial Intelligence & Machine Learning
VIT-AP University

### Areas of Focus


AI / ML
Generative AI
RAG Systems
Agentic AI
Context Engineering
Prompt Engineering
Automation
Backend Development
Data Structures & Algorithms


---

## ⭐ Project Summary

JERRY.AI is a local-first conversational RAG system that combines:


FastAPI
+
HTML/CSS/JavaScript
+
LangChain
+
Gemini Embeddings
+
FAISS
+
SQLite
+
Groq LLM


to create a document-grounded assistant with **persistent notebooks, semantic retrieval, conversational memory, context engineering, and source-level citations**.



### One recommendation

For GitHub, I would use this README as the main `README.md`, and **not put API keys, `.env` contents with real values, screenshots containing secrets, databases, uploaded documents, or FAISS files into the repository**.

The README also now matches the actual project code much more closely than the original version you pasted, including the implemented **MMR retrieval and context/citation flow**.
```

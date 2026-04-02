# 📄 FastAPI Financial Document Management System with RAG

## 🚀 Project Overview
This project is a **Financial Document Management System** built using **FastAPI** with advanced **RAG (Retrieval-Augmented Generation)** capabilities.

It allows users to:
- Upload financial documents (PDF/Text)
- Extract and process document content
- Store embeddings in a vector database
- Perform semantic search on financial data
- Retrieve meaningful financial insights

---

## 🧠 Key Features

### 🔐 Authentication & Authorization
- User Registration & Login (JWT based)
- Secure API access using Bearer Token
- Role-Based Access Control (RBAC)
  - Admin
  - User
- Permission-based actions (upload, view, delete)

### 📂 Document Management
- Upload financial documents (PDF / Text)
- Extract text using PyPDF2
- Store metadata in database
- Retrieve documents by ID
- Search documents by company name
- Delete documents (DB + Vector DB)

### 🤖 RAG (Retrieval-Augmented Generation)
- Document → Text → Chunking → Embeddings → Vector DB
- Semantic search using embeddings
- Financial insight retrieval

**Features:**
- Chunking of document text
- Embedding generation (Sentence Transformers)
- Vector storage (FAISS / Chroma)
- Context retrieval

### 🔍 Semantic Search
Search using natural language queries.

**Example:**
```json
{
  "query": "financial risk due to high debt"
}
```

Returns the most relevant document chunks.

### 🔄 Reranking System
Improves search results quality.

**Pipeline:**
```
User Query
   ↓
Embedding
   ↓
Vector Search
   ↓
Top Results
   ↓
Reranking Model
   ↓
Top Relevant Results
```

---

## 🛠️ Tech Stack

- FastAPI
- Python
- SQLAlchemy
- SQLite
- JWT (python-jose)
- Passlib (bcrypt)
- PyPDF2
- Sentence Transformers
- FAISS / Chroma

---

## 📁 Project Structure

```
Financial_management_system/
│
├── app/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── routes/
│   ├── utils/
│   ├── uploads/
│   ├── main.py
│
├── venv/
├── .gitignore
├── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/pranali1911/FastAPI-Financial-Document-Management-with-Semantic-Analysis.git
cd FastAPI-Financial-Document-Management-with-Semantic-Analysis
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Server
```bash
uvicorn app.main:app --reload
```

Open in browser:
```
http://127.0.0.1:8000/docs
```

---

## 🔑 API Endpoints

### Auth
- POST /auth/register
- POST /auth/login

### Documents
- POST /documents/upload
- GET /documents
- GET /documents/{doc_id}
- GET /documents/search
- DELETE /documents/{doc_id}

### Roles & Permissions
- POST /users/assign-role
- GET /users/{user_id}/roles
- GET /users/{user_id}/permissions

### RAG APIs
- POST /rag/index-document
- DELETE /rag/remove-document/{doc_id}
- POST /rag/search
- GET /rag/context/{doc_id}

---

## 📌 Example Workflow
1. Register user  
2. Login → Get JWT Token  
3. Authorize in Swagger  
4. Upload document  
5. Index document (RAG)  
6. Perform semantic search  
7. Get financial insights  

---

## 📊 Example Output
```json
{
  "query": "financial risk due to debt",
  "results": [
    "Company has moderate debt but high ratio may increase financial risk"
  ]
}
```

---

## ⚠️ Important Notes
- Password length must be ≤ 72 bytes (bcrypt limitation)
- Always send token in header:
```
Authorization: Bearer <your_token>
```
- Ensure correct role for permissions (Admin required for delete)

---

## 🔒 .gitignore
```
venv/
__pycache__/
*.pyc
*.db
uploads/
.env
```

---

## 🌟 Future Enhancements
- UI Dashboard (React / Streamlit)
- Advanced financial analytics
- Multi-document comparison
- Cloud deployment (AWS / Azure)
- Improved reranking models

---

## 👩‍💻 Author
**Pranali Rahangdale**  
📧 pranalirahangdale53@gmail.com  
🔗 https://github.com/pranali1911  

---


# 📄 FastAPI Financial Document Management System with RAG

## 🚀 Project Overview

This project is a Financial Document Management System built using FastAPI with advanced RAG (Retrieval-Augmented Generation) capabilities.

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

---

### 📂 Document Management
- Upload financial documents (PDF / Text)
- Extract text using PyPDF2
- Store metadata in database
- Retrieve documents by ID
- Search documents by company name
- Delete documents (DB + Vector DB)

---

### 🤖 RAG (Retrieval-Augmented Generation)
- Document → Text → Chunking → Embeddings → Vector DB
- Semantic search using embeddings
- Financial insight retrieval

#### Features:
- Chunking of document text
- Embedding generation (Sentence Transformers)
- Vector storage (FAISS / Chroma)
- Context retrieval

---

### 🔍 Semantic Search

Example request:
```json
{
  "query": "financial risk due to high debt"
}

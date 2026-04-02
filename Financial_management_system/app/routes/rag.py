from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from models.document import Document
from utils.rag import store_document, delete_document
from utils.rag import search_documents, get_document_chunks
from fastapi import APIRouter



router = APIRouter()


# =================================================
# Index Document (store embeddings)
# =================================================
@router.post("/rag/index-document")
def index_document(doc_id: int, db: Session = Depends(get_db)):

    document = db.query(Document).filter(Document.id == doc_id).first()

    if not document:
        return {"error": "Document not found"}

    # Combine metadata as text
    text = f"{document.title}. {document.company_name}. {document.document_type}"

    store_document(doc_id, text)

    return {"message": "Document indexed with chunking"}


# =================================================
# Remove Document from vector DB
# =================================================
from fastapi import HTTPException

@router.delete("/rag/remove-document/{doc_id}")
def remove_document(doc_id: int):

    try:
        from utils.rag import delete_document
        delete_document(doc_id)

        return {"message": "Document removed from vector DB"}

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Failed to delete from vector DB")




@router.post("/rag/search")
def rag_search(query: str):

    results = search_documents(query)

    return {
        "query": query,
        "results": results["documents"]
    }
    
    
@router.get("/rag/context/{doc_id}")
def get_context(doc_id: int):

    chunks = get_document_chunks(doc_id)

    return {
        "document_id": doc_id,
        "chunks": chunks
    }
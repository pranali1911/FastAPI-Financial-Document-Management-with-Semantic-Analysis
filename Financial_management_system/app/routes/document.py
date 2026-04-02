from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from models.document import Document
from utils.file import save_file
from core.auth import get_current_user
from utils.rbac import has_permission
from routes.role import user_roles
from PyPDF2 import PdfReader
from utils.rag import store_document
from fastapi import HTTPException

router = APIRouter()

# =================================================
# Upload Document (PDF + RAG + RBAC)
# =================================================
@router.post("/documents/upload")
def upload_document(
    title: str,
    company_name: str,
    document_type: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    role = user_roles.get(user_id)

    # Check permission
    if not has_permission(role, "upload"):
        return {"error": "Permission denied"}

    # ===============================
    # SAVE FILE
    # ===============================
    file_path = save_file(file.file, file.filename)

    # ===============================
    # EXTRACT TEXT (PDF / TEXT)
    # ===============================
    content = ""

    file.file.seek(0)   # IMPORTANT

    if file.filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        for page in reader.pages:
            content += page.extract_text() or ""
    else:
        content = file.file.read().decode("utf-8")

    # ===============================
    # SAVE TO DATABASE
    # ===============================
    doc = Document(
        title=title,
        company_name=company_name,
        document_type=document_type,
        file_path=file_path,
        uploaded_by=user_id
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)

    # ===============================
    # STORE IN VECTOR DB (RAG)
    # ===============================
    store_document(doc.id, content)

    return {"message": "Document uploaded and indexed successfully"}


# =================================================
# Get All Documents (Protected)
# =================================================
@router.get("/documents")
def get_all_documents(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    role = user_roles.get(user_id)

    if not has_permission(role, "view"):
        return {"error": "Permission denied"}

    return db.query(Document).all()

# =================================================
# Search Documents (Metadata)
# =================================================
@router.get("/documents/search")
def search_documents(
    company_name: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    role = user_roles.get(user_id)

    if not has_permission(role, "view"):
        return {"error": "Permission denied"}

    results = db.query(Document).filter(
        Document.company_name == company_name
    ).all()

    return results


# =================================================
# Get Single Document
# =================================================
@router.get("/documents/{doc_id}")
def get_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    role = user_roles.get(user_id)

    if not has_permission(role, "view"):
        return {"error": "Permission denied"}

    document = db.query(Document).filter(Document.id == doc_id).first()

    if not document:
        return {"error": "Document not found"}

    return document


@router.delete("/documents/{doc_id}")
def delete_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user.get("user_id")
    role = user_roles.get(user_id)

    # permission check
    if not has_permission(role, "delete"):
        raise HTTPException(status_code=403, detail="Permission denied")

    # get document
    document = db.query(Document).filter(Document.id == doc_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # delete from DB
    db.delete(document)
    db.commit()

    # delete from vector DB (safe)
    try:
        from utils.rag import delete_document as delete_vector
        delete_vector(doc_id)
    except Exception as e:
        print("Vector DB delete failed:", e)

    return {"message": "Document deleted successfully"}


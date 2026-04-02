from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company_name = Column(String)
    document_type = Column(String)
    file_path = Column(String)
    uploaded_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    

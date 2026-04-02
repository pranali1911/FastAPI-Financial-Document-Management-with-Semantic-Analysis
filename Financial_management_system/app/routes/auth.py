from passlib.hash import bcrypt
from core.auth import create_access_token
from sqlalchemy.orm import Session
from database.database import get_db    
from models.user import User
#update auth.py
from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/auth/register")
def register(email: str, password: str, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return {"error": "User already exists"}

    hashed_password = bcrypt.hash(password)

    new_user = User(email=email, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

# create Login API 
@router.post("/auth/login")
def login(email: str, password: str, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        return {"error": "User not found"}

    if not bcrypt.verify(password, user.password):
        return {"error": "Invalid password"}

    # create JWT token
    token = create_access_token({"user_id": user.id})

    return {
        "message": "Login successful",
        "access_token": token
    }
from fastapi import FastAPI
from database.database import Base, engine
from routes import auth, document
from routes import role
from routes import rag

app = FastAPI()

# Create all tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Financial Document API Running"}


# include auth routes
app.include_router(auth.router)
app.include_router(document.router)
app.include_router(role.router)
app.include_router(rag.router)
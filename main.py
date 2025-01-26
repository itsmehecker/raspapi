import secrets
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, text
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class APIKey(Base):
    __tablename__ = "api_keys"
    key = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    level = Column(Integer, default=1)  # Ensure level column is defined

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Function to add the level column if it doesn't exist
def add_level_column():
    with engine.connect() as connection:
        try:
            connection.execute(text("ALTER TABLE api_keys ADD COLUMN level INTEGER DEFAULT 1;"))
        except ProgrammingError:
            pass  # Column already exists

add_level_column()

class NameRequest(BaseModel):
    name: str

class LevelUpdateRequest(BaseModel):
    api_key: str
    level: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_api_key() -> str:
    return secrets.token_urlsafe(32)

@app.post("/get-api-key")
async def get_api_key(request: NameRequest, db: Session = Depends(get_db)):
    api_key = generate_api_key()
    db_api_key = APIKey(key=api_key, name=request.name)
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return {"api_key": api_key}

def verify_api_key(api_key: str, db: Session = Depends(get_db)):
    db_api_key = db.query(APIKey).filter(APIKey.key == api_key).first()
    if not db_api_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return db_api_key

@app.get("/")
async def root(api_key: str = Depends(verify_api_key)):
    return {"message": "This is the app description."}

@app.get("/level")
async def get_level(api_key: APIKey = Depends(verify_api_key)):
    return {"level": api_key.level}

@app.post("/update-level")
async def update_level(request: LevelUpdateRequest, db: Session = Depends(get_db)):
    db_api_key = db.query(APIKey).filter(APIKey.key == request.api_key).first()
    if not db_api_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    db_api_key.level = request.level
    db.commit()
    db.refresh(db_api_key)
    return {"message": "Level updated", "level": db_api_key.level}
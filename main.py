import secrets
from fastapi import FastAPI, HTTPException, Depends, Query
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

def verify_api_key(api_key: str, db: Session = Depends(get_db)) -> APIKey:
    db_api_key = db.query(APIKey).filter(APIKey.key == api_key).first()
    if not db_api_key:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return db_api_key

@app.get("/")
async def root(api_key: APIKey = Depends(verify_api_key), choice: int = Query(None)):
    if api_key.level == 1:
        if choice is None:
            return {
                "message": "You are a fresh avocado now that you have been checked by the store keeper.",
                "stage": "You've been accused of salt by a flower you once hooked up with. She thinks you made her gain weight.",
                "choices": {
                    "1": "Fight the accusation in court.",
                    "2": "Flee the country."
                }
            }
        elif choice == 1:
            api_key.level = 2
            db = next(get_db())
            db.commit()
            return {"message": "You chose to fight the accusation in court. Prepare your defense!", "level": api_key.level}
        elif choice == 2:
            api_key.level = 3
            db = next(get_db())
            db.commit()
            return {"message": "You chose to flee the country. You are now a fugitive!. also broke","nav":"go to /mexico?apikey=YOURAPIKEY","level": api_key.level}
        else:
            return {"message": "Invalid choice. Please choose 1 or 2."}
    
    elif api_key.level == 2:
        return {"message": "You are in court now. Present your evidence to defend yourself.", "level": api_key.level}
    
    elif api_key.level == 3:
        return {"message": "You are on the run. Stay hidden and avoid capture.", "level": api_key.level}
    
    else:
        return {"message": "Unknown level. Please contact support.", "level": api_key.level}

@app.get("/mexico")
async def root(api_key: APIKey = Depends(verify_api_key), choice: int = Query(None)):
    if api_key.level==3:
        if choice==None:
            return {"choices": {1: "sell fertilizers to kids",2:"become a shopkeepers show item"}}
        elif choice==1:
            return {"message": "The kids were FBV(FEDERAL BUREAU OF VEGETABLES!!), You gone straight to jail go to /jail?apikey=You're api key"}
@app.get("/jail")
@app.get("/dontmindtherottenveggies")#you die a cold and by old age bcoz you were a smushy veggie
@app.get("/meet_with_rotten_veggies")#they tell you to do something
@app.get("/do_what_they_say")
#they say you've got guts
@app.get("/dont_do_what_they_say")
#they say you've got guts
@app.get("/the_mafia_gets_her_killed")
#The End you completed the game (fake ending)
@app.get("/enjoy_hybridisation_with_the_flowers_sister")
#the mafia was her she killed you and cut you and also threw your seed in the fire
@app.get("/jury_flower")
#you still go to jail no matter what coz the victim is a flower ik it's sexist I'm sorry (wait till you get to the johny depp level 🚶‍♂️)
@app.get("/bailout_j")
#Jonhny depp bails you out and helps you fight the flower with 
@app.get("/do_a_jar_of_powdered_sugar")
#
@app.get("/dont_do_the_jar_of_powdered_sugar")
#you're lame get tf out of here
@app.get()
@app.get("/level")
async def get_level(api_key: APIKey = Depends(verify_api_key)):
    return {"level": api_key.level}
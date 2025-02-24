import uuid
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

Base.metadata.create_all(bind=engine)

def add_level_column():
    with engine.connect() as connection:
        try:
            connection.execute(text("ALTER TABLE api_keys ADD COLUMN level INTEGER DEFAULT 1;"))
        except ProgrammingError:
            pass  # Column already exists

add_level_column()

class NameRequest(BaseModel):
    name: str
class riddle_ans(BaseModel):
    answer: str
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_api_key() -> str:
    return str(uuid.uuid4())

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

@app.post("/smuggle_fertilizer")
async def root(request: riddle_ans,api_key: APIKey = Depends(verify_api_key),db: Session = Depends(get_db)):
    ans=request.ans
    if ans.lower()=="avacado":
        update_level(api_key, 6, db)
        return {"message": "You smuggled the fertilizer successfully. go to /the_mafia_gets_her_killed .", "level": api_key.level}
def update_level(api_key: APIKey, new_level: int, db: Session):
    api_key.level = new_level
    db.commit()
    db.refresh(api_key)

@app.get("/")
async def root(api_key: APIKey = Depends(verify_api_key), choice: int = Query(None), db: Session = Depends(get_db)):
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
            update_level(api_key, 2, db)
            return {"message": "You chose to fight the accusation in court. Prepare your defense!,go to /jury_flower.", "level": api_key.level}
        elif choice == 2:
            update_level(api_key, 3, db)
            return {"message": "You chose to flee the country. You are now a fugitive! go to /mexico", "level": api_key.level}
        else:
            return {"message": "Invalid choice. Please choose 1 or 2."}
    
    else:
        return {"message": "Unknown level. Please contact support.", "level": api_key.level}

@app.get("/mexico")
async def mexico(api_key: APIKey = Depends(verify_api_key), choice: int = Query(None), db: Session = Depends(get_db)):
    if api_key.level == 3:
        if choice is None:
            return {
                "choices": {
                    1: "Sell fertilizers to kids",
                    2: "Become a shopkeeper's show item"
                }
            }
        elif choice == 1:
            update_level(api_key, 4, db)
            return {
                "message": "The kids were FBV (FEDERAL BUREAU OF VEGETABLES!!), You gone straight to jail.",
                "nav": "/jail?apikey=YOURAPIKEY",
                "level": api_key.level
            }
        elif choice == 2:
            update_level(api_key, 5, db)
            return {
                "message": "You became a shopkeeper's show item. You are now on display.",
                "level": api_key.level
            }
        else:
            return {"message": "Invalid choice. Please choose 1 or 2."}
    else:
        return {"message": "You are not at the correct level to access this endpoint.", "level": api_key.level}

@app.get("/jail")
async def root(api_key: APIKey = Depends(verify_api_key)):
    if api_key.level==4:
        return {"message": "You see some rotten veggies in the jail cell. They seem to be looking at you and saying something.", "level": api_key.level,"mission":"go to /rotten_veggies?apikey=YOURAPIKEY"} 
    
@app.get("/rotten_veggies")#they tell you to do something
async def root(api_key: APIKey = Depends(verify_api_key), choice: int = Query(None)):
    if api_key.level==4:
        if choice==None:
            return {"message":"they tell you to do something for them","choices": {1: "do what they say",2:"dont do what they say"}}
        elif choice==1:
            return {"message": "they say you've got guts","level": api_key.level,"mission":"go to /do_what_they_say?apikey=YOURAPIKEY"}
        elif choice==2:
            return {"message": "they say you've got guts","level": api_key.level,"mission":"go to /dont_do_what_they_say?apikey=YOURAPIKEY"}
        else:
            return {"message": "Invalid choice. Please choose 1 or 2."}

@app.get("/do_what_they_say")
async def root(api_key: APIKey = Depends(verify_api_key)):
    return {"message":"they tell you to smuggle some syntethic fertilizer in","TO DO:": "do a POST req to /smuggle_fertilizer with an argument (intruction in docs) of this famous riddle","riddle":"Guac is my fame, but what is my name?"}

@app.get("/dont_do_what_they_say")
async def root(api_key: APIKey = Depends(verify_api_key)):
    return {"hint":"insert nike's slogan here"}
@app.get("/the_mafia_gets_her_killed")#The End you completed the game (fake ending)
async def root(api_key: APIKey = Depends(verify_api_key)):
    if api_key.level==3:
        return {"message":"you see the flowers sister and immediately flirt with her and she flirts back and asks you to come to her place","level": api_key.level,"mission":"go to /enjoy_hybridisation_with_the_flowers_sister"}


@app.get("/jury_flower")
async def root(api_key: APIKey = Depends(verify_api_key)):
    if api_key.level==2: 
        return {"message": "you  go to jail no matter due to the speciest laws","waitaminute":"The guard comes in and tell you someone bailed you out","level": api_key.level,"mission":"go to /bailout_j to meet the person who bailed you out"}

@app.get("/enjoy_hybridisation_with_the_flowers_sister")#the mafia was her she killed you and cut you and also threw your seed in the fire
async def root(api_key: APIKey = Depends(verify_api_key)):
    if api_key.level==6:
        return {"message": "The mafia was her (the flower) she killed you and cut you and also threw your seed in the fire","level": api_key.level}

@app.get("/bailout_j")#Jonhny Pepp(pepper) bails you out and helps you fight the flower with the help of his lawyer
async def root(api_key: APIKey = Depends(verify_api_key)):
    if api_key.level==2:
        return {"message": "Jonhny Pepp(pepper) bails you out and tells you he can help you fight the flower with the help of his lawyer","test":"to test you he puts a jar of powdered sugar on the table","level": api_key.level,"mission":"go to /do_a_jar_of_powdered_sugar or to /dont_do_the_jar_of_powdered_sugar"}

@app.get("/do_a_jar_of_powdered_sugar")#you're cool you get to fight the flower
async def root(api_key: APIKey = Depends(verify_api_key)):
    if api_key.level==2:
        api_key.level=1
        return {"message": "you're cool you get to fight the flower","status":"Game Over ;)(ik its a lame game)","level": api_key.level,"reset":"game has been reset try going to /"}

@app.get("/dont_do_the_jar_of_powdered_sugar")#you're lame get tf out of here
async def root(api_key: APIKey = Depends(verify_api_key)):
    if api_key.level==2:
        return {"message": "you're lame get tf out of here","status":"pls do some sugar","level": api_key.level}

@app.get("/level")
async def get_level(api_key: APIKey = Depends(verify_api_key)):
    return {"level": api_key.level}
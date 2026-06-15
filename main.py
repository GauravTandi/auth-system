from fastapi import FastAPI, Depends
from database import Base, engine, SessionLocal
from models import User
from schemas import UserCreate
from auth import hash_password
from sqlalchemy.orm import Session
import models


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Auth system running"}


#DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup")
def singup(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pwd = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_pwd,
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User Created successfully",
        "user_id": new_user.id
    }

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models.user import User
from crud.database import get_db
from fastapi import Request


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_password_hash(password: str):
    return pwd_context.hash(password)

@router.post("/register")
def register_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(password)
    db_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"msg": "User created successfully"}

@router.post("/login")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user or not pwd_context.verify(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"msg": "Login successful", "user": db_user}

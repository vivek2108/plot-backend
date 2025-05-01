from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models.users import Users as UsersModel
from schemas.users import Users
from schemas.users import UsersBase, UserCredential
from crud.database import get_db
from crud.users import create_user as create_user_crud
from fastapi import Request


router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_password_hash(password: str):
    return pwd_context.hash(password)

@router.post("/register",
             status_code=status.HTTP_201_CREATED,
             response_model=Users,
)
def create_user(request: Request, payload: UserCredential, db: Session = Depends(get_db)):
    return create_user_crud(db, payload)
    # payload = payload.model_dump(exclude={"resource_type"})
    # # db_user = db.query(UsersModel).filter(UsersModel.email == payload.email).first()
    # # if db_user:
    # #     raise HTTPException(status_code=400, detail="Email already registered")
    # hashed_password = get_password_hash(payload.password)
    # db_user = UsersModel(username=payload.username, email=payload.email, hashed_password=hashed_password)
    # db.add(db_user)
    # db.commit()
    # db.refresh(db_user)
    # return {"msg": "User created successfully"}

@router.post("/login")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(UsersModel).filter(UsersModel.email == email).first()
    if not db_user or not pwd_context.verify(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"msg": "Login successful", "user": db_user}

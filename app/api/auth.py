from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.users import Users as UsersModel
from app.schemas.users import Users
from app.schemas.users import UserCredential, UserLogin
from app.config.database import get_db
from app.crud.users import create_user as create_user_crud, validate_user


router = APIRouter()

@router.post("/register",
             status_code=status.HTTP_201_CREATED,
             response_model=Users,
)
def create_user(payload: UserCredential, db: Session = Depends(get_db)):
    return create_user_crud(db, payload)


@router.post("/login",
             response_model=dict,)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    if validate_user(db, payload):
        return {"msg": "Successful"}
    return {"msg": "Failed"}

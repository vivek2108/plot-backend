from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.auth import create_access_token
from app.config.database import get_db
from app.crud.users import authenticate_user
from app.schemas.users import UserLogin

router = APIRouter()


@router.post(
    "/login",
    response_model=dict,
)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, payload)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    data = {"sub": user.username, "role": user.role.name, "user_id": user.id}
    access_token = create_access_token(data=data, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token")
def token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    data = {"sub": user.username, "role": user.role.name, "user_id": user.id}
    access_token = create_access_token(data=data)
    return {"access_token": access_token, "token_type": "bearer"}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.users import Users as UsersModel
from app.schemas.users import Users
from app.schemas.users import UserCredential, UsersBase
from app.config.database import get_db
from app.crud.users import get_user, update_user, create_user, get_all_user
from typing import List
from app.auth.auth import get_current_user
from app.auth.auth import require_role


router = APIRouter()


@router.get("/",
             response_model=List[Users],)
def fetch_all(db: Session = Depends(get_db), user: dict = Depends(require_role(["admin"]))):
    return get_all_user(db)


@router.get("/{id}",)
            #  response_model=dict,)
def get(id: int, db: Session = Depends(get_db), current_user: UsersModel = Depends(get_current_user)):
    if current_user["user_id"] != id:
        raise HTTPException(status_code=403, detail="Access denied to other user's data")

    user = get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/register",
             status_code=status.HTTP_201_CREATED,
             response_model=Users,
)
def create(payload: UserCredential, db: Session = Depends(get_db), current_user: dict = Depends(require_role(["admin"]))):
    return create_user(db, payload, current_user)


@router.put("/update/{id}",
             response_model=Users,)
def update(payload: UsersBase, id: int, db: Session = Depends(get_db), current_user: UsersModel = Depends(get_current_user)):
    payload.updated_by = current_user
    return update_user(db, id, payload, current_user)

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth import get_current_user, require_role
from app.auth.currentuser import CurrentUser
from app.config.database import get_db
from app.crud.users import create_user, get_all_user, get_user, update_user
from app.schemas.users import UserCredential, Users

router = APIRouter()


@router.get(
    "/",
    response_model=List[Users],
)
# @require_role(["admin"])
def fetch_all(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_role(["admin"])),
):
    return get_all_user(db)


@router.get(
    "/{id}",
    response_model=Users,
)
# @require_auth
def get(
    id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.user_id != id:
        raise HTTPException(
            status_code=403, detail="Access denied to other user's data"
        )

    user = get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=Users,
)
def create(
    payload: UserCredential,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_role(["admin"])),
):
    return create_user(db, payload, current_user)


@router.put(
    "/{id}",
    response_model=Users,
)
def update(
    payload: UserCredential,
    id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.is_admin() or current_user.user_id == id:
        return update_user(db, id, payload, current_user)
    raise HTTPException(status_code=403, detail="Access denied to other user's data")

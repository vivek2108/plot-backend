from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth.auth import get_current_user, require_role
from app.auth.currentuser import CurrentUser
from app.config.database import get_db
from app.crud.buyers import (create_buyer, get_all_buyers, get_buyer,
                             update_buyer)
from app.schemas.buyers import Buyers, BuyersBase

router = APIRouter()


@router.get(
    "/",
    response_model=List[Buyers],
)
def fetch_all(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_role(["admin", "manager"])),
):
    return get_all_buyers(db)


@router.get(
    "/{id}",
    response_model=Buyers,
)
def get(
    id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return get_buyer(db, id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Buyers,
)
def create(
    payload: BuyersBase,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_role(["admin", "manager"])),
):
    return create_buyer(db, payload, current_user)


@router.put(
    "/{id}",
    response_model=Buyers,
)
def update(
    payload: BuyersBase,
    id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return update_buyer(db, id, payload, current_user)

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth import get_current_user, require_role
from app.auth.currentuser import CurrentUser
from app.config.database import get_db
from app.crud.buyers import create_buyer, get_all_buyers, get_buyer, update_buyer, soft_delete_buyer
from app.schemas.buyers import Buyers, BuyersBase

router = APIRouter()


@router.get("/", response_model=List[Buyers])
def fetch_all(
    db: Session = Depends(get_db),
    skip: int = 0,  # Pagination
    limit: int = 10,  # Pagination
    filters: dict = {},  # Optional filters
    current_user: CurrentUser = Depends(require_role(["admin", "manager"])),
) -> List[Buyers]:
    """
    Get a list of all buyers.
    Access restricted to users with 'admin' or 'manager' roles.

    Args:
        db (Session): Database session.
        current_user (CurrentUser): Authenticated user with proper role.

    Returns:
        List[Buyers]: List of buyer records.
    """
    return get_all_buyers(db, skip=skip, limit=limit, filters=filters)


@router.get("/{id}", response_model=Buyers)
def get(
    id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> Buyers:
    """
    Retrieve a single buyer by ID.
    Authenticated access required.

    Args:
        id (int): Buyer ID.
        db (Session): Database session.
        current_user (CurrentUser): Authenticated user.

    Returns:
        Buyers: Buyer details.
    """
    return get_buyer(db, id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Buyers)
def create(
    payload: BuyersBase,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_role(["admin", "manager"])),
) -> Buyers:
    """
    Create a new buyer.
    Access restricted to users with 'admin' or 'manager' roles.

    Args:
        payload (BuyersBase): Data for the new buyer.
        db (Session): Database session.
        current_user (CurrentUser): Authenticated user with proper role.

    Returns:
        Buyers: The newly created buyer.
    """
    return create_buyer(db, payload, current_user)


@router.put("/{id}", response_model=Buyers)
def update(
    id: int,
    payload: BuyersBase,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> Buyers:
    """
    Update an existing buyer by ID.
    Authenticated access required.

    Args:
        id (int): Buyer ID.
        payload (BuyersBase): Updated buyer data.
        db (Session): Database session.
        current_user (CurrentUser): Authenticated user.

    Returns:
        Buyers: Updated buyer record.
    """
    return update_buyer(db, id, payload, current_user)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    buyer = soft_delete_buyer(db, id, current_user)
    if not buyer:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return {"detail": "Buyer soft deleted"}

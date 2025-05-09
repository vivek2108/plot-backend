from sqlalchemy import func
from sqlalchemy.orm import Session

from app.auth.currentuser import CurrentUser
from app.models.buyers import Buyers as BuyersModel
from app.schemas.buyers import BuyersBase


def create_buyer(db: Session, buyer: BuyersBase, current_user: CurrentUser):
    """
    Create a new buyer record in the database.

    Args:
        db (Session): SQLAlchemy DB session.
        buyer (BuyersBase): Input schema with buyer details.
        current_user (CurrentUser): Authenticated user creating the entry.

    Returns:
        BuyersModel: The newly created buyer record.
    """
    buyer_data = buyer.dict(exclude={"resource_type"})
    buyer_data["created_by"] = current_user.username
    buyer_data["updated_by"] = current_user.username
    db_buyer = BuyersModel(**buyer_data)

    db.add(db_buyer)
    db.commit()
    db.refresh(db_buyer)
    return db_buyer


def get_buyer(db: Session, buyer_id: int) -> BuyersModel | None:
    """
    Retrieve a buyer by ID.

    Args:
        db (Session): DB session.
        buyer_id (int): ID of the buyer.

    Returns:
        BuyersModel | None: Buyer object if found, else None.
    """
    return (
        db.query(BuyersModel)
        .filter(BuyersModel.id == buyer_id, BuyersModel.deleted_at == None)
        .first()
    )


def get_all_buyers(
    db: Session, skip: int = 0, limit: int = 10, filters: dict = None
) -> list[BuyersModel]:
    """
    Fetch all buyers from the database with pagination and optional filters.

    Args:
        db (Session): DB session.
        skip (int): The number of records to skip (pagination).
        limit (int): The number of records to return.
        filters (dict): Filters to apply to the query, e.g. {"name": "buyer name"}.

    Returns:
        list[BuyersModel]: List of buyers with applied filters and pagination.
    """
    query = db.query(BuyersModel).filter(
        BuyersModel.deleted_at == None
    )  # Exclude soft-deleted records

    # Apply filters if provided
    if filters:
        for field, value in filters.items():
            query = query.filter(
                getattr(BuyersModel, field).ilike(f"%{value}%")
            )  # Case-insensitive search

    # Apply pagination
    query = query.offset(skip).limit(limit)

    return query.all()


def update_buyer(
    db: Session, buyer_id: int, buyer_update: BuyersBase, current_user: CurrentUser
) -> BuyersModel | None:
    """
    Update a buyer's details.

    Args:
        db (Session): DB session.
        buyer_id (int): ID of the buyer to update.
        buyer_update (BuyersBase): Fields to update.
        current_user (CurrentUser): User making the update.

    Returns:
        BuyersModel | None: Updated buyer or None if not found.
    """
    buyer = db.query(BuyersModel).filter(BuyersModel.id == buyer_id).first()
    if not buyer:
        return None

    update_data = {
        key: value
        for key, value in buyer_update.dict(exclude_unset=True).items()
        if value not in (None, "")
    }

    for field, value in update_data.items():
        setattr(buyer, field, value)

    buyer.updated_by = current_user.username
    db.commit()
    db.refresh(buyer)
    return buyer


def soft_delete_buyer(
    db: Session, buyer_id: int, current_user: CurrentUser
) -> BuyersModel | None:
    """
    Soft delete a buyer by setting the `deleted_at` field to the current time.

    Args:
        db (Session): DB session.
        buyer_id (int): ID of the buyer to delete.
        current_user (CurrentUser): The user performing the deletion.

    Returns:
        BuyersModel | None: The deleted buyer, or None if not found.
    """
    buyer = db.query(BuyersModel).filter(BuyersModel.id == buyer_id).first()
    if not buyer:
        return None

    buyer.deleted_at = func.now()  # Set the deletion timestamp
    buyer.updated_by = current_user.username
    db.commit()
    db.refresh(buyer)
    return buyer

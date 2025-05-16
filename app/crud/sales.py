from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.auth.currentuser import CurrentUser
from app.models.sales import Sales as SalesModel
from app.schemas.sales import SalesBase, SaleUpdate


def create_sale(db: Session, sale: SalesBase, current_user: CurrentUser) -> SalesModel:
    """
    Create a new sale entry in the database.

    Args:
        db (Session): SQLAlchemy database session.
        sale (SalesBase): Sale input data.
        current_user (CurrentUser): The user creating the sale.

    Returns:
        SalesModel: The created sale record.
    """
    sale_data = sale.dict(exclude={"resource_type"})
    sale_data["created_by"] = current_user.username
    sale_data["updated_by"] = current_user.username
    db_sale = SalesModel(**sale_data)

    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale


def get_sale(db: Session, sale_id: int) -> Optional[SalesModel]:
    """
    Retrieve a single sale record by its ID.

    Args:
        db (Session): SQLAlchemy session.
        sale_id (int): Sale ID to retrieve.

    Returns:
        Optional[SalesModel]: Sale record if found, else None.
    """
    return db.query(SalesModel).filter(SalesModel.id == sale_id).first()


def get_all_sales(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[Dict[str, str]] = None,
) -> List[SalesModel]:
    """
    Retrieve all sales records, with optional filters and pagination.

    Args:
        db (Session): SQLAlchemy session.
        skip (int): Number of records to skip (for pagination).
        limit (int): Max number of records to return.
        filters (Optional[Dict[str, str]]): Optional filters (field-value pairs).

    Returns:
        List[SalesModel]: List of sales records.
    """
    query = db.query(SalesModel)

    if filters:
        for field, value in filters.items():
            if hasattr(SalesModel, field):
                query = query.filter(getattr(SalesModel, field).ilike(f"%{value}%"))

    return query.offset(skip).limit(limit).all()


def update_sale(
    db: Session,
    sale_id: int,
    sale: SaleUpdate,
    current_user: CurrentUser,
) -> Optional[SalesModel]:
    """
    Update an existing sale record with new data.

    Args:
        db (Session): SQLAlchemy session.
        sale_id (int): ID of the sale to update.
        sale (SaleUpdate): New data to update.
        current_user (CurrentUser): User performing the update.

    Returns:
        Optional[SalesModel]: Updated sale record, or None if not found.
    """
    db_sale = get_sale(db, sale_id)
    if not db_sale:
        return None

    update_data = {
        key: value
        for key, value in sale.dict(exclude_unset=True).items()
        if value not in (None, "")
    }

    for field, value in update_data.items():
        setattr(db_sale, field, value)

    db_sale.updated_by = current_user.username
    db.commit()
    db.refresh(db_sale)
    return db_sale


# def delete_sale(db: Session, sale_id: int, current_user: CurrentUser):
#     db_sale = get_sale(db, sale_id)
#     if not db_sale:
#         return None
#     db.delete(db_sale)
#     db.commit()
#     return db_sale

from sqlalchemy.orm import Session

from app.auth.currentuser import CurrentUser
from app.models.sales import Sales as SalesModel
from app.schemas.sales import Sales, SalesBase, SaleUpdate


def create_sale(db: Session, sale: SalesBase, current_user: CurrentUser):
    sale_data = sale.dict(exclude={"resource_type"})
    sale_data["created_by"] = current_user.username
    sale_data["updated_by"] = current_user.username
    db_sale = SalesModel(**sale_data)

    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale


def get_sale(db: Session, sale_id: int):
    return db.query(SalesModel).filter(SalesModel.id == sale_id).first()


def get_all_sales(db: Session, skip: int = 0, limit: int = 100, filters: dict = None):
    query = db.query(SalesModel)

    # Apply filters if provided
    if filters:
        for field, value in filters.items():
            query = query.filter(
                getattr(SalesModel, field).ilike(f"%{value}%")
            )  # Case-insensitive search

    # Apply pagination
    query = query.offset(skip).limit(limit)

    return query.all()


def update_sale(db: Session, sale_id: int, sale: SaleUpdate, current_user: CurrentUser):
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

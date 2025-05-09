from sqlalchemy.orm import Session

from app.auth.currentuser import CurrentUser
from app.models.buyers import Buyers as BuyersModel
from app.schemas.buyers import BuyersBase


def create_buyer(db: Session, buyer: BuyersBase, current_user: CurrentUser):
    buyer_data = buyer.dict(exclude={"resource_type"})
    buyer_data["created_by"] = current_user.username
    buyer_data["updated_by"] = current_user.username
    db_buyer = BuyersModel(**buyer_data)

    db.add(db_buyer)
    db.commit()
    db.refresh(db_buyer)
    return db_buyer


def get_buyer(db: Session, buyer_id: int):
    return db.query(BuyersModel).filter(BuyersModel.id == buyer_id).first()


def get_all_buyers(db: Session):
    return db.query(BuyersModel).all()


def update_buyer(
    db: Session, buyer_id: int, buyer_update: BuyersBase, current_user: CurrentUser
):
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

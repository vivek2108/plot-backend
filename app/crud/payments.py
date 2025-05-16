from sqlalchemy.orm import Session

from app.auth.currentuser import CurrentUser
from app.models.payments import Payments as PaymentsModel
from app.schemas.payments import PaymentBase, PaymentUpdate


def create_payment(db: Session, payment: PaymentBase, current_user: CurrentUser):
    db_payment = PaymentsModel(**payment.dict(exclude={"resource_type"}))
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def get_payment(db: Session, payment_id: int):
    return (
        db.query(PaymentsModel)
        .filter(PaymentsModel.id == payment_id, PaymentsModel.is_deleted == False)
        .first()
    )


def get_all_payments(
    db: Session, skip: int = 0, limit: int = 100, filters: dict = None
):

    query = db.query(PaymentsModel).filter(
        PaymentsModel.is_deleted == False
    )  # Exclude soft-deleted records

    # Apply filters if provided
    if filters:
        for field, value in filters.items():
            query = query.filter(
                getattr(PaymentsModel, field).ilike(f"%{value}%")
            )  # Case-insensitive search

    # Apply pagination
    query = query.offset(skip).limit(limit)

    return query.all()


def update_payment(
    db: Session, payment_id: int, payment: PaymentUpdate, current_user: CurrentUser
):
    db_payment = get_payment(db, payment_id)
    if not db_payment:
        return None
    update_data = {
        key: value
        for key, value in payment.dict(exclude_unset=True).items()
        if value not in (None, "")
    }

    for field, value in update_data.items():
        setattr(db_payment, field, value)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def soft_delete_payments(db: Session, payment_id: int, current_user: CurrentUser):
    db_payment = get_payment(db, payment_id)
    if not db_payment or db_payment.is_deleted:
        return None
    db_payment.is_deleted = True
    db.commit()
    db.refresh(db_payment)
    return db_payment


def read_deleted_payments(db: Session):
    return db.query(PaymentsModel).filter(PaymentsModel.is_deleted == True).all()

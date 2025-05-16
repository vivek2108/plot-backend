from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.auth.currentuser import CurrentUser
from app.models.payments import Payments as PaymentsModel
from app.schemas.payments import PaymentBase, PaymentUpdate


def create_payment(
    db: Session, payment: PaymentBase, current_user: CurrentUser
) -> PaymentsModel:
    """
    Create a new payment entry.

    Args:
        db (Session): SQLAlchemy session.
        payment (PaymentBase): Payment input data.
        current_user (CurrentUser): The user performing the action.

    Returns:
        PaymentsModel: The newly created payment record.
    """
    db_payment = PaymentsModel(**payment.dict(exclude={"resource_type"}))
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def get_payment(db: Session, payment_id: int) -> Optional[PaymentsModel]:
    """
    Fetch a single payment record by its ID, excluding soft-deleted ones.

    Args:
        db (Session): SQLAlchemy session.
        payment_id (int): Payment ID.

    Returns:
        Optional[PaymentsModel]: The payment if found, otherwise None.
    """
    return (
        db.query(PaymentsModel)
        .filter(PaymentsModel.id == payment_id, PaymentsModel.is_deleted.is_(False))
        .first()
    )


def get_all_payments(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    filters: Optional[Dict[str, str]] = None,
) -> List[PaymentsModel]:
    """
    Retrieve a paginated list of payments, with optional filters.

    Args:
        db (Session): SQLAlchemy session.
        skip (int): Number of records to skip.
        limit (int): Max number of records to return.
        filters (Optional[Dict[str, str]]): Optional field-based filters.

    Returns:
        List[PaymentsModel]: List of payment records.
    """
    query = db.query(PaymentsModel).filter(PaymentsModel.is_deleted.is_(False))

    if filters:
        for field, value in filters.items():
            if hasattr(PaymentsModel, field):
                query = query.filter(getattr(PaymentsModel, field).ilike(f"%{value}%"))

    return query.offset(skip).limit(limit).all()


def update_payment(
    db: Session,
    payment_id: int,
    payment: PaymentUpdate,
    current_user: CurrentUser,
) -> Optional[PaymentsModel]:
    """
    Update an existing payment with provided values.

    Args:
        db (Session): SQLAlchemy session.
        payment_id (int): ID of the payment to update.
        payment (PaymentUpdate): Fields to update.
        current_user (CurrentUser): The user performing the update.

    Returns:
        Optional[PaymentsModel]: Updated payment record, or None if not found.
    """
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


def soft_delete_payments(
    db: Session,
    payment_id: int,
    current_user: CurrentUser,
) -> Optional[PaymentsModel]:
    """
    Soft delete a payment record by setting its is_deleted flag.

    Args:
        db (Session): SQLAlchemy session.
        payment_id (int): ID of the payment to soft delete.
        current_user (CurrentUser): The user performing the delete.

    Returns:
        Optional[PaymentsModel]: The updated payment record, or None if not found.
    """
    db_payment = get_payment(db, payment_id)
    if not db_payment or db_payment.is_deleted:
        return None

    db_payment.is_deleted = True
    db.commit()
    db.refresh(db_payment)
    return db_payment


def read_deleted_payments(db: Session) -> List[PaymentsModel]:
    """
    Retrieve all payments that have been soft-deleted.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[PaymentsModel]: List of soft-deleted payment records.
    """
    return db.query(PaymentsModel).filter(PaymentsModel.is_deleted.is_(True)).all()

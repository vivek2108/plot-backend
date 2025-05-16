from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth import get_current_user, require_role
from app.auth.currentuser import CurrentUser
from app.config.database import get_db
from app.core.logger import get_logger
from app.crud.payments import (
    create_payment,
    get_all_payments,
    get_payment,
    read_deleted_payments,
    soft_delete_payments,
    update_payment,
)
from app.schemas.payments import PaymentBase, PaymentOut, PaymentUpdate

logger = get_logger(__name__)
router = APIRouter()


@router.get("/", response_model=List[PaymentOut], summary="List Payments")
def list_payments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_role(["admin", "manager"])),
):
    """
    Retrieve a list of active (non-deleted) payments.

    - Requires `admin` or `manager` role.
    - Supports pagination via `skip` and `limit`.
    """
    payments = get_all_payments(db, skip=skip, limit=limit)
    logger.info(f"Retrieved {len(payments)} payments for user {current_user.email}")
    return payments


@router.get("/{payment_id}", response_model=PaymentOut, summary="Get Payment by ID")
def retrieve_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    """
    Retrieve a specific payment by its ID.

    - Accessible by any authenticated user.
    """
    payment = get_payment(db, payment_id)
    if not payment:
        logger.warning(
            f"Payment ID {payment_id} not found by user {current_user.email}"
        )
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PaymentOut,
    summary="Create Payment",
)
def create_new_payment(
    payment: PaymentBase,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    """
    Create a new payment entry.

    - Accessible by any authenticated user.
    """
    new_payment = create_payment(db, payment, current_user)
    logger.info(f"Payment created by user {current_user.email}")
    return new_payment


@router.put("/{payment_id}", response_model=PaymentOut, summary="Update Payment")
def update_existing_payment(
    payment_id: int,
    payment: PaymentUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    """
    Update an existing payment by ID.

    - Accessible by any authenticated user.
    - Returns 404 if payment does not exist.
    """
    updated = update_payment(db, payment_id, payment, current_user)
    if not updated:
        logger.warning(f"Attempted to update non-existent payment ID {payment_id}")
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated


@router.delete(
    "/{payment_id}", response_model=PaymentOut, summary="Soft Delete Payment"
)
def soft_delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    """
    Soft delete a payment (mark as deleted but not removed from DB).

    - Accessible by any authenticated user.
    - Returns 404 if payment does not exist.
    """
    deleted = soft_delete_payments(db, payment_id, current_user)
    if not deleted:
        logger.warning(f"Attempted to delete non-existent payment ID {payment_id}")
        raise HTTPException(status_code=404, detail="Payment not found")
    return deleted


@router.get(
    "/deleted/", response_model=List[PaymentOut], summary="List Soft Deleted Payments"
)
def list_deleted_payments(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_role(["admin"])),
):
    """
    Retrieve a list of soft-deleted payments.

    - Requires `admin` role.
    """
    deleted_payments = read_deleted_payments(db)
    logger.info(
        f"User {current_user.email} viewed {len(deleted_payments)} deleted payments"
    )
    return deleted_payments


# from fastapi import BackgroundTasks

# def send_sms_background(background_tasks: BackgroundTasks,
#  msg: str, phone_number: str):
#     background_tasks.add_task(send_sms, msg, phone_number)

# def create_payment_upd(db: Session, payment: PaymentCreate,
#  background_tasks: BackgroundTasks):
#     db_payment = Payments(**payment.dict())
#     db.add(db_payment)
#     db.commit()
#     db.refresh(db_payment)

#     # Lookup phone number
#     sale = db.query(Sales).filter(Sales.id == db_payment.sale_id).first()
#     if sale and sale.buyer and sale.buyer.phone_number:
#         phone_number = sale.buyer.phone_number
#         msg = (
#             f"Payment Confirmation: ₹{db_payment.amount_paid} received. "
#             f"Remaining Balance: ₹{db_payment.remaining_balance}. "
#             f"Thank you for your payment!"
#         )
#         send_sms_background(background_tasks, msg, phone_number)

#     return db_payment

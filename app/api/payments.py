from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth import get_current_user, require_role
from app.auth.currentuser import CurrentUser
from app.config.database import get_db
from app.core.logger import get_logger
from app.crud.payments import (create_payment, soft_delete_payments,
                               get_all_payments, get_payment,
                               read_deleted_payments, update_payment)
from app.schemas.payments import PaymentBase, PaymentOut, PaymentUpdate

logger = get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=List[PaymentOut])
def get_payments(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    # filters: dict = {},
    current_user: CurrentUser = Depends(require_role(["admin", "manager"])),
):
    return get_all_payments(db, skip=skip, limit=limit)


@router.get("/{payment_id}", response_model=PaymentOut)
def get(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    db_payment = get_payment(db, payment_id)
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    return db_payment


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PaymentOut)
def create(
    payment: PaymentBase,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return create_payment(db, payment, current_user)


@router.put("/{payment_id}", response_model=PaymentOut)
def update(
    payment_id: int,
    payment: PaymentUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    db_payment = update_payment(db, payment_id, payment, current_user)
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment


@router.delete("/{payment_id}", response_model=PaymentOut)
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    db_payment = soft_delete_payments(db, payment_id, current_user)
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment


@router.get("/deleted/", response_model=List[PaymentOut])
def read_soft_deleted_payments(db: Session = Depends(get_db)):
    return read_deleted_payments(db)


# from fastapi import BackgroundTasks

# def send_sms_background(background_tasks: BackgroundTasks, msg: str, phone_number: str):
#     background_tasks.add_task(send_sms, msg, phone_number)

# def create_payment_upd(db: Session, payment: PaymentCreate, background_tasks: BackgroundTasks):
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

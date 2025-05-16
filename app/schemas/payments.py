from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PaymentBase(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True, from_attributes=True
    )  # Switch alias and field name

    resource_type: Optional[str] = Field("Payments", alias="resourceType")
    sale_id: int
    amount_paid: Decimal
    payment_date: date
    payment_mode: str | None = None
    remaining_balance: Decimal


class PaymentUpdate(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True, from_attributes=True
    )  # Switch alias and field name

    amount_paid: Decimal | None = None
    payment_date: date
    payment_mode: str | None = None
    remaining_balance: Decimal | None = None


class PaymentOut(PaymentBase):
    id: int
    is_deleted: bool = False  # Optional

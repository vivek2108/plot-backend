from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PaymentBase(BaseModel):
    """
    Shared fields used for creating or displaying a payment.
    """

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    resource_type: Optional[str] = Field(
        default="Payments",
        alias="resourceType",
        description="Resource type identifier for API consumers.",
    )
    sale_id: int = Field(..., description="ID of the associated sale.")
    amount_paid: Decimal = Field(..., description="Amount paid in the transaction.")
    payment_date: date = Field(..., description="Date of the payment.")
    payment_mode: Optional[str] = Field(
        None, description="Mode of payment (e.g., Cash, Bank, UPI)."
    )
    remaining_balance: Decimal = Field(
        ..., description="Outstanding amount remaining after the payment."
    )


class PaymentUpdate(BaseModel):
    """
    Fields allowed for updating an existing payment.
    All fields are optional to support partial updates.
    """

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    amount_paid: Optional[Decimal] = Field(None, description="Updated amount paid.")
    payment_date: Optional[date] = Field(None, description="Updated payment date.")
    payment_mode: Optional[str] = Field(None, description="Updated payment mode.")
    remaining_balance: Optional[Decimal] = Field(
        None, description="Updated remaining balance."
    )


class PaymentOut(PaymentBase):
    """
    Full representation of a Payment as returned from the API.
    Inherits all fields from PaymentBase.
    """

    id: int = Field(..., description="Unique identifier for the payment.")
    is_deleted: bool = Field(
        False, description="Flag indicating if the payment is soft-deleted."
    )

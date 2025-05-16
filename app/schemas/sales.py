from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SalesBase(BaseModel):
    """
    Base schema for creating or referencing a sale.
    Used in create and output schemas.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )

    resource_type: Optional[str] = Field(
        default="Sales",
        alias="resourceType",
        description="Resource type identifier for API clients.",
    )
    plot_id: int = Field(..., description="ID of the plot being sold.")
    associate_id: int = Field(
        ..., description="ID of the sales associate handling the sale."
    )
    buyer_id: int = Field(..., description="ID of the buyer making the purchase.")
    sale_amount: Decimal = Field(..., description="Total sale amount.")
    payment_mode: Optional[str] = Field(
        None, description="Mode of payment (e.g., Cash, UPI, Bank Transfer)."
    )
    payment_timeframe: datetime = Field(
        ..., description="Expected or actual payment timeframe."
    )
    sale_date: date = Field(..., description="Date on which the sale was made.")


class SaleUpdate(BaseModel):
    """
    Fields allowed to update in a sale record.
    Allows partial updates (PATCH-style).
    """

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )

    payment_mode: Optional[str] = Field(None, description="Updated payment method.")
    payment_timeframe: Optional[datetime] = Field(
        None, description="Updated payment timeframe."
    )


class Sales(SalesBase):
    """
    Output schema for a Sale record.
    Inherits from SalesBase and includes metadata.
    """

    id: int = Field(..., description="Unique identifier for the sale.")

    created_by: Optional[str] = Field(
        None,
        alias="createdBy",
        description="Username of the user who created this record.",
    )
    updated_by: Optional[str] = Field(
        None,
        alias="updatedBy",
        description="Username of the user who last updated this record.",
    )
    create_dt: Optional[datetime] = Field(
        None,
        alias="createDate",
        description="Timestamp of when this record was created.",
    )
    update_dt: Optional[datetime] = Field(
        None,
        alias="updateDate",
        description="Timestamp of the most recent update to this record.",
    )

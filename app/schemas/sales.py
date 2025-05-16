from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SalesBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
    resource_type: Optional[str] = Field("Sales", alias="resourceType")

    plot_id: int
    associate_id: int
    buyer_id: int
    sale_amount: Decimal
    payment_mode: Optional[str] = None
    payment_timeframe: datetime
    sale_date: date


class SaleUpdate(BaseModel):

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
    payment_mode: Optional[str] = None
    payment_timeframe: Optional[datetime] = None


class Sales(SalesBase):
    id: int
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
        None, alias="createDate", description="Timestamp of record creation."
    )
    update_dt: Optional[datetime] = Field(
        None, alias="updateDate", description="Timestamp of record last update."
    )

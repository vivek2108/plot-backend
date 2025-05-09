"""Schema for buyers."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BuyersBase(BaseModel):
    """Base class to handle http request"""

    model_config = ConfigDict(
        populate_by_name=True, from_attributes=True
    )  # Switch alias and field name

    resource_type: Optional[str] = Field("Buyers", alias="resourceType")
    name: str = Field()
    contact: Optional[str] = Field()
    address: Optional[str] = Field()
    id_proof_path: Optional[str] = Field()


class Buyers(BuyersBase):
    """Base class to handle http request

    Args:
        BuyersBase: Inherits from the BuyersBase
    """

    id: int = Field()
    created_by: Optional[str] = Field(alias="createdBy")
    updated_by: Optional[str] = Field(alias="updatedBy")
    create_dt: Optional[datetime] = Field(alias="createDate")
    update_dt: Optional[datetime] = Field(alias="updateDate")

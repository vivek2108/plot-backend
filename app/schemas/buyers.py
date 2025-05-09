"""Schema for buyers."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class BuyersBase(BaseModel):
    """
    Base class to handle HTTP requests for the 'buyers' resource.

    Attributes:
        resource_type (Optional[str]): The type of the resource, defaulting to 'Buyers'.
        name (str): The name of the buyer (required).
        contact (Optional[str]): Contact information for the buyer (optional).
        address (Optional[str]): Address of the buyer (optional).
        id_proof_path (Optional[str]): Path to the buyer's ID proof (optional).
        
    Configuration:
        - Switches alias and field name with `populate_by_name=True, from_attributes=True`.
    """
    model_config = ConfigDict(
        populate_by_name=True, from_attributes=True
    )  # Switch alias and field name

    resource_type: Optional[str] = Field("Buyers", alias="resourceType")
    name: str = Field(..., description="The name of the buyer.")
    contact: Optional[str] = Field(None, description="Contact information of the buyer.")
    address: Optional[str] = Field(None, description="The address of the buyer.")
    id_proof_path: Optional[str] = Field(None, description="File path to the buyer's ID proof.")


class Buyers(BuyersBase):
    """
    Full class to represent a 'buyer' in the system, inheriting from `BuyersBase`.

    This schema includes additional fields for metadata and timestamps.

    Attributes:
        id (int): The unique identifier for the buyer.
        created_by (Optional[str]): The username of the user who created this record (optional).
        updated_by (Optional[str]): The username of the user who last updated this record (optional).
        create_dt (Optional[datetime]): Timestamp of when the buyer was created.
        update_dt (Optional[datetime]): Timestamp of when the buyer's record was last updated.
        
    Args:
        BuyersBase: Inherits common fields from the `BuyersBase` schema.
    """
    id: int = Field(..., description="Unique identifier for the buyer.")
    created_by: Optional[str] = Field(None, alias="createdBy", description="Username of the user who created this record.")
    updated_by: Optional[str] = Field(None, alias="updatedBy", description="Username of the user who last updated this record.")
    create_dt: Optional[datetime] = Field(None, alias="createDate", description="Timestamp of record creation.")
    update_dt: Optional[datetime] = Field(None, alias="updateDate", description="Timestamp of record last update.")

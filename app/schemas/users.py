"""Schema for Job Family."""

from datetime import datetime
from typing import Optional

from pydantic import Field
from pydantic import BaseModel
from pydantic import ConfigDict


class UsersBase(BaseModel):
    """Base class to handle http request
    """

    model_config = ConfigDict(
        populate_by_name=True
    )  # Switch alias and field name

    resource_type: Optional[str] = Field("Users", alias="resourceType")
    username: str = Field()
    full_name: Optional[str] = Field()
    email: str = Field()
    designation: str = Field()
    role: str = Field()


class Users(UsersBase):
    """Base class to handle http request

    Args:
        UsersBase: Inherits from the UsersBase
    """

    id: int = Field()
    created_by: Optional[str] = Field(alias="createdBy")
    updated_by: Optional[str] = Field(alias="updatedBy")
    create_dt: Optional[datetime] = Field(alias="createDate")
    update_dt: Optional[datetime] = Field(alias="updateDate")


class UserCredential(UsersBase):
    password: str = Field()


class UserLogin(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )
    username: str = Field()
    password: str = Field()

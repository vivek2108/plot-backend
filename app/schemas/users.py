"""Schema for users."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UsersBase(BaseModel):
    """
    Base class to handle HTTP requests for the 'users' resource.

    Attributes:
        resource_type (Optional[str]): The type of the resource, defaulting to 'Users'.
        username (str): The unique username of the user (required).
        full_name (Optional[str]): The full name of the user (optional).
        email (str): The email address of the user (required).
        designation (str): The designation or job title of the user (required).
        role (str): The role of the user, e.g., 'Admin', 'User' (required).

    Configuration:
        - Switches alias and field name with
        `populate_by_name=True, from_attributes=True`.
    """

    model_config = ConfigDict(
        populate_by_name=True, from_attributes=True
    )  # Switch alias and field name

    resource_type: Optional[str] = Field(
        "Users", alias="resourceType", description="Type of the resource."
    )
    username: str = Field(..., description="The unique username of the user.")
    full_name: Optional[str] = Field(None, description="The full name of the user.")
    email: str = Field(..., description="The unique email address of the user.")
    designation: str = Field(..., description="The designation/job title of the user.")
    role: str = Field(..., description="The role of the user (e.g., 'Admin', 'User').")


class Users(UsersBase):
    """
    Full class to represent a user in the system, inheriting from `UsersBase`.

    This schema includes additional fields for metadata and timestamps.

    Attributes:
        id (int): The unique identifier for the user.
        created_by (Optional[str]): The username of the user who created this
        record (optional).
        updated_by (Optional[str]): The username of the user who last updated
        this record (optional).
        create_dt (Optional[datetime]): Timestamp when the user was created.
        update_dt (Optional[datetime]): Timestamp when the user's record was
        last updated.

    Args:
        UsersBase: Inherits common fields from the `UsersBase` schema.
    """

    id: int = Field(..., description="Unique identifier for the user.")
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


class UserCredential(UsersBase):
    """
    Schema for handling user credentials, including password.

    This schema is used during user registration or password update.

    Attributes:
        password (str): The password for the user (required).
    """

    password: str = Field(..., description="The password for the user.")


class UserLogin(BaseModel):
    """
    Schema for handling user login.

    Attributes:
        username (str): The username of the user (required).
        password (str): The password of the user (required).

    Configuration:
        - Switches alias and field name with `populate_by_name=True`.
    """

    model_config = ConfigDict(populate_by_name=True)

    username: str = Field(..., description="The username of the user.")
    password: str = Field(..., description="The password of the user.")

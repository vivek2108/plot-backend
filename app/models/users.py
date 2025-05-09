from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Roles(Base):
    """
    Represents a role in the system, such as 'Admin', 'User', etc.

    Attributes:
        id (int): Primary key for the role record.
        name (str): Name of the role (e.g., 'Admin', 'User').

    Relationships:
        users (List[Users]): List of users associated with this role.
    """

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)

    # Relationship with Users
    users = relationship("Users", back_populates="role")


class Designations(Base):
    """
    Represents a designation in the system, such as 'Manager', 'Developer', etc.

    Attributes:
        id (int): Primary key for the designation record.
        title (str): Title of the designation (e.g., 'Manager', 'Developer').

    Relationships:
        users (List[Users]): List of users associated with this designation.
    """

    __tablename__ = "designations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String)

    # Relationship with Users
    users = relationship("Users", back_populates="designation")


class Users(Base):
    """
    Represents a user in the system, including their credentials and roles.

    Attributes:
        id (int): Primary key for the user record.
        username (str): Unique username for the user.
        full_name (str | None): Full name of the user.
        email (str): Unique email address for the user.
        hashed_password (str): The hashed password of the user.
        designation_id (int): Foreign key to the 'designations' table.
        role_id (int): Foreign key to the 'roles' table.
        create_dt (datetime): Timestamp when the record was created.
        update_dt (datetime): Timestamp when the record was last updated.
        created_by (str | None): Username of the user who created the record.
        updated_by (str | None): Username of the user who last updated the record.

    Relationships:
        role (Roles): The role assigned to the user.
        designation (Designations): The designation assigned to the user.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    designation_id: Mapped[int] = mapped_column(Integer, ForeignKey("designations.id"))
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"))
    create_dt: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    update_dt: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )
    created_by: Mapped[str | None] = mapped_column(String, nullable=True)
    updated_by: Mapped[str | None] = mapped_column(String, nullable=True)

    # Relationships
    role = relationship("Roles", back_populates="users")
    designation = relationship("Designations", back_populates="users")

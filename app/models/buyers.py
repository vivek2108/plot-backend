from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Buyers(Base):
    """
    Represents a buyer in the system.

    Attributes:
        id (int): Primary key for the buyer.
        name (str | None): Name of the buyer.
        contact (str | None): Contact information.
        address (str | None): Address of the buyer.
        id_proof_path (str | None): File path to the buyer's ID proof.
        deleted_at (datetime | None): Timestamp for soft deletion.
        create_dt (datetime): Timestamp when the record was created.
        update_dt (datetime): Timestamp when the record was last updated.
        created_by (str | None): Username who created the record.
        updated_by (str | None): Username who last updated the record.
    """

    __tablename__ = "buyers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    contact: Mapped[str | None] = mapped_column(String, nullable=True)
    address: Mapped[str | None] = mapped_column(String, nullable=True)
    id_proof_path: Mapped[str | None] = mapped_column(String, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)  # Soft delete flag
    create_dt: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    update_dt: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    created_by: Mapped[str | None] = mapped_column(String, nullable=True)
    updated_by: Mapped[str | None] = mapped_column(String, nullable=True)

    sales = relationship("Sales", back_populates="buyer")

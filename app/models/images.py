from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base


class Images(Base):
    """
    Represents image records related to plots, including metadata and optional highlight coordinates.

    Attributes:
        id (int): Primary key of the image record.
        plot_id (int): Foreign key or reference ID to the associated plot.
        image_type (str | None): Type/category of the image.
        image_path (str | None): Filesystem or URL path to the image.
        highlight_coordinates (dict | None): Optional JSONB field for storing polygon or area highlights.
        create_dt (datetime): Timestamp when the record was created.
        update_dt (datetime): Timestamp when the record was last updated.
        created_by (str | None): User who created the record.
        updated_by (str | None): User who last updated the record.
    """
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    plot_id: Mapped[int] = mapped_column()
    image_type: Mapped[str | None] = mapped_column(String, nullable=True)
    image_path: Mapped[str | None] = mapped_column(String, nullable=True)
    highlight_coordinates: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    create_dt: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    update_dt: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    created_by: Mapped[str | None] = mapped_column(String, nullable=True)
    updated_by: Mapped[str | None] = mapped_column(String, nullable=True)

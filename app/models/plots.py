from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base
from app.models.areas import Areas
from app.models.images import Images


class Plots(Base):
    """
    Represents a plot of land, including its details and associated metadata.

    Attributes:
        id (int): Primary key of the plot record.
        plot_number (int): Unique plot number identifier.
        area_id (int): Identifier for the area the plot belongs to.
        dimensions (str | None): Dimensions of the plot (e.g., "10x20 meters").
        status (str | None): Status of the plot (e.g., "available", "sold").
        assigned_to (str | None): The person or entity to whom the plot is assigned.
        image_id (int | None): Identifier for the associated image record.
        svg_path_id (str | None): Path to the associated SVG file.
        ocr_data (dict | None): OCR data extracted from an image (JSON).
        create_dt (datetime): Timestamp when the plot record was created.
        update_dt (datetime): Timestamp when the plot record was last updated.
        created_by (str | None): User who created the plot record.
        updated_by (str | None): User who last updated the plot record.
    """

    __tablename__ = "plots"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    # plot_number: Mapped[int] = mapped_column()
    area_id: Mapped[int] = mapped_column(Integer, ForeignKey("areas.id"))
    dimensions: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str | None] = mapped_column(String, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(15, 4))
    assigned_to: Mapped[str | None] = mapped_column(String, nullable=True)
    image_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("images.id"))
    svg_path_id: Mapped[str | None] = mapped_column(String, nullable=True)
    ocr_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    create_dt: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    update_dt: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    created_by: Mapped[str | None] = mapped_column(String, nullable=True)
    updated_by: Mapped[str | None] = mapped_column(String, nullable=True)

    area = relationship("Areas", back_populates="plots")
    sales = relationship("Sales", back_populates="plot")
    images = relationship("Images", back_populates="plots")

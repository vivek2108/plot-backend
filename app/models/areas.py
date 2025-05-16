from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Areas(Base):
    """
    Represents a geographic area within a city and state.

    Attributes:
        id (int): Primary key, auto-incremented.
        name (str | None): Name of the area (nullable).
        city (str | None): City in which the area is located (nullable).
        state (str | None): State in which the area is located (nullable).
    """

    __tablename__ = "areas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column(String, nullable=True)
    city: Mapped[str | None] = mapped_column(String, nullable=True)
    state: Mapped[str | None] = mapped_column(String, nullable=True)

    plots = relationship("Plots", back_populates="area")

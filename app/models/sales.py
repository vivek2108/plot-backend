from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (Date, DateTime, ForeignKey, Integer, Numeric, String,
                        func)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.database import Base


class Sales(Base):
    """
    Represents a sale of a plot, including sale details, associated buyer, associate, and payment information.

    Attributes:
        id (int): Primary key for the sale record.
        plot_id (int): The ID of the plot being sold.
        associate_id (int): The ID of the associate handling the sale.
        buyer_id (int): The ID of the buyer purchasing the plot.
        sale_amount (Decimal): The total sale amount for the plot.
        payment_mode (str | None): The method of payment (e.g., 'Cash', 'Bank Transfer').
        payment_timeframe (datetime): The expected payment timeframe for the sale.
        sale_date (date): The date the sale was made.
        create_dt (datetime): Timestamp when the record was created.
        update_dt (datetime): Timestamp when the record was last updated.
        created_by (str | None): The user who created the sale record.
        updated_by (str | None): The user who last updated the sale record.
    """

    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    plot_id: Mapped[int] = mapped_column(Integer, ForeignKey("plots.id"))
    associate_id: Mapped[int] = mapped_column(Integer, ForeignKey("associates.id"))
    buyer_id: Mapped[int] = mapped_column(Integer, ForeignKey("buyers.id"))
    sale_amount: Mapped[Decimal] = mapped_column(Numeric(15, 2))
    payment_mode: Mapped[str | None] = mapped_column(String, nullable=True)
    payment_timeframe: Mapped[datetime] = mapped_column(DateTime)
    sale_date: Mapped[date] = mapped_column(Date)
    create_dt: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    update_dt: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )
    created_by: Mapped[str | None] = mapped_column(String, nullable=True)
    updated_by: Mapped[str | None] = mapped_column(String, nullable=True)

    # Relationships
    plot = relationship("Plots", back_populates="sales", cascade="all, delete-orphan")
    associate = relationship("Associates", back_populates="sales")
    buyer = relationship("Buyers", back_populates="sales")

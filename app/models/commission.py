from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base


class Commission(Base):
    """
    Represents a commission record earned by an associate for a sale.

    Attributes:
        id (int): Primary key for the commission record.
        associate_id (int): Identifier of the associate who earned the commission.
        sale_id (int): Identifier of the sale for which the commission was earned.
        commission_percentage (Decimal): Commission rate as a percentage (e.g., 5.2500).
        commission_amount (Decimal): Calculated commission amount.
        calculated_on (date): Date when the commission was calculated.
    """
    __tablename__ = "commission"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    associate_id: Mapped[int] = mapped_column()
    sale_id: Mapped[int] = mapped_column()
    commission_percentage: Mapped[Decimal] = mapped_column(Numeric(8, 4))
    commission_amount: Mapped[Decimal] = mapped_column(Numeric(15, 4))
    calculated_on: Mapped[date] = mapped_column(Date)

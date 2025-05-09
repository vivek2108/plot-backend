from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.config.database import Base


class Payments(Base):
    """
    Represents a payment made toward a sale.

    Attributes:
        id (int): Primary key for the payment record.
        sale_id (int): Identifier of the related sale.
        amount_paid (Decimal): Amount of money paid.
        payment_date (date): Date when the payment was made.
        payment_mode (str | None): Method of payment (e.g., 'Cash', 'Bank Transfer').
        remaining_balance (Decimal): Remaining balance after this payment.
    """

    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sale_id: Mapped[int] = mapped_column()
    amount_paid: Mapped[Decimal] = mapped_column(Numeric(15, 4))
    payment_date: Mapped[date] = mapped_column(Date)
    payment_mode: Mapped[str | None] = mapped_column(String, nullable=True)
    remaining_balance: Mapped[Decimal] = mapped_column(Numeric(15, 4))

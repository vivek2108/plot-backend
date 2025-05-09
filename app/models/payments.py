from sqlalchemy import Column, Date, Integer, Numeric, String

from app.config.database import Base


class Payments(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer)
    amount_paid = Column(Numeric(15, 4))
    payment_date = Column(Date)
    payment_mode = Column(String, nullable=True)
    remaining_balance = Column(Numeric(15, 4))

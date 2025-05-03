from sqlalchemy import Column, Integer, String, Boolean, Numeric
from sqlalchemy import Date
from app.config.database import Base
from datetime import datetime

class Payments(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer)
    amount_paid = Column(Numeric(15,4))
    payment_date = Column(Date)
    payment_mode = Column(String, nullable=True)
    remaining_balance = Column(Numeric(15,4))

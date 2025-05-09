from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Integer, Numeric, String

from app.config.database import Base


class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    plot_id = Column(Integer)
    associate_id = Column(Integer)
    buyer_id = Column(Integer)
    sale_amount = Column(Numeric(15, 2))
    payment_mode = Column(String, nullable=True)
    payment_timeframe = Column(DateTime)
    sale_date = Column(Date)
    create_dt = Column(DateTime, default=datetime.now())
    update_dt = Column(DateTime, default=datetime.now())
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)

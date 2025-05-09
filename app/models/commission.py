from sqlalchemy import Column, Date, Integer, Numeric

from app.config.database import Base


class Commission(Base):
    __tablename__ = "commission"

    id = Column(Integer, primary_key=True, index=True)
    associate_id = Column(Integer)
    sale_id = Column(Integer)
    commission_percentage = Column(Numeric(8, 4))
    commission_amount = Column(Numeric(15, 4))
    calculated_on = Column(Date)

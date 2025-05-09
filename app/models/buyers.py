from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.config.database import Base


class Buyers(Base):
    __tablename__ = "buyers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    contact = Column(String, nullable=True)
    address = Column(String, nullable=True)
    id_proof_path = Column(String, nullable=True)
    create_dt = Column(DateTime, default=datetime.now())
    update_dt = Column(DateTime, default=datetime.now())
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)

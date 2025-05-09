from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from app.config.database import Base


class Plots(Base):
    __tablename__ = "plots"

    id = Column(Integer, primary_key=True, index=True)
    plot_number = Column(Integer)
    area_id = Column(Integer)
    dimensions = Column(String, nullable=True)
    status = Column(String, nullable=True)
    assigned_to = Column(String, nullable=True)
    image_id = Column(Integer)
    svg_path_id = Column(String, nullable=True)
    ocr_data = Column(JSONB, nullable=True)
    create_dt = Column(DateTime, default=datetime.now())
    update_dt = Column(DateTime, default=datetime.now())
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)

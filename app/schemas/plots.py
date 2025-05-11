from datetime import datetime
from typing import Optional, Dict

from pydantic import BaseModel, ConfigDict, Field
import logging

# Initialize logger
logger = logging.getLogger(__name__)


class PlotBase(BaseModel):
    """
    Base schema for creating or updating a plot.

    Attributes:
        plot_number (int): Unique plot number.
        area_id (int): ID of the area the plot belongs to.
        dimensions (Optional[str]): Plot dimensions (e.g., "10x20").
        status (Optional[str]): Plot status ("available", "sold", etc.).
        assigned_to (Optional[str]): Name or ID of the assignee.
        image_id (Optional[int]): Foreign key to associated image.
        svg_path_id (Optional[str]): Path to SVG file for plot layout.
        ocr_data (Optional[Dict]): OCR data extracted from image.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

    plot_number: int = Field(..., description="Unique number identifying the plot")
    area_id: int = Field(..., description="ID of the area the plot is located in")
    dimensions: Optional[str] = Field(None, description="Dimensions of the plot")
    status: Optional[str] = Field(None, description="Status of the plot")
    assigned_to: Optional[str] = Field(None, description="Assigned person or entity")
    image_id: Optional[int] = Field(None, description="Associated image ID")
    svg_path_id: Optional[str] = Field(None, description="Path to the SVG representation")
    ocr_data: Optional[Dict] = Field(None, description="OCR data in JSON format")


class PlotCreate(PlotBase):
    """
    Schema for creating a new plot.

    Inherits all fields from PlotBase.
    """
    pass


class PlotUpdate(BaseModel):
    """
    Schema for updating an existing plot.

    """
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
    
    dimensions: Optional[str] = Field(None, description="Dimensions of the plot")
    status: Optional[str] = Field(None, description="Status of the plot")
    assigned_to: Optional[str] = Field(None, description="Assigned person or entity")
    image_id: Optional[int] = Field(None, description="Associated image ID")
    svg_path_id: Optional[str] = Field(None, description="Path to the SVG representation")
    ocr_data: Optional[Dict] = Field(None, description="OCR data in JSON format")


class Plot(PlotBase):
    """
    Schema for reading plot details.

    Attributes:
        id (int): Unique identifier of the plot.
        create_dt (datetime): Timestamp of plot creation.
        update_dt (datetime): Timestamp of the last update.
        created_by (Optional[str]): User who created the record.
        updated_by (Optional[str]): User who last updated the record.
    """
    id: int = Field(..., description="Unique plot ID")
    create_dt: datetime = Field(..., alias="createDate", description="Creation timestamp")
    update_dt: datetime = Field(..., alias="updateDate", description="Last update timestamp")
    created_by: Optional[str] = Field(None, alias="createdBy", description="Creator of the plot")
    updated_by: Optional[str] = Field(None, alias="updatedBy", description="Last user to update the plot")

    class Config:
        orm_mode = True
        populate_by_name = True
        from_attributes = True

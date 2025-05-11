from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List

from app.models.plots import Plots
from app.schemas.plots import PlotCreate, PlotUpdate
from app.core.logger import get_logger

logger = get_logger(__name__)


def create_plot(db: Session, plot_data: PlotCreate, user: str) -> Plots:
    """
    Create a new plot record in the database.

    Args:
        db (Session): SQLAlchemy database session.
        plot_data (PlotCreate): Plot data from request.
        user (str): Username of the creator.

    Returns:
        Plots: The created plot record.
    """
    try:
        new_plot = plot_data.dict(exclude={"resource_type"})
        new_plot["created_by"] = user
        new_plot["updated_by"] = user

        db.add(new_plot)
        db.commit()
        db.refresh(new_plot)
        logger.info(f"Plot created successfully by {user}: ID {new_plot.id}")
        return new_plot
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating plot: {e}")
        raise


def get_plot(db: Session, plot_id: int) -> Optional[Plots]:
    """
    Retrieve a plot by its ID.

    Args:
        db (Session): SQLAlchemy session.
        plot_id (int): ID of the plot.

    Returns:
        Optional[Plots]: Plot instance if found, else None.
    """
    logger.debug(f"Fetching plot with ID: {plot_id}")
    return db.query(Plots).filter(Plots.id == plot_id).first()


def get_all_plots(db: Session, skip: int = 0, limit: int = 10) -> List[Plots]:
    """
    Retrieve all plots with pagination.

    Args:
        db (Session): SQLAlchemy session.
        skip (int): Number of records to skip.
        limit (int): Max number of records to return.

    Returns:
        List[Plots]: List of plot records.
    """
    logger.debug(f"Fetching plots: skip={skip}, limit={limit}")
    return db.query(Plots).offset(skip).limit(limit).all()


def update_plot(db: Session, plot_id: int, plot_data: PlotUpdate, user: str) -> Optional[Plots]:
    """
    Update an existing plot record.

    Args:
        db (Session): SQLAlchemy session.
        plot_id (int): ID of the plot to update.
        plot_data (PlotUpdate): Data to update.
        user (str): Username performing the update.

    Returns:
        Optional[Plots]: Updated plot if found and updated, else None.
    """
    plot = db.query(Plots).filter(Plots.id == plot_id).first()
    if not plot:
        logger.warning(f"Plot ID {plot_id} not found for update by {user}")
        return None

    logger.debug(f"Updating plot ID {plot_id} by {user}")
    update_data = {
        key: value
        for key, value in plot_data.dict(exclude_unset=True).items()
        if value not in (None, "")
    }

    for field, value in update_data.items():
        setattr(plot, field, value)

    plot.updated_by = user
    db.commit()
    db.refresh(plot)
    logger.info(f"Plot ID {plot_id} updated successfully by {user}")
    return plot


def delete_plot(db: Session, plot_id: int, user: str) -> bool:
    """
    Delete a plot record from the database.

    Args:
        db (Session): SQLAlchemy session.
        plot_id (int): ID of the plot to delete.
        user (str): Username performing the deletion.

    Returns:
        bool: True if deleted, False if not found.
    """
    plot = db.query(Plots).filter(Plots.id == plot_id).first()
    if plot:
        db.delete(plot)
        db.commit()
        logger.info(f"Plot ID {plot_id} deleted by {user}")
        return True

    logger.warning(f"Plot ID {plot_id} not found for deletion by {user}")
    return False

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.auth.auth import get_current_user
from app.schemas.plots import PlotCreate, PlotUpdate, Plot
from app.crud.plots import create_plot, get_plot, get_all_plots, update_plot, delete_plot
from app.auth.currentuser import CurrentUser

router = APIRouter()


@router.post("/", response_model=Plot, status_code=status.HTTP_201_CREATED)
def create(
    plot_data: PlotCreate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Create a new plot.
    Accessible by authorized users (admin, manager).

    Args:
        plot_data (PlotCreate): Data for the new plot.
        db (Session): Database session.
        current_user (CurrentUser): Authenticated user.

    Returns:
        Plot: Created plot details.
    """
    plot = create_plot(db, plot_data, current_user.username)
    return plot


@router.get("/{plot_id}", response_model=Plot)
def get(
    plot_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Retrieve details of a specific plot by ID.
    Accessible by any authenticated user.

    Args:
        plot_id (int): The ID of the plot.
        db (Session): Database session.
        current_user (CurrentUser): Authenticated user.

    Returns:
        Plot: Plot details.
    """
    plot = get_plot(db, plot_id)
    if not plot:
        raise HTTPException(status_code=404, detail="Plot not found")
    return plot


@router.get("/", response_model=List[Plot])
def get_all(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Get a list of all plots with pagination.
    Accessible by any authenticated user.

    Args:
        skip (int): The number of records to skip.
        limit (int): The maximum number of records to return.
        db (Session): Database session.
        current_user (CurrentUser): Authenticated user.

    Returns:
        List[Plot]: List of plot records.
    """
    return get_all_plots(db, skip=skip, limit=limit)


@router.put("/{plot_id}", response_model=Plot)
def update(
    plot_id: int,
    plot_data: PlotUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Update an existing plot.
    Accessible by authorized users (admin, manager).

    Args:
        plot_id (int): The ID of the plot to update.
        plot_data (PlotUpdate): Updated plot data.
        db (Session): Database session.
        current_user (CurrentUser): Authenticated user.

    Returns:
        Plot: Updated plot details.
    """
    plot = update_plot(db, plot_id, plot_data, current_user.username)
    if not plot:
        raise HTTPException(status_code=404, detail="Plot not found")
    return plot


@router.delete("/{plot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    plot_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    Soft delete a plot by ID.
    Accessible by authorized users (admin, manager).

    Args:
        plot_id (int): The ID of the plot to delete.
        db (Session): Database session.
        current_user (CurrentUser): Authenticated user.

    Returns:
        None
    """
    deleted = delete_plot(db, plot_id, current_user.username)
    if not deleted:
        raise HTTPException(status_code=404, detail="Plot not found")
    return {"detail": "Plot successfully deleted"}

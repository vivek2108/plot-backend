from typing import Dict

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.core.logger import get_logger
from app.crud.dashboard import total_sales_amount, total_plots_sold, remaining_inventory, monthly_sales_trend, pending_payments, sales_by_agent, revenue_by_location

logger = get_logger(__name__)
router = APIRouter()


@router.get(
    "/total-sales",
    summary="Get Total Sales Amount",
    response_model=Dict[str, float],
)
def get_total_sales(db: Session = Depends(get_db)):
    """
    Retrieves the total sales amount from all transactions.
    """
    return {"total_sales_amount": total_sales_amount(db)}


@router.get(
    "/plots-sold",
    summary="Get Total Plots Sold",
    response_model=Dict[str, int],
)
def get_plots_sold(db: Session = Depends(get_db)):
    """
    Retrieves the number of plots that have been sold.
    """
    return {"total_plots_sold": total_plots_sold(db)}


@router.get(
    "/remaining-inventory",
    summary="Get Remaining Inventory",
    response_model=Dict[str, int],
)
def get_inventory(db: Session = Depends(get_db)):
    """
    Retrieves the number of plots remaining in inventory.
    """
    return {"remaining_inventory": remaining_inventory(db)}


@router.get(
    "/monthly-trend",
    summary="Get Monthly Sales Trend",
    response_model=Dict[str, list],
)
def get_sales_trend(db: Session = Depends(get_db)):
    """
    Retrieves the monthly trend of sales for analytics.
    """
    return {"monthly_sales": monthly_sales_trend(db)}


@router.get(
    "/pending-payments",
    summary="Get Pending Payments",
    response_model=Dict[str, float],
)
def get_pending_payments(db: Session = Depends(get_db)):
    """
    Retrieves the total amount of payments that are pending.
    """
    return {"pending_payments": pending_payments(db)}


@router.get(
    "/sales-by-agent",
    summary="Get Sales by Agent",
    response_model=Dict[str, dict],
)
def get_sales_by_agent(db: Session = Depends(get_db)):
    """
    Retrieves the sales performance of each sales agent.
    """
    return {"sales_by_agent": sales_by_agent(db)}


@router.get(
    "/revenue-by-location",
    summary="Get Revenue by Location",
    response_model=Dict[str, dict],
)
def get_revenue_by_location(db: Session = Depends(get_db)):
    """
    Retrieves the revenue generated categorized by location.
    """
    return {"revenue_by_location": revenue_by_location(db)}

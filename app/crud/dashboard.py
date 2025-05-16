from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import sales, plots, payments, users


def total_sales_amount(db: Session) -> float:
    """
    Calculate the total sales amount from all sale records.

    Returns:
        float: The sum of all sale_amount values, or 0 if none exist.
    """
    return db.query(func.sum(sales.Sales.sale_amount)).scalar() or 0.0


def total_plots_sold(db: Session) -> int:
    """
    Count the total number of distinct plots that have been sold.

    Returns:
        int: Number of unique sold plot IDs.
    """
    return db.query(sales.Sales.plot_id).distinct().count()


def remaining_inventory(db: Session) -> int:
    """
    Count the number of plots available in inventory (not archived or sold).

    Returns:
        int: Number of plots with 'available' status and not archived.
    """
    return (
        db.query(plots.Plots)
        .filter(plots.Plots.status == "available", plots.Plots.archived.is_(False))
        .count()
    )


def monthly_sales_trend(db: Session):
    """
    Retrieve monthly aggregated sales amounts.

    Returns:
        List[Tuple[datetime, float]]: A list of (month, total_sales) tuples.
    """
    return (
        db.query(
            func.date_trunc("month", sales.Sales.sale_date).label("month"),
            func.sum(sales.Sales.sale_amount).label("total_sales"),
        )
        .group_by("month")
        .order_by("month")
        .all()
    )


def pending_payments(db: Session) -> float:
    """
    Calculate the total pending payment amount.

    Returns:
        float: Sum of remaining balances from non-deleted payments.
    """
    return (
        db.query(func.sum(payments.Payments.remaining_balance))
        .filter(payments.Payments.is_deleted.is_(False))
        .scalar()
        or 0.0
    )


def sales_by_agent(db: Session):
    """
    Aggregate total sales per sales associate.

    Returns:
        List[Tuple[str, float]]: A list of (agent_name, total_sales) tuples.
    """
    return (
        db.query(
            users.Users.name.label("agent"),
            func.sum(sales.Sales.sale_amount).label("total_sales"),
        )
        .join(sales.Sales.associate)
        .group_by(users.name)
        .order_by(func.sum(sales.Sales.sale_amount).desc())
        .all()
    )


def revenue_by_location(db: Session):
    """
    Aggregate total revenue by plot location.

    Returns:
        List[Tuple[str, float]]: A list of (location, total_sales) tuples.
    """
    return (
        db.query(
            plots.Plots.location.label("location"),
            func.sum(sales.Sales.sale_amount).label("total_revenue"),
        )
        .join(sales.Sales.plot)
        .group_by(plots.Plots.location)
        .order_by(func.sum(sales.Sales.sale_amount).desc())
        .all()
    )

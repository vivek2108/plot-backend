from sqlalchemy import func
from sqlalchemy.orm import Session

from ..api import models


def total_sales_amount(db: Session):
    return db.query(func.sum(models.Sale.sale_amount)).scalar()


def total_plots_sold(db: Session):
    return db.query(models.Sale.plot_id).distinct().count()


def remaining_inventory(db: Session):
    return (
        db.query(models.Plot)
        .filter(models.Plot.status == "available", models.Plot.archived == False)
        .count()
    )


def monthly_sales_trend(db: Session):
    return (
        db.query(
            func.date_trunc("month", models.Sale.sale_date).label("month"),
            func.sum(models.Sale.sale_amount),
        )
        .group_by("month")
        .order_by("month")
        .all()
    )


def pending_payments(db: Session):
    return (
        db.query(func.sum(models.Payment.remaining_balance))
        .filter(models.Payment.is_deleted == False)
        .scalar()
    )


def sales_by_agent(db: Session):
    return (
        db.query(models.Associate.name, func.sum(models.Sale.sale_amount))
        .join(models.Sale.associate)
        .group_by(models.Associate.name)
        .all()
    )


def revenue_by_location(db: Session):
    return (
        db.query(models.Plot.location, func.sum(models.Sale.sale_amount))
        .join(models.Sale.plot)
        .group_by(models.Plot.location)
        .all()
    )

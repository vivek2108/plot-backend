from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud
from .database import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/dashboard/total-sales")
def get_total_sales(db: Session = Depends(get_db)):
    return {"total_sales_amount": crud.total_sales_amount(db)}


@app.get("/dashboard/plots-sold")
def get_plots_sold(db: Session = Depends(get_db)):
    return {"total_plots_sold": crud.total_plots_sold(db)}


@app.get("/dashboard/remaining-inventory")
def get_inventory(db: Session = Depends(get_db)):
    return {"remaining_inventory": crud.remaining_inventory(db)}


@app.get("/dashboard/monthly-trend")
def get_sales_trend(db: Session = Depends(get_db)):
    return {"monthly_sales": crud.monthly_sales_trend(db)}


@app.get("/dashboard/pending-payments")
def get_pending_payments(db: Session = Depends(get_db)):
    return {"pending_payments": crud.pending_payments(db)}


@app.get("/dashboard/sales-by-agent")
def get_sales_by_agent(db: Session = Depends(get_db)):
    return {"sales_by_agent": crud.sales_by_agent(db)}


@app.get("/dashboard/revenue-by-location")
def get_revenue_by_location(db: Session = Depends(get_db)):
    return {"revenue_by_location": crud.revenue_by_location(db)}

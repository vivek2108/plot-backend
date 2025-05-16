from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth import get_current_user, require_role
from app.auth.currentuser import CurrentUser
from app.config.database import get_db
from app.core.logger import get_logger
from app.crud.sales import (create_sale, get_all_sales, get_sale,
                            update_sale)
from app.schemas.sales import Sales, SalesBase, SaleUpdate

logger = get_logger(__name__)

router = APIRouter()


@router.get("/", response_model=List[Sales])
def read_sales(db: Session = Depends(get_db), skip: int = 0, limit: int = 100,
    # filters: dict = {}, 
    current_user: CurrentUser = Depends(require_role(["admin", "manager"]))):
    return get_all_sales(db, skip=skip, limit=limit)


@router.get("/{sale_id}", response_model=Sales)
def read_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = get_sale(db, sale_id)
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale


@router.post("/", response_model=Sales)
def create(sale: SalesBase, db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)):
    return create_sale(db, sale, current_user)


@router.put("/{sale_id}", response_model=Sales)
def update(sale_id: int, sale: SaleUpdate, db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)):
    db_sale = update_sale(db, sale_id, sale, current_user)
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale


# @router.delete("/{sale_id}", response_model=Sales)
# def delete(sale_id: int, db: Session = Depends(get_db), 
#     current_user: CurrentUser = Depends(get_current_user),):
#     db_sale = delete_sale(db, sale_id)
#     if not db_sale:
#         raise HTTPException(status_code=404, detail="Sale not found")
#     return db_sale

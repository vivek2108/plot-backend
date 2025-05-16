from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.auth import get_current_user, require_role
from app.auth.currentuser import CurrentUser
from app.config.database import get_db
from app.core.logger import get_logger
from app.crud.sales import create_sale, get_all_sales, get_sale, update_sale
from app.schemas.sales import Sales, SalesBase, SaleUpdate

logger = get_logger(__name__)
router = APIRouter(prefix="/sales", tags=["Sales"])


@router.get("/", response_model=List[Sales], summary="List Sales")
def list_sales(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(require_role(["admin", "manager"])),
):
    """
    Retrieve a paginated list of all sales records.

    - Requires `admin` or `manager` role.
    - Supports pagination via `skip` and `limit`.
    """
    sales = get_all_sales(db, skip=skip, limit=limit)
    logger.info(f"User {current_user.email} retrieved {len(sales)} sales.")
    return sales


@router.get("/{sale_id}", response_model=Sales, summary="Get Sale by ID")
def get_sale_by_id(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    """
    Retrieve details of a specific sale by ID.

    - Requires any authenticated user.
    - Returns 404 if sale is not found.
    """
    sale = get_sale(db, sale_id)
    if not sale:
        logger.warning(f"Sale ID {sale_id} not found by user {current_user.email}")
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale


@router.post(
    "/",
    response_model=Sales,
    status_code=status.HTTP_201_CREATED,
    summary="Create a New Sale",
)
def create_new_sale(
    sale: SalesBase,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    """
    Create a new sale record.

    - Requires any authenticated user.
    """
    new_sale = create_sale(db, sale, current_user)
    logger.info(f"Sale created by user {current_user.email}")
    return new_sale


@router.put("/{sale_id}", response_model=Sales, summary="Update a Sale")
def update_existing_sale(
    sale_id: int,
    sale: SaleUpdate,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    """
    Update an existing sale by ID.

    - Requires any authenticated user.
    - Returns 404 if the sale does not exist.
    """
    updated_sale = update_sale(db, sale_id, sale, current_user)
    if not updated_sale:
        logger.warning(f"Attempted to update non-existent sale ID {sale_id}")
        raise HTTPException(status_code=404, detail="Sale not found")
    logger.info(f"Sale ID {sale_id} updated by user {current_user.email}")
    return updated_sale


# @router.delete("/{sale_id}", response_model=Sales)
# def delete(sale_id: int, db: Session = Depends(get_db),
#     current_user: CurrentUser = Depends(get_current_user),):
#     db_sale = delete_sale(db, sale_id)
#     if not db_sale:
#         raise HTTPException(status_code=404, detail="Sale not found")
#     return db_sale

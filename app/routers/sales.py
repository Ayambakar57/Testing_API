from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..dependencies import get_current_active_user
from .. import crud, schemas, models
import math

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/", response_model=schemas.HeadPenjualan)
def create_sales_transaction(
    sales_data: schemas.HeadPenjualanCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    try:
        return crud.create_sales_transaction(db=db, sales_data=sales_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=schemas.PaginatedResponse)
def read_sales_transactions(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    skip = (page - 1) * size
    result = crud.get_sales_transactions(db, skip=skip, limit=size, search=search)
    
    return {
        "data": result["data"],
        "total": result["total"],
        "page": page,
        "size": size,
        "total_pages": math.ceil(result["total"] / size)
    }

@router.get("/{transaction_id}", response_model=schemas.HeadPenjualan)
def read_sales_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_transaction = crud.get_sales_transaction(db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction
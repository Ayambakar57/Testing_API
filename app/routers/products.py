from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from ..database import get_db
from ..dependencies import get_current_active_user
from .. import crud, schemas, models
import math

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return crud.create_product(db=db, product=product)

@router.get("/", response_model=schemas.PaginatedResponse)
def read_products(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    skip = (page - 1) * size
    result = crud.get_products(db, skip=skip, limit=size, search=search)
    
    return {
        "data": result["data"],
        "total": result["total"],
        "page": page,
        "size": size,
        "total_pages": math.ceil(result["total"] / size)
    }

@router.get("/{product_id}", response_model=schemas.Product)
def read_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    product_update: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_product = crud.update_product(db, product_id=product_id, product_update=product_update)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_product = crud.delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
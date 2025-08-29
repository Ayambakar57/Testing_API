from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional, List
from . import models, schemas, auth
from datetime import datetime
import math

# User CRUD
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 10, search: Optional[str] = None):
    query = db.query(models.User)
    if search:
        query = query.filter(
            or_(
                models.User.username.ilike(f"%{search}%"),
                models.User.email.ilike(f"%{search}%")
            )
        )
    total = query.count()
    users = query.offset(skip).limit(limit).all()
    return {"data": users, "total": total}

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# Product CRUD
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10, search: Optional[str] = None):
    query = db.query(models.Product)
    if search:
        query = query.filter(
            or_(
                models.Product.sku.ilike(f"%{search}%"),
                models.Product.nama_produk.ilike(f"%{search}%")
            )
        )
    total = query.count()
    products = query.offset(skip).limit(limit).all()
    return {"data": products, "total": total}

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: schemas.ProductUpdate):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        for key, value in product_update.dict(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

# Sales CRUD
def generate_sales_number():
    """Generate unique sales number"""
    now = datetime.now()
    return f"TRX{now.strftime('%Y%m%d%H%M%S')}"

def create_sales_transaction(db: Session, sales_data: schemas.HeadPenjualanCreate):
    # Generate sales number
    nomor_penjualan = generate_sales_number()
    
    # Create head transaction
    total_amount = sum(detail.nominal for detail in sales_data.details)
    db_head = models.HeadPenjualan(
        nomor_penjualan=nomor_penjualan,
        total_amount=total_amount,
        status="pending"
    )
    db.add(db_head)
    db.flush()  # To get the ID without committing
    
    # Create details and update stock
    for detail in sales_data.details:
        # Check product stock
        product = db.query(models.Product).filter(models.Product.id == detail.produk_id).first()
        if not product:
            raise ValueError(f"Product with ID {detail.produk_id} not found")
        
        if product.stok < detail.jml:
            raise ValueError(f"Insufficient stock for product {product.nama_produk}")
        
        # Create detail
        db_detail = models.DetailPenjualan(
            nomor_penjualan=nomor_penjualan,
            produk_id=detail.produk_id,
            jml=detail.jml,
            nominal=detail.nominal
        )
        db.add(db_detail)
        
        # Update product stock
        product.stok -= detail.jml
    
    # Complete transaction
    db_head.status = "completed"
    db.commit()
    db.refresh(db_head)
    return db_head

def get_sales_transactions(db: Session, skip: int = 0, limit: int = 10, search: Optional[str] = None):
    query = db.query(models.HeadPenjualan)
    if search:
        query = query.filter(models.HeadPenjualan.nomor_penjualan.ilike(f"%{search}%"))
    
    total = query.count()
    transactions = query.offset(skip).limit(limit).all()
    return {"data": transactions, "total": total}

def get_sales_transaction(db: Session, transaction_id: int):
    return db.query(models.HeadPenjualan).filter(models.HeadPenjualan.id == transaction_id).first()
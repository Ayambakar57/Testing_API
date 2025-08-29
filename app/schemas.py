from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[bool] = None

class User(UserBase):
    id: int
    last_login: Optional[datetime] = None
    attempt: int
    status: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Product Schemas
class ProductBase(BaseModel):
    sku: str
    nama_produk: str
    hpp: Decimal
    stok: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    sku: Optional[str] = None
    nama_produk: Optional[str] = None
    hpp: Optional[Decimal] = None
    stok: Optional[int] = None
    status: Optional[bool] = None

class Product(ProductBase):
    id: int
    status: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Sales Schemas
class DetailPenjualanCreate(BaseModel):
    produk_id: int
    jml: int
    nominal: Decimal

class DetailPenjualan(DetailPenjualanCreate):
    id: int
    nomor_penjualan: str
    product: Product
    created_at: datetime
    
    class Config:
        from_attributes = True

class HeadPenjualanCreate(BaseModel):
    details: List[DetailPenjualanCreate]

class HeadPenjualan(BaseModel):
    id: int
    nomor_penjualan: str
    tgl_penjualan: datetime
    status: str
    total_amount: Decimal
    details: List[DetailPenjualan]
    
    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

# Pagination
class PaginationParams(BaseModel):
    page: int = 1
    size: int = 10
    search: Optional[str] = None

class PaginatedResponse(BaseModel):
    data: List
    total: int
    page: int
    size: int
    total_pages: int
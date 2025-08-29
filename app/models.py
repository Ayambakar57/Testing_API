from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship  
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    email = Column(String(100), unique=True, index=True)
    last_login = Column(DateTime, nullable=True)
    attempt = Column(Integer, default=0)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), unique=True, index=True)
    nama_produk = Column(String(255), index=True)
    hpp = Column(Numeric(10, 2))
    stok = Column(Integer, default=0)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class HeadPenjualan(Base):
    __tablename__ = "head_penjualan"
    
    id = Column(Integer, primary_key=True, index=True)
    nomor_penjualan = Column(String(255), unique=True, index=True)
    tgl_penjualan = Column(DateTime, server_default=func.now())
    status = Column(String(50), default="pending")  # pending, completed, cancelled
    total_amount = Column(Numeric(10, 2), default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationship
    details = relationship("DetailPenjualan", back_populates="head")

class DetailPenjualan(Base):
    __tablename__ = "detail_penjualan"
    
    id = Column(Integer, primary_key=True, index=True)
    nomor_penjualan = Column(String(255), ForeignKey("head_penjualan.nomor_penjualan"))
    produk_id = Column(Integer, ForeignKey("products.id"))
    jml = Column(Integer)
    nominal = Column(Numeric(10, 2))
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    head = relationship("HeadPenjualan", back_populates="details")
    product = relationship("Product")
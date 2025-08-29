from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
from .routers import auth, users, products, sales

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sales Management API",
    description="REST API for Sales Management System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(sales.router)

@app.get("/")
def read_root():
    return {
        "message": "Sales Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
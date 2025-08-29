# FastAPI Sales Management API

A RESTful API for Sales Management System built with FastAPI and SQLAlchemy.

## Features

- User Authentication with JWT
- User Management
- Product Management
- Sales Management
- Pagination and Search functionality

## Tech Stack

- FastAPI
- SQLAlchemy (MySQL)
- Pydantic
- JWT Authentication
- Bcrypt Password Hashing

## Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/fastapi_sales.git
cd fastapi_sales
```

2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Configure environment variables

Create a `.env` file in the root directory with the following variables:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_db_name
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000
```

5. Run the application

```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Initial Setup

To create an initial admin user, run the provided script:

```bash
python create_user.py
```

## License

MIT
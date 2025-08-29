# create_user.py
from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash
import sys

def create_admin_user(username, email, password):
    db = SessionLocal()
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print(f"User {username} already exists!")
            return
            
        # Create new user
        hashed_password = get_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            status=True
        )
        db.add(new_user)
        db.commit()
        print(f"User {username} created successfully!")
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python create_user.py <username> <email> <password>")
    else:
        username = sys.argv[1]
        email = sys.argv[2]
        password = sys.argv[3]
        create_admin_user(username, email, password)
from passlib.context import CryptContext
import sys

# Use the same password hashing configuration as in the app
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_password_hash.py <password>")
        sys.exit(1)
    
    password = sys.argv[1]
    hashed_password = get_password_hash(password)
    
    print("\nPassword Hash for SQL Insert:")
    print(f"'{hashed_password}'")
    print("\nExample SQL:")
    print(f"INSERT INTO users (username, email, password, status) VALUES ('admin', 'admin@example.com', '{hashed_password}', 1);")
    print("\nAfter inserting this user, you can login with:")
    print(f"Username: admin")
    print(f"Password: {password}")
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function used to hash a new users password in the database.
def hash(password: str):
    return pwd_context.hash(password)

    
# Function to compare a users password to the one stored in the database.
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


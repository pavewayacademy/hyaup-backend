from datetime import datetime
from h11._abnf import status_code
from fastapi import status
from fastapi import HTTPException
from sqlalchemy import text
from models.user import User, CreateUser, UserResponse, UserLogin
from fastapi import FastAPI, Depends
from Crypto.Hash import SHA256
from config.database import Base, engine, get_db
from sqlalchemy.orm import Session

app = FastAPI(
    title= "Hyaup Backend",
    description= "Hyaup Backend",
    version= "0.0.1",
    debug= True,
)

# Create the database tables on startup (if they don't exist)
Base.metadata.create_all(bind=engine)

@app.get("/healthcheck")
def check_db_connection(db: Session = Depends(get_db)):
    # Simple query rto verify the connection works
    db.execute(text('SELECT 1'))
    return {"message": "Database connection successful"}

@app.post("/user", response_model=UserResponse)
def create_user(data: CreateUser, db: Session = Depends(get_db)):
    # Generate username from email address
    username = data.email.split("@")[0].lower()

    # Check if the username and email already exists
    db_user = db.query(User).filter(
        (User.email == data.email) | (User.username == username)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    # In production, ALWAYS hash passwords before saving them (e.g., using bcrypt, passlib, Crypto)
    hashed_password = SHA256.new(data=data.password.encode("UTF-8")).hexdigest()

    # Create the user model instance
    new_user = User(
        email=data.email,
        username=username,
        age=data.age,
        role=data.role,
        first_name=data.first_name,
        last_name=data.last_name,
        gender=data.gender,
        hashed_password=hashed_password
    )

    # Save to MySQL DB
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login", response_model=UserResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    # Check if a user with the provided email address exist
    db_user = db.query(User).filter(User.email == data.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify the user password
    hashed_password = SHA256.new(data=data.password.encode("UTF-8")).hexdigest()
    if hashed_password != db_user.hashed_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Update the last login time
    db_user.last_login_at = datetime.now()
    db.commit()
    db.refresh(db_user)

    return db_user

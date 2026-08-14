from sqlalchemy import text
from models.user import CreateUser
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

@app.post("/user")
def create_user(data: CreateUser):
    data.password_hash = SHA256.new(data.password.encode("utf-8")).hexdigest()
    return data.model_dump()


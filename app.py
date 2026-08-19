from datetime import datetime
from models.job import JobCreate, JobDB
from fastapi import FastAPI, Depends, HTTPException, status
from Crypto.Hash import SHA256
from config.database import Base, engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError



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
    # Simple query to verify the connection works
    db.execute("SELECT 1")
    return {"message": "Database connection successful"}


#THE JOB POSTING ENDPOINT
@app.post("/job")
def Job_create(data: JobCreate, db: Session = Depends(get_db)):
    
    # Converts the incoming Pydantic validation data into a standard Python dictionary
    job_dict = data.model_dump()
    
    # Automatically adds todys date as a string
    job_dict["post_date"] = datetime.today().strftime("%Y-%m-%d")
    
    # this Unpacks the dictionary data to create a new SQLAlchemy database model instance
    db_job = JobDB(**job_dict)
    
    try:
        db.add(db_job) # Stages new job object
        db.commit() # permanently saves job records into the daatabase
        db.refresh(db_job) # refresh the job object to pull newly generated database ID
        return db_job # retrns job data back to the user
    except IntegrityError:
        db.rollback()  # Clean up the failed transaction
        # stops and sends a clean error message to the browser
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A job with this unique identifier or title already exists."
        )





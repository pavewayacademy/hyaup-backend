from fastapi import FastAPI
from config.database import engine, Base
from datetime import datetime
from models.user import UserResponse, UserLogin, User
import httpx, asyncio, json
from models.job import JobCreate, JobDB
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from typing import List
from Crypto.Hash import SHA256
from config.database import Base, engine, get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from bs4 import BeautifulSoup



app = FastAPI(
    title= "Hyaup Backend",
    description= "Hyaup Backend",
    version= "0.0.1",
    debug= True,
)

# Create the database tables on startup (if they don't exist)
Base.metadata.create_all(bind=engine)


# ==========================================
# STANDARD API ENDPOINTS
# ==========================================

@app.get("/")
def read_root():
    return {"message": "Welcome to the Multi-Source Job Search Engine API! Visit /docs for documentation."}


@app.get("/healthcheck")
def check_db_connection(db: Session = Depends(get_db)):
    # Simple query to verify the connection works
    db.execute("SELECT 1")
    return {"message": "Database connection successful"}


    # Check if the username and email already exists
    db_user = db.query(User).filter(
        (User.email == data.email) | (User.username == username)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    # In production, ALWAYS hash passwords before saving them
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
#THE JOB POSTING ENDPOINT
@app.post("/job")
def Job_create(data: JobCreate, db: Session = Depends(get_db)):
    
    # Converts the incoming Pydantic validation data into a standard Python dictionary
    job_dict = data.model_dump()

    job_dict["required_skills"] = json.dumps(job_dict.get("required_skills", []))
    
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




    return db_user


# ==========================================
# SCRAPER CORE PIPELINE (AI DRIVEN)
# ==========================================

async def fetch_external_jobs_page(client: httpx.AsyncClient, url: str) -> tuple[str, str]:
    """Asynchronously fetches HTML content and returns (url, html_text)."""
    try:
        response = await client.get(url, timeout=20.0, follow_redirects=True)
        response.raise_for_status()
        return url, response.text
    except httpx.HTTPError as e:
        print(f"[SCRAPER ERROR] Failed to fetch {url}: {e}")
        return url, ""


async def run_scraper_pipeline(target_urls: List[str]):
    """Fetches pages, extracts raw text, and forwards it to the AI team."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    AI_TEAM_ENDPOINT = "https://ai-team-api-url/v1/process-text" # <-- Replace with actual AI API URL
    
    async with httpx.AsyncClient(headers=headers) as client:
        tasks = [fetch_external_jobs_page(client, url) for url in target_urls]
        results = await asyncio.gather(*tasks)

        for url, html in results:
            if not html:
                continue
            
            soup = BeautifulSoup(html, "html.parser")
            raw_text = soup.get_text(separator=" ", strip=True)

            #print scrapped jobs on terminal
            print(f"\n=================== SCRAPED TEXT FROM: {url} ===================")
            print(raw_text[:2000])  # Prints the first 2000 characters so it doesn't flood your screen
            print("==================================================================\n")

            payload = {
                "source_url": url,
                "raw_html_text": raw_text,
                # Directs the AI team's system to your specific webhook endpoint
                "callback_url": "https://funny-onions-like.loca.lt/webhook/ai-results"  
            }

            try:
                print(f"[SCRAPER] Sending extracted text from {url} to the AI Team...")
                response = await client.post(AI_TEAM_ENDPOINT, json=payload, timeout=30.0)
                response.raise_for_status()
                print(f"[SCRAPER] Successfully delivered text payload for {url}")
            except httpx.HTTPError as e:
                print(f"[SCRAPER ERROR] Failed to send data to AI team for {url}: {e}")


# ==========================================
# SCRAPER & AI WEBHOOK API ENDPOINTS
# ==========================================

@app.post("/jobs/scrape", status_code=202)
async def trigger_scraper(background_tasks: BackgroundTasks):
    """
    Triggers scrapers for target platforms concurrently in the background.
    """
    target_urls = [
        "https://cameroonjobs.net",
        "https://unjobs.org",
        "https://www.cameroondesks.com"
    ]
    background_tasks.add_task(run_scraper_pipeline, target_urls)
    return {
        "status": "accepted",
        "message": "Scraper pipeline triggered in the background. Text will be sent to the AI Team."
    }


@app.post("/webhook/ai-results", status_code=200)
async def receive_ai_job_listings(jobs: List[JobCreate], db: Session = Depends(get_db)):
    """
    Webhook endpoint for the AI team to return the structured dictionary of jobs.
    """
    # TODO: Once you create a SQL database model for Jobs, you will loop and insert them here:
    # for job in jobs:
    #     db.add(JobModel(**job.model_dump()))
    # db.commit()
    
    print(f"[WEBHOOK] Received {len(jobs)} structured job entries from AI team.")
    return {
        "status": "success", 
        "message": f"Successfully received {len(jobs)} listings. Database saving block pending model structure."
    }



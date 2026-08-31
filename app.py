import json
import logging
from fastapi import FastAPI
from config.config import settings
from config.firebase import init_firebase

# Initialize logging
logger = logging.getLogger(__name__)


# Initialize the FastAPI application
hyaup_app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION
)

# Define a root route
@hyaup_app.get("/", summary="Root Endpoint", description="Default Endpoint")
async def read_root():
    # Initialize Firebase when module is imported
    # This ensures it's ready when FastAPI app starts
    init_firebase()
    return {"message": "Welcome to the HyaUp API!"}



logger.info("HyaUp Backend API Starting....")
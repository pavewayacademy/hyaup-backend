import json
import logging
from fastapi import FastAPI
from config.config import settings
from config.firebase import init_firebase
from contextlib import asynccontextmanager
from routes.user import userRouter
from config.database import init_db

# Initialize logging
logger = logging.getLogger(__name__)

# Define the startup and shutdown event handlers
@asynccontextmanager
async def startup(app: FastAPI):
    """
    Handles secure initialization and shutdown of the Firebase Admin SDK
    and application resources.
    Prevents duplicate inititilization exceptions on hot-reloads.
    """
    try:
        logger.info("Initializing Firebase Admin SDK")
        init_firebase()
        logger.info("Firebase Admin SDK initialized successfully")
        logger.info("Initializing database")
        await init_db()
        logger.info("Database initialized successfully")
        yield
    finally:
        logger.info("Shutting down application resources")

# Initialize the FastAPI application
hyaup_app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=startup
)

# Define a root route
@hyaup_app.get("/", summary="Root Endpoint", description="Default Endpoint")
async def read_root():
    return {"message": "Welcome to the HyaUp API!"}

# Include our routers in the application
hyaup_app.include_router(userRouter, prefix="/users", tags=["users"])
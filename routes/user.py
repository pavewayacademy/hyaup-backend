# routes/user.py
# Define all users related endpoints
# prefix = /api/v1/users
# routers for the user 
# Create user /users POST
# Update user /users/{id} PUT
# Delete user /users/{id} DELETE
# Get user /users/{id} GET
# Get all users /users GET
# Get user by email /users/get-by-email/{email} GET
# Get user by phone /users/get-by-phone/{phone} GET

from pydantic import EmailStr
import logging
from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, Path, Body, status

from utils.firebase import create_firebase_user, update_firebase_user, get_user_by_uid, get_user_by_email, get_user_by_phone_number, delete_firebase_user
from models.user import FirebaseUser, CreateFirebaseUser, UpdateFirebaseUser

# Initiliaze the logger
logger = logging.getLogger(__name__)

# Initialize the router
userRouter = APIRouter(
    responses={
        200: {"description": "OK"},
        201: {"description": "Created"},
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Not Found"},
        500: {"description": "Internal Server Error"}
    }
)


# Add a route for creating a Firebase User
@userRouter.post("", summary="Create User with Email and Password", description="Create a new user with email and password")
async def create_user_with_email_and_password(new_user: CreateFirebaseUser = Body(...)):
    try:
        result = create_firebase_user(new_user)
    except Exception as e:
        logger.error(f"Error creating new user: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return result

# Add a route for getting a Firebase User by UID
@userRouter.get("/{uid}", summary="Get Firebase User by UID", description="Get a Firebase user by UID", response_model=FirebaseUser)
async def get_firebase_user_by_uid(uid: str):
    try:
        result = get_user_by_uid(uid)
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return result

# Add a route for getting a Firebase User by email
@userRouter.get("/get-by-email/{email}", summary="Get Firebase User by Email", description="Get a Firebase user by email", response_model=FirebaseUser)
async def get_firebase_user_by_email(email: EmailStr):
    try:
        result = get_user_by_email(email)
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return result

# Add a route for getting a Firebase User by phone number
@userRouter.get("/get-by-phone/{phone_number}", summary="Get Firebase User by Phone Number", description="Get a Firebase user by phone number", response_model=FirebaseUser)
async def get_firebase_user_by_phone_number(phone_number: str):
    try:
        result = get_user_by_phone_number(phone_number)
    except Exception as e:
        logger.error(f"Error getting user: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return result

# Add a route for updating a Firebase User
@userRouter.patch("/{uid}", summary="Update Firebase User", description="Update a Firebase user by UID")
async def patch_firebase_user(uid: str, user: UpdateFirebaseUser = Body(...)):
    try:
        result = update_firebase_user(user, uid)
    except Exception as e:
        logger.error(f"Error updating user: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return result

# Add a route to delete a Firebase User
@userRouter.delete("/{uid}", summary="Delete Firebase User", description="Delete a Firebase user by UID")
async def delete_user(uid: str):
    try:
        result = delete_firebase_user(uid)
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return result
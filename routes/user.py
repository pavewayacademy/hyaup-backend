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

from sqlalchemy.orm import Session
from pydantic import EmailStr
import logging
from sqlmodel import select
from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, Path, Body, status

from utils.firebase import create_firebase_user, update_firebase_user, get_user_by_uid, get_user_by_email, get_user_by_phone_number, delete_firebase_user
from models.user import FirebaseUser, CreateFirebaseUser, UpdateFirebaseUser, UpdateUserAccount, User
from middleware.auth import verify_firebase_token
from config.database import get_session
from services.account import AccountService

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
async def get_firebase_user_by_uid(uid: str, user: dict = Depends(verify_firebase_token)):
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
@userRouter.patch("/{uid}", summary="Update Firebase User", description="Update a Firebase user by UID", dependencies=[Depends(get_session)])
async def update_user_account(uid: str, userData: UpdateUserAccount = Body(...), session: Session = Depends(get_session), account_service = Depends(AccountService)):
    try:
        # Check if user account already exist
        statement = select(User).where((User.email == userData.email) | (User.uid == userData.uid))
        statement_exec = await session.exec(statement)
        existing_user = statement_exec.first()
        print(existing_user)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exist")
        result = None
        # Check if user is onboarding
        if userData.is_onboarded == False:
            # Create new user account
            logger.info(f"Creating new user account for {userData.uid}")
            result = await account_service.create_user_account(userData, session)
        else:
            # Update user data
            logger.info(f"Updating user account for {userData.uid}")
            result = await account_service.update_user_account(userData, session)

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
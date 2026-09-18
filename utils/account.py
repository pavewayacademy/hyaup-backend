# utils/account.py

from models.user import UpdateUserAccount, User
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

# Initiliaze the logger
logger = logging.getLogger(__name__)


async def save_user_account(userData: UpdateUserAccount, session: Session) -> User:
    try:
        # Map our data to the user model
        new_user = User(
            uid=userData.uid,
            email=userData.email,
            name=userData.name,
            city=userData.city,
            phone_number=userData.phone,
            profile_picture=userData.profile_picture,
            role=userData.role,
            is_onboarded=userData.is_onboarded,
        )
        # Add user to session
        session.add(new_user)
        # Commit the changes
        await session.commit()
        # Refresh the user
        await session.refresh(new_user)
        return new_user

    except Exception as e:
        print(f"Util Error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
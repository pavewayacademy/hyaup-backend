# services/account.py

from models.user import UpdateUserAccount
from models.company import NewCompany
from fastapi import HTTPException, status
import logging
from sqlalchemy.orm import Session
from utils.account import save_user_account
from utils.company import create_company


# Initiliaze the logger
logger = logging.getLogger(__name__)


class AccountService:
    def __init__(self):
        pass
    
    async def create_user_account(self, user: UpdateUserAccount, session: Session) -> dict:
        try:
            # Save user account
            result = await save_user_account(user, session)
            print(result)
            # Check if user is employer
            if user.role == "employer":
                # Create account account
                user_data = user.model_dump()
                user_data["user_id"] = result.id
                new_company_data = NewCompany.model_validate(user_data)
                print(new_company_data)
                new_company = await create_company(new_company_data, session)
                print(new_company)
            
            return result
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error saving user account: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        
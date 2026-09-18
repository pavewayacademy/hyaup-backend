# utils/company.py

from models.company import NewCompany, Company
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

# Initiliaze the logger
logger = logging.getLogger(__name__)


async def create_company(companyData: NewCompany, session: Session) -> dict:
    try:
        # Map our data to the company model
        new_company = Company(
            user_id=companyData.user_id,
            email=companyData.email,
            name=companyData.company_name,
            industry=companyData.industry,
            city=companyData.city,
            size=companyData.company_size,
            phone=companyData.phone,
            website=companyData.website,
            bio=companyData.bio,
        )
        # Add user to session
        session.add(new_company)
        # Commit the changes
        await session.commit()
        # Refresh the user
        await session.refresh(new_company)
        print(f"Company {new_company} saved successfully.")
        return companyData.dict()

    except Exception as e:
        print(f"Util Error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
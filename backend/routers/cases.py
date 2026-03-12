import re
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.database import get_db
from backend.models.case import CourtCase
from backend.schemas import CaseData
from backend.services.ecourts import get_case_data

router = APIRouter(prefix="/api/case", tags=["cases"])

# 16 char string format: 2 State, 2 Dist, 2 Est, 6 Case, 4 Year
# Adjusting regex slightly to accommodate potential real-world CNR anomalies,
# but keeping it robust as requested.
CNR_REGEX = re.compile(r"^[A-Z]{2}[A-Z0-9]{2}[0-9]{2}[0-9]{6}[0-9]{4}$")

@router.get("/{cnr}", response_model=CaseData)
async def get_case(cnr: str, db: AsyncSession = Depends(get_db)):
    cnr = cnr.upper().strip()
    
    # Optional Regex validation
    if not CNR_REGEX.match(cnr):
        raise HTTPException(
            status_code=400, 
            detail="Invalid CNR format. Must be 16 characters (e.g., UPAH010012342024)"
        )
        
    try:
        case_data = await get_case_data(cnr)
        
        # Upsert in PostgreSQL
        stmt = select(CourtCase).where(CourtCase.cnr == cnr)
        result = await db.execute(stmt)
        existing_case = result.scalar_one_or_none()
        
        if existing_case:
            existing_case.case_type = case_data.case_type
            existing_case.court = case_data.court
            existing_case.district = case_data.district
            existing_case.sections = case_data.sections
            existing_case.petitioner = case_data.petitioner
            existing_case.respondent = case_data.respondent
            existing_case.filing_date = case_data.filing_date
            existing_case.status = case_data.status
            existing_case.next_hearing = case_data.next_hearing or ""
            existing_case.data_source = case_data.data_source
        else:
            new_case = CourtCase(
                cnr=case_data.cnr,
                case_type=case_data.case_type,
                court=case_data.court,
                district=case_data.district,
                sections=case_data.sections,
                petitioner=case_data.petitioner,
                respondent=case_data.respondent,
                filing_date=case_data.filing_date,
                status=case_data.status,
                next_hearing=case_data.next_hearing or "",
                data_source=case_data.data_source
            )
            db.add(new_case)
            
        await db.commit()
        return case_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

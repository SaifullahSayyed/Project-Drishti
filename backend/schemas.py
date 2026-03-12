from pydantic import BaseModel
from typing import List, Optional

class CaseData(BaseModel):
    cnr: str
    case_type: str
    court: str
    district: str
    sections: List[str] = []
    petitioner: str
    respondent: str
    filing_date: str
    status: str
    next_hearing: Optional[str] = None
    data_source: str = "ecourts_api"

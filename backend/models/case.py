import datetime
from sqlalchemy import Column, Integer, String, DateTime, ARRAY
from sqlalchemy.orm import relationship
from backend.database import Base

class CourtCase(Base):
    __tablename__ = "court_cases"

    id = Column(Integer, primary_key=True, index=True)
    cnr = Column(String, unique=True, index=True, nullable=False)
    case_type = Column(String, nullable=False, index=True)
    court = Column(String, nullable=False)
    district = Column(String, nullable=False, index=True)
    sections = Column(ARRAY(String), default=[])
    petitioner = Column(String)
    respondent = Column(String)
    filing_date = Column(String)
    status = Column(String)
    next_hearing = Column(String)
    data_source = Column(String)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    predictions = relationship("Prediction", back_populates="case", cascade="all, delete-orphan")

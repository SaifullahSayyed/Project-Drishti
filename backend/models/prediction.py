import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("court_cases.id"), nullable=False)
    
    petitioner_probability = Column(Float, nullable=False)
    respondent_probability = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    
    predicted_years = Column(Float)
    range_min = Column(Float)
    range_max = Column(Float)
    district_average = Column(Float)
    national_average = Column(Float)
    
    top_features = Column(JSON)
    data_source = Column(String)
    cases_analyzed = Column(Integer)
    
    pathway_recommended = Column(String)
    pathway_details = Column(JSON)
    
    bottlenecks = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    case = relationship("CourtCase", back_populates="predictions")

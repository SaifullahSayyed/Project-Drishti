import logging
from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from backend.schemas import CaseData
from backend.services.ecourts import ecourts_service
from backend.services.prediction_engine import engine as prediction_engine
from backend.services.pathway_router import router_engine
from backend.services.indian_kanoon import search_indian_kanoon, Precedent
from backend.services.groq_service import groq_service

logger = logging.getLogger(__name__)
router = APIRouter()

class PredictResponse(BaseModel):
    cnr: str
    case_data: CaseData
    outcome: Dict[str, Any]
    pathway: Dict[str, Any]
    bottlenecks: List[Dict[str, Any]]
    precedents: List[Precedent]
    rag_summary: str
    citizen_report_url: str

@router.get("/{cnr}", response_model=PredictResponse)
async def predict_case_outcome(
    cnr: str = Path(..., description="16-character CNR number", min_length=16, max_length=16)
):
    """
    Main Orchestrator endpoint for DRISHTI.
    1. Fetch live case data (eCourts)
    2. Run ML Outcome Model (XGBoost/Stats)
    3. Determine Optimal Resolution Pathway
    4. Fetch Precedents (Indian Kanoon API)
    5. Generate RAG text string using LLaMA3 (Groq API)
    """
    logger.info(f"Orchestrating full predictive pipeline for CNR: {cnr}")
    
    # 1. Fetch live data
    try:
        case_data = await ecourts_service.get_case_data(cnr)
    except Exception as e:
        logger.error(f"Failed to fetch case data: {e}")
        raise HTTPException(status_code=404, detail="Case not found or eCourts API unreachable")

    # 2. ML Prediction (Win probability, time range, features & bottlenecks)
    try:
        prediction_result = prediction_engine.predict(case_data)
        bottlenecks = getattr(prediction_result, 'bottlenecks', [])
    except Exception as e:
        logger.error(f"Prediction engine error: {e}")
        raise HTTPException(status_code=500, detail="Failed to run predictive models")

    # 3. Pathway Recommendation
    try:
        pathway_result = router_engine.analyze(case_data, prediction_result.predicted_years)
    except Exception as e:
        logger.error(f"Pathway router error: {e}")
        raise HTTPException(status_code=500, detail="Failed to route case pathway")

    # 4. Fetch Precedents
    # In a real app we would use "Pinecone" to vectorize the case facts and semantic search.
    # For speed under hackathon constraints, we use the Kanoon search API directly on case type/district
    search_query = f"{case_data.case_type} {case_data.district} high court"
    try:
        precedents = await search_indian_kanoon(search_query, limit=3)
    except Exception as e:
        logger.error(f"Precedent fetch error: {e}")
        precedents = []

    # 5. Groq RAG Response
    try:
        rag_summary = await groq_service.generate_rag_response(
            case_cnr=cnr,
            case_type=case_data.case_type,
            pet_prob=prediction_result.petitioner_probability,
            months_est=prediction_result.predicted_years * 12.0,
            pathway=pathway_result.recommended,
            legal_basis=pathway_result.eligibility_reason,
            precedents=precedents
        )
    except Exception as e:
        logger.error(f"Groq RAG error: {e}")
        rag_summary = "Prediction summary could not be generated at this time."

    return PredictResponse(
        cnr=cnr,
        case_data=case_data,
        outcome={
            "petitioner_win_prob": prediction_result.petitioner_probability,
            "respondent_win_prob": prediction_result.respondent_probability,
            "confidence_score": prediction_result.confidence,
            "estimated_years": prediction_result.predicted_years,
            "range_min": prediction_result.range_min,
            "range_max": prediction_result.range_max,
            "district_avg": prediction_result.district_average,
            "national_avg": prediction_result.national_average,
            "top_features": prediction_result.top_features
        },
        pathway=pathway_result.model_dump(),
        bottlenecks=bottlenecks,
        precedents=precedents,
        rag_summary=rag_summary,
        citizen_report_url=f"/api/report/{cnr}" # Will implement in Step 11
    )

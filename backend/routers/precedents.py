import logging
from fastapi import APIRouter, HTTPException

logger = logging.getLogger(__name__)
router = APIRouter()

# For a Hackathon, the precedents logic is already integrated 
# directly in the `predict_case_outcome` orchestrator for a single API call flow.
# This router remains to support independent precedent queries if the frontend
# wants to build a separate search view.

from backend.services.indian_kanoon import search_indian_kanoon, Precedent
from typing import List

@router.get("/search", response_model=List[Precedent])
async def get_precedents(q: str):
    logger.info(f"Independent precedent search for: {q}")
    return await search_indian_kanoon(q, limit=5)

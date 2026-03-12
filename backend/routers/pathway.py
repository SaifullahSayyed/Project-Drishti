import logging
from fastapi import APIRouter
from backend.services.pathway_router import router_engine

logger = logging.getLogger(__name__)
router = APIRouter()

# For the hackathon, the Pathway Orchestration is integrated directly into the `predict` router.
# This standalone endpoint allows the frontend to fetch the raw rules if it wants to build UI
# for explaining the Rules directly to the user.

@router.get("/rules")
async def get_pathway_rules():
    return router_engine.rules

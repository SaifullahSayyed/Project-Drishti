import logging
from fastapi import APIRouter, HTTPException, Path
from fastapi.responses import StreamingResponse

from backend.routers.predict import predict_case_outcome
from backend.services.pdf_generator import generate_citizen_report

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/{cnr}")
async def get_citizen_report(
    cnr: str = Path(..., description="16-character CNR number", min_length=16, max_length=16)
):
    """
    Generates a PDF citizen report for the given CNR.
    It internally calls the orchestrator to fetch the latest prediction
    and formats it into a downloadable PDF document.
    """
    logger.info(f"Generating PDF Citizen Report for {cnr}")
    
    try:
        # Instead of recalculating, we just await the orchestrator directly in-memory
        # (In a true prod app, we'd cache the orchestration result to avoid double Groq API calls 
        # or separate the PDF gen to a background task, but this is fine for the Hackathon)
        prediction_obj = await predict_case_outcome(cnr)
        
        # Convert Pydantic object to dict for the report generator
        predict_dict = prediction_obj.model_dump()
        
        pdf_buffer = generate_citizen_report(predict_dict)
        
        headers = {
            'Content-Disposition': f'attachment; filename="DRISHTI_Report_{cnr}.pdf"'
        }
        
        return StreamingResponse(
            pdf_buffer, 
            media_type="application/pdf", 
            headers=headers
        )
        
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Failed to generate PDF for {cnr}: {e}")
        raise HTTPException(status_code=500, detail="Could not generate PDF report at this time.")

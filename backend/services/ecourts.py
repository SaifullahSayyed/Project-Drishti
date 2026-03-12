import json
import logging
import httpx
from redis.asyncio import Redis

from backend.config import settings
from backend.schemas import CaseData
from backend.services.njdg import scrape_case_from_njdg

logger = logging.getLogger(__name__)

# Initialize Redis client safely in case REDIS_URL has problems
try:
    redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
except Exception as e:
    logger.error(f"Failed to initialize Redis: {e}")
    redis_client = None

ECOURTS_API_URL = "https://apis.ecourts.gov.in/public_api/case_status"
HEADERS = {
    "User-Agent": "DRISHTI-JusticeEngine/1.0 (India Innovates 2026 Hackathon)",
    "Accept": "application/json",
    "Accept-Language": "en-IN"
}

async def get_case_data(cnr: str) -> CaseData:
    cache_key = f"case:{cnr}"
    
    # 1. Check Cache
    if redis_client:
        try:
            cached = await redis_client.get(cache_key)
            if cached:
                logger.info(f"Cache hit for CNR {cnr}")
                return CaseData.model_validate_json(cached)
        except Exception as e:
            logger.warning(f"Redis cache error: {str(e)}")

    # 2. Try eCourts API
    try:
        logger.info(f"Fetching {cnr} from eCourts API")
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(
                ECOURTS_API_URL, 
                params={"cnr_number": cnr}, 
                headers=HEADERS
            )
            
            if response.status_code == 200:
                data = response.json()
                if data and not data.get("error"):
                    case_data = CaseData(
                        cnr=cnr,
                        case_type=data.get("case_type", "Unknown"),
                        court=data.get("court_name", "Unknown Court"),
                        district=data.get("district", "Unknown District"),
                        sections=data.get("sections", []),
                        petitioner=data.get("petitioner", "Unknown"),
                        respondent=data.get("respondent", "Unknown"),
                        filing_date=data.get("filing_date", "Unknown"),
                        status=data.get("status", "Pending"),
                        next_hearing=data.get("next_hearing", ""),
                        data_source="ecourts_api"
                    )
                    
                    if redis_client:
                        try:
                            await redis_client.setex(cache_key, 3600, case_data.model_dump_json())
                        except Exception as ce:
                            pass
                    return case_data
    except Exception as e:
        logger.error(f"eCourts API failed for {cnr}: {str(e)}")

    # 3. Fallback to NJDG Scraper
    logger.info(f"Falling back to NJDG scraper for {cnr}")
    case_data = await scrape_case_from_njdg(cnr)
    
    if redis_client:
        try:
            await redis_client.setex(cache_key, 3600, case_data.model_dump_json())
        except Exception as ce:
            pass

    return case_data

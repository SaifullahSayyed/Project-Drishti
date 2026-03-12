import json
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

from backend.schemas import CaseData

logger = logging.getLogger(__name__)

class PathwayDetail(BaseModel):
    name: str
    eligible: bool
    reason: str
    estimated_months: Optional[float] = None
    cost_saving_inr: int = 0
    how_to_apply: str = ""
    nearest_centre: str = ""
    legal_basis: str = ""
    success_rate: Optional[float] = None

class PathwayRecommendation(BaseModel):
    recommended: str
    estimated_months: Optional[float] = None
    cost_saving_inr: int = 0
    eligibility: bool
    eligibility_reason: str
    how_to_apply: str
    nearest_centre: str
    all_pathways: List[PathwayDetail]

PATHWAY_RULES = {
    "Lok Adalat": {
        "eligible_case_types": [
            "motor_accident", "matrimonial", "land_acquisition",
            "property_dispute", "cheque_bounce", "labour_dispute"
        ],
        "max_case_value_inr": 10_000_000,
        "requires_mutual_consent": True,
        "avg_resolution_months": 3.5,
        "cost_saving_inr": 45000,
        "success_rate": 0.78,
        "legal_basis": "Legal Services Authorities Act 1987",
        "how_to_apply": "Contact District Legal Services Authority (DLSA)",
        "contact_lookup": {
            "allahabad": "DLSA Allahabad — 0532-2623073",
            "lucknow": "DLSA Lucknow — 0522-2239197",
            "default": "DLSA situated at the local District Court Complex"
        }
    },
    "Fast Track Court": {
        "eligible_case_types": ["criminal_assault", "criminal_rape", "atrocities"],
        "cost_saving_inr": 12000,
        "requires_mutual_consent": False,
        "avg_resolution_months": 8.0,
        "success_rate": 0.71,
        "legal_basis": "Fast Track Special Court Act 2019",
        "how_to_apply": "File application through public prosecutor to Designated Fast Track Judge",
        "contact_lookup": {"default": "Designated Fast Track Court, District Sessions Division"}
    },
    "Mediation": {
        "eligible_case_types": ["matrimonial", "property_dispute", "commercial"],
        "cost_saving_inr": 35000,
        "requires_mutual_consent": True,
        "avg_resolution_months": 5.0,
        "success_rate": 0.65,
        "legal_basis": "Mediation Act 2023",
        "how_to_apply": "File application for reference to Mediation Centre under Sec 89 CPC",
        "contact_lookup": {"default": "Mediation and Conciliation Centre, District Court"}
    },
    "Standard Trial": {
        "eligible_case_types": ["all"],
        "cost_saving_inr": 0,
        "requires_mutual_consent": False,
        "avg_resolution_months": None, # Depends on district, handled in code
        "success_rate": None,
        "legal_basis": "Code of Civil/Criminal Procedure",
        "how_to_apply": "Standard litigation track",
        "contact_lookup": {"default": "Respective Court Room"}
    }
}

class PathwayRouter:
    def __init__(self):
        self.rules = PATHWAY_RULES

    def _get_contact(self, pathway_name: str, district: str) -> str:
        contacts = self.rules[pathway_name].get("contact_lookup", {})
        dist_key = district.lower().strip()
        return contacts.get(dist_key, contacts.get("default", "Local Court"))

    def analyze(self, case_data: CaseData, predicted_years: float) -> PathwayRecommendation:
        ctype = case_data.case_type.lower()
        district = case_data.district
        
        all_pathways = []
        best_pathway = None
        best_score = -1
        
        for name, rules in self.rules.items():
            is_eligible = False
            reason = ""
            
            # Eligibility check
            if "all" in rules["eligible_case_types"]:
                is_eligible = True
                reason = "Default standard procedure"
            elif ctype in rules["eligible_case_types"]:
                is_eligible = True
                reason = f"Case type '{ctype}' is eligible under {rules['legal_basis']}."
            else:
                is_eligible = False
                reason = f"Case type '{ctype}' is not statutorily eligible for {name}."

            detail = PathwayDetail(
                name=name,
                eligible=is_eligible,
                reason=reason,
                estimated_months=rules["avg_resolution_months"],
                cost_saving_inr=rules["cost_saving_inr"],
                legal_basis=rules["legal_basis"],
                success_rate=rules["success_rate"],
                how_to_apply=rules["how_to_apply"],
                nearest_centre=self._get_contact(name, district)
            )
            
            # Standard Trial needs dynamic months from prediction engine
            if name == "Standard Trial":
                detail.estimated_months = predicted_years * 12.0
                
            all_pathways.append(detail)
            
            # Scoring algorithm to pick recommendation
            if is_eligible:
                score = 0
                if name != "Standard Trial":
                    score += 50 # Strongly prefer ADR/Fast track over standard
                if detail.estimated_months:
                    # Higher score for faster resolution
                    score += (predicted_years * 12.0) - detail.estimated_months
                
                if score > best_score:
                    best_score = score
                    best_pathway = detail
                    
        if not best_pathway:
            # Fallback
            best_pathway = next(p for p in all_pathways if p.name == "Standard Trial")

        return PathwayRecommendation(
            recommended=best_pathway.name,
            estimated_months=best_pathway.estimated_months,
            cost_saving_inr=best_pathway.cost_saving_inr,
            eligibility=best_pathway.eligible,
            eligibility_reason=best_pathway.reason,
            how_to_apply=best_pathway.how_to_apply,
            nearest_centre=best_pathway.nearest_centre,
            all_pathways=all_pathways
        )

router_engine = PathwayRouter()

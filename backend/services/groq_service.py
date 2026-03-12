import logging
import os
from groq import AsyncGroq
from backend.config import settings

logger = logging.getLogger(__name__)

class GroqService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.is_configured = bool(self.api_key and "your_" not in self.api_key)
        if self.is_configured:
            self.client = AsyncGroq(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("Groq API key missing or invalid. RAG responses will fallback to static text.")

    async def generate_rag_response(
        self, 
        case_cnr: str,
        case_type: str,
        pet_prob: float,
        months_est: float,
        pathway: str,
        legal_basis: str,
        precedents: list
    ) -> str:
        
        if not self.is_configured:
            return self._fallback_response(case_cnr, pathway, months_est)

        # Build Context from the previous orchestration steps
        precedent_text = "\n".join([f"- {p.title} ({p.year}): {p.key_principle}" for p in precedents[:3]])
        
        prompt = f"""
        You are DRISHTI, India's premier Predictive Justice AI, advising a citizen on their case.
        Be highly professional, empathetic, clear, and legally accurate but accessible.
        
        Case Details:
        - CNR: {case_cnr}
        - Type: {case_type}
        - Petitioner Win Probability: {pet_prob}% (Based on district stats & XGBoost)
        - Estimated Timeline: {months_est} months
        - Recommended Pathway: {pathway} (Basis: {legal_basis})
        
        Relevant Legal Precedents (Indian Kanoon):
        {precedent_text}
        
        Task:
        Write a 3-paragraph executive summary for the citizen.
        Paragraph 1: Clear status and prediction.
        Paragraph 2: Justification citing the precedents.
        Paragraph 3: Actionable next steps via the recommended pathway.
        
        Do not use markdown formatting like ** or ##. Just clean text paragraphs.
        """

        try:
            # We use LLaMA 3 8b or 70b via Groq for ultra-fast inference (< 1 sec)
            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful Indian legal assistant."},
                    {"role": "user", "content": prompt}
                ],
                model="llama3-8b-8192", 
                temperature=0.3,
                max_tokens=500
            )
            return chat_completion.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Groq API Error: {e}")
            return self._fallback_response(case_cnr, pathway, months_est)

    def _fallback_response(self, cnr: str, pathway: str, months: float) -> str:
        return (
            f"Based on historical data for CNR {cnr}, we estimate a resolution time of {months} months. "
            f"Data suggests pursuing the {pathway} track will be most efficient. "
            "Please consult your legal counsel to initiate this recommended pathway and reference similar jurisdictional precedents."
        )

groq_service = GroqService()

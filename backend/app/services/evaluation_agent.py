from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.services.llm_service import llm_service
from typing import Dict, Any, List

class MatchEvaluation(BaseModel):
    score: float = Field(description="A score from 0.0 to 100.0 representing the match percentage.")
    reasoning: str = Field(description="Brief explanation of why this score was given.")
    passes_threshold: bool = Field(description="True if score >= 80, False otherwise.")
    missing_critical_skills: List[str] = Field(description="List of critical skills missing from the resume.")

class EvaluationAgent:
    def __init__(self):
        self.is_mock = False
        try:
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
            self.eval_llm = self.llm.with_structured_output(MatchEvaluation)
        except Exception:
            self.is_mock = True
        
    def evaluate_match(self, job_description: str, master_resume_json: Dict[str, Any]) -> MatchEvaluation:
        """Evaluate how well a user's resume fits a job description."""
        
        if self.is_mock:
            return MatchEvaluation(
                score=85.0,
                reasoning="Mock mode evaluation: The candidate seems like a strong fit based on the provided skills.",
                passes_threshold=True,
                missing_critical_skills=["None"]
            )
            
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert AI recruiter matching a candidate to a job. Read the candidate's resume and the job description. Score the match from 0 to 100 based on overlap in technical skills, years of experience, and responsibilities. Be strict. Only return passing if the score is 80 or above."),
            ("human", "Candidate Resume: {resume}\n\nJob Description: {job}")
        ])
        
        chain = prompt | self.eval_llm
        import json
        return chain.invoke({
            "resume": json.dumps(master_resume_json),
            "job": job_description
        })

evaluation_agent = EvaluationAgent()

import os
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- Pydantic Output Schemas ---
class ExtractedJobRequirements(BaseModel):
    required_skills: List[str] = Field(description="Hard skills required for the job")
    preferred_skills: List[str] = Field(description="Nice-to-have hard skills")
    soft_skills: List[str] = Field(description="Soft skills and behavioral traits desired")
    years_of_experience: Optional[int] = Field(description="Minimum years of experience required, if stated")
    education_level: Optional[str] = Field(description="Required education degree, if stated")
    ats_keywords: List[str] = Field(description="High-frequency keywords critical for ATS parsing")

class TailoredResumeSection(BaseModel):
    title: str = Field(description="Job title or project name")
    company: Optional[str] = Field(description="Company name, if applicable")
    date_range: Optional[str] = Field(description="Dates of employment/project")
    bullets: List[str] = Field(description="3-5 action-oriented bullet points tailored to the job description, emphasizing relevant keywords without stuffing")

class TailoredResume(BaseModel):
    summary: str = Field(description="A powerful 2-3 sentence professional summary tailored to the role")
    skills: List[str] = Field(description="A rearranged list of skills prioritizing those found in the job description")
    experience: List[TailoredResumeSection] = Field(description="Tailored work experience sections")
    projects: List[TailoredResumeSection] = Field(description="Tailored personal/academic project sections")

class CoverLetterOutput(BaseModel):
    content: str = Field(description="The full text of the cover letter, well-formatted with appropriate paragraphs")

class LLMService:
    def __init__(self):
        # We assume OPENAI_API_KEY is set in the environment or .env file
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        self.creative_llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        
        self.parser_llm = self.llm.with_structured_output(ExtractedJobRequirements)
        self.tailoring_llm = self.llm.with_structured_output(TailoredResume)

    def parse_job_description(self, job_description: str) -> ExtractedJobRequirements:
        """Extract structured requirements from a raw job description string."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert technical recruiter and ATS specialist. Extract the core requirements, skills, and ATS keywords from the following job description. Be precise and exhaustive."),
            ("human", "{job_description}")
        ])
        chain = prompt | self.parser_llm
        return chain.invoke({"job_description": job_description})

    def tailor_resume(self, master_resume_json: Dict[str, Any], job_requirements: ExtractedJobRequirements) -> TailoredResume:
        """Rewrite and reorder the master resume to align with the job requirements."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert career coach and resume writer. You will be provided with a candidate's master resume and the parsed requirements for a target job. Your task is to output a tailored resume. Rewrite bullet points to highlight relevant experience using the required ATS keywords naturally. Ensure facts are NOT hallucinated; only emphasize and rephrase what already exists. Maximize the ATS match score."),
            ("human", "Candidate Master Resume:\n{resume}\n\nTarget Job Requirements:\n{requirements}\n\nProduce the tailored resume:")
        ])
        chain = prompt | self.tailoring_llm
        req_str = job_requirements.model_dump_json()
        res_str = json.dumps(master_resume_json)
        return chain.invoke({"resume": res_str, "requirements": req_str})

    def generate_cover_letter(self, master_resume_json: Dict[str, Any], job_description: str, company_name: str, role_title: str) -> str:
        """Generate a personalized, modern cover letter."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert executive communicator. Write a concise, modern, and compelling cover letter. Avoid robotic or overly formal 'AI' language (e.g., 'I am writing to express my interest'). Start strong, align the candidate's top 2 achievements with the company's needs, and close with a clear call to action. Keep it under 300 words."),
            ("human", "Company: {company}\nRole: {role}\nJob Description: {jd}\nCandidate Info: {resume}\n\nWrite the cover letter text:")
        ])
        chain = prompt | self.creative_llm | StrOutputParser()
        return chain.invoke({
            "company": company_name,
            "role": role_title,
            "jd": job_description,
            "resume": json.dumps(master_resume_json)
        })

llm_service = LLMService()

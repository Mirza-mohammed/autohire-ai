import os
import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

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
        self.is_mock = False
        try:
            # Try to initialize OpenAI if key is present
            self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
            self.creative_llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
            self.parser_llm = self.llm.with_structured_output(ExtractedJobRequirements)
            self.tailoring_llm = self.llm.with_structured_output(TailoredResume)
        except Exception as e:
            print(f"[!] Warning: OpenAI API Key not found. Running LLMService in MOCK mode.")
            self.is_mock = True

    def parse_job_description(self, job_description: str) -> ExtractedJobRequirements:
        if self.is_mock:
            return ExtractedJobRequirements(
                required_skills=["Python", "React", "Docker"],
                preferred_skills=["AWS", "Redis"],
                soft_skills=["Communication", "Teamwork"],
                years_of_experience=3,
                education_level="Bachelors",
                ats_keywords=["Python", "React", "Docker"]
            )
        """Extract structured requirements from a raw job description string."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert technical recruiter and ATS specialist. Extract the core requirements, skills, and ATS keywords from the following job description. Be precise and exhaustive."),
            ("human", "{job_description}")
        ])
        chain = prompt | self.parser_llm
        return chain.invoke({"job_description": job_description})

    def tailor_resume(self, master_resume_json: Dict[str, Any], job_requirements: ExtractedJobRequirements, historical_feedback: str = "") -> TailoredResume:
        """Rewrite and reorder the master resume to align with the job requirements, using historical feedback."""
        if self.is_mock:
            return TailoredResume(
                summary="Passionate software engineer experienced with React and Python.",
                skills=["Python", "React", "Docker"],
                experience=[TailoredResumeSection(title="Software Developer", company="MockCorp", date_range="2021-Present", bullets=["Built amazing things."])],
                projects=[]
            )
        
        system_prompt = (
            "You are an expert career coach and resume writer. "
            "You will be provided with a candidate's master resume and the parsed requirements for a target job. "
            "Your task is to output a tailored resume. Rewrite bullet points to highlight relevant experience "
            "using the required ATS keywords naturally. Ensure facts are NOT hallucinated; only emphasize and rephrase what already exists. Maximize the ATS match score."
        )
        
        if historical_feedback:
            system_prompt += (
                f"\n\nIMPORTANT REINFORCEMENT FEEDBACK FROM RECENT REJECTIONS:\n"
                f"{historical_feedback}\n"
                f"You MUST adjust your tailoring strategy to address the above feedback."
            )
            
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Candidate Master Resume:\n{resume}\n\nTarget Job Requirements:\n{requirements}\n\nProduce the tailored resume:")
        ])
        chain = prompt | self.tailoring_llm
        req_str = job_requirements.model_dump_json()
        res_str = json.dumps(master_resume_json)
        return chain.invoke({"resume": res_str, "requirements": req_str})

    def parse_raw_resume(self, raw_text: str) -> dict:
        """
        Parses raw text from a PDF resume and converts it into structured Knowledge Base data.
        """
        if self.is_mock:
            return {
                "first_name": "Demo",
                "last_name": "User",
                "email": "demo@example.com",
                "skills": ["JavaScript", "Python", "TailwindCSS", "Node.js", "Docker"],
                "experience": [
                    {
                        "title": "Senior Frontend Engineer",
                        "company": "Tech Startup Inc.",
                        "dates": "Jan 2022 - Present",
                        "bullets": "Led the development of a React dashboard. Optimized rendering performance by 40%."
                    },
                    {
                        "title": "Web Developer",
                        "company": "Digital Agency",
                        "dates": "Mar 2019 - Dec 2021",
                        "bullets": "Created responsive e-commerce websites. Integrated payment gateways."
                    }
                ]
            }

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert resume parser. Extract the user's name, email, skills, and work experience from the following raw PDF text. Return it in the exact JSON schema provided."),
            ("user", "{raw_text}")
        ])

        # Define the expected schema for the UI
        class ParsedResume(BaseModel):
            first_name: str = Field(description="The user's first name")
            last_name: str = Field(description="The user's last name")
            email: str = Field(description="The user's primary email address")
            skills: List[str] = Field(description="A comprehensive list of all technical and soft skills found")
            experience: List[dict] = Field(description="A list of objects containing 'title', 'company', 'dates', and 'bullets' (a single string combining all bullet points)")

        parser = JsonOutputParser(pydantic_object=ParsedResume)
        
        chain = prompt | self.llm | parser
        
        try:
            return chain.invoke({"raw_text": raw_text})
        except Exception as e:
            print(f"Error parsing raw resume: {e}")
            return {
                "first_name": "", "last_name": "", "email": "", "skills": [], "experience": []
            }

    def generate_cover_letter(self, master_resume_json: Dict[str, Any], job_description: str, company_name: str, role_title: str) -> str:
        """Generate a personalized, modern cover letter."""
        if self.is_mock:
            return f"Dear Hiring Manager at {company_name},\n\nI am thrilled to apply for the {role_title} position. Given my background, I believe I would be an excellent fit for your team.\n\nThank you for your consideration.\n\nBest regards,\nDemo User"
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

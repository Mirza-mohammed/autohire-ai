from pydantic import BaseModel, HttpUrl, EmailStr
from typing import List, Dict, Any, Optional
from datetime import datetime

# --- Profiles ---
class ProfileBase(BaseModel):
    skills: List[str] = []
    experience: List[Dict[str, Any]] = []
    education: List[Dict[str, Any]] = []
    master_resume_json: Dict[str, Any] = {}

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: str
    user_id: str

    class Config:
        from_attributes = True

# --- Users ---
class UserBase(BaseModel):
    email: EmailStr
    preferences: Dict[str, Any] = {}

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    profile: Optional[Profile] = None

    class Config:
        from_attributes = True

# --- Job Postings ---
class JobPostingBase(BaseModel):
    title: str
    company_name: str
    description: str
    source_url: str

class JobPostingCreate(JobPostingBase):
    pass

class JobPosting(JobPostingBase):
    id: str
    extracted_reqs: Dict[str, Any] = {}
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Applications ---
class ApplicationBase(BaseModel):
    status: str = "pending_review"

class ApplicationCreate(ApplicationBase):
    job_id: str

class Application(ApplicationBase):
    id: str
    user_id: str
    job_id: str
    applied_resume: Dict[str, Any] = {}
    match_score: float
    applied_at: datetime
    job: Optional[JobPosting] = None

    class Config:
        from_attributes = True
